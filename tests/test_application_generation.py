from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from callumployed.data import db
from callumployed.data.models import Company, Role, RoleStatus
from callumployed.data.repositories import add_company, add_role
from callumployed.services import application_generation as generation
from callumployed.services import autoprep as autoprep_service
from callumployed.services.autoprep import (
    complete_application_answer,
    create_application_answer,
    ensure_autoprep_schema,
    list_application_answers,
    recover_interrupted_application_answers,
)


def test_prompt_contains_complete_material_and_source_policy() -> None:
    prompt = generation.build_application_prompt(
        task="answer_question",
        role={"id": 4, "title": "Engineer", "description": "Saved exact role"},
        question="Why us?",
        master_resume="MASTER DISTINCTIVE",
        tailored_resume="TAILORED DISTINCTIVE",
        cover_letter="CURRENT LETTER",
        cover_letter_examples=[{"filename": "example.tex", "content": "EXAMPLE DISTINCTIVE"}],
        experience_sections=[{"title": "Deep project", "content": "FULL NOTE DISTINCTIVE"}],
        role_context=[{"section": "description", "content": "ROLE CHUNK DISTINCTIVE"}],
    )
    for phrase in (
        "Saved exact role",
        "MASTER DISTINCTIVE",
        "TAILORED DISTINCTIVE",
        "CURRENT LETTER",
        "EXAMPLE DISTINCTIVE",
        "FULL NOTE DISTINCTIVE",
        "ROLE CHUNK DISTINCTIVE",
        "web search is unavailable",
        "must not invent applicant facts",
        "the only authorities",
        "normal sentence capitalization",
        "strict JSON",
        "first person as the applicant",
        "ready to paste unchanged",
        "answer the employer's question directly",
        "keep source authority internal",
        "do not infer that no events are planned",
    ):
        assert phrase.lower() in prompt.lower()
    for leaked_instruction in (
        "label all facts as saved-material facts",
        "state when the supplied material does not support an answer",
        '"sources"',
        '"research"',
    ):
        assert leaked_instruction.lower() not in prompt.lower()


def test_prompt_bounds_every_source_category_without_dropping_its_edges() -> None:
    def oversized(name: str) -> str:
        return f"{name}_HEAD_" + ("x" * 220_000) + f"_{name}_TAIL"

    prompt = generation.build_application_prompt(
        task="answer_question",
        role={"id": 4, "title": "Engineer", "description": oversized("ROLE")},
        question=oversized("QUESTION"),
        master_resume=oversized("MASTER"),
        tailored_resume=oversized("TAILORED"),
        cover_letter=oversized("COVER"),
        previous_output=oversized("PREVIOUS"),
        deterministic_instructions=oversized("INSTRUCTIONS"),
        cover_letter_examples=[{"content": oversized("EXAMPLE")}],
        experience_sections=[{"content": oversized("EXPERIENCE")}],
        role_context=[{"content": oversized("CONTEXT")}],
    )

    assert len(prompt) <= generation.MAX_APPLICATION_CONTEXT_CHARS
    for name in (
        "ROLE",
        "QUESTION",
        "MASTER",
        "TAILORED",
        "COVER",
        "PREVIOUS",
        "INSTRUCTIONS",
        "EXAMPLE",
        "EXPERIENCE",
        "CONTEXT",
    ):
        assert f"{name}_HEAD" in prompt
        assert f"{name}_TAIL" in prompt
    assert prompt.count("[... truncated by Callumployed ...]") == 10


def _saved_role(connection, *, company_name: str, title: str) -> int:
    company = add_company(connection, Company(name=company_name))
    assert company.id is not None
    role = add_role(
        connection,
        Role(
            company_id=company.id,
            title=title,
            role_url=f"https://example.com/{title.lower().replace(' ', '-')}",
            role_status=RoleStatus.INTERESTED,
            description="Build reliable software.",
        ),
    )
    assert role.id is not None
    return role.id


