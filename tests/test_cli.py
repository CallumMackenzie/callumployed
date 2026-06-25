from pathlib import Path

import pytest
from typer.testing import CliRunner

from callumployed.cli import app
from callumployed.data.models import Company, ScanRun, ScanStatus
from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    RenderedPageState,
    ScoredLinkCandidate,
)

runner = CliRunner()


def _scan_payload(result: CareersPageScanResult) -> dict[str, object]:
    return {
        "scan_run": ScanRun(id=1, company_id=1, scan_status=ScanStatus.SUCCEEDED),
        "results": [result],
        "career_pages": [],
        "external_browser_port": None,
    }


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
            "--external-browser-port",
            "9222",
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


def test_companies_update_command_sets_scan_options(tmp_path: Path) -> None:
    database = tmp_path / "company-update.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)
    result = runner.invoke(
        app,
        [
            "companies",
            "update",
            "1",
            "--external-browser-port",
            "9222",
            "--career-page",
            "https://example.com/jobs",
        ],
        env=env,
    )
    show_result = runner.invoke(app, ["companies", "show", "1"], env=env)

    assert result.exit_code == 0
    assert "Updated company #1: Acme" in result.output
    assert show_result.exit_code == 0
    assert "External browser CDP port: 9222" in show_result.output
    assert "- 1: https://example.com/jobs (Main)" in show_result.output


def test_companies_update_requires_at_least_one_flag(tmp_path: Path) -> None:
    database = tmp_path / "company-empty-update.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)
    result = runner.invoke(
        app,
        ["companies", "update", "1"],
        env=env,
    )

    assert result.exit_code != 0
    assert "provide at least one of --external-browser-port" in result.output
    assert "--career-page" in result.output
    assert "--add-career-page" in result.output


def test_companies_update_label_requires_add_career_page(tmp_path: Path) -> None:
    database = tmp_path / "company-update-label.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)
    result = runner.invoke(
        app,
        ["companies", "update", "1", "--label", "Internships"],
        env=env,
    )

    assert result.exit_code != 0
    assert "use --label only when adding a careers page" in result.output


def test_companies_show_command_prints_saved_company_info(tmp_path: Path) -> None:
    database = tmp_path / "company-show.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(
        app,
        [
            "companies",
            "add",
            "Acme",
            "https://example.com/careers",
            "--notes",
            "High-priority target.",
            "--prestige-tier",
            "A",
            "--external-browser-port",
            "9222",
        ],
        env=env,
    )
    runner.invoke(
        app,
        [
            "companies",
            "update",
            "1",
            "--add-career-page",
            "https://example.com/internships",
            "--label",
            "Internships",
        ],
        env=env,
    )

    result = runner.invoke(app, ["companies", "show", "1"], env=env)

    assert result.exit_code == 0
    assert "Company #1: Acme" in result.output
    assert "Prestige tier: A" in result.output
    assert "Notes: High-priority target." in result.output
    assert "External browser CDP port: 9222" in result.output
    assert "Created:" in result.output
    assert "Updated:" in result.output
    assert "Career pages:" in result.output
    assert "- 1: https://example.com/careers (Main)" in result.output
    assert "- 2: https://example.com/internships (Internships)" in result.output


def test_companies_show_reports_missing_company(tmp_path: Path) -> None:
    database = tmp_path / "missing-company-show.sqlite3"

    result = runner.invoke(
        app,
        ["companies", "show", "999"],
        env={"CALLUMPLOYED_DATABASE_PATH": str(database)},
    )

    assert result.exit_code != 0
    assert "company not found: 999" in result.output


def test_config_external_browser_port_commands(tmp_path: Path) -> None:
    database = tmp_path / "config.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    set_result = runner.invoke(app, ["config", "set-external-browser-port", "9222"], env=env)
    show_result = runner.invoke(app, ["config", "show"], env=env)
    clear_result = runner.invoke(app, ["config", "clear-external-browser-port"], env=env)
    show_after_clear_result = runner.invoke(app, ["config", "show"], env=env)

    assert set_result.exit_code == 0
    assert "Default external browser CDP port: 9222" in set_result.output
    assert show_result.exit_code == 0
    assert "external_browser_port: 9222" in show_result.output
    assert clear_result.exit_code == 0
    assert "Default external browser CDP port cleared." in clear_result.output
    assert show_after_clear_result.exit_code == 0
    assert show_after_clear_result.output == "No app config set.\n"


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
    async def fake_scan_url(
        url: str,
    ) -> CareersPageScanResult:
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

    monkeypatch.setattr("callumployed.cli.run_scan_url", fake_scan_url)

    result = runner.invoke(app, ["scan", "url", "https://example.com/careers"])

    assert result.exit_code == 0
    assert "Scanned: https://example.com/careers" in result.output
    assert "Title: Example Careers" in result.output
    assert "Candidates scanned: 4" in result.output
    assert "Confidence: high" in result.output
    assert "[0.78] <https://example.com/jobs/backend> - Backend Engineer" in result.output


