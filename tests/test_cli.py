from collections.abc import Awaitable, Callable, Mapping
from pathlib import Path

import pytest
from typer.testing import CliRunner

from callumployed import cli as cli_module
from callumployed.central.config import DEFAULT_CENTRAL_API_URL
from callumployed.cli import app
from callumployed.data.models import (
    Company,
    Role,
    RoleDiscoveryAttempt,
    RoleDiscoveryStatus,
    ScanRun,
    ScanStatus,
)
from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    RenderedPageState,
    RolePageAssessment,
    ScoredLinkCandidate,
)
from callumployed.webscraping.profile_manager import BrowserProfileManager

runner = CliRunner()


def _scan_payload(
    result: CareersPageScanResult,
    role_discovery_attempts: list[RoleDiscoveryAttempt] | None = None,
) -> dict[str, object]:
    return {
        "scan_run": ScanRun(id=1, company_id=1, scan_status=ScanStatus.SUCCEEDED),
        "results": [result],
        "career_pages": [],
        "role_discovery_attempts": role_discovery_attempts or [],
    }


def test_update_command_runs_remote_installer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "update.sqlite3"
    calls: list[tuple[list[str], bool]] = []

    def fake_run(args: list[str], *, check: bool) -> None:
        calls.append((args, check))

    monkeypatch.setattr(cli_module.subprocess, "run", fake_run)

    result = runner.invoke(
        app,
        ["update"],
        env={"CALLUMPLOYED_DATABASE_PATH": str(database)},
    )

    assert result.exit_code == 0
    assert calls == [
        (
            [
                "bash",
                "-c",
                (
                    "curl -fsSL "
                    "https://raw.githubusercontent.com/CallumMackenzie/callumployed/"
                    "master/scripts/install.sh | bash"
                ),
            ],
            True,
        )
    ]


class PassthroughProfileManager:
    async def render(
        self,
        render: Callable[..., Awaitable[RenderedPageState]],
        url: str,
        *,
        render_options: Mapping[str, object] | None = None,
    ) -> RenderedPageState:
        return await render(url, **(render_options or {}))


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
    assert (
        "1: Acme - Software Engineer <https://example.com/jobs/1> - Vancouver"
        in list_result.output
    )


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
    status_query_result = runner.invoke(app, ["roles", "list", "--query", "interested"], env=env)
    company_result = runner.invoke(app, ["roles", "list", "--company-id", "2"], env=env)
    company_text_result = runner.invoke(app, ["roles", "list", "--company", "acm"], env=env)
    title_result = runner.invoke(app, ["roles", "list", "--title", "backend"], env=env)
    link_result = runner.invoke(app, ["roles", "list", "--link", "designer"], env=env)
    location_result = runner.invoke(app, ["roles", "list", "--location", "vancouver"], env=env)
    empty_result = runner.invoke(app, ["roles", "list", "--location", "Montreal"], env=env)

    assert interested_result.exit_code == 0
    assert "Acme - Backend Engineer" in interested_result.output
    assert "Beta - Product Designer" not in interested_result.output
    assert search_result.exit_code == 0
    assert "Beta - Product Designer" in search_result.output
    assert "Acme - Backend Engineer" not in search_result.output
    assert status_query_result.exit_code == 0
    assert "Acme - Backend Engineer" in status_query_result.output
    assert "Beta - Product Designer" not in status_query_result.output
    assert company_result.exit_code == 0
    assert "Beta - Product Designer" in company_result.output
    assert "Acme - Backend Engineer" not in company_result.output
    assert company_text_result.exit_code == 0
    assert "Acme - Backend Engineer" in company_text_result.output
    assert "Beta - Product Designer" not in company_text_result.output
    assert title_result.exit_code == 0
    assert "Acme - Backend Engineer" in title_result.output
    assert "Beta - Product Designer" not in title_result.output
    assert link_result.exit_code == 0
    assert "Beta - Product Designer" in link_result.output
    assert "Acme - Backend Engineer" not in link_result.output
    assert location_result.exit_code == 0
    assert "Acme - Backend Engineer" in location_result.output
    assert "Beta - Product Designer" not in location_result.output
    assert empty_result.exit_code == 0
    assert empty_result.output == "No roles found.\n"


