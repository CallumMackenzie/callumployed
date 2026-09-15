from __future__ import annotations

import json
import sqlite3
from typing import Any

from callumployed.central.normalization import role_identity

CENTRAL_LINK_REPAIR_KEY = "central_ats_identity_repair_v1"

_STATUS_RANK = {
    "offer": 90,
    "interview": 80,
    "OA": 70,
    "applied": 60,
    "rejected": 55,
    "closed": 40,
    "interested": 30,
    "disinterested": 20,
    "archived": 10,
    "discovered": 0,
}


def repair_local_integrity(connection: sqlite3.Connection) -> None:
    connection.execute("SAVEPOINT local_integrity_repair")
    try:
        _invalidate_legacy_central_links(connection)
        _ensure_role_identities(connection)
    except Exception:
        connection.execute("ROLLBACK TO local_integrity_repair")
        connection.execute("RELEASE local_integrity_repair")
        raise
    connection.execute("RELEASE local_integrity_repair")


def reassign_role_to_company(
    connection: sqlite3.Connection, role_id: int, company_id: int
) -> tuple[int, bool]:
    role = connection.execute("SELECT * FROM roles WHERE id = ?", (role_id,)).fetchone()
    if role is None:
        raise LookupError(f"role not found: {role_id}")
    if int(role["company_id"]) == company_id:
        return role_id, False
    collision = connection.execute(
        "SELECT * FROM roles WHERE company_id = ? AND role_url = ? AND id != ?",
        (company_id, role["role_url"], role_id),
    ).fetchone()
    if collision is None:
        connection.execute(
            "UPDATE roles SET company_id = ?, updated_at = datetime('now') WHERE id = ?",
            (company_id, role_id),
        )
        return role_id, False

    survivor = max((role, collision), key=_survivor_key)
    duplicate = collision if survivor["id"] == role["id"] else role
    _merge_role(connection, int(survivor["id"]), int(duplicate["id"]))
    connection.execute(
        "UPDATE roles SET company_id = ?, updated_at = datetime('now') WHERE id = ?",
        (company_id, survivor["id"]),
    )
    return int(survivor["id"]), True


