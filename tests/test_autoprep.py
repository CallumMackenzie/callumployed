import json
import time
from pathlib import Path
from threading import Event, Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
from pypdf import PdfWriter

import callumployed.services.autoprep as autoprep_service
import callumployed.web.server as web_server
from callumployed.data import db
from callumployed.data.models import Company, Role, RoleStatus
from callumployed.data.repositories import (
    add_company,
    add_role,
    get_config_value,
    set_config_value,
    set_role_status,
    upsert_master_resume,
)
from callumployed.services.app_settings import APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY
from callumployed.services.autoprep import (
    AutoprepConflictError,
    AutoprepCoordinator,
    claim_next_autoprep_job,
    enqueue_autoprep_jobs,
    ensure_autoprep_schema,
    finish_autoprep_worker,
    get_autoprep_job,
    list_autoprep_jobs,
    mark_autoprep_document,
    queue_autoprep_regeneration,
    recover_interrupted_autoprep_jobs,
    release_autoprep_claim,
    retry_autoprep_document,
)
from callumployed.web.server import LocalThreadingHTTPServer, create_handler


def _interested_role(connection, *, company: str = "Acme", title: str = "Engineer") -> int:
    saved_company = add_company(connection, Company(name=company))
    assert saved_company.id is not None
    role = add_role(
        connection,
        Role(
            company_id=saved_company.id,
            title=title,
            role_url=f"https://example.com/{title.lower().replace(' ', '-')}",
            location="London",
            role_status=RoleStatus.INTERESTED,
            description="Build reliable Python services.",
        ),
    )
    assert role.id is not None
    return role.id


def test_enqueue_is_durable_and_idempotent(tmp_path: Path) -> None:
    database = tmp_path / "autoprep.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        first_role_id = _interested_role(connection, title="Backend Engineer")
        second_role_id = _interested_role(connection, company="Beta", title="Security Engineer")

        first = enqueue_autoprep_jobs(
            connection,
            [first_role_id, second_role_id],
            idempotency_key="attempt-1",
        )
        replay = enqueue_autoprep_jobs(
            connection,
            [second_role_id, first_role_id],
            idempotency_key="attempt-1",
        )
        repeated_selection = enqueue_autoprep_jobs(
            connection,
            [first_role_id, second_role_id],
            idempotency_key="attempt-2",
        )

        assert [item["id"] for item in replay] == [item["id"] for item in first]
        assert [item["id"] for item in repeated_selection] == [item["id"] for item in first]
        assert all(item["overall_status"] == "queued" for item in first)
        assert len(list_autoprep_jobs(connection)) == 2

        with pytest.raises(AutoprepConflictError):
            enqueue_autoprep_jobs(
                connection,
                [first_role_id],
                idempotency_key="attempt-1",
            )


def test_role_and_autoprep_enqueue_can_share_one_atomic_transaction(tmp_path: Path) -> None:
    database = tmp_path / "autoprep-atomic-role.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None

        connection.execute("BEGIN IMMEDIATE")
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Platform Engineer",
                role_url="https://example.com/platform-engineer",
                role_status=RoleStatus.INTERESTED,
            ),
            commit=False,
        )
        assert role.id is not None
        [job] = enqueue_autoprep_jobs(
            connection,
            [role.id],
            idempotency_key=f"explicit-role-{role.id}",
            manage_transaction=False,
        )
        assert job["worker_state"] == "queued"

        connection.rollback()
        assert connection.execute("SELECT COUNT(*) AS count FROM roles").fetchone()["count"] == 0
        assert (
            connection.execute("SELECT COUNT(*) AS count FROM autoprep_jobs").fetchone()["count"]
            == 0
        )
        autoprep_request_count = connection.execute(
            "SELECT COUNT(*) AS count FROM autoprep_requests"
        ).fetchone()["count"]
        assert autoprep_request_count == 0


def test_enqueue_rejects_roles_that_are_not_interested(tmp_path: Path) -> None:
    database = tmp_path / "autoprep-status.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        set_role_status(connection, role_id, RoleStatus.APPLIED, summary="Applied")

        with pytest.raises(ValueError, match="Interested"):
            enqueue_autoprep_jobs(connection, [role_id], idempotency_key="attempt")


def test_document_updates_can_share_one_atomic_transaction(tmp_path: Path) -> None:
    database = tmp_path / "autoprep-atomic-documents.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="atomic")

        mark_autoprep_document(
            connection,
            job["id"],
            "resume",
            "ready",
            artifact_path="/old/resume.pdf",
            artifact_directory="/old",
        )
        mark_autoprep_document(
            connection,
            job["id"],
            "cover_letter",
            "ready",
            artifact_path="/new/cover-letter.pdf",
            artifact_directory="/new",
            commit=False,
        )
        pending = get_autoprep_job(connection, job["id"])
        assert pending["cover_letter_artifact_path"] == "/new/cover-letter.pdf"
        assert pending["artifact_directory"] == "/new"

        connection.rollback()
        restored = get_autoprep_job(connection, job["id"])
        assert restored["resume_artifact_path"] == "/old/resume.pdf"
        assert restored["cover_letter_artifact_path"] is None
        assert restored["artifact_directory"] == "/old"


