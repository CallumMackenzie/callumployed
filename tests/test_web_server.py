import ast
import asyncio
import base64
import gzip
import inspect
import json
import os
import socket
from io import BytesIO
from pathlib import Path
from threading import Event, Thread
from types import SimpleNamespace
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from zipfile import ZipFile

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
from typer.testing import CliRunner

import callumployed.web.server as web_server
from callumployed.agents.cover_letter import ApplicantProfile
from callumployed.central.client import CentralStoreError
from callumployed.central.config import DEFAULT_CENTRAL_API_URL
from callumployed.central.models import ResolveCompanyRequest, ResolveCompanyResponse
from callumployed.cli import app
from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    ExperienceNote,
    Role,
    RoleDiscoveryAttempt,
    RoleStatus,
    ScanStatus,
)
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    add_cover_letter_example,
    add_experience_note,
    add_role,
    add_role_discovery_attempt,
    count_resume_feedback_history,
    create_scan_run,
    finish_scan_run,
    get_company,
    get_config_value,
    get_role,
    list_companies,
    list_company_career_pages,
    list_cover_letter_examples,
    list_experience_notes,
    list_scan_runs,
    record_resume_feedback_history,
    set_role_status,
)
from callumployed.services import autoprep as autoprep_service
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


def test_debounced_action_collapses_changes_into_one_callback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    timers: list[SimpleNamespace] = []

    def fake_timer(_delay: float, callback: object) -> SimpleNamespace:
        timer = SimpleNamespace(
            callback=callback,
            daemon=False,
            cancelled=False,
            start=lambda: None,
        )
        timer.cancel = lambda: setattr(timer, "cancelled", True)
        timers.append(timer)
        return timer

    monkeypatch.setattr(web_server.threading, "Timer", fake_timer)
    calls: list[bool] = []
    action = web_server.DebouncedAction(lambda: calls.append(True), delay_seconds=30)

    action.schedule()
    action.schedule()
    action.schedule()
    assert [timer.cancelled for timer in timers] == [True, True, False]

    timers[0].callback()
    timers[1].callback()
    assert calls == []

    timers[-1].callback()
    assert calls == [True]

    action.schedule()
    final_timer = timers[-1]
    action.close()
    action.schedule()
    final_timer.callback()

    assert final_timer.cancelled is True
    assert len(timers) == 4
    assert calls == [True]


def _add_positioned_text(
    writer: PdfWriter,
    page: object,
    y_positions: tuple[int, ...],
    transform: str | None = None,
) -> None:
    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    font_ref = writer._add_object(font)
    page[NameObject("/Resources")] = DictionaryObject(  # type: ignore[index]
        {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font_ref})}
    )
    stream = DecodedStreamObject()
    commands = [
        f"BT /F1 12 Tf 50 {y} Td (Resume content line {index}) Tj ET"
        for index, y in enumerate(y_positions)
    ]
    content = "\n".join(commands)
    if transform is not None:
        content = f"q {transform} cm\n{content}\nQ"
    stream.set_data(content.encode("ascii"))
    page[NameObject("/Contents")] = writer._add_object(stream)  # type: ignore[index]


def _valid_pdf_bytes(page_count: int = 1) -> bytes:
    output = BytesIO()
    writer = PdfWriter()
    for _ in range(page_count):
        page = writer.add_blank_page(width=612, height=792)
        _add_positioned_text(writer, page, (740, 600, 450, 300, 150, 60))
    writer.write(output)
    return output.getvalue()


def _blank_pdf_bytes() -> bytes:
    output = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.write(output)
    return output.getvalue()


def _positioned_text_pdf_bytes(
    y_positions: tuple[int, ...],
    *,
    transform: str | None = None,
) -> bytes:
    output = BytesIO()
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    _add_positioned_text(writer, page, y_positions, transform)
    writer.write(output)
    return output.getvalue()


def test_local_server_enables_address_reuse_before_binding() -> None:
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    try:
        assert server.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
    finally:
        server.server_close()


