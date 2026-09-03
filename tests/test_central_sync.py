import json
from datetime import UTC, datetime

import httpx
import pytest

from callumployed.central.client import CentralStoreClient, CentralStoreError
from callumployed.central.config import (
    DEFAULT_CENTRAL_API_URL,
    get_central_api_url,
    set_central_api_url,
)
from callumployed.central.metrics import _rejection_reason_category, build_scan_metrics
from callumployed.central.models import (
    CentralCompaniesResponse,
    CentralCompany,
    CentralRole,
    CentralRolesResponse,
    ResolveCompanyRequest,
    ResolveCompanyResponse,
    ScanMetricsRequest,
)
from callumployed.central.sync import pull_companies, pull_roles, resolve_unlinked_companies
from callumployed.data import db
from callumployed.data.models import Company, CompanyCareerPage, Role, RoleStatus, ScanStatus
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    add_role,
    create_scan_run,
    finish_scan_run,
    get_company,
    list_companies,
    list_company_career_pages,
    list_roles,
)
from callumployed.services.autoprep import ensure_autoprep_schema


class FakeCentralClient:
    def __init__(self) -> None:
        self.resolved_names: list[str] = []

    def resolve_company(self, request: object) -> ResolveCompanyResponse:
        name = request.name
        self.resolved_names.append(name)
        return ResolveCompanyResponse(
            action="matched",
            global_company_id=f"co_{name.lower()}",
            confidence=100,
            matched_on=["normalized_name"],
            canonical_domain="example.com",
            normalized_name=name.lower(),
        )

    def list_roles(self) -> CentralRolesResponse:
        return CentralRolesResponse(
            roles=[
                CentralRole(
                    global_role_id="role_1",
                    global_company_id="co_acme",
                    company_name="Acme",
                    title="Backend Intern",
                    role_url="https://example.com/jobs/backend",
                    location="Vancouver",
                    description="Build APIs.",
                    posting_id="backend-1",
                    tier_classification="tier 1",
                    status="open",
                )
            ]
        )

    def list_companies(self) -> CentralCompaniesResponse:
        return CentralCompaniesResponse(
            companies=[
                CentralCompany(
                    global_company_id="co_acme",
                    display_name="Acme",
                    normalized_names=["acme"],
                    domains=["example.com"],
                    default_tier="1",
                    career_page_urls=["https://example.com/careers"],
                ),
                CentralCompany(
                    global_company_id="co_beta",
                    display_name="Beta",
                    normalized_names=["beta"],
                    domains=["beta.example"],
                    default_tier="2",
                    career_page_urls=["https://beta.example/careers"],
                ),
            ]
        )


class UnavailableCentralClient:
    def resolve_company(self, request: object) -> ResolveCompanyResponse:
        _ = request
        raise CentralStoreError("central store request failed: connection refused")


@pytest.mark.parametrize("tier", [str(value) for value in range(8)])
def test_resolve_company_request_accepts_company_tiers_zero_through_seven(tier: str) -> None:
    request = ResolveCompanyRequest(name="Acme", prestige_tier=tier)

    assert request.prestige_tier == tier


@pytest.mark.parametrize("tier", ["-1", "8", "A", "tier 7"])
def test_resolve_company_request_rejects_unsupported_company_tiers(tier: str) -> None:
    with pytest.raises(ValueError):
        ResolveCompanyRequest(name="Acme", prestige_tier=tier)


def test_resolve_unlinked_companies_stores_global_company_id() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    add_company_career_page(
        connection,
        CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
    )
    client = FakeCentralClient()

    result = resolve_unlinked_companies(connection, client)  # type: ignore[arg-type]

    linked = get_company(connection, company.id)
    assert result.linked == 1
    assert linked.central_company_id == "co_acme"
    assert linked.central_sync_status == "linked"
    assert linked.canonical_domain == "example.com"


def test_resolve_unlinked_companies_keeps_local_data_when_central_is_down() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    add_company_career_page(
        connection,
        CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
    )

    result = resolve_unlinked_companies(
        connection,
        UnavailableCentralClient(),  # type: ignore[arg-type]
    )

    preserved = get_company(connection, company.id)
    assert result.failed == 1
    assert preserved.name == "Acme"
    assert preserved.central_company_id is None
    assert preserved.central_sync_status == "failed"
    assert "connection refused" in (preserved.central_sync_error or "")
    assert [page.url for page in list_company_career_pages(connection, company.id)] == [
        "https://example.com/careers"
    ]


