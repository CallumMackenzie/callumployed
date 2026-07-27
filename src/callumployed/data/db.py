import os
from pathlib import Path

import turso
from platformdirs import user_data_path

ROOT = Path(__file__).resolve().parents[3]
MIGRATIONS_DIR = ROOT / "migrations"
DATABASE_PATH_ENV = "CALLUMPLOYED_DATABASE_PATH"


def default_database_path() -> Path:
    return user_data_path("callumployed", appauthor=False) / "callumployed.sqlite3"


def connect(database: str | Path | None = None) -> turso.Connection:
    configured_database = database or os.environ.get(DATABASE_PATH_ENV)
    database_path = default_database_path() if configured_database is None else configured_database
    if database_path != ":memory:":
        Path(database_path).expanduser().parent.mkdir(parents=True, exist_ok=True)

    connection = turso.connect(str(database_path))
    connection.row_factory = turso.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def run_migrations(connection: turso.Connection) -> None:
    for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
        connection.executescript(migration.read_text())
    _ensure_app_config_table(connection)
    _ensure_master_resumes_table(connection)
    _ensure_cover_letter_examples_table(connection)
    _ensure_company_browser_wait_column(connection)
    _ensure_role_information_columns(connection)
    _ensure_role_discovery_assessment_columns(connection)
    _backfill_legacy_company_career_pages(connection)
    connection.commit()


def _ensure_app_config_table(connection: turso.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS app_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )


def _ensure_master_resumes_table(connection: turso.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS master_resumes (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            content_sha256 TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )


def _ensure_cover_letter_examples_table(connection: turso.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS cover_letter_examples (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            content_sha256 TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_cover_letter_examples_updated_at
            ON cover_letter_examples (updated_at)
        """
    )


def _ensure_company_browser_wait_column(connection: turso.Connection) -> None:
    company_columns = connection.execute("PRAGMA table_info(companies)").fetchall()
    existing_columns = {row["name"] for row in company_columns}
    if "browser_extra_wait_ms" not in existing_columns:
        connection.execute(
            "ALTER TABLE companies ADD COLUMN browser_extra_wait_ms INTEGER NOT NULL DEFAULT 0"
        )


def _ensure_role_information_columns(connection: turso.Connection) -> None:
    role_columns = connection.execute("PRAGMA table_info(roles)").fetchall()
    existing_columns = {row["name"] for row in role_columns}
    columns = {
        "description": "TEXT",
        "posting_id": "TEXT",
    }
    for column_name, definition in columns.items():
        if column_name not in existing_columns:
            connection.execute(f"ALTER TABLE roles ADD COLUMN {column_name} {definition}")


def _ensure_role_discovery_assessment_columns(connection: turso.Connection) -> None:
    role_discovery_columns = connection.execute(
        "PRAGMA table_info(role_discovery_attempts)"
    ).fetchall()
    existing_columns = {row["name"] for row in role_discovery_columns}
    columns = {
        "assessment_is_role": "INTEGER CHECK (assessment_is_role IN (0, 1))",
        "assessment_is_closed": "INTEGER CHECK (assessment_is_closed IN (0, 1))",
        "assessment_confidence": "REAL",
        "assessment_location": "TEXT",
        "assessment_description": "TEXT",
        "assessment_posting_id": "TEXT",
        "assessment_extraction_method": "TEXT",
        "assessment_rejection_reason": "TEXT",
        "assessment_reasons_json": "TEXT NOT NULL DEFAULT '[]'",
    }
    for column_name, definition in columns.items():
        if column_name not in existing_columns:
            connection.execute(
                f"ALTER TABLE role_discovery_attempts ADD COLUMN {column_name} {definition}"
            )


def _backfill_legacy_company_career_pages(connection: turso.Connection) -> None:
    company_columns = connection.execute("PRAGMA table_info(companies)").fetchall()
    if not any(row["name"] == "careers_url" for row in company_columns):
        return

    connection.execute(
        """
        INSERT OR IGNORE INTO company_career_pages (company_id, url, label)
        SELECT id, careers_url, 'Main'
        FROM companies
        WHERE careers_url IS NOT NULL
            AND careers_url != ''
        """
    )


def ensure_initialized() -> None:
    with connect() as connection:
        run_migrations(connection)