def test_scan_company_uses_saved_career_page(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_run_scan_company(
        company: Company,
        *,
        default_external_browser_port: int | None,
    ) -> dict[str, object]:
        assert default_external_browser_port is None
        assert company.external_browser_port == 9222
        url = "https://example.com/careers"
        result = CareersPageScanResult(
            source_url=url,
            final_url=url,
            candidates=[
                ScoredLinkCandidate(
                    url="https://example.com/jobs/backend",
                    source_url=url,
                    text="Backend Engineer",
                    confidence=0.78,
                    reasons=["job-like URL path"],
                ),
                ScoredLinkCandidate(
                    url="https://example.com/about",
                    source_url=url,
                    text="About",
                    confidence=0.0,
                    reasons=[],
                ),
            ],
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
            candidates_scanned=0,
            confidence=ExtractionConfidence.LOW,
        )
        return _scan_payload(result)

    database = tmp_path / "scan-company.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr(
        "callumployed.cli.run_scan_company",
        fake_run_scan_company,
    )
    runner.invoke(
        app,
        [
            "companies",
            "add",
            "Acme",
            "https://example.com/careers",
            "--external-browser-port",
            "9222",
        ],
        env=env,
    )

    result = runner.invoke(app, ["scan", "company", "1"], env=env)

    assert result.exit_code == 0
    assert "Scanning Acme: 1 careers page(s)" in result.output
    assert "Scan run #1" in result.output
    assert "External browser CDP port: 9222 (company)" in result.output
    assert "Scanning URL: https://example.com/careers" in result.output
    assert "[0.78] <https://example.com/jobs/backend> - Backend Engineer" in result.output


def test_scan_company_rejects_removed_agent_flag(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_run_scan_company(
        company: Company,
        *,
        default_external_browser_port: int | None,
    ) -> dict[str, object]:
        assert company.name == "Acme"
        assert default_external_browser_port is None
        result = CareersPageScanResult(
            source_url="https://example.com/careers",
            final_url="https://example.com/careers",
            candidates_scanned=0,
            confidence=ExtractionConfidence.LOW,
        )
        return _scan_payload(result)

    database = tmp_path / "scan-company-agent.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr("callumployed.cli.run_scan_company", fake_run_scan_company)

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)
    result = runner.invoke(app, ["scan", "company", "1", "--agent"], env=env)

    assert result.exit_code != 0
    assert "No such option: --agent" in result.output


def test_scan_company_calls_service_with_company_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    company_names: list[str] = []

    async def fake_run_scan_company(
        company: Company,
        *,
        default_external_browser_port: int | None,
    ) -> dict[str, object]:
        assert default_external_browser_port is None
        company_names.append(company.name)
        result = CareersPageScanResult(
            source_url="https://example.com/careers",
            final_url="https://example.com/careers",
            candidates_scanned=0,
            confidence=ExtractionConfidence.LOW,
        )
        return _scan_payload(result)

    database = tmp_path / "scan-company-context.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr("callumployed.cli.run_scan_company", fake_run_scan_company)
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)

    result = runner.invoke(app, ["scan", "company", "1"], env=env)

    assert result.exit_code == 0
    assert company_names == ["Acme"]


def test_scan_company_uses_default_external_browser_port(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scanned_external_browser_ports: list[int | None] = []

    async def fake_run_scan_company(
        company: Company,
        *,
        default_external_browser_port: int | None,
    ) -> dict[str, object]:
        assert company.name == "Acme"
        scanned_external_browser_ports.append(default_external_browser_port)
        result = CareersPageScanResult(
            source_url="https://example.com/careers",
            final_url="https://example.com/careers",
            candidates_scanned=0,
            confidence=ExtractionConfidence.LOW,
        )
        return _scan_payload(result)

    database = tmp_path / "scan-company-default-browser.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr("callumployed.cli.run_scan_company", fake_run_scan_company)

    runner.invoke(app, ["config", "set-external-browser-port", "9222"], env=env)
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)
    result = runner.invoke(app, ["scan", "company", "1"], env=env)

    assert result.exit_code == 0
    assert scanned_external_browser_ports == [9222]
    assert "External browser CDP port: 9222 (app default)" in result.output


