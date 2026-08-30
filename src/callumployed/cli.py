import asyncio
import subprocess
from pathlib import Path
from typing import Annotated

import turso
import typer

from callumployed.central.client import CentralStoreClient, CentralStoreError
from callumployed.central.config import (
    get_central_api_url,
    get_central_client_id,
    get_central_passkey,
    set_central_api_url,
    set_central_passkey,
)
from callumployed.central.models import ResolveCompanyRequest
from callumployed.central.sync import pull_companies, pull_roles, resolve_unlinked_companies
from callumployed.config import BrowserSettings
from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    Role,
    RoleDiscoveryAttempt,
    RoleStatus,
)
from callumployed.data.repositories import (
    APPLICATION_STATUSES,
    add_company,
    add_company_career_page,
    add_cover_letter_example,
    add_role,
    clear_roles,
    get_company,
    get_location_filter,
    get_master_resume,
    get_role,
    get_scan_run,
    get_tracking_stats,
    list_companies,
    list_company_career_pages,
    list_config_values,
    list_cover_letter_examples,
    list_role_discovery_attempts,
    list_role_events,
    list_role_items,
    list_scan_candidates,
    list_scan_pages,
    list_scan_runs,
    set_company_central_link,
    set_company_central_sync_status,
    set_include_graduate_degree_roles,
    set_include_hardware_roles,
    set_internship_mode,
    set_location_filter,
    set_primary_company_career_page_url,
    set_require_software_keywords,
    set_role_status,
    update_role,
    upsert_master_resume,
)
from callumployed.services.app_settings import (
    configured_browser_profile_manager,
    get_settings,
    set_setting,
)
from callumployed.services.scan_schedule import (
    set_scan_schedule_enabled,
    set_scan_schedule_time,
)
from callumployed.services.scan_workflow import refilter_collected_roles
from callumployed.services.scan_workflow import rescan_role as run_rescan_role
from callumployed.services.scan_workflow import scan_company as run_scan_company
from callumployed.services.scan_workflow import scan_url as run_scan_url
from callumployed.web.server import run_server
from callumployed.webscraping.browser import render_careers_page
from callumployed.webscraping.errors import ScrapingError
from callumployed.webscraping.models import CareersPageScanResult
from callumployed.webscraping.profile_manager import BrowserProfileManager

app = typer.Typer(help="Local-first job-search automation CLI.")
companies_app = typer.Typer(help="Manage target companies.")
roles_app = typer.Typer(help="Manage job roles.")
scan_app = typer.Typer(help="Scan careers pages.")
config_app = typer.Typer(help="Manage app-wide configuration.")
browser_app = typer.Typer(help="Inspect managed browser profiles.")
materials_app = typer.Typer(help="Manage resumes and cover letter examples.")
central_app = typer.Typer(help="Sync with the central Callumployed role store.")

INSTALLER_SCRIPT_URL = (
    "https://raw.githubusercontent.com/CallumMackenzie/callumployed/master/scripts/install.sh"
)

app.add_typer(companies_app, name="companies")
app.add_typer(roles_app, name="roles")
app.add_typer(scan_app, name="scan")
app.add_typer(config_app, name="config")
app.add_typer(browser_app, name="browser")
app.add_typer(materials_app, name="materials")
app.add_typer(central_app, name="central")


@app.callback()
def main(ctx: typer.Context) -> None:
    """Manage target companies, roles, applications, and job-search artifacts."""
    if ctx.invoked_subcommand is not None:
        db.ensure_initialized()


@app.command("stats")
def stats_command() -> None:
    """Show application and job tracking stats."""
    with db.connect() as connection:
        stats = get_tracking_stats(connection)

    _print_stats(stats)