@pytest.mark.parametrize("error_type", [httpx.ConnectError, httpx.ReadTimeout])
def test_central_client_normalizes_network_outages(
    error_type: type[httpx.HTTPError],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise error_type("central unavailable", request=request)

    client = CentralStoreClient(
        api_url="https://central.example",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(CentralStoreError, match="central store request failed"):
        client.list_companies()


def test_pull_roles_imports_central_roles_without_overwriting_local_status() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(
        connection,
        Company(name="Acme", central_company_id="co_acme", central_sync_status="linked"),
    )
    client = FakeCentralClient()

    first_result = pull_roles(connection, client)  # type: ignore[arg-type]
    role = list_roles(connection)[0]

    assert first_result.roles_created == 1
    assert role.central_role_id == "role_1"
    assert role.central_source == "central"
    assert role.role_status is RoleStatus.DISCOVERED

    connection.execute(
        "UPDATE roles SET role_status = 'applied' WHERE id = ?",
        (role.id,),
    )
    connection.commit()

    second_result = pull_roles(connection, client)  # type: ignore[arg-type]
    updated_role = list_roles(connection)[0]

    assert company.id is not None
    assert second_result.roles_updated == 1
    assert updated_role.role_status is RoleStatus.APPLIED


def test_pull_companies_imports_remote_companies_and_links_existing() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    client = FakeCentralClient()

    first_result = pull_companies(connection, client)  # type: ignore[arg-type]
    companies = {company.name: company for company in list_companies(connection)}

    assert first_result.companies_created == 1
    assert first_result.companies_linked == 1
    assert first_result.companies_existing == 0
    assert companies["Acme"].central_company_id == "co_acme"
    assert companies["Acme"].central_sync_status == "linked"
    assert companies["Beta"].central_company_id == "co_beta"
    assert companies["Beta"].prestige_tier == "2"
    assert company.id is not None
    assert [
        career_page.url
        for career_page in list_company_career_pages(connection, companies["Acme"].id or 0)
    ] == ["https://example.com/careers"]
    assert [
        career_page.url
        for career_page in list_company_career_pages(connection, companies["Beta"].id or 0)
    ] == ["https://beta.example/careers"]

    second_result = pull_companies(connection, client)  # type: ignore[arg-type]

    assert second_result.companies_created == 0
    assert second_result.companies_linked == 0
    assert second_result.companies_existing == 2


def test_central_client_resolves_company_without_passkey() -> None:
    seen_headers: dict[str, str] = {}
    seen_payload: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen_headers.update(request.headers)
        seen_payload.update(json.loads(request.content))
        return httpx.Response(200, json={"global_company_id": "co_public"})

    client = CentralStoreClient(
        api_url="https://central.example",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    response = client.resolve_company(
        ResolveCompanyRequest(
            name="Acme",
            career_page_urls=["https://example.com/careers"],
            prestige_tier="7",
            tier_source_id="client-1",
        )
    )

    assert response.global_company_id == "co_public"
    assert response.action == "matched"
    assert "authorization" not in seen_headers
    assert "x-callumployed-passkey" not in seen_headers
    assert seen_payload["prestige_tier"] == "7"
    assert seen_payload["tier_source_id"] == "client-1"


def test_central_api_url_defaults_to_deployed_store(monkeypatch) -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    monkeypatch.delenv("CALLUMPLOYED_CENTRAL_API_URL", raising=False)

    assert get_central_api_url(connection) == DEFAULT_CENTRAL_API_URL

    set_central_api_url(connection, "https://central.example/")
    assert get_central_api_url(connection) == "https://central.example"

    monkeypatch.setenv("CALLUMPLOYED_CENTRAL_API_URL", "https://env.example/")
    assert get_central_api_url(connection) == "https://env.example"


def test_central_client_uses_custom_passkey_header() -> None:
    seen_headers: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen_headers.update(request.headers)
        return httpx.Response(200, json={"roles": []})

    client = CentralStoreClient(
        api_url="https://central.example",
        passkey="secret",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    assert client.list_roles().roles == []
    assert seen_headers["x-callumployed-passkey"] == "secret"
    assert "authorization" not in seen_headers


def test_central_client_submits_scan_metrics_without_passkey() -> None:
    seen_headers: dict[str, str] = {}
    seen_payload: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen_headers.update(request.headers)
        seen_payload.update(__import__("json").loads(request.content))
        return httpx.Response(
            200,
            json={"accepted": True, "scan_metric_id": "scan_metric_123"},
        )

    client = CentralStoreClient(
        api_url="https://central.example",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    response = client.submit_scan_metrics(
        ScanMetricsRequest(
            client_id="client-1",
            scan_event_id="event-1",
            company_name="Acme",
            scan_status="succeeded",
            started_at=datetime(2026, 8, 27, tzinfo=UTC),
            finished_at=datetime(2026, 8, 27, 0, 0, 1, tzinfo=UTC),
            duration_ms=1_000,
            career_pages_total=1,
            pages_scanned=1,
            candidates_scanned=4,
            potential_roles_discovered=2,
            role_verification_attempts=2,
            verified_open_roles=1,
            roles_saved=1,
            failed_role_visits=0,
            app_version="0.1.0",
        )
    )

    assert response.scan_metric_id == "scan_metric_123"
    assert seen_payload["company_name"] == "Acme"
    assert "authorization" not in seen_headers
    assert "x-callumployed-passkey" not in seen_headers


def test_build_scan_metrics_aggregates_persisted_scan_data() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(
        connection,
        Company(name="Acme", central_company_id="co_acme"),
    )
    assert company.id is not None
    outcome_roles = [
        add_role(
            connection,
            Role(
                company_id=company.id,
                title=f"{status.value} role",
                role_url=f"https://example.com/{status.value}",
                role_status=status,
            ),
        )
        for status in (
            RoleStatus.INTERESTED,
            RoleStatus.DISINTERESTED,
            RoleStatus.ARCHIVED,
            RoleStatus.APPLIED,
        )
    ]
    add_company_career_page(
        connection,
        CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
    )
    scan_run = create_scan_run(connection, company.id)
    assert scan_run.id is not None
    page_cursor = connection.execute(
        """
        INSERT INTO scan_pages (scan_run_id, source_url, final_url, candidates_scanned)
        VALUES (?, 'https://example.com/careers', 'https://example.com/careers', 4)
        """,
        (scan_run.id,),
    )
    scan_page_id = int(page_cursor.lastrowid)
    connection.execute(
        """
        INSERT INTO scan_candidates (scan_page_id, url, source_url, tag, confidence, selected)
        VALUES
            (?, 'https://example.com/1', 'https://example.com/careers', 'a', 1.0, 1),
            (?, 'https://example.com/2', 'https://example.com/careers', 'a', 0.5, 0)
        """,
        (scan_page_id, scan_page_id),
    )
    finished = finish_scan_run(connection, scan_run.id, ScanStatus.SUCCEEDED)

    ensure_autoprep_schema(connection)
    connection.executemany(
        """
        INSERT INTO autoprep_jobs (
            role_id, overall_status, worker_state, resume_status, cover_letter_status
        ) VALUES (?, ?, 'idle', ?, ?)
        """,
        [
            (outcome_roles[0].id, "ready", "ready", "ready"),
            (outcome_roles[1].id, "failed", "failed", "failed"),
        ],
    )

    metrics = build_scan_metrics(connection, company, finished)

    assert metrics.global_company_id == "co_acme"
    assert metrics.pages_scanned == 1
    assert metrics.candidates_scanned == 4
    assert metrics.potential_roles_discovered == 1
    assert metrics.scan_status == "succeeded"
    assert metrics.schema_version == 3
    assert metrics.page_confidence_counts == {"low": 1}
    assert metrics.candidate_confidence_counts == {"high": 1, "medium": 1}
    assert metrics.candidate_selection_counts == {"selected": 1, "rejected": 1}
    assert metrics.candidate_discovery_method_counts == {"unclassified": 2}
    assert metrics.agent_trace_present is False
    assert metrics.role_status_counts == {
        "applied": 1,
        "archived": 1,
        "disinterested": 1,
        "interested": 1,
    }
    assert metrics.autoprep_outcome_counts == {"failure": 1, "success": 1}


def test_scan_metric_rejection_reasons_are_privacy_safe_categories() -> None:
    assert _rejection_reason_category(None) == "unspecified"
    assert (
        _rejection_reason_category("location filtered by app config")
        == "location_filter"
    )
    assert (
        _rejection_reason_category(
            "Rejected because jane@example.com appeared in the source posting"
        )
        == "other"
    )
