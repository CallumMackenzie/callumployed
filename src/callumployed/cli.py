from typing import Annotated

import typer

from callumployed.data import db
from callumployed.data.models import Company, Role, RoleStatus
from callumployed.data.repositories import (
    add_company,
    add_role,
    list_companies,
    list_role_items,
    set_role_status,
)

app = typer.Typer(help="Local-first job-search automation CLI.")
companies_app = typer.Typer(help="Manage target companies.")
roles_app = typer.Typer(help="Manage job roles.")

app.add_typer(companies_app, name="companies")
app.add_typer(roles_app, name="roles")


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
        role = set_role_status(connection, role_id, status, summary=summary)
    typer.echo(f"Updated role #{role.id}: {role.role_status.value}")