@app.command("serve")
def serve_command(
    host: Annotated[str, typer.Option("--host", help="Host interface to bind.")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", help="Port to bind.")] = 8765,
) -> None:
    """Serve the local web tracker."""
    typer.echo(f"Serving callumployed at http://{host}:{port}")
    run_server(host=host, port=port)


@app.command("update")
def update_command() -> None:
    """Update Callumployed by running the remote installer."""
    typer.echo("Updating callumployed with the remote installer...")
    try:
        subprocess.run(
            ["bash", "-c", f"curl -fsSL {INSTALLER_SCRIPT_URL} | bash"],
            check=True,
        )
    except FileNotFoundError as error:
        raise typer.Exit(1) from error
    except subprocess.CalledProcessError as error:
        raise typer.Exit(error.returncode) from error


@materials_app.command("set-master-resume")
def set_master_resume_command(
    resume_path: Annotated[Path, typer.Argument(help="Path to the master .tex resume.")]
) -> None:
    """Set or replace the stored master resume from a .tex file."""
    content = resume_path.read_text()
    try:
        with db.connect() as connection:
            resume = upsert_master_resume(
                connection,
                filename=resume_path.name,
                content=content,
            )
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error

    typer.echo(f"Stored master resume: {resume.filename}")


@materials_app.command("add-cover-letter-example")
def add_cover_letter_example_command(
    cover_letter_paths: Annotated[
        list[Path],
        typer.Argument(help="One or more cover letter example files."),
    ],
) -> None:
    """Add one or more cover letter examples."""
    if not cover_letter_paths:
        raise typer.BadParameter("provide at least one cover letter example file")

    stored_filenames: list[str] = []
    try:
        with db.connect() as connection:
            for cover_letter_path in cover_letter_paths:
                example = add_cover_letter_example(
                    connection,
                    filename=cover_letter_path.name,
                    content=cover_letter_path.read_text(),
                )
                stored_filenames.append(example.filename)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error

    typer.echo(
        f"Stored {len(stored_filenames)} cover letter "
        f"{'example' if len(stored_filenames) == 1 else 'examples'}: "
        + ", ".join(stored_filenames)
    )


@materials_app.command("show")
def show_materials_command() -> None:
    """Show stored resume and cover letter example metadata."""
    with db.connect() as connection:
        resume = get_master_resume(connection)
        examples = list_cover_letter_examples(connection)

    if resume is None:
        typer.echo("Master resume: none")
    else:
        typer.echo(f"Master resume: {resume.filename}")

    if not examples:
        typer.echo("Cover letter examples: none")
        return

    typer.echo(f"Cover letter examples: {len(examples)}")
    for example in examples:
        typer.echo(f"- {example.id}: {example.filename}")


@companies_app.command("add")
def add_company_command(
    name: Annotated[str, typer.Argument(help="Company name.")],
    career_page_url: Annotated[str, typer.Argument(help="Initial careers page URL.")],
    notes: Annotated[str | None, typer.Option("--notes", help="Optional notes.")] = None,
    prestige_tier: Annotated[
        str | None,
        typer.Option("--prestige-tier", help="Optional tier label."),
    ] = None,
) -> None:
    """Add a target company."""
    with db.connect() as connection:
        company = add_company(
            connection,
            Company(
                name=name,
                notes=notes,
                prestige_tier=prestige_tier,
            ),
        )
        if company.id is None:
            raise RuntimeError("created company did not include an id")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url=career_page_url, label="Main"),
        )
        _try_resolve_company_with_central_store(
            connection,
            company,
            career_page_urls=[career_page_url],
        )
    typer.echo(f"Added company #{company.id}: {company.name}")


@companies_app.command("update")
def update_company_command(
    company_id: Annotated[int, typer.Argument(help="Company ID.")],
    career_page: Annotated[
        str | None,
        typer.Option("--career-page", help="Primary careers page URL."),
    ] = None,
    add_career_page: Annotated[
        str | None,
        typer.Option("--add-career-page", help="Add another careers page URL."),
    ] = None,
    label: Annotated[
        str | None,
        typer.Option("--label", help="Optional label for the added careers page."),
    ] = None,
) -> None:
    """Update scan settings for a company."""
    if label is not None and add_career_page is None:
        raise typer.BadParameter("use --label only when adding a careers page")
    if career_page is None and add_career_page is None:
        raise typer.BadParameter(
            "provide at least one of --career-page or --add-career-page"
        )

    with db.connect() as connection:
        try:
            company = get_company(connection, company_id)
            if career_page is not None:
                set_primary_company_career_page_url(connection, company_id, career_page)
            if add_career_page is not None:
                add_company_career_page(
                    connection,
                    CompanyCareerPage(
                        company_id=company_id,
                        url=add_career_page,
                        label=label,
                    ),
                )
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error

    typer.echo(f"Updated company #{company.id}: {company.name}")


@companies_app.command("list")
def list_companies_command() -> None:
    """List target companies."""
    with db.connect() as connection:
        companies = list_companies(connection)

    if not companies:
        typer.echo("No companies yet.")
        return

    for company in companies:
        typer.echo(f"{company.id}: {company.name}")


@companies_app.command("show")
def show_company_command(
    company_id: Annotated[int, typer.Argument(help="Company ID.")],
) -> None:
    """Show all saved info for a company."""
    with db.connect() as connection:
        try:
            company = get_company(connection, company_id)
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error
        career_pages = list_company_career_pages(connection, company_id)

    typer.echo(f"Company #{company.id}: {company.name}")
    if company.prestige_tier:
        typer.echo(f"Prestige tier: {company.prestige_tier}")
    if company.notes:
        typer.echo(f"Notes: {company.notes}")
    if company.created_at:
        typer.echo(f"Created: {company.created_at}")
    if company.updated_at:
        typer.echo(f"Updated: {company.updated_at}")

    if not career_pages:
        typer.echo("Career pages: none")
        return

    typer.echo("Career pages:")
    for career_page in career_pages:
        label = f" ({career_page.label})" if career_page.label else ""
        typer.echo(f"- {career_page.id}: {career_page.url}{label}")


@central_app.command("configure")
def central_configure_command(
    api_url: Annotated[
        str | None,
        typer.Option("--api-url", help="Optional central API base URL override."),
    ] = None,
    passkey: Annotated[
        str | None,
        typer.Option("--passkey", help="Optional central API passkey for role-feed access."),
    ] = None,
    prompt_passkey: Annotated[
        bool,
        typer.Option("--prompt-passkey", help="Prompt securely for the central API passkey."),
    ] = False,
) -> None:
    """Save central store API configuration."""
    if passkey is None and prompt_passkey:
        passkey = typer.prompt("Central passkey", hide_input=True)
    try:
        if api_url is not None:
            with db.connect() as connection:
                set_central_api_url(connection, api_url)
        if passkey is not None:
            set_central_passkey(passkey)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error

    typer.echo("Central store configured.")