def test_saved_application_answers_are_durable_and_role_scoped(tmp_path: Path) -> None:
    with db.connect(tmp_path / "answers.sqlite3") as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        first_role_id = _saved_role(connection, company_name="Acme", title="Engineer")
        second_role_id = _saved_role(connection, company_name="Beta", title="Developer")

        pending = create_application_answer(
            connection,
            role_id=first_role_id,
            question="Why do you want to join us?",
            backend="openai",
        )
        completed = complete_application_answer(
            connection,
            answer_id=pending["id"],
            answer="I want to build Acme's reliable developer tools.",
            sources=[{"title": "Acme Products", "url": "https://acme.example/products"}],
        )
        create_application_answer(
            connection,
            role_id=second_role_id,
            question="Why Beta?",
            backend="openai",
        )
        connection.execute(
            "UPDATE application_answers SET session_id = ? WHERE id = ?",
            ("legacy-external-session", completed["id"]),
        )
        connection.commit()

        first_answers = list_application_answers(connection, first_role_id)
        second_answers = list_application_answers(connection, second_role_id)

    assert first_answers == [completed]
    assert "session_id" not in first_answers[0]
    assert first_answers[0]["sources"][0]["url"] == "https://acme.example/products"
    assert [item["question"] for item in second_answers] == ["Why Beta?"]


def test_application_answer_validation_distinguishes_provenance_from_applicant_prose(
    tmp_path: Path,
) -> None:
    with db.connect(tmp_path / "answer-validation.sqlite3") as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _saved_role(connection, company_name="Acme", title="Engineer")
        valid_pending = create_application_answer(
            connection,
            role_id,
            question="Describe a cost-saving accomplishment.",
            backend="codex",
        )
        valid = complete_application_answer(
            connection,
            int(valid_pending["id"]),
            answer="I saved material costs by 20% through supplier consolidation.",
        )
        for leaked_answer in (
            "According to the resume you provided, I attended nwHacks 2025.",
            "The resume shows that I attended nwHacks 2025.",
            "My supplied resume shows that I attended nwHacks 2025.",
            "The provided materials show that I attended nwHacks 2025.",
        ):
            leaked_pending = create_application_answer(
                connection,
                role_id,
                question="Which conferences have you attended?",
                backend="codex",
            )
            with pytest.raises(ValueError, match="paste-ready application answer"):
                complete_application_answer(
                    connection,
                    int(leaked_pending["id"]),
                    answer=leaked_answer,
                )
            leaked = autoprep_service.get_application_answer(
                connection, int(leaked_pending["id"])
            )
            assert leaked["status"] == "pending"
            assert leaked["answer"] is None

    assert valid["status"] == "completed"
    assert valid["answer"] == "I saved material costs by 20% through supplier consolidation."


def _create_intermediate_application_answers_schema(
    connection: sqlite3.Connection,
) -> None:
    connection.executescript(
        """
            CREATE TABLE application_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT,
                backend TEXT NOT NULL,
                status TEXT NOT NULL,
                error TEXT,
                session_id TEXT,
                source_metadata_json TEXT,
                research_metadata_json TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now')),
                completed_at TEXT,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
                CHECK (backend IN ('openai', 'hermes', 'openclaw')),
                CHECK (status IN ('pending', 'completed', 'failed'))
            );
        """
    )


def test_schema_migrates_intermediate_answer_backends_without_losing_rows(
    tmp_path: Path,
) -> None:
    with db.connect(tmp_path / "legacy-answers.sqlite3") as connection:
        db.run_migrations(connection)
        role_id = _saved_role(connection, company_name="Acme", title="Engineer")
        _create_intermediate_application_answers_schema(connection)
        connection.execute(
            """
            INSERT INTO application_answers (
                role_id, question, backend, status, error
            ) VALUES (?, ?, 'hermes', 'failed', ?)
            """,
            (
                role_id,
                "Why Acme?",
                "error code: 429 - insufficient_quota credit_balance_exhausted "
                "https://platform.openai.com/settings/organization/billing/",
            ),
        )
        connection.commit()

        ensure_autoprep_schema(connection)
        legacy = connection.execute(
            "SELECT backend, error FROM application_answers WHERE role_id = ?",
            (role_id,),
        ).fetchone()
        created = create_application_answer(
            connection,
            role_id,
            question="How do you use AI?",
            backend="codex",
        )
        table_sql = str(
            connection.execute(
                "SELECT sql FROM sqlite_master WHERE name = 'application_answers'"
            ).fetchone()["sql"]
        )

    assert legacy is not None
    assert legacy["backend"] == "hermes"
    assert "remaining credits" in str(legacy["error"])
    assert "platform.openai.com" not in str(legacy["error"])
    assert created["backend"] == "codex"
    assert "'codex'" in table_sql