def test_application_answer_can_be_regenerated_and_deleted_through_role_scoped_api(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "application-answer-actions.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Engineer",
                role_url="https://example.com/engineer",
                role_status=RoleStatus.INTERESTED,
                description="Build reliable software.",
            ),
        )
        assert role.id is not None
        autoprep_service.ensure_autoprep_schema(connection)
        web_server.set_config_value(connection, "llm_provider", "codex")
        pending = autoprep_service.create_application_answer(
            connection,
            role.id,
            question="Why Acme?",
            backend="openai",
        )
        saved = autoprep_service.complete_application_answer(
            connection,
            int(pending["id"]),
            answer="The previous valid answer.",
        )

    monkeypatch.setattr(
        web_server,
        "generate_saved_application_answer",
        lambda role_id, *, question, llm_settings: {
            "answer": "Acme Builds Reliable Products.",
            "session_id": None,
            "sources": [{"kind": "saved_material", "title": "Resume"}],
            "research": {"used_web": False},
        },
    )
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        endpoint = (
            f"http://127.0.0.1:{port}/api/autoprep/roles/{role.id}"
            f"/application-answers/{saved['id']}"
        )
        request = Request(f"{endpoint}/regenerate", data=b"", method="POST")
        with urlopen(request, timeout=5) as response:
            regenerated = json.loads(response.read())["answer"]

        assert regenerated["id"] == saved["id"]
        assert regenerated["answer"] == "Acme Builds Reliable Products."
        assert regenerated["backend"] == "codex"
        assert "session_id" not in regenerated
        assert regenerated["status"] == "completed"

        with urlopen(Request(endpoint, method="DELETE"), timeout=5) as response:
            deleted = json.loads(response.read())
        assert deleted == {"deleted_id": saved["id"]}

        with urlopen(
            f"http://127.0.0.1:{port}/api/autoprep/roles/{role.id}/application-answers",
            timeout=5,
        ) as response:
            assert json.loads(response.read()) == {"answers": []}
        with db.connect() as connection:
            revision_count = connection.execute(
                "SELECT COUNT(*) AS count FROM application_answer_revisions WHERE answer_id = ?",
                (saved["id"],),
            ).fetchone()["count"]
        assert revision_count == 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_application_answer_quota_failure_is_not_exposed_or_counted_as_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "application-answer-quota.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Engineer",
                role_url="https://example.com/engineer",
                role_status=RoleStatus.INTERESTED,
            ),
        )
        assert role.id is not None

    def exhausted_provider(
        _role_id: int, *, question: str, llm_settings: object
    ) -> dict[str, Any]:
        assert question
        assert llm_settings
        raise RuntimeError(
            "error code: 429 - insufficient_quota credit_balance_exhausted "
            "https://platform.openai.com/settings/organization/billing/"
        )

    monkeypatch.setattr(web_server, "generate_saved_application_answer", exhausted_provider)
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        endpoint = (
            f"http://127.0.0.1:{server.server_address[1]}/api/autoprep/roles/"
            f"{role.id}/application-answers"
        )
        request = Request(
            endpoint,
            data=json.dumps({"question": "What AI tools do you use?"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(HTTPError) as response_error:
            urlopen(request, timeout=5)
        assert response_error.value.code == 503
        payload = json.loads(response_error.value.read())["answer"]

        assert payload["status"] == "failed"
        assert payload["answer"] is None
        assert "no remaining credits" in payload["error"]
        assert "platform.openai.com" not in payload["error"]
        assert "credit_balance_exhausted" not in payload["error"]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


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


def test_company_tier_guide_state_defaults_closed_and_survives_server_restarts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "company-tier-guide-state.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        with urlopen(f"{base_url}/api/companies", timeout=5) as response:
            initial = json.loads(response.read().decode())
        assert initial["company_tier_guide_open"] is False

        open_request = Request(
            f"{base_url}/api/ui-state/company-tier-guide",
            data=json.dumps({"open": True}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(open_request, timeout=5) as response:
            saved = json.loads(response.read().decode())
        assert saved == {"company_tier_guide_open": True}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    restarted_server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    restarted_thread = Thread(target=restarted_server.serve_forever, daemon=True)
    restarted_thread.start()
    try:
        base_url = f"http://127.0.0.1:{restarted_server.server_address[1]}"
        with urlopen(f"{base_url}/api/companies", timeout=5) as response:
            restored = json.loads(response.read().decode())
        assert restored["company_tier_guide_open"] is True

        close_request = Request(
            f"{base_url}/api/ui-state/company-tier-guide",
            data=json.dumps({"open": False}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(close_request, timeout=5) as response:
            closed = json.loads(response.read().decode())
        assert closed == {"company_tier_guide_open": False}
    finally:
        restarted_server.shutdown()
        restarted_server.server_close()
        restarted_thread.join(timeout=5)

    assert build_companies_payload()["company_tier_guide_open"] is False


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
    body = "".join(f"<w:p><w:r><w:t>{paragraph}</w:t></w:r></w:p>" for paragraph in paragraphs)
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
            body = response.read()
            assert body.startswith(b'<?xml version="1.0" encoding="UTF-8"?>')
            assert b"path { fill: #00897b; }" in body
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_pwa_manifest_and_apple_icon_are_served_with_correct_content_types() -> None:
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urlopen(f"http://127.0.0.1:{port}/assets/manifest.webmanifest", timeout=5) as response:
            assert response.status == 200
            assert response.headers["Content-Type"] == "application/manifest+json; charset=utf-8"
            manifest = json.loads(response.read())
        with urlopen(f"http://127.0.0.1:{port}/assets/apple-touch-icon.png", timeout=5) as response:
            assert response.status == 200
            assert response.headers["Content-Type"] == "image/png"
            assert response.read().startswith(b"\x89PNG\r\n\x1a\n")

        assert manifest["display"] == "standalone"
        assert {icon["sizes"] for icon in manifest["icons"]} == {"192x192", "512x512"}
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
        with urlopen(f"http://127.0.0.1:{port}/assets/app.js", timeout=5) as response:
            assert response.status == 200
            assert response.headers["Content-Type"] == "text/javascript; charset=utf-8"
            app_javascript = response.read().decode()

        static_directory = Path(web_server.__file__).with_name("static")
        repository_root = Path(web_server.__file__).parents[3]
        markup = index_markup
        app_styles = (static_directory / "app.css").read_text()

        assert not (repository_root / "frontend").exists()
        assert not (static_directory / "build").exists()
        assert not (static_directory / "shell.html").exists()
        assert (static_directory / "app.js").read_text() == app_javascript
        assert "dangerouslySetInnerHTML" not in markup
        assert "dangerouslySetInnerHTML" not in app_javascript
        assert '<div id="root"></div>' not in index_markup
        assert '<script type="module" src="/assets/app.js?v=vanilla-20260904-23"></script>' in (
            index_markup
        )

        assert 'id="toggle-all"' in markup
        assert (
            '<link rel="icon" href="/assets/camackenzie-logo.svg?v=20260827-2" '
            'type="image/svg+xml" />' in index_markup
        )
        assert 'rel="apple-touch-icon"' in index_markup
        assert 'sizes="180x180"' in index_markup
        assert 'href="/assets/apple-touch-icon.png?v=20260827-2"' in index_markup
        assert '<link rel="manifest" href="/assets/manifest.webmanifest" />' in index_markup
        assert '<meta name="apple-mobile-web-app-capable" content="yes" />' in index_markup
        assert '<meta name="apple-mobile-web-app-title" content="callumployed" />' in index_markup

        assert "expand all" in markup
        assert 'id="expand-all"' not in markup
        assert 'id="collapse-all"' not in markup
        assert 'id="scan-all-button"' in markup
        assert 'id="manage-companies-button"' in markup
        assert 'id="companies-view"' in markup
        assert 'class="company-form-panel"' in markup
        assert 'id="company-create-form"' in markup
        assert 'id="company-tier-guide-heading"' in markup
        assert 'id="company-tier-guide-list"' in markup
        assert '<details class="company-tier-guide" id="company-tier-guide"' in markup
        assert '<details class="company-tier-guide" id="company-tier-guide" open' not in markup
        assert 'class="company-tier-guide-header"' in markup
        assert "0 is highest priority." in markup
        assert "tiers 5 through 7 progressively prioritize gaining experience" in markup
        assert "COMPANY_TIER_DEFINITIONS" in app_javascript
        assert 'fetch("/api/ui-state/company-tier-guide", {' in app_javascript
        assert "applyCompanyTierGuideState(undefined);" in app_javascript
        assert "renderCompanies(await response.json(), message, true);" in app_javascript
        assert 'companyTierGuide.addEventListener("toggle"' in app_javascript
        for tier in range(8):
            assert f'value: "{tier}"' in app_javascript
            assert f".company-tier-{tier}" in app_styles
        assert 'examples: ["TikTok", "Rivian", "Disney"' in app_javascript
        assert 'shortLabel: "broad fallback"' in app_javascript
        assert 'shortLabel: "last resort"' in app_javascript
        assert 'class="company-tier-badge"' in app_javascript
        assert 'class="company-tier-select"' in app_javascript
        assert 'class="company-tier-select-shell"' in app_javascript
        assert 'id="company-create-status"' in markup
        assert 'id="company-url-input"' in markup
        assert 'name="career_url"' in markup
        assert 'inputmode="url"' in markup
        assert "normalizeCompanyCareerUrl" in app_javascript
        assert '`https://${trimmed}`' in app_javascript
        assert 'id="companies-list"' in markup
        assert 'id="prep-interested"' not in markup
        assert 'class="quick-action" type="button" id="prepped-roles"' in markup
        assert 'id="autoprep-view"' not in markup
        assert 'id="autoprep-selected"' not in markup
        assert 'id="autoprep-interested"' not in app_javascript
        assert "function submitAutoprepSelection" not in app_javascript
        assert "body: JSON.stringify({role_ids:" not in app_javascript
        assert 'id="role-add-form"' in markup
        assert 'list="role-company-options"' in markup
        assert 'id="role-company-options"' in markup
        assert "renderRoleCompanyOptions(companies)" in app_javascript
        assert "{ company_id: company.id } : { company_name: companyName }" in app_javascript
        assert 'roleAddStatus.textContent = "pick a saved company."' not in app_javascript
        assert "Add Explicit Role" in markup
        assert 'id="role-url-input"' in markup
        assert 'id="role-company-input"' in markup
        assert 'id="role-company-options"' in markup
        assert "added to Interested and queued for prep." in app_javascript
        assert 'id="prep-view"' in markup
        prep_later_index = markup.index('data-prep-action="later"')
        autoprep_action_index = markup.index('data-prep-action="autoprep"')
        move_applied_index = markup.index('data-prep-action="applied"')
        assert prep_later_index < autoprep_action_index < move_applied_index
        assert 'id="resume-resource-upload"' in markup
        assert 'id="resume-resource-upload-button"' in markup
        assert 'id="resume-resource-list"' in markup
        assert 'id="scan-summary"' in markup
        assert markup.index('id="review-discovered"') < markup.index('id="prepped-roles"')
        assert markup.index('id="prepped-roles"') < markup.index('id="scan-all-button"')
        assert markup.index('id="scan-all-button"') < markup.index('id="manage-companies-button"')
        assert markup.index('id="manage-companies-button"') < markup.index('id="scan-summary"')
        assert markup.index('id="scan-all-button"') < markup.index('class="status-toolbar"')
        assert markup.index('id="status-list"') < markup.index('id="role-add-form"')
        assert 'id="scan-status-bar"' in markup
        assert 'id="scan-status-text"' in markup
        assert markup.index('id="scan-summary"') < markup.index('id="scan-status-text"')
        assert 'window.confirm("Cancel the running scan?")' not in app_javascript
        assert 'id="settings-open"' in markup
        assert 'aria-label="open settings"' in markup
        assert 'id="settings-view"' in markup
        assert 'aria-label="applicant profile"' in markup
        assert 'id="settings-profile-options"' in markup
        assert 'id="settings-profile-extract"' not in markup
        assert "Changes save automatically." in markup
        assert "Prepared cover letters refresh after 30 seconds" in markup
        assert "never submits an application or marks a role applied" in markup
        assert '<button type="submit">save settings</button>' not in markup
        assert "input[data-setting-text]" in app_javascript
        assert 'const response = await fetch("/api/config", {' in app_javascript
        assert "body: JSON.stringify(payload)" in app_javascript
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
        # Material indexing is server-owned and automatic after source changes; no
        # manual index action is exposed in the dashboard.
        assert 'id="material-index-button"' not in markup
        assert 'id="material-index-warning"' in markup
        assert 'id="material-index-status"' in markup
        assert 'id="materials-required-warning"' in markup
        assert 'aria-label="missing required application materials"' in markup
        assert 'id="toolbar-summary"' in markup
        assert 'id="scan-failures-open" hidden>view scan failures</button>' in markup
        assert 'id="scan-failures-dialog"' in markup
        assert 'id="scan-failures-list"' in markup
        assert 'id="scan-failures-close"' in markup
        assert 'id="scan-errors"' not in markup
        assert 'id="status-tabs"' not in markup
        assert 'class="status-tabs"' not in markup
        assert "/assets/app.css?v=vanilla-20260904-23" in index_markup
        assert "/assets/app.js?v=vanilla-20260904-23" in index_markup
        assert '.status-pane[data-bucket="applied"]' in app_styles
        assert "--bucket: var(--purple);" in app_styles
        assert '.status-pane[data-bucket="closed"]' in app_styles
        assert "--bucket: #4b3d78;" in app_styles
        assert "résumé" not in markup
        assert "résumé" not in app_javascript
        assert "grid-template-columns: minmax(0, 1fr);" in app_styles
        assert "width: auto;" in app_styles
        assert 'class="prep-role-hero"' in app_javascript
        assert 'class="prep-workspace-nav"' in app_javascript
        assert 'data-prep-section-target="prep-resume-' in app_javascript
        assert 'class="prep-document-workspace"' in app_javascript
        assert 'class="prepped-document status-${escapeHtml(status)}"' in app_javascript
        assert 'class="prepped-filename-link"' in app_javascript
        assert 'data-autoprep-view="${documentKind}"' in app_javascript
        assert ">View PDF</a>" not in app_javascript
        assert "Preview PDF" not in app_javascript
        assert "data-autoprep-preview" not in app_javascript
        assert 'id="regenerate-all-resumes"' in markup
        assert 'id="regenerate-all-cover-letters"' in markup
        assert 'id="prepped-bulk-status"' not in markup
        assert "No cover letters were queued." not in app_javascript
        assert "Skipped before queueing:" not in app_javascript
        assert "data-autoprep-disinterested" in app_javascript
        assert 'class="review-action danger prepped-disinterested"' in app_javascript
        assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in app_styles
        assert ".prepped-detail-actions > button:last-child" in app_styles
        assert 'updateRoleStatusById(roleId, "disinterested")' in app_javascript
        assert 'fetch("/api/autoprep/cover-letters/regenerate", {' in app_javascript
        assert 'idempotency_key: autoprepActionKey("regenerate-all-cover-letters")' in (
            app_javascript
        )
        assert "movingToDisinterested || autoprepJobIsActive(job)" in app_javascript
        assert 'const commentsLabel = "Optional comments for the next version";' in (
            app_javascript
        )
        assert "autoprepJobHasGenerationFailure(job)" in app_javascript
        assert "autoprepCoverLetterIsGenerating(job)" in app_javascript
        assert "autoprepJobIsGenerating(job)" in app_javascript
        assert '" is-document-generating"' in app_javascript
        assert (
            "const documentGenerating = !hasGenerationFailure && autoprepJobIsGenerating(job);"
        ) in app_javascript
        assert ".prepped-list-item.is-document-generating" in app_styles
        assert "@keyframes prepped-cover-letter-pulse" in app_styles
        assert "autoprepJobIsQueued(job)" in app_javascript
        assert '" is-generation-queued"' in app_javascript
        assert ".prepped-list-item.is-generation-queued" in app_styles
        assert "@keyframes prepped-queue-breathe" in app_styles
        assert "prefers-reduced-motion: reduce" in app_styles
        assert "openPreppedDetailSections" in app_javascript
        assert 'data-prepped-detail-section="description"' in app_javascript
        assert 'preppedDetail.addEventListener("toggle"' in app_javascript
        failed_list_item_class = (
            'class="prepped-list-item${generationQueued ? " is-generation-queued" : ""}'
            '${documentGenerating ? " is-document-generating" : ""}'
            '${hasGenerationFailure ? " has-generation-failure" : ""}${activeClass}"'
        )
        assert failed_list_item_class in app_javascript
        assert ".prepped-list-item.has-generation-failure" in app_styles
        assert "data-autoprep-retry" not in app_javascript
        assert "async function retryAutoprepDocument" not in app_javascript
        assert 'const retryingFailedDocument = ["failed", "interrupted"].includes(status);' in (
            app_javascript
        )
        assert 'retryingFailedDocument ? "retry" : "regenerate"' in app_javascript
        empty_resume_guard = (
            'if (!comments && documentKind !== "cover-letter" && !retryingFailedDocument)'
        )
        assert empty_resume_guard not in app_javascript
        bulk_function = app_javascript[
            app_javascript.index(
                "async function regenerateAllPreppedCoverLetters()"
            ) : app_javascript.index("async function markPreppedRoleDisinterested")
        ]
        assert "await refreshPreppedRoles();\n    startPreppedPolling();" in bulk_function
        assert ".prep-role-hero" in app_styles
        assert ".prep-document-workspace" in app_styles
        assert ".prepped-document.has-open-preview" not in app_styles
        assert ".prepped-pdf-preview" not in app_styles
        assert "grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);" in app_styles
        assert "height: clamp(640px, 78vh, 900px);" not in app_styles
        assert 'fetch("/api/central/resolve-companies", { method: "POST" })' in app_javascript
        assert "loadInitialTrackerData().finally(scheduleCentralCompanySync);" in app_javascript
        assert "}, 10_000);" in app_javascript
        assert "await companySync;" not in app_javascript
        assert "syncCompaniesOnPageLoad().catch(() => {});" in app_javascript
        assert 'id="role-information-view"' in markup
        assert 'id="role-information-card"' in markup
        assert 'id="close-role-information"' in markup
        assert 'data-view-role-info="${job.id}"' in app_javascript
        assert "function openRoleInformation(roleId)" in app_javascript
        assert "function closeRoleInformation()" in app_javascript
        assert 'event.key === "Escape" && !roleInformationView.hidden' in app_javascript
        assert "Number(status.count) - status.jobs.length" in app_javascript
        assert '... and ${hiddenCount} more' in app_javascript
        assert "settingsProfileOptions.innerHTML" in app_javascript
        assert 'setting.input_type ?? "text"' in app_javascript
        assert 'setting.autocomplete ?? "name"' in app_javascript
        assert 'aria-label="disinterested role actions"' in app_javascript
        assert 'data-autoprep-role-id="${job.id}"' in app_javascript
        assert 'data-autoprep-role-id="${job.id}">prep</button>' in app_javascript
        assert "data-prep-role-id" not in app_javascript
        assert "view / regenerate prep" not in app_javascript
        assert "already prepped" not in app_javascript
        assert "prep-started-dot" not in app_javascript
        assert "prep-started-dot" not in app_styles
        assert "if (trackedRole?.autoprep_started)" in app_javascript
        assert "if (current.autoprep_started)" in app_javascript
        assert "await openExistingPreppedRole(current.id);" in app_javascript
        assert 'async function queueRoleForAutoprep(roleId)' in app_javascript
        assert 'if (queuingAutoprepRoleIds.has(numericRoleId)) return null;' in app_javascript
        assert 'queuingAutoprepRoleIds.add(numericRoleId);' in app_javascript
        assert 'body: JSON.stringify({' in app_javascript
        assert 'role_ids: [numericRoleId]' in app_javascript
        assert "trackedRole.autoprep_started = true;" in app_javascript
        assert 'selectedPreppedRoleId = numericRoleId;' in app_javascript
        assert (
            'await openPreppedView({seedJobs: [...seededJobsByRoleId.values()]});'
            in app_javascript
        )
        assert (
            'const autoprepAction = event.target.closest("[data-autoprep-role-id]");'
            in app_javascript
        )
        assert 'if (action === "autoprep")' in app_javascript
        assert (
            ".prep-actions .review-action {\n"
            "    padding-inline: 6px;\n"
            "    font-size: 0.78rem;\n"
            "    line-height: 1.15;\n"
            "    white-space: normal;\n"
            "  }"
            in app_styles
        )
        assert 'src="${escapeHtml(pdfUrl)}"' in app_javascript
        assert "data:application/pdf;base64" not in app_javascript
        assert "scanFailuresOpenButton.hidden = failures.length === 0;" in app_javascript
        assert 'scanFailuresOpenButton.addEventListener("click", openScanFailuresDialog);' in (
            app_javascript
        )
        assert 'scanFailuresCloseButton.addEventListener("click", closeScanFailuresDialog);' in (
            app_javascript
        )
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_effective_role_company_name_prefers_explicit_job_description_identity() -> None:
    role = {
        "company_name": "Ramp",
        "role_url": "https://jobs.ashbyhq.com/cohere/example",
        "description": (
            "Who are we?\n"
            "Cohere is the leading security-first enterprise AI company. "
            "We build foundation models and end-to-end products."
        ),
    }

    assert web_server._effective_role_company_name(role) == "Cohere"
    assert web_server._role_with_effective_company(role)["company_name"] == "Cohere"
    assert (
        web_server._effective_role_company_name(
            {
                "company_name": "Ramp",
                "description": "About Cohere\nCohere is an enterprise AI company.",
            }
        )
        == "Cohere"
    )


def test_role_generation_context_prefers_explicit_posting_title_and_location() -> None:
    role = {
        "company_name": "SAP",
        "title": (
            "Vancouver SAP iXp Intern HANA and Analytics%2C Agile Developer "
            "Vancouver Brit V6B 1A9"
        ),
        "location": None,
        "description": (
            "Position Title: SAP iXp Intern\n"
            "HANA and Analytics, Agile Developer\n"
            "Location: Vancouver, BC (Hybrid; 3 days in-office per week)\n"
            "Anticipated Start Date: 4 January 2027\n"
        ),
    }

    resolved = web_server._role_with_effective_company(role)

    assert resolved["title"] == "SAP iXp Intern HANA and Analytics, Agile Developer"
    assert resolved["location"] == "Vancouver, BC (Hybrid; 3 days in-office per week)"


def test_role_generation_context_does_not_absorb_posting_prose_into_title() -> None:
    role = {
        "company_name": "Example",
        "title": "Fallback title",
        "description": (
            "Position Title: Engineer\n"
            "This arbitrary PDF continuation fragment is unrelated prose\n"
            "Another arbitrary fragment\n"
            "Location: Toronto"
        ),
    }

    resolved = web_server._role_with_effective_company(role)

    assert resolved["title"] == "Engineer"


def test_role_generation_context_stops_at_inline_posting_field() -> None:
    role = {
        "company_name": "Example",
        "title": "Fallback title",
        "description": "Position Title: Engineer Responsibilities: Build APIs\nLocation: Toronto",
    }

    resolved = web_server._role_with_effective_company(role)

    assert resolved["title"] == "Engineer"


def test_effective_role_company_name_does_not_use_incidental_company_mentions() -> None:
    role = {
        "company_name": "Ramp",
        "description": (
            "About Engineering\n"
            "Engineering is central to this team.\n"
            "Ramp works with Cohere and other AI vendors to serve finance teams."
        ),
    }

    assert web_server._effective_role_company_name(role) == "Ramp"


def test_autoprep_pdf_filename_uses_job_description_company_identity(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_pdf = tmp_path / "source.pdf"
    source_pdf.write_bytes(_valid_pdf_bytes())
    monkeypatch.setattr(web_server, "user_data_path", lambda *_args, **_kwargs: tmp_path)

    directory, target = web_server._copy_autoprep_pdf(
        {
            "id": 312,
            "company_name": "Ramp",
            "title": "Machine Learning Intern Co-op",
            "description": (
                "Who are we?\nCohere is the leading security-first enterprise AI company."
            ),
        },
        source_pdf,
        kind="cover-letter",
    )

    assert directory.name == "cohere-machine-learning-intern-co-op-role-312"
    assert target.name == "cohere-machine-learning-intern-co-op-cover-letter.pdf"

    old_resume = tmp_path / "ramp-role-312-resume.pdf"
    old_resume.write_bytes(_valid_pdf_bytes())
    counterpart = web_server._copy_autoprep_counterpart(
        {
            "id": 312,
            "company_name": "Ramp",
            "title": "Machine Learning Intern Co-op",
            "description": (
                "Who are we?\nCohere is the leading security-first enterprise AI company."
            ),
        },
        {"resume_status": "ready", "resume_artifact_path": str(old_resume)},
        directory,
        generated_kind="cover-letter",
    )
    assert counterpart == (
        "resume",
        str(directory / "cohere-machine-learning-intern-co-op-resume.pdf"),
    )

    resume_directory, resume_target = web_server._copy_autoprep_pdf(
        {
            "id": 312,
            "company_name": "Ramp",
            "title": "Machine Learning Intern Co-op",
            "description": (
                "Who are we?\nCohere is the leading security-first enterprise AI company."
            ),
        },
        source_pdf,
        kind="resume",
    )

    assert resume_directory == directory
    assert resume_target.name == "cohere-machine-learning-intern-co-op-resume.pdf"


def test_autoprep_regeneration_reuses_persisted_role_directory(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_pdf = tmp_path / "new-resume.pdf"
    source_pdf.write_bytes(_valid_pdf_bytes())
    root = tmp_path / "prepared-applications"
    original_directory = root / "sap-original-title-role-378"
    original_directory.mkdir(parents=True)
    original_resume = original_directory / "sap-original-title-resume.pdf"
    original_resume.write_bytes(_valid_pdf_bytes())
    monkeypatch.setattr(web_server, "user_data_path", lambda *_args, **_kwargs: tmp_path)

    directory, target = web_server._copy_autoprep_pdf(
        {
            "id": 378,
            "company_name": "SAP",
            "title": "Resolved title changed during regeneration",
        },
        source_pdf,
        kind="resume",
        existing_job={
            "artifact_directory": str(original_directory),
            "resume_artifact_path": str(original_resume),
        },
    )

    assert directory == original_directory
    assert target == original_resume
    assert sorted(path.name for path in original_directory.iterdir()) == [original_resume.name]
    assert not (root / "sap-resolved-title-changed-during-regeneration-role-378").exists()


def test_autoprep_atomic_pdf_copy_preserves_previous_file_when_replacement_is_invalid(
    tmp_path: Path,
) -> None:
    target = tmp_path / "role-resume.pdf"
    original = _valid_pdf_bytes()
    target.write_bytes(original)
    invalid = tmp_path / "invalid.pdf"
    invalid.write_bytes(b"not a pdf")

    with pytest.raises(RuntimeError, match="could not be verified"):
        web_server._atomic_copy_verified_pdf(invalid, target)

    assert target.read_bytes() == original


def test_autoprep_regeneration_preserves_unrelated_user_files(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(web_server, "user_data_path", lambda *_args, **_kwargs: tmp_path)
    directory = tmp_path / "prepared-applications" / "sap-engineer-role-378"
    directory.mkdir(parents=True)
    resume = directory / "sap-engineer-resume.pdf"
    user_pdf = directory / "personal-resume.pdf"
    notes = directory / "notes.txt"
    resume.write_bytes(_valid_pdf_bytes())
    user_pdf.write_bytes(_valid_pdf_bytes())
    notes.write_text("user-authored notes")
    source = tmp_path / "replacement.pdf"
    source.write_bytes(_valid_pdf_bytes())

    web_server._copy_autoprep_pdf(
        {"id": 378, "company_name": "SAP", "title": "Engineer"},
        source,
        kind="resume",
        existing_job={
            "artifact_directory": str(directory),
            "resume_artifact_path": str(resume),
        },
    )

    assert sorted(path.name for path in directory.iterdir()) == [
        "notes.txt",
        "personal-resume.pdf",
        "sap-engineer-resume.pdf",
    ]
    assert user_pdf.is_file()
    assert notes.read_text() == "user-authored notes"


def test_currently_applying_directory_exchange_is_atomic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    (first / "old.txt").write_text("old")
    (second / "new.txt").write_text("new")

    web_server._exchange_directories_atomically(first, second)

    assert sorted(path.name for path in first.iterdir()) == ["new.txt"]
    assert sorted(path.name for path in second.iterdir()) == ["old.txt"]


def test_currently_applying_folder_atomically_projects_selected_role_pair(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(web_server, "user_data_path", lambda *_args, **_kwargs: tmp_path)
    role_directory = tmp_path / "prepared-applications" / "acme-engineer-role-42"
    role_directory.mkdir(parents=True)
    resume = role_directory / "acme-engineer-resume.pdf"
    cover_letter = role_directory / "acme-engineer-cover-letter.pdf"
    resume.write_bytes(_valid_pdf_bytes())
    cover_letter.write_bytes(_valid_pdf_bytes())
    job = {
        "role_id": 42,
        "resume_status": "ready",
        "cover_letter_status": "ready",
        "resume_artifact_path": str(resume),
        "cover_letter_artifact_path": str(cover_letter),
        "artifact_directory": str(role_directory),
    }

    result = web_server._sync_currently_applying_folder(job)
    current = tmp_path / "prepared-applications" / "currently-applying"

    assert result["role_id"] == 42
    assert Path(str(result["path"])) == current
    assert sorted(path.name for path in current.iterdir()) == [
        "acme-engineer-cover-letter.pdf",
        "acme-engineer-resume.pdf",
    ]
    assert resume.is_file()
    assert cover_letter.is_file()

    previous_files = {path.name: path.read_bytes() for path in current.iterdir()}
    backup = current.with_name(".currently-applying-previous")
    current.replace(backup)
    cover_letter.unlink()
    with pytest.raises(FileNotFoundError):
        web_server._sync_currently_applying_folder(job)
    assert {path.name: path.read_bytes() for path in current.iterdir()} == previous_files
    assert not backup.exists()


def test_currently_applying_role_selection_and_open_folder_api(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    database = tmp_path / "currently-applying.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "user_data_path", lambda *_args, **_kwargs: tmp_path)
    db.ensure_initialized()
    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Engineer",
                role_url="https://example.com/engineer",
                role_status=RoleStatus.INTERESTED,
            ),
        )
        assert role.id is not None
        autoprep_service.ensure_autoprep_schema(connection)
        [job] = autoprep_service.enqueue_autoprep_jobs(
            connection,
            [role.id],
            idempotency_key="currently-applying-role",
        )
        role_directory = tmp_path / "prepared-applications" / f"acme-engineer-role-{role.id}"
        role_directory.mkdir(parents=True)
        resume = role_directory / "acme-engineer-resume.pdf"
        cover_letter = role_directory / "acme-engineer-cover-letter.pdf"
        resume.write_bytes(_valid_pdf_bytes())
        cover_letter.write_bytes(_valid_pdf_bytes())
        autoprep_service.mark_autoprep_document(
            connection,
            int(job["id"]),
            "resume",
            "ready",
            artifact_path=str(resume),
            artifact_directory=str(role_directory),
        )
        autoprep_service.mark_autoprep_document(
            connection,
            int(job["id"]),
            "cover_letter",
            "ready",
            artifact_path=str(cover_letter),
            artifact_directory=str(role_directory),
        )
        autoprep_service.finish_autoprep_worker(connection, int(job["id"]))

    open_calls: list[list[str]] = []

    def fake_open(arguments: list[str], **_kwargs: object) -> SimpleNamespace:
        open_calls.append(arguments)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(web_server.subprocess, "run", fake_open)
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        select = Request(
            f"{base_url}/api/autoprep/roles/{role.id}/currently-applying",
            data=b"",
            method="POST",
        )
        with urlopen(select, timeout=5) as response:
            selected = json.loads(response.read().decode())
        assert selected["updated"] is True
        current = tmp_path / "prepared-applications" / "currently-applying"
        assert sorted(path.name for path in current.iterdir()) == [
            "acme-engineer-cover-letter.pdf",
            "acme-engineer-resume.pdf",
        ]

        open_request = Request(
            f"{base_url}/api/autoprep/currently-applying/open",
            data=b"",
            method="POST",
        )
        with urlopen(open_request, timeout=5) as response:
            opened = json.loads(response.read().decode())
        assert opened == {"opened": True, "path": str(current.resolve())}
        assert open_calls == [["open", str(current.resolve())]]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_ai_role_experience_retrieval_requests_concrete_ai_project_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, str] = {}

    def fake_retrieve(
        _sources: list[dict[str, object]],
        *,
        query: str,
        total_content_limit: int,
    ) -> list[dict[str, object]]:
        captured["query"] = query
        return [{"filename": "ai-project.md", "content": "source-grounded AI project"}]

    monkeypatch.setattr(web_server, "retrieve_indexed_materials", fake_retrieve)

    note = ExperienceNote(
        id=1,
        filename="projects.md",
        content=(
            "## 3. Independently Directed AI-Assisted Projects\n\n"
            "Used Hermes Agent responsibly while building Nourish, an AI-enabled application."
        ),
        content_sha256="abc123",
        updated_at=None,
    )
    result = web_server._generation_experience_context(
        [note],
        role={
            "title": "Software Engineer, AI Platform - Intern",
            "company_name": "Nuro",
            "description": "Build machine learning infrastructure.",
        },
        tweaks=None,
    )

    assert result[0]["filename"] == "ai-project.md"
    assert result[1]["filename"] == "projects.md — AI project evidence"
    assert "Nourish" in str(result[1]["content"])
    assert "Hermes Agent" in str(result[1]["content"])
    assert "independently directed AI-assisted projects" in captured["query"]
    assert "Hermes AI application product architecture testing outcome" in captured["query"]


def test_tracker_json_uses_gzip_when_client_accepts_it(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CALLUMPLOYED_DATABASE_PATH",
        str(tmp_path / "tracker-gzip.sqlite3"),
    )
    db.ensure_initialized()
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/tracker",
            headers={"Accept-Encoding": "gzip"},
        )
        with urlopen(request, timeout=5) as response:
            compressed = response.read()
            assert response.status == 200
            assert response.headers["Content-Encoding"] == "gzip"
            assert response.headers["Vary"] == "Accept-Encoding"
            assert int(response.headers["Content-Length"]) == len(compressed)

        payload = json.loads(gzip.decompress(compressed))
        assert "stats" in payload
        assert "statuses" in payload
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
        candidate_id = int(
            connection.execute(
                "SELECT id FROM scan_candidates WHERE discovery_method = 'heuristic+agent'"
            ).fetchone()["id"]
        )
        add_role_discovery_attempt(
            connection,
            RoleDiscoveryAttempt(
                scan_run_id=scan_run.id,
                scan_candidate_id=candidate_id,
                company_id=company.id,
                url="https://example.com/jobs/accepted",
                assessment_is_role=True,
                assessment_confidence=0.92,
                assessment_extraction_method="llm",
            ),
        )
        finish_scan_run(connection, scan_run.id, ScanStatus.SUCCEEDED)
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
    assert overview["agent-assisted scan runs"] == 1
    assert sections["scan runs"]["succeeded"] == 1
    assert sections["scan runs"]["candidate observations"] == 2
    assert sections["candidate links"]["stored candidates"] == 2
    assert sections["ai usage"]["agent-selected links"] == 1
    assert sections["ai usage"]["llm role assessments"] == 1
    assert sections["ai usage"]["agent-assisted scan runs"] == 1
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
        captured["settings"] = kwargs.get("settings")

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
        web_server.set_config_value(connection, "llm_provider", "codex")

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
    assert isinstance(captured["settings"], web_server.LlmSettings)
    assert captured["settings"].provider == "codex"
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
    monkeypatch.setenv(
        "CALLUMPLOYED_MATERIAL_INDEX_ROOT",
        str(tmp_path / "application-material-index"),
    )
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")
    compile_attempts = 0

    def fake_run(command: object, **kwargs: object) -> object:
        nonlocal compile_attempts
        compile_attempts += 1
        cwd = Path(kwargs["cwd"])
        (cwd / "cover-letter.pdf").write_bytes(
            _positioned_text_pdf_bytes((740, 670, 600, 530))
        )

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)

    captured_calls: list[dict[str, object]] = []

    async def fake_generate_cover_letter(**kwargs: object) -> object:
        captured_calls.append(dict(kwargs))

        class Draft:
            latex = (
                "\\documentclass{letter}\\begin{document}\n"
                "Dear Acme,\n\nBody.\n\nSincerely,\\\\\nJake Yeo\n"
                "\\end{document}"
            )
            summary = "generated from examples"
            example_ids = [1]

        search_tool = kwargs["search_tool"]
        search_tool("Python backend", limit=1)
        return Draft()

    monkeypatch.setattr(web_server, "generate_cover_letter", fake_generate_cover_letter)
    monkeypatch.setattr(web_server, "_cover_letter_body_word_count", lambda _latex: 250)
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
        note = add_experience_note(
            connection,
            filename="projects.md",
            content=(
                "# Projects\n"
                "## Backend Telemetry\n"
                "Built a Python backend for secure sensor ingestion on AWS.\n"
                "## Community Campaign\n"
                "Organized a neighborhood arts event and social campaign."
            ),
        )
        web_server.set_config_value(connection, "applicant_first_name", "Jake")
        web_server.set_config_value(connection, "applicant_last_name", "Yeo")
        web_server.set_config_value(connection, "applicant_email", "jake@example.com")
        web_server.set_config_value(connection, "applicant_institution", "University of Victoria")
        web_server.set_config_value(connection, "applicant_degree", "Software Engineering")
        web_server.set_config_value(connection, "llm_provider", "codex")
        web_server.set_config_value(connection, "cover_letter_model", "gpt-5.6-terra")
        web_server.build_material_index([web_server._experience_note_index_source(note)])
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
                        "\\documentclass{letter}\\begin{document}Previous Acme draft\\end{document}"
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
        assert cover_letter["summary"] == (
            "Drafted cover letter for Backend Intern at Acme using resume, "
            "job description, and 1 stored cover letter example."
        )
        assert cover_letter["path"] == str(resume_root / "role-1" / "cover-letter.tex")
        assert cover_letter["pdf_path"] == str(resume_root / "role-1" / "cover-letter.pdf")
        assert cover_letter["pdf_base64"]
        assert base64.b64decode(cover_letter["pdf_base64"]) == _positioned_text_pdf_bytes(
            (740, 670, 600, 530)
        )
        assert compile_attempts == 1
        assert len(captured_calls) == 1
        assert cover_letter["tweaks"] == "Make it warmer and shorten the Amazon paragraph."
        assert captured_calls[0]["tweaks"] == "Make it warmer and shorten the Amazon paragraph."
        assert captured_calls[0]["previous_cover_letter_latex"] == (
            "\\documentclass{letter}\\begin{document}Previous Acme draft\\end{document}"
        )

        indexed_context = captured_calls[0]["other_experience_context"]
        assert isinstance(indexed_context, list)
        assert len(indexed_context) == 1
        indexed_page = indexed_context[0]
        assert isinstance(indexed_page, dict)
        assert indexed_page["title"] == "Backend Telemetry"
        assert str(indexed_page["filename"]).startswith("sections/")
        assert "Python backend for secure sensor ingestion" in str(indexed_page["content"])
        assert "neighborhood arts event" not in str(indexed_page["content"])
        applicant_profile = captured_calls[0]["applicant_profile"]
        assert isinstance(applicant_profile, ApplicantProfile)
        assert applicant_profile.model_dump() == {
            "first_name": "Jake",
            "last_name": "Yeo",
            "email": "jake@example.com",
            "phone": "",
            "institution": "University of Victoria",
            "degree": "Software Engineering",
        }
        settings = captured_calls[0]["settings"]
        assert isinstance(settings, web_server.LlmSettings)
        assert settings.provider == "codex"
        assert settings.model == "gpt-5.6-terra"
        assert settings.codex_model == "gpt-5.6-terra"
        saved_latex = (resume_root / "role-1" / "cover-letter.tex").read_text()
        assert "Dear Hiring Manager" in saved_latex
        assert "Dear Acme" not in saved_latex
        assert "\\setlength{\\parskip}{0.55em}" in saved_latex
        assert "\\setlength{\\parindent}{1.5em}" in saved_latex
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
        (cwd / "cover-letter.pdf").write_bytes(_valid_pdf_bytes())

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
    with db.connect() as connection:
        connection.execute(
            "UPDATE roles SET description = ? WHERE id = 1",
            ("Hiring Manager: Jane Doe\nApply by Friday.",),
        )
        connection.commit()

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
                        "Dear Hiring Manager,\n\n"
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
        assert "Dear Jane Doe" in cover_letter["latex"]
        assert "Dear Hiring Manager" not in cover_letter["latex"]
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
        assert path.name == "selected.tex"
        generated_pdf = path.with_suffix(".pdf")
        generated_pdf.write_bytes(b"fresh pdf")
        return generated_pdf, base64.b64encode(b"fresh pdf").decode()

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
        disposition = response.headers["Content-Disposition"]
        assert disposition.startswith("inline;")
        assert 'filename="CallumMackenzie-acme-backend-intern-cover-letter.pdf"' in disposition
        assert body == b"%PDF saved cover letter"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_role_material_pdf_filename_includes_safe_job_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        web_server,
        "_applicant_pdf_filename_prefix",
        lambda: "CallumMackenzie",
    )

    filename = web_server._role_material_pdf_filename(
        {
            "id": 7,
            "company_name": "München / R&D",
            "title": "ML Engineer — Safety/Trust",
        },
        kind="cover_letter",
    )

    assert filename == ("CallumMackenzie-munchen-r-d-ml-engineer-safety-trust-cover-letter.pdf")


def test_cover_letter_latex_normalizer_adds_compact_one_page_layout() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass{letter}\n\\begin{document}\nHello\n\\end{document}"
    )

    assert "\\documentclass{letter}" in normalized
    assert "\\usepackage[margin=1in]{geometry}" in normalized
    assert "\\setlength{\\parskip}{0.55em}" in normalized
    assert "\\setlength{\\parindent}{1.5em}" in normalized
    assert "\\linespread{0.97}" not in normalized
    assert "\\pagestyle{empty}" in normalized
    assert "\\hyphenpenalty=10000" in normalized
    assert "\\exhyphenpenalty=10000" in normalized
    assert "\\setlength{\\emergencystretch}{2em}" in normalized
    assert normalized.index("\\setlength{\\parskip}") < normalized.index("\\begin{document}")


def test_cover_letter_latex_normalizer_adds_role_title_to_recipient_header() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{article}\n"
        "\\begin{document}\n"
        "\\noindent Apple\\\\\n"
        "Remote\\\\\n"
        "August 29, 2026\\par\n"
        "\\vspace{1.1em}\n"
        "\\noindent Dear Hiring Manager,\\par\n"
        "Body.\n"
        "\\end{document}",
        role_title="Software Engineering Intern",
    )

    recipient_header = normalized[
        normalized.index("\\noindent Apple") : normalized.index("Dear Hiring Manager")
    ]
    assert "Remote\\\\\nSoftware Engineering Intern\\\\\nAugust 29, 2026" in recipient_header
    assert normalized.count("Software Engineering Intern") == 1


def test_cover_letter_latex_normalizer_does_not_mistake_sender_degree_for_role_title() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[letterpaper,11pt]{article}\n"
        "\\begin{document}\n"
        "\\noindent Jane Doe\\\\\n"
        "Software Engineer\\\\\n"
        "jane@example.com\\par\n"
        "\\vspace{1em}\n"
        "\\noindent Acme\\\\\n"
        "Remote\\\\\n"
        "August 29, 2026\\par\n"
        "\\vspace{1em}\n"
        "\\noindent Dear Hiring Manager,\\par\n"
        "Body.\n"
        "\\end{document}",
        role_title="Software Engineer",
    )

    recipient_header = normalized[
        normalized.index("\\noindent Acme") : normalized.index("Dear Hiring Manager")
    ]
    assert "Remote\\\\\nSoftware Engineer\\\\\nAugust 29, 2026" in recipient_header


def test_cover_letter_latex_normalizer_separates_and_professionalizes_salutation() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{article}\n"
        "\\begin{document}\n"
        "Dear Hiring Team, I am applying for the role.\n\n"
        "Second paragraph.\n\n"
        "Sincerely,\\\\[12pt]\nJake Yeo\n"
        "\\end{document}"
    )

    assert "Dear Hiring Team" not in normalized
    assert (
        "\\noindent Dear Hiring Manager,\\par\n\\vspace{0.35em}\n\nI am applying for the role."
    ) in normalized


def test_cover_letter_latex_normalizer_replaces_punctuationless_salutation() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{article}\n"
        "\\begin{document}\n"
        "Dear Acme\n\n"
        "I am applying for the role.\n"
        "\\end{document}"
    )

    assert "Dear Acme" not in normalized
    assert "\\noindent Dear Hiring Manager,\\par" in normalized
    assert "I am applying for the role." in normalized


def test_cover_letter_latex_normalizer_deduplicates_salutation_spacing() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{article}\n"
        "\\begin{document}\n"
        "\\noindent Dear Hiring Manager,\\par\n"
        "\\vspace{0.35em}\n\n"
        "First paragraph.\n"
        "\\end{document}"
    )

    assert normalized.count("\\vspace{0.35em}") == 1


