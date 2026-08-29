from __future__ import annotations

import hashlib
import json
import logging
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import suppress
from typing import Any, Literal

import turso

from callumployed.data import db

DocumentKind = Literal["resume", "cover_letter"]
LOGGER = logging.getLogger(__name__)
DEFAULT_COVER_LETTER_REGENERATION_INSTRUCTION = (
    "Refresh this cover letter using the current role description and approved application "
    "materials. Preserve source fidelity and professional one-page formatting."
)
BULK_COVER_LETTER_REGENERATION_INSTRUCTION = (
    DEFAULT_COVER_LETTER_REGENERATION_INSTRUCTION
)

_RESUME_STATUSES = {
    "queued",
    "generating_tweaks",
    "regenerating",
    "ready",
    "failed",
    "interrupted",
}
_COVER_LETTER_STATUSES = {
    "queued",
    "generating",
    "ready",
    "failed",
    "interrupted",
}
_TERMINAL_DOCUMENT_STATUSES = {"ready", "failed", "interrupted"}


class AutoprepConflictError(ValueError):
    pass


class AutoprepCoordinator:
    """Claim persisted role jobs and run a bounded number outside request threads."""

    def __init__(self, process_job: Any, *, max_workers: int = 2) -> None:
        self.process_job = process_job
        self.max_workers = max_workers
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._claim_lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._executor: ThreadPoolExecutor | None = None
        self._futures: set[Future[Any]] = set()

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._executor = ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="callumployed-autoprep",
        )
        self._thread = threading.Thread(
            target=self._run,
            name="callumployed-autoprep-coordinator",
            daemon=True,
        )
        self._thread.start()

    def wake(self) -> None:
        self._wake.set()

    def stop_claiming(self) -> None:
        """Stop accepting persisted work without waiting for active role workers."""
        self._stop.set()
        self._wake.set()
        # Wait for any claim/submit decision already in progress. Once this
        # lock is acquired, no queued job can become a new worker future.
        with self._claim_lock:
            pass
        if self._thread is not None:
            self._thread.join(timeout=5)

    def wait_for_workers(self) -> None:
        """Wait until active workers have recorded their final durable state."""
        if self._executor is not None:
            # Every submitted future owns a persisted running claim. Let queued
            # executor futures start so the stopped Hermes runner can mark them
            # Interrupted; canceling them would strand the claim as running.
            self._executor.shutdown(wait=True, cancel_futures=False)

    def stop(self) -> None:
        self.stop_claiming()
        self.wait_for_workers()

    def _run(self) -> None:
        while not self._stop.is_set():
            self._futures = {future for future in self._futures if not future.done()}
            while len(self._futures) < self.max_workers and not self._stop.is_set():
                job: dict[str, Any] | None = None
                with self._claim_lock:
                    if self._stop.is_set():
                        break
                    try:
                        with db.connect() as connection:
                            ensure_autoprep_schema(connection)
                            job = claim_next_autoprep_job(connection)
                    except Exception:  # noqa: BLE001 - keep the durable queue alive.
                        LOGGER.exception("Autoprep coordinator could not claim queued work")
                        break
                    if job is None:
                        break
                    if self._stop.is_set():
                        with db.connect() as connection:
                            release_autoprep_claim(connection, int(job["id"]))
                        break
                    if self._executor is None:
                        return
                    future = self._executor.submit(self._process_safely, int(job["id"]))
                    self._futures.add(future)
            self._wake.wait(timeout=0.5)
            self._wake.clear()

    def _process_safely(self, job_id: int) -> None:
        try:
            self.process_job(job_id)
        except Exception as error:  # noqa: BLE001 - persist worker failures for retry UI.
            with suppress(Exception), db.connect() as connection:
                ensure_autoprep_schema(connection)
                fail_running_autoprep_documents(
                    connection,
                    job_id,
                    error=_safe_worker_error(error),
                )
        finally:
            self._wake.set()


