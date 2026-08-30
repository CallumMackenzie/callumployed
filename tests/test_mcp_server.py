import asyncio
import tomllib
from pathlib import Path

import pytest

from callumployed import mcp_server
from callumployed.central.config import DEFAULT_CENTRAL_API_URL
from callumployed.central.models import CentralCompaniesResponse, ResolveCompanyResponse
from callumployed.config import LlmSettings


@pytest.fixture(autouse=True)
def disable_mcp_remote_company_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        mcp_server,
        "_try_resolve_company_with_central_store",
        lambda *args, **kwargs: None,
    )


def test_mcp_company_and_role_tools_return_structured_data(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "mcp.sqlite3"))

    company_payload = mcp_server.add_company(
        "Acme",
        "https://example.com/careers",
        notes="High-priority target.",
        prestige_tier="A",
    )

    assert company_payload["company"]["id"] == 1
    assert company_payload["company"]["name"] == "Acme"
    assert company_payload["career_page"]["url"] == "https://example.com/careers"

    companies = mcp_server.list_companies()
    assert companies == [
        {
            **company_payload["company"],
            "career_pages": [company_payload["career_page"]],
        }
    ]

    role = mcp_server.add_role(
        1,
        "Software Engineer",
        "https://example.com/jobs/1",
        location="Vancouver",
    )
    assert role["id"] == 1
    assert role["role_status"] == "discovered"

    discovered_roles = mcp_server.list_roles(status="discovered")
    assert discovered_roles[0]["company_name"] == "Acme"
    assert discovered_roles[0]["title"] == "Software Engineer"

    updated_role = mcp_server.set_role_status(
        1,
        "interested",
        summary="Looks worth applying to.",
    )
    assert updated_role["role_status"] == "interested"

    shown_role = mcp_server.show_role(1)
    assert shown_role["company"]["name"] == "Acme"
    assert shown_role["role"]["role_status"] == "interested"
    assert shown_role["events"][0]["event_type"] == "status_changed"


def test_mcp_stats_tool_returns_application_and_job_counts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "stats.sqlite3"))

    mcp_server.add_company("Acme", "https://example.com/careers")
    mcp_server.add_company("Beta", "https://beta.example.com/careers")
    mcp_server.add_role(1, "Backend Engineer", "https://example.com/jobs/backend")
    mcp_server.add_role(2, "Product Designer", "https://beta.example.com/jobs/designer")
    mcp_server.set_role_status(1, "applied")

    stats = mcp_server.get_stats()

    assert stats["companies_total"] == 2
    assert stats["jobs_total"] == 2
    assert stats["applications_total"] == 1
    assert stats["jobs_by_status"]["discovered"] == 1
    assert stats["jobs_by_status"]["applied"] == 1
    assert stats["applications_by_status"]["applied"] == 1


def test_mcp_material_tools_store_and_return_resume_and_cover_letters(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "materials.sqlite3"))

    empty_resume = mcp_server.get_master_resume()
    stored_resume = mcp_server.set_master_resume(
        "master.tex",
        "\\documentclass{article}",
    )
    first_example = mcp_server.add_cover_letter_example(
        "apple-cover.tex",
        "Dear Apple,",
    )
    second_example = mcp_server.add_cover_letter_example(
        "/tmp/stripe-cover.md",
        "Dear Stripe,",
    )
    examples = mcp_server.list_cover_letter_examples()

    assert empty_resume == {"master_resume": None}
    assert stored_resume["master_resume"]["filename"] == "master.tex"
    assert stored_resume["master_resume"]["content"] == "\\documentclass{article}"
    assert first_example["cover_letter_example"]["filename"] == "apple-cover.tex"
    assert second_example["cover_letter_example"]["filename"] == "stripe-cover.md"
    assert [example["filename"] for example in examples] == [
        "stripe-cover.md",
        "apple-cover.tex",
    ]
    assert examples[0]["content"] == "Dear Stripe,"