def test_cover_letter_latex_normalizer_uses_explicit_hiring_contact() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{article}\n"
        "\\begin{document}\n"
        "Dear Hiring Manager, I am applying for the role.\n"
        "\\end{document}",
        hiring_contact="Jane Doe",
    )

    assert "\\noindent Dear Jane Doe,\\par" in normalized
    assert "Dear Hiring Manager" not in normalized


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


def test_cover_letter_latex_normalizer_preserves_configured_signature() -> None:
    normalized = web_server._normalize_cover_letter_latex(
        "\\documentclass[11pt]{letter}\n"
        "\\signature{Jake Yeo}\n"
        "\\begin{document}\n"
        "\\begin{letter}{Hiring Team}\n"
        "Hello\n"
        "\\end{letter}\n"
        "\\end{document}"
    )

    assert "\\signature{Jake Yeo}" in normalized
    assert "Callum Mackenzie" not in normalized


def test_fallback_cover_letter_uses_profile_and_experience_notes() -> None:
    latex = web_server._fallback_cover_letter_latex(
        {
            "title": "Backend Kubernetes Intern",
            "company_name": "Acme",
            "description": "Build Kubernetes infrastructure",
        },
        web_server.MasterResume(
            filename="resume.tex",
            content="Python backend experience",
            content_sha256="abc",
        ),
        applicant_profile=ApplicantProfile(
            first_name="Jake",
            last_name="Yeo",
            email="jake@example.com",
            institution="University of Victoria",
            degree="Software Engineering",
        ),
        other_experience_context=[
            {
                "filename": "projects.md",
                "content": "Built and operated a Kubernetes scheduler.",
                "updated_at": "2026-08-27T00:00:00Z",
            }
        ],
    )

    assert "Jake Yeo" in latex
    assert "jake@example.com" in latex
    assert "University of Victoria" in latex
    assert "Software Engineering" in latex
    assert "kubernetes" in latex.lower()
    assert "Callum Mackenzie" not in latex


