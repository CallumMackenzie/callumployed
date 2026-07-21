import asyncio
import json
from pathlib import Path
from threading import Event, Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
from typer.testing import CliRunner

from callumployed.cli import app
from callumployed.data import db
from callumployed.data.models import Company
from callumployed.data.repositories import add_company, create_scan_run
from callumployed.web.server import (
    LocalThreadingHTTPServer,
    ScanCoordinator,
    build_scan_status_payload,
    build_tracker_payload,
    create_handler,
)

runner = CliRunner()


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
            markup = response.read().decode()

        assert 'id="toggle-all"' in markup
        assert "expand all" in markup
        assert 'id="expand-all"' not in markup
        assert 'id="collapse-all"' not in markup
        assert 'id="scan-all-button"' in markup
        assert 'id="scan-summary"' in markup
        assert markup.index('id="review-discovered"') < markup.index('id="scan-all-button"')
        assert markup.index('id="scan-all-button"') < markup.index('id="scan-summary"')
        assert markup.index('id="scan-all-button"') < markup.index('class="status-toolbar"')
        assert 'id="scan-status-bar"' in markup
        assert 'id="scan-status-text"' in markup
        assert markup.index('id="scan-summary"') < markup.index('id="scan-status-text"')
        assert "/assets/app.css?v=20260721-3" in markup
        assert "/assets/app.js?v=20260721-3" in markup
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

    assert payload["last_scan_at"] == scan_run.started_at.isoformat()
    assert payload["latest_scan"]["started_at"] == scan_run.started_at.isoformat()
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
    assert applied["jobs"][0]["created_at"] is not None


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
            assert response.status == 200
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    payload = build_tracker_payload()
    interested = next(status for status in payload["statuses"] if status["key"] == "interested")
    discovered = next(status for status in payload["statuses"] if status["key"] == "discovered")
    assert interested["count"] == 1
    assert discovered["count"] == 0


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
            assert response.status == 200
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


def test_application_materials_endpoint_reports_default_collapsed_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "tracker-application-materials.sqlite3"
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(database))
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
        assert empty_payload["ui"]["has_master_resume"] is False
        assert empty_payload["ui"]["cover_letter_example_count"] == 0

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
        assert resume_only_payload["ui"]["has_master_resume"] is True

        cover_letter_request = Request(
            f"{base_url}/api/cover-letter-examples",
            data=json.dumps({"filename": "cover.md", "content": "Dear team,"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(cover_letter_request, timeout=5):
            pass

        with urlopen(f"{base_url}/api/application-materials", timeout=5) as response:
            ready_payload = json.loads(response.read().decode())
        assert ready_payload["ui"]["default_collapsed"] is True
        assert ready_payload["ui"]["cover_letter_example_count"] == 1
        assert ready_payload["master_resume"]["filename"] == "resume.tex"
        assert ready_payload["cover_letter_examples"][0]["filename"] == "cover.md"
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


@pytest.mark.parametrize("status", ["interview", "rejected"])
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