def test_mcp_config_tools_return_defaults_and_updates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "config.sqlite3"))
    monkeypatch.setattr(mcp_server, "get_central_passkey", lambda: None)

    defaults = mcp_server.show_config()
    assert defaults["values"] == {}
    assert defaults["settings"]["scan_headless"] is False
    assert defaults["settings"]["applicant_email"] == ""
    assert defaults["include_graduate_degree_roles"] is False
    assert defaults["central"] == {
        "api_url": DEFAULT_CENTRAL_API_URL,
        "passkey_configured": False,
        "companies_linked": 0,
        "companies_unlinked": 0,
        "companies_needs_review": 0,
        "companies_failed": 0,
    }

    updated = mcp_server.update_config(
        include_graduate_degree_roles=True,
        require_software_keywords=False,
        internship_mode=False,
        location_filter="canada",
    )

    assert updated["include_graduate_degree_roles"] is True
    assert updated["include_hardware_roles"] is False
    assert updated["require_software_keywords"] is False
    assert updated["internship_mode"] is False
    assert updated["location_filter"] == "canada"
    assert updated["values"] == {
        "include_graduate_degree_roles": "true",
        "internship_mode": "false",
        "location_filter": "canada",
        "require_software_keywords": "false",
    }

    profile_update = mcp_server.set_config("applicant_email", "callum@example.com")
    assert profile_update["value"] == "callum@example.com"
    assert profile_update["config"]["settings"]["applicant_email"] == "callum@example.com"


def test_mcp_scan_uses_persisted_headless_setting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "scan-config.sqlite3"))
    observed_headless: list[bool] = []
    observed_providers: list[str] = []

    async def fake_scan_url(
        url: str,
        *,
        browser_profile_manager: object,
        llm_settings: LlmSettings,
    ) -> dict[str, object]:
        observed_headless.append(bool(browser_profile_manager.headless))
        observed_providers.append(str(llm_settings.provider))
        return {"source_url": url, "links": []}

    monkeypatch.setattr(mcp_server, "run_scan_url", fake_scan_url)
    mcp_server.set_config("scan_headless", False)
    mcp_server.set_config("llm_provider", "codex")

    asyncio.run(mcp_server.scan_url("https://example.com/careers"))

    assert observed_headless == [False]
    assert observed_providers == ["codex"]


def test_mcp_central_tools_configure_resolve_and_pull(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "central.sqlite3"))
    saved_passkey: dict[str, str | None] = {"value": None}
    monkeypatch.setattr(mcp_server, "get_central_passkey", lambda: saved_passkey["value"])
    monkeypatch.setattr(
        mcp_server,
        "set_central_passkey",
        lambda passkey: saved_passkey.update({"value": passkey}),
    )

    class FakeCentralClient:
        def __init__(self, *, api_url: str, passkey: str | None = None) -> None:
            self.api_url = api_url
            self.passkey = passkey

        def resolve_company(self, request: object) -> ResolveCompanyResponse:
            return ResolveCompanyResponse(
                action="matched",
                global_company_id="co_acme",
                confidence=100,
                matched_on=["normalized_name"],
                canonical_domain="example.com",
                normalized_name="acme",
            )

        def list_roles(self) -> object:
            return type("RolesResponse", (), {"roles": []})()

        def list_companies(self) -> CentralCompaniesResponse:
            return CentralCompaniesResponse(companies=[])

    monkeypatch.setattr(mcp_server, "CentralStoreClient", FakeCentralClient)
    mcp_server.add_company("Acme", "https://example.com/careers")

    status = mcp_server.central_status()
    assert status["api_url"] == DEFAULT_CENTRAL_API_URL
    assert status["passkey_configured"] is False
    assert status["companies_unlinked"] == 1

    configured = mcp_server.central_configure(passkey="secret-passkey")
    assert configured["passkey_configured"] is True
    assert saved_passkey["value"] == "secret-passkey"

    resolved = mcp_server.central_resolve_companies()
    assert resolved["result"] == {
        "linked": 1,
        "created": 0,
        "needs_review": 0,
        "failed": 0,
    }
    assert resolved["central"]["companies_linked"] == 1

    pulled = mcp_server.central_pull_roles()
    assert pulled["pulled_companies"] == {
        "companies_created": 0,
        "companies_linked": 0,
        "companies_existing": 0,
    }
    assert pulled["pulled_roles"] == {
        "companies_created": 0,
        "roles_created": 0,
        "roles_updated": 0,
        "skipped_roles": 0,
    }


def test_mcp_project_script_and_dependency_are_configured() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    assert pyproject["project"]["scripts"]["callumployed-mcp"] == (
        "callumployed.mcp_server:main"
    )
    assert "mcp>=1.27,<2" in pyproject["project"]["optional-dependencies"]["mcp"]
