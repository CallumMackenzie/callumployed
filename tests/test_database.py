import os
import sqlite3
import subprocess
import sys

from callumployed.data import db


def test_connection_context_closes_connection() -> None:
    with db.connect(":memory:") as connection:
        connection.execute("SELECT 1")

    try:
        connection.execute("SELECT 1")
    except sqlite3.ProgrammingError:
        pass
    else:
        raise AssertionError("database connection remained open after context exit")


def test_separate_process_can_use_database_while_connection_is_open(tmp_path) -> None:
    database = tmp_path / "multiprocess.sqlite3"
    with db.connect(database) as frontend_connection:
        frontend_connection.execute("CREATE TABLE values_for_test (value TEXT)")
        frontend_connection.commit()

        environment = os.environ.copy()
        environment[db.DATABASE_PATH_ENV] = str(database)
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "from callumployed.data import db; "
                    "connection = db.connect(); "
                    "connection.execute(\"INSERT INTO values_for_test VALUES ('cli')\"); "
                    "connection.commit(); "
                    "connection.close()"
                ),
            ],
            capture_output=True,
            check=False,
            env=environment,
            text=True,
            timeout=5,
        )

        assert result.returncode == 0, result.stderr
        saved_value = frontend_connection.execute(
            "SELECT value FROM values_for_test"
        ).fetchone()
        assert saved_value is not None
        assert saved_value[0] == "cli"
