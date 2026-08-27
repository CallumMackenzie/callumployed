import asyncio
import base64
import json
import os
from io import BytesIO
from pathlib import Path
from threading import Event, Thread
from types import SimpleNamespace
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from zipfile import ZipFile

import pytest
from typer.testing import CliRunner

import callumployed.web.server as web_server
from callumployed.central.config import DEFAULT_CENTRAL_API_URL
from callumployed.cli import app
from callumployed.data import db
from callumployed.data.models import Company, Role, RoleDiscoveryAttempt, RoleStatus, ScanStatus
from callumployed.data.repositories import (
    add_company,
    add_experience_note,
    add_role,
    add_role_discovery_attempt,
    count_resume_feedback_history,
    create_scan_run,
    finish_scan_run,
    get_company,
    list_company_career_pages,
    list_cover_letter_examples,
    list_experience_notes,
    list_scan_runs,
    record_resume_feedback_history,
    set_role_status,
)
from callumployed.web.server import (
    LocalThreadingHTTPServer,
    ScanCoordinator,
    build_companies_payload,
    build_config_payload,
    build_metrics_payload,
    build_role_sankey_payload,
    build_scan_status_payload,
    build_tracker_payload,
    create_handler,
)

runner = CliRunner()


def test_companies_payload_reports_zero_discovered_roles_after_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "company-scan-counts.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        scan = create_scan_run(connection, company.id)
        assert scan.id is not None
        finish_scan_run(connection, scan.id, ScanStatus.SUCCEEDED)

    [company_payload] = build_companies_payload()["companies"]
    assert company_payload["scan_count"] == 1
    assert company_payload["discovered_role_count"] == 0


def _add_scan_candidate(connection: Any, scan_run_id: int, url: str) -> int:
    page_cursor = connection.execute(
        """
        INSERT INTO scan_pages (scan_run_id, source_url, final_url, candidates_scanned, confidence)
        VALUES (?, ?, ?, 1, 'high')
        """,
        (scan_run_id, "https://example.com/careers", "https://example.com/careers"),
    )
    scan_page_id = int(page_cursor.lastrowid)
    candidate_cursor = connection.execute(
        """
        INSERT INTO scan_candidates (
            scan_page_id,
            url,
            source_url,
            text,
            tag,
            confidence,
            selected
        )
        VALUES (?, ?, ?, 'Backend Engineer', 'a', 0.95, 1)
        """,
        (scan_page_id, url, "https://example.com/careers"),
    )
    return int(candidate_cursor.lastrowid)


def _minimal_docx(paragraphs: list[str]) -> bytes:
    body = "".join(
        f"<w:p><w:r><w:t>{paragraph}</w:t></w:r></w:p>"
        for paragraph in paragraphs
    )
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body>"
        "</w:document>"
    )
    archive_bytes = BytesIO()
    with ZipFile(archive_bytes, "w") as archive:
        archive.writestr("word/document.xml", document_xml)
    return archive_bytes.getvalue()


def test_static_svg_assets_are_served_with_svg_content_type() -> None:
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/assets/camackenzie-logo.svg"

        with urlopen(url, timeout=5) as response:
            assert response.status == 200
            assert response.headers["Content-Type"] == "image/svg+xml; charset=utf-8"
            assert response.read().startswith(b'<?xml version="1.0" encoding="UTF-8"?>')
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_index_serves_single_state_aware_status_toggle() -> None:
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/"

        with urlopen(url, timeout=5) as response:
            index_markup = response.read().decode()
        with urlopen(
            f"http://127.0.0.1:{port}/assets/build/app.js", timeout=5
        ) as response:
            assert response.status == 200
            assert response.headers["Content-Type"] == "text/javascript; charset=utf-8"

        static_directory = Path(web_server.__file__).with_name("static")
        markup = (static_directory / "shell.html").read_text()
        repository_root = Path(web_server.__file__).parents[3]
        app_javascript = (repository_root / "frontend" / "src" / "legacy.ts").read_text()

        assert 'id="toggle-all"' in markup
        assert (
            '<link rel="icon" href="/assets/camackenzie-logo.svg" type="image/svg+xml" />'
            in index_markup
        )
        assert (
            '<link rel="apple-touch-icon" href="/assets/camackenzie-logo.svg" />'
            in index_markup
        )
        assert '<div id="root"></div>' in index_markup
        assert "expand all" in markup
        assert 'id="expand-all"' not in markup
        assert 'id="collapse-all"' not in markup
        assert 'id="scan-all-button"' in markup
        assert 'id="manage-companies-button"' in markup
        assert 'id="companies-view"' in markup
        assert 'class="company-form-panel"' in markup
        assert 'id="company-create-form"' in markup
        assert 'id="companies-list"' in markup
        assert 'id="prep-interested"' in markup
        assert 'id="role-add-form"' in markup
        assert "Add Explicit Role" in markup
        assert 'id="role-url-input"' in markup
        assert 'id="role-company-input"' in markup
        assert 'id="role-company-options"' in markup
        assert 'id="prep-view"' in markup
        assert 'id="resume-resource-upload"' in markup
        assert 'id="resume-resource-upload-button"' in markup
        assert 'id="resume-resource-list"' in markup
        assert 'id="scan-summary"' in markup
        assert markup.index('id="review-discovered"') < markup.index('id="prep-interested"')
        assert markup.index('id="prep-interested"') < markup.index('id="scan-all-button"')
        assert markup.index('id="scan-all-button"') < markup.index('id="manage-companies-button"')
        assert markup.index('id="manage-companies-button"') < markup.index('id="scan-summary"')
        assert markup.index('id="scan-all-button"') < markup.index('class="status-toolbar"')
        assert markup.index('id="status-list"') < markup.index('id="role-add-form"')
        assert 'id="scan-status-bar"' in markup
        assert 'id="scan-status-text"' in markup
        assert markup.index('id="scan-summary"') < markup.index('id="scan-status-text"')
        assert 'id="settings-open"' in markup
        assert 'aria-label="open settings"' in markup
        assert 'id="settings-view"' in markup
        assert 'id="settings-options"' in markup
        assert 'aria-label="filters"' in markup
        assert 'aria-label="config"' in markup
        assert 'aria-label="app controls"' in markup
        assert 'id="metrics-open-button"' in markup
        assert "view metrics" in markup
        assert 'id="metrics-view"' in markup
        assert 'id="metrics-overview"' in markup
        assert 'id="metrics-sections"' in markup
        assert 'id="metrics-scan-list"' in markup
        assert 'id="sankey-open-button"' in markup
        assert "view sankey" in markup
        assert 'id="sankey-view"' in markup
        assert 'id="sankey-canvas"' in markup
        assert 'id="sankey-path-list"' in markup
        assert 'id="central-api-url-input"' in markup
        assert DEFAULT_CENTRAL_API_URL in markup
        assert 'id="central-passkey-input"' in markup
        assert 'id="central-sync-button"' in markup
        assert 'id="app-update-button"' in markup
        assert 'id="stats"' in markup
        assert 'class="stats-grid"' in markup
        assert 'id="experience-note-upload"' in markup
        assert 'id="experience-note-upload-button"' in markup
        assert "projects / employment history notes" in markup
        assert 'id="materials-required-warning"' in markup
        assert 'aria-label="missing required application materials"' in markup
        assert 'id="toolbar-summary"' in markup
        assert 'id="scan-errors"' in markup
        assert 'id="status-tabs"' not in markup
        assert 'class="status-tabs"' not in markup
        assert "/assets/app.css?v=react-ts" in index_markup
        assert "/assets/build/app.js?v=react-ts" in index_markup
        assert 'fetch("/api/central/resolve-companies", { method: "POST" })' in app_javascript
        assert "await syncCompaniesOnPageLoad().catch(() => {});" in app_javascript
        assert "loadInitialTrackerData();" in app_javascript
        assert 'aria-label="disinterested role actions"' in app_javascript
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_metrics_payload_reports_scan_candidate_and_ai_counts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-metrics.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        scan_run = create_scan_run(connection, company.id)
        assert scan_run.id is not None
        scan_page_cursor = connection.execute(
            """
            INSERT INTO scan_pages (
                scan_run_id,
                source_url,
                final_url,
                candidates_scanned,
                confidence
            )
            VALUES (?, 'https://example.com/careers', 'https://example.com/careers', 2, 'high')
            """,
            (scan_run.id,),
        )
        scan_page_id = int(scan_page_cursor.lastrowid)
        connection.execute(
            """
            INSERT INTO scan_candidates (
                scan_page_id,
                url,
                source_url,
                text,
                tag,
                confidence,
                selected,
                discovery_method
            )
            VALUES
                (?, 'https://example.com/jobs/accepted', 'https://example.com/careers',
                    'Backend Intern', 'a', 0.95, 1, 'heuristic+agent'),
                (?, 'https://example.com/about', 'https://example.com/careers',
                    'About', 'a', 0.10, 0, NULL)
            """,
            (scan_page_id, scan_page_id),
        )
        finish_scan_run(connection, scan_run.id, ScanStatus.SUCCEEDED, agent_trace="agent")
        connection.commit()

    payload = build_metrics_payload()
    overview = {metric["label"]: metric["value"] for metric in payload["overview"]}
    sections = {
        section["title"]: {metric["label"]: metric["value"] for metric in section["metrics"]}
        for section in payload["sections"]
    }

    assert overview["scan runs"] == 1
    assert overview["accepted links"] == 1
    assert overview["rejected links"] == 1
    assert overview["ai-assisted items"] == 2
    assert sections["scan runs"]["succeeded"] == 1
    assert sections["scan runs"]["candidate observations"] == 2
    assert sections["candidate links"]["stored candidates"] == 2
    assert sections["ai usage"]["agent-selected links"] == 1
    assert sections["ai usage"]["scan runs with agent trace"] == 1
    assert payload["recent_scans"][0]["company_name"] == "Acme"