def test_scan_all_scans_saved_companies_sequentially(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scanned: list[tuple[str, int | None]] = []

    async def fake_run_scan_company(
        company: Company,
        *,
        default_external_browser_port: int | None,
    ) -> dict[str, object]:
        external_browser_port = company.external_browser_port or default_external_browser_port
        url = (
            "https://example.com/careers"
            if company.name == "Acme"
            else "https://beta.example.com/careers"
        )
        scanned.append((url, external_browser_port))
        result = CareersPageScanResult(
            source_url=url,
            final_url=url,
            candidates_scanned=0,
            confidence=ExtractionConfidence.LOW,
        )
        return _scan_payload(result)

    database = tmp_path / "scan-all.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr("callumployed.cli.run_scan_company", fake_run_scan_company)

    runner.invoke(app, ["config", "set-external-browser-port", "9222"], env=env)
    runner.invoke(app, ["companies", "add", "Beta", "https://beta.example.com/careers"], env=env)
    runner.invoke(
        app,
        [
            "companies",
            "add",
            "Acme",
            "https://example.com/careers",
            "--external-browser-port",
            "9333",
        ],
        env=env,
    )
    result = runner.invoke(app, ["scan", "all"], env=env)

    assert result.exit_code == 0
    assert scanned == [
        ("https://example.com/careers", 9333),
        ("https://beta.example.com/careers", 9222),
    ]
    assert "Scanning all companies: 2 total" in result.output
    assert "--- Acme (#2) ---" in result.output
    assert "--- Beta (#1) ---" in result.output
    assert "Scan all complete: 2 succeeded, 0 failed, 0 skipped" in result.output


def test_scan_history_and_show_optionally_includes_link_candidates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
    ) -> RenderedPageState:
        assert external_browser_port is None
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Example Careers",
            html="""
            <a href="/jobs/software-engineering-intern-12345">
              Software Engineering Intern
            </a>
            <a href="/about">About</a>
            """,
        )

    database = tmp_path / "scan-history.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr(
        "callumployed.services.scan_workflow.render_careers_page",
        fake_render_careers_page,
    )

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)
    scan_result = runner.invoke(app, ["scan", "company", "1"], env=env)
    history_result = runner.invoke(app, ["scan", "history"], env=env)
    show_result = runner.invoke(app, ["scan", "show", "1"], env=env)
    show_candidates_result = runner.invoke(
        app,
        ["scan", "show", "1", "--candidates", "1"],
        env=env,
    )

    assert scan_result.exit_code == 0
    assert history_result.exit_code == 0
    assert "1: [succeeded] Acme (#1)" in history_result.output
    assert show_result.exit_code == 0
    assert "Scan run #1: Acme [succeeded]" in show_result.output
    assert "Role pages visited: 1" in show_result.output
    assert "Page #1: https://example.com/careers" in show_result.output
    assert "Candidates scanned: 2" in show_result.output
    assert "Candidates taken: 1" in show_result.output
    assert "URL: <https://example.com/jobs/software-engineering-intern-12345>" not in (
        show_result.output
    )
    assert "- [0.00] URL: <https://example.com/about>" not in show_result.output
    assert show_candidates_result.exit_code == 0
    assert "Candidates taken: 1" in show_candidates_result.output
    assert "Link candidates:" in show_candidates_result.output
    assert "* [" in show_candidates_result.output
    assert "URL: <https://example.com/jobs/software-engineering-intern-12345>" in (
        show_candidates_result.output
    )
    assert "Text: Software Engineering Intern" in show_candidates_result.output
    assert "Reasons: job-like URL path; numeric job id;" in show_candidates_result.output
    assert "Visit: succeeded" in show_candidates_result.output
    assert (
        "Final URL: https://example.com/jobs/software-engineering-intern-12345"
        in show_candidates_result.output
    )
    assert "Page title: Example Careers" in show_candidates_result.output
    assert "- [0.00] URL: <https://example.com/about>" not in show_candidates_result.output


def test_company_career_page_commands_and_scan_multiple_pages(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scanned_urls: list[str] = []

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
    ) -> RenderedPageState:
        assert external_browser_port is None
        scanned_urls.append(url)
        return RenderedPageState(
            url=url,
            final_url=url,
            html="",
        )

    database = tmp_path / "career-pages.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr(
        "callumployed.services.scan_workflow.render_careers_page",
        fake_render_careers_page,
    )

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/main"], env=env)
    add_page_result = runner.invoke(
        app,
        [
            "companies",
            "update",
            "1",
            "--add-career-page",
            "https://example.com/internships",
            "--label",
            "Internships",
        ],
        env=env,
    )
    scan_result = runner.invoke(app, ["scan", "company", "1"], env=env)

    assert add_page_result.exit_code == 0
    assert "Updated company #1: Acme" in add_page_result.output
    assert scan_result.exit_code == 0
    assert scanned_urls == ["https://example.com/main", "https://example.com/internships"]
    assert "Scanning Acme: 2 careers page(s)" in scan_result.output


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
