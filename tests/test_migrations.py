import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def apply_initial_schema(connection: sqlite3.Connection) -> None:
    migration = ROOT / "migrations" / "001_initial_tracking_schema.sql"
    connection.executescript(migration.read_text())


def test_initial_schema_creates_minimal_tracking_tables() -> None:
    connection = sqlite3.connect(":memory:")
    apply_initial_schema(connection)

    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        )
    }

    assert {"companies", "roles", "scan_runs", "events"}.issubset(tables)


def test_initial_schema_rejects_invalid_role_status() -> None:
    connection = sqlite3.connect(":memory:")
    apply_initial_schema(connection)
    connection.execute(
        "INSERT INTO companies (id, name, careers_url) VALUES (1, 'Acme', 'https://example.com')"
    )

    try:
        connection.execute(
            """
            INSERT INTO roles (company_id, title, role_url, role_status)
            VALUES (1, 'Software Engineer', 'https://example.com/jobs/1', 'maybe')
            """
        )
    except sqlite3.IntegrityError:
        return

    raise AssertionError("invalid role_status should violate the CHECK constraint")


def test_initial_schema_supports_company_role_scan_and_event() -> None:
    connection = sqlite3.connect(":memory:")
    apply_initial_schema(connection)
    connection.execute(
        """
        INSERT INTO companies (id, name, careers_url, notes, prestige_tier)
        VALUES (1, 'Acme', 'https://example.com/careers', 'Interesting infra team.', 'A')
        """
    )
    connection.execute(
        """
        INSERT INTO roles (id, company_id, title, role_url, location)
        VALUES (1, 1, 'Software Engineer', 'https://example.com/jobs/1', 'Vancouver')
        """
    )
    connection.execute(
        """
        INSERT INTO scan_runs (id, company_id, scan_status)
        VALUES (1, 1, 'succeeded')
        """
    )
    connection.execute(
        """
        INSERT INTO events (
            company_id,
            role_id,
            event_type,
            old_status,
            new_status,
            source,
            summary
        )
        VALUES (
            1,
            1,
            'status_changed',
            'discovered',
            'interested',
            'manual',
            'Marked as interesting.'
        )
        """
    )

    row = connection.execute(
        """
        SELECT companies.name, roles.title, roles.role_status, scan_runs.scan_status
        FROM companies
        JOIN roles ON roles.company_id = companies.id
        JOIN scan_runs ON scan_runs.company_id = companies.id
        """
    ).fetchone()

    assert row == ("Acme", "Software Engineer", "discovered", "succeeded")
