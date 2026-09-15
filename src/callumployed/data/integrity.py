from __future__ import annotations

import sqlite3

from callumployed.central.normalization import role_identity

CENTRAL_LINK_REPAIR_KEY = "central_ats_identity_repair_v1"

_STATUS_RANK = {
    "offer": 90,
    "rejected": 85,
    "interview": 80,
    "oa": 70,
    "applied": 60,
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
    return role_id, False


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
    for identity, candidates in grouped.items():
        owner = max(candidates, key=_survivor_key)
        connection.execute(
            "INSERT INTO role_identities (identity, role_id) VALUES (?, ?)",
            (identity, owner["id"]),
        )


def _survivor_key(role: sqlite3.Row) -> tuple[int, int, str, int]:
    keys = set(role.keys())
    owned_fields = sum(
        bool(role[field]) for field in ("notes", "description", "posting_id") if field in keys
    )
    return (
        _STATUS_RANK.get(str(role["role_status"]).casefold(), -1),
        owned_fields,
        str(role["updated_at"] or ""),
        -int(role["id"]),
    )