@central_app.command("status")
def central_status_command() -> None:
    """Show central store configuration and local link status."""
    with db.connect() as connection:
        api_url = get_central_api_url(connection)
        companies = list_companies(connection, include_inactive=True)
    passkey = get_central_passkey()
    linked_count = sum(company.central_company_id is not None for company in companies)
    pending_count = sum(company.central_company_id is None for company in companies)

    typer.echo(f"api_url: {api_url or 'missing'}")
    typer.echo(f"passkey: {'configured' if passkey is not None else 'missing'}")
    typer.echo(f"companies_linked: {linked_count}")
    typer.echo(f"companies_unlinked: {pending_count}")


@central_app.command("resolve-companies")
def central_resolve_companies_command() -> None:
    """Resolve local companies without central IDs."""
    with db.connect() as connection:
        client = _central_client_from_config(connection, require_passkey=False)
        result = resolve_unlinked_companies(connection, client)

    typer.echo(
        "Resolved companies: "
        f"{result.linked} matched, {result.created} created, "
        f"{result.needs_review} need review, {result.failed} failed"
    )


@central_app.command("pull-roles")
def central_pull_roles_command() -> None:
    """Pull all central roles into the local database."""
    with db.connect() as connection:
        client = _central_client_from_config(connection, require_passkey=True)
        resolve_result = resolve_unlinked_companies(connection, client)
        company_pull_result = pull_companies(connection, client)
        pull_result = pull_roles(connection, client)

    typer.echo(
        "Resolved companies before pull: "
        f"{resolve_result.linked} matched, {resolve_result.created} created, "
        f"{resolve_result.needs_review} need review, {resolve_result.failed} failed"
    )
    typer.echo(
        "Pulled companies: "
        f"{company_pull_result.companies_created} created, "
        f"{company_pull_result.companies_linked} linked, "
        f"{company_pull_result.companies_existing} already linked"
    )
    typer.echo(
        "Pulled roles: "
        f"{pull_result.roles_created} created, {pull_result.roles_updated} updated, "
        f"{pull_result.companies_created} companies created, "
        f"{pull_result.skipped_roles} skipped"
    )


@central_app.command("sync")
def central_sync_command() -> None:
    """Resolve companies and pull central roles."""
    central_pull_roles_command()


@config_app.command("include-graduate-degree-roles")
def include_graduate_degree_roles_command() -> None:
    """Allow Master's and PhD roles to be tracked."""
    with db.connect() as connection:
        set_include_graduate_degree_roles(connection, True)

    typer.echo("Graduate-degree role tracking enabled.")


@config_app.command("exclude-graduate-degree-roles")
def exclude_graduate_degree_roles_command() -> None:
    """Filter Master's and PhD roles from tracked roles."""
    with db.connect() as connection:
        set_include_graduate_degree_roles(connection, False)

    typer.echo("Graduate-degree role tracking disabled.")


@config_app.command("include-hardware-roles")
def include_hardware_roles_command() -> None:
    """Allow hardware-only roles to be tracked."""
    with db.connect() as connection:
        set_include_hardware_roles(connection, True)

    typer.echo("Hardware role tracking enabled.")


@config_app.command("exclude-hardware-roles")
def exclude_hardware_roles_command() -> None:
    """Filter hardware-only roles from tracked roles."""
    with db.connect() as connection:
        set_include_hardware_roles(connection, False)

    typer.echo("Hardware role tracking disabled.")


@config_app.command("require-software-keywords")
def require_software_keywords_command() -> None:
    """Require software-related keywords in discovered role links."""
    with db.connect() as connection:
        set_require_software_keywords(connection, True)

    typer.echo("Software keyword requirement enabled.")


@config_app.command("allow-non-software-keywords")
def allow_non_software_keywords_command() -> None:
    """Allow role links without software-related keywords."""
    with db.connect() as connection:
        set_require_software_keywords(connection, False)

    typer.echo("Software keyword requirement disabled.")


@config_app.command("enable-internship-mode")
def enable_internship_mode_command() -> None:
    """Require intern evidence before tracking roles."""
    with db.connect() as connection:
        set_internship_mode(connection, True)

    typer.echo("Internship mode enabled.")


@config_app.command("disable-internship-mode")
def disable_internship_mode_command() -> None:
    """Do not require intern evidence before tracking roles."""
    with db.connect() as connection:
        set_internship_mode(connection, False)

    typer.echo("Internship mode disabled.")


@config_app.command("set-location-filter")
def set_location_filter_command(
    location_filter: Annotated[
        str,
        typer.Argument(help="One of: all, canada, usa, north_america, international."),
    ],
) -> None:
    """Set the location filter for newly scanned or re-filtered roles."""
    try:
        with db.connect() as connection:
            set_location_filter(connection, location_filter)
            saved_location_filter = get_location_filter(connection)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error

    typer.echo(f"Location filter set to {saved_location_filter}.")


@config_app.command("enable-scan-schedule")
def enable_scan_schedule_command() -> None:
    """Enable the automatic daily full scan."""
    with db.connect() as connection:
        set_scan_schedule_enabled(connection, True)
    typer.echo("Daily scan schedule enabled.")


@config_app.command("disable-scan-schedule")
def disable_scan_schedule_command() -> None:
    """Disable the automatic daily full scan."""
    with db.connect() as connection:
        set_scan_schedule_enabled(connection, False)
    typer.echo("Daily scan schedule disabled.")


