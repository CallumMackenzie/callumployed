import os
import sqlite3
from pathlib import Path
from types import TracebackType
from typing import Literal

from platformdirs import user_data_path

ROOT = Path(__file__).resolve().parents[3]
MIGRATIONS_DIR = ROOT / "migrations"
DATABASE_PATH_ENV = "CALLUMPLOYED_DATABASE_PATH"


class _ClosingConnection(sqlite3.Connection):
    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        try:
            return super().__exit__(exception_type, exception, traceback)
        finally:
            self.close()


def default_database_path() -> Path:
    return user_data_path("callumployed", appauthor=False) / "callumployed.sqlite3"


def connect(database: str | Path | None = None) -> sqlite3.Connection:
    configured_database = database or os.environ.get(DATABASE_PATH_ENV)
    database_path = default_database_path() if configured_database is None else configured_database
    if database_path != ":memory:":
        Path(database_path).expanduser().parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(database_path), timeout=10, factory=_ClosingConnection)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    if database_path != ":memory:":
        connection.execute("PRAGMA journal_mode = WAL")
    return connection


def run_migrations(connection: sqlite3.Connection) -> None:
    for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
        connection.executescript(migration.read_text())
    _ensure_app_config_table(connection)
    _ensure_master_resumes_table(connection)
    _ensure_cover_letter_examples_table(connection)
    _ensure_cover_letter_example_vectors_table(connection)
    _ensure_experience_notes_table(connection)
    _ensure_role_context_vectors_table(connection)
    _ensure_resume_feedback_history_table(connection)
    _ensure_company_is_active_column(connection)
    _ensure_company_browser_wait_column(connection)
    _ensure_company_central_columns(connection)
    _ensure_role_information_columns(connection)
    _ensure_role_central_columns(connection)
    _ensure_role_discovery_assessment_columns(connection)
    _remove_prepared_role_status(connection)
    _backfill_legacy_company_career_pages(connection)
    connection.commit()


def _ensure_app_config_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS app_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )


def _ensure_master_resumes_table(connection: sqlite3.Connection) -> None:
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


def _ensure_cover_letter_examples_table(connection: sqlite3.Connection) -> None:
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


def _ensure_cover_letter_example_vectors_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS cover_letter_example_vectors (
            cover_letter_example_id INTEGER PRIMARY KEY,
            knowledge_text TEXT NOT NULL,
            vector_json TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (cover_letter_example_id) REFERENCES cover_letter_examples (id)
                ON DELETE CASCADE
        )
        """
    )


def _ensure_experience_notes_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS experience_notes (
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
        CREATE INDEX IF NOT EXISTS idx_experience_notes_updated_at
            ON experience_notes (updated_at)
        """
    )


def _ensure_role_context_vectors_table(connection: sqlite3.Connection) -> None:
    """Persist deterministic, role-local retrieval chunks for document generation."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS role_context_vectors (
            role_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            label TEXT NOT NULL,
            content TEXT NOT NULL,
            content_sha256 TEXT NOT NULL,
            vector_json TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            PRIMARY KEY (role_id, chunk_index),
            FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_role_context_vectors_role_updated
            ON role_context_vectors (role_id, updated_at)
        """
    )


def _ensure_resume_feedback_history_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS resume_feedback_history (
            id INTEGER PRIMARY KEY,
            role_id INTEGER,
            company_id INTEGER,
            role_title TEXT NOT NULL,
            role_url TEXT,
            role_description TEXT,
            feedback_index INTEGER NOT NULL,
            feedback_label TEXT,
            feedback_title TEXT NOT NULL,
            feedback_detail TEXT NOT NULL,
            target_text TEXT,
            replacement_text TEXT,
            latex_addition TEXT,
            response TEXT NOT NULL CHECK (response IN ('accepted', 'ignored')),
            comment TEXT,
            knowledge_text TEXT NOT NULL,
            vector_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE SET NULL,
            FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE SET NULL
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_resume_feedback_history_created_at
            ON resume_feedback_history (created_at)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_resume_feedback_history_role_id
            ON resume_feedback_history (role_id)
        """
    )


def _ensure_company_browser_wait_column(connection: sqlite3.Connection) -> None:
    company_columns = connection.execute("PRAGMA table_info(companies)").fetchall()
    existing_columns = {row["name"] for row in company_columns}
    if "browser_extra_wait_ms" not in existing_columns:
        connection.execute(
            "ALTER TABLE companies ADD COLUMN browser_extra_wait_ms INTEGER NOT NULL DEFAULT 0"
        )


def _ensure_company_central_columns(connection: sqlite3.Connection) -> None:
    company_columns = connection.execute("PRAGMA table_info(companies)").fetchall()
    existing_columns = {row["name"] for row in company_columns}
    columns = {
        "central_company_id": "TEXT",
        "canonical_domain": "TEXT",
        "normalized_name": "TEXT",
        "central_sync_status": "TEXT NOT NULL DEFAULT 'pending'",
        "central_sync_error": "TEXT",
        "central_matched_at": "TEXT",
    }
    for column_name, definition in columns.items():
        if column_name not in existing_columns:
            connection.execute(f"ALTER TABLE companies ADD COLUMN {column_name} {definition}")
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_companies_central_company_id
            ON companies (central_company_id)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_companies_central_sync_status
            ON companies (central_sync_status)
        """
    )


def _ensure_company_is_active_column(connection: sqlite3.Connection) -> None:
    company_columns = connection.execute("PRAGMA table_info(companies)").fetchall()
    existing_columns = {row["name"] for row in company_columns}
    if "is_active" not in existing_columns:
        connection.execute(
            "ALTER TABLE companies ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1 "
            "CHECK (is_active IN (0, 1))"
        )


def _ensure_role_information_columns(connection: sqlite3.Connection) -> None:
    role_columns = connection.execute("PRAGMA table_info(roles)").fetchall()
    existing_columns = {row["name"] for row in role_columns}
    columns = {
        "description": "TEXT",
        "posting_id": "TEXT",
    }
    for column_name, definition in columns.items():
        if column_name not in existing_columns:
            connection.execute(f"ALTER TABLE roles ADD COLUMN {column_name} {definition}")


def _ensure_role_central_columns(connection: sqlite3.Connection) -> None:
    role_columns = connection.execute("PRAGMA table_info(roles)").fetchall()
    existing_columns = {row["name"] for row in role_columns}
    columns = {
        "central_role_id": "TEXT",
        "central_source": "TEXT NOT NULL DEFAULT 'local'",
        "central_synced_at": "TEXT",
    }
    for column_name, definition in columns.items():
        if column_name not in existing_columns:
            connection.execute(f"ALTER TABLE roles ADD COLUMN {column_name} {definition}")
    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_roles_central_role_id
            ON roles (central_role_id)
            WHERE central_role_id IS NOT NULL
        """
    )


def _ensure_role_discovery_assessment_columns(connection: sqlite3.Connection) -> None:
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


def _remove_prepared_role_status(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        UPDATE roles
        SET role_status = 'interested',
            updated_at = datetime('now')
        WHERE role_status = 'prepared'
        """
    )


def _backfill_legacy_company_career_pages(connection: sqlite3.Connection) -> None:
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