def test_partial_failure_preserves_resume_and_retries_only_cover_letter(tmp_path: Path) -> None:
    database = tmp_path / "autoprep-partial.sqlite3"
    resume_pdf = tmp_path / "resume.pdf"
    resume_pdf.write_bytes(b"%PDF-resume")
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [queued] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="attempt")
        claimed = claim_next_autoprep_job(connection)
        assert claimed is not None and claimed["id"] == queued["id"]

        mark_autoprep_document(
            connection,
            queued["id"],
            "resume",
            "ready",
            artifact_path=str(resume_pdf),
        )
        partial = mark_autoprep_document(
            connection,
            queued["id"],
            "cover_letter",
            "failed",
            error="generation failed",
        )

        assert partial["overall_status"] == "partially_complete"
        assert partial["resume_status"] == "ready"
        assert partial["resume_artifact_path"] == str(resume_pdf)
        assert partial["cover_letter_status"] == "failed"

        blocked_while_role_worker_runs = retry_autoprep_document(
            connection,
            role_id,
            "cover_letter",
            idempotency_key="retry-cover-1",
        )
        assert blocked_while_role_worker_runs["cover_letter_status"] == "failed"
        assert blocked_while_role_worker_runs["worker_state"] == "running"
        finish_autoprep_worker(connection, queued["id"])

        retried = retry_autoprep_document(
            connection,
            role_id,
            "cover_letter",
            idempotency_key="retry-cover-1",
        )
        replay = retry_autoprep_document(
            connection,
            role_id,
            "cover_letter",
            idempotency_key="retry-cover-1",
        )

        assert retried["resume_status"] == "ready"
        assert retried["resume_artifact_path"] == str(resume_pdf)
        assert retried["cover_letter_status"] == "queued"
        assert replay["cover_letter_attempt"] == retried["cover_letter_attempt"] == 2


def test_resume_regeneration_uses_default_instruction_when_comments_are_empty(
    tmp_path: Path,
) -> None:
    database = tmp_path / "autoprep-empty-resume-comments.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="initial")
        assert claim_next_autoprep_job(connection) is not None
        mark_autoprep_document(connection, job["id"], "resume", "ready")
        mark_autoprep_document(connection, job["id"], "cover_letter", "ready")
        finish_autoprep_worker(connection, job["id"])

        regenerated = queue_autoprep_regeneration(
            connection,
            role_id,
            "resume",
            instruction="",
            idempotency_key="empty-resume-comments",
        )

        assert regenerated["resume_status"] == "queued"
        assert regenerated["resume_instruction"] == (
            autoprep_service.DEFAULT_RESUME_REGENERATION_INSTRUCTION
        )
        assert regenerated["cover_letter_status"] == "ready"


def test_failed_sibling_documents_can_join_one_queued_retry(tmp_path: Path) -> None:
    database = tmp_path / "autoprep-transition-retry.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="attempt")
        assert claim_next_autoprep_job(connection) is not None
        mark_autoprep_document(connection, job["id"], "resume", "failed", error="failed")
        mark_autoprep_document(
            connection, job["id"], "cover_letter", "failed", error="failed"
        )
        finish_autoprep_worker(connection, job["id"])

        retry_autoprep_document(
            connection, role_id, "resume", idempotency_key="transition-resume-1"
        )
        retried = retry_autoprep_document(
            connection, role_id, "cover_letter", idempotency_key="transition-cover-1"
        )

        assert retried["worker_state"] == "queued"
        assert retried["resume_status"] == "queued"
        assert retried["cover_letter_status"] == "queued"
        assert retried["resume_attempt"] == 2
        assert retried["cover_letter_attempt"] == 2


def test_ready_document_can_be_regenerated_with_persisted_comments(tmp_path: Path) -> None:
    database = tmp_path / "autoprep-regeneration.sqlite3"
    resume_pdf = tmp_path / "resume.pdf"
    resume_pdf.write_bytes(b"%PDF-resume")
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="attempt")
        assert claim_next_autoprep_job(connection) is not None
        mark_autoprep_document(
            connection,
            job["id"],
            "resume",
            "ready",
            artifact_path=str(resume_pdf),
            resume_latex="\\documentclass{article}",
        )
        mark_autoprep_document(
            connection,
            job["id"],
            "cover_letter",
            "ready",
            artifact_path=str(tmp_path / "cover-letter.pdf"),
        )
        finish_autoprep_worker(connection, job["id"])

        regenerated = queue_autoprep_regeneration(
            connection,
            role_id,
            "resume",
            instruction="Emphasize the Kubernetes project and shorten the summary.",
            idempotency_key="regenerate-resume-1",
        )

        assert regenerated["worker_state"] == "queued"
        assert regenerated["resume_status"] == "queued"
        assert regenerated["cover_letter_status"] == "ready"
        assert regenerated["resume_instruction"] == (
            "Emphasize the Kubernetes project and shorten the summary."
        )
        assert regenerated["resume_attempt"] == 2
        assert regenerated["resume_artifact_path"] == str(resume_pdf)
        assert "resume_session_id" not in regenerated
        stored_session_id = connection.execute(
            "SELECT resume_session_id FROM autoprep_jobs WHERE id = ?", (job["id"],)
        ).fetchone()["resume_session_id"]
        assert stored_session_id is None
        assert regenerated["role_url"].startswith("https://example.com/")
        assert regenerated["description"] == "Build reliable Python services."


