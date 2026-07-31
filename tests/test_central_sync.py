import httpx

from callumployed.central.client import CentralStoreClient
from callumployed.central.config import (
    DEFAULT_CENTRAL_API_URL,
    get_central_api_url,
    set_central_api_url,
)
from callumployed.central.models import (
    CentralCompaniesResponse,
    CentralCompany,
    CentralRole,
    CentralRolesResponse,
    ResolveCompanyRequest,
    ResolveCompanyResponse,
)
from callumployed.central.sync import pull_companies, pull_roles, resolve_unlinked_companies
from callumployed.data import db
from callumployed.data.models import Company, CompanyCareerPage, RoleStatus
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    get_company,
    list_companies,
    list_company_career_pages,
    list_roles,
)


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

    def handler(request: httpx.Request) -> httpx.Response:
        seen_headers.update(request.headers)
        return httpx.Response(200, json={"global_company_id": "co_public"})

    client = CentralStoreClient(
        api_url="https://central.example",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    response = client.resolve_company(
        ResolveCompanyRequest(name="Acme", career_page_urls=["https://example.com/careers"])
    )

    assert response.global_company_id == "co_public"
    assert response.action == "matched"
    assert "authorization" not in seen_headers
    assert "x-callumployed-passkey" not in seen_headers


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
