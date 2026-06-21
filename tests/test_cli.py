from pathlib import Path

import pytest
from typer.testing import CliRunner

from callumployed.cli import app
from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
)

runner = CliRunner()


def test_company_and_role_commands_share_database_file(tmp_path: Path) -> None:
    database = tmp_path / "callumployed.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    company_result = runner.invoke(
        app,
        [
            "companies",
            "add",
            "Acme",
            "https://example.com/careers",
        ],
        env=env,
    )
    role_result = runner.invoke(
        app,
        [
            "roles",
            "add",
            "1",
            "Software Engineer",
            "https://example.com/jobs/1",
            "--location",
            "Vancouver",
        ],
        env=env,
    )
    status_result = runner.invoke(
        app,
        [
            "roles",
            "set-status",
            "1",
            "interested",
            "--summary",
            "Looks worth applying to.",
        ],
        env=env,
    )
    list_result = runner.invoke(app, ["roles", "list"], env=env)

    assert company_result.exit_code == 0
    assert "Added company #1: Acme" in company_result.output
    assert role_result.exit_code == 0
    assert "Added role #1: Software Engineer" in role_result.output
    assert status_result.exit_code == 0
    assert "Updated role #1: interested" in status_result.output
    assert list_result.exit_code == 0
    assert "1: [interested] Acme - Software Engineer (Vancouver)" in list_result.output


def test_roles_list_filters_by_status_and_search_query(tmp_path: Path) -> None:
    database = tmp_path / "roles-list.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(app, ["companies", "add", "Beta", "https://beta.example.com"], env=env)
    runner.invoke(
        app,
        [
            "roles",
            "add",
            "1",
            "Backend Engineer",
            "https://example.com/jobs/backend",
            "--location",
            "Vancouver",
        ],
        env=env,
    )
    runner.invoke(
        app,
        [
            "roles",
            "add",
            "2",
            "Product Designer",
            "https://beta.example.com/jobs/designer",
            "--location",
            "Toronto",
        ],
        env=env,
    )
    runner.invoke(
        app,
        ["roles", "set-status", "1", "interested", "--summary", "Worth tracking."],
        env=env,
    )

    interested_result = runner.invoke(app, ["roles", "list", "--status", "interested"], env=env)
    search_result = runner.invoke(app, ["roles", "list", "--query", "designer"], env=env)
    company_result = runner.invoke(app, ["roles", "list", "--company-id", "2"], env=env)
    location_result = runner.invoke(app, ["roles", "list", "--location", "vancouver"], env=env)
    empty_result = runner.invoke(app, ["roles", "list", "--location", "Montreal"], env=env)

    assert interested_result.exit_code == 0
    assert "Acme - Backend Engineer" in interested_result.output
    assert "Beta - Product Designer" not in interested_result.output
    assert search_result.exit_code == 0
    assert "Beta - Product Designer" in search_result.output
    assert "Acme - Backend Engineer" not in search_result.output
    assert company_result.exit_code == 0
    assert "Beta - Product Designer" in company_result.output
    assert "Acme - Backend Engineer" not in company_result.output
    assert location_result.exit_code == 0
    assert "Acme - Backend Engineer" in location_result.output
    assert "Beta - Product Designer" not in location_result.output
    assert empty_result.exit_code == 0
    assert empty_result.output == "No roles found.\n"