def _invalidate_legacy_central_links(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS migration_state (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            completed_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    repaired = connection.execute(
        "SELECT value FROM migration_state WHERE key = ?",
        (CENTRAL_LINK_REPAIR_KEY,),
    ).fetchone()
    if repaired is not None:
        return
    connection.execute("DELETE FROM company_career_pages WHERE label = 'Central' COLLATE NOCASE")
    connection.execute(
        """
        UPDATE companies
        SET central_company_id = NULL,
            canonical_domain = NULL,
            normalized_name = NULL,
            central_sync_status = 'pending',
            central_sync_error = NULL,
            central_matched_at = NULL,
            updated_at = datetime('now')
        WHERE central_company_id IS NOT NULL
           OR central_sync_status != 'pending'
        """
    )
    connection.execute(
        "INSERT INTO migration_state (key, value) VALUES (?, 'completed')",
        (CENTRAL_LINK_REPAIR_KEY,),
    )


def _ensure_role_identities(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS role_identities (
            identity TEXT PRIMARY KEY,
            role_id INTEGER NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
        )
        """
    )
    roles = connection.execute("SELECT * FROM roles ORDER BY id").fetchall()
    grouped: dict[str, list[sqlite3.Row]] = {}
    for role in roles:
        identity = role_identity(role["role_url"], role["posting_id"])
        if identity is not None:
            grouped.setdefault(identity, []).append(role)

    connection.execute("DELETE FROM role_identities")
    for identity, duplicates in grouped.items():
        survivor = max(duplicates, key=_survivor_key)
        for duplicate in duplicates:
            if duplicate["id"] != survivor["id"]:
                _merge_role(connection, int(survivor["id"]), int(duplicate["id"]))
        connection.execute(
            "INSERT INTO role_identities (identity, role_id) VALUES (?, ?)",
            (identity, survivor["id"]),
        )


def _survivor_key(role: sqlite3.Row) -> tuple[int, int, str, int]:
    keys = set(role.keys())
    owned_fields = sum(
        bool(role[field]) for field in ("notes", "description", "posting_id") if field in keys
    )
    return (
        _STATUS_RANK.get(str(role["role_status"]), -1),
        owned_fields,
        str(role["updated_at"] or ""),
        -int(role["id"]),
    )


def _merge_role(connection: sqlite3.Connection, survivor_id: int, duplicate_id: int) -> None:
    survivor = connection.execute("SELECT * FROM roles WHERE id = ?", (survivor_id,)).fetchone()
    duplicate = connection.execute("SELECT * FROM roles WHERE id = ?", (duplicate_id,)).fetchone()
    if survivor is None or duplicate is None:
        return

    _merge_role_context_vectors(connection, survivor_id, duplicate_id)
    _merge_autoprep_jobs(connection, survivor_id, duplicate_id)
    for table in ("application_answers", "autoprep_job_archives"):
        if _table_exists(connection, table):
            connection.execute(
                f"UPDATE {table} SET role_id = ? WHERE role_id = ?",
                (survivor_id, duplicate_id),
            )
    for table in ("events", "role_discovery_attempts"):
        connection.execute(
            f"UPDATE {table} SET role_id = ? WHERE role_id = ?",
            (survivor_id, duplicate_id),
        )
    connection.execute(
        """
        INSERT INTO events (
            company_id, role_id, event_type, old_status, new_status, source, summary
        ) VALUES (?, ?, 'role_reconciled', ?, ?, 'manual', ?)
        """,
        (
            survivor["company_id"],
            survivor_id,
            duplicate["role_status"],
            survivor["role_status"],
            f"Merged duplicate role #{duplicate_id} into role #{survivor_id}.",
        ),
    )
    connection.execute(
        "UPDATE resume_feedback_history SET role_id = ?, company_id = ? WHERE role_id = ?",
        (survivor_id, survivor["company_id"], duplicate_id),
    )

    notes = _merge_text(survivor["notes"], duplicate["notes"])
    description = survivor["description"] or duplicate["description"]
    location = survivor["location"] or duplicate["location"]
    posting_id = survivor["posting_id"] or duplicate["posting_id"]
    central_role_id = survivor["central_role_id"] or duplicate["central_role_id"]
    first_seen_at = min(str(survivor["first_seen_at"]), str(duplicate["first_seen_at"]))
    last_seen_at = max(str(survivor["last_seen_at"]), str(duplicate["last_seen_at"]))

    connection.execute("DELETE FROM roles WHERE id = ?", (duplicate_id,))
    connection.execute(
        """
        UPDATE roles
        SET notes = ?, description = ?, location = ?, posting_id = ?, central_role_id = ?,
            first_seen_at = ?, last_seen_at = ?, updated_at = datetime('now')
        WHERE id = ?
        """,
        (
            notes,
            description,
            location,
            posting_id,
            central_role_id,
            first_seen_at,
            last_seen_at,
            survivor_id,
        ),
    )


def _merge_role_context_vectors(
    connection: sqlite3.Connection, survivor_id: int, duplicate_id: int
) -> None:
    if not _table_exists(connection, "role_context_vectors"):
        return
    connection.execute(
        """
        INSERT OR IGNORE INTO role_context_vectors (
            role_id, chunk_index, label, content, content_sha256, vector_json, updated_at
        )
        SELECT ?, chunk_index, label, content, content_sha256, vector_json, updated_at
        FROM role_context_vectors WHERE role_id = ?
        """,
        (survivor_id, duplicate_id),
    )
    connection.execute("DELETE FROM role_context_vectors WHERE role_id = ?", (duplicate_id,))


def _merge_autoprep_jobs(
    connection: sqlite3.Connection, survivor_id: int, duplicate_id: int
) -> None:
    if not _table_exists(connection, "autoprep_jobs"):
        return
    survivor_job = connection.execute(
        "SELECT * FROM autoprep_jobs WHERE role_id = ?", (survivor_id,)
    ).fetchone()
    duplicate_job = connection.execute(
        "SELECT * FROM autoprep_jobs WHERE role_id = ?", (duplicate_id,)
    ).fetchone()
    if duplicate_job is None:
        return
    if survivor_job is None:
        connection.execute(
            "UPDATE autoprep_jobs SET role_id = ? WHERE id = ?",
            (survivor_id, duplicate_job["id"]),
        )
        return

    if _table_exists(connection, "autoprep_job_archives"):
        snapshot: dict[str, Any] = dict(duplicate_job)
        for table in ("autoprep_retries", "autoprep_regenerations"):
            if _table_exists(connection, table):
                snapshot[table] = [
                    dict(row)
                    for row in connection.execute(
                        f"SELECT * FROM {table} WHERE job_id = ? ORDER BY id",
                        (duplicate_job["id"],),
                    ).fetchall()
                ]
        connection.execute(
            """
            INSERT OR IGNORE INTO autoprep_job_archives (job_id, role_id, snapshot_json, reason)
            VALUES (?, ?, ?, 'duplicate role reconciled')
            """,
            (duplicate_job["id"], survivor_id, json.dumps(snapshot, sort_keys=True)),
        )
    connection.execute("DELETE FROM autoprep_jobs WHERE id = ?", (duplicate_job["id"],))


def _merge_text(primary: object, secondary: object) -> str | None:
    values = [str(value).strip() for value in (primary, secondary) if value and str(value).strip()]
    return "\n\n--- merged duplicate ---\n\n".join(dict.fromkeys(values)) or None


def _table_exists(connection: sqlite3.Connection, table: str) -> bool:
    return (
        connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)
        ).fetchone()
        is not None
    )
