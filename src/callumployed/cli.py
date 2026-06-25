import asyncio
from typing import Annotated

import typer

from callumployed.data import db
from callumployed.data.models import Company, CompanyCareerPage, Role, RoleStatus
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    add_role,
    clear_default_external_browser_port,
    get_company,
    get_default_external_browser_port,
    get_role,
    get_scan_run,
    list_companies,
    list_company_career_pages,
    list_config_values,
    list_role_discovery_attempts,
    list_role_events,
    list_role_items,
    list_scan_candidates,
    list_scan_pages,
    list_scan_runs,
    set_company_external_browser_port,
    set_default_external_browser_port,
    set_primary_company_career_page_url,
    set_role_status,
    update_role,
)
from callumployed.services.scan_workflow import scan_company as run_scan_company
from callumployed.services.scan_workflow import scan_url as run_scan_url
from callumployed.webscraping.errors import ScrapingError
from callumployed.webscraping.models import CareersPageScanResult

app = typer.Typer(help="Local-first job-search automation CLI.")
companies_app = typer.Typer(help="Manage target companies.")
roles_app = typer.Typer(help="Manage job roles.")
scan_app = typer.Typer(help="Scan careers pages.")
config_app = typer.Typer(help="Manage app-wide configuration.")

app.add_typer(companies_app, name="companies")
app.add_typer(roles_app, name="roles")
app.add_typer(scan_app, name="scan")
app.add_typer(config_app, name="config")


@app.callback()
def main(ctx: typer.Context) -> None:
    """Manage target companies, roles, applications, and job-search artifacts."""
    if ctx.invoked_subcommand is not None:
        db.ensure_initialized()


@companies_app.command("add")
def add_company_command(
    name: Annotated[str, typer.Argument(help="Company name.")],
    career_page_url: Annotated[str, typer.Argument(help="Initial careers page URL.")],
    notes: Annotated[str | None, typer.Option("--notes", help="Optional notes.")] = None,
    prestige_tier: Annotated[
        str | None,
        typer.Option("--prestige-tier", help="Optional tier label."),
    ] = None,
    external_browser_port: Annotated[
        int | None,
        typer.Option(
            "--external-browser-port",
            help="Optional CDP port for an already-running external Chromium browser.",
        ),
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
                external_browser_port=external_browser_port,
            ),
        )
        if company.id is None:
            raise RuntimeError("created company did not include an id")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url=career_page_url, label="Main"),
        )
    typer.echo(f"Added company #{company.id}: {company.name}")


@companies_app.command("update")
def update_company_command(
    company_id: Annotated[int, typer.Argument(help="Company ID.")],
    external_browser_port: Annotated[
        int | None,
        typer.Option(
            "--external-browser-port",
            help="CDP port for an already-running external Chromium browser.",
        ),
    ] = None,
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
    if external_browser_port is None and career_page is None and add_career_page is None:
        raise typer.BadParameter(
            "provide at least one of --external-browser-port, --career-page, "
            "or --add-career-page"
        )

    with db.connect() as connection:
        try:
            company = get_company(connection, company_id)
            if external_browser_port is not None:
                company = set_company_external_browser_port(
                    connection,
                    company_id,
                    external_browser_port,
                )
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
    if company.external_browser_port is not None:
        typer.echo(f"External browser CDP port: {company.external_browser_port}")
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


@config_app.command("set-external-browser-port")
def set_default_external_browser_port_command(
    port: Annotated[int, typer.Argument(help="Default CDP port for external browser scans.")],
) -> None:
    """Set the app-wide external browser CDP port."""
    with db.connect() as connection:
        set_default_external_browser_port(connection, port)

    typer.echo(f"Default external browser CDP port: {port}")


@config_app.command("clear-external-browser-port")
def clear_default_external_browser_port_command() -> None:
    """Clear the app-wide external browser CDP port."""
    with db.connect() as connection:
        clear_default_external_browser_port(connection)

    typer.echo("Default external browser CDP port cleared.")


@config_app.command("show")
def show_config_command() -> None:
    """Show app-wide configuration."""
    with db.connect() as connection:
        values = list_config_values(connection)

    if not values:
        typer.echo("No app config set.")
        return

    for key, value in values.items():
        typer.echo(f"{key}: {value}")


@scan_app.command("url")
def scan_url_command(
    url: Annotated[str, typer.Argument(help="Careers page URL.")],
) -> None:
    """Scan a careers page URL and print discovered job links."""
    try:
        result = asyncio.run(run_scan_url(url))
    except ScrapingError as error:
        raise typer.BadParameter(str(error)) from error

    _print_scan_result(result)


@scan_app.command("company")
def scan_company_command(
    company_id: Annotated[int, typer.Argument(help="Company ID.")],
) -> None:
    """Scan a saved company's careers URLs and print discovered job links."""
    with db.connect() as connection:
        try:
            company = get_company(connection, company_id)
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error
        default_external_browser_port = get_default_external_browser_port(connection)

    try:
        _scan_company(
            company,
            default_external_browser_port=default_external_browser_port,
        )
    except ScrapingError as error:
        raise typer.BadParameter(str(error)) from error


@scan_app.command("all")
def scan_all_command() -> None:
    """Scan all saved companies sequentially."""
    with db.connect() as connection:
        companies = list_companies(connection)
        default_external_browser_port = get_default_external_browser_port(connection)

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
                default_external_browser_port=default_external_browser_port,
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
    default_external_browser_port: int | None,
) -> bool:
    if company.id is None:
        raise RuntimeError("company did not include an id")

    with db.connect() as connection:
        career_pages = list_company_career_pages(connection, company.id)

    urls = [career_page.url for career_page in career_pages]
    if not urls:
        typer.echo(f"No career pages found for {company.name}.")
        return False

    external_browser_port = company.external_browser_port or default_external_browser_port

    typer.echo(f"Scanning {company.name}: {len(urls)} careers page(s)")
    if external_browser_port:
        source = "company" if company.external_browser_port else "app default"
        typer.echo(f"External browser CDP port: {external_browser_port} ({source})")
    scan = asyncio.run(
        run_scan_company(
            company,
            default_external_browser_port=default_external_browser_port,
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
                    if attempt.error:
                        typer.echo(f"  Error: {attempt.error}")


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
    status: Annotated[
        RoleStatus | None,
        typer.Option("--status", help="Filter by role status."),
    ] = None,
    location: Annotated[
        str | None,
        typer.Option("--location", help="Filter by location text."),
    ] = None,
    query: Annotated[
        str | None,
        typer.Option("--query", "-q", help="Search title, company, or location."),
    ] = None,
) -> None:
    """List roles."""
    with db.connect() as connection:
        roles = list_role_items(
            connection,
            company_id=company_id,
            role_status=status,
            location=location,
            query=query,
        )

    if not roles:
        typer.echo("No roles found.")
        return

    for role in roles:
        location = f" ({role.location})" if role.location else ""
        typer.echo(
            f"{role.id}: [{role.role_status.value}] "
            f"{role.company_name} - {role.title}{location} <{role.role_url}>"
        )


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
    with db.connect() as connection:
        try:
            role = set_role_status(connection, role_id, status, summary=summary)
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error
    typer.echo(f"Updated role #{role.id}: {role.role_status.value}")


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