@config_app.command("set-scan-schedule-time")
def set_scan_schedule_time_command(
    scan_time: Annotated[str, typer.Argument(help="Local time in 24-hour HH:MM format.")],
) -> None:
    """Set the local time for the automatic daily scan."""
    try:
        with db.connect() as connection:
            saved_time = set_scan_schedule_time(connection, scan_time)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error
    typer.echo(f"Daily scan time set to {saved_time} local time.")


@config_app.command("show")
def show_config_command() -> None:
    """Show app-wide configuration."""
    with db.connect() as connection:
        settings = get_settings(connection)
        persisted = list_config_values(connection)
    if not persisted:
        typer.echo("No app config set.")
    for key, value in settings.items():
        rendered = str(value).lower() if isinstance(value, bool) else value
        suffix = "" if key in persisted else " (default)"
        typer.echo(f"{key}: {rendered}{suffix}")


@config_app.command("set")
def set_config_command(
    key: Annotated[str, typer.Argument(help="Settings key.")],
    value: Annotated[str, typer.Argument(help="New setting value.")],
) -> None:
    """Set any setting exposed by the web Settings page."""
    try:
        with db.connect() as connection:
            saved = set_setting(connection, key, value)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error
    rendered = str(saved).lower() if isinstance(saved, bool) else saved
    typer.echo(f"{key}: {rendered}")


@browser_app.command("profiles")
def browser_profiles_command() -> None:
    """List managed browser profile records."""
    try:
        profiles = BrowserProfileManager().list_profiles()
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error
    if not profiles:
        typer.echo("No managed browser profiles found.")
        return
    for profile in profiles:
        reason = f" - {profile.blocked_reason}" if profile.blocked_reason else ""
        typer.echo(
            f"{profile.name}: {profile.status} path=<{profile.path}>{reason}"
        )


@browser_app.command("config")
def browser_config_command() -> None:
    """Show browser backend configuration without printing secrets."""
    settings = BrowserSettings()
    typer.echo(f"backend: {settings.backend}")
    typer.echo(f"headless: {str(settings.headless).lower()}")
    typer.echo(f"timeout_ms: {settings.timeout_ms}")
    typer.echo(
        "browserbase_api_key: "
        f"{'configured' if settings.browserbase_api_key is not None else 'missing'}"
    )


@browser_app.command("smoke")
def browser_smoke_command(
    url: Annotated[str, typer.Argument(help="URL to render.")] = "https://example.com",
) -> None:
    """Render a single page through the configured browser backend."""
    try:
        page = asyncio.run(render_careers_page(url, stealth=False))
    except ScrapingError as error:
        raise typer.BadParameter(str(error)) from error

    typer.echo(f"Rendered: {page.final_url}")
    typer.echo(f"Title: {page.title or '(none)'}")
    typer.echo(f"HTML bytes: {len(page.html.encode('utf-8'))}")


def _configured_scan_browser_profile_manager() -> BrowserProfileManager:
    with db.connect() as connection:
        manager = configured_browser_profile_manager(connection)
    return manager


@scan_app.command("url")
def scan_url_command(
    url: Annotated[str, typer.Argument(help="Careers page URL.")],
) -> None:
    """Scan a careers page URL and print discovered job links."""
    try:
        result = asyncio.run(
            run_scan_url(
                url,
                browser_profile_manager=_configured_scan_browser_profile_manager(),
            )
        )
    except ScrapingError as error:
        raise typer.BadParameter(str(error)) from error
    except (LookupError, RuntimeError) as error:
        raise typer.BadParameter(str(error)) from error

    _print_scan_result(result)


@scan_app.command("company")
def scan_company_command(
    company_id: Annotated[int, typer.Argument(help="Company ID.")],
    retry_rejected_roles: Annotated[
        bool,
        typer.Option(
            "--retry-rejected-roles",
            help="Revisit candidate URLs previously classified as non-role pages.",
        ),
    ] = False,
) -> None:
    """Scan a saved company's careers URLs and print discovered job links."""
    with db.connect() as connection:
        try:
            company = get_company(connection, company_id)
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error

    try:
        _scan_company(
            company,
            retry_rejected_roles=retry_rejected_roles,
        )
    except ScrapingError as error:
        raise typer.BadParameter(str(error)) from error
    except (LookupError, RuntimeError) as error:
        raise typer.BadParameter(str(error)) from error


@scan_app.command("all")
def scan_all_command(
    retry_rejected_roles: Annotated[
        bool,
        typer.Option(
            "--retry-rejected-roles",
            help="Revisit candidate URLs previously classified as non-role pages.",
        ),
    ] = False,
) -> None:
    """Scan all saved companies sequentially."""
    with db.connect() as connection:
        companies = list_companies(connection)

    if not companies:
        typer.echo("No companies found.")
        return

    typer.echo(f"Scanning all companies: {len(companies)} total")
    succeeded = 0
    failed = 0
    skipped = 0
    for company in companies:
        typer.echo(f"--- {company.name} (#{company.id}) ---")
        try:
            scanned = _scan_company(
                company,
                retry_rejected_roles=retry_rejected_roles,
            )
        except ScrapingError as error:
            failed += 1
            typer.echo(f"Failed: {error}")
            continue

        if scanned:
            succeeded += 1
        else:
            skipped += 1

    typer.echo(f"Scan all complete: {succeeded} succeeded, {failed} failed, {skipped} skipped")