def test_role_sankey_payload_collapses_state_history_loops(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-role-sankey.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Backend Engineer",
                role_url="https://example.com/jobs/backend",
            ),
        )
        assert role.id is not None
        untouched_role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Frontend Engineer",
                role_url="https://example.com/jobs/frontend",
            ),
        )
        assert untouched_role.id is not None
        archived_role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Archived Engineer",
                role_url="https://example.com/jobs/archived",
            ),
        )
        assert archived_role.id is not None
        set_role_status(connection, role.id, RoleStatus.INTERESTED, summary="Worth tracking.")
        set_role_status(connection, role.id, RoleStatus.DISCOVERED, summary="Moved back.")
        set_role_status(connection, role.id, RoleStatus.INTERESTED, summary="Worth tracking again.")
        set_role_status(connection, role.id, RoleStatus.APPLIED, summary="Applied.")
        set_role_status(connection, archived_role.id, RoleStatus.APPLIED, summary="Applied.")
        set_role_status(connection, archived_role.id, RoleStatus.ARCHIVED, summary="Archived.")

    payload = build_role_sankey_payload()
    links = {(link["source"], link["target"]): link["value"] for link in payload["links"]}
    nodes = {
        node["id"]: {
            "current_count": node["current_count"],
            "history_count": node["history_count"],
        }
        for node in payload["nodes"]
    }
    path_counts = {tuple(path["path"]): path["value"] for path in payload["path_counts"]}
    backend_path = next(path for path in payload["paths"] if path["title"] == "Backend Engineer")
    frontend_path = next(path for path in payload["paths"] if path["title"] == "Frontend Engineer")

    assert payload["role_count"] == 2
    assert "archived" not in nodes
    assert links == {
        ("discovered", "interested"): 1,
        ("interested", "applied"): 1,
    }
    assert nodes["discovered"] == {"current_count": 1, "history_count": 2}
    assert nodes["interested"] == {"current_count": 0, "history_count": 1}
    assert nodes["applied"] == {"current_count": 1, "history_count": 1}
    assert path_counts == {
        ("discovered",): 1,
        ("discovered", "interested", "applied"): 1,
    }
    assert backend_path["path"] == ["discovered", "interested", "applied"]
    assert backend_path["loops_collapsed"] == 2
    assert frontend_path["path"] == ["discovered"]