def test_stats_command_counts_companies_jobs_and_applications(tmp_path: Path) -> None:
    database = tmp_path / "stats.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(app, ["companies", "add", "Beta", "https://beta.example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    runner.invoke(
        app,
        ["roles", "add", "2", "Product Designer", "https://beta.example.com/jobs/designer"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "applied"], env=env)

    result = runner.invoke(app, ["stats"], env=env)

    assert result.exit_code == 0
    assert "Companies: 2" in result.output
    assert "Jobs: 2" in result.output
    assert "Applications: 1" in result.output
    assert "- discovered: 1" in result.output
    assert "- applied: 1" in result.output
    assert "- interview: 0" in result.output


def test_materials_commands_store_resume_and_cover_letter_examples(tmp_path: Path) -> None:
    database = tmp_path / "materials.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    resume_path = tmp_path / "master.tex"
    first_cover_path = tmp_path / "apple-cover.tex"
    second_cover_path = tmp_path / "stripe-cover.md"
    resume_path.write_text("\\documentclass{article}")
    first_cover_path.write_text("Dear Apple,")
    second_cover_path.write_text("Dear Stripe,")

    resume_result = runner.invoke(
        app,
        ["materials", "set-master-resume", str(resume_path)],
        env=env,
    )
    examples_result = runner.invoke(
        app,
        [
            "materials",
            "add-cover-letter-example",
            str(first_cover_path),
            str(second_cover_path),
        ],
        env=env,
    )
    show_result = runner.invoke(app, ["materials", "show"], env=env)

    assert resume_result.exit_code == 0
    assert "Stored master resume: master.tex" in resume_result.output
    assert examples_result.exit_code == 0
    assert "Stored 2 cover letter examples: apple-cover.tex, stripe-cover.md" in (
        examples_result.output
    )
    assert show_result.exit_code == 0
    assert "Master resume: master.tex" in show_result.output
    assert "Cover letter examples: 2" in show_result.output
    assert "stripe-cover.md" in show_result.output


def test_materials_set_master_resume_rejects_non_tex_file(tmp_path: Path) -> None:
    database = tmp_path / "materials-reject.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    resume_path = tmp_path / "resume.txt"
    resume_path.write_text("not tex")

    result = runner.invoke(
        app,
        ["materials", "set-master-resume", str(resume_path)],
        env=env,
    )

    assert result.exit_code != 0
    assert "master resume must be a .tex file" in result.output


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
            "--career-page",
            "https://example.com/jobs",
        ],
        env=env,
    )
    show_result = runner.invoke(app, ["companies", "show", "1"], env=env)

    assert result.exit_code == 0
    assert "Updated company #1: Acme" in result.output
    assert show_result.exit_code == 0
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
    assert "provide at least one of --career-page or --add-career-page" in result.output
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
    assert "Prestige tier: 1" in result.output
    assert "Notes: High-priority target." in result.output
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


def test_config_show_prints_defaults(tmp_path: Path) -> None:
    database = tmp_path / "config.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    show_result = runner.invoke(app, ["config", "show"], env=env)

    assert show_result.exit_code == 0
    assert "No app config set." in show_result.output
    assert "applicant_first_name:  (default)" in show_result.output
    assert "scan_headless: false (default)" in show_result.output
    assert "include_graduate_degree_roles: false (default)" in show_result.output
    assert "scan_schedule_time: 04:30 (default)" in show_result.output


def test_config_set_and_scan_use_persisted_headless_setting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "config-set-scan.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    observed_headless: list[bool] = []

    async def fake_scan_url(
        url: str,
        *,
        browser_profile_manager: object,
    ) -> CareersPageScanResult:
        observed_headless.append(bool(browser_profile_manager.headless))
        return CareersPageScanResult(
            source_url=url,
            final_url=url,
            title="Careers",
            candidates_scanned=0,
            confidence=ExtractionConfidence.HIGH,
            links=[],
        )

    monkeypatch.setattr(cli_module, "run_scan_url", fake_scan_url)

    save_result = runner.invoke(app, ["config", "set", "scan_headless", "false"], env=env)
    scan_result = runner.invoke(app, ["scan", "url", "https://example.com"], env=env)

    assert save_result.exit_code == 0
    assert save_result.output == "scan_headless: false\n"
    assert scan_result.exit_code == 0
    assert observed_headless == [False]


