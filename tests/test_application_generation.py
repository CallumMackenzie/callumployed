from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from callumployed.data import db
from callumployed.data.models import Company, Role, RoleStatus
from callumployed.data.repositories import add_company, add_role
from callumployed.services import application_generation as generation
from callumployed.services import autoprep as autoprep_service
from callumployed.services.autoprep import (
    complete_application_answer,
    create_application_answer,
    enqueue_autoprep_jobs,
    ensure_autoprep_schema,
    get_autoprep_document_session_id,
    get_role_autoprep_job,
    list_application_answers,
    recover_interrupted_application_answers,
)
from callumployed.services.hermes_generation import (
    HermesGenerationError,
    HermesSessionRunner,
    OpenClawSessionRunner,
    require_openclaw_agent_policy,
    runtime_availability,
)
from callumployed.web import server as web_server


def test_application_backend_validation_and_default() -> None:
    assert generation.clean_application_generation_backend(None) == "openai"
    assert generation.clean_application_generation_backend("hermes") == "hermes"
    assert generation.clean_application_generation_backend("openclaw") == "openclaw"
    with pytest.raises(ValueError, match="application_generation_backend"):
        generation.clean_application_generation_backend("codex")


def test_openclaw_uses_argv_and_stable_safe_session_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[list[str], dict[str, object]]] = []

    class Process:
        returncode = 0

        def communicate(self, *, timeout: float) -> tuple[str, str]:
            return (json.dumps({"content": '{"answer":"ok"}'}), "")

    def popen(argv: list[str], **kwargs: object) -> Process:
        calls.append((argv, kwargs))
        return Process()

    monkeypatch.setattr("callumployed.services.hermes_generation.subprocess.Popen", popen)
    runner = OpenClawSessionRunner(executable="/opt/open claw", cwd=tmp_path)
    result = runner.start("question; touch /tmp/nope", session_key="Role 1; rm -rf /")

    argv, kwargs = calls[0]
    assert argv[0] == "/opt/open claw"
    assert argv[1:3] == ["agent", "--message"]
    assert argv[3] == "question; touch /tmp/nope"
    assert argv[4:6] == ["--session-key", "agent:main:role-1-rm-rf"]
    assert kwargs.get("shell") is not True
    assert result.session_id == "agent:main:role-1-rm-rf"
    assert result.content == '{"answer":"ok"}'


def test_hermes_separates_web_research_from_private_generation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[list[str]] = []

    class Process:
        returncode = 0

        def communicate(self, *, timeout: float) -> tuple[str, str]:
            return ('{"answer":"ok"}', "session_id: bounded-session")

    def popen(argv: list[str], **_kwargs: object) -> Process:
        calls.append(argv)
        return Process()

    monkeypatch.setattr("callumployed.services.hermes_generation.subprocess.Popen", popen)
    runner = HermesSessionRunner(executable="hermes", cwd=tmp_path)
    runner.start("public role only", allow_web=True)
    runner.start("private applicant data", allow_web=False)

    assert "web" in calls[0]
    assert "--ignore-rules" in calls[0]
    assert "none" in calls[1]
    assert "--safe-mode" in calls[1]


def test_openclaw_research_policy_rejects_broader_allowlist(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agents = [
        {
            "id": "callumployed-research",
            "tools": {
                "profile": "minimal",
                "alsoAllow": ["web_search", "web_fetch"],
                "allow": [],
            },
        }
    ]
    monkeypatch.setattr(
        "callumployed.services.hermes_generation.resolve_openclaw_executable",
        lambda: "openclaw",
    )
    monkeypatch.setattr(
        "callumployed.services.hermes_generation.subprocess.run",
        lambda *_args, **_kwargs: SimpleNamespace(
            returncode=0, stdout=json.dumps(agents), stderr=""
        ),
    )

    with pytest.raises(HermesGenerationError, match="bounded research tool policy"):
        require_openclaw_agent_policy("research")


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
        backend="hermes",
    )
    for phrase in (
        "Saved exact role",
        "MASTER DISTINCTIVE",
        "TAILORED DISTINCTIVE",
        "CURRENT LETTER",
        "EXAMPLE DISTINCTIVE",
        "FULL NOTE DISTINCTIVE",
        "ROLE CHUNK DISTINCTIVE",
        "web search",
        "official company",
        "must not invent applicant facts",
        "must not override saved role facts",
        "normal sentence capitalization",
        "strict JSON",
    ):
        assert phrase.lower() in prompt.lower()


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
        backend="hermes",
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


