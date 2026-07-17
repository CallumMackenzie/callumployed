from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
from typer.testing import CliRunner

from callumployed.cli import app
from callumployed.data import db
from callumployed.web.server import LocalThreadingHTTPServer, build_tracker_payload, create_handler

runner = CliRunner()


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