def test_fallback_cover_letter_excludes_material_index_metadata() -> None:
    latex = web_server._fallback_cover_letter_latex(
        {
            "title": "API Platform Intern",
            "company_name": "SAP",
            "location": "Vancouver, BC",
            "description": "Build and test reliable API services",
        },
        web_server.MasterResume(
            filename="resume.tex",
            content=r"\resumeItem{Built arbitrary resume fragment without terminal punctuation}",
            content_sha256="abc",
        ),
        applicant_profile=ApplicantProfile(first_name="Jake", last_name="Yeo"),
        other_experience_context=[
            {
                "filename": "project.md",
                "content": (
                    "# Indexed project\n\n"
                    "- Tools: Git\n"
                    "- Useful attributes: architecture, automation, data, product.\n\n"
                    "## Index summary\n\n"
                    "Tools: Git. Useful attributes: architecture and automation. "
                    "Evidence: Repository-verified.\n\n"
                    "## Source details\n\n"
                    "details, teamwork, testing, infrastructure, and outcomes so that shorter "
                    "application materials can be derived.\n\n"
                    "cloud infrastructure, authentication, document generation, stakeholder "
                    "collaboration, technical documentation.\n\n"
                    "Built arbitrary PDF continuation fragment without terminal punctuation\n\n"
                    "Built and tested a production API used by a mobile application.\n\n"
                    "I strengthened its API validation and authentication behavior.\n\n"
                    "Designed and shipped a reliable deployment workflow!"
                ),
            }
        ],
    )

    assert "I built and tested a production API" in latex
    assert "SAP\\\\\nVancouver, BC\\\\\nAPI Platform Intern" in latex
    assert "I strengthened its API validation" in latex
    assert "I i strengthened" not in latex
    assert "details, teamwork" not in latex
    assert "cloud infrastructure, authentication" not in latex
    assert "built arbitrary pdf continuation" not in latex.lower()
    assert "built arbitrary resume fragment" not in latex.lower()
    assert "I designed and shipped a reliable deployment workflow." in latex
    assert "workflow!." not in latex
    assert "Tools:" not in latex
    assert "Useful attributes:" not in latex
    assert "Repository-verified:" not in latex
    assert "User-confirmed:" not in latex
    assert "I tools" not in latex
    assert "I useful attributes" not in latex


def test_cover_letter_quality_rejects_internal_evidence_metadata() -> None:
    malformed = (
        "\\documentclass{article}\n\\begin{document}\n"
        "Dear Hiring Manager,\\par\n"
        "Evidence: I built and tested the API.\n"
        "Sincerely,\\\\\nJake Yeo\n\\end{document}\n"
    )

    with pytest.raises(web_server.GeneratedDocumentQualityError):
        web_server._validate_cover_letter_quality(malformed)


def test_cover_letter_quality_rejects_latex_formatted_metadata_label() -> None:
    malformed = r"\textbf{Evidence}: I built and tested the API."

    with pytest.raises(web_server.GeneratedDocumentQualityError):
        web_server._validate_cover_letter_quality(malformed)


def test_cover_letter_quality_allows_user_edited_evidence_label() -> None:
    edited = "Evidence: this wording was intentionally added by the user."

    web_server._validate_cover_letter_quality_for_source(
        edited,
        source="edited_cover_letter",
    )