def _scan_company(
    company: Company,
    *,
    retry_rejected_roles: bool = False,
) -> bool:
    if company.id is None:
        raise RuntimeError("company did not include an id")

    with db.connect() as connection:
        career_pages = list_company_career_pages(connection, company.id)

    urls = [career_page.url for career_page in career_pages]
    if not urls:
        typer.echo(f"No career pages found for {company.name}.")
        return False

    typer.echo(f"Scanning {company.name}: {len(urls)} careers page(s)")
    if retry_rejected_roles:
        scan = asyncio.run(
            run_scan_company(
                company,
                browser_profile_manager=_configured_scan_browser_profile_manager(),
                retry_rejected_roles=True,
            )
        )
    else:
        scan = asyncio.run(
            run_scan_company(
                company,
                browser_profile_manager=_configured_scan_browser_profile_manager(),
            )
        )
    if scan is None:
        typer.echo(f"No career pages found for {company.name}.")
        return False
    typer.echo(f"Scan run #{scan['scan_run'].id}")
    for career_page in career_pages:
        typer.echo(f"Scanning URL: {career_page.url}")
    for result in scan["results"]:
        _print_scan_result(result)
    _print_scan_summary(scan["results"], scan["role_discovery_attempts"])
    return True


@scan_app.command("history")
def scan_history_command(
    company_id: Annotated[
        int | None,
        typer.Option("--company-id", help="Filter by company ID."),
    ] = None,
    limit: Annotated[int, typer.Option("--limit", help="Maximum scan runs to show.")] = 10,
) -> None:
    """List historical company scan runs."""
    with db.connect() as connection:
        scan_runs = list_scan_runs(connection, company_id=company_id, limit=limit)

    if not scan_runs:
        typer.echo("No scan runs found.")
        return

    for scan_run in scan_runs:
        finished = f", finished {scan_run.finished_at}" if scan_run.finished_at else ""
        typer.echo(
            f"{scan_run.id}: [{scan_run.scan_status.value}] "
            f"{scan_run.company_name} (#{scan_run.company_id}) "
            f"started {scan_run.started_at}{finished}"
        )
        if scan_run.error:
            typer.echo(f"  Error: {scan_run.error}")


@scan_app.command("show")
def scan_show_command(
    scan_run_id: Annotated[int, typer.Argument(help="Scan run ID.")],
    candidate_limit: Annotated[
        int,
        typer.Option(
            "--candidates",
            "--candidate-limit",
            min=0,
            help="Number of link candidates to show per scanned page.",
        ),
    ] = 0,
) -> None:
    """Show a historical scan run."""
    with db.connect() as connection:
        try:
            scan_run = get_scan_run(connection, scan_run_id)
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error
        company = get_company(connection, scan_run.company_id)
        scan_pages = list_scan_pages(connection, scan_run_id)
        role_discovery_attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run_id)
        attempts_by_candidate_id = {
            attempt.scan_candidate_id: attempt for attempt in role_discovery_attempts
        }
        candidate_counts_by_page = {}
        candidates_by_page = {}
        for page in scan_pages:
            if page.id is None:
                continue
            candidates = list_scan_candidates(connection, page.id)
            candidate_counts_by_page[page.id] = sum(candidate.selected for candidate in candidates)
            if candidate_limit > 0:
                candidates_by_page[page.id] = candidates[:candidate_limit]

    typer.echo(f"Scan run #{scan_run.id}: {company.name} [{scan_run.scan_status.value}]")
    typer.echo(f"Started: {scan_run.started_at}")
    if scan_run.finished_at:
        typer.echo(f"Finished: {scan_run.finished_at}")
    if scan_run.error:
        typer.echo(f"Error: {scan_run.error}")
    typer.echo(f"Role pages visited: {len(role_discovery_attempts)}")
    if not scan_pages:
        typer.echo("No scanned pages recorded.")
        return

    for page in scan_pages:
        typer.echo(f"Page #{page.id}: {page.source_url}")
        if page.final_url != page.source_url:
            typer.echo(f"Final URL: {page.final_url}")
        if page.title:
            typer.echo(f"Title: {page.title}")
        typer.echo(f"Candidates scanned: {page.candidates_scanned}")
        candidate_count = candidate_counts_by_page.get(page.id, 0) if page.id is not None else 0
        typer.echo(f"Candidates taken: {candidate_count}")
        if candidate_limit == 0:
            continue
        candidates = candidates_by_page.get(page.id, []) if page.id is not None else []
        if not candidates:
            typer.echo("Candidates: none")
            continue
        typer.echo("Link candidates:")
        for candidate in candidates:
            marker = "*" if candidate.selected else "-"
            typer.echo(f"{marker} [{candidate.confidence:.2f}] URL: <{candidate.url}>")
            if candidate.text:
                typer.echo(f"  Text: {candidate.text}")
            if candidate.reasons:
                typer.echo(f"  Reasons: {'; '.join(candidate.reasons)}")
            if candidate.id is not None:
                attempt = attempts_by_candidate_id.get(candidate.id)
                if attempt is not None:
                    typer.echo(f"  Visit: {attempt.status.value}")
                    if attempt.final_url:
                        typer.echo(f"  Final URL: {attempt.final_url}")
                    if attempt.title:
                        typer.echo(f"  Page title: {attempt.title}")
                    if attempt.role_id is not None:
                        typer.echo(f"  Role ID: {attempt.role_id}")
                    if attempt.assessment_is_role is not None:
                        typer.echo(f"  Is role: {attempt.assessment_is_role}")
                    if attempt.assessment_is_closed is not None:
                        typer.echo(f"  Is closed: {attempt.assessment_is_closed}")
                    if attempt.assessment_confidence is not None:
                        typer.echo(f"  Assessment confidence: {attempt.assessment_confidence:.2f}")
                    if attempt.assessment_extraction_method:
                        typer.echo(f"  Extraction method: {attempt.assessment_extraction_method}")
                    if attempt.assessment_location:
                        typer.echo(f"  Location: {attempt.assessment_location}")
                    if attempt.assessment_posting_id:
                        typer.echo(f"  Posting ID: {attempt.assessment_posting_id}")
                    if attempt.assessment_rejection_reason:
                        typer.echo(f"  Rejection: {attempt.assessment_rejection_reason}")
                    if attempt.assessment_reasons:
                        typer.echo(f"  Assessment reasons: {'; '.join(attempt.assessment_reasons)}")
                    if attempt.visible_text_excerpt:
                        typer.echo(f"  Excerpt: {attempt.visible_text_excerpt[:240]}")
                    if attempt.error:
                        typer.echo(f"  Error: {attempt.error}")