def test_config_scan_schedule_commands(tmp_path: Path) -> None:
    database = tmp_path / "config-scan-schedule.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    enable_result = runner.invoke(app, ["config", "enable-scan-schedule"], env=env)
    time_result = runner.invoke(
        app, ["config", "set-scan-schedule-time", "06:15"], env=env
    )
    show_result = runner.invoke(app, ["config", "show"], env=env)
    invalid_result = runner.invoke(
        app, ["config", "set-scan-schedule-time", "25:00"], env=env
    )
    disable_result = runner.invoke(app, ["config", "disable-scan-schedule"], env=env)

    assert enable_result.exit_code == 0
    assert time_result.exit_code == 0
    assert "scan_schedule_enabled: true" in show_result.output
    assert "scan_schedule_time: 06:15" in show_result.output
    assert invalid_result.exit_code != 0
    assert disable_result.exit_code == 0


def test_central_configure_can_save_passkey_without_api_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "central-configure.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    saved_passkey: dict[str, str | None] = {"value": None}
    monkeypatch.setattr(
        cli_module,
        "set_central_passkey",
        lambda passkey: saved_passkey.update({"value": passkey}),
    )
    monkeypatch.setattr(cli_module, "get_central_passkey", lambda: saved_passkey["value"])

    configure_result = runner.invoke(
        app,
        ["central", "configure", "--prompt-passkey"],
        input="secret-passkey\n",
        env=env,
    )
    status_result = runner.invoke(app, ["central", "status"], env=env)

    assert configure_result.exit_code == 0
    assert "Central store configured." in configure_result.output
    assert saved_passkey["value"] == "secret-passkey"
    assert status_result.exit_code == 0
    assert f"api_url: {DEFAULT_CENTRAL_API_URL}" in status_result.output
    assert "passkey: configured" in status_result.output


def test_browser_profiles_command_lists_internal_profiles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    template = tmp_path / "template"
    template.mkdir()
    manager_root = tmp_path / "manager"
    monkeypatch.setattr(
        "callumployed.cli.BrowserProfileManager",
        lambda: BrowserProfileManager(root=manager_root),
    )

    manager = BrowserProfileManager(root=manager_root)
    manager.ensure_default_pool(
        template_path=template,
        size=2,
        browser_executable="/tmp/brave",
    )

    list_result = runner.invoke(app, ["browser", "profiles"])

    assert list_result.exit_code == 0
    assert "default-001: available" in list_result.output
    assert "default-002: available" in list_result.output


def test_browser_config_command_reports_key_without_printing_secret() -> None:
    result = runner.invoke(
        app,
        ["browser", "config"],
        env={
            "CALLUMPLOYED_BROWSER_BACKEND": "browserbase",
            "BROWSERBASE_API_KEY": "test-secret",
        },
    )

    assert result.exit_code == 0
    assert "backend: browserbase" in result.output
    assert "browserbase_api_key: configured" in result.output
    assert "test-secret" not in result.output


def test_config_graduate_degree_role_filter_commands(tmp_path: Path) -> None:
    database = tmp_path / "config-graduate-roles.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    default_result = runner.invoke(app, ["config", "show"], env=env)
    include_result = runner.invoke(app, ["config", "include-graduate-degree-roles"], env=env)
    show_include_result = runner.invoke(app, ["config", "show"], env=env)
    exclude_result = runner.invoke(app, ["config", "exclude-graduate-degree-roles"], env=env)
    show_exclude_result = runner.invoke(app, ["config", "show"], env=env)

    assert default_result.exit_code == 0
    assert "include_graduate_degree_roles: false (default)" in default_result.output
    assert include_result.exit_code == 0
    assert "Graduate-degree role tracking enabled." in include_result.output
    assert show_include_result.exit_code == 0
    assert "include_graduate_degree_roles: true" in show_include_result.output
    assert exclude_result.exit_code == 0
    assert "Graduate-degree role tracking disabled." in exclude_result.output
    assert show_exclude_result.exit_code == 0
    assert "include_graduate_degree_roles: false" in show_exclude_result.output


