"""MCP server for structured access to callumployed."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, cast

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from callumployed.central.client import CentralStoreClient, CentralStoreError
from callumployed.central.config import (
    get_central_api_url,
    get_central_passkey,
    set_central_api_url,
    set_central_passkey,
)
from callumployed.central.models import ResolveCompanyRequest
from callumployed.central.sync import pull_roles, resolve_unlinked_companies
from callumployed.data import db
from callumployed.data import repositories as repo
from callumployed.data.models import Company, CompanyCareerPage, Role, RoleStatus
from callumployed.services.scan_workflow import scan_company as run_scan_company
from callumployed.services.scan_workflow import scan_url as run_scan_url
from callumployed.webscraping.profile_manager import BrowserProfileManager

mcp = FastMCP("callumployed")


def _ensure_initialized() -> None:
    db.ensure_initialized()


def _to_json(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return _to_json(asdict(value))
    if isinstance(value, dict):
        return {str(key): _to_json(item) for key, item in value.items()}
    if isinstance(value, list | tuple | set):
        return [_to_json(item) for item in value]
    return value


def _to_json_object(value: Any) -> dict[str, Any]:
    dumped = _to_json(value)
    if not isinstance(dumped, dict):
        raise TypeError(f"expected JSON object, got {type(dumped).__name__}")
    return cast(dict[str, Any], dumped)


def _to_json_object_list(value: Any) -> list[dict[str, Any]]:
    dumped = _to_json(value)
    if not isinstance(dumped, list):
        raise TypeError(f"expected JSON object list, got {type(dumped).__name__}")
    return cast(list[dict[str, Any]], dumped)


def _role_status(value: str | None) -> RoleStatus | None:
    if value is None:
        return None
    try:
        return RoleStatus(value)
    except ValueError as error:
        allowed = ", ".join(status.value for status in RoleStatus)
        raise ValueError(f"invalid role status: {value}; expected one of: {allowed}") from error


def _config_payload() -> dict[str, Any]:
    _ensure_initialized()
    with db.connect() as connection:
        values = repo.list_config_values(connection)
        central = _central_status_payload(connection)
        payload = {
            "values": values,
            "include_graduate_degree_roles": repo.should_include_graduate_degree_roles(
                connection
            ),
            "include_hardware_roles": repo.should_include_hardware_roles(connection),
            "require_software_keywords": repo.should_require_software_keywords(connection),
            "internship_mode": repo.should_use_internship_mode(connection),
            "location_filter": repo.get_location_filter(connection),
            "central": central,
        }
    return payload


def _central_status_payload(connection: Any) -> dict[str, Any]:
    companies = repo.list_companies(connection, include_inactive=True)
    return {
        "api_url": get_central_api_url(connection),
        "passkey_configured": get_central_passkey() is not None,
        "companies_linked": sum(company.central_company_id is not None for company in companies),
        "companies_unlinked": sum(company.central_company_id is None for company in companies),
        "companies_needs_review": sum(
            company.central_sync_status == "needs_review" for company in companies
        ),
        "companies_failed": sum(company.central_sync_status == "failed" for company in companies),
    }


@mcp.tool()
def add_company(
    name: str,
    career_page_url: str,
    notes: str | None = None,
    prestige_tier: str | None = None,
) -> dict[str, Any]:
    """Add a target company and its initial careers page."""
    _ensure_initialized()
    with db.connect() as connection:
        company = repo.add_company(
            connection,
            Company(name=name, notes=notes, prestige_tier=prestige_tier),
        )
        if company.id is None:
            raise RuntimeError("created company did not include an id")
        career_page = repo.add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url=career_page_url, label="Main"),
        )
        _try_resolve_company_with_central_store(
            connection,
            company,
            career_page_urls=[career_page_url],
        )
        company = repo.get_company(connection, company.id)
    return {"company": _to_json(company), "career_page": _to_json(career_page)}


@mcp.tool()
def get_master_resume() -> dict[str, Any]:
    """Return the stored master resume, including content."""
    _ensure_initialized()
    with db.connect() as connection:
        resume = repo.get_master_resume(connection)
    return {"master_resume": _to_json(resume)}


@mcp.tool()
def set_master_resume(filename: str, content: str) -> dict[str, Any]:
    """Set or replace the stored master .tex resume."""
    _ensure_initialized()
    with db.connect() as connection:
        resume = repo.upsert_master_resume(
            connection,
            filename=filename,
            content=content,
        )
    return {"master_resume": _to_json(resume)}


@mcp.tool()
def list_cover_letter_examples() -> list[dict[str, Any]]:
    """List stored cover letter examples, including content."""
    _ensure_initialized()
    with db.connect() as connection:
        examples = repo.list_cover_letter_examples(connection)
    return _to_json_object_list(examples)


@mcp.tool()
def add_cover_letter_example(filename: str, content: str) -> dict[str, Any]:
    """Add a cover letter example."""
    _ensure_initialized()
    with db.connect() as connection:
        example = repo.add_cover_letter_example(
            connection,
            filename=filename,
            content=content,
        )
        examples = repo.list_cover_letter_examples(connection)
    return {
        "cover_letter_example": _to_json(example),
        "cover_letter_examples": _to_json(examples),
    }


@mcp.tool()
def update_company_career_pages(
    company_id: int,
    primary_career_page_url: str | None = None,
    add_career_page_url: str | None = None,
    add_career_page_label: str | None = None,
) -> dict[str, Any]:
    """Update a company's primary careers page or add another careers page."""
    if add_career_page_label is not None and add_career_page_url is None:
        raise ValueError("use add_career_page_label only when add_career_page_url is set")
    if primary_career_page_url is None and add_career_page_url is None:
        raise ValueError("provide primary_career_page_url or add_career_page_url")

    _ensure_initialized()
    with db.connect() as connection:
        company = repo.get_company(connection, company_id)
        updated_primary = None
        added_page = None
        if primary_career_page_url is not None:
            updated_primary = repo.set_primary_company_career_page_url(
                connection,
                company_id,
                primary_career_page_url,
            )
        if add_career_page_url is not None:
            added_page = repo.add_company_career_page(
                connection,
                CompanyCareerPage(
                    company_id=company_id,
                    url=add_career_page_url,
                    label=add_career_page_label,
                ),
            )
        sync_urls = [
            url
            for url in (primary_career_page_url, add_career_page_url)
            if url is not None
        ]
        if sync_urls:
            _try_resolve_company_with_central_store(
                connection,
                company,
                career_page_urls=sync_urls,
            )
            company = repo.get_company(connection, company_id)
        career_pages = repo.list_company_career_pages(connection, company_id)

    return {
        "company": _to_json(company),
        "updated_primary_career_page": _to_json(updated_primary),
        "added_career_page": _to_json(added_page),
        "career_pages": _to_json(career_pages),
    }