def test_runtime_availability_missing_is_nonfatal(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("callumployed.services.hermes_generation.shutil.which", lambda _name: None)
    monkeypatch.delenv("CALLUMPLOYED_HERMES_EXECUTABLE", raising=False)
    monkeypatch.delenv("CALLUMPLOYED_OPENCLAW_EXECUTABLE", raising=False)
    monkeypatch.setenv("HERMES_HOME", "/definitely/missing/hermes-home")
    availability = runtime_availability()
    assert availability["openai"]["available"] is True
    assert availability["hermes"]["available"] is False
    assert availability["openclaw"]["available"] is False
    assert availability["hermes"]["reason"]


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
            backend="hermes",
        )
        completed = complete_application_answer(
            connection,
            answer_id=pending["id"],
            answer="I want to build Acme's reliable developer tools.",
            session_id="role-scoped-session",
            sources=[{"title": "Acme Products", "url": "https://acme.example/products"}],
        )
        create_application_answer(
            connection,
            role_id=second_role_id,
            question="Why Beta?",
            backend="openai",
        )

        first_answers = list_application_answers(connection, first_role_id)
        second_answers = list_application_answers(connection, second_role_id)

    assert first_answers == [completed]
    assert first_answers[0]["session_id"] == "role-scoped-session"
    assert first_answers[0]["sources"][0]["url"] == "https://acme.example/products"
    assert [item["question"] for item in second_answers] == ["Why Beta?"]


def test_interrupted_application_answers_are_recoverable(tmp_path: Path) -> None:
    with db.connect(tmp_path / "answers-recovery.sqlite3") as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _saved_role(connection, company_name="Acme", title="Engineer")
        create_application_answer(
            connection,
            role_id=role_id,
            question="Why us?",
            backend="openclaw",
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
            backend="hermes",
        )
        completed = complete_application_answer(
            connection,
            answer_id=pending["id"],
            answer="Acme builds reliable products.",
            session_id="existing-session",
            sources=[{"kind": "saved_material", "title": "Resume"}],
        )

        regenerating = autoprep_service.queue_application_answer_regeneration(
            connection,
            role_id,
            int(completed["id"]),
            backend="hermes",
        )

        assert regenerating["status"] == "pending"
        assert regenerating["answer"] == "Acme builds reliable products."
        assert regenerating["session_id"] == "existing-session"
        [revision] = connection.execute(
            "SELECT answer, backend, status, session_id FROM application_answer_revisions "
            "WHERE answer_id = ?",
            (completed["id"],),
        ).fetchall()
        assert dict(revision) == {
            "answer": "Acme builds reliable products.",
            "backend": "hermes",
            "status": "completed",
            "session_id": "existing-session",
        }
        with pytest.raises(ValueError, match="already being generated"):
            autoprep_service.queue_application_answer_regeneration(
                connection,
                role_id,
                int(completed["id"]),
                backend="hermes",
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


def test_external_runtime_session_namespace_is_database_scoped(tmp_path: Path) -> None:
    def namespace_for(path: Path) -> str:
        namespace: str | None = None
        with db.connect(path) as connection:
            db.run_migrations(connection)
            namespace = web_server._application_session_namespace(connection)
        assert namespace is not None
        return namespace

    first_path = tmp_path / "first.sqlite3"
    second_path = tmp_path / "second.sqlite3"
    first = namespace_for(first_path)
    first_again = namespace_for(first_path)
    second = namespace_for(second_path)

    assert first == first_again
    assert first != second
    assert len(first) == 24


def test_document_sessions_resume_internally_without_api_exposure(tmp_path: Path) -> None:
    public_job: dict[str, object] | None = None
    with db.connect(tmp_path / "sessions.sqlite3") as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_id = _saved_role(connection, company_name="Acme", title="Engineer")
        enqueue_autoprep_jobs(connection, [role_id], idempotency_key="session-test")
        connection.execute(
            "UPDATE autoprep_jobs SET resume_session_id = ?, cover_letter_session_id = ? "
            "WHERE role_id = ?",
            ("resume-session", "letter-session", role_id),
        )
        connection.commit()

        assert get_autoprep_document_session_id(connection, role_id, "resume") == "resume-session"
        assert (
            get_autoprep_document_session_id(connection, role_id, "cover_letter")
            == "letter-session"
        )
        public_job = get_role_autoprep_job(connection, role_id)

    assert public_job is not None
    assert "resume_session_id" not in public_job
    assert "cover_letter_session_id" not in public_job