def ensure_autoprep_schema(connection: turso.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS autoprep_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idempotency_key TEXT NOT NULL UNIQUE,
            request_hash TEXT NOT NULL,
            role_ids_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS autoprep_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER NOT NULL UNIQUE,
            overall_status TEXT NOT NULL DEFAULT 'queued',
            worker_state TEXT NOT NULL DEFAULT 'queued',
            resume_status TEXT NOT NULL DEFAULT 'queued',
            cover_letter_status TEXT NOT NULL DEFAULT 'queued',
            -- Legacy Hermes session references are retained for historical jobs only.
            -- Direct LangChain generation never reads or writes these values.
            resume_session_id TEXT,
            cover_letter_session_id TEXT,
            resume_artifact_path TEXT,
            cover_letter_artifact_path TEXT,
            artifact_directory TEXT,
            resume_latex TEXT,
            resume_instruction TEXT,
            cover_letter_instruction TEXT,
            resume_error TEXT,
            cover_letter_error TEXT,
            resume_attempt INTEGER NOT NULL DEFAULT 1,
            cover_letter_attempt INTEGER NOT NULL DEFAULT 1,
            queued_at TEXT NOT NULL DEFAULT (datetime('now')),
            started_at TEXT,
            completed_at TEXT,
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_autoprep_jobs_worker
            ON autoprep_jobs(worker_state, queued_at, id);

        CREATE TABLE IF NOT EXISTS autoprep_retries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idempotency_key TEXT NOT NULL UNIQUE,
            job_id INTEGER NOT NULL,
            document_kind TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (job_id) REFERENCES autoprep_jobs(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS autoprep_regenerations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idempotency_key TEXT NOT NULL UNIQUE,
            job_id INTEGER NOT NULL,
            document_kind TEXT NOT NULL,
            instruction_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (job_id) REFERENCES autoprep_jobs(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS autoprep_bulk_cover_letter_requests (
            idempotency_key TEXT PRIMARY KEY,
            result_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """
    )
    job_columns = {
        str(row["name"])
        for row in connection.execute("PRAGMA table_info(autoprep_jobs)").fetchall()
    }
    for column_name in ("resume_instruction", "cover_letter_instruction"):
        if column_name not in job_columns:
            connection.execute(f"ALTER TABLE autoprep_jobs ADD COLUMN {column_name} TEXT")
    connection.commit()


def enqueue_autoprep_jobs(
    connection: turso.Connection,
    role_ids: list[int],
    *,
    idempotency_key: str,
) -> list[dict[str, Any]]:
    normalized_role_ids = sorted(set(role_ids))
    if not normalized_role_ids:
        raise ValueError("Select at least one Interested role.")
    clean_key = idempotency_key.strip()
    if not clean_key:
        raise ValueError("An idempotency key is required.")
    request_hash = _request_hash(normalized_role_ids)

    try:
        connection.execute("BEGIN IMMEDIATE")
        existing_request = connection.execute(
            "SELECT request_hash, role_ids_json FROM autoprep_requests WHERE idempotency_key = ?",
            (clean_key,),
        ).fetchone()
        if existing_request is not None:
            if str(existing_request["request_hash"]) != request_hash:
                raise AutoprepConflictError("This Autoprep submission key was already used.")
            saved_role_ids = [int(value) for value in json.loads(existing_request["role_ids_json"])]
            connection.commit()
            return _jobs_for_role_ids(connection, saved_role_ids)

        placeholders = ", ".join("?" for _ in normalized_role_ids)
        rows = connection.execute(
            f"SELECT id, role_status FROM roles WHERE id IN ({placeholders})",  # noqa: S608
            tuple(normalized_role_ids),
        ).fetchall()
        statuses = {int(row["id"]): str(row["role_status"]) for row in rows}
        invalid = [
            role_id
            for role_id in normalized_role_ids
            if statuses.get(role_id) != "interested"
        ]
        if invalid:
            raise ValueError("Autoprep can only queue roles currently marked Interested.")

        connection.execute(
            """
            INSERT INTO autoprep_requests (idempotency_key, request_hash, role_ids_json)
            VALUES (?, ?, ?)
            """,
            (clean_key, request_hash, json.dumps(normalized_role_ids)),
        )
        for role_id in normalized_role_ids:
            connection.execute(
                """
                INSERT INTO autoprep_jobs (role_id)
                VALUES (?)
                ON CONFLICT(role_id) DO NOTHING
                """,
                (role_id,),
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    return _jobs_for_role_ids(connection, normalized_role_ids)


def list_autoprep_jobs(
    connection: turso.Connection,
    *,
    include_applied: bool = False,
) -> list[dict[str, Any]]:
    where_clause = "" if include_applied else "WHERE r.role_status = 'interested'"
    rows = connection.execute(
        f"""
        SELECT
            j.*,
            r.title,
            r.role_url,
            r.location,
            r.notes,
            r.description,
            r.posting_id,
            r.first_seen_at,
            r.last_seen_at,
            r.role_status,
            r.created_at AS role_created_at,
            r.updated_at AS role_updated_at,
            c.name AS company_name
        FROM autoprep_jobs AS j
        JOIN roles AS r ON r.id = j.role_id
        JOIN companies AS c ON c.id = r.company_id
        {where_clause}
        ORDER BY j.queued_at ASC, j.id ASC
        """  # noqa: S608
    ).fetchall()
    return [_job_payload(row) for row in rows]


def list_interested_autoprep_roles(connection: turso.Connection) -> list[dict[str, Any]]:
    rows = connection.execute(
        """
        SELECT
            r.id,
            r.title,
            r.location,
            r.created_at AS date_added,
            r.updated_at,
            c.name AS company_name,
            j.overall_status AS preparation_status,
            j.resume_status,
            j.cover_letter_status
        FROM roles AS r
        JOIN companies AS c ON c.id = r.company_id
        LEFT JOIN autoprep_jobs AS j ON j.role_id = r.id
        WHERE r.role_status = 'interested'
        ORDER BY r.created_at DESC, r.id DESC
        """
    ).fetchall()
    return [dict(row) for row in rows]


def get_autoprep_job(connection: turso.Connection, job_id: int) -> dict[str, Any]:
    row = connection.execute(
        """
        SELECT
            j.*,
            r.title,
            r.role_url,
            r.location,
            r.notes,
            r.description,
            r.posting_id,
            r.first_seen_at,
            r.last_seen_at,
            r.role_status,
            r.created_at AS role_created_at,
            r.updated_at AS role_updated_at,
            c.name AS company_name
        FROM autoprep_jobs AS j
        JOIN roles AS r ON r.id = j.role_id
        JOIN companies AS c ON c.id = r.company_id
        WHERE j.id = ?
        """,
        (job_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"Autoprep job {job_id} was not found.")
    return _job_payload(row)


def get_role_autoprep_job(connection: turso.Connection, role_id: int) -> dict[str, Any] | None:
    row = connection.execute(
        "SELECT id FROM autoprep_jobs WHERE role_id = ?",
        (role_id,),
    ).fetchone()
    return get_autoprep_job(connection, int(row["id"])) if row is not None else None


def get_autoprep_resume_latex(connection: turso.Connection, job_id: int) -> str | None:
    row = connection.execute(
        "SELECT resume_latex FROM autoprep_jobs WHERE id = ?",
        (job_id,),
    ).fetchone()
    if row is None or row["resume_latex"] is None:
        return None
    return str(row["resume_latex"])


def claim_next_autoprep_job(connection: turso.Connection) -> dict[str, Any] | None:
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            """
            SELECT id
            FROM autoprep_jobs
            WHERE worker_state = 'queued'
            ORDER BY queued_at ASC, id ASC
            LIMIT 1
            """
        ).fetchone()
        if row is None:
            connection.commit()
            return None
        job_id = int(row["id"])
        connection.execute(
            """
            UPDATE autoprep_jobs
            SET worker_state = 'running',
                started_at = COALESCE(started_at, datetime('now')),
                updated_at = datetime('now')
            WHERE id = ? AND worker_state = 'queued'
            """,
            (job_id,),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    return get_autoprep_job(connection, job_id)


def release_autoprep_claim(connection: turso.Connection, job_id: int) -> None:
    """Return a claim to the durable queue when shutdown wins before submission."""
    connection.execute(
        """
        UPDATE autoprep_jobs
        SET worker_state = 'queued', updated_at = datetime('now')
        WHERE id = ? AND worker_state = 'running'
        """,
        (job_id,),
    )
    connection.commit()


def mark_autoprep_document(
    connection: turso.Connection,
    job_id: int,
    document_kind: DocumentKind,
    status: str,
    *,
    session_id: str | None = None,
    artifact_path: str | None = None,
    artifact_directory: str | None = None,
    resume_latex: str | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    _validate_document_status(document_kind, status)
    prefix = _document_prefix(document_kind)
    assignments = [f"{prefix}_status = ?", f"{prefix}_error = ?", "updated_at = datetime('now')"]
    values: list[object] = [status, error]
    if session_id is not None:
        assignments.append(f"{prefix}_session_id = ?")
        values.append(session_id)
    if artifact_path is not None:
        assignments.append(f"{prefix}_artifact_path = ?")
        values.append(artifact_path)
    if artifact_directory is not None:
        assignments.append("artifact_directory = ?")
        values.append(artifact_directory)
    if document_kind == "resume" and resume_latex is not None:
        assignments.append("resume_latex = ?")
        values.append(resume_latex)
    values.append(job_id)
    connection.execute(
        f"UPDATE autoprep_jobs SET {', '.join(assignments)} WHERE id = ?",  # noqa: S608
        tuple(values),
    )
    _refresh_overall_status(connection, job_id)
    connection.commit()
    return get_autoprep_job(connection, job_id)


def finish_autoprep_worker(connection: turso.Connection, job_id: int) -> dict[str, Any]:
    _refresh_overall_status(connection, job_id)
    connection.execute(
        """
        UPDATE autoprep_jobs
        SET worker_state = 'idle',
            completed_at = CASE
                WHEN overall_status IN ('ready', 'partially_complete', 'failed', 'interrupted')
                THEN datetime('now')
                ELSE completed_at
            END,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (job_id,),
    )
    connection.commit()
    return get_autoprep_job(connection, job_id)


def fail_running_autoprep_documents(
    connection: turso.Connection,
    job_id: int,
    *,
    error: str,
) -> dict[str, Any]:
    job = get_autoprep_job(connection, job_id)
    for document_kind in ("resume", "cover_letter"):
        status_key = f"{document_kind}_status"
        if job[status_key] not in _TERMINAL_DOCUMENT_STATUSES:
            mark_autoprep_document(
                connection,
                job_id,
                document_kind,
                "failed",
                error=error,
            )
            job = get_autoprep_job(connection, job_id)
    return finish_autoprep_worker(connection, job_id)


def retry_autoprep_document(
    connection: turso.Connection,
    role_id: int,
    document_kind: DocumentKind,
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    clean_key = idempotency_key.strip()
    if not clean_key:
        raise ValueError("An idempotency key is required.")
    prefix = _document_prefix(document_kind)
    try:
        connection.execute("BEGIN IMMEDIATE")
        job = get_role_autoprep_job(connection, role_id)
        if job is None:
            raise ValueError("No Autoprep job exists for this role.")
        existing = connection.execute(
            "SELECT job_id, document_kind FROM autoprep_retries WHERE idempotency_key = ?",
            (clean_key,),
        ).fetchone()
        if existing is not None:
            if (
                int(existing["job_id"]) != job["id"]
                or str(existing["document_kind"]) != document_kind
            ):
                raise AutoprepConflictError("This retry key was already used for another action.")
            connection.commit()
            return get_autoprep_job(connection, job["id"])

        # A document can fail while the same role worker is still preparing the
        # other document. Do not make that role claimable a second time until
        # the original worker has finished and made the partial state stable.
        # A queued worker has not been claimed yet, so a second failed sibling
        # may safely join the same pending role run.
        if job["worker_state"] not in {"idle", "queued"}:
            connection.commit()
            return job
        current_status = str(job[f"{prefix}_status"])
        if current_status == "ready" or current_status not in {"failed", "interrupted"}:
            connection.commit()
            return job
        connection.execute(
            """
            INSERT INTO autoprep_retries (idempotency_key, job_id, document_kind)
            VALUES (?, ?, ?)
            """,
            (clean_key, job["id"], document_kind),
        )
        connection.execute(
            f"""
            UPDATE autoprep_jobs
            SET {prefix}_status = 'queued',
                {prefix}_error = NULL,
                {prefix}_attempt = {prefix}_attempt + 1,
                overall_status = 'queued',
                worker_state = 'queued',
                completed_at = NULL,
                queued_at = datetime('now'),
                updated_at = datetime('now')
            WHERE id = ?
            """,  # noqa: S608
            (job["id"],),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    return get_autoprep_job(connection, job["id"])


def _queue_autoprep_regeneration_in_transaction(
    connection: turso.Connection,
    job: dict[str, Any],
    document_kind: DocumentKind,
    *,
    clean_instruction: str,
    clean_key: str,
) -> int:
    prefix = _document_prefix(document_kind)
    instruction_hash = hashlib.sha256(clean_instruction.encode()).hexdigest()
    existing = connection.execute(
        """
        SELECT job_id, document_kind, instruction_hash
        FROM autoprep_regenerations
        WHERE idempotency_key = ?
        """,
        (clean_key,),
    ).fetchone()
    if existing is not None:
        if (
            int(existing["job_id"]) != job["id"]
            or str(existing["document_kind"]) != document_kind
            or str(existing["instruction_hash"]) != instruction_hash
        ):
            raise AutoprepConflictError(
                "This regeneration key was already used for another action."
            )
        return int(existing["job_id"])
    if job["worker_state"] != "idle":
        raise AutoprepConflictError("This role is already being prepared.")
    if str(job[f"{prefix}_status"]) != "ready":
        raise AutoprepConflictError("Only a ready document can be regenerated.")
    connection.execute(
        """
        INSERT INTO autoprep_regenerations (
            idempotency_key, job_id, document_kind, instruction_hash
        ) VALUES (?, ?, ?, ?)
        """,
        (clean_key, job["id"], document_kind, instruction_hash),
    )
    connection.execute(
        f"""
        UPDATE autoprep_jobs
        SET {prefix}_status = 'queued',
            {prefix}_error = NULL,
            {prefix}_instruction = ?,
            {prefix}_attempt = {prefix}_attempt + 1,
            overall_status = 'queued',
            worker_state = 'queued',
            completed_at = NULL,
            queued_at = datetime('now'),
            updated_at = datetime('now')
        WHERE id = ?
        """,  # noqa: S608
        (clean_instruction, job["id"]),
    )
    return int(job["id"])


def queue_autoprep_regeneration(
    connection: turso.Connection,
    role_id: int,
    document_kind: DocumentKind,
    *,
    instruction: str,
    idempotency_key: str,
) -> dict[str, Any]:
    clean_key = idempotency_key.strip()
    clean_instruction = instruction.strip()
    if not clean_key:
        raise ValueError("An idempotency key is required.")
    if not clean_instruction:
        if document_kind == "cover_letter":
            clean_instruction = DEFAULT_COVER_LETTER_REGENERATION_INSTRUCTION
        else:
            raise ValueError("Add comments before regenerating the document.")
    if len(clean_instruction) > 4000:
        raise ValueError("Regeneration comments must be 4000 characters or fewer.")
    try:
        connection.execute("BEGIN IMMEDIATE")
        job = get_role_autoprep_job(connection, role_id)
        if job is None:
            raise ValueError("No Autoprep job exists for this role.")
        job_id = _queue_autoprep_regeneration_in_transaction(
            connection,
            job,
            document_kind,
            clean_instruction=clean_instruction,
            clean_key=clean_key,
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    return get_autoprep_job(connection, job_id)


def _bulk_cover_letter_result(
    connection: turso.Connection,
    saved: dict[str, Any],
) -> dict[str, Any]:
    queued_role_ids = [int(role_id) for role_id in saved["queued_role_ids"]]
    skipped = list(saved["skipped"])
    return {
        "requested_count": int(saved["requested_count"]),
        "queued_count": len(queued_role_ids),
        "skipped_count": len(skipped),
        "jobs": _jobs_for_role_ids(connection, queued_role_ids),
        "skipped": skipped,
    }


def get_latest_bulk_cover_letter_regeneration(
    connection: turso.Connection,
) -> dict[str, Any] | None:
    row = connection.execute(
        """
        SELECT idempotency_key, result_json, created_at
        FROM autoprep_bulk_cover_letter_requests
        ORDER BY created_at DESC, rowid DESC
        LIMIT 1
        """
    ).fetchone()
    if row is None:
        return None
    result = _bulk_cover_letter_result(connection, json.loads(str(row["result_json"])))
    result["idempotency_key"] = str(row["idempotency_key"])
    result["created_at"] = str(row["created_at"])
    return result


def queue_all_prepped_cover_letter_regenerations(
    connection: turso.Connection,
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    clean_key = idempotency_key.strip()
    if not clean_key:
        raise ValueError("An idempotency key is required.")
    try:
        connection.execute("BEGIN IMMEDIATE")
        existing = connection.execute(
            """
            SELECT result_json
            FROM autoprep_bulk_cover_letter_requests
            WHERE idempotency_key = ?
            """,
            (clean_key,),
        ).fetchone()
        if existing is not None:
            saved = json.loads(str(existing["result_json"]))
            connection.commit()
            return _bulk_cover_letter_result(connection, saved)

        prepped_jobs = list_autoprep_jobs(connection)
        queued_role_ids: list[int] = []
        skipped: list[dict[str, Any]] = []
        for job in prepped_jobs:
            try:
                _queue_autoprep_regeneration_in_transaction(
                    connection,
                    job,
                    "cover_letter",
                    clean_instruction=BULK_COVER_LETTER_REGENERATION_INSTRUCTION,
                    clean_key=f"{clean_key}-role-{job['role_id']}",
                )
                queued_role_ids.append(int(job["role_id"]))
            except (AutoprepConflictError, ValueError) as error:
                skipped.append(
                    {
                        "role_id": int(job["role_id"]),
                        "company_name": str(job["company_name"]),
                        "title": str(job["title"]),
                        "reason": str(error),
                    }
                )
        saved = {
            "requested_count": len(prepped_jobs),
            "queued_role_ids": queued_role_ids,
            "skipped": skipped,
        }
        connection.execute(
            """
            INSERT INTO autoprep_bulk_cover_letter_requests (idempotency_key, result_json)
            VALUES (?, ?)
            """,
            (clean_key, json.dumps(saved, separators=(",", ":"))),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    return _bulk_cover_letter_result(connection, saved)


def clear_autoprep_instruction(
    connection: turso.Connection,
    job_id: int,
    document_kind: DocumentKind,
) -> None:
    prefix = _document_prefix(document_kind)
    connection.execute(
        f"UPDATE autoprep_jobs SET {prefix}_instruction = NULL WHERE id = ?",  # noqa: S608
        (job_id,),
    )
    connection.commit()


def recover_interrupted_autoprep_jobs(connection: turso.Connection) -> int:
    rows = connection.execute(
        """
        SELECT id, resume_status, cover_letter_status
        FROM autoprep_jobs
        WHERE worker_state = 'running'
        """
    ).fetchall()
    for row in rows:
        job_id = int(row["id"])
        for document_kind in ("resume", "cover_letter"):
            prefix = _document_prefix(document_kind)
            if str(row[f"{prefix}_status"]) not in _TERMINAL_DOCUMENT_STATUSES:
                connection.execute(
                    f"""
                    UPDATE autoprep_jobs
                    SET {prefix}_status = 'interrupted',
                        {prefix}_error = 'Preparation was interrupted by an application restart.'
                    WHERE id = ?
                    """,  # noqa: S608
                    (job_id,),
                )
        _refresh_overall_status(connection, job_id)
        connection.execute(
            """
            UPDATE autoprep_jobs
            SET worker_state = 'idle', updated_at = datetime('now')
            WHERE id = ?
            """,
            (job_id,),
        )
    connection.commit()
    return len(rows)


def _jobs_for_role_ids(connection: turso.Connection, role_ids: list[int]) -> list[dict[str, Any]]:
    jobs_by_role: dict[int, dict[str, Any]] = {}
    for role_id in role_ids:
        job = get_role_autoprep_job(connection, role_id)
        if job is not None:
            jobs_by_role[role_id] = job
    return [jobs_by_role[role_id] for role_id in role_ids if role_id in jobs_by_role]


def _request_hash(role_ids: list[int]) -> str:
    canonical = json.dumps(role_ids, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _document_prefix(document_kind: DocumentKind | str) -> str:
    return "cover_letter" if document_kind == "cover_letter" else "resume"


def _validate_document_status(document_kind: DocumentKind, status: str) -> None:
    allowed = _COVER_LETTER_STATUSES if document_kind == "cover_letter" else _RESUME_STATUSES
    if status not in allowed:
        raise ValueError(f"Unsupported {document_kind} status: {status}")


def _refresh_overall_status(connection: turso.Connection, job_id: int) -> None:
    row = connection.execute(
        "SELECT resume_status, cover_letter_status FROM autoprep_jobs WHERE id = ?",
        (job_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"Autoprep job {job_id} was not found.")
    resume_status = str(row["resume_status"])
    cover_status = str(row["cover_letter_status"])
    overall_status = _derive_overall_status(resume_status, cover_status)
    connection.execute(
        """
        UPDATE autoprep_jobs
        SET overall_status = ?,
            completed_at = CASE WHEN ? = 'ready' THEN datetime('now') ELSE completed_at END,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (overall_status, overall_status, job_id),
    )


def _derive_overall_status(resume_status: str, cover_status: str) -> str:
    if resume_status == "ready" and cover_status == "ready":
        return "ready"
    if "ready" in {resume_status, cover_status} and (
        resume_status in {"failed", "interrupted"} or cover_status in {"failed", "interrupted"}
    ):
        return "partially_complete"
    if resume_status in {"failed", "interrupted"} and cover_status in {"failed", "interrupted"}:
        return "failed" if "failed" in {resume_status, cover_status} else "interrupted"
    if resume_status == "generating_tweaks":
        return "generating_resume_tweaks"
    if resume_status == "regenerating":
        return "regenerating_resume"
    if cover_status == "generating":
        return "generating_cover_letter"
    return "queued"


def _job_payload(row: Any) -> dict[str, Any]:
    payload = dict(row)
    payload.pop("resume_latex", None)
    # Preserve legacy session IDs in storage for auditability without exposing
    # them as active generation state in the API/UI.
    payload.pop("resume_session_id", None)
    payload.pop("cover_letter_session_id", None)
    payload["resume_available"] = bool(payload.get("resume_artifact_path"))
    payload["cover_letter_available"] = bool(payload.get("cover_letter_artifact_path"))
    return payload


def _safe_worker_error(error: Exception) -> str:
    detail = " ".join(str(error).strip().split())
    return (detail or "Autoprep generation failed.")[-1000:]
