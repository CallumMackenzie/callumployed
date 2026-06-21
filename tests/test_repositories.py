from callumployed.data import db
from callumployed.data.models import Company, Role, RoleStatus
from callumployed.data.repositories import (
    add_company,
    add_role,
    get_event,
    list_companies,
    list_role_events,
    list_role_items,
    list_roles,
    set_role_status,
    update_role,
)


def test_company_repository_adds_and_lists_companies() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(
        connection,
        Company(name="Acme", careers_url="https://example.com/careers", prestige_tier="A"),
    )

    assert company.id == 1
    assert list_companies(connection) == [company]


def test_role_repository_adds_filters_and_records_status_events() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme", careers_url="https://example.com"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(
            company_id=company.id,
            title="Software Engineer",
            role_url="https://example.com/jobs/1",
            location="Vancouver",
        ),
    )
    assert role.id is not None

    filtered_roles = list_roles(
        connection,
        company_id=company.id,
        role_status=RoleStatus.DISCOVERED,
    )

    assert filtered_roles == [role]

    updated_role = set_role_status(
        connection,
        role.id,
        RoleStatus.INTERESTED,
        summary="Looks worth applying to.",
    )
    event = get_event(connection, 1)

    assert updated_role.role_status is RoleStatus.INTERESTED
    assert event.old_status is RoleStatus.DISCOVERED
    assert event.new_status is RoleStatus.INTERESTED


def test_role_list_items_include_company_and_filter_by_query() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme", careers_url="https://example.com"))
    assert company.id is not None
    add_role(
        connection,
        Role(
            company_id=company.id,
            title="Backend Engineer",
            role_url="https://example.com/jobs/backend",
            location="Vancouver",
        ),
    )

    roles = list_role_items(connection, query="backend")

    assert len(roles) == 1
    assert roles[0].company_name == "Acme"
    assert roles[0].title == "Backend Engineer"


def test_update_role_changes_and_clears_fields() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme", careers_url="https://example.com"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(
            company_id=company.id,
            title="Software Engineer",
            role_url="https://example.com/jobs/1",
            location="Remote",
            notes="Initial notes.",
        ),
    )
    assert role.id is not None

    updated_role = update_role(
        connection,
        role.id,
        title="Backend Engineer",
        role_url="https://example.com/jobs/backend",
        clear_location=True,
        clear_notes=True,
    )

    assert updated_role.title == "Backend Engineer"
    assert updated_role.role_url == "https://example.com/jobs/backend"
    assert updated_role.location is None
    assert updated_role.notes is None


def test_list_role_events_returns_recent_role_events() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme", careers_url="https://example.com"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(company_id=company.id, title="Backend Engineer", role_url="https://example.com"),
    )
    assert role.id is not None

    set_role_status(connection, role.id, RoleStatus.INTERESTED, summary="Worth tracking.")

    events = list_role_events(connection, role.id)

    assert len(events) == 1
    assert events[0].summary == "Worth tracking."