def test_config_hardware_role_filter_commands(tmp_path: Path) -> None:
    database = tmp_path / "config-hardware-roles.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    default_result = runner.invoke(app, ["config", "show"], env=env)
    include_result = runner.invoke(app, ["config", "include-hardware-roles"], env=env)
    show_include_result = runner.invoke(app, ["config", "show"], env=env)
    exclude_result = runner.invoke(app, ["config", "exclude-hardware-roles"], env=env)
    show_exclude_result = runner.invoke(app, ["config", "show"], env=env)

    assert default_result.exit_code == 0
    assert "include_hardware_roles: false (default)" in default_result.output
    assert include_result.exit_code == 0
    assert "Hardware role tracking enabled." in include_result.output
    assert show_include_result.exit_code == 0
    assert "include_hardware_roles: true" in show_include_result.output
    assert exclude_result.exit_code == 0
    assert "Hardware role tracking disabled." in exclude_result.output
    assert show_exclude_result.exit_code == 0
    assert "include_hardware_roles: false" in show_exclude_result.output


def test_config_software_keyword_requirement_commands(tmp_path: Path) -> None:
    database = tmp_path / "config-software-keywords.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    default_result = runner.invoke(app, ["config", "show"], env=env)
    allow_result = runner.invoke(app, ["config", "allow-non-software-keywords"], env=env)
    show_allow_result = runner.invoke(app, ["config", "show"], env=env)
    require_result = runner.invoke(app, ["config", "require-software-keywords"], env=env)
    show_require_result = runner.invoke(app, ["config", "show"], env=env)

    assert default_result.exit_code == 0
    assert "require_software_keywords: true (default)" in default_result.output
    assert allow_result.exit_code == 0
    assert "Software keyword requirement disabled." in allow_result.output
    assert show_allow_result.exit_code == 0
    assert "require_software_keywords: false" in show_allow_result.output
    assert require_result.exit_code == 0
    assert "Software keyword requirement enabled." in require_result.output
    assert show_require_result.exit_code == 0
    assert "require_software_keywords: true" in show_require_result.output


def test_config_internship_mode_commands(tmp_path: Path) -> None:
    database = tmp_path / "config-internship-mode.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    default_result = runner.invoke(app, ["config", "show"], env=env)
    disable_result = runner.invoke(app, ["config", "disable-internship-mode"], env=env)
    show_disabled_result = runner.invoke(app, ["config", "show"], env=env)
    enable_result = runner.invoke(app, ["config", "enable-internship-mode"], env=env)
    show_enabled_result = runner.invoke(app, ["config", "show"], env=env)

    assert default_result.exit_code == 0
    assert "internship_mode: true (default)" in default_result.output
    assert disable_result.exit_code == 0
    assert "Internship mode disabled." in disable_result.output
    assert show_disabled_result.exit_code == 0
    assert "internship_mode: false" in show_disabled_result.output
    assert enable_result.exit_code == 0
    assert "Internship mode enabled." in enable_result.output
    assert show_enabled_result.exit_code == 0
    assert "internship_mode: true" in show_enabled_result.output


def test_config_location_filter_command(tmp_path: Path) -> None:
    database = tmp_path / "config-location-filter.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    default_result = runner.invoke(app, ["config", "show"], env=env)
    set_result = runner.invoke(
        app,
        ["config", "set-location-filter", "north-america"],
        env=env,
    )
    show_result = runner.invoke(app, ["config", "show"], env=env)
    invalid_result = runner.invoke(
        app,
        ["config", "set-location-filter", "mars"],
        env=env,
    )

    assert default_result.exit_code == 0
    assert "location_filter: all (default)" in default_result.output
    assert set_result.exit_code == 0
    assert "Location filter set to north_america." in set_result.output
    assert show_result.exit_code == 0
    assert "location_filter: north_america" in show_result.output
    assert invalid_result.exit_code != 0
    assert "location_filter must be one of" in invalid_result.output


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