def test_ready_cover_letter_can_be_regenerated_without_comments(tmp_path: Path) -> None:
    database = tmp_path / "autoprep-cover-letter-regeneration.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="attempt")
        assert claim_next_autoprep_job(connection) is not None
        mark_autoprep_document(connection, job["id"], "resume", "ready")
        mark_autoprep_document(connection, job["id"], "cover_letter", "ready")
        finish_autoprep_worker(connection, job["id"])

        regenerated = queue_autoprep_regeneration(
            connection,
            role_id,
            "cover_letter",
            instruction="   ",
            idempotency_key="regenerate-cover-letter-without-comments",
        )

        assert regenerated["worker_state"] == "queued"
        assert regenerated["resume_status"] == "ready"
        assert regenerated["cover_letter_status"] == "queued"
        assert regenerated["cover_letter_instruction"] == (
            "Refresh this cover letter using the current role description and approved "
            "application materials. Preserve source fidelity and professional one-page "
            "formatting."
        )


def test_startup_recovery_marks_unfinished_documents_interrupted(tmp_path: Path) -> None:
    database = tmp_path / "autoprep-recovery.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="attempt")
        assert recover_interrupted_autoprep_jobs(connection) == 0
        still_queued = get_autoprep_job(connection, job["id"])
        assert still_queued["worker_state"] == "queued"
        assert still_queued["resume_status"] == "queued"
        claimed = claim_next_autoprep_job(connection)
        assert claimed is not None
        release_autoprep_claim(connection, job["id"])
        released = get_autoprep_job(connection, job["id"])
        assert released["worker_state"] == "queued"
        assert recover_interrupted_autoprep_jobs(connection) == 0
        assert claim_next_autoprep_job(connection) is not None
        mark_autoprep_document(connection, job["id"], "resume", "generating_tweaks")

        changed = recover_interrupted_autoprep_jobs(connection)
        recovered = get_autoprep_job(connection, job["id"])

        assert changed == 1
        assert recovered["overall_status"] == "interrupted"
        assert recovered["resume_status"] == "interrupted"
        assert recovered["cover_letter_status"] == "interrupted"
        assert "restart" in recovered["resume_error"].lower()


def test_database_connections_wait_for_brief_concurrent_write_lock(tmp_path: Path) -> None:
    database = tmp_path / "busy.sqlite3"
    with db.connect(database) as connection:
        connection.execute("CREATE TABLE writes (value INTEGER)")
        connection.commit()
    holder = db.connect(database)
    holder.execute("BEGIN IMMEDIATE")
    result: list[str] = []

    def write_after_holder() -> None:
        with db.connect(database) as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("INSERT INTO writes VALUES (1)")
            connection.commit()
            result.append("written")

    writer = Thread(target=write_after_holder)
    writer.start()
    time.sleep(0.1)
    assert writer.is_alive()
    holder.commit()
    writer.join(timeout=3)
    holder.close()

    assert result == ["written"]


def test_coordinator_defers_new_claims_until_role_inputs_are_finalized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "coordinator-defer.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    processed = Event()
    job_id: int | None = None

    def process_claimed_job(job_id: int) -> None:
        with db.connect() as connection:
            finish_autoprep_worker(connection, job_id)
        processed.set()

    coordinator = AutoprepCoordinator(process_claimed_job, max_workers=1)
    with coordinator.defer_claiming():
        with db.connect() as connection:
            ensure_autoprep_schema(connection)
            role_id = _interested_role(connection)
            [job] = enqueue_autoprep_jobs(
                connection,
                [role_id],
                idempotency_key="deferred-claim",
            )
            job_id = int(job["id"])
        coordinator.start()
        coordinator.wake()
        claimed_while_deferred = processed.wait(timeout=0.2)

    try:
        assert claimed_while_deferred is False
        assert processed.wait(timeout=3)
    finally:
        coordinator.stop()
    assert job_id is not None
    with db.connect() as connection:
        assert get_autoprep_job(connection, job_id)["worker_state"] == "idle"


def test_coordinator_survives_a_transient_claim_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "coordinator-retry.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="claim-retry")
    original_claim = autoprep_service.claim_next_autoprep_job
    attempts = 0
    processed = Event()

    def flaky_claim(connection):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RuntimeError("database is locked")
        return original_claim(connection)

    def process_claimed_job(job_id: int) -> None:
        with db.connect() as connection:
            finish_autoprep_worker(connection, job_id)
        processed.set()

    monkeypatch.setattr(autoprep_service, "claim_next_autoprep_job", flaky_claim)
    coordinator = AutoprepCoordinator(process_claimed_job, max_workers=1)
    coordinator.start()
    coordinator.wake()
    try:
        assert processed.wait(timeout=3)
    finally:
        coordinator.stop()
    assert attempts >= 2
    with db.connect() as connection:
        assert get_autoprep_job(connection, job["id"])["worker_state"] == "idle"