def test_prep_analysis_endpoint_reports_resume_fit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-prep-analysis.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(
        web_server,
        "_prepared_resumes_root",
        lambda: tmp_path / "prepared-resumes",
    )
    monkeypatch.setattr(
        web_server,
        "_resume_resources_root",
        lambda: tmp_path / "resume-resources",
    )
    monkeypatch.setattr(
        web_server,
        "evaluate_resume_feedback",
        lambda **_: (_ for _ in ()).throw(RuntimeError("no test LLM")),
    )
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    with db.connect() as connection:
        connection.execute(
            """
            UPDATE roles
            SET description = 'Python distributed systems data platform work'
            WHERE id = 1
            """
        )
        connection.execute(
            """
            INSERT INTO master_resumes (id, filename, content, content_sha256)
            VALUES (1, 'resume.tex', 'Python systems backend projects', 'abc')
            """
        )
        connection.commit()
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urlopen(f"http://127.0.0.1:{port}/api/roles/1/prep-analysis", timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert payload["analysis"]["role_id"] == 1
        assert payload["analysis"]["verdict"] == "tweak"
        assert "overview" in payload["analysis"]
        assert "python" in payload["analysis"]["matched_terms"]
        assert payload["analysis"]["feedback_items"]
        titles = [item["title"] for item in payload["analysis"]["feedback_items"]]
        assert any(title.startswith("change wording to align with posting") for title in titles)
        assert any(title.startswith("add skills matching the posting") for title in titles)
        assert not (tmp_path / "prepared-resumes" / "role-1" / "resume.tex").exists()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_prep_analysis_passes_recommendation_history_to_agent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-prep-analysis-history.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    captured: dict[str, object] = {}

    def fake_list_knowledge(*args: object, **kwargs: object) -> list[dict[str, object]]:
        return [
            {
                "response": "ignored",
                "comment": "too generic",
                "feedback_title": "add skills matching the posting: React",
                "feedback_detail": "add React",
                "knowledge_text": "ignored because too generic",
                "similarity": 0.9,
            }
        ]

    async def fake_evaluate_resume_feedback(**kwargs: object) -> object:
        captured["knowledge_base"] = kwargs.get("knowledge_base")
        captured["other_experience_context"] = kwargs.get("other_experience_context")

        class Response:
            def model_dump(self, **_kwargs: object) -> dict[str, object]:
                return {
                    "verdict": "ready_to_apply",
                    "overview": "ready",
                    "feedback_items": [],
                }

        return Response()

    monkeypatch.setattr(web_server, "list_resume_feedback_knowledge", fake_list_knowledge)
    monkeypatch.setattr(web_server, "evaluate_resume_feedback", fake_evaluate_resume_feedback)
    db.ensure_initialized()
    with db.connect() as connection:
        add_experience_note(
            connection,
            filename="projects.md",
            content="Built a Kubernetes scheduler that is not on the current resume.",
        )

    analysis = web_server.build_prep_analysis(
        {
            "id": 1,
            "company_id": 1,
            "title": "Backend Intern",
            "role_url": "https://example.com/jobs/backend",
            "description": "Python backend",
        },
        web_server.MasterResume(
            filename="resume.tex",
            content="Python backend",
            content_sha256="abc",
        ),
    )

    assert analysis["recommendation_history_matches"] == 1
    assert captured["knowledge_base"] == fake_list_knowledge()
    other_experience_context = captured["other_experience_context"]
    assert isinstance(other_experience_context, list)
    assert len(other_experience_context) == 1
    assert other_experience_context == [
        {
            "filename": "projects.md",
            "content": "Built a Kubernetes scheduler that is not on the current resume.",
            "updated_at": other_experience_context[0]["updated_at"],
        }
    ]


def test_prep_feedback_acceptance_returns_tweak_prompt_without_updating_resume(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-prep-feedback.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(
        web_server,
        "_resume_resources_root",
        lambda: tmp_path / "resume-resources",
    )
    monkeypatch.setattr(
        web_server,
        "evaluate_resume_feedback",
        lambda **_: (_ for _ in ()).throw(RuntimeError("no test LLM")),
    )
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    with db.connect() as connection:
        connection.execute(
            """
            UPDATE roles
            SET description = 'Python kubernetes distributed systems data platform work'
            WHERE id = 1
            """
        )
        connection.execute(
            """
            INSERT INTO master_resumes (id, filename, content, content_sha256)
            VALUES (1, 'resume.tex', ?, 'abc')
            """,
            ("\\documentclass{article}\\begin{document}Python systems\\end{document}",),
        )
        web_server.set_config_value(connection, "applicant_first_name", "Callum")
        web_server.set_config_value(connection, "applicant_last_name", "Mackenzie")
        connection.commit()
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/prep-feedback",
            data=json.dumps(
                {
                    "feedback_index": 0,
                    "feedback_item": {
                        "label": "gap",
                        "title": "add distributed systems signal",
                        "detail": "mention distributed systems experience",
                        "tweak_prompt": (
                            "Revise the resume to emphasize existing distributed systems "
                            "experience for this backend internship."
                        ),
                    },
                    "comment": "good targeted edit",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert payload["accepted"] is True
        assert payload["tweak_prompt"] == (
            "Revise the resume to emphasize existing distributed systems "
            "experience for this backend internship."
        )
        assert payload["role"]["role_status"] == "discovered"
        assert not (resume_root / "role-1" / "resume.tex").exists()
        with db.connect() as connection:
            rows = connection.execute(
                """
                SELECT response, comment, feedback_title
                FROM resume_feedback_history
                """
            ).fetchall()
        assert len(rows) == 1
        assert rows[0]["response"] == "accepted"
        assert rows[0]["comment"] == "good targeted edit"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_endpoint_generates_role_specific_latex(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-generate.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")

    def fake_run(command: object, **kwargs: object) -> object:
        cwd = Path(kwargs["cwd"])
        (cwd / "cover-letter.pdf").write_bytes(b"cover pdf")

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)

    captured: dict[str, object] = {}

    async def fake_generate_cover_letter(**kwargs: object) -> object:
        captured["tweaks"] = kwargs.get("tweaks")
        captured["previous_cover_letter_latex"] = kwargs.get("previous_cover_letter_latex")
        captured["other_experience_context"] = kwargs.get("other_experience_context")

        class Draft:
            latex = "\\documentclass{letter}\\begin{document}Dear Acme\\end{document}"
            summary = "generated from examples"
            example_ids = [1]

        search_tool = kwargs["search_tool"]
        search_tool("Python backend", limit=1)
        return Draft()

    monkeypatch.setattr(web_server, "generate_cover_letter", fake_generate_cover_letter)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    with db.connect() as connection:
        connection.execute(
            """
            UPDATE roles
            SET description = 'Python backend internship'
            WHERE id = 1
            """
        )
        connection.execute(
            """
            INSERT INTO master_resumes (id, filename, content, content_sha256)
            VALUES (1, 'resume.tex', 'Python backend resume', 'abc')
            """
        )
        connection.commit()
        add_experience_note(
            connection,
            filename="projects.md",
            content="Built a BLE sensor network for motion analysis.",
        )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/cover-letter",
            data=json.dumps(
                {
                    "tweaks": "Make it warmer and shorten the Amazon paragraph.",
                    "previous_latex": (
                        "\\documentclass{letter}\\begin{document}"
                        "Previous Acme draft"
                        "\\end{document}"
                    ),
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        cover_letter = payload["cover_letter"]
        assert response.status == 200
        assert (
            cover_letter["summary"]
            == (
                "Drafted cover letter for Backend Intern at Acme using resume, "
                "job description, and 1 stored cover letter example."
            )
        )
        assert cover_letter["path"] == str(resume_root / "role-1" / "cover-letter.tex")
        assert cover_letter["pdf_path"] == str(resume_root / "role-1" / "cover-letter.pdf")
        assert cover_letter["pdf_base64"]
        assert cover_letter["tweaks"] == "Make it warmer and shorten the Amazon paragraph."
        assert captured["tweaks"] == "Make it warmer and shorten the Amazon paragraph."
        assert captured["previous_cover_letter_latex"] == (
            "\\documentclass{letter}\\begin{document}Previous Acme draft\\end{document}"
        )
        assert captured["other_experience_context"] == [
            {
                "filename": "projects.md",
                "content": "Built a BLE sensor network for motion analysis.",
                "updated_at": captured["other_experience_context"][0]["updated_at"],
            }
        ]
        saved_latex = (resume_root / "role-1" / "cover-letter.tex").read_text()
        assert "Dear Acme" in saved_latex
        assert "\\setlength{\\parskip}{0.85em}" in saved_latex
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_save_endpoint_writes_edited_latex(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-save.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")

    def fake_run(command: object, **kwargs: object) -> object:
        cwd = Path(kwargs["cwd"])
        (cwd / "cover-letter.pdf").write_bytes(b"edited cover pdf")

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/cover-letter/save",
            data=json.dumps(
                {
                    "latex": (
                        "\\documentclass{letter}\n"
                        "\\begin{document}\n"
                        "Edited Acme letter\n"
                        "\\end{document}"
                    )
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        cover_letter = payload["cover_letter"]
        assert response.status == 200
        assert cover_letter["source"] == "edited_cover_letter"
        assert cover_letter["summary"] == "Saved edited cover letter for Backend Intern at Acme."
        assert cover_letter["pdf_base64"]
        assert "Edited Acme letter" in cover_letter["latex"]
        assert (resume_root / "role-1" / "cover-letter.tex").read_text() == cover_letter["latex"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_display_summary_does_not_use_agent_blurb() -> None:
    summary = web_server._cover_letter_display_summary(
        {
            "title": "Campus AI Research Engineer - Research Automation (Intern)",
            "company_name": "Jump Trading Group",
        },
        source="ai_cover_letter",
        example_count=2,
    )

    assert summary == (
        "Drafted cover letter for Campus AI Research Engineer - Research Automation "
        "(Intern) at Jump Trading Group using resume, job description, and 2 stored "
        "cover letter examples."
    )
    assert "concise, professional latex cover letter" not in summary


def test_cover_letter_endpoint_loads_saved_role_cover_letter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-load.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    db.ensure_initialized()
    with db.connect() as connection:
        web_server.set_config_value(connection, "applicant_first_name", "Callum")
        web_server.set_config_value(connection, "applicant_last_name", "Mackenzie")

    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True)
    (role_dir / "cover-letter.tex").write_text("\\documentclass{letter}")
    (role_dir / "cover-letter.pdf").write_bytes(b"pdf")

    def fake_generate_pdf(path: Path) -> tuple[Path, str]:
        pdf_path = path.with_suffix(".pdf")
        pdf_path.write_bytes(b"fresh pdf")
        return pdf_path, base64.b64encode(b"fresh pdf").decode()

    monkeypatch.setattr(web_server, "_generate_cover_letter_pdf_preview", fake_generate_pdf)

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urlopen(f"http://127.0.0.1:{port}/api/roles/1/cover-letter", timeout=5) as response:
            payload = json.loads(response.read().decode())

        cover_letter = payload["cover_letter"]
        assert response.status == 200
        assert cover_letter["source"] == "saved_cover_letter"
        assert "\\documentclass{letter}" in cover_letter["latex"]
        assert cover_letter["pdf_base64"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_endpoint_recompiles_stale_saved_pdf(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-stale-pdf.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    db.ensure_initialized()
    with db.connect() as connection:
        web_server.set_config_value(connection, "applicant_first_name", "Callum")
        web_server.set_config_value(connection, "applicant_last_name", "Mackenzie")

    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True)
    cover_letter_path = role_dir / "cover-letter.tex"
    pdf_path = role_dir / "cover-letter.pdf"
    cover_letter_path.write_text("\\documentclass{letter}\\begin{document}new\\end{document}")
    pdf_path.write_bytes(b"stale pdf")
    os.utime(pdf_path, (1, 1))

    def fake_generate_pdf(path: Path) -> tuple[Path, str]:
        assert path == cover_letter_path
        pdf_path.write_bytes(b"fresh pdf")
        return pdf_path, base64.b64encode(b"fresh pdf").decode()

    monkeypatch.setattr(web_server, "_generate_cover_letter_pdf_preview", fake_generate_pdf)

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urlopen(f"http://127.0.0.1:{port}/api/roles/1/cover-letter", timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert base64.b64decode(payload["cover_letter"]["pdf_base64"]) == b"fresh pdf"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_pdf_endpoint_serves_saved_role_pdf(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-pdf.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    db.ensure_initialized()
    with db.connect() as connection:
        web_server.set_config_value(connection, "applicant_first_name", "Callum")
        web_server.set_config_value(connection, "applicant_last_name", "Mackenzie")

    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True)
    (role_dir / "cover-letter.tex").write_text("\\documentclass{letter}")
    (role_dir / "cover-letter.pdf").write_bytes(b"%PDF saved cover letter")

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urlopen(
            f"http://127.0.0.1:{port}/api/roles/1/cover-letter.pdf",
            timeout=5,
        ) as response:
            body = response.read()

        assert response.status == 200
        assert response.headers["Content-Type"] == "application/pdf"
        assert response.headers["Content-Disposition"].startswith("inline;")
        assert 'filename="CallumMackenzieCL1.pdf"' in response.headers[
            "Content-Disposition"
        ]
        assert body == b"%PDF saved cover letter"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_latex_normalizer_adds_compact_one_page_layout() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass{letter}\n\\begin{document}\nHello\n\\end{document}"
    )

    assert "\\documentclass{letter}" in normalized
    assert "\\usepackage[margin=1in]{geometry}" in normalized
    assert "\\setlength{\\parskip}{0.85em}" in normalized
    assert "\\setlength{\\parindent}{0pt}" in normalized
    assert "\\linespread{0.97}" not in normalized
    assert "\\pagestyle{empty}" in normalized
    assert normalized.index("\\setlength{\\parskip}") < normalized.index("\\begin{document}")


def test_cover_letter_latex_normalizer_strips_em_dashes() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass{letter}\n"
        "\\begin{document}\n"
        "AI infrastructure \u2014 distributed systems --- backend tooling "
        "\\textemdash{} platform work -- reliability\n"
        "\\end{document}"
    )

    assert "\u2014" not in normalized
    assert "---" not in normalized
    assert "--" not in normalized
    assert "\\textemdash" not in normalized
    assert (
        "AI infrastructure, distributed systems, backend tooling, platform work, reliability"
        in normalized
    )


def test_cover_letter_latex_normalizer_left_aligns_sender_header() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{letter}\n"
        "\\address{Callum Mackenzie \\\\ callum@camackenzie.com}\n"
        "\\date{\\today}\n"
        "\\begin{document}\n"
        "\\begin{letter}{Hiring Team}\n"
        "\\opening{Dear Hiring Team,}\n"
        "Hi\n"
        "\\end{letter}\n"
        "\\end{document}"
    )

    assert "\\address{" not in normalized
    assert "\\date{" not in normalized
    assert "\\noindent\\begin{tabular}{@{}l@{}}" in normalized
    assert "Callum Mackenzie\\\\\ncallum@camackenzie.com" in normalized
    assert normalized.index("\\end{tabular}") < normalized.index("\\begin{letter}")


def test_cover_letter_latex_normalizer_escapes_header_ampersands() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass{letter}\n"
        "\\address{Callum Mackenzie \\\\ BSc Computer Science & Statistics}\n"
        "\\begin{document}\n"
        "\\begin{letter}{Hiring Team}\n"
        "Hi\n"
        "\\end{letter}\n"
        "\\end{document}"
    )

    assert "Computer Science \\& Statistics" in normalized
    assert "Computer Science & Statistics" not in normalized


def test_cover_letter_latex_normalizer_escapes_body_ampersands() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "I contributed to General Dynamics' defense R&D team and improved reliability.\n"
        "\\end{document}"
    )

    assert "R\\&D team" in normalized
    assert "R&D team" not in normalized


def test_cover_letter_latex_normalizer_strips_resume_pdf_compatibility_commands() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass{article}\n"
        "\\usepackage[margin=1in]{geometry}\n"
        "\\pdfgentounicode=1\n"
        "\\input{glyphtounicode}\n"
        "\\providecommand{\\pdfglyphtounicode}[2]{}\n"
        "\\begin{document}\n"
        "Dear Hiring Team,\n"
        "\\end{document}"
    )

    assert "\\pdfgentounicode" not in normalized
    assert "glyphtounicode" not in normalized


def test_cover_letter_latex_normalizer_repairs_invalid_text_characters() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "I am drawn to Jump\x19s research culture and the team's focus.\n"
        "\\end{document}"
    )

    assert "Jump's research culture" in normalized
    assert "\x19" not in normalized


def test_cover_letter_latex_normalizer_migrates_manual_minipage_header() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass{letter}\n"
        "\\begin{document}\n"
        "\\noindent\\begin{minipage}{\\textwidth}\n"
        "Callum Mackenzie \\\\ BSc Computer Science & Statistics\\\\\n"
        "\\today\n"
        "\\end{minipage}\n"
        "\\vspace{1em}\n"
        "\\begin{letter}{Hiring Team}\n"
        "Hi\n"
        "\\end{letter}\n"
        "\\end{document}"
    )

    assert "\\begin{minipage}" not in normalized
    assert "\\noindent\\begin{tabular}{@{}l@{}}" in normalized
    assert "Computer Science \\& Statistics" in normalized


def test_cover_letter_latex_normalizer_repairs_generated_broken_header() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{letter}\n"
        "\\usepackage[margin=1in]{geometry}\n"
        "\\usepackage{hyperref}\n"
        "\\signature{Callum Mackenzie}\n"
        "{callum@camackenzie.com} \\\\ +1 403-473-1818 \\\\ "
        "\\href{https://camackenzie.com}{camackenzie.com}}\n"
        "\\begin{document}\n"
        "\\noindent\\begin{tabular}{@{}l@{}}\n"
        "Callum Mackenzie\\\\\n"
        "\\href{mailto:callum@camackenzie.com\n"
        "\\end{tabular}\n"
        "\\vspace{1em}\n"
        "\\begin{letter}{Hiring Team}\n"
        "Hi\n"
        "\\end{letter}\n"
        "\\end{document}"
    )

    assert "{callum@camackenzie.com} \\\\ +1" not in normalized
    assert "\\signature{Callum Mackenzie}" in normalized
    assert "\\href{mailto:callum@camackenzie.com}{callum@camackenzie.com}" in normalized


def test_cover_letter_latex_normalizer_repairs_single_slash_article_header() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{article}\n"
        "\\usepackage[empty]{fullpage}\n"
        "\\usepackage{parskip}\n"
        "\\begin{document}\n"
        "% Sender Information\n"
        "Callum Mackenzie \\\n"
        "University of British Columbia \\\n"
        "BSc Computer Science \\& Statistics \\\n"
        "\\href{mailto:callum@camackenzie.com}{callum@camackenzie.com} \\\n"
        "\\href{https://camackenzie.com}{camackenzie.com} \\\\[12pt]\n"
        "\\vspace{1em}\n"
        "Dear Hiring Team,\n"
        "\n"
        "First paragraph improved reliability by 50%.\n"
        "\n"
        "Second paragraph.\n"
        "\n"
        "Sincerely, \\\n"
        "Callum Mackenzie\n"
        "\\end{document}"
    )

    assert "\\usepackage[empty]{fullpage}" not in normalized
    assert "\\usepackage{parskip}" not in normalized
    assert "% Sender Information" not in normalized
    assert "camackenzie.com}{camackenzie.com}" not in normalized
    assert "mailto:callum@camackenzie.com" in normalized
    assert "\\href{mailto:callum@camackenzie.com}{callum@camackenzie.com}\\\\[12pt]" in normalized
    assert "50\\%." in normalized
    assert "\\setlength{\\parskip}{0.85em}" in normalized
    assert "Callum Mackenzie\\\\\nUniversity of British Columbia\\\\" in normalized
    assert "Sincerely,\\\\\nCallum Mackenzie" in normalized


def test_prep_feedback_ignore_records_comment_without_updating_resume(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-prep-feedback-ignore.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/prep-feedback-ignore",
            data=json.dumps(
                {
                    "feedback_index": 1,
                    "feedback_item": {
                        "label": "add_skills",
                        "title": "add skills matching the posting: Kubernetes",
                        "detail": "mention Kubernetes if supported",
                    },
                    "comment": "not actually supported by the resume",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert payload["ignored"] is True
        assert not (resume_root / "role-1" / "resume.tex").exists()
        with db.connect() as connection:
            rows = connection.execute(
                """
                SELECT response, comment, feedback_title
                FROM resume_feedback_history
                """
            ).fetchall()
        assert len(rows) == 1
        assert rows[0]["response"] == "ignored"
        assert rows[0]["comment"] == "not actually supported by the resume"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_role_resume_endpoint_loads_and_saves_editable_latex(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-role-resume.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")

    def fake_run(command: object, **kwargs: object) -> object:
        cwd = Path(kwargs["cwd"])
        (cwd / "resume.pdf").write_bytes(b"role resume pdf")

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    with db.connect() as connection:
        connection.execute(
            """
            INSERT INTO master_resumes (id, filename, content, content_sha256)
            VALUES (1, 'resume.tex', ?, 'abc')
            """,
            ("\\documentclass{article}\\begin{document}Python systems\\end{document}",),
        )
        web_server.set_config_value(connection, "applicant_first_name", "Callum")
        web_server.set_config_value(connection, "applicant_last_name", "Mackenzie")
        connection.commit()
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urlopen(f"http://127.0.0.1:{port}/api/roles/1/resume", timeout=5) as response:
            payload = json.loads(response.read().decode())

        resume = payload["resume"]
        assert response.status == 200
        assert "Python systems" in resume["latex"]
        assert resume["pdf_base64"]
        assert base64.b64decode(resume["pdf_base64"]) == b"role resume pdf"
        assert (resume_root / "role-1" / "resume.tex").exists()

        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/resume/save",
            data=json.dumps(
                {
                    "latex": (
                        "\\documentclass{article}\\begin{document}"
                        "Edited role resume"
                        "\\end{document}"
                    )
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            save_payload = json.loads(response.read().decode())

        saved_resume = save_payload["resume"]
        assert response.status == 200
        assert "Edited role resume" in saved_resume["latex"]
        assert (resume_root / "role-1" / "resume.tex").read_text() == saved_resume["latex"]

        with urlopen(f"http://127.0.0.1:{port}/api/roles/1/resume.pdf", timeout=5) as response:
            body = response.read()

        assert response.status == 200
        assert response.headers["Content-Disposition"].startswith("inline;")
        assert 'filename="CallumMackenzieResume1.pdf"' in response.headers[
            "Content-Disposition"
        ]
        assert body == b"role resume pdf"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_role_resume_endpoint_regenerates_with_tweaks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-role-resume-regenerate.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")

    def fake_run(command: object, **kwargs: object) -> object:
        cwd = Path(kwargs["cwd"])
        (cwd / "resume.pdf").write_bytes(b"regenerated resume pdf")

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    captured: dict[str, object] = {}

    async def fake_generate_resume_tweak(**kwargs: object) -> object:
        captured["resume_content"] = kwargs.get("resume_content")
        captured["tweaks"] = kwargs.get("tweaks")
        captured["other_experience_context"] = kwargs.get("other_experience_context")

        class Draft:
            latex = (
                "\\documentclass{article}\\begin{document}"
                "Python distributed systems\\end{document}"
            )
            summary = "emphasized distributed systems"

        return Draft()

    monkeypatch.setattr(web_server, "generate_resume_tweak", fake_generate_resume_tweak)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    with db.connect() as connection:
        connection.execute(
            """
            UPDATE roles
            SET description = 'Python distributed systems internship'
            WHERE id = 1
            """
        )
        connection.execute(
            """
            INSERT INTO master_resumes (id, filename, content, content_sha256)
            VALUES (1, 'resume.tex', 'Master resume', 'abc')
            """
        )
        add_experience_note(
            connection,
            filename="projects.md",
            content="Built a Kubernetes scheduler.",
        )
        connection.commit()
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/resume",
            data=json.dumps(
                {
                    "tweaks": "Emphasize distributed systems.",
                    "previous_latex": "Current editor latex",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        resume = payload["resume"]
        assert response.status == 200
        assert resume["summary"] == "emphasized distributed systems"
        assert resume["tweaks"] == "Emphasize distributed systems."
        assert "Python distributed systems" in resume["latex"]
        assert base64.b64decode(resume["pdf_base64"]) == b"regenerated resume pdf"
        assert captured["resume_content"] == "Current editor latex"
        assert captured["tweaks"] == "Emphasize distributed systems."
        assert captured["other_experience_context"] == [
            {
                "filename": "projects.md",
                "content": "Built a Kubernetes scheduler.",
                "updated_at": captured["other_experience_context"][0]["updated_at"],
            }
        ]
        assert (resume_root / "role-1" / "resume.tex").read_text() == resume["latex"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_role_chat_endpoint_uses_role_material_contexts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-role-chat.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    captured: dict[str, object] = {}

    async def fake_generate_role_chat(**kwargs: object) -> object:
        captured.update(kwargs)
        return SimpleNamespace(answer="Emphasize Python backend systems.")

    monkeypatch.setattr(web_server, "generate_role_chat", fake_generate_role_chat)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True)
    (role_dir / "resume.tex").write_text("Role resume latex")
    (role_dir / "cover-letter.tex").write_text("Cover letter latex")
    with db.connect() as connection:
        connection.execute(
            """
            UPDATE roles
            SET description = 'Python distributed systems internship'
            WHERE id = 1
            """
        )
        connection.execute(
            """
            INSERT INTO master_resumes (id, filename, content, content_sha256)
            VALUES (1, 'resume.tex', 'Master resume latex', 'abc')
            """
        )
        add_experience_note(
            connection,
            filename="projects.md",
            content="Built a Kubernetes scheduler.",
        )
        connection.commit()
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/chat",
            data=json.dumps(
                {
                    "messages": [
                        {"role": "user", "content": "What should I emphasize?"}
                    ]
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert payload["message"] == {
            "role": "assistant",
            "content": "Emphasize Python backend systems.",
        }
        assert captured["role"]["company_name"] == "Acme"
        assert captured["role"]["title"] == "Backend Intern"
        assert captured["resume_content"] == "Role resume latex"
        assert captured["cover_letter_content"] == "Cover letter latex"
        assert captured["messages"][0].content == "What should I emphasize?"
        assert captured["employment_history_context"] == [
            {
                "filename": "projects.md",
                "content": "Built a Kubernetes scheduler.",
                "updated_at": captured["employment_history_context"][0]["updated_at"],
            }
        ]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_resume_pdf_endpoint_reports_missing_latex_compiler(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-resume-pdf.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(
        web_server,
        "_prepared_resumes_root",
        lambda: tmp_path / "prepared-resumes",
    )
    monkeypatch.setattr(
        web_server,
        "_resume_resources_root",
        lambda: tmp_path / "resume-resources",
    )
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    with db.connect() as connection:
        connection.execute(
            """
            INSERT INTO master_resumes (id, filename, content, content_sha256)
            VALUES (1, 'resume.tex', ?, 'abc')
            """,
            ("\\documentclass{article}\\begin{document}Python systems\\end{document}",),
        )
        connection.commit()
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/resume-pdf",
            data=b"",
            method="POST",
        )

        with pytest.raises(HTTPError) as error_info:
            urlopen(request, timeout=5)

        assert error_info.value.code == 503
        payload = json.loads(error_info.value.read().decode())
        assert "Install tectonic, latexmk, or pdflatex" in payload["error"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_resume_resource_endpoint_uploads_shared_compile_dependency(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-resume-resource.sqlite3"
    resource_root = tmp_path / "resume-resources"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: resource_root)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        content = b"\x89PNG\r\n"
        request = Request(
            f"http://127.0.0.1:{port}/api/resume-resources",
            data=json.dumps(
                {
                    "filename": "../logo.png",
                    "content_base64": base64.b64encode(content).decode(),
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        resource_path = resource_root / "logo.png"
        assert response.status == 200
        assert resource_path.read_bytes() == content
        assert payload["resource"]["filename"] == "logo.png"
        assert payload["resources"] == [{"filename": "logo.png", "bytes": len(content)}]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_shared_resume_resources_sync_into_role_resume_copy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    resource_root = tmp_path / "resume-resources"
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: resource_root)
    resource_root.mkdir(parents=True)
    (resource_root / "logo.png").write_bytes(b"png")

    web_server._ensure_role_resume_copy(
        1,
        web_server.MasterResume(
            filename="resume.tex",
            content="\\documentclass{article}\\begin{document}hi\\end{document}",
            content_sha256="abc",
        ),
    )

    assert (resume_root / "role-1" / "resume.tex").exists()
    assert (resume_root / "role-1" / "logo.png").read_bytes() == b"png"


def test_tectonic_resume_input_adds_pdftex_compatibility(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.tex"
    resume_path.write_text(
        "\\documentclass{article}\n"
        "\\input{glyphtounicode}\n"
        "\\pdfgentounicode=1\n"
        "\\begin{document}hello\\end{document}\n"
    )

    compile_path = web_server._write_tectonic_resume_input(resume_path)
    compile_content = compile_path.read_text()

    assert compile_path == tmp_path / "resume-tectonic.tex"
    assert "\\providecommand{\\pdfglyphtounicode}[2]{}" in compile_content
    assert "\\newcount\\pdfgentounicode" in compile_content


def test_resume_pdf_uses_temporary_resume_when_role_has_no_custom_copy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "resume-pdf.sqlite3"))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")
    monkeypatch.setattr(web_server.Path, "home", lambda: tmp_path)

    def fake_run(command: object, **kwargs: object) -> object:
        cwd = Path(kwargs["cwd"])
        (cwd / "resume.pdf").write_bytes(b"pdf")

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    db.ensure_initialized()
    with db.connect() as connection:
        web_server.set_config_value(connection, "applicant_first_name", "Callum")
        web_server.set_config_value(connection, "applicant_last_name", "Mackenzie")

    pdf_path = web_server._generate_role_resume_pdf(
        {"id": 1, "title": "Backend Intern"},
        web_server.MasterResume(
            filename="resume.tex",
            content="\\documentclass{article}\\begin{document}hi\\end{document}",
            content_sha256="abc",
        ),
    )

    assert pdf_path == downloads / "CallumMackenzieResume1.pdf"
    assert pdf_path.read_bytes() == b"pdf"
    assert not (resume_root / "role-1" / "resume.tex").exists()


def test_role_resume_resource_list_hides_compile_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True)
    (role_dir / "resume.tex").write_text("resume")
    (role_dir / "resume-tectonic.tex").write_text("generated")
    (role_dir / "resume-tectonic.pdf").write_bytes(b"pdf")
    (role_dir / "resume-tectonic.log").write_text("log")
    (role_dir / "logo.png").write_bytes(b"png")

    assert web_server._list_role_resume_resources(1) == [{"filename": "logo.png", "bytes": 3}]


def test_config_payload_returns_current_settings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-config.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "get_central_passkey", lambda: None)

    defaults = build_config_payload()

    assert defaults["values"] == {}
    assert defaults["recommendation_history_count"] == 0
    assert defaults["central"] == {
        "api_url": DEFAULT_CENTRAL_API_URL,
        "passkey_configured": False,
        "companies_linked": 0,
        "companies_unlinked": 0,
        "companies_needs_review": 0,
        "companies_failed": 0,
    }
    assert defaults["settings"] == [
        {
            "key": "applicant_first_name",
            "label": "first name",
            "description": "used for saved resume and cover letter PDF filenames",
            "control": "text",
            "value": "",
            "default": "",
            "editable": True,
        },
        {
            "key": "applicant_last_name",
            "label": "last name",
            "description": "used for saved resume and cover letter PDF filenames",
            "control": "text",
            "value": "",
            "default": "",
            "editable": True,
        },
        {
            "key": "include_graduate_degree_roles",
            "label": "graduate-degree roles",
            "description": "include roles that require or strongly prefer a graduate degree",
            "control": "toggle",
            "value": False,
            "default": False,
            "editable": True,
        },
        {
            "key": "include_hardware_roles",
            "label": "hardware roles",
            "description": "include hardware, embedded, fpga, and silicon-heavy roles",
            "control": "toggle",
            "value": False,
            "default": False,
            "editable": True,
        },
        {
            "key": "require_software_keywords",
            "label": "software keywords",
            "description": "reject roles without software-oriented keywords",
            "control": "toggle",
            "value": True,
            "default": True,
            "editable": True,
        },
        {
            "key": "internship_mode",
            "label": "internship mode",
            "description": "require intern evidence before tracking roles",
            "control": "toggle",
            "value": True,
            "default": True,
            "editable": True,
        },
        {
            "key": "location_filter",
            "label": "location filter",
            "description": (
                "only applies while scanning; existing roles are unaffected "
                "unless re-filtered"
            ),
            "control": "select",
            "value": "all",
            "default": "all",
            "editable": True,
            "options": [
                {"value": "canada", "label": "Canada"},
                {"value": "usa", "label": "USA"},
                {"value": "north_america", "label": "North America"},
                {"value": "international", "label": "International"},
                {"value": "all", "label": "All"},
            ],
        },
    ]


def test_config_endpoint_updates_settings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-config-endpoint.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "get_central_passkey", lambda: None)
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base_url = f"http://127.0.0.1:{port}"

        with urlopen(f"{base_url}/api/config", timeout=5) as response:
            defaults = json.loads(response.read().decode())

        request = Request(
            f"{base_url}/api/config",
            data=json.dumps(
                {
                    "include_graduate_degree_roles": True,
                    "applicant_first_name": "Callum",
                    "applicant_last_name": "Mackenzie",
                    "require_software_keywords": False,
                    "internship_mode": False,
                    "location_filter": "north_america",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            updated = json.loads(response.read().decode())

        assert response.status == 200
        default_values = {setting["key"]: setting["value"] for setting in defaults["settings"]}
        assert default_values["include_graduate_degree_roles"] is False
        assert updated["values"] == {
            "applicant_first_name": "Callum",
            "applicant_last_name": "Mackenzie",
            "include_graduate_degree_roles": "true",
            "internship_mode": "false",
            "location_filter": "north_america",
            "require_software_keywords": "false",
        }
        setting_values = {setting["key"]: setting["value"] for setting in updated["settings"]}
        assert setting_values == {
            "applicant_first_name": "Callum",
            "applicant_last_name": "Mackenzie",
            "include_graduate_degree_roles": True,
            "include_hardware_roles": False,
            "require_software_keywords": False,
            "internship_mode": False,
            "location_filter": "north_america",
        }
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_central_settings_and_company_sync_endpoints(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-central-settings.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    saved_passkey: dict[str, str | None] = {"value": None}
    monkeypatch.setattr(web_server, "get_central_passkey", lambda: saved_passkey["value"])
    monkeypatch.setattr(
        web_server,
        "set_central_passkey",
        lambda passkey: saved_passkey.update({"value": passkey}),
    )
    monkeypatch.setattr(
        web_server,
        "resolve_unlinked_companies",
        lambda connection, client: SimpleNamespace(
            linked=1,
            created=0,
            needs_review=0,
            failed=0,
        ),
    )
    monkeypatch.setattr(
        web_server,
        "pull_companies",
        lambda connection, client: SimpleNamespace(
            companies_created=2,
            companies_linked=1,
            companies_existing=3,
        ),
    )

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base_url = f"http://127.0.0.1:{port}"

        config_request = Request(
            f"{base_url}/api/config",
            data=json.dumps(
                {
                    "central_api_url": "https://central.example",
                    "central_passkey": "secret-passkey",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(config_request, timeout=5) as response:
            config = json.loads(response.read().decode())

        sync_request = Request(
            f"{base_url}/api/central/resolve-companies",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(sync_request, timeout=5) as response:
            sync_payload = json.loads(response.read().decode())

        assert config["central"]["api_url"] == "https://central.example"
        assert config["central"]["passkey_configured"] is True
        assert saved_passkey["value"] == "secret-passkey"
        assert sync_payload["result"] == {
            "linked": 1,
            "created": 0,
            "needs_review": 0,
            "failed": 0,
        }
        assert sync_payload["pulled_companies"] == {
            "created": 2,
            "linked": 1,
            "existing": 3,
        }
        assert sync_payload["config"]["central"]["api_url"] == "https://central.example"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_recommendation_history_clear_endpoint_removes_feedback_decisions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-recommendation-history-clear.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    with db.connect() as connection:
        db.run_migrations(connection)
        company = add_company(connection, Company(name="Acme"))
        role = Role(
            company_id=company.id or 1,
            title="Backend Intern",
            role_url="https://example.com/jobs/backend",
            description="Python systems",
        )
        record_resume_feedback_history(
            connection,
            role=role,
            feedback_index=0,
            feedback={
                "title": "add skills matching the posting: Python",
                "detail": "add Python",
            },
            response="accepted",
        )

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/recommendation-history/clear",
            data=b"{}",
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert payload["cleared"] is True
        assert payload["deleted_count"] == 1
        assert payload["config"]["recommendation_history_count"] == 0
        with db.connect() as connection:
            assert count_resume_feedback_history(connection) == 0
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_app_update_endpoint_starts_detached_update_and_shutdown(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-app-update.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    popen_calls: list[dict[str, object]] = []
    shutdown_called = Event()

    class FakeProcess:
        pass

    def fake_popen(
        args: list[str],
        *,
        cwd: Path,
        start_new_session: bool,
    ) -> FakeProcess:
        popen_calls.append(
            {
                "args": args,
                "cwd": cwd,
                "start_new_session": start_new_session,
            }
        )
        return FakeProcess()

    def fake_shutdown(_server: object) -> None:
        shutdown_called.set()

    monkeypatch.setattr(web_server.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(web_server, "_shutdown_server", fake_shutdown)

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/app/update",
            data=b"{}",
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 202
        assert payload["message"] == "update started; callumployed will restart shortly"
        assert shutdown_called.wait(timeout=5)
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert len(popen_calls) == 1
    call = popen_calls[0]
    assert call["start_new_session"] is True
    args = call["args"]
    assert isinstance(args, list)
    assert args[:2] == ["bash", "-lc"]
    script = args[2]
    assert "scripts/install.sh" in script
    assert f"--port {port}" in script


def test_company_management_endpoints_create_link_and_delete_link(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-company-management.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        company_request = Request(
            f"http://127.0.0.1:{port}/api/companies",
            data=json.dumps(
                {
                    "name": "Acme",
                    "notes": "interesting infra team",
                    "career_url": "https://example.com/careers",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(company_request, timeout=5) as response:
            created_payload = json.loads(response.read().decode())

        assert response.status == 200
        [company] = created_payload["companies"]
        assert company["name"] == "Acme"
        assert company["notes"] == "interesting infra team"
        assert company["career_pages"][0]["url"] == "https://example.com/careers"

        company_id = company["id"]
        update_request = Request(
            f"http://127.0.0.1:{port}/api/companies/{company_id}",
            data=json.dumps(
                {
                    "notes": "autosaved note",
                    "prestige_tier": "1",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(update_request, timeout=5) as response:
            updated_payload = json.loads(response.read().decode())

        assert response.status == 200
        [company] = updated_payload["companies"]
        assert company["notes"] == "autosaved note"
        assert company["prestige_tier"] == "1"

        invalid_tier_request = Request(
            f"http://127.0.0.1:{port}/api/companies/{company_id}",
            data=json.dumps(
                {
                    "notes": "autosaved note",
                    "prestige_tier": "A",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with pytest.raises(HTTPError) as error:
            urlopen(invalid_tier_request, timeout=5)

        assert error.value.code == 400

        link_request = Request(
            f"http://127.0.0.1:{port}/api/companies/{company_id}/career-pages",
            data=json.dumps(
                {
                    "label": "students",
                    "url": "https://example.com/students",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(link_request, timeout=5) as response:
            linked_payload = json.loads(response.read().decode())

        assert response.status == 200
        [company] = linked_payload["companies"]
        assert [page["label"] for page in company["career_pages"]] == ["Main", "students"]

        career_page_id = company["career_pages"][0]["id"]
        delete_request = Request(
            f"http://127.0.0.1:{port}/api/company-career-pages/{career_page_id}",
            method="DELETE",
        )

        with urlopen(delete_request, timeout=5) as response:
            deleted_payload = json.loads(response.read().decode())

        assert response.status == 200
        [company] = deleted_payload["companies"]
        assert [page["url"] for page in company["career_pages"]] == [
            "https://example.com/students"
        ]

        delete_company_request = Request(
            f"http://127.0.0.1:{port}/api/companies/{company_id}",
            method="DELETE",
        )

        with urlopen(delete_company_request, timeout=5) as response:
            deleted_company_payload = json.loads(response.read().decode())

        assert response.status == 200
        assert deleted_company_payload["companies"] == []
        with db.connect() as connection:
            deactivated_company = get_company(connection, company_id)
            assert deactivated_company.is_active is False
            assert [
                page.url for page in list_company_career_pages(connection, company_id)
            ] == ["https://example.com/students"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_scan_all_endpoint_runs_in_background_and_reports_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-scan-all.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)

    scan_started = Event()
    scan_release = Event()

    async def fake_scan_company(*args: object, **kwargs: object) -> None:
        scan_started.set()
        await asyncio.to_thread(scan_release.wait, 2)

    monkeypatch.setattr("callumployed.web.server.run_scan_company", fake_scan_company)

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base_url = f"http://127.0.0.1:{port}"
        request = Request(f"{base_url}/api/scan/all", data=b"{}", method="POST")

        with urlopen(request, timeout=5) as response:
            started_payload = json.loads(response.read().decode())

        assert response.status == 202
        assert started_payload["scanning"] is True
        assert scan_started.wait(timeout=5)

        with urlopen(f"{base_url}/api/scan/status", timeout=5) as response:
            scanning_payload = json.loads(response.read().decode())
        assert scanning_payload["scanning"] is True
        assert scanning_payload["total_companies"] == 1

        scan_release.set()
        for _ in range(20):
            with urlopen(f"{base_url}/api/scan/status", timeout=5) as response:
                finished_payload = json.loads(response.read().decode())
            if not finished_payload["scanning"]:
                break
            scan_release.wait(timeout=0.05)

        assert finished_payload["scanning"] is False
        assert finished_payload["completed_companies"] == 1
        assert finished_payload["last_scan_at"] is not None
    finally:
        scan_release.set()
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_scan_all_endpoint_can_cancel_running_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-scan-cancel.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "SCAN_COORDINATOR", ScanCoordinator())
    with db.connect() as connection:
        db.run_migrations(connection)
        add_company(connection, Company(name="Acme"))

    scan_started = Event()
    scan_release = Event()

    async def fake_scan_company(*args: object, **kwargs: object) -> None:
        scan_started.set()
        await asyncio.to_thread(scan_release.wait, 5)

    monkeypatch.setattr("callumployed.web.server.run_scan_company", fake_scan_company)

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base_url = f"http://127.0.0.1:{port}"

        with urlopen(Request(f"{base_url}/api/scan/all", data=b"{}", method="POST"), timeout=5):
            pass
        assert scan_started.wait(timeout=5)

        with urlopen(
            Request(f"{base_url}/api/scan/cancel", data=b"{}", method="POST"),
            timeout=5,
        ) as response:
            cancel_payload = json.loads(response.read().decode())

        assert response.status == 202
        assert cancel_payload["cancel_requested"] is True

        for _ in range(20):
            with urlopen(f"{base_url}/api/scan/status", timeout=5) as response:
                finished_payload = json.loads(response.read().decode())
            if not finished_payload["scanning"]:
                break
            scan_release.wait(timeout=0.05)

        assert finished_payload["scanning"] is False
        assert finished_payload["cancel_requested"] is False
        assert finished_payload["error"] == "Cancelled scan while scanning Acme."
    finally:
        scan_release.set()
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_scan_status_reports_recent_company_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-scan-failures.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    coordinator = ScanCoordinator()
    monkeypatch.setattr(web_server, "SCAN_COORDINATOR", coordinator)
    with db.connect() as connection:
        db.run_migrations(connection)
        add_company(connection, Company(name="Acme"))

    async def fake_scan_company(*args: object, **kwargs: object) -> None:
        raise RuntimeError("AI classification failed: quota exceeded")

    monkeypatch.setattr("callumployed.web.server.run_scan_company", fake_scan_company)

    asyncio.run(coordinator._scan_all_companies())

    payload = build_scan_status_payload()

    assert payload["failed_companies"] == 1
    assert payload["failures"] == [
        {
            "company_id": 1,
            "company_name": "Acme",
            "error": "AI classification failed: quota exceeded",
        }
    ]


def test_scan_all_times_out_company_and_continues(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-scan-all-timeout.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    with db.connect() as connection:
        db.run_migrations(connection)
        slow_company = add_company(connection, Company(name="A Slowco"))
        fast_company = add_company(connection, Company(name="B Fastco"))
    assert slow_company.id is not None
    assert fast_company.id is not None

    scanned_companies: list[str] = []

    async def fake_scan_company(company: Company, **_kwargs: object) -> None:
        scanned_companies.append(company.name)
        with db.connect() as connection:
            scan_run = create_scan_run(connection, company.id)
        if company.name == "A Slowco":
            await asyncio.sleep(1)
            return
        with db.connect() as connection:
            finish_scan_run(connection, scan_run.id, ScanStatus.SUCCEEDED)

    monkeypatch.setattr("callumployed.web.server.run_scan_company", fake_scan_company)
    coordinator = ScanCoordinator(company_timeout_seconds=0.01)

    asyncio.run(coordinator._scan_all_companies())

    snapshot = coordinator.snapshot()
    assert scanned_companies == ["A Slowco", "B Fastco"]
    assert snapshot.completed_companies == 2
    assert snapshot.failed_companies == 1
    assert snapshot.error == "Timed out scanning A Slowco after 0.01 seconds."

    with db.connect() as connection:
        slow_scan = list_scan_runs(connection, company_id=slow_company.id, limit=1)[0]
        fast_scan = list_scan_runs(connection, company_id=fast_company.id, limit=1)[0]

    assert slow_scan.scan_status == ScanStatus.FAILED
    assert slow_scan.error == "Timed out scanning A Slowco after 0.01 seconds."
    assert fast_scan.scan_status == ScanStatus.SUCCEEDED


def test_scan_status_reports_persisted_started_time_for_interrupted_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-interrupted-scan.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr("callumployed.web.server.SCAN_COORDINATOR", ScanCoordinator())
    with db.connect() as connection:
        db.run_migrations(connection)
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        scan_run = create_scan_run(connection, company.id)

    payload = build_scan_status_payload()

    expected_started_at = f"{scan_run.started_at.isoformat()}Z"
    assert payload["last_scan_at"] == expected_started_at
    assert payload["latest_scan"]["started_at"] == expected_started_at
    assert payload["latest_scan"]["finished_at"] is None


def test_tracker_payload_groups_roles_by_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        [
            "roles",
            "add",
            "1",
            "Backend Engineer",
            "https://example.com/jobs/backend",
            "--location",
            "Vancouver",
            "--notes",
            "Remote-friendly team.",
        ],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "applied"], env=env)

    payload = build_tracker_payload()

    assert payload["stats"]["companies_total"] == 1
    assert payload["stats"]["jobs_total"] == 1
    assert payload["stats"]["applications_total"] == 1
    applied = next(status for status in payload["statuses"] if status["key"] == "applied")
    assert applied["count"] == 1
    assert applied["jobs"][0]["company_name"] == "Acme"
    assert applied["jobs"][0]["title"] == "Backend Engineer"
    assert applied["jobs"][0]["location"] == "Vancouver"
    assert applied["jobs"][0]["notes"] == "Remote-friendly team."
    assert applied["jobs"][0]["first_seen_at"] is not None
    assert applied["jobs"][0]["first_seen_at"].endswith("Z")
    assert applied["jobs"][0]["created_at"] is not None
    assert applied["jobs"][0]["created_at"].endswith("Z")
    assert applied["jobs"][0]["updated_at"].endswith("Z")


def test_tracker_payload_marks_closed_roles_updated_in_latest_scan_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-latest-closed-updates.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Older Closed", "https://example.com/jobs/older"],
        env=env,
    )
    runner.invoke(
        app,
        ["roles", "add", "1", "Latest Closed", "https://example.com/jobs/latest"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "closed"], env=env)
    runner.invoke(app, ["roles", "set-status", "2", "closed"], env=env)

    with db.connect() as connection:
        old_scan = create_scan_run(connection, 1)
        assert old_scan.id is not None
        add_role_discovery_attempt(
            connection,
            RoleDiscoveryAttempt(
                scan_run_id=old_scan.id,
                scan_candidate_id=_add_scan_candidate(
                    connection,
                    old_scan.id,
                    "https://example.com/jobs/older",
                ),
                company_id=1,
                role_id=1,
                url="https://example.com/jobs/older",
            ),
        )
        finish_scan_run(connection, old_scan.id, ScanStatus.SUCCEEDED)

        latest_scan = create_scan_run(connection, 1)
        assert latest_scan.id is not None
        add_role_discovery_attempt(
            connection,
            RoleDiscoveryAttempt(
                scan_run_id=latest_scan.id,
                scan_candidate_id=_add_scan_candidate(
                    connection,
                    latest_scan.id,
                    "https://example.com/jobs/latest",
                ),
                company_id=1,
                role_id=2,
                url="https://example.com/jobs/latest",
            ),
        )
        finish_scan_run(connection, latest_scan.id, ScanStatus.SUCCEEDED)

    payload = build_tracker_payload()
    closed = next(status for status in payload["statuses"] if status["key"] == "closed")
    assert [job["title"] for job in closed["jobs"]] == ["Latest Closed", "Older Closed"]
    jobs_by_title = {job["title"]: job for job in closed["jobs"]}
    assert jobs_by_title["Older Closed"]["updated_in_latest_scan"] is False
    assert jobs_by_title["Latest Closed"]["updated_in_latest_scan"] is True


def test_tracker_payload_marks_and_sorts_roles_with_prep_started(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-prep-started.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "No Prep", "https://example.com/jobs/no-prep"],
        env=env,
    )
    runner.invoke(
        app,
        ["roles", "add", "1", "Cover Letter Prep", "https://example.com/jobs/cl"],
        env=env,
    )
    runner.invoke(
        app,
        ["roles", "add", "1", "Resume Prep", "https://example.com/jobs/resume"],
        env=env,
    )
    for role_id in (1, 2, 3):
        runner.invoke(app, ["roles", "set-status", str(role_id), "interested"], env=env)

    cover_letter_dir = resume_root / "role-2"
    cover_letter_dir.mkdir(parents=True)
    (cover_letter_dir / "cover-letter.tex").write_text("\\documentclass{letter}")
    resume_dir = resume_root / "role-3"
    resume_dir.mkdir(parents=True)
    (resume_dir / "resume.tex").write_text("\\documentclass{article}")

    payload = build_tracker_payload()

    interested = next(status for status in payload["statuses"] if status["key"] == "interested")
    assert {job["title"] for job in interested["jobs"][:2]} == {
        "Cover Letter Prep",
        "Resume Prep",
    }
    assert interested["jobs"][2]["title"] == "No Prep"
    prep_by_title = {job["title"]: job["prep_started"] for job in interested["jobs"]}
    assert prep_by_title == {
        "Cover Letter Prep": True,
        "Resume Prep": True,
        "No Prep": False,
    }


def test_tracker_payload_marks_discovered_and_interested_roles_missing_from_latest_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-missing-latest-scan.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(app, ["companies", "add", "Beta", "https://beta.example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Missing Discovered", "https://example.com/jobs/missing"],
        env=env,
    )
    runner.invoke(
        app,
        ["roles", "add", "1", "Seen Interested", "https://example.com/jobs/seen"],
        env=env,
    )
    runner.invoke(
        app,
        ["roles", "add", "1", "Stale Interested", "https://example.com/jobs/stale"],
        env=env,
    )
    runner.invoke(
        app,
        [
            "roles",
            "add",
            "2",
            "Other Company Interested",
            "https://beta.example.com/jobs/other",
        ],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "2", "interested"], env=env)
    runner.invoke(app, ["roles", "set-status", "3", "interested"], env=env)
    runner.invoke(app, ["roles", "set-status", "4", "interested"], env=env)

    with db.connect() as connection:
        old_scan = create_scan_run(connection, 1)
        assert old_scan.id is not None
        _add_scan_candidate(connection, old_scan.id, "https://example.com/jobs/stale")
        finish_scan_run(connection, old_scan.id, ScanStatus.SUCCEEDED)

        latest_scan = create_scan_run(connection, 1)
        assert latest_scan.id is not None
        _add_scan_candidate(connection, latest_scan.id, "https://example.com/jobs/seen")
        finish_scan_run(connection, latest_scan.id, ScanStatus.SUCCEEDED)

    payload = build_tracker_payload()
    discovered = next(status for status in payload["statuses"] if status["key"] == "discovered")
    interested = next(status for status in payload["statuses"] if status["key"] == "interested")
    assert discovered["jobs"][0]["missing_from_latest_scan"] is True
    interested_by_title = {job["title"]: job for job in interested["jobs"]}
    assert interested_by_title["Seen Interested"]["missing_from_latest_scan"] is False
    assert interested_by_title["Stale Interested"]["missing_from_latest_scan"] is True
    assert interested_by_title["Other Company Interested"]["missing_from_latest_scan"] is False


def test_tracker_status_endpoint_moves_role(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-status.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/roles/1/status"
        request = Request(
            url,
            data=b'{"status":"interested"}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            response_payload = json.loads(response.read().decode())
            assert response.status == 200
        assert response_payload["role"]["updated_at"].endswith("Z")
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    interested = next(status for status in payload["statuses"] if status["key"] == "interested")
    discovered = next(status for status in payload["statuses"] if status["key"] == "discovered")
    assert interested["count"] == 1
    assert discovered["count"] == 0


def test_roles_create_endpoint_adds_role_and_runs_rescan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-role-create.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)

    async def fake_run_rescan_role(
        role_id: int,
        *,
        browser_profile_manager: object,
        update_status: bool,
    ) -> dict[str, object]:
        assert role_id == 1
        assert browser_profile_manager is not None
        assert update_status is True
        return {
            "role": Role(
                id=1,
                company_id=1,
                title="Backend Platform Intern",
                role_url="https://example.com/jobs/backend-platform-intern",
                location="Vancouver",
            )
        }

    monkeypatch.setattr(web_server, "run_rescan_role", fake_run_rescan_role)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/roles",
            data=json.dumps(
                {
                    "company_id": 1,
                    "role_url": "https://example.com/jobs/backend-platform-intern",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert payload["role"]["title"] == "Backend Platform Intern"
        assert payload["scan_error"] is None
        assert payload["tracker"]["stats"]["jobs_total"] == 1
        discovered = next(
            status for status in payload["tracker"]["statuses"] if status["key"] == "discovered"
        )
        [role] = discovered["jobs"]
        assert role["company_name"] == "Acme"
        assert role["role_url"] == "https://example.com/jobs/backend-platform-intern"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_tracker_review_later_endpoint_records_postponement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-review-later.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/roles/1/review-later"
        request = Request(url, data=b"", method="POST")

        with urlopen(request, timeout=5) as response:
            response_payload = json.loads(response.read().decode())
            assert response.status == 200
            assert response_payload["role"]["review_later_count"] == 1
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    discovered = next(status for status in payload["statuses"] if status["key"] == "discovered")
    assert discovered["jobs"][0]["review_later_count"] == 1


def test_master_resume_endpoint_uploads_and_replaces_tex_resume(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-master-resume.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base_url = f"http://127.0.0.1:{port}/api/master-resume"

        with urlopen(base_url, timeout=5) as response:
            empty_payload = json.loads(response.read().decode())
        assert empty_payload == {"master_resume": None}

        request = Request(
            base_url,
            data=json.dumps(
                {
                    "filename": "/tmp/master.tex",
                    "content": "\\documentclass{article}",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            created_payload = json.loads(response.read().decode())

        assert created_payload["master_resume"]["filename"] == "master.tex"
        assert created_payload["master_resume"]["content_bytes"] == len(
            b"\\documentclass{article}"
        )

        replacement_request = Request(
            base_url,
            data=json.dumps(
                {
                    "filename": "replacement.tex",
                    "content": "\\documentclass{article}\n\\begin{document}Hi\\end{document}",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(replacement_request, timeout=5) as response:
            replaced_payload = json.loads(response.read().decode())
        assert replaced_payload["master_resume"]["filename"] == "replacement.tex"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_master_resume_endpoint_rejects_non_tex_resume(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-master-resume-reject.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/master-resume"
        request = Request(
            url,
            data=json.dumps({"filename": "resume.pdf", "content": "not tex"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with pytest.raises(HTTPError) as error:
            urlopen(request, timeout=5)
        assert error.value.code == 400
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_master_resume_upload_replaces_resumes_for_interested_roles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-interested-resumes.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Interested", "https://example.com/interested"],
        env=env,
    )
    runner.invoke(
        app,
        ["roles", "add", "1", "Applied", "https://example.com/applied"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "interested"], env=env)
    runner.invoke(app, ["roles", "set-status", "2", "applied"], env=env)
    (resume_root / "role-1").mkdir(parents=True)
    (resume_root / "role-2").mkdir(parents=True)
    (resume_root / "role-1" / "resume.tex").write_text("old interested resume")
    (resume_root / "role-2" / "resume.tex").write_text("old applied resume")

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        request = Request(
            f"http://127.0.0.1:{server.server_address[1]}/api/master-resume",
            data=json.dumps(
                {"filename": "new.tex", "content": "new master resume"}
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert payload["interested_resumes_updated"] == 1
        assert (resume_root / "role-1" / "resume.tex").read_text() == "new master resume"
        assert (resume_root / "role-2" / "resume.tex").read_text() == "old applied resume"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_examples_endpoint_uploads_multiple_examples(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-examples.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base_url = f"http://127.0.0.1:{port}/api/cover-letter-examples"

        with urlopen(base_url, timeout=5) as response:
            empty_payload = json.loads(response.read().decode())
        assert empty_payload == {"cover_letter_examples": []}

        first_request = Request(
            base_url,
            data=json.dumps(
                {
                    "filename": "/tmp/apple-cover.tex",
                    "content": "Dear Apple,",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(first_request, timeout=5) as response:
            first_payload = json.loads(response.read().decode())

        second_request = Request(
            base_url,
            data=json.dumps(
                {
                    "filename": "stripe-cover.md",
                    "content": "Dear Stripe,",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(second_request, timeout=5) as response:
            second_payload = json.loads(response.read().decode())

        assert first_payload["cover_letter_example"]["filename"] == "apple-cover.tex"
        assert first_payload["cover_letter_example"]["content_bytes"] == len(b"Dear Apple,")
        assert [item["filename"] for item in second_payload["cover_letter_examples"]] == [
            "stripe-cover.md",
            "apple-cover.tex",
        ]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_experience_notes_endpoint_uploads_multiple_notes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-experience-notes.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base_url = f"http://127.0.0.1:{port}/api/experience-notes"

        with urlopen(base_url, timeout=5) as response:
            empty_payload = json.loads(response.read().decode())
        assert empty_payload == {"experience_notes": []}

        first_request = Request(
            base_url,
            data=json.dumps(
                {
                    "filename": "/tmp/projects.md",
                    "content": "Built a Kubernetes scheduler.",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(first_request, timeout=5) as response:
            first_payload = json.loads(response.read().decode())

        second_request = Request(
            base_url,
            data=json.dumps(
                {
                    "filename": "employment-history.txt",
                    "content": "Maintained Redis-backed operations tools.",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(second_request, timeout=5) as response:
            second_payload = json.loads(response.read().decode())

        assert first_payload["experience_note"]["filename"] == "projects.md"
        assert first_payload["experience_note"]["content_bytes"] == len(
            b"Built a Kubernetes scheduler."
        )
        assert [item["filename"] for item in second_payload["experience_notes"]] == [
            "employment-history.txt",
            "projects.md",
        ]
        with db.connect() as connection:
            notes = list_experience_notes(connection)
        assert [note.content for note in notes] == [
            "Maintained Redis-backed operations tools.",
            "Built a Kubernetes scheduler.",
        ]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_application_materials_endpoint_reports_default_collapsed_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-application-materials.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(
        web_server,
        "_resume_resources_root",
        lambda: tmp_path / "resume-resources",
    )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base_url = f"http://127.0.0.1:{port}"

        with urlopen(f"{base_url}/api/application-materials", timeout=5) as response:
            empty_payload = json.loads(response.read().decode())
        assert empty_payload["ui"]["default_collapsed"] is False
        assert empty_payload["ui"]["has_missing_required_materials"] is True
        assert empty_payload["ui"]["has_master_resume"] is False
        assert empty_payload["ui"]["cover_letter_example_count"] == 0
        assert empty_payload["ui"]["experience_note_count"] == 0
        assert empty_payload["ui"]["resume_resource_count"] == 0
        assert empty_payload["resume_resources"] == []
        assert empty_payload["experience_notes"] == []

        resume_request = Request(
            f"{base_url}/api/master-resume",
            data=json.dumps(
                {
                    "filename": "resume.tex",
                    "content": "\\documentclass{article}",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(resume_request, timeout=5):
            pass

        with urlopen(f"{base_url}/api/application-materials", timeout=5) as response:
            resume_only_payload = json.loads(response.read().decode())
        assert resume_only_payload["ui"]["default_collapsed"] is False
        assert resume_only_payload["ui"]["has_missing_required_materials"] is True
        assert resume_only_payload["ui"]["has_master_resume"] is True

        cover_letter_request = Request(
            f"{base_url}/api/cover-letter-examples",
            data=json.dumps({"filename": "cover.md", "content": "Dear team,"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(cover_letter_request, timeout=5):
            pass

        note_request = Request(
            f"{base_url}/api/experience-notes",
            data=json.dumps(
                {"filename": "projects.md", "content": "Built data platform tools."}
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(note_request, timeout=5):
            pass

        with urlopen(f"{base_url}/api/application-materials", timeout=5) as response:
            ready_payload = json.loads(response.read().decode())
        assert ready_payload["ui"]["default_collapsed"] is True
        assert ready_payload["ui"]["has_missing_required_materials"] is False
        assert ready_payload["ui"]["cover_letter_example_count"] == 1
        assert ready_payload["ui"]["experience_note_count"] == 1
        assert ready_payload["ui"]["resume_resource_count"] == 0
        assert ready_payload["master_resume"]["filename"] == "resume.tex"
        assert ready_payload["cover_letter_examples"][0]["filename"] == "cover.md"
        assert ready_payload["experience_notes"][0]["filename"] == "projects.md"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_examples_endpoint_extracts_docx_upload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-docx.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/cover-letter-examples"
        request = Request(
            url,
            data=json.dumps(
                {
                    "filename": "google-cover.docx",
                    "content_base64": base64.b64encode(
                        _minimal_docx(
                            [
                                "Dear Google,",
                                "I am excited about this internship.",
                            ]
                        )
                    ).decode(),
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert payload["cover_letter_example"]["filename"] == "google-cover.docx"
        with db.connect() as connection:
            examples = list_cover_letter_examples(connection)
        assert len(examples) == 1
        assert examples[0].content == (
            "Dear Google,\nI am excited about this internship."
        )
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_examples_endpoint_rejects_empty_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-examples-reject.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/cover-letter-examples"
        request = Request(
            url,
            data=json.dumps({"filename": "empty.tex", "content": "  "}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with pytest.raises(HTTPError) as error:
            urlopen(request, timeout=5)
        assert error.value.code == 400
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_tracker_status_endpoint_rejects_unsupported_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-status-reject.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/roles/1/status"
        request = Request(
            url,
            data=b'{"status":"prepared"}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with pytest.raises(HTTPError) as error:
            urlopen(request, timeout=5)
        assert error.value.code == 400
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.mark.parametrize("status", ["OA", "interview", "rejected"])
def test_tracker_status_endpoint_moves_applied_role(
    status: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / f"tracker-applied-{status}.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "applied"], env=env)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/roles/1/status"
        request = Request(
            url,
            data=f'{{"status":"{status}"}}'.encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    applied = next(item for item in payload["statuses"] if item["key"] == "applied")
    target = next(item for item in payload["statuses"] if item["key"] == status)
    assert applied["count"] == 0
    assert target["count"] == 1


@pytest.mark.parametrize("status", ["applied", "disinterested"])
def test_tracker_status_endpoint_moves_interested_role(
    status: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / f"tracker-interested-{status}.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "interested"], env=env)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/roles/1/status"
        request = Request(
            url,
            data=f'{{"status":"{status}"}}'.encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    interested = next(item for item in payload["statuses"] if item["key"] == "interested")
    target = next(item for item in payload["statuses"] if item["key"] == status)
    assert interested["count"] == 0
    assert target["count"] == 1


def test_tracker_status_endpoint_moves_disinterested_role_to_interested(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-disinterested-interested.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "disinterested"], env=env)

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        request = Request(
            f"http://127.0.0.1:{server.server_address[1]}/api/roles/1/status",
            data=b'{"status":"interested"}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    disinterested = next(item for item in payload["statuses"] if item["key"] == "disinterested")
    interested = next(item for item in payload["statuses"] if item["key"] == "interested")
    assert disinterested["count"] == 0
    assert interested["count"] == 1


@pytest.mark.parametrize("status", ["interview", "disinterested", "rejected"])
def test_tracker_status_endpoint_moves_oa_role(
    status: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / f"tracker-oa-{status}.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "OA"], env=env)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/roles/1/status"
        request = Request(
            url,
            data=f'{{"status":"{status}"}}'.encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    oa = next(item for item in payload["statuses"] if item["key"] == "OA")
    target = next(item for item in payload["statuses"] if item["key"] == status)
    assert oa["count"] == 0
    assert target["count"] == 1


@pytest.mark.parametrize("status", ["rejected", "offer"])
def test_tracker_status_endpoint_moves_interview_role(
    status: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / f"tracker-interview-{status}.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "interview"], env=env)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/roles/1/status"
        request = Request(
            url,
            data=f'{{"status":"{status}"}}'.encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    interview = next(item for item in payload["statuses"] if item["key"] == "interview")
    target = next(item for item in payload["statuses"] if item["key"] == status)
    assert interview["count"] == 0
    assert target["count"] == 1


def test_tracker_status_endpoint_moves_closed_role_to_interested(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-closed-interested.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}

    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Engineer", "https://example.com/jobs/backend"],
        env=env,
    )
    runner.invoke(app, ["roles", "set-status", "1", "closed"], env=env)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/api/roles/1/status"
        request = Request(
            url,
            data=b'{"status":"interested"}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    closed = next(item for item in payload["statuses"] if item["key"] == "closed")
    interested = next(item for item in payload["statuses"] if item["key"] == "interested")
    assert closed["count"] == 0
    assert interested["count"] == 1
