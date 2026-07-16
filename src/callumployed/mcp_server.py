"""MCP server for structured access to callumployed."""

from __future__ import annotations

from enum import Enum
from typing import Any, cast

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

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
        payload = {
            "values": values,
            "include_graduate_degree_roles": repo.should_include_graduate_degree_roles(
                connection
            ),
            "include_hardware_roles": repo.should_include_hardware_roles(connection),
            "require_software_keywords": repo.should_require_software_keywords(connection),
        }
    return payload


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
    return {"company": _to_json(company), "career_page": _to_json(career_page)}


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
def show_config() -> dict[str, Any]:
    """Show app-wide configuration, including defaulted values."""
    return _config_payload()


@mcp.tool()
def update_config(
    include_graduate_degree_roles: bool | None = None,
    include_hardware_roles: bool | None = None,
    require_software_keywords: bool | None = None,
) -> dict[str, Any]:
    """Update app-wide scan filtering configuration."""
    if (
        include_graduate_degree_roles is None
        and include_hardware_roles is None
        and require_software_keywords is None
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
    return _config_payload()


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


def main() -> None:
    """Run the callumployed MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