@scan_app.command("refilter")
def scan_refilter_command(
    company_id: Annotated[
        int | None,
        typer.Option("--company-id", help="Only re-filter attempts for one company."),
    ] = None,
    scan_run_id: Annotated[
        int | None,
        typer.Option("--scan-run-id", help="Only re-filter one scan run."),
    ] = None,
    apply: Annotated[
        bool,
        typer.Option("--apply", help="Persist changed attempt classifications and role updates."),
    ] = False,
) -> None:
    """Re-apply current scan filters to stored attempts without re-scraping."""
    result = refilter_collected_roles(
        company_id=company_id,
        scan_run_id=scan_run_id,
        apply=apply,
    )

    mode = "Applied" if apply else "Dry run"
    create_count = (
        result["roles_created"]
        if apply
        else sum(attempt["action"] == "create_role" for attempt in result["attempts"])
    )
    archive_count = (
        result["roles_archived"]
        if apply
        else sum(attempt["action"] == "archive_role" for attempt in result["attempts"])
    )
    typer.echo(f"{mode}: re-filtered {result['scanned_attempts']} stored attempt(s).")
    typer.echo(f"Changed attempts: {result['changed_attempts']}")
    typer.echo(f"Roles {'created' if apply else 'to create'}: {create_count}")
    typer.echo(f"Roles {'archived' if apply else 'to archive'}: {archive_count}")
    if result["protected_roles"]:
        typer.echo(f"Protected non-discovered roles: {result['protected_roles']}")
    if not result["attempts"]:
        typer.echo("No stored attempts would change.")
        return

    typer.echo("Changes:")
    for attempt in result["attempts"]:
        role = f" role #{attempt['role_id']}" if attempt["role_id"] is not None else ""
        title = f" - {attempt['title']}" if attempt["title"] else ""
        reason = f" ({attempt['reason']})" if attempt["reason"] else ""
        typer.echo(
            f"- attempt #{attempt['attempt_id']}: {attempt['action']}{role}; "
            f"is_role {attempt['previous_is_role']} -> {attempt['new_is_role']}"
            f"{reason}{title} <{attempt['url']}>"
        )


@roles_app.command("add")
def add_role_command(
    company_id: Annotated[int, typer.Argument(help="Company ID.")],
    title: Annotated[str, typer.Argument(help="Role title.")],
    role_url: Annotated[str, typer.Argument(help="Role posting URL.")],
    location: Annotated[
        str | None,
        typer.Option("--location", help="Optional role location."),
    ] = None,
    notes: Annotated[str | None, typer.Option("--notes", help="Optional notes.")] = None,
) -> None:
    """Add a role for a target company."""
    with db.connect() as connection:
        role = add_role(
            connection,
            Role(
                company_id=company_id,
                title=title,
                role_url=role_url,
                location=location,
                notes=notes,
            ),
        )
    typer.echo(f"Added role #{role.id}: {role.title}")


@roles_app.command("list")
def list_roles_command(
    company_id: Annotated[
        int | None,
        typer.Option("--company-id", help="Filter by company ID."),
    ] = None,
    company: Annotated[
        str | None,
        typer.Option("--company", help="Filter by company name text."),
    ] = None,
    status: Annotated[
        RoleStatus | None,
        typer.Option("--status", help="Filter by role status."),
    ] = None,
    title: Annotated[
        str | None,
        typer.Option("--title", help="Filter by role title text."),
    ] = None,
    link: Annotated[
        str | None,
        typer.Option("--link", "--url", help="Filter by role link text."),
    ] = None,
    location: Annotated[
        str | None,
        typer.Option("--location", help="Filter by location text."),
    ] = None,
    query: Annotated[
        str | None,
        typer.Option("--query", "-q", help="Search company, title, link, status, or location."),
    ] = None,
) -> None:
    """List roles."""
    with db.connect() as connection:
        roles = list_role_items(
            connection,
            company_id=company_id,
            company=company,
            role_status=status,
            title=title,
            link=link,
            location=location,
            query=query,
        )

    if not roles:
        typer.echo("No roles found.")
        return

    for role in roles:
        location = f" - {role.location}" if role.location else ""
        typer.echo(f"{role.id}: {role.company_name} - {role.title} <{role.role_url}>{location}")


