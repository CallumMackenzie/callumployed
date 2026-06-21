import asyncio
from typing import Annotated

import typer

from callumployed.data import db
from callumployed.data.models import Company, Role, RoleStatus
from callumployed.data.repositories import (
    add_company,
    add_role,
    get_company,
    get_role,
    list_companies,
    list_role_events,
    list_role_items,
    set_role_status,
    update_role,
)
from callumployed.webscraping.errors import ScrapingError
from callumployed.webscraping.models import CareersPageScanResult
from callumployed.webscraping.scanner import scan_careers_page

app = typer.Typer(help="Local-first job-search automation CLI.")
companies_app = typer.Typer(help="Manage target companies.")
roles_app = typer.Typer(help="Manage job roles.")
scan_app = typer.Typer(help="Scan careers pages.")

app.add_typer(companies_app, name="companies")
app.add_typer(roles_app, name="roles")
app.add_typer(scan_app, name="scan")


@app.callback()
def main(ctx: typer.Context) -> None:
    """Manage target companies, roles, applications, and job-search artifacts."""
    if ctx.invoked_subcommand is not None:
        db.ensure_initialized()


@companies_app.command("add")
def add_company_command(
    name: Annotated[str, typer.Argument(help="Company name.")],
    careers_url: Annotated[str, typer.Argument(help="Company careers page URL.")],
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
                careers_url=careers_url,
                notes=notes,
                prestige_tier=prestige_tier,
            ),
        )
    typer.echo(f"Added company #{company.id}: {company.name}")


@companies_app.command("list")
def list_companies_command() -> None:
    """List target companies."""
    with db.connect() as connection:
        companies = list_companies(connection)

    if not companies:
        typer.echo("No companies yet.")
        return

    for company in companies:
        typer.echo(f"{company.id}: {company.name} <{company.careers_url}>")


@scan_app.command("url")
def scan_url_command(
    url: Annotated[str, typer.Argument(help="Careers page URL.")],
) -> None:
    """Scan a careers page URL and print discovered job links."""
    try:
        result = asyncio.run(scan_careers_page(url))
    except ScrapingError as error:
        raise typer.BadParameter(str(error)) from error

    _print_scan_result(result)


@scan_app.command("company")
def scan_company_command(
    company_id: Annotated[int, typer.Argument(help="Company ID.")],
) -> None:
    """Scan a saved company's careers URL and print discovered job links."""
    with db.connect() as connection:
        try:
            company = get_company(connection, company_id)
        except LookupError as error:
            raise typer.BadParameter(str(error)) from error

    typer.echo(f"Scanning {company.name}: {company.careers_url}")
    try:
        result = asyncio.run(scan_careers_page(company.careers_url))
    except ScrapingError as error:
        raise typer.BadParameter(str(error)) from error

    _print_scan_result(result)


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
        typer.echo(f"- [{link.confidence:.2f}] {link.url}{text}")