def test_roles_rescan_command_reports_refreshed_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "roles-rescan.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    async def fake_run_rescan_role(
        role_id: int,
        *,
        browser_profile_manager: object,
        update_status: bool,
    ) -> dict[str, object]:
        assert role_id == 1
        assert isinstance(browser_profile_manager, BrowserProfileManager)
        assert update_status is True
        previous_role = Role(
            id=1,
            company_id=1,
            title="Old Intern",
            role_url="https://example.com/jobs/1",
        )
        role = previous_role.model_copy(
            update={
                "title": "Software Engineering Intern",
                "location": "Vancouver",
                "posting_id": "REQ-1",
            }
        )
        return {
            "previous_role": previous_role,
            "role": role,
            "assessment": RolePageAssessment(
                is_role=True,
                is_closed=False,
                confidence=0.95,
                title="Software Engineering Intern",
                location="Vancouver",
                posting_id="REQ-1",
                extraction_method="jobposting_structured_data",
                reasons=["schema.org JobPosting structured data"],
            ),
            "final_url": "https://example.com/jobs/1",
        }

    monkeypatch.setattr("callumployed.cli.run_rescan_role", fake_run_rescan_role)

    result = runner.invoke(
        app,
        ["roles", "rescan", "1", "--update-status"],
        env=env,
    )

    assert result.exit_code == 0
    assert "Rescanned role #1: Software Engineering Intern" in result.output
    assert "Is role: True" in result.output
    assert "Confidence: 0.95" in result.output
    assert "Title: Old Intern -> Software Engineering Intern" in result.output
    assert "Location: none -> Vancouver" in result.output
    assert "Posting ID: none -> REQ-1" in result.output


def test_roles_set_status_reports_missing_role(tmp_path: Path) -> None:
    database = tmp_path / "missing-role.sqlite3"

    result = runner.invoke(
        app,
        ["roles", "set-status", "999", "interested"],
        env={"CALLUMPLOYED_DATABASE_PATH": str(database)},
    )

    assert result.exit_code != 0
    assert "role not found: 999" in result.output


def test_roles_clear_requires_two_confirmations(tmp_path: Path) -> None:
    database = tmp_path / "roles-clear.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    aborted_result = runner.invoke(app, ["roles", "clear"], input="y\nnope\n", env=env)
    list_after_abort_result = runner.invoke(app, ["roles", "list"], env=env)
    clear_result = runner.invoke(app, ["roles", "clear"], input="y\nclear roles\n", env=env)
    list_after_clear_result = runner.invoke(app, ["roles", "list"], env=env)
    companies_result = runner.invoke(app, ["companies", "list"], env=env)

    assert aborted_result.exit_code != 0
    assert "Backend Engineer" in list_after_abort_result.output
    assert clear_result.exit_code == 0
    assert "Deleted 1 role." in clear_result.output
    assert list_after_clear_result.output == "No roles found.\n"
    assert "1: Acme" in companies_result.output


def test_scan_url_command_prints_discovered_links(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_scan_url(
        url: str,
        *,
        browser_profile_manager: object,
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
        browser_profile_manager: object,
    ) -> dict[str, object]:
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
        ],
        env=env,
    )

    result = runner.invoke(app, ["scan", "company", "1"], env=env)

    assert result.exit_code == 0
    assert "Scanning Acme: 1 careers page(s)" in result.output
    assert "Scan run #1" in result.output
    assert "Scanning URL: https://example.com/careers" in result.output
    assert "[0.78] <https://example.com/jobs/backend> - Backend Engineer" in result.output
    assert "Scan summary:" in result.output
    assert "- Discovered links selected: 1" in result.output
    assert "- New roles created: 0" in result.output


def test_scan_company_prints_scan_summary_metrics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_run_scan_company(
        company: Company,
        *,
        browser_profile_manager: object,
    ) -> dict[str, object]:
        assert company.name == "Acme"
        url = "https://example.com/careers"
        result = CareersPageScanResult(
            source_url=url,
            final_url=url,
            candidates=[
                ScoredLinkCandidate(
                    url="https://example.com/jobs/new",
                    source_url=url,
                    text="Software Intern",
                    confidence=0.78,
                    reasons=["job-like URL path"],
                ),
                ScoredLinkCandidate(
                    url="https://example.com/jobs/existing",
                    source_url=url,
                    text="Existing Software Intern",
                    confidence=0.0,
                    reasons=["already in database"],
                ),
                ScoredLinkCandidate(
                    url="https://example.com/jobs/rejected",
                    source_url=url,
                    text="Rejected Software Intern",
                    confidence=0.0,
                    reasons=["already rejected as non-role"],
                ),
            ],
            links=[
                DiscoveredJobLink(
                    url="https://example.com/jobs/new",
                    source_url=url,
                    text="Software Intern",
                    confidence=0.78,
                    discovery_method="heuristic",
                    reasons=["job-like URL path"],
                )
            ],
            candidates_scanned=3,
            confidence=ExtractionConfidence.LOW,
        )
        attempts = [
            RoleDiscoveryAttempt(
                scan_run_id=1,
                scan_candidate_id=1,
                company_id=1,
                role_id=10,
                url="https://example.com/jobs/new",
                assessment_is_role=True,
                status=RoleDiscoveryStatus.SUCCEEDED,
            ),
            RoleDiscoveryAttempt(
                scan_run_id=1,
                scan_candidate_id=2,
                company_id=1,
                url="https://example.com/jobs/false-positive",
                assessment_is_role=False,
                status=RoleDiscoveryStatus.SUCCEEDED,
            ),
            RoleDiscoveryAttempt(
                scan_run_id=1,
                scan_candidate_id=3,
                company_id=1,
                url="https://example.com/jobs/error",
                status=RoleDiscoveryStatus.FAILED,
            ),
        ]
        return _scan_payload(result, attempts)

    database = tmp_path / "scan-company-summary.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr("callumployed.cli.run_scan_company", fake_run_scan_company)
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)

    result = runner.invoke(app, ["scan", "company", "1"], env=env)

    assert result.exit_code == 0
    assert "- Candidates scanned: 3" in result.output
    assert "- Discovered links selected: 1" in result.output
    assert "- Skipped existing roles: 1" in result.output
    assert "- Skipped previously rejected: 1" in result.output
    assert "- Role pages visited: 3" in result.output
    assert "- New roles created: 1" in result.output
    assert "- Rejected after visit: 1" in result.output
    assert "- Visit failures: 1" in result.output


