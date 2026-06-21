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
    _backfill_legacy_company_career_pages(connection)
    connection.commit()


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