@roles_app.command("show")
def show_role_command(
    role_id: Annotated[int, typer.Argument(help="Role ID.")],
) -> None:
    """Show role details."""
    with db.connect() as connection:
        try:
            role = get_role(connection, role_id)
            company = get_company(connection, role.company_id)
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error
        events = list_role_events(connection, role_id)

    typer.echo(f"Role #{role.id}: {role.title}")
    typer.echo(f"Company: {company.name} (#{company.id})")
    typer.echo(f"Status: {role.role_status.value}")
    if role.location:
        typer.echo(f"Location: {role.location}")
    typer.echo(f"URL: {role.role_url}")
    if role.posting_id:
        typer.echo(f"Posting ID: {role.posting_id}")
    if role.description:
        typer.echo(f"Description: {role.description[:1000]}")
    if role.notes:
        typer.echo(f"Notes: {role.notes}")
    if role.first_seen_at:
        typer.echo(f"First seen: {role.first_seen_at.isoformat()}")
    if role.last_seen_at:
        typer.echo(f"Last seen: {role.last_seen_at.isoformat()}")
    if role.updated_at:
        typer.echo(f"Updated: {role.updated_at.isoformat()}")

    if events:
        typer.echo("Events:")
        for event in events:
            transition = ""
            if event.old_status is not None or event.new_status is not None:
                old_status = event.old_status.value if event.old_status is not None else "none"
                new_status = event.new_status.value if event.new_status is not None else "none"
                transition = f" ({old_status} -> {new_status})"
            typer.echo(f"- {event.event_type}{transition}: {event.summary}")


@roles_app.command("clear")
def clear_roles_command() -> None:
    """Delete all tracked roles after two confirmations."""
    typer.confirm(
        "This will delete every tracked role and role-linked event. Continue?",
        abort=True,
    )
    confirmation = typer.prompt('Type "clear roles" to confirm')
    if confirmation != "clear roles":
        raise typer.Abort()

    with db.connect() as connection:
        deleted_count = clear_roles(connection)

    typer.echo(f"Deleted {deleted_count} role{'s' if deleted_count != 1 else ''}.")


@roles_app.command("update")
def update_role_command(
    role_id: Annotated[int, typer.Argument(help="Role ID.")],
    title: Annotated[str | None, typer.Option("--title", help="New role title.")] = None,
    role_url: Annotated[str | None, typer.Option("--url", help="New role posting URL.")] = None,
    location: Annotated[str | None, typer.Option("--location", help="New role location.")] = None,
    notes: Annotated[str | None, typer.Option("--notes", help="New notes.")] = None,
    clear_location: Annotated[
        bool,
        typer.Option("--clear-location", help="Clear the role location."),
    ] = False,
    clear_notes: Annotated[
        bool,
        typer.Option("--clear-notes", help="Clear the role notes."),
    ] = False,
) -> None:
    """Update role fields."""
    if location is not None and clear_location:
        raise typer.BadParameter("use either --location or --clear-location, not both")
    if notes is not None and clear_notes:
        raise typer.BadParameter("use either --notes or --clear-notes, not both")

    with db.connect() as connection:
        try:
            role = update_role(
                connection,
                role_id,
                title=title,
                role_url=role_url,
                location=location,
                notes=notes,
                clear_location=clear_location,
                clear_notes=clear_notes,
            )
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error

    typer.echo(f"Updated role #{role.id}: {role.title}")


@roles_app.command("rescan")
def rescan_role_command(
    role_id: Annotated[int, typer.Argument(help="Role ID.")],
    update_status: Annotated[
        bool,
        typer.Option(
            "--update-status",
            help="Mark the role closed when the rescan finds a closed posting.",
        ),
    ] = False,
) -> None:
    """Revisit an existing role URL and refresh extracted role fields."""
    try:
        result = asyncio.run(
            run_rescan_role(
                role_id,
                browser_profile_manager=_configured_scan_browser_profile_manager(),
                update_status=update_status,
            )
        )
    except ScrapingError as error:
        raise typer.BadParameter(str(error)) from error
    except (LookupError, RuntimeError) as error:
        raise typer.BadParameter(str(error)) from error

    previous_role = result["previous_role"]
    role = result["role"]
    assessment = result["assessment"]
    typer.echo(f"Rescanned role #{role.id}: {role.title}")
    typer.echo(f"Final URL: {result['final_url']}")
    typer.echo(f"Is role: {assessment.is_role}")
    typer.echo(f"Is closed: {assessment.is_closed}")
    typer.echo(f"Confidence: {assessment.confidence:.2f}")
    typer.echo(f"Extraction method: {assessment.extraction_method}")
    if previous_role.title != role.title:
        typer.echo(f"Title: {previous_role.title} -> {role.title}")
    if previous_role.location != role.location:
        typer.echo(f"Location: {previous_role.location or 'none'} -> {role.location or 'none'}")
    if previous_role.posting_id != role.posting_id:
        typer.echo(
            f"Posting ID: {previous_role.posting_id or 'none'} -> {role.posting_id or 'none'}"
        )
    if previous_role.role_status != role.role_status:
        typer.echo(f"Status: {previous_role.role_status.value} -> {role.role_status.value}")
    if assessment.rejection_reason:
        typer.echo(f"Rejection: {assessment.rejection_reason}")