@mcp.tool()
def list_companies() -> list[dict[str, Any]]:
    """List target companies with their careers pages."""
    _ensure_initialized()
    with db.connect() as connection:
        companies = repo.list_companies(connection)
        payload = [
            {
                **_to_json_object(company),
                "career_pages": _to_json(
                    repo.list_company_career_pages(connection, company.id)
                    if company.id is not None
                    else []
                ),
            }
            for company in companies
        ]
    return payload


@mcp.tool()
def show_company(company_id: int) -> dict[str, Any]:
    """Show one target company and its careers pages."""
    _ensure_initialized()
    with db.connect() as connection:
        company = repo.get_company(connection, company_id)
        career_pages = repo.list_company_career_pages(connection, company_id)
    return {"company": _to_json(company), "career_pages": _to_json(career_pages)}


@mcp.tool()
def add_role(
    company_id: int,
    title: str,
    role_url: str,
    location: str | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    """Add a role for a target company."""
    _ensure_initialized()
    with db.connect() as connection:
        role = repo.add_role(
            connection,
            Role(
                company_id=company_id,
                title=title,
                role_url=role_url,
                location=location,
                notes=notes,
            ),
        )
    return _to_json_object(role)


@mcp.tool()
def list_roles(
    company_id: int | None = None,
    company: str | None = None,
    status: str | None = None,
    title: str | None = None,
    link: str | None = None,
    location: str | None = None,
    query: str | None = None,
) -> list[dict[str, Any]]:
    """List roles with optional filters."""
    _ensure_initialized()
    with db.connect() as connection:
        roles = repo.list_role_items(
            connection,
            company_id=company_id,
            company=company,
            role_status=_role_status(status),
            title=title,
            link=link,
            location=location,
            query=query,
        )
    return _to_json_object_list(roles)


@mcp.tool()
def show_role(role_id: int) -> dict[str, Any]:
    """Show role details and recent events."""
    _ensure_initialized()
    with db.connect() as connection:
        role = repo.get_role(connection, role_id)
        company = repo.get_company(connection, role.company_id)
        events = repo.list_role_events(connection, role_id)
    return {
        "role": _to_json(role),
        "company": _to_json(company),
        "events": _to_json(events),
    }


@mcp.tool()
def update_role(
    role_id: int,
    title: str | None = None,
    role_url: str | None = None,
    location: str | None = None,
    notes: str | None = None,
    clear_location: bool = False,
    clear_notes: bool = False,
) -> dict[str, Any]:
    """Update a tracked role."""
    if location is not None and clear_location:
        raise ValueError("use either location or clear_location, not both")
    if notes is not None and clear_notes:
        raise ValueError("use either notes or clear_notes, not both")

    _ensure_initialized()
    with db.connect() as connection:
        role = repo.update_role(
            connection,
            role_id,
            title=title,
            role_url=role_url,
            location=location,
            notes=notes,
            clear_location=clear_location,
            clear_notes=clear_notes,
        )
    return _to_json_object(role)


@mcp.tool()
def set_role_status(
    role_id: int,
    status: str,
    summary: str = "Status updated via MCP.",
) -> dict[str, Any]:
    """Update a role status and record a manual event."""
    _ensure_initialized()
    with db.connect() as connection:
        role = repo.set_role_status(
            connection,
            role_id,
            _role_status(status) or RoleStatus.DISCOVERED,
            summary=summary,
        )
    return _to_json_object(role)


@mcp.tool()
def get_stats() -> dict[str, Any]:
    """Show application and job tracking stats."""
    _ensure_initialized()
    with db.connect() as connection:
        stats = repo.get_tracking_stats(connection)
    return _to_json_object(stats)


@mcp.tool()
def show_config() -> dict[str, Any]:
    """Show app-wide configuration, including defaulted values."""
    return _config_payload()


@mcp.tool()
def update_config(
    include_graduate_degree_roles: bool | None = None,
    include_hardware_roles: bool | None = None,
    require_software_keywords: bool | None = None,
    internship_mode: bool | None = None,
    location_filter: str | None = None,
) -> dict[str, Any]:
    """Update app-wide scan filtering configuration."""
    if (
        include_graduate_degree_roles is None
        and include_hardware_roles is None
        and require_software_keywords is None
        and internship_mode is None
        and location_filter is None
    ):
        raise ValueError("provide at least one config value to update")

    _ensure_initialized()
    with db.connect() as connection:
        if include_graduate_degree_roles is not None:
            repo.set_include_graduate_degree_roles(connection, include_graduate_degree_roles)
        if include_hardware_roles is not None:
            repo.set_include_hardware_roles(connection, include_hardware_roles)
        if require_software_keywords is not None:
            repo.set_require_software_keywords(connection, require_software_keywords)
        if internship_mode is not None:
            repo.set_internship_mode(connection, internship_mode)
        if location_filter is not None:
            repo.set_location_filter(connection, location_filter)
    return _config_payload()


@mcp.tool()
def central_configure(
    api_url: str | None = None,
    passkey: str | None = None,
) -> dict[str, Any]:
    """Configure the central role store URL override and/or private-feed passkey."""
    _ensure_initialized()
    with db.connect() as connection:
        if api_url is not None:
            set_central_api_url(connection, api_url)
        if passkey is not None:
            set_central_passkey(passkey)
        status = _central_status_payload(connection)
    return status


@mcp.tool()
def central_status() -> dict[str, Any]:
    """Show central role store configuration and local company link status."""
    _ensure_initialized()
    with db.connect() as connection:
        status = _central_status_payload(connection)
    return status


@mcp.tool()
def central_resolve_companies() -> dict[str, Any]:
    """Resolve local companies without central IDs. Does not require a passkey."""
    _ensure_initialized()
    with db.connect() as connection:
        client = _central_client_from_config(connection, require_passkey=False)
        result = resolve_unlinked_companies(connection, client)
        payload = {
            "result": _to_json(result),
            "central": _central_status_payload(connection),
        }
    return payload


@mcp.tool()
def central_pull_roles() -> dict[str, Any]:
    """Pull private central roles into the local database. Requires the passkey."""
    return _central_pull_roles_payload()


def _central_pull_roles_payload() -> dict[str, Any]:
    _ensure_initialized()
    with db.connect() as connection:
        client = _central_client_from_config(connection, require_passkey=True)
        resolve_result = resolve_unlinked_companies(connection, client)
        pull_result = pull_roles(connection, client)
        payload = {
            "resolved_companies": _to_json(resolve_result),
            "pulled_roles": _to_json(pull_result),
            "central": _central_status_payload(connection),
        }
    return payload


@mcp.tool()
def central_sync() -> dict[str, Any]:
    """Resolve local companies and pull private central roles. Requires the passkey."""
    return _central_pull_roles_payload()


@mcp.tool()
async def scan_url(url: str) -> dict[str, Any]:
    """Scan a careers page URL and return discovered job links."""
    _ensure_initialized()
    result = await run_scan_url(
        url,
        browser_profile_manager=BrowserProfileManager(),
    )
    return _to_json_object(result)


@mcp.tool()
async def scan_company(company_id: int, retry_rejected_roles: bool = False) -> dict[str, Any]:
    """Scan a saved company's careers pages."""
    _ensure_initialized()
    with db.connect() as connection:
        company = repo.get_company(connection, company_id)
    result = await run_scan_company(
        company,
        browser_profile_manager=BrowserProfileManager(),
        retry_rejected_roles=retry_rejected_roles,
    )
    return {"company": _to_json(company), "scan": _to_json(result)}


@mcp.tool()
def list_scan_runs(
    company_id: int | None = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """List historical company scan runs."""
    _ensure_initialized()
    with db.connect() as connection:
        scan_runs = repo.list_scan_runs(connection, company_id=company_id, limit=limit)
    return _to_json_object_list(scan_runs)


@mcp.tool()
def show_scan_run(scan_run_id: int, candidate_limit: int = 0) -> dict[str, Any]:
    """Show a historical scan run with pages, attempts, and optional candidates."""
    if candidate_limit < 0:
        raise ValueError("candidate_limit must be non-negative")

    _ensure_initialized()
    with db.connect() as connection:
        scan_run = repo.get_scan_run(connection, scan_run_id)
        company = repo.get_company(connection, scan_run.company_id)
        pages = repo.list_scan_pages(connection, scan_run_id)
        attempts = repo.list_role_discovery_attempts(connection, scan_run_id=scan_run_id)
        attempts_by_candidate_id = {
            attempt.scan_candidate_id: attempt
            for attempt in attempts
            if attempt.scan_candidate_id is not None
        }
        page_payloads: list[dict[str, Any]] = []
        for page in pages:
            candidates: list[dict[str, Any]] = []
            selected_candidate_count = 0
            if page.id is not None:
                page_candidates = repo.list_scan_candidates(connection, page.id)
                selected_candidate_count = sum(candidate.selected for candidate in page_candidates)
                if candidate_limit > 0:
                    candidates = [
                        {
                            **_to_json_object(candidate),
                            "role_discovery_attempt": _to_json(
                                attempts_by_candidate_id.get(candidate.id)
                                if candidate.id is not None
                                else None
                            ),
                        }
                        for candidate in page_candidates[:candidate_limit]
                    ]
            page_payloads.append(
                {
                    **_to_json_object(page),
                    "selected_candidate_count": selected_candidate_count,
                    "candidates": candidates,
                }
            )

    return {
        "scan_run": _to_json(scan_run),
        "company": _to_json(company),
        "pages": page_payloads,
        "role_discovery_attempts": _to_json(attempts),
    }


def _central_client_from_config(
    connection: Any,
    *,
    require_passkey: bool,
) -> CentralStoreClient:
    api_url = get_central_api_url(connection)
    passkey = get_central_passkey()
    if api_url is None:
        raise ValueError("central API URL is not configured")
    if passkey is None and require_passkey:
        raise ValueError(
            "central passkey is not configured; run "
            "`callumployed central configure --prompt-passkey`"
        )
    return CentralStoreClient(api_url=api_url, passkey=passkey)


def _try_resolve_company_with_central_store(
    connection: Any,
    company: Company,
    *,
    career_page_urls: list[str],
) -> None:
    if company.id is None:
        return
    api_url = get_central_api_url(connection)
    if api_url is None:
        return

    client = CentralStoreClient(api_url=api_url, passkey=get_central_passkey())
    try:
        response = client.resolve_company(
            ResolveCompanyRequest(
                name=company.name,
                career_page_urls=career_page_urls,
            )
        )
    except CentralStoreError as error:
        repo.set_company_central_sync_status(
            connection,
            company.id,
            status="failed",
            error=str(error),
        )
        return

    if response.action == "needs_review" or response.global_company_id is None:
        repo.set_company_central_sync_status(connection, company.id, status="needs_review")
        return

    repo.set_company_central_link(
        connection,
        company.id,
        central_company_id=response.global_company_id,
        canonical_domain=response.canonical_domain,
        normalized_name=response.normalized_name,
    )


def main() -> None:
    """Run the callumployed MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