def test_scan_company_rejects_removed_agent_flag(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_run_scan_company(
        company: Company,
        *,
        browser_profile_manager: object,
    ) -> dict[str, object]:
        assert company.name == "Acme"
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
        browser_profile_manager: object,
    ) -> dict[str, object]:
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


def test_scan_company_can_retry_rejected_roles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    retry_values: list[bool] = []

    async def fake_run_scan_company(
        company: Company,
        *,
        browser_profile_manager: object,
        retry_rejected_roles: bool = False,
    ) -> dict[str, object]:
        assert company.name == "Acme"
        retry_values.append(retry_rejected_roles)
        result = CareersPageScanResult(
            source_url="https://example.com/careers",
            final_url="https://example.com/careers",
            candidates_scanned=0,
            confidence=ExtractionConfidence.LOW,
        )
        return _scan_payload(result)

    database = tmp_path / "scan-company-retry-rejected.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr("callumployed.cli.run_scan_company", fake_run_scan_company)
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com/careers"], env=env)

    result = runner.invoke(app, ["scan", "company", "1", "--retry-rejected-roles"], env=env)

    assert result.exit_code == 0
    assert retry_values == [True]


def test_scan_company_uses_managed_browser_profiles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scanned_profile_managers: list[object] = []

    async def fake_run_scan_company(
        company: Company,
        *,
        browser_profile_manager: object,
    ) -> dict[str, object]:
        assert company.name == "Tesla"
        assert browser_profile_manager is not None
        scanned_profile_managers.append(browser_profile_manager)
        result = CareersPageScanResult(
            source_url="https://www.tesla.com/careers/search",
            final_url="https://www.tesla.com/careers/search",
            candidates_scanned=0,
            confidence=ExtractionConfidence.LOW,
        )
        return _scan_payload(result)

    database = tmp_path / "scan-company-browser-profiles.sqlite3"
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    monkeypatch.setattr("callumployed.cli.run_scan_company", fake_run_scan_company)
    runner.invoke(
        app,
        ["companies", "add", "Tesla", "https://www.tesla.com/careers/search"],
        env=env,
    )

    result = runner.invoke(app, ["scan", "company", "1"], env=env)

    assert result.exit_code == 0
    assert len(scanned_profile_managers) == 1