@roles_app.command("set-status")
def set_status_command(
    role_id: Annotated[int, typer.Argument(help="Role ID.")],
    status: Annotated[RoleStatus, typer.Argument(help="New role status.")],
    summary: Annotated[
        str,
        typer.Option("--summary", help="Event summary."),
    ] = "Status updated manually.",
) -> None:
    """Update a role status and record an event."""
    _set_role_state(role_id, status, summary=summary)


def _set_role_state(role_id: int, state: RoleStatus, *, summary: str) -> None:
    with db.connect() as connection:
        try:
            role = set_role_status(connection, role_id, state, summary=summary)
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error
    typer.echo(f"Updated role #{role.id}: {role.role_status.value}")


def _central_client_from_config(
    connection: turso.Connection,
    *,
    require_passkey: bool,
) -> CentralStoreClient:
    api_url = get_central_api_url(connection)
    passkey = get_central_passkey()
    if api_url is None:
        raise typer.BadParameter(
            "central API URL is not configured; run `callumployed central configure`"
        )
    if passkey is None and require_passkey:
        raise typer.BadParameter(
            "central passkey is not configured; run "
            "`callumployed central configure --prompt-passkey`"
        )
    return CentralStoreClient(api_url=api_url, passkey=passkey)


def _try_resolve_company_with_central_store(
    connection: turso.Connection,
    company: Company,
    *,
    career_page_urls: list[str],
) -> None:
    if company.id is None:
        return
    api_url = get_central_api_url(connection)
    passkey = get_central_passkey()
    if api_url is None:
        return

    client = CentralStoreClient(api_url=api_url, passkey=passkey)
    try:
        response = client.resolve_company(
            ResolveCompanyRequest(
                name=company.name,
                career_page_urls=career_page_urls,
                prestige_tier=company.prestige_tier,
                tier_source_id=get_central_client_id(connection),
            )
        )
    except CentralStoreError as error:
        set_company_central_sync_status(
            connection,
            company.id,
            status="failed",
            error=str(error),
        )
        return

    if response.action == "needs_review" or response.global_company_id is None:
        set_company_central_sync_status(
            connection,
            company.id,
            status="needs_review",
        )
        return

    set_company_central_link(
        connection,
        company.id,
        central_company_id=response.global_company_id,
        canonical_domain=response.canonical_domain,
        normalized_name=response.normalized_name,
        prestige_tier=response.default_tier,
    )


def _print_stats(stats: dict[str, object]) -> None:
    typer.echo(f"Companies: {stats['companies_total']}")
    typer.echo(f"Jobs: {stats['jobs_total']}")
    typer.echo(f"Applications: {stats['applications_total']}")

    jobs_by_status = stats["jobs_by_status"]
    if not isinstance(jobs_by_status, dict):
        raise TypeError("jobs_by_status must be a dict")
    typer.echo("Jobs by status:")
    for status in RoleStatus:
        typer.echo(f"- {status.value}: {jobs_by_status.get(status.value, 0)}")

    applications_by_status = stats["applications_by_status"]
    if not isinstance(applications_by_status, dict):
        raise TypeError("applications_by_status must be a dict")
    typer.echo("Applications by status:")
    for status in APPLICATION_STATUSES:
        typer.echo(f"- {status.value}: {applications_by_status.get(status.value, 0)}")


def _print_scan_result(result: CareersPageScanResult) -> None:
    typer.echo(f"Scanned: {result.final_url}")
    if result.title:
        typer.echo(f"Title: {result.title}")
    typer.echo(f"Candidates scanned: {result.candidates_scanned}")
    typer.echo(f"Confidence: {result.confidence.value}")

    if not result.links:
        typer.echo("No job links discovered.")
        return

    typer.echo("Discovered job links:")
    for link in result.links:
        text = f" - {link.text}" if link.text else ""
        typer.echo(f"- [{link.confidence:.2f}] <{link.url}>{text}")


def _print_scan_summary(
    results: list[CareersPageScanResult],
    role_discovery_attempts: list[RoleDiscoveryAttempt],
) -> None:
    candidates = [candidate for result in results for candidate in result.candidates]
    skipped_existing_roles = sum(
        "already in database" in candidate.reasons for candidate in candidates
    )
    skipped_previously_rejected = sum(
        "already rejected as non-role" in candidate.reasons for candidate in candidates
    )
    created_role_ids = {
        attempt.role_id
        for attempt in role_discovery_attempts
        if attempt.assessment_is_role is True and attempt.role_id is not None
    }
    rejected_after_visit = sum(
        attempt.assessment_is_role is False for attempt in role_discovery_attempts
    )
    visit_failures = sum(attempt.status.value == "failed" for attempt in role_discovery_attempts)

    typer.echo("Scan summary:")
    typer.echo(f"- Candidates scanned: {sum(result.candidates_scanned for result in results)}")
    typer.echo(f"- Discovered links selected: {sum(len(result.links) for result in results)}")
    typer.echo(f"- Skipped existing roles: {skipped_existing_roles}")
    typer.echo(f"- Skipped previously rejected: {skipped_previously_rejected}")
    typer.echo(f"- Role pages visited: {len(role_discovery_attempts)}")
    typer.echo(f"- New roles created: {len(created_role_ids)}")
    typer.echo(f"- Rejected after visit: {rejected_after_visit}")
    typer.echo(f"- Visit failures: {visit_failures}")
