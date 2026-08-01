import sqlite3
from pathlib import Path

from callumployed.data import db as app_db

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

    assert {
        "companies",
        "app_config",
        "cover_letter_examples",
        "cover_letter_example_vectors",
        "company_career_pages",
        "roles",
        "scan_runs",
        "scan_pages",
        "scan_candidates",
        "role_discovery_attempts",
        "events",
        "resume_feedback_history",
    }.issubset(tables)

    role_discovery_columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(role_discovery_attempts)").fetchall()
    }
    assert {
        "assessment_is_role",
        "assessment_is_closed",
        "assessment_confidence",
        "assessment_location",
        "assessment_description",
        "assessment_posting_id",
        "assessment_extraction_method",
        "assessment_rejection_reason",
        "assessment_reasons_json",
    }.issubset(role_discovery_columns)

    role_columns = {row[1] for row in connection.execute("PRAGMA table_info(roles)").fetchall()}
    assert {
        "description",
        "posting_id",
        "central_role_id",
        "central_source",
        "central_synced_at",
    }.issubset(role_columns)

    company_columns = {
        row[1] for row in connection.execute("PRAGMA table_info(companies)").fetchall()
    }
    assert {
        "browser_extra_wait_ms",
        "is_active",
        "central_company_id",
        "canonical_domain",
        "normalized_name",
        "central_sync_status",
        "central_sync_error",
        "central_matched_at",
    }.issubset(company_columns)


def test_initial_schema_rejects_invalid_role_status() -> None:
    connection = sqlite3.connect(":memory:")
    apply_initial_schema(connection)
    connection.execute("INSERT INTO companies (id, name) VALUES (1, 'Acme')")

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


def test_initial_schema_rejects_prepared_role_status() -> None:
    connection = sqlite3.connect(":memory:")
    apply_initial_schema(connection)
    connection.execute("INSERT INTO companies (id, name) VALUES (1, 'Acme')")

    try:
        connection.execute(
            """
            INSERT INTO roles (company_id, title, role_url, role_status)
            VALUES (1, 'Software Engineer', 'https://example.com/jobs/1', 'prepared')
            """
        )
    except sqlite3.IntegrityError:
        return

    raise AssertionError("prepared should no longer be a valid role_status")


def test_migrations_convert_legacy_prepared_roles_to_interested() -> None:
    connection = app_db.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE roles (
            id INTEGER PRIMARY KEY,
            company_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            role_url TEXT NOT NULL,
            role_status TEXT NOT NULL DEFAULT 'discovered' CHECK (
                role_status IN ('discovered', 'interested', 'prepared')
            ),
            first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
            last_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
        )
        """
    )
    connection.execute("INSERT INTO companies (id, name) VALUES (1, 'Acme')")
    connection.execute(
        """
        INSERT INTO roles (company_id, title, role_url, role_status)
        VALUES (1, 'Software Engineer', 'https://example.com/jobs/1', 'prepared')
        """
    )

    app_db.run_migrations(connection)

    row = connection.execute("SELECT role_status FROM roles WHERE id = 1").fetchone()
    assert row["role_status"] == "interested"


def test_initial_schema_supports_company_role_scan_and_event() -> None:
    connection = sqlite3.connect(":memory:")
    apply_initial_schema(connection)
    connection.execute(
        """
        INSERT INTO companies (
            id,
            name,
            notes,
            prestige_tier
        )
        VALUES (1, 'Acme', 'Interesting infra team.', 'A')
        """
    )
    connection.execute(
        """
        INSERT INTO company_career_pages (company_id, url, label)
        VALUES (1, 'https://example.com/careers', 'Main')
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
        SELECT
            companies.name,
            company_career_pages.url,
            roles.title,
            roles.role_status,
            scan_runs.scan_status
        FROM companies
        JOIN company_career_pages ON company_career_pages.company_id = companies.id
        JOIN roles ON roles.company_id = companies.id
        JOIN scan_runs ON scan_runs.company_id = companies.id
        """
    ).fetchone()

    assert row == (
        "Acme",
        "https://example.com/careers",
        "Software Engineer",
        "discovered",
        "succeeded",
    )
