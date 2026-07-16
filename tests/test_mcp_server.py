import tomllib
from pathlib import Path

import pytest

from callumployed import mcp_server


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


def test_mcp_config_tools_return_defaults_and_updates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "config.sqlite3"))

    defaults = mcp_server.show_config()
    assert defaults == {
        "values": {},
        "include_graduate_degree_roles": False,
        "include_hardware_roles": False,
        "require_software_keywords": True,
    }

    updated = mcp_server.update_config(
        include_graduate_degree_roles=True,
        require_software_keywords=False,
    )

    assert updated["include_graduate_degree_roles"] is True
    assert updated["include_hardware_roles"] is False
    assert updated["require_software_keywords"] is False
    assert updated["values"] == {
        "include_graduate_degree_roles": "true",
        "require_software_keywords": "false",
    }


def test_mcp_project_script_and_dependency_are_configured() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    assert pyproject["project"]["scripts"]["callumployed-mcp"] == (
        "callumployed.mcp_server:main"
    )
    assert "mcp>=1.27,<2" in pyproject["project"]["optional-dependencies"]["mcp"]