def test_backend_migration_rolls_back_on_foreign_key_violation(tmp_path: Path) -> None:
    with db.connect(tmp_path / "invalid-legacy-answers.sqlite3") as connection:
        db.run_migrations(connection)
        connection.execute("PRAGMA foreign_keys = OFF")
        _create_intermediate_application_answers_schema(connection)
        connection.execute(
            """
            INSERT INTO application_answers (role_id, question, backend, status)
            VALUES (999999, 'Orphaned question', 'openai', 'failed')
            """
        )
        connection.commit()
        connection.execute("PRAGMA foreign_keys = ON")

        with pytest.raises(
            RuntimeError,
            match="migration violated a foreign key constraint",
        ):
            ensure_autoprep_schema(connection)

        table_sql = str(
            connection.execute(
                "SELECT sql FROM sqlite_master WHERE name = 'application_answers'"
            ).fetchone()["sql"]
        )
        legacy_row = connection.execute(
            "SELECT role_id, question FROM application_answers"
        ).fetchone()
        migrated_table = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE name = 'application_answers_migrated'"
        ).fetchone()
        foreign_keys_enabled = connection.execute("PRAGMA foreign_keys").fetchone()[0]

    assert "'codex'" not in table_sql
    assert tuple(legacy_row) == (999999, "Orphaned question")
    assert migrated_table is None
    assert foreign_keys_enabled == 1


def test_interrupted_application_answers_are_recoverable(tmp_path: Path) -> None:
    with db.connect(tmp_path / "answers-recovery.sqlite3") as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _saved_role(connection, company_name="Acme", title="Engineer")
        create_application_answer(
            connection,
            role_id=role_id,
            question="Why us?",
            backend="openai",
        )

        assert recover_interrupted_application_answers(connection) == 1
        recovered = list_application_answers(connection, role_id)

    assert recovered[0]["status"] == "failed"
    assert "interrupted" in recovered[0]["error"].lower()


def test_application_answer_regeneration_preserves_last_good_answer_until_replaced(
    tmp_path: Path,
) -> None:
    with db.connect(tmp_path / "answer-regeneration.sqlite3") as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _saved_role(connection, company_name="Acme", title="Engineer")
        pending = create_application_answer(
            connection,
            role_id=role_id,
            question="Why Acme?",
            backend="openai",
        )
        completed = complete_application_answer(
            connection,
            answer_id=pending["id"],
            answer="Acme builds reliable products.",
            sources=[{"kind": "saved_material", "title": "Resume"}],
        )

        regenerating = autoprep_service.queue_application_answer_regeneration(
            connection,
            role_id,
            int(completed["id"]),
            backend="openai",
        )

        assert regenerating["status"] == "pending"
        assert regenerating["answer"] == "Acme builds reliable products."
        assert "session_id" not in regenerating
        [revision] = connection.execute(
            "SELECT answer, backend, status, session_id FROM application_answer_revisions "
            "WHERE answer_id = ?",
            (completed["id"],),
        ).fetchall()
        assert dict(revision) == {
            "answer": "Acme builds reliable products.",
            "backend": "openai",
            "status": "completed",
            "session_id": None,
        }
        with pytest.raises(ValueError, match="already being generated"):
            autoprep_service.queue_application_answer_regeneration(
                connection,
                role_id,
                int(completed["id"]),
                backend="openai",
            )

        failed = autoprep_service.fail_application_answer(
            connection,
            int(completed["id"]),
            error="Provider unavailable",
        )

    assert failed["status"] == "failed"
    assert failed["answer"] == "Acme builds reliable products."


def test_application_answer_delete_is_role_scoped_and_rejects_pending_work(tmp_path: Path) -> None:
    with db.connect(tmp_path / "answer-delete.sqlite3") as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        first_role_id = _saved_role(connection, company_name="Acme", title="Engineer")
        second_role_id = _saved_role(connection, company_name="Beta", title="Developer")
        pending = create_application_answer(
            connection,
            role_id=first_role_id,
            question="Why Acme?",
            backend="openai",
        )

        with pytest.raises(ValueError, match="being generated"):
            autoprep_service.delete_application_answer(
                connection,
                first_role_id,
                int(pending["id"]),
            )

        completed = complete_application_answer(
            connection,
            answer_id=int(pending["id"]),
            answer="Because Acme is compelling.",
        )
        with pytest.raises(ValueError, match="was not found"):
            autoprep_service.delete_application_answer(
                connection,
                second_role_id,
                int(completed["id"]),
            )

        deleted = autoprep_service.delete_application_answer(
            connection,
            first_role_id,
            int(completed["id"]),
        )

        assert deleted["id"] == completed["id"]
        assert list_application_answers(connection, first_role_id) == []