def test_roles_show_and_update_commands(tmp_path: Path) -> None:
    database = tmp_path / "roles-show-update.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        [
            "roles",
            "add",
            "1",
            "Software Engineer",
            "https://example.com/jobs/1",
            "--location",
            "Remote",
            "--notes",
            "Initial notes.",
        ],
        env=env,
    )
    update_result = runner.invoke(
        app,
        [
            "roles",
            "update",
            "1",
            "--title",
            "Backend Engineer",
            "--location",
            "Vancouver",
            "--notes",
            "Infra team.",
        ],
        env=env,
    )
    status_result = runner.invoke(
        app,
        ["roles", "set-status", "1", "interested", "--summary", "Worth tracking."],
        env=env,
    )
    show_result = runner.invoke(app, ["roles", "show", "1"], env=env)
    clear_result = runner.invoke(app, ["roles", "update", "1", "--clear-notes"], env=env)
    show_after_clear_result = runner.invoke(app, ["roles", "show", "1"], env=env)

    assert update_result.exit_code == 0
    assert "Updated role #1: Backend Engineer" in update_result.output
    assert status_result.exit_code == 0
    assert show_result.exit_code == 0
    assert "Role #1: Backend Engineer" in show_result.output
    assert "Company: Acme (#1)" in show_result.output
    assert "Status: interested" in show_result.output
    assert "Location: Vancouver" in show_result.output
    assert "Notes: Infra team." in show_result.output
    assert "- status_changed (discovered -> interested): Worth tracking." in show_result.output
    assert clear_result.exit_code == 0
    assert show_after_clear_result.exit_code == 0
    assert "Notes:" not in show_after_clear_result.output


def test_roles_set_status_reports_missing_role(tmp_path: Path) -> None:
    database = tmp_path / "missing-role.sqlite3"

    result = runner.invoke(
        app,
        ["roles", "set-status", "999", "interested"],
        env={"CALLUMPLOYED_DATABASE_PATH": str(database)},
    )

    assert result.exit_code != 0
    assert "role not found: 999" in result.output


def test_scan_url_command_prints_discovered_links(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_scan_careers_page(url: str) -> CareersPageScanResult:
        return CareersPageScanResult(
            source_url=url,
            final_url=url,
            title="Example Careers",
            candidates_scanned=4,
            confidence=ExtractionConfidence.HIGH,
            links=[
                DiscoveredJobLink(
                    url="https://example.com/jobs/backend",
                    source_url=url,
                    text="Backend Engineer",
                    confidence=0.78,
                    discovery_method="heuristic",
                    reasons=["job-like URL path"],
                )
            ],
        )

    monkeypatch.setattr("callumployed.cli.scan_careers_page", fake_scan_careers_page)

    result = runner.invoke(app, ["scan", "url", "https://example.com/careers"])

    assert result.exit_code == 0
    assert "Scanned: https://example.com/careers" in result.output
    assert "Title: Example Careers" in result.output
    assert "Candidates scanned: 4" in result.output
    assert "Confidence: high" in result.output
    assert "[0.78] https://example.com/jobs/backend - Backend Engineer" in result.output


def test_scan_company_uses_saved_careers_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scanned_urls: list[str] = []

    async def fake_scan_careers_page(url: str) -> CareersPageScanResult:
        scanned_urls.append(url)
        return CareersPageScanResult(
            source_url=url,
            final_url=url,
            candidates_scanned=0,
            confidence=ExtractionConfidence.LOW,
        )

    database = tmp_path / "scan-company.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr("callumployed.cli.scan_careers_page", fake_scan_careers_page)
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)

    result = runner.invoke(app, ["scan", "company", "1"], env=env)

    assert result.exit_code == 0
    assert scanned_urls == ["https://example.com/careers"]
    assert "Scanning Acme: https://example.com/careers" in result.output
    assert "No job links discovered." in result.output


def test_database_commands_and_options_are_hidden_from_help() -> None:
    result = runner.invoke(app, ["--help"])
    companies_result = runner.invoke(app, ["companies", "add", "--help"])

    assert result.exit_code == 0
    assert "init-db" not in result.output
    assert "--database" not in result.output
    assert companies_result.exit_code == 0
    assert "--database" not in companies_result.output


def test_database_initializes_on_normal_command(tmp_path: Path) -> None:
    database = tmp_path / "fresh.sqlite3"

    result = runner.invoke(
        app,
        ["companies", "list"],
        env={"CALLUMPLOYED_DATABASE_PATH": str(database)},
    )

    assert result.exit_code == 0
    assert result.output == "No companies yet.\n"
    assert database.exists()