def test_scan_all_scans_saved_companies_sequentially(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scanned: list[str] = []

    async def fake_run_scan_company(
        company: Company,
        *,
        browser_profile_manager: object,
    ) -> dict[str, object]:
        url = (
            "https://example.com/careers"
            if company.name == "Acme"
            else "https://beta.example.com/careers"
        )
        scanned.append(url)
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

    runner.invoke(app, ["companies", "add", "Beta", "https://beta.example.com/careers"], env=env)
    runner.invoke(
        app,
        [
            "companies",
            "add",
            "Acme",
            "https://example.com/careers",
        ],
        env=env,
    )
    result = runner.invoke(app, ["scan", "all"], env=env)

    assert result.exit_code == 0
    assert scanned == [
        "https://example.com/careers",
        "https://beta.example.com/careers",
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
        **_render_options: object,
    ) -> RenderedPageState:
        assert external_browser_port is None
        if not url.endswith("/careers"):
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Example Careers",
                html="""
                <script type="application/ld+json">
                {
                  "@context": "https://schema.org",
                  "@type": "JobPosting",
                  "title": "Software Engineering Intern",
                  "description": "Software Engineering Intern Vancouver Apply now",
                  "identifier": {"value": "REQ-123"},
                  "jobLocation": {
                    "@type": "Place",
                    "address": {
                      "@type": "PostalAddress",
                      "addressLocality": "Vancouver",
                      "addressRegion": "BC",
                      "addressCountry": "CA"
                    }
                  }
                }
                </script>
                <h1>Example Careers</h1>
                """,
            )
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

    async def classify_no_ambiguous_links(*_args: object) -> list[object]:
        return []

    monkeypatch.setattr(
        "callumployed.services.scan_workflow.build_posting_link_agent_classifier",
        lambda **_kwargs: classify_no_ambiguous_links,
    )
    monkeypatch.setattr(
        "callumployed.services.scan_workflow.render_careers_page",
        fake_render_careers_page,
    )
    monkeypatch.setattr(
        "callumployed.cli.BrowserProfileManager",
        lambda: PassthroughProfileManager(),
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
    show_role_result = runner.invoke(app, ["roles", "show", "1"], env=env)

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
    assert show_role_result.exit_code == 0
    assert "Candidates taken: 1" in show_candidates_result.output
    assert "Link candidates:" in show_candidates_result.output
    assert "* [" in show_candidates_result.output
    assert "URL: <https://example.com/jobs/software-engineering-intern-12345>" in (
        show_candidates_result.output
    )
    assert "Text: Software Engineering Intern" in show_candidates_result.output
    assert "Reasons: job-like URL path; numeric job id;" in show_candidates_result.output
    assert "Visit: succeeded" in show_candidates_result.output
    assert "Role ID:" in show_candidates_result.output
    assert "Is role: True" in show_candidates_result.output
    assert "Is closed: False" in show_candidates_result.output
    assert "Assessment confidence:" in show_candidates_result.output
    assert "Extraction method:" in show_candidates_result.output
    assert "Excerpt:" in show_candidates_result.output
    assert (
        "Final URL: https://example.com/jobs/software-engineering-intern-12345"
        in show_candidates_result.output
    )
    assert "Page title: Software Engineering Intern" in show_candidates_result.output
    assert "- [0.00] URL: <https://example.com/about>" not in show_candidates_result.output
    assert "Location: Vancouver, BC, Canada" in show_role_result.output
    assert "Posting ID: REQ-123" in show_role_result.output
    assert "Description: Software Engineering Intern Vancouver Apply now" in show_role_result.output


def test_scan_refilter_command_reports_dry_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "callumployed.cli.refilter_collected_roles",
        lambda **_kwargs: {
            "scanned_attempts": 3,
            "changed_attempts": 1,
            "roles_created": 0,
            "roles_archived": 0,
            "protected_roles": 0,
            "dry_run": True,
            "attempts": [
                {
                    "attempt_id": 7,
                    "company_id": 1,
                    "role_id": None,
                    "url": "https://example.com/jobs/software-engineer",
                    "title": "Software Engineer",
                    "previous_is_role": False,
                    "new_is_role": True,
                    "action": "create_role",
                    "reason": None,
                }
            ],
        },
    )

    result = runner.invoke(
        app,
        ["scan", "refilter", "--scan-run-id", "1"],
        env={"CALLUMPLOYED_DATABASE_PATH": str(tmp_path / "scan-refilter.sqlite3")},
    )

    assert result.exit_code == 0
    assert "Dry run: re-filtered 3 stored attempt(s)." in result.output
    assert "Changed attempts: 1" in result.output
    assert "Roles to create: 1" in result.output
    assert "attempt #7: create_role; is_role False -> True" in result.output


def test_company_career_page_commands_and_scan_multiple_pages(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scanned_urls: list[str] = []

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
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
    monkeypatch.setattr(
        "callumployed.cli.BrowserProfileManager",
        lambda: PassthroughProfileManager(),
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