def test_role_title_from_url_decodes_percent_encoded_punctuation() -> None:
    role_url = (
        "https://jobs.sap.com/job/Vancouver-SAP-iXp-Intern-HANA-and-"
        "Analytics%2C-Agile-Developer-Vancouver-Brit-V6B-1A9/1432658533"
    )

    assert web_server._role_title_from_url(role_url) == (
        "Vancouver SAP iXp Intern HANA and Analytics, Agile Developer Vancouver Brit V6B 1A9"
    )


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
    assert "\\setlength{\\parskip}{0.55em}" in normalized
    assert "\\setlength{\\parindent}{1.5em}" in normalized
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
        (cwd / "resume.pdf").write_bytes(_valid_pdf_bytes())

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
        assert base64.b64decode(resume["pdf_base64"]) == _valid_pdf_bytes()
        assert (resume_root / "role-1" / "resume.tex").exists()

        request = Request(
            f"http://127.0.0.1:{port}/api/roles/1/resume/save",
            data=json.dumps(
                {
                    "latex": (
                        "\\documentclass{article}\\begin{document}Edited role resume\\end{document}"
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
        assert (
            'filename="CallumMackenzie-acme-backend-intern-resume.pdf"'
            in response.headers["Content-Disposition"]
        )
        assert body == _valid_pdf_bytes()
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
    monkeypatch.setenv(
        "CALLUMPLOYED_MATERIAL_INDEX_ROOT",
        str(tmp_path / "application-material-index"),
    )
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")
    compile_attempts = 0

    def fake_run(command: object, **kwargs: object) -> object:
        nonlocal compile_attempts
        compile_attempts += 1
        cwd = Path(kwargs["cwd"])
        (cwd / "resume.pdf").write_bytes(_valid_pdf_bytes(2 if compile_attempts <= 3 else 1))

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    captured_calls: list[dict[str, object]] = []

    async def fake_generate_resume_tweak(**kwargs: object) -> object:
        captured_calls.append(dict(kwargs))

        class Draft:
            latex = (
                "\\documentclass{article}\n\\begin{document}\nMaster resume\n"
                "Python distributed systems\n\\end{document}"
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
            VALUES (
                1,
                'resume.tex',
                '\\documentclass{article}
\\begin{document}
Master resume
\\end{document}',
                'abc'
            )
            """
        )
        note = add_experience_note(
            connection,
            filename="projects.md",
            content=(
                "# Projects\n"
                "## Distributed Scheduler\n"
                "Built a Kubernetes scheduler for Python distributed systems.\n"
                "## Art Portfolio\n"
                "Curated a watercolor gallery."
            ),
        )
        web_server.set_config_value(connection, "llm_provider", "codex")
        connection.commit()
        web_server.build_material_index([web_server._experience_note_index_source(note)])
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
        assert base64.b64decode(resume["pdf_base64"]) == _valid_pdf_bytes()
        assert compile_attempts == 4
        assert len(captured_calls) == 1
        assert captured_calls[0]["resume_content"] == "Current editor latex"
        assert captured_calls[0]["tweaks"] == "Emphasize distributed systems."
        settings = captured_calls[0]["settings"]
        assert isinstance(settings, web_server.LlmSettings)
        assert settings.provider == "codex"

        indexed_context = captured_calls[0]["other_experience_context"]
        assert isinstance(indexed_context, list)
        assert len(indexed_context) == 1
        indexed_page = indexed_context[0]
        assert isinstance(indexed_page, dict)
        assert indexed_page["title"] == "Distributed Scheduler"
        assert "Kubernetes scheduler for Python distributed systems" in str(indexed_page["content"])
        assert "watercolor gallery" not in str(indexed_page["content"])
        assert (resume_root / "role-1" / "resume.tex").read_text() == resume["latex"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_save_role_resume_rejects_materially_underfilled_one_page_pdf(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")

    def fake_run(command: object, **kwargs: object) -> object:
        cwd_arg = kwargs["cwd"]
        assert isinstance(cwd_arg, (str, Path))
        cwd = Path(cwd_arg)
        (cwd / "resume.pdf").write_bytes(_valid_pdf_bytes())

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    monkeypatch.setattr(web_server, "_pdf_page_fill_ratio", lambda _path: 0.61)
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content="source",
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )

    with pytest.raises(web_server.GeneratedDocumentLayoutError, match="underfilled"):
        web_server.save_role_resume(
            {"id": 1, "company_name": "Acme", "title": "Product Intern"},
            resume,
            r"\documentclass{article}\begin{document}Complete experience\end{document}",
            required_page_count=1,
            minimum_page_fill_ratio=0.82,
        )


def test_pdf_page_fill_ratio_uses_real_positioned_text_and_fails_closed(
    tmp_path: Path,
) -> None:
    filled = tmp_path / "filled.pdf"
    underfilled = tmp_path / "underfilled.pdf"
    transformed = tmp_path / "transformed.pdf"
    blank = tmp_path / "blank.pdf"
    filled.write_bytes(_positioned_text_pdf_bytes((740, 600, 450, 300, 150, 60)))
    underfilled.write_bytes(_positioned_text_pdf_bytes((740, 650, 560, 500)))
    transformed.write_bytes(
        _positioned_text_pdf_bytes(
            (740, 600, 450, 300, 150, 60),
            transform="1 0 0 0.5 0 0",
        )
    )
    blank.write_bytes(_blank_pdf_bytes())

    assert web_server._pdf_page_fill_ratio(filled) > 0.82
    assert web_server._pdf_page_fill_ratio(underfilled) < 0.40
    assert 0.40 < web_server._pdf_page_fill_ratio(transformed) < 0.50
    assert web_server._pdf_page_fill_ratio(blank) is None


def test_source_resume_fidelity_preserves_entries_while_allowing_bullet_rewrites() -> None:
    source = r"""\documentclass{article}
\begin{document}
\section{Work}
Email: owner@example.com
\resumeProjectHeading{\textbf{Employer \{Platform\}}}{2026}
\resumeItem{Built nested \textbf{systems} at 70\% scale.}
\resumeItem{Published \href{https://example.com/proof}{project proof}.}
\section{Technical Skills}
\item{Python, TypeScript}
\end{document}
"""
    rewritten = source.replace(
        "Built nested \\textbf{systems} at 70\\% scale.",
        "Improved source-supported systems at documented scale.",
    ).replace("Python, TypeScript", "TypeScript, Python")
    rewritten = rewritten.replace("project proof", "supporting evidence")
    assert web_server._missing_source_resume_entries(source, rewritten) == []
    for candidate in (
        source.replace("\\section{Technical Skills}\n", ""),
        source.replace(
            "\\resumeProjectHeading{\\textbf{Employer \\{Platform\\}}}{2026}\n",
            "",
        ),
        source.replace("2026", "2025"),
        source.replace("https://example.com/proof", "https://example.com/other"),
    ):
        assert web_server._missing_source_resume_entries(source, candidate)


def test_cover_letter_body_word_count_handles_professional_layout_commands() -> None:
    latex = (
        "\\documentclass{article}\n\\begin{document}\n"
        "\\noindent Dear Hiring Manager,\\par\n"
        "\\vspace{0.35em}\n\n"
        "First body paragraph has five words.\n\n"
        "\\noindent Sincerely,\\\\[12pt]\nJake Yeo\n"
        "\\end{document}\n"
    )

    assert web_server._cover_letter_body_word_count(latex) == 6


def test_cover_letter_body_word_count_handles_letter_class_commands() -> None:
    latex = (
        "\\documentclass{letter}\n\\begin{document}\n"
        "\\opening{Dear Hiring Manager,}\n"
        "First body paragraph has five words.\n\n"
        "\\closing{Sincerely,}\n"
        "\\end{document}\n"
    )

    assert web_server._cover_letter_body_word_count(latex) == 6


def test_write_role_cover_letter_rejects_only_excessive_body_length(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body_words = 301
    latex = (
        "\\documentclass{article}\n\\begin{document}\n"
        "Jake Yeo\\\\\njake@example.com\n\n"
        "August 28, 2026\n\n"
        "Acme Inc.\\\\\nVancouver, BC\n\n"
        "Dear Hiring Team, "
        + " ".join(["grounded"] * body_words)
        + "\n\nSincerely,\\\\\nJake Yeo\n\\end{document}\n"
    )
    assert web_server._cover_letter_body_word_count(latex) == body_words
    with pytest.raises(web_server.GeneratedDocumentLengthError):
        web_server._write_role_cover_letter(
            {"id": 1, "company_name": "Acme", "title": "Product Intern"},
            latex,
            source="ai_cover_letter",
            example_ids=[],
            tweaks=None,
            required_page_count=1,
            minimum_page_fill_ratio=None,
            minimum_body_word_count=None,
            maximum_body_word_count=300,
        )


def test_write_role_cover_letter_accepts_concise_one_page_body(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: tmp_path)
    body_words = 145
    latex = (
        "\\documentclass{article}\n\\begin{document}\n"
        "\\noindent Dear Hiring Manager,\\par\n\n"
        + " ".join(["grounded"] * body_words)
        + "\n\n\\noindent Sincerely,\\\\\nCallum Mackenzie\n\\end{document}\n"
    )
    assert web_server._cover_letter_body_word_count(latex) == body_words
    def create_pdf(path: Path) -> tuple[Path, str]:
        pdf_path = path.with_suffix(".pdf")
        pdf_path.write_bytes(_valid_pdf_bytes())
        return pdf_path, base64.b64encode(_valid_pdf_bytes()).decode()

    monkeypatch.setattr(web_server, "_generate_cover_letter_pdf_preview", create_pdf)
    result = web_server._write_role_cover_letter(
        {"id": 1, "company_name": "Acme", "title": "Product Intern"},
        latex,
        source="ai_cover_letter",
        example_ids=[],
        tweaks=None,
        required_page_count=1,
        minimum_page_fill_ratio=None,
        minimum_body_word_count=None,
        maximum_body_word_count=300,
    )

    assert result["source"] == "ai_cover_letter"
    assert result["pdf_path"].endswith("cover-letter.pdf")


def test_save_role_resume_rejects_unmeasurable_fill_and_rolls_back_pair(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")

    def fake_run(command: object, **kwargs: object) -> object:
        cwd = Path(kwargs["cwd"])
        (cwd / "resume.pdf").write_bytes(_blank_pdf_bytes())
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content="source",
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )
    role = {"id": 1, "company_name": "Acme", "title": "Product Intern"}
    with pytest.raises(web_server.GeneratedDocumentLayoutError, match="could not be measured"):
        web_server.save_role_resume(
            role,
            resume,
            r"\documentclass{article}\begin{document}Complete\end{document}",
            required_page_count=1,
            minimum_page_fill_ratio=0.82,
        )

    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True, exist_ok=True)
    target_tex = role_dir / "resume.tex"
    target_pdf = role_dir / "resume.pdf"
    target_tex.write_text("previous tex")
    target_pdf.write_bytes(b"previous pdf")
    monkeypatch.setattr(web_server, "_pdf_page_fill_ratio", lambda _path: 0.90)
    real_replace = os.replace

    def fail_pdf_commit(source: object, destination: object) -> None:
        if Path(source).name == "selected.pdf" and Path(destination) == target_pdf:
            raise OSError("injected PDF commit failure")
        real_replace(source, destination)

    monkeypatch.setattr(web_server.os, "replace", fail_pdf_commit)
    with pytest.raises(OSError, match="injected PDF commit failure"):
        web_server.save_role_resume(
            role,
            resume,
            r"\documentclass{article}\begin{document}Replacement\end{document}",
            required_page_count=1,
            minimum_page_fill_ratio=0.82,
        )
    assert target_tex.read_text() == "previous tex"
    assert target_pdf.read_bytes() == b"previous pdf"


def test_role_resume_generation_falls_back_to_full_source_when_ai_omits_experience(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-role-resume-fidelity.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")

    def fake_run(command: object, **kwargs: object) -> object:
        cwd_arg = kwargs["cwd"]
        assert isinstance(cwd_arg, (str, Path))
        cwd = Path(cwd_arg)
        (cwd / "resume.pdf").write_bytes(_valid_pdf_bytes())

        class Completed:
            returncode = 0

        return Completed()

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    source_latex = r"""\documentclass{article}
\begin{document}
\section{Work}
\resumeProjectHeading{\textbf{Vital Employer}}{2026}
\resumeItem{Vital production systems experience that must never be removed.}
\section{Projects}
\resumeProjectHeading{\textbf{Vital Project}}{2025}
\resumeItem{Vital project experience that must never be removed.}
\end{document}
"""
    generated_latex = r"""\documentclass{article}
\begin{document}
\section{Work}
\resumeProjectHeading{\textbf{Vital Employer}}{2026}
\resumeItem{Vital production systems experience that must never be removed.}
\end{document}
"""
    calls: list[dict[str, object]] = []

    async def fake_generate_resume_tweak(**kwargs: object) -> object:
        calls.append(dict(kwargs))

        class Draft:
            latex = generated_latex
            summary = "removed less relevant experience"

        return Draft()

    monkeypatch.setattr(web_server, "generate_resume_tweak", fake_generate_resume_tweak)
    db.ensure_initialized()
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content=source_latex,
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )

    result = web_server.build_role_resume(
        {"id": 1, "company_name": "Acme", "title": "Product Intern"},
        resume,
        tweaks="Tailor this resume without removing experience.",
    )

    assert len(calls) == 3
    assert all(call["resume_content"] == source_latex for call in calls)
    assert "Vital production systems experience" in result["latex"]
    assert "Vital project experience" in result["latex"]
    assert (resume_root / "role-1" / "resume.tex").read_text() == source_latex


def test_role_resume_generation_falls_back_when_ai_latex_does_not_compile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-role-resume-compile-fallback.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")
    source_latex = (
        "\\documentclass{article}\n\\begin{document}\n"
        "\\section{Work}\n\\resumeItem{Complete source experience.}\n\\end{document}\n"
    )
    broken_latex = source_latex.replace(
        "\\begin{document}\n",
        "\\begin{document}\n% BROKEN AI LATEX\n",
    )
    compile_attempts = 0

    def fake_run(command: object, **kwargs: object) -> object:
        nonlocal compile_attempts
        compile_attempts += 1
        cwd = Path(kwargs["cwd"])
        if "BROKEN AI LATEX" in (cwd / "resume.tex").read_text():
            return SimpleNamespace(returncode=1)
        (cwd / "resume.pdf").write_bytes(_valid_pdf_bytes())
        return SimpleNamespace(returncode=0)

    async def fake_generate_resume_tweak(**_kwargs: object) -> object:
        return SimpleNamespace(latex=broken_latex, summary="broken")

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    monkeypatch.setattr(web_server, "generate_resume_tweak", fake_generate_resume_tweak)
    db.ensure_initialized()
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content=source_latex,
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )

    result = web_server.build_role_resume(
        {"id": 1, "company_name": "Acme", "title": "Product Intern"},
        resume,
        tweaks="Tailor without removing content.",
    )

    assert compile_attempts == 4
    assert result["latex"] == source_latex
    assert (resume_root / "role-1" / "resume.tex").read_text() == source_latex


def test_save_role_resume_emergency_profile_fits_bounded_overflow(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")
    compile_attempts = 0

    def fake_run(command: object, **kwargs: object) -> object:
        nonlocal compile_attempts
        compile_attempts += 1
        cwd_arg = kwargs["cwd"]
        assert isinstance(cwd_arg, (str, Path))
        cwd = Path(cwd_arg)
        candidate = (cwd / "resume.tex").read_text()
        page_count = 1 if "% callumployed emergency one-page fit" in candidate else 2
        (cwd / "resume.pdf").write_bytes(_valid_pdf_bytes(page_count))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    source_latex = (
        "\\documentclass[letterpaper,11pt]{article}\n"
        "\\begin{document}\n"
        "\\section{Work}\n"
        "\\resumeProjectHeading{\\textbf{Complete Employer}}{2026}\n"
        "\\resumeItem{Complete source experience.}\n"
        "\\end{document}\n"
    )
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content=source_latex,
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )

    result = web_server.save_role_resume(
        {"id": 1, "company_name": "Acme", "title": "Product Intern"},
        resume,
        source_latex,
        required_page_count=1,
    )

    assert compile_attempts <= 6
    assert "% callumployed emergency one-page fit" in result["latex"]
    assert "Complete Employer" in result["latex"]
    assert len(PdfReader(result["pdf_path"]).pages) == 1


def test_role_resume_generation_returns_source_artifact_when_provider_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-role-resume-provider-fallback.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: tmp_path / "resources")
    monkeypatch.setattr(web_server.shutil, "which", lambda _name: "/usr/bin/pdflatex")

    async def unavailable_provider(**_kwargs: object) -> object:
        raise RuntimeError("provider unavailable")

    def fake_run(command: object, **kwargs: object) -> object:
        cwd_arg = kwargs["cwd"]
        assert isinstance(cwd_arg, (str, Path))
        cwd = Path(cwd_arg)
        (cwd / "resume.pdf").write_bytes(_valid_pdf_bytes())
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(web_server, "generate_resume_tweak", unavailable_provider)
    monkeypatch.setattr(web_server.subprocess, "run", fake_run)
    db.ensure_initialized()
    source_latex = (
        "\\documentclass{article}\n\\begin{document}\n"
        "\\section{Work}\nComplete source experience.\n\\end{document}\n"
    )
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content=source_latex,
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )

    result = web_server.build_role_resume(
        {"id": 1, "company_name": "Acme", "title": "Product Intern"},
        resume,
        tweaks="Tailor this resume.",
    )

    assert result["latex"] == source_latex
    assert result["source"] == "source_resume_fallback"
    assert len(PdfReader(result["pdf_path"]).pages) == 1


def test_cover_letter_generation_returns_concise_local_artifact_when_provider_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-provider-fallback.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)

    async def unavailable_provider(**_kwargs: object) -> object:
        raise RuntimeError("provider unavailable")

    def create_pdf(path: Path) -> tuple[Path, str]:
        pdf_path = path.with_suffix(".pdf")
        pdf = _valid_pdf_bytes()
        pdf_path.write_bytes(pdf)
        return pdf_path, base64.b64encode(pdf).decode()

    monkeypatch.setattr(web_server, "generate_cover_letter", unavailable_provider)
    monkeypatch.setattr(web_server, "_generate_cover_letter_pdf_preview", create_pdf)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    with db.connect() as connection:
        connection.execute(
            "UPDATE roles SET description = 'Python backend internship' WHERE id = 1"
        )
        connection.commit()
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content="Python backend and distributed systems experience.",
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )

    result = web_server.build_role_cover_letter(
        {"id": 1, "company_name": "Acme", "title": "Backend Intern"},
        resume,
        allow_local_fallback=True,
        required_page_count=1,
    )

    assert result["source"] == "local_cover_letter_fallback"
    assert web_server._cover_letter_body_word_count(result["latex"]) <= 300
    assert len(PdfReader(result["pdf_path"]).pages) == 1


def test_cover_letter_overflow_uses_bounded_attempts_then_local_artifact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-overflow-fallback.sqlite3"
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    generation_calls = 0

    async def overflowing_provider(**_kwargs: object) -> object:
        nonlocal generation_calls
        generation_calls += 1
        return SimpleNamespace(
            latex=(
                "\\documentclass{article}\n\\begin{document}\n"
                "\\noindent Dear Hiring Manager,\\par\n\n"
                + " ".join(["grounded"] * 301)
                + "\n\n\\noindent Sincerely,\\\\\nCallum Mackenzie\n"
                "\\end{document}\n"
            ),
            summary="too long",
            example_ids=[],
        )

    def create_pdf(path: Path) -> tuple[Path, str]:
        pdf_path = path.with_suffix(".pdf")
        pdf = _valid_pdf_bytes()
        pdf_path.write_bytes(pdf)
        return pdf_path, base64.b64encode(pdf).decode()

    monkeypatch.setattr(web_server, "generate_cover_letter", overflowing_provider)
    monkeypatch.setattr(web_server, "_generate_cover_letter_pdf_preview", create_pdf)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content="Python backend and distributed systems experience.",
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )

    result = web_server.build_role_cover_letter(
        {"id": 1, "company_name": "Acme", "title": "Backend Intern"},
        resume,
        required_page_count=1,
    )

    assert generation_calls == 3
    assert result["source"] == "local_cover_letter_fallback"
    assert web_server._cover_letter_body_word_count(result["latex"]) <= 300
    assert len(PdfReader(result["pdf_path"]).pages) == 1


@pytest.mark.parametrize(
    ("failure_mode", "expected_generation_calls"),
    [("compile", 3), ("repair_provider", 2)],
)
def test_cover_letter_repair_failures_publish_local_fallback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_mode: str,
    expected_generation_calls: int,
) -> None:
    database = tmp_path / f"tracker-cover-letter-{failure_mode}.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    generation_calls = 0

    async def provider(**_kwargs: object) -> object:
        nonlocal generation_calls
        generation_calls += 1
        if failure_mode == "repair_provider" and generation_calls == 2:
            raise RuntimeError("provider failed during repair")
        return SimpleNamespace(
            latex="\\documentclass{article}\\begin{document}Draft\\end{document}",
            summary="draft",
            example_ids=[],
        )

    def write_document(
        role: dict[str, object],
        latex: str,
        *,
        source: str,
        **_kwargs: object,
    ) -> dict[str, object]:
        if source == "local_cover_letter_fallback":
            return {
                "role_id": role["id"],
                "source": source,
                "latex": latex,
                "pdf_path": str(tmp_path / "fallback.pdf"),
            }
        if failure_mode == "compile":
            raise RuntimeError("LaTeX failed to compile the cover letter")
        raise web_server.GeneratedDocumentLengthError(301, 0, 300)

    monkeypatch.setattr(web_server, "generate_cover_letter", provider)
    monkeypatch.setattr(web_server, "_write_role_cover_letter", write_document)
    env = {"CALLUMPLOYED_DATABASE_PATH": str(database)}
    runner.invoke(app, ["companies", "add", "Acme", "https://example.com"], env=env)
    runner.invoke(
        app,
        ["roles", "add", "1", "Backend Intern", "https://example.com/jobs/backend"],
        env=env,
    )
    resume = web_server.MasterResume(
        id=1,
        filename="resume.tex",
        content="Python backend experience.",
        content_sha256="source",
        created_at=None,
        updated_at=None,
    )

    result = web_server.build_role_cover_letter(
        {"id": 1, "company_name": "Acme", "title": "Backend Intern"},
        resume,
    )

    assert generation_calls == expected_generation_calls
    assert result["source"] == "local_cover_letter_fallback"



def test_cover_letter_publication_rolls_back_tex_and_pdf_together(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    role = {"id": 1, "company_name": "Acme", "title": "Backend Intern"}
    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True)
    target_tex = role_dir / "cover-letter.tex"
    target_pdf = role_dir / "cover-letter.pdf"
    target_tex.write_text("old cover letter")
    target_pdf.write_bytes(b"old cover pdf")

    def create_pdf(path: Path) -> tuple[Path, str]:
        pdf_path = path.with_suffix(".pdf")
        pdf = _valid_pdf_bytes()
        pdf_path.write_bytes(pdf)
        return pdf_path, base64.b64encode(pdf).decode()

    monkeypatch.setattr(web_server, "_generate_cover_letter_pdf_preview", create_pdf)
    real_replace = os.replace
    failed_install = False

    def fail_pdf_install(source: object, destination: object) -> None:
        nonlocal failed_install
        source_path = Path(str(source))
        destination_path = Path(str(destination))
        if not failed_install and destination_path == target_pdf:
            failed_install = True
            raise OSError("injected cover PDF commit failure")
        real_replace(source_path, destination_path)

    monkeypatch.setattr(web_server.os, "replace", fail_pdf_install)
    latex = (
        "\\documentclass{article}\\begin{document}"
        "Dear Hiring Manager, new letter. Sincerely, Callum"
        "\\end{document}"
    )

    with pytest.raises(OSError, match="injected cover PDF commit failure"):
        web_server._write_role_cover_letter(
            role,
            latex,
            source="ai_cover_letter",
            example_ids=[],
            tweaks=None,
            required_page_count=1,
            maximum_body_word_count=300,
        )

    assert target_tex.read_text() == "old cover letter"
    assert target_pdf.read_bytes() == b"old cover pdf"


def test_cover_letter_fallback_retains_prior_verified_pair(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True)
    (role_dir / "cover-letter.tex").write_text("prior verified letter")
    (role_dir / "cover-letter.pdf").write_bytes(_valid_pdf_bytes())

    def failed_publish(*_args: object, **_kwargs: object) -> dict[str, object]:
        raise OSError("disk unavailable")

    monkeypatch.setattr(web_server, "_write_role_cover_letter", failed_publish)
    result = web_server._publish_reliable_cover_letter_fallback(
        {"id": 1, "company_name": "Acme", "title": "Backend Intern"},
        web_server.MasterResume(
            filename="resume.tex",
            content="Python backend experience.",
            content_sha256="source",
        ),
        applicant_profile=ApplicantProfile(first_name="Callum", last_name="Mackenzie"),
        experience_context=[],
        tweaks="Keep it concise.",
        required_page_count=1,
    )

    assert result["source"] == "existing_cover_letter_fallback"
    assert result["latex"] == "prior verified letter"
    assert base64.b64decode(result["pdf_base64"]) == _valid_pdf_bytes()

    os.utime(role_dir / "cover-letter.pdf", (1, 1))
    with pytest.raises(OSError, match="disk unavailable"):
        web_server._publish_reliable_cover_letter_fallback(
            {"id": 1, "company_name": "Acme", "title": "Backend Intern"},
            web_server.MasterResume(
                filename="resume.tex",
                content="Python backend experience.",
                content_sha256="source",
            ),
            applicant_profile=ApplicantProfile(first_name="Callum", last_name="Mackenzie"),
            experience_context=[],
            tweaks="Keep it concise.",
            required_page_count=1,
        )


def test_resume_fallback_rejects_stale_prior_pdf(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resume_root = tmp_path / "prepared-resumes"
    monkeypatch.setattr(web_server, "_prepared_resumes_root", lambda: resume_root)
    role_dir = resume_root / "role-1"
    role_dir.mkdir(parents=True)
    resume_path = role_dir / "resume.tex"
    pdf_path = role_dir / "resume.pdf"
    pdf_path.write_bytes(_valid_pdf_bytes())
    os.utime(pdf_path, (1, 1))
    resume_path.write_text("newer resume source")

    def failed_source_publish(*_args: object, **_kwargs: object) -> dict[str, object]:
        raise RuntimeError("source publication failed")

    monkeypatch.setattr(web_server, "save_role_resume", failed_source_publish)
    resume = web_server.MasterResume(
        filename="resume.tex",
        content="complete source resume",
        content_sha256="source",
    )

    with pytest.raises(RuntimeError, match="source publication failed"):
        web_server._source_resume_fallback(
            {"id": 1, "company_name": "Acme", "title": "Backend Intern"},
            resume,
            required_page_count=1,
            tweaks="Tailor truthfully.",
            summary="fallback",
        )


def test_local_cover_letter_fallback_uses_concrete_resume_and_role_evidence() -> None:
    assert "2027" not in web_server._prep_keywords("Software Engineer Intern Winter 2027")
    resume = web_server.MasterResume(
        filename="resume.tex",
        content=(
            "\\documentclass{article}\n"
            "\\begin{document}\n"
            "\\resumeProjectHeading{\\textbf{University of British Columbia}}"
            "{Graduation Date: 2027}\n"
            "\\resumeItem{Built AWS Lambda and Docker pipelines that generated large PDF and "
            "DOCX documents for hundreds of researchers.}\n"
            "\\resumeItem{Implemented OIDC authentication, PostgreSQL features, and GraphQL "
            "workflows.}\n"
            "\\resumeProjectHeading{\\textbf{PullUp}}{2026}\n"
            "\\resumeItem{Strengthened a 34-route Express API with input validation and secure "
            "HTTP-only session cookies.}\n"
            "\\resumeItem{Built automated Python and PyTest coverage to catch API regressions.}\n"
            "\\end{document}\n"
        ),
        content_sha256="source",
    )
    role = {
        "id": 1,
        "company_name": "Cohere",
        "title": "Software Engineer Intern (Winter 2027)",
        "description": (
            "Build features for the API platform, robust data pipelines, scalable services and "
            "infrastructure, security features, developer tooling, and reliable production code."
        ),
    }

    latex = web_server._fallback_cover_letter_latex(
        role,
        resume,
        applicant_profile=ApplicantProfile(first_name="Jake", last_name="Yeo"),
    )
    normalized = web_server._normalize_cover_letter_latex(
        latex,
        role_title=role["title"],
    )
    body_words = web_server._cover_letter_body_word_count(normalized)

    assert 140 <= body_words <= 300
    assert "My background aligns especially around" not in normalized
    assert "around 2027" not in normalized
    assert "AWS Lambda" in normalized
    assert "Docker" in normalized
    assert "34-route Express API" in normalized
    assert "API platform" in normalized
    assert "scalable services" in normalized
    assert "role's focus aligns" not in normalized


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
        web_server.set_config_value(connection, "llm_provider", "codex")
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
                {"messages": [{"role": "user", "content": "What should I emphasize?"}]}
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
        assert isinstance(captured["settings"], web_server.LlmSettings)
        assert captured["settings"].provider == "codex"
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
        {"id": 1, "title": "Backend Intern", "company_name": "Acme"},
        web_server.MasterResume(
            filename="resume.tex",
            content="\\documentclass{article}\\begin{document}hi\\end{document}",
            content_sha256="abc",
        ),
    )

    assert pdf_path == downloads / "CallumMackenzie-acme-backend-intern-resume.pdf"
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


@pytest.mark.parametrize(
    "model",
    ["gpt-5.6-terra", "gpt-5.6-luna", "gpt-5.6-sol", "gpt-4.1-mini"],
)
def test_cover_letter_model_accepts_only_dropdown_options(model: str) -> None:
    assert web_server._clean_cover_letter_model(model) == model

    with pytest.raises(ValueError, match="supported cover letter model"):
        web_server._clean_cover_letter_model("other-model")


@pytest.mark.parametrize("provider", ["openai", "codex"])
def test_llm_provider_accepts_only_settings_options(provider: str) -> None:
    assert web_server._clean_llm_provider(provider) == provider

    with pytest.raises(ValueError, match="llm_provider must be one of"):
        web_server._clean_llm_provider("hermes")


def test_application_generation_uses_configured_provider_and_document_model(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "provider-config.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setenv("CALLUMPLOYED_LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

    with web_server.db.connect() as connection:
        web_server.db.run_migrations(connection)
        defaults = web_server._llm_settings_for_generation(
            connection,
            model="gpt-4.1-mini",
        )
        web_server.set_config_value(connection, "llm_provider", "codex")
        selected = web_server._llm_settings_for_generation(
            connection,
            model="gpt-5.6-terra",
        )

    assert defaults.provider == "openai"
    assert defaults.model == "gpt-4.1-mini"
    assert defaults.openai_api_key is not None
    assert selected.provider == "codex"
    assert selected.model == "gpt-5.6-terra"
    assert selected.codex_model == "gpt-5.6-terra"
    assert selected.openai_api_key is not None


def test_saved_application_answers_use_configured_llm_provider(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "application-answer-provider.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Engineer",
                role_url="https://example.com/engineer",
                role_status=RoleStatus.INTERESTED,
                description="Build reliable software.",
            ),
        )
        assert role.id is not None
        web_server.upsert_master_resume(
            connection,
            filename="resume.tex",
            content=r"\documentclass{article}\begin{document}Resume\end{document}",
        )
        web_server.set_config_value(connection, "llm_provider", "codex")

    observed_providers: list[str] = []

    async def fake_generate_role_chat(**kwargs: object) -> SimpleNamespace:
        settings = kwargs["settings"]
        assert isinstance(settings, web_server.LlmSettings)
        observed_providers.append(str(settings.provider))
        return SimpleNamespace(answer="I use grounded AI tooling.")

    monkeypatch.setattr(web_server, "generate_role_chat", fake_generate_role_chat)
    monkeypatch.setattr(web_server, "sync_role_context_vectors", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(web_server, "retrieve_role_context", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(web_server, "_saved_role_cover_letter", lambda _role_id: None)

    result = web_server.generate_saved_application_answer(
        role.id,
        question="What AI technologies are you comfortable with?",
    )

    assert observed_providers == ["codex"]
    assert result["answer"] == "I use grounded AI tooling."


def test_profile_extraction_fills_only_blank_settings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "profile-extraction.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    captured: dict[str, object] = {}

    async def fake_extract_applicant_profile(**kwargs: object) -> SimpleNamespace:
        captured.update(kwargs)
        return SimpleNamespace(
            model_dump=lambda: {
                "first_name": "Extracted",
                "last_name": "Mackenzie-Smith",
                "email": "callum@example.com",
                "phone": "+1 (250) 555-0123",
                "institution": "University of Victoria",
                "degree": "BEng Software Engineering",
            }
        )

    monkeypatch.setattr(
        web_server,
        "extract_applicant_profile",
        fake_extract_applicant_profile,
    )
    with web_server.db.connect() as connection:
        web_server.db.run_migrations(connection)
        web_server.upsert_master_resume(
            connection,
            filename="resume.tex",
            content=r"\documentclass{article}\begin{document}Resume\end{document}",
        )
        web_server.set_config_value(connection, "applicant_first_name", "Callum")
        web_server.set_config_value(connection, "llm_provider", "codex")

    populated = web_server._populate_missing_applicant_profile_from_resume()

    assert populated["applicant_last_name"] == "Mackenzie-Smith"
    assert isinstance(captured["settings"], web_server.LlmSettings)
    assert captured["settings"].provider == "codex"
    with web_server.db.connect() as connection:
        assert web_server.get_config_value(connection, "applicant_first_name") == "Callum"
        assert web_server.get_config_value(connection, "applicant_last_name") == "Mackenzie-Smith"
        assert web_server.get_config_value(connection, "applicant_email") == "callum@example.com"
        assert (
            web_server.get_config_value(
                connection,
                web_server.APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY,
            )
            is not None
        )


def test_profile_extraction_skips_llm_when_profile_is_complete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "complete-profile.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))

    async def unexpected_extract(**_kwargs: object) -> None:
        raise AssertionError("extractor should not run")

    monkeypatch.setattr(web_server, "extract_applicant_profile", unexpected_extract)
    with web_server.db.connect() as connection:
        web_server.db.run_migrations(connection)
        web_server.upsert_master_resume(
            connection,
            filename="resume.tex",
            content=r"\documentclass{article}\begin{document}Resume\end{document}",
        )
        for key, value in {
            "applicant_first_name": "Callum",
            "applicant_last_name": "Mackenzie",
            "applicant_email": "callum@example.com",
            "applicant_phone": "+1 250 555 0123",
            "applicant_institution": "University of Victoria",
            "applicant_degree": "BEng Software Engineering",
        }.items():
            web_server.set_config_value(connection, key, value)

    assert web_server._populate_missing_applicant_profile_from_resume() == {}


def test_master_resume_profile_extraction_is_scheduled_in_background(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    started = Event()
    release = Event()

    def fake_populate() -> dict[str, str]:
        started.set()
        release.wait(timeout=2)
        return {}

    monkeypatch.setattr(
        web_server,
        "_populate_missing_applicant_profile_from_resume",
        fake_populate,
    )

    web_server._schedule_master_resume_profile_extraction()

    assert started.wait(timeout=1)
    release.set()


def test_profile_extraction_requires_an_explicit_post(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "explicit-profile-extraction.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    calls = 0

    def fake_populate() -> dict[str, str]:
        nonlocal calls
        calls += 1
        return {"applicant_first_name": "Callum"}

    monkeypatch.setattr(
        web_server,
        "_populate_missing_applicant_profile_from_resume",
        fake_populate,
    )
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        endpoint = f"http://127.0.0.1:{server.server_address[1]}/api/config"
        with urlopen(endpoint, timeout=5) as response:
            assert response.status == 200
        assert calls == 0

        request = Request(f"{endpoint}/extract-profile", data=b"", method="POST")
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read())
        assert calls == 1
        assert payload["populated"] == ["applicant_first_name"]
        assert payload["config"]["settings"]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_config_payload_returns_current_settings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-config.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setenv("CALLUMPLOYED_LLM_PROVIDER", "openai")
    monkeypatch.setattr(web_server, "get_central_passkey", lambda: None)
    with db.connect() as connection:
        db.run_migrations(connection)
        web_server.set_config_value(connection, "application_generation_backend", "hermes")

    defaults = build_config_payload()

    assert defaults["values"] == {}
    assert "application_generation_runtimes" not in defaults
    assert all(
        setting["key"] != "application_generation_backend"
        for setting in defaults["settings"]
    )
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
            "description": "used in generated documents and saved PDF filenames",
            "control": "text",
            "value": "",
            "default": "",
            "editable": True,
        },
        {
            "key": "applicant_last_name",
            "label": "last name",
            "description": "used in generated documents and saved PDF filenames",
            "control": "text",
            "value": "",
            "default": "",
            "editable": True,
        },
        {
            "key": "applicant_email",
            "label": "email",
            "description": "used in the cover letter sender block",
            "control": "text",
            "input_type": "email",
            "autocomplete": "email",
            "value": "",
            "default": "",
            "editable": True,
        },
        {
            "key": "applicant_phone",
            "label": "phone number",
            "description": "shown below the email in the cover letter sender block",
            "control": "text",
            "input_type": "tel",
            "autocomplete": "tel",
            "value": "",
            "default": "",
            "editable": True,
        },
        {
            "key": "applicant_institution",
            "label": "institution",
            "description": "school or university used in cover letters",
            "control": "text",
            "autocomplete": "organization",
            "value": "",
            "default": "",
            "editable": True,
        },
        {
            "key": "applicant_degree",
            "label": "degree / program",
            "description": "education description used in cover letters",
            "control": "text",
            "autocomplete": "off",
            "value": "",
            "default": "",
            "editable": True,
        },
        {
            "key": "llm_provider",
            "label": "AI provider",
            "description": "used for every AI-backed feature in Callumployed",
            "control": "select",
            "value": "openai",
            "default": "openai",
            "editable": True,
            "options": [
                {"value": "openai", "label": "OpenAI API key"},
                {"value": "codex", "label": "Codex subscription (local CLI)"},
            ],
        },

        {
            "key": "cover_letter_model",
            "label": "cover letter model",
            "description": "model used only for cover letter generation",
            "control": "select",
            "value": "gpt-4.1-mini",
            "default": "gpt-4.1-mini",
            "editable": True,
            "options": [
                {"value": "gpt-5.6-terra", "label": "Terra"},
                {"value": "gpt-5.6-luna", "label": "Luna"},
                {"value": "gpt-5.6-sol", "label": "Sol"},
                {"value": "gpt-4.1-mini", "label": "GPT-4.1 mini"},
            ],
        },
        {
            "key": "autoprep_tailor_resume",
            "label": "tailor resumes",
            "description": (
                "when off, Autoprep copies the master resume and only tailors the cover letter"
            ),
            "control": "toggle",
            "value": True,
            "default": True,
            "editable": True,
        },
        {
            "key": "autoprep_resume_prompt",
            "label": "resume prompt",
            "description": "base instructions used whenever Autoprep tailors a resume",
            "control": "textarea",
            "value": web_server.DEFAULT_AUTOPREP_RESUME_PROMPT,
            "default": web_server.DEFAULT_AUTOPREP_RESUME_PROMPT,
            "editable": True,
        },
        {
            "key": "autoprep_cover_letter_prompt",
            "label": "cover letter prompt",
            "description": (
                "base instructions used for Autoprep cover letters; indexed material is "
                "retrieved separately and supplied to the generator"
            ),
            "control": "textarea",
            "value": web_server.DEFAULT_AUTOPREP_COVER_LETTER_PROMPT,
            "default": web_server.DEFAULT_AUTOPREP_COVER_LETTER_PROMPT,
            "editable": True,
        },
        {
            "key": "scan_headless",
            "label": "headless job scanning",
            "description": "run scan browsers without opening visible browser windows",
            "control": "toggle",
            "value": False,
            "default": False,
            "editable": True,
        },
        {
            "key": "scan_schedule_enabled",
            "label": "daily scan schedule",
            "description": (
                "run one full scan each day at the configured local time; missed runs are "
                "not started later"
            ),
            "control": "toggle",
            "value": False,
            "default": False,
            "editable": True,
        },
        {
            "key": "scan_schedule_time",
            "label": "daily scan time",
            "description": "local time for the automatic daily scan",
            "control": "text",
            "input_type": "time",
            "autocomplete": "off",
            "value": "04:30",
            "default": "04:30",
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
                "only applies while scanning; existing roles are unaffected unless re-filtered"
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
    monkeypatch.setenv("CALLUMPLOYED_LLM_PROVIDER", "openai")
    monkeypatch.setattr(web_server, "get_central_passkey", lambda: None)
    scheduled_repreps: list[bool] = []
    monkeypatch.setattr(web_server, "AUTOPREP_COORDINATOR", object())
    monkeypatch.setattr(
        web_server,
        "APPLICANT_PROFILE_REPREP_SCHEDULER",
        SimpleNamespace(schedule=lambda: scheduled_repreps.append(True)),
    )
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
                    "applicant_email": "callum@example.com",
                    "applicant_phone": "+1 (250) 555-0123",
                    "applicant_institution": "University of Victoria",
                    "applicant_degree": "Bachelor of Engineering in Software Engineering",
                    "cover_letter_model": "gpt-5.6-terra",
                    "autoprep_tailor_resume": False,
                    "autoprep_resume_prompt": "Prioritize product leadership evidence.",
                    "autoprep_cover_letter_prompt": "Review every indexed source first.",
                    "llm_provider": "codex",
                    "scan_headless": False,
                    "scan_schedule_enabled": True,
                    "scan_schedule_time": "06:15",
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
            "applicant_degree": "Bachelor of Engineering in Software Engineering",
            "applicant_email": "callum@example.com",
            "applicant_first_name": "Callum",
            "applicant_institution": "University of Victoria",
            "applicant_last_name": "Mackenzie",
            "applicant_phone": "+1 (250) 555-0123",
            "autoprep_tailor_resume": "false",
            "autoprep_resume_prompt": "Prioritize product leadership evidence.",
            "autoprep_cover_letter_prompt": "Review every indexed source first.",
            "cover_letter_model": "gpt-5.6-terra",
            "llm_provider": "codex",
            "include_graduate_degree_roles": "true",
            "internship_mode": "false",
            "location_filter": "north_america",
            "require_software_keywords": "false",
            "scan_headless": "false",
            "scan_schedule_enabled": "true",
            "scan_schedule_time": "06:15",
        }
        setting_values = {setting["key"]: setting["value"] for setting in updated["settings"]}
        assert setting_values == {

            "applicant_degree": "Bachelor of Engineering in Software Engineering",
            "applicant_email": "callum@example.com",
            "applicant_first_name": "Callum",
            "applicant_institution": "University of Victoria",
            "applicant_last_name": "Mackenzie",
            "applicant_phone": "+1 (250) 555-0123",
            "autoprep_tailor_resume": False,
            "autoprep_resume_prompt": "Prioritize product leadership evidence.",
            "autoprep_cover_letter_prompt": "Review every indexed source first.",
            "cover_letter_model": "gpt-5.6-terra",
            "llm_provider": "codex",
            "include_graduate_degree_roles": True,
            "include_hardware_roles": False,
            "require_software_keywords": False,
            "internship_mode": False,
            "location_filter": "north_america",
            "scan_headless": False,
            "scan_schedule_enabled": True,
            "scan_schedule_time": "06:15",
        }
        assert scheduled_repreps == [True]
        assert web_server.APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY not in updated["values"]

        retired_backend_request = Request(
            f"{base_url}/api/config",
            data=json.dumps({"application_generation_backend": "hermes"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(HTTPError) as retired_backend_error:
            urlopen(retired_backend_request, timeout=5)
        assert retired_backend_error.value.code == 400

        with db.connect() as connection:
            durable_reprep_due = get_config_value(
                connection,
                web_server.APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY,
            )
            assert durable_reprep_due is not None
            assert float(durable_reprep_due) > 0
        assert web_server._configured_browser_profile_manager().headless is False
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_config_endpoint_validates_full_payload_before_persisting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-config-atomic.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        initial_request = Request(
            f"{base_url}/api/config",
            data=json.dumps({"cover_letter_model": "gpt-4.1-mini"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(initial_request, timeout=5):
            pass

        invalid_request = Request(
            f"{base_url}/api/config",
            data=json.dumps(
                {
                    "cover_letter_model": "gpt-5.6-sol",
                    "applicant_email": "not-an-email",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(HTTPError) as error:
            urlopen(invalid_request, timeout=5)
        assert error.value.code == 400

        with urlopen(f"{base_url}/api/config", timeout=5) as response:
            config = json.loads(response.read().decode())
        settings = {setting["key"]: setting["value"] for setting in config["settings"]}
        assert settings["cover_letter_model"] == "gpt-4.1-mini"
        assert settings["applicant_email"] == ""
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


def test_central_outage_does_not_break_local_company_or_tracker_endpoints(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-central-outage.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "get_central_passkey", lambda: "configured-passkey")

    class UnavailableCentralClient:
        def __init__(self, **_options: object) -> None:
            pass

        def resolve_company(self, request: object) -> object:
            _ = request
            raise CentralStoreError("central store request failed: connection refused")

        def list_companies(self) -> object:
            raise CentralStoreError("central store request failed: connection refused")

    monkeypatch.setattr(web_server, "CentralStoreClient", UnavailableCentralClient)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        company_request = Request(
            f"{base_url}/api/companies",
            data=json.dumps(
                {
                    "name": "Acme",
                    "career_url": "https://example.com/careers",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(company_request, timeout=5) as response:
            company_payload = json.loads(response.read().decode())

        [company] = company_payload["companies"]
        assert response.status == 200
        assert company["name"] == "Acme"
        assert company["central_sync_status"] == "failed"
        assert "connection refused" in company["central_sync_error"]

        sync_request = Request(
            f"{base_url}/api/central/resolve-companies",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(HTTPError) as sync_error:
            urlopen(sync_request, timeout=5)

        assert sync_error.value.code == 503

        with urlopen(f"{base_url}/api/tracker", timeout=5) as response:
            tracker_payload = json.loads(response.read().decode())

        assert response.status == 200
        assert tracker_payload["stats"]["companies_total"] == 1
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
    monkeypatch.setattr(web_server, "get_central_api_url", lambda connection: None)
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
        for tier in range(8):
            update_request = Request(
                f"http://127.0.0.1:{port}/api/companies/{company_id}",
                data=json.dumps(
                    {
                        "notes": "autosaved note",
                        "prestige_tier": str(tier),
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
            assert company["prestige_tier"] == str(tier)

        invalid_tier_request = Request(
            f"http://127.0.0.1:{port}/api/companies/{company_id}",
            data=json.dumps(
                {
                    "notes": "autosaved note",
                    "prestige_tier": "8",
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
        assert [page["url"] for page in company["career_pages"]] == ["https://example.com/students"]

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
            assert [page.url for page in list_company_career_pages(connection, company_id)] == [
                "https://example.com/students"
            ]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_browser_client_supports_company_tiers_zero_through_seven() -> None:
    static_directory = Path(web_server.__file__).with_name("static")
    app_javascript = (static_directory / "app.js").read_text()
    app_styles = (static_directory / "app.css").read_text()
    index_markup = (static_directory / "index.html").read_text()

    for tier in range(8):
        assert f'value: "{tier}"' in app_javascript
        assert f".company-tier-{tier}" in app_styles
    assert 'value: "8"' not in app_javascript
    assert "0 highest · 7 last resort" in app_javascript
    assert "tiers 5 through 7 progressively prioritize gaining experience" in index_markup


def test_company_create_endpoint_accepts_every_tier_zero_through_seven(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-company-create-tiers.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "get_central_api_url", lambda connection: None)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        for tier in range(8):
            request = Request(
                f"http://127.0.0.1:{port}/api/companies",
                data=json.dumps(
                    {"name": f"Tier {tier} Co", "prestige_tier": str(tier)}
                ).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=5) as response:
                payload = json.loads(response.read().decode())
            created = next(
                company for company in payload["companies"] if company["name"] == f"Tier {tier} Co"
            )
            assert created["prestige_tier"] == str(tier)
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_company_tier_update_is_pushed_to_central(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "web-company-tier-sync.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    db.ensure_initialized()
    with db.connect() as connection:
        company = add_company(
            connection,
            Company(
                name="Acme",
                prestige_tier="2",
                central_company_id="co_acme",
                central_sync_status="linked",
            ),
        )
        assert company.id is not None
        add_company_career_page(
            connection,
            CompanyCareerPage(
                company_id=company.id,
                url="https://example.com/careers",
            ),
        )

    resolved_requests: list[ResolveCompanyRequest] = []

    class FakeCentralStoreClient:
        def __init__(self, **kwargs: object) -> None:
            assert kwargs["api_url"] == "https://central.example"

        def resolve_company(self, request: ResolveCompanyRequest) -> ResolveCompanyResponse:
            resolved_requests.append(request)
            return ResolveCompanyResponse(
                action="matched",
                global_company_id="co_acme",
                confidence=100,
                canonical_domain="example.com",
                normalized_name="acme",
                default_tier="7",
            )

    monkeypatch.setattr(
        web_server,
        "get_central_api_url",
        lambda connection: "https://central.example",
    )
    monkeypatch.setattr(web_server, "get_central_client_id", lambda connection: "client-1")
    monkeypatch.setattr(web_server, "get_central_passkey", lambda: None)
    monkeypatch.setattr(web_server, "CentralStoreClient", FakeCentralStoreClient)

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        request = Request(
            f"http://127.0.0.1:{port}/api/companies/{company.id}",
            data=json.dumps({"notes": "", "prestige_tier": "7"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert payload["companies"][0]["prestige_tier"] == "7"
        assert len(resolved_requests) == 1
        central_request = resolved_requests[0]
        assert central_request.prestige_tier == "7"
        assert central_request.tier_source_id == "client-1"
        assert central_request.career_page_urls == ["https://example.com/careers"]
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

    with db.connect() as connection:
        web_server.set_config_value(connection, "llm_provider", "codex")

    scan_started = Event()
    scan_release = Event()
    observed_providers: list[str] = []

    async def fake_scan_company(*args: object, **kwargs: object) -> None:
        llm_settings = kwargs.get("llm_settings")
        assert isinstance(llm_settings, web_server.LlmSettings)
        observed_providers.append(llm_settings.provider)
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
        assert observed_providers == ["codex"]
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
    assert "description" not in applied["jobs"][0]
    assert applied["jobs"][0]["first_seen_at"] is not None
    assert applied["jobs"][0]["first_seen_at"].endswith("Z")
    assert applied["jobs"][0]["created_at"] is not None
    assert applied["jobs"][0]["created_at"].endswith("Z")
    assert applied["jobs"][0]["updated_at"].endswith("Z")


def test_tracker_payload_sends_archived_count_without_archived_roles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-archived-count.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    with db.connect() as connection:
        db.run_migrations(connection)
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        archived = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Archived Engineer",
                role_url="https://example.com/jobs/archived",
            ),
        )
        assert archived.id is not None
        set_role_status(connection, archived.id, RoleStatus.ARCHIVED, summary="Archived.")

    payload = build_tracker_payload()

    archived_status = next(status for status in payload["statuses"] if status["key"] == "archived")
    assert archived_status["count"] == 1
    assert archived_status["jobs"] == []


def test_tracker_payload_only_sends_recently_disinterested_roles_but_keeps_full_count(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-recent-disinterested.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    with db.connect() as connection:
        db.run_migrations(connection)
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        for title in ("Recently dismissed", "Dismissed earlier"):
            role = add_role(
                connection,
                Role(
                    company_id=company.id,
                    title=title,
                    role_url=f"https://example.com/jobs/{title.lower().replace(' ', '-')}",
                ),
            )
            assert role.id is not None
            set_role_status(
                connection,
                role.id,
                RoleStatus.DISINTERESTED,
                summary="Not interested.",
            )
        connection.execute(
            """
            UPDATE events
            SET created_at = datetime('now', '-3 days')
            WHERE role_id = 2 AND event_type = 'status_changed'
            """
        )
        connection.commit()

    payload = build_tracker_payload()

    disinterested = next(
        status for status in payload["statuses"] if status["key"] == "disinterested"
    )
    assert disinterested["count"] == 2
    assert [job["title"] for job in disinterested["jobs"]] == ["Recently dismissed"]

    search_payload = build_tracker_payload(query="Dismissed earlier")
    search_disinterested = next(
        status for status in search_payload["statuses"] if status["key"] == "disinterested"
    )
    assert search_disinterested["count"] == 1
    assert [job["title"] for job in search_disinterested["jobs"]] == ["Dismissed earlier"]


@pytest.mark.parametrize("limited_status", [RoleStatus.REJECTED, RoleStatus.CLOSED])
def test_tracker_payload_limits_terminal_roles_unless_searching(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    limited_status: RoleStatus,
) -> None:
    status_label = limited_status.value.title()
    database = tmp_path / f"tracker-{limited_status.value}-limit.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    with db.connect() as connection:
        db.run_migrations(connection)
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        for index in range(12):
            role = add_role(
                connection,
                Role(
                    company_id=company.id,
                    title=f"{status_label} Role {index:02d}",
                    role_url=f"https://example.com/jobs/{limited_status.value}-{index:02d}",
                ),
            )
            assert role.id is not None
            set_role_status(
                connection,
                role.id,
                limited_status,
                summary=f"{status_label}.",
            )

    payload = build_tracker_payload()
    limited = next(
        status for status in payload["statuses"] if status["key"] == limited_status.value
    )
    assert limited["count"] == 12
    assert len(limited["jobs"]) == 10
    assert f"{status_label} Role 00" not in {job["title"] for job in limited["jobs"]}

    search_payload = build_tracker_payload(query=f"{status_label} Role 00")
    search_limited = next(
        status for status in search_payload["statuses"] if status["key"] == limited_status.value
    )
    assert search_limited["count"] == 1
    assert [job["title"] for job in search_limited["jobs"]] == [f"{status_label} Role 00"]


@pytest.mark.parametrize(
    "status",
    [RoleStatus.APPLIED, RoleStatus.REJECTED, RoleStatus.CLOSED],
)
def test_tracker_payload_omits_descriptions_for_inactive_application_roles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    status: RoleStatus,
) -> None:
    database = tmp_path / f"tracker-{status.value}-description.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    with db.connect() as connection:
        db.run_migrations(connection)
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Backend Engineer",
                role_url="https://example.com/jobs/backend",
                description="A deliberately large job description.",
                notes="Keep this useful role metadata.",
            ),
        )
        assert role.id is not None
        set_role_status(connection, role.id, status, summary="Status updated.")

    payload = build_tracker_payload()

    status_payload = next(item for item in payload["statuses"] if item["key"] == status.value)
    assert status_payload["jobs"][0]["notes"] == "Keep this useful role metadata."
    assert "description" not in status_payload["jobs"][0]


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

    with db.connect() as connection:
        db.run_migrations(connection)
        autoprep_service.ensure_autoprep_schema(connection)
        autoprep_service.enqueue_autoprep_jobs(
            connection,
            [1],
            idempotency_key="tracker-existing-autoprep",
        )

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
    autoprep_by_title = {
        job["title"]: job["autoprep_started"] for job in interested["jobs"]
    }
    assert autoprep_by_title == {
        "Cover Letter Prep": False,
        "Resume Prep": False,
        "No Prep": True,
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
        assert response_payload["autoprep_job"]["role_id"] == 1
        assert response_payload["autoprep_job"]["worker_state"] == "queued"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    interested = next(status for status in payload["statuses"] if status["key"] == "interested")
    discovered = next(status for status in payload["statuses"] if status["key"] == "discovered")
    assert interested["count"] == 1
    assert discovered["count"] == 0


def test_roles_create_endpoint_creates_unknown_company_without_career_page_and_scans_role(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-role-create-company.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(
        web_server,
        "_try_resolve_company_with_central_store",
        lambda *_args, **_kwargs: None,
    )
    scanned_urls: list[str] = []

    async def fake_run_rescan_role(
        role_id: int,
        *,
        browser_profile_manager: object,
        update_status: bool,
    ) -> dict[str, object]:
        assert browser_profile_manager is not None
        assert update_status is False
        with db.connect() as connection:
            role = get_role(connection, role_id)
            company = get_company(connection, role.company_id)
            assert company.name == "New Company"
            assert list_company_career_pages(connection, company.id or 0) == []
        scanned_urls.append(role.role_url)
        return {
            "role": role.model_copy(
                update={"title": "New Company Platform Intern", "location": "Remote"}
            )
        }

    monkeypatch.setattr(web_server, "run_rescan_role", fake_run_rescan_role)
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        role_url = "https://new-company.example/jobs/platform-intern"
        request = Request(
            f"http://127.0.0.1:{server.server_address[1]}/api/roles",
            data=json.dumps(
                {
                    "company_name": "  New   Company  ",
                    "role_url": role_url,
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert scanned_urls == [role_url]
        assert payload["role"]["title"] == "New Company Platform Intern"
        assert payload["role"]["role_status"] == "interested"
        assert [company["name"] for company in payload["companies"]["companies"]] == [
            "New Company"
        ]
        with db.connect() as connection:
            [company] = list_companies(connection)
            assert company.name == "New Company"
            assert company.id is not None
            assert list_company_career_pages(connection, company.id) == []
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


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
        assert update_status is False
        queued_job = None
        with db.connect() as connection:
            queued_job = connection.execute(
                "SELECT role_id, worker_state FROM autoprep_jobs WHERE role_id = ?",
                (role_id,),
            ).fetchone()
        assert queued_job is not None
        assert int(queued_job["role_id"]) == role_id
        assert str(queued_job["worker_state"]) == "queued"
        return {
            "role": Role(
                id=1,
                company_id=1,
                title="Backend Platform Intern",
                role_url="https://example.com/jobs/backend-platform-intern",
                location="Vancouver",
                role_status=RoleStatus.INTERESTED,
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
        assert payload["role"]["role_status"] == "interested"
        assert payload["scan_error"] is None
        assert payload["autoprep_job"]["role_id"] == 1
        assert payload["autoprep_job"]["worker_state"] == "queued"
        assert payload["tracker"]["stats"]["jobs_total"] == 1
        interested = next(
            status for status in payload["tracker"]["statuses"] if status["key"] == "interested"
        )
        discovered = next(
            status for status in payload["tracker"]["statuses"] if status["key"] == "discovered"
        )
        [role] = interested["jobs"]
        assert discovered["jobs"] == []
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
    extraction_schedules: list[bool] = []
    monkeypatch.setattr(
        web_server,
        "_schedule_master_resume_profile_extraction",
        lambda: extraction_schedules.append(True),
    )
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
        assert created_payload["master_resume"]["content_bytes"] == len(b"\\documentclass{article}")
        assert created_payload["profile_extraction_scheduled"] is True

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
        assert extraction_schedules == [True, True]
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
    monkeypatch.setattr(web_server, "_schedule_master_resume_profile_extraction", lambda: None)
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
            data=json.dumps({"filename": "new.tex", "content": "new master resume"}).encode(),
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


def test_experience_notes_endpoint_extracts_pdf_upload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-experience-pdf.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(
        web_server,
        "_extract_pdf_text",
        lambda _content: "# Employment\n## Platform Engineer\nBuilt Kubernetes tooling.",
    )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}/api/experience-notes"
        request = Request(
            base_url,
            data=json.dumps(
                {
                    "filename": "employment-history.pdf",
                    "content_base64": base64.b64encode(b"pdf content").decode(),
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5):
            pass

        notes = []
        with db.connect() as connection:
            notes = list_experience_notes(connection)
        assert len(notes) == 1
        assert notes[0].filename == "employment-history.pdf"
        assert notes[0].content == ("# Employment\n## Platform Engineer\nBuilt Kubernetes tooling.")
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
    monkeypatch.setattr(web_server, "_schedule_master_resume_profile_extraction", lambda: None)
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


def test_application_material_sources_can_be_previewed_and_removed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "material-management.sqlite3"
    resources = tmp_path / "resume-resources"
    resources.mkdir()
    resource = resources / "portfolio.pdf"
    resource.write_bytes(b"%PDF-resource")
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(web_server, "_resume_resources_root", lambda: resources)
    db.ensure_initialized()
    legacy_pdf_note = None
    with db.connect() as connection:
        example = add_cover_letter_example(
            connection,
            filename="example.txt",
            content="Distinctive cover letter source.",
        )
        note = add_experience_note(
            connection,
            filename="projects.md",
            content="Distinctive employment and project source.",
        )
        legacy_pdf_note = add_experience_note(
            connection,
            filename="legacy-history.pdf",
            content="%PDF-1.4 legacy binary data",
        )
    assert example.id is not None
    assert note.id is not None
    assert legacy_pdf_note is not None
    assert legacy_pdf_note.id is not None

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        with urlopen(f"{base_url}/api/cover-letter-examples/{example.id}", timeout=5) as response:
            assert json.loads(response.read())["content"] == "Distinctive cover letter source."
        with urlopen(f"{base_url}/api/experience-notes/{note.id}", timeout=5) as response:
            assert json.loads(response.read())["content"] == (
                "Distinctive employment and project source."
            )
        with urlopen(
            f"{base_url}/api/experience-notes/{legacy_pdf_note.id}", timeout=5
        ) as response:
            legacy_preview = json.loads(response.read())
        assert legacy_preview["preview_warning"].startswith("This legacy PDF")
        assert legacy_preview["content"] == legacy_preview["preview_warning"]
        with urlopen(f"{base_url}/api/resume-resources/portfolio.pdf", timeout=5) as response:
            assert response.headers["Content-Type"] == "application/pdf"
            assert response.read() == b"%PDF-resource"

        for path in (
            f"cover-letter-examples/{example.id}",
            f"experience-notes/{note.id}",
            f"experience-notes/{legacy_pdf_note.id}",
            "resume-resources/portfolio.pdf",
        ):
            request = Request(f"{base_url}/api/{path}", method="DELETE")
            with urlopen(request, timeout=5) as response:
                assert response.status == 200

        with db.connect() as connection:
            assert list_cover_letter_examples(connection) == []
            assert list_experience_notes(connection) == []
        assert not resource.exists()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_application_material_index_endpoint_tracks_upload_freshness(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-material-index.sqlite3"
    index_root = tmp_path / "application-material-index"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setenv("CALLUMPLOYED_MATERIAL_INDEX_ROOT", str(index_root))
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
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        note_request = Request(
            f"{base_url}/api/experience-notes",
            data=json.dumps(
                {
                    "filename": "history.md",
                    "content": "# Projects\n## Scheduler\nBuilt Kubernetes tools in Python.",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(note_request, timeout=5):
            pass

        with urlopen(f"{base_url}/api/application-materials", timeout=5) as response:
            missing_payload = json.loads(response.read().decode())
        assert missing_payload["material_index"]["status"] == "ready"
        assert missing_payload["material_index"]["needs_index"] is False
        assert missing_payload["material_index"]["document_count"] == 2
        assert (index_root / "index.md").is_file()

        changed_request = Request(
            f"{base_url}/api/experience-notes",
            data=json.dumps(
                {
                    "filename": "employment.md",
                    "content": "# Employment\n## Engineer\nImproved PostgreSQL reliability.",
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(changed_request, timeout=5):
            pass

        with urlopen(f"{base_url}/api/application-materials", timeout=5) as response:
            stale_payload = json.loads(response.read().decode())
        assert stale_payload["material_index"]["status"] == "ready"
        assert stale_payload["material_index"]["needs_index"] is False
        assert stale_payload["material_index"]["document_count"] == 4
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
        assert examples[0].content == ("Dear Google,\nI am excited about this internship.")
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_cover_letter_examples_endpoint_extracts_pdf_upload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-cover-letter-pdf.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
    monkeypatch.setattr(
        web_server,
        "_extract_pdf_text",
        lambda _content: "Dear team,\nI build reliable systems.",
    )
    db.ensure_initialized()

    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/api/cover-letter-examples"
        request = Request(
            url,
            data=json.dumps(
                {
                    "filename": "example.pdf",
                    "content_base64": base64.b64encode(b"pdf content").decode(),
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5):
            pass

        examples = []
        with db.connect() as connection:
            examples = list_cover_letter_examples(connection)
        assert examples[0].content == "Dear team,\nI build reliable systems."
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


def test_production_ai_calls_always_receive_explicit_settings_snapshot() -> None:
    """Prevent server workflows from silently falling back to agent environment defaults."""
    required_keyword = {
        "extract_applicant_profile": "settings",
        "evaluate_resume_feedback": "settings",
        "generate_saved_application_answer": "llm_settings",
        "generate_cover_letter": "settings",
        "generate_resume_tweak": "settings",
        "generate_role_chat": "settings",
        "run_scan_company": "llm_settings",
    }
    seen: set[str] = set()
    violations: list[str] = []
    tree = ast.parse(inspect.getsource(web_server))

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        else:
            continue
        keyword_name = required_keyword.get(function_name)
        if keyword_name is None:
            continue
        seen.add(function_name)
        keyword = next((item for item in node.keywords if item.arg == keyword_name), None)
        if keyword is None or (
            isinstance(keyword.value, ast.Constant) and keyword.value.value is None
        ):
            violations.append(f"{function_name} at line {node.lineno}")

    assert seen == set(required_keyword)
    assert violations == []