def test_autoprep_api_lists_only_interested_and_returns_accepted_jobs_immediately(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "autoprep-api.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        interested_id = _interested_role(connection, title="Backend Engineer")
        applied_id = _interested_role(connection, company="Beta", title="Applied Engineer")
        set_role_status(connection, applied_id, RoleStatus.APPLIED, summary="Already applied")

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        with urlopen(f"{base_url}/api/autoprep/interested", timeout=5) as response:
            interested = json.loads(response.read())
        assert [role["id"] for role in interested["roles"]] == [interested_id]

        body = json.dumps(
            {"role_ids": [interested_id], "idempotency_key": "browser-click-1"}
        ).encode()
        request = Request(
            f"{base_url}/api/autoprep/jobs",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            assert response.status == 202
            accepted = json.loads(response.read())
        assert accepted["accepted"] is True
        assert accepted["jobs"][0]["overall_status"] == "queued"

        with urlopen(request, timeout=5) as response:
            replay = json.loads(response.read())
        assert replay["jobs"][0]["id"] == accepted["jobs"][0]["id"]

        with urlopen(f"{base_url}/api/autoprep/jobs", timeout=5) as response:
            jobs = json.loads(response.read())["jobs"]
        assert len(jobs) == 1
        assert jobs[0]["role_id"] == interested_id
        assert jobs[0]["role_url"].endswith("/backend-engineer")
        assert jobs[0]["description"] == "Build reliable Python services."

        documents = tmp_path / "prepared-documents"
        documents.mkdir()
        resume_pdf = documents / "cohere-backend-engineer-resume.pdf"
        cover_pdf = documents / "cohere-backend-engineer-cover-letter.pdf"
        resume_pdf.write_bytes(b"resume")
        cover_pdf.write_bytes(b"cover")
        with db.connect() as connection:
            mark_autoprep_document(
                connection,
                accepted["jobs"][0]["id"],
                "resume",
                status="ready",
                artifact_path=str(resume_pdf),
                artifact_directory=str(documents),
            )
            mark_autoprep_document(
                connection,
                accepted["jobs"][0]["id"],
                "cover_letter",
                status="ready",
                artifact_path=str(cover_pdf),
                artifact_directory=str(documents),
            )
            finish_autoprep_worker(connection, accepted["jobs"][0]["id"])

        for document_kind, expected, expected_filename in (
            ("resume", b"resume", resume_pdf.name),
            ("cover-letter", b"cover", cover_pdf.name),
        ):
            with urlopen(
                f"{base_url}/api/autoprep/roles/{interested_id}/documents/{document_kind}.pdf",
                timeout=5,
            ) as response:
                assert response.headers["Content-Type"] == "application/pdf"
                assert expected_filename in response.headers["Content-Disposition"]
                assert response.read() == expected

        regenerate_request = Request(
            f"{base_url}/api/autoprep/roles/{interested_id}/regenerate/resume",
            data=json.dumps(
                {
                    "comments": "Put the Kubernetes project first.",
                    "idempotency_key": "regenerate-resume-api-1",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(regenerate_request, timeout=5) as response:
            assert response.status == 202
            regenerating = json.loads(response.read())["job"]
        assert regenerating["resume_status"] == "queued"
        assert regenerating["resume_instruction"] == "Put the Kubernetes project first."
        with db.connect() as connection:
            mark_autoprep_document(
                connection,
                accepted["jobs"][0]["id"],
                "resume",
                status="ready",
                artifact_path=str(resume_pdf),
            )
            finish_autoprep_worker(connection, accepted["jobs"][0]["id"])

        empty_regenerate_request = Request(
            f"{base_url}/api/autoprep/roles/{interested_id}/regenerate/resume",
            data=json.dumps(
                {
                    "comments": "",
                    "idempotency_key": "regenerate-resume-api-empty",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(empty_regenerate_request, timeout=5) as response:
            assert response.status == 202
            empty_regeneration = json.loads(response.read())["job"]
        assert empty_regeneration["resume_status"] == "queued"
        assert empty_regeneration["resume_instruction"] == (
            autoprep_service.DEFAULT_RESUME_REGENERATION_INSTRUCTION
        )
        with db.connect() as connection:
            mark_autoprep_document(
                connection,
                accepted["jobs"][0]["id"],
                "resume",
                status="ready",
                artifact_path=str(resume_pdf),
            )
            finish_autoprep_worker(connection, accepted["jobs"][0]["id"])

        opened: list[list[str]] = []
        monkeypatch.setattr(
            web_server.subprocess,
            "run",
            lambda command, **_kwargs: opened.append(command),
        )
        open_request = Request(
            f"{base_url}/api/autoprep/roles/{interested_id}/open-folder",
            data=b"",
            method="POST",
        )
        with urlopen(open_request, timeout=5) as response:
            assert response.status == 200
        assert opened == [["open", str(documents)]]

        with db.connect() as connection:
            events_before_applied = connection.execute(
                "SELECT COUNT(*) FROM events WHERE role_id = ?",
                (interested_id,),
            ).fetchone()[0]
        applied_request = Request(
            f"{base_url}/api/autoprep/roles/{interested_id}/applied",
            data=b"",
            method="POST",
        )
        with urlopen(applied_request, timeout=5) as response:
            assert json.loads(response.read())["role"]["role_status"] == "applied"
        with urlopen(applied_request, timeout=5) as response:
            assert json.loads(response.read())["role"]["role_status"] == "applied"
        with db.connect() as connection:
            events_after_applied = connection.execute(
                "SELECT COUNT(*) FROM events WHERE role_id = ?",
                (interested_id,),
            ).fetchone()[0]
        assert events_after_applied == events_before_applied + 1
        with urlopen(f"{base_url}/api/autoprep/jobs", timeout=5) as response:
            assert json.loads(response.read())["jobs"] == []
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_prepped_jobs_stop_listing_a_role_after_it_moves_to_disinterested(
    tmp_path: Path,
) -> None:
    database = tmp_path / "autoprep-disinterested.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection, title="Security Engineer")
        enqueue_autoprep_jobs(connection, [role_id], idempotency_key="disinterested-role")

        set_role_status(
            connection,
            role_id,
            RoleStatus.DISINTERESTED,
            summary="Moved to Disinterested from Prepped Roles.",
        )

        assert list_autoprep_jobs(connection) == []
        assert [job["role_id"] for job in list_autoprep_jobs(connection, include_applied=True)] == [
            role_id
        ]


def test_bulk_cover_letter_regeneration_queues_ready_roles_and_reports_skips(
    tmp_path: Path,
) -> None:
    database = tmp_path / "autoprep-bulk-cover-letters.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        ready_role_id = _interested_role(connection, title="Ready Engineer")
        busy_role_id = _interested_role(
            connection,
            company="Beta",
            title="Busy Engineer",
        )
        partial_role_id = _interested_role(
            connection,
            company="Gamma",
            title="Partial Engineer",
        )
        interrupted_role_id = _interested_role(
            connection,
            company="Delta",
            title="Interrupted Engineer",
        )
        ready_job, busy_job, partial_job, interrupted_job = enqueue_autoprep_jobs(
            connection,
            [ready_role_id, busy_role_id, partial_role_id, interrupted_role_id],
            idempotency_key="bulk-cover-setup",
        )
        claimed = claim_next_autoprep_job(connection)
        assert claimed is not None
        assert claimed["id"] == ready_job["id"]
        mark_autoprep_document(
            connection,
            ready_job["id"],
            "resume",
            "ready",
            artifact_path=str(tmp_path / "resume.pdf"),
        )
        mark_autoprep_document(
            connection,
            ready_job["id"],
            "cover_letter",
            "ready",
            artifact_path=str(tmp_path / "cover-letter.pdf"),
        )
        finish_autoprep_worker(connection, ready_job["id"])
        claimed_busy = claim_next_autoprep_job(connection)
        assert claimed_busy is not None
        assert claimed_busy["id"] == busy_job["id"]
        claimed_partial = claim_next_autoprep_job(connection)
        assert claimed_partial is not None
        assert claimed_partial["id"] == partial_job["id"]
        mark_autoprep_document(
            connection,
            partial_job["id"],
            "resume",
            "ready",
            artifact_path=str(tmp_path / "partial-resume.pdf"),
        )
        mark_autoprep_document(
            connection,
            partial_job["id"],
            "cover_letter",
            "failed",
            error="Provider generation failed.",
        )
        partial_job = finish_autoprep_worker(connection, partial_job["id"])
        assert partial_job["overall_status"] == "partially_complete"
        claimed_interrupted = claim_next_autoprep_job(connection)
        assert claimed_interrupted is not None
        assert claimed_interrupted["id"] == interrupted_job["id"]
        mark_autoprep_document(
            connection,
            interrupted_job["id"],
            "resume",
            "ready",
            artifact_path=str(tmp_path / "interrupted-resume.pdf"),
        )
        mark_autoprep_document(
            connection,
            interrupted_job["id"],
            "cover_letter",
            "interrupted",
            error="Worker stopped before generation completed.",
        )
        interrupted_job = finish_autoprep_worker(connection, interrupted_job["id"])
        assert interrupted_job["overall_status"] == "partially_complete"

        result = autoprep_service.queue_all_prepped_cover_letter_regenerations(
            connection,
            idempotency_key="bulk-cover-click",
        )

        assert result["requested_count"] == 4
        assert result["queued_count"] == 3
        assert [job["role_id"] for job in result["jobs"]] == [
            ready_role_id,
            partial_role_id,
            interrupted_role_id,
        ]
        assert all(job["resume_status"] == "ready" for job in result["jobs"])
        assert all(job["cover_letter_status"] == "queued" for job in result["jobs"])
        assert all(
            job["cover_letter_instruction"]
            == autoprep_service.BULK_COVER_LETTER_REGENERATION_INSTRUCTION
            for job in result["jobs"]
        )
        assert result["skipped"] == [
            {
                "role_id": int(busy_job["role_id"]),
                "company_name": "Beta",
                "title": "Busy Engineer",
                "reason": "This role is already being prepared.",
            }
        ]

        connection.execute(
            """
            UPDATE autoprep_jobs
            SET worker_state = 'idle', overall_status = 'ready',
                resume_status = 'ready', cover_letter_status = 'ready'
            WHERE id = ?
            """,
            (busy_job["id"],),
        )
        connection.commit()
        replay = autoprep_service.queue_all_prepped_cover_letter_regenerations(
            connection,
            idempotency_key="bulk-cover-click",
        )
        assert [job["role_id"] for job in replay["jobs"]] == [
            ready_role_id,
            partial_role_id,
            interrupted_role_id,
        ]
        assert replay["skipped"] == result["skipped"]
        unchanged_busy = get_autoprep_job(connection, busy_job["id"])
        assert unchanged_busy["cover_letter_status"] == "ready"


def test_bulk_resume_regeneration_queues_resumes_without_touching_cover_letters(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "autoprep-bulk-resume.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        ensure_autoprep_schema(connection)
        ready_role_id = _interested_role(connection, company="Alpha", title="Ready Engineer")
        failed_role_id = _interested_role(connection, company="Beta", title="Failed Engineer")
        ready_job, failed_job = enqueue_autoprep_jobs(
            connection,
            [ready_role_id, failed_role_id],
            idempotency_key="bulk-resume-setup",
        )
        for job, resume_status in ((ready_job, "ready"), (failed_job, "failed")):
            claimed = claim_next_autoprep_job(connection)
            assert claimed is not None
            assert claimed["id"] == job["id"]
            mark_autoprep_document(
                connection,
                job["id"],
                "resume",
                resume_status,
                artifact_path=(
                    str(tmp_path / f"resume-{job['id']}.pdf")
                    if resume_status == "ready"
                    else None
                ),
                error="Resume generation failed." if resume_status == "failed" else None,
            )
            mark_autoprep_document(
                connection,
                job["id"],
                "cover_letter",
                "ready",
                artifact_path=str(tmp_path / f"cover-letter-{job['id']}.pdf"),
            )
            finish_autoprep_worker(connection, job["id"])

        result = autoprep_service.queue_all_prepped_resume_regenerations(
            connection,
            idempotency_key="bulk-resume-click",
        )

        assert result["requested_count"] == 2
        assert result["queued_count"] == 2
        assert [job["role_id"] for job in result["jobs"]] == [
            ready_role_id,
            failed_role_id,
        ]
        assert all(job["resume_status"] == "queued" for job in result["jobs"])
        assert all(job["cover_letter_status"] == "ready" for job in result["jobs"])
        assert all(
            job["resume_instruction"] == autoprep_service.BULK_RESUME_REGENERATION_INSTRUCTION
            for job in result["jobs"]
        )

        replay = autoprep_service.queue_all_prepped_resume_regenerations(
            connection,
            idempotency_key="bulk-resume-click",
        )
        assert replay["queued_count"] == 2
        assert [job["role_id"] for job in replay["jobs"]] == [
            ready_role_id,
            failed_role_id,
        ]


def test_bulk_resume_regeneration_rolls_back_jobs_and_request_ledger(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "autoprep-bulk-resume-rollback.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_ids = [
            _interested_role(connection, company="Acme", title="First Engineer"),
            _interested_role(connection, company="Beta", title="Second Engineer"),
        ]
        jobs = enqueue_autoprep_jobs(connection, role_ids, idempotency_key="initial")
        for _job in jobs:
            claimed = claim_next_autoprep_job(connection)
            assert claimed is not None
            mark_autoprep_document(connection, claimed["id"], "resume", "ready")
            mark_autoprep_document(connection, claimed["id"], "cover_letter", "ready")
            finish_autoprep_worker(connection, claimed["id"])

        original_queue = autoprep_service._queue_autoprep_regeneration_in_transaction
        retry_count = 0

        def fail_second_retry(*args, **kwargs):
            nonlocal retry_count
            retry_count += 1
            if retry_count == 2:
                raise RuntimeError("forced second retry failure")
            return original_queue(*args, **kwargs)

        monkeypatch.setattr(
            autoprep_service,
            "_queue_autoprep_regeneration_in_transaction",
            fail_second_retry,
        )
        with pytest.raises(RuntimeError, match="forced second retry failure"):
            autoprep_service.queue_all_prepped_resume_regenerations(
                connection,
                idempotency_key="bulk-resume-rollback",
            )

        restored = [get_autoprep_job(connection, job["id"]) for job in jobs]
        assert [job["resume_status"] for job in restored] == ["ready", "ready"]
        ledger_count = connection.execute(
            "SELECT COUNT(*) FROM autoprep_bulk_resume_requests"
        ).fetchone()[0]
        assert ledger_count == 0


def test_bulk_document_regeneration_namespaces_per_role_idempotency_keys(
    tmp_path: Path,
) -> None:
    database = tmp_path / "autoprep-bulk-document-key-namespace.sqlite3"
    with db.connect(database) as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection)
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="initial")
        assert claim_next_autoprep_job(connection) is not None
        mark_autoprep_document(connection, job["id"], "resume", "ready")
        mark_autoprep_document(connection, job["id"], "cover_letter", "ready")
        finish_autoprep_worker(connection, job["id"])

        cover_result = autoprep_service.queue_all_prepped_cover_letter_regenerations(
            connection,
            idempotency_key="shared-client-key",
        )
        assert cover_result["queued_count"] == 1
        mark_autoprep_document(connection, job["id"], "cover_letter", "ready")
        finish_autoprep_worker(connection, job["id"])

        resume_result = autoprep_service.queue_all_prepped_resume_regenerations(
            connection,
            idempotency_key="shared-client-key",
        )

        assert resume_result["queued_count"] == 1
        assert resume_result["skipped"] == []
        assert resume_result["jobs"][0]["resume_status"] == "queued"
        assert resume_result["jobs"][0]["cover_letter_status"] == "ready"


def test_bulk_cover_letter_regeneration_api_queues_prepped_cover_letters(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "autoprep-bulk-cover-api.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    role_id = -1
    job_id = -1
    with db.connect() as connection:
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection, title="Platform Engineer")
        [job] = enqueue_autoprep_jobs(
            connection,
            [role_id],
            idempotency_key="bulk-api-setup",
        )
        job_id = int(job["id"])
        claimed = claim_next_autoprep_job(connection)
        assert claimed is not None
        mark_autoprep_document(
            connection,
            job["id"],
            "resume",
            "ready",
            artifact_path=str(tmp_path / "resume.pdf"),
        )
        mark_autoprep_document(
            connection,
            job["id"],
            "cover_letter",
            "ready",
            artifact_path=str(tmp_path / "cover-letter.pdf"),
        )
        finish_autoprep_worker(connection, job["id"])

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        request = Request(
            f"{base_url}/api/autoprep/cover-letters/regenerate",
            data=json.dumps({"idempotency_key": "bulk-cover-api-click"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            assert response.status == 202
            payload = json.loads(response.read())

        assert payload["accepted"] is True
        assert payload["requested_count"] == 1
        assert payload["queued_count"] == 1
        assert payload["skipped_count"] == 0
        assert payload["jobs"][0]["role_id"] == role_id
        assert payload["jobs"][0]["resume_status"] == "ready"
        assert payload["jobs"][0]["cover_letter_status"] == "queued"
        with urlopen(f"{base_url}/api/autoprep/jobs", timeout=5) as response:
            refreshed = json.loads(response.read())
        latest_bulk = refreshed["bulk_cover_letter_regeneration"]
        assert latest_bulk["idempotency_key"] == "bulk-cover-api-click"
        assert latest_bulk["requested_count"] == 1
        assert latest_bulk["jobs"][0]["role_id"] == role_id
        assert latest_bulk["jobs"][0]["cover_letter_status"] == "queued"

        disinterested_request = Request(
            f"{base_url}/api/roles/{role_id}/status",
            data=json.dumps({"status": "disinterested"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(HTTPError) as caught:
            urlopen(disinterested_request, timeout=5)
        assert caught.value.code == 409
        with db.connect() as connection:
            assert get_autoprep_job(connection, job_id)["role_status"] == "interested"

        with urlopen(request, timeout=5) as response:
            replay = json.loads(response.read())
        assert replay["jobs"][0]["id"] == payload["jobs"][0]["id"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_bulk_resume_regeneration_api_queues_only_resumes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "autoprep-bulk-resume-api.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection, title="Platform Engineer")
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="resume-api-setup")
        assert claim_next_autoprep_job(connection) is not None
        mark_autoprep_document(
            connection,
            job["id"],
            "resume",
            "ready",
            artifact_path=str(tmp_path / "resume.pdf"),
        )
        mark_autoprep_document(
            connection,
            job["id"],
            "cover_letter",
            "ready",
            artifact_path=str(tmp_path / "cover-letter.pdf"),
        )
        finish_autoprep_worker(connection, job["id"])

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        request = Request(
            f"http://127.0.0.1:{server.server_address[1]}/api/autoprep/resumes/regenerate",
            data=json.dumps({"idempotency_key": "bulk-resume-api-click"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            assert response.status == 202
            payload = json.loads(response.read())

        assert payload["accepted"] is True
        assert payload["queued_count"] == 1
        assert payload["jobs"][0]["role_id"] == role_id
        assert payload["jobs"][0]["resume_status"] == "queued"
        assert payload["jobs"][0]["cover_letter_status"] == "ready"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_autoprep_worker_uses_direct_generation_and_preserves_document_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "autoprep-worker.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection, title="Platform Engineer")
        upsert_master_resume(
            connection,
            filename="resume.tex",
            content="\\documentclass{article}\\begin{document}Python\\end{document}",
        )
        web_server.set_config_value(
            connection,
            web_server.AUTOPREP_RESUME_PROMPT_CONFIG_KEY,
            "Use the saved resume prompt.",
        )
        web_server.set_config_value(
            connection,
            web_server.AUTOPREP_COVER_LETTER_PROMPT_CONFIG_KEY,
            "Review indexed evidence before drafting.",
        )
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="worker")
        assert claim_next_autoprep_job(connection) is not None

    generated_resume = tmp_path / "generated-resume.pdf"
    generated_cover = tmp_path / "generated-cover.pdf"
    for path in (generated_resume, generated_cover):
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.write(path)
    resume_calls: list[dict[str, object]] = []
    cover_calls: list[dict[str, object]] = []
    monkeypatch.setattr(web_server, "user_data_path", lambda *_args, **_kwargs: tmp_path / "data")
    monkeypatch.setattr(
        web_server,
        "build_role_resume",
        lambda role, resume, **kwargs: resume_calls.append(kwargs) or {
            "pdf_path": str(generated_resume),
            "latex": "\\documentclass{article}\\begin{document}Tailored\\end{document}",
        },
    )
    monkeypatch.setattr(
        web_server,
        "build_role_cover_letter",
        lambda role, resume, **kwargs: cover_calls.append(kwargs) or {
            "pdf_path": str(generated_cover),
        },
    )

    web_server._process_autoprep_job(job["id"])

    with db.connect() as connection:
        completed = get_autoprep_job(connection, job["id"])
        stored_resume_latex = connection.execute(
            "SELECT resume_latex, resume_session_id, cover_letter_session_id "
            "FROM autoprep_jobs WHERE id = ?",
            (job["id"],),
        ).fetchone()
    assert completed["overall_status"] == "ready"
    assert "resume_session_id" not in completed
    assert "cover_letter_session_id" not in completed
    assert stored_resume_latex[0] == (
        "\\documentclass{article}\\begin{document}Tailored\\end{document}"
    )
    assert stored_resume_latex[1] is None and stored_resume_latex[2] is None
    assert resume_calls and cover_calls
    assert resume_calls[0]["tweaks"] == "Use the saved resume prompt."
    assert cover_calls[0]["tweaks"] == "Review indexed evidence before drafting."
    assert resume_calls[0]["required_page_count"] == 1
    assert cover_calls[0]["allow_local_fallback"] is True
    assert cover_calls[0]["required_page_count"] == 1
    assert Path(completed["resume_artifact_path"]).is_file()
    assert Path(completed["cover_letter_artifact_path"]).is_file()

    with db.connect() as connection:
        queue_autoprep_regeneration(
            connection, role_id, "cover_letter", instruction="Make the opening direct.",
            idempotency_key="regenerate-worker-cover",
        )
        assert claim_next_autoprep_job(connection) is not None
    web_server._process_autoprep_job(job["id"])
    assert len(cover_calls) == 2
    assert cover_calls[-1]["tweaks"] == (
        "Review indexed evidence before drafting.\n\n"
        "User feedback for this specific document version:\n"
        "Make the opening direct."
    )


def test_autoprep_cover_letter_only_mode_copies_master_resume_with_public_filename(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "autoprep-cover-letter-only.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    master_latex = "\\documentclass{article}\\begin{document}Master resume\\end{document}"
    with db.connect() as connection:
        ensure_autoprep_schema(connection)
        role_id = _interested_role(connection, title="Data Science Intern")
        upsert_master_resume(connection, filename="resume.tex", content=master_latex)
        web_server.set_config_value(connection, "autoprep_tailor_resume", "false")
        [job] = enqueue_autoprep_jobs(connection, [role_id], idempotency_key="cover-only")
        assert claim_next_autoprep_job(connection) is not None

    resume_pdf = tmp_path / "master-resume.pdf"
    cover_pdf = tmp_path / "generated-cover.pdf"
    for path in (resume_pdf, cover_pdf):
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.write(path)
    copied_latex: list[str] = []
    cover_resume_content: list[str] = []
    monkeypatch.setattr(web_server, "user_data_path", lambda *_args, **_kwargs: tmp_path / "data")
    monkeypatch.setattr(
        web_server,
        "build_role_resume",
        lambda *_args, **_kwargs: pytest.fail("cover-letter-only mode called the AI resume path"),
    )
    monkeypatch.setattr(
        web_server,
        "save_role_resume",
        lambda _role, _resume, latex, **_kwargs: copied_latex.append(latex)
        or {"pdf_path": str(resume_pdf), "latex": latex},
    )
    monkeypatch.setattr(
        web_server,
        "build_role_cover_letter",
        lambda _role, resume, **_kwargs: cover_resume_content.append(resume.content)
        or {"pdf_path": str(cover_pdf)},
    )

    web_server._process_autoprep_job(job["id"])

    with db.connect() as connection:
        completed = get_autoprep_job(connection, job["id"])
    assert completed["overall_status"] == "ready"
    assert copied_latex == [master_latex]
    assert cover_resume_content == [master_latex]
    assert Path(completed["resume_artifact_path"]).name == (
        "acme-data-science-intern-resume.pdf"
    )
    assert Path(completed["resume_artifact_path"]).is_file()
    assert Path(completed["cover_letter_artifact_path"]).is_file()


def test_due_applicant_profile_refresh_is_durable_and_debounced(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "profile-due.sqlite3"))
    db.ensure_initialized()
    queued_keys: list[str] = []

    def fake_queue(_connection: object, *, idempotency_key: str) -> dict[str, object]:
        queued_keys.append(idempotency_key)
        return {"requested_count": 0, "queued_role_ids": [], "skipped": []}

    monkeypatch.setattr(
        autoprep_service,
        "queue_all_prepped_cover_letter_regenerations",
        fake_queue,
    )
    with db.connect() as connection:
        set_config_value(connection, APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY, "130.0")
        monkeypatch.setattr(autoprep_service.time, "time", lambda: 129.0)
        assert autoprep_service._queue_due_applicant_profile_reprep(connection) is False
        assert queued_keys == []

        monkeypatch.setattr(autoprep_service.time, "time", lambda: 130.0)
        assert autoprep_service._queue_due_applicant_profile_reprep(connection) is True
        assert queued_keys == ["profile-settings-130.0"]
        assert get_config_value(connection, APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY) == ""
