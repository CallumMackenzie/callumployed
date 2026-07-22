from __future__ import annotations

import asyncio
import json
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import PurePosixPath
from socketserver import BaseServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from callumployed.data import db
from callumployed.data.models import CoverLetterExample, MasterResume, RoleStatus
from callumployed.data.repositories import (
    add_cover_letter_example,
    get_location_filter,
    get_master_resume,
    get_tracking_stats,
    list_companies,
    list_config_values,
    list_cover_letter_examples,
    list_role_items,
    list_scan_runs,
    record_role_review_later,
    set_include_graduate_degree_roles,
    set_include_hardware_roles,
    set_internship_mode,
    set_location_filter,
    set_require_software_keywords,
    set_role_status,
    should_include_graduate_degree_roles,
    should_include_hardware_roles,
    should_require_software_keywords,
    should_use_internship_mode,
    upsert_master_resume,
)
from callumployed.services.scan_workflow import scan_company as run_scan_company
from callumployed.webscraping.profile_manager import BrowserProfileManager

STATIC_PACKAGE = "callumployed.web.static"
STATUS_LABELS: dict[str, str] = {
    RoleStatus.DISCOVERED.value: "discovered",
    RoleStatus.INTERESTED.value: "interested",
    RoleStatus.DISINTERESTED.value: "disinterested",
    RoleStatus.PREPARED.value: "prepared",
    RoleStatus.APPLIED.value: "applied",
    RoleStatus.OA.value: "oa",
    RoleStatus.INTERVIEW.value: "interview",
    RoleStatus.REJECTED.value: "rejected",
    RoleStatus.OFFER.value: "offer",
    RoleStatus.CLOSED.value: "closed",
    RoleStatus.ARCHIVED.value: "archived",
}


@dataclass(frozen=True)
class ScanCoordinatorSnapshot:
    scanning: bool
    started_at: datetime | None
    finished_at: datetime | None
    completed_companies: int
    total_companies: int
    failed_companies: int
    error: str | None


class ScanCoordinator:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._started_at: datetime | None = None
        self._finished_at: datetime | None = None
        self._completed_companies = 0
        self._total_companies = 0
        self._failed_companies = 0
        self._error: str | None = None

    def start(self) -> bool:
        with self._lock:
            if self._thread is not None and self._thread.is_alive():
                return False
            self._started_at = _now_utc()
            self._finished_at = None
            self._completed_companies = 0
            self._total_companies = 0
            self._failed_companies = 0
            self._error = None
            self._thread = threading.Thread(
                target=self._run,
                name="callumployed-scan-all",
                daemon=True,
            )
            self._thread.start()
            return True

    def snapshot(self) -> ScanCoordinatorSnapshot:
        with self._lock:
            scanning = self._thread is not None and self._thread.is_alive()
            return ScanCoordinatorSnapshot(
                scanning=scanning,
                started_at=self._started_at,
                finished_at=self._finished_at,
                completed_companies=self._completed_companies,
                total_companies=self._total_companies,
                failed_companies=self._failed_companies,
                error=self._error,
            )

    def _run(self) -> None:
        try:
            asyncio.run(self._scan_all_companies())
        except Exception as error:
            with self._lock:
                self._error = str(error)
        finally:
            with self._lock:
                self._finished_at = _now_utc()

    async def _scan_all_companies(self) -> None:
        with db.connect() as connection:
            companies = list_companies(connection)
        with self._lock:
            self._total_companies = len(companies)

        browser_profile_manager = BrowserProfileManager()
        for company in companies:
            try:
                await run_scan_company(
                    company,
                    browser_profile_manager=browser_profile_manager,
                )
            except Exception as error:
                with self._lock:
                    self._failed_companies += 1
                    self._error = str(error)
            finally:
                with self._lock:
                    self._completed_companies += 1


SCAN_COORDINATOR = ScanCoordinator()


class LocalThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True

    def server_bind(self) -> None:
        self.socket.bind(self.server_address)
        host, port = self.socket.getsockname()[:2]
        self.server_address = (host, port)
        self.server_name = str(host)
        self.server_port = int(port)


def build_tracker_payload(query: str | None = None) -> dict[str, Any]:
    with db.connect() as connection:
        stats = get_tracking_stats(connection)
        roles = list_role_items(connection, query=query)

    grouped_roles: dict[str, list[dict[str, Any]]] = {status.value: [] for status in RoleStatus}
    for role in roles:
        grouped_roles[role.role_status.value].append(role.model_dump(mode="json"))

    statuses = [
        {
            "key": status.value,
            "label": STATUS_LABELS[status.value],
            "count": len(grouped_roles[status.value]),
            "jobs": grouped_roles[status.value],
        }
        for status in RoleStatus
    ]

    return {
        "stats": stats,
        "statuses": statuses,
        "query": query or "",
    }


def create_handler() -> type[BaseHTTPRequestHandler]:
    class CallumployedHandler(BaseHTTPRequestHandler):
        server_version = "callumployed"

        def do_GET(self) -> None:
            parsed_url = urlparse(self.path)
            if parsed_url.path in {"/", "/index.html"}:
                self._send_static_file("index.html", "text/html; charset=utf-8")
                return
            if parsed_url.path == "/api/tracker":
                query_values = parse_qs(parsed_url.query).get("q", [""])
                query = query_values[0].strip() or None
                self._send_json(build_tracker_payload(query=query))
                return
            if parsed_url.path == "/api/scan/status":
                self._send_json(build_scan_status_payload())
                return
            if parsed_url.path == "/api/application-materials":
                self._send_json(build_application_materials_payload())
                return
            if parsed_url.path == "/api/config":
                self._send_json(build_config_payload())
                return
            if parsed_url.path == "/api/master-resume":
                self._send_json(build_master_resume_payload())
                return
            if parsed_url.path == "/api/cover-letter-examples":
                self._send_json(build_cover_letter_examples_payload())
                return
            if parsed_url.path.startswith("/assets/"):
                filename = PurePosixPath(parsed_url.path).name
                content_type = _content_type_for(filename)
                self._send_static_file(filename, content_type)
                return
            self.send_error(HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:
            parsed_url = urlparse(self.path)
            path_parts = [part for part in PurePosixPath(parsed_url.path).parts if part != "/"]
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "status"
            ):
                self._update_role_status(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "review-later"
            ):
                self._record_review_later(path_parts[2])
                return
            if len(path_parts) == 2 and path_parts == ["api", "master-resume"]:
                self._upsert_master_resume()
                return
            if len(path_parts) == 2 and path_parts == ["api", "cover-letter-examples"]:
                self._add_cover_letter_example()
                return
            if len(path_parts) == 3 and path_parts == ["api", "scan", "all"]:
                self._start_scan_all()
                return
            if len(path_parts) == 2 and path_parts == ["api", "config"]:
                self._update_config()
                return
            self.send_error(HTTPStatus.NOT_FOUND)

        def log_message(self, format: str, *args: object) -> None:
            return

        def _send_json(self, payload: dict[str, Any]) -> None:
            body = json.dumps(payload).encode()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_json_with_status(self, payload: dict[str, Any], status: HTTPStatus) -> None:
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json_body(self) -> dict[str, Any] | None:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                return {}
            try:
                payload = json.loads(self.rfile.read(length).decode())
            except json.JSONDecodeError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON body")
                return None
            if not isinstance(payload, dict):
                self.send_error(HTTPStatus.BAD_REQUEST, "JSON body must be an object")
                return None
            return payload

        def _update_role_status(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return

            payload = self._read_json_body()
            if payload is None:
                return
            status_value = payload.get("status")
            if not isinstance(status_value, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role status")
                return
            try:
                status = RoleStatus(status_value)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role status")
                return

            if status not in {
                RoleStatus.APPLIED,
                RoleStatus.CLOSED,
                RoleStatus.DISINTERESTED,
                RoleStatus.INTERESTED,
                RoleStatus.INTERVIEW,
                RoleStatus.OA,
                RoleStatus.OFFER,
                RoleStatus.REJECTED,
            }:
                self.send_error(HTTPStatus.BAD_REQUEST, "Unsupported role status")
                return

            try:
                with db.connect() as connection:
                    role = set_role_status(
                        connection,
                        role_id,
                        status,
                        summary="Status updated from tracker.",
                    )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return

            self._send_json({"role": role.model_dump(mode="json")})

        def _record_review_later(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return

            try:
                with db.connect() as connection:
                    role = record_role_review_later(connection, role_id)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return

            self._send_json({"role": role.model_dump(mode="json")})

        def _upsert_master_resume(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return

            filename = payload.get("filename")
            content = payload.get("content")
            if not isinstance(filename, str) or not isinstance(content, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected filename and content")
                return

            try:
                with db.connect() as connection:
                    resume = upsert_master_resume(
                        connection,
                        filename=filename,
                        content=content,
                    )
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            self._send_json({"master_resume": _master_resume_summary(resume)})

        def _add_cover_letter_example(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return

            filename = payload.get("filename")
            content = payload.get("content")
            if not isinstance(filename, str) or not isinstance(content, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected filename and content")
                return

            try:
                with db.connect() as connection:
                    example = add_cover_letter_example(
                        connection,
                        filename=filename,
                        content=content,
                    )
                    examples = list_cover_letter_examples(connection)
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            self._send_json(
                {
                    "cover_letter_example": _cover_letter_example_summary(example),
                    "cover_letter_examples": [
                        _cover_letter_example_summary(item) for item in examples
                    ],
                }
            )

        def _start_scan_all(self) -> None:
            started = SCAN_COORDINATOR.start()
            status = HTTPStatus.ACCEPTED if started else HTTPStatus.CONFLICT
            self._send_json_with_status(build_scan_status_payload(), status)

        def _update_config(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return

            allowed_keys = {
                "include_graduate_degree_roles",
                "include_hardware_roles",
                "internship_mode",
                "location_filter",
                "require_software_keywords",
            }
            invalid_keys = sorted(set(payload) - allowed_keys)
            if invalid_keys:
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    f"Unsupported config values: {', '.join(invalid_keys)}",
                )
                return
            if not payload:
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected at least one config value")
                return
            bool_keys = {
                "include_graduate_degree_roles",
                "include_hardware_roles",
                "internship_mode",
                "require_software_keywords",
            }
            if not all(
                isinstance(value, bool) if key in bool_keys else isinstance(value, str)
                for key, value in payload.items()
            ):
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid config value type")
                return

            try:
                with db.connect() as connection:
                    if "include_graduate_degree_roles" in payload:
                        set_include_graduate_degree_roles(
                            connection,
                            payload["include_graduate_degree_roles"],
                        )
                    if "include_hardware_roles" in payload:
                        set_include_hardware_roles(
                            connection,
                            payload["include_hardware_roles"],
                        )
                    if "require_software_keywords" in payload:
                        set_require_software_keywords(
                            connection,
                            payload["require_software_keywords"],
                        )
                    if "internship_mode" in payload:
                        set_internship_mode(
                            connection,
                            payload["internship_mode"],
                        )
                    if "location_filter" in payload:
                        set_location_filter(
                            connection,
                            payload["location_filter"],
                        )
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            self._send_json(build_config_payload())

        def _send_static_file(self, filename: str, content_type: str) -> None:
            try:
                body = resources.files(STATIC_PACKAGE).joinpath(filename).read_bytes()
            except FileNotFoundError:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return CallumployedHandler


def build_scan_status_payload() -> dict[str, Any]:
    snapshot = SCAN_COORDINATOR.snapshot()
    with db.connect() as connection:
        latest_scan_runs = list_scan_runs(connection, limit=1)
    latest_scan = latest_scan_runs[0] if latest_scan_runs else None
    latest_started_at = latest_scan.started_at if latest_scan else None
    latest_finished_at = latest_scan.finished_at if latest_scan else None
    last_scan_at = _latest_datetime(
        snapshot.started_at if snapshot.scanning else None,
        snapshot.finished_at,
        latest_finished_at,
        latest_started_at,
    )
    latest_scan_status = latest_scan.scan_status if latest_scan else None
    return {
        "scanning": snapshot.scanning,
        "started_at": _datetime_or_none(snapshot.started_at),
        "finished_at": _datetime_or_none(snapshot.finished_at),
        "last_scan_at": _datetime_or_none(last_scan_at),
        "completed_companies": snapshot.completed_companies,
        "total_companies": snapshot.total_companies,
        "failed_companies": snapshot.failed_companies,
        "error": snapshot.error,
        "latest_scan": (
            {
                "id": latest_scan.id,
                "company_id": latest_scan.company_id,
                "company_name": latest_scan.company_name,
                "scan_status": latest_scan_status.value if latest_scan_status else None,
                "started_at": _datetime_or_none(latest_started_at),
                "finished_at": _datetime_or_none(latest_finished_at),
            }
            if latest_scan
            else None
        ),
    }


def build_config_payload() -> dict[str, Any]:
    with db.connect() as connection:
        db.run_migrations(connection)
        values = list_config_values(connection)
        include_graduate_degree_roles = should_include_graduate_degree_roles(connection)
        include_hardware_roles = should_include_hardware_roles(connection)
        require_software_keywords = should_require_software_keywords(connection)
        internship_mode = should_use_internship_mode(connection)
        location_filter = get_location_filter(connection)
    return {
        "values": values,
        "settings": [
            {
                "key": "include_graduate_degree_roles",
                "label": "graduate-degree roles",
                "description": "include roles that require or strongly prefer a graduate degree",
                "control": "toggle",
                "value": include_graduate_degree_roles,
                "default": False,
                "editable": True,
            },
            {
                "key": "include_hardware_roles",
                "label": "hardware roles",
                "description": "include hardware, embedded, fpga, and silicon-heavy roles",
                "control": "toggle",
                "value": include_hardware_roles,
                "default": False,
                "editable": True,
            },
            {
                "key": "require_software_keywords",
                "label": "software keywords",
                "description": "reject roles without software-oriented keywords",
                "control": "toggle",
                "value": require_software_keywords,
                "default": True,
                "editable": True,
            },
            {
                "key": "internship_mode",
                "label": "internship mode",
                "description": (
                    "for internship-focused source pages, require intern evidence "
                    "before tracking roles"
                ),
                "control": "toggle",
                "value": internship_mode,
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
                "value": location_filter,
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
        ],
    }


def build_master_resume_payload() -> dict[str, Any]:
    with db.connect() as connection:
        resume = get_master_resume(connection)
    return {"master_resume": _master_resume_summary(resume) if resume else None}


def build_cover_letter_examples_payload() -> dict[str, Any]:
    with db.connect() as connection:
        examples = list_cover_letter_examples(connection)
    return {
        "cover_letter_examples": [
            _cover_letter_example_summary(example) for example in examples
        ]
    }


def build_application_materials_payload() -> dict[str, Any]:
    with db.connect() as connection:
        resume = get_master_resume(connection)
        examples = list_cover_letter_examples(connection)
    return _application_materials_payload(resume, examples)


def _application_materials_payload(
    resume: MasterResume | None,
    examples: list[CoverLetterExample],
) -> dict[str, Any]:
    return {
        "master_resume": _master_resume_summary(resume) if resume else None,
        "cover_letter_examples": [
            _cover_letter_example_summary(example) for example in examples
        ],
        "ui": {
            "default_collapsed": resume is not None and len(examples) >= 1,
            "has_master_resume": resume is not None,
            "cover_letter_example_count": len(examples),
        },
    }


def _master_resume_summary(resume: MasterResume) -> dict[str, Any]:
    return {
        "filename": resume.filename,
        "content_sha256": resume.content_sha256,
        "content_bytes": len(resume.content.encode()),
        "created_at": resume.created_at.isoformat() if resume.created_at else None,
        "updated_at": resume.updated_at.isoformat() if resume.updated_at else None,
    }


def _cover_letter_example_summary(example: CoverLetterExample) -> dict[str, Any]:
    return {
        "id": example.id,
        "filename": example.filename,
        "content_sha256": example.content_sha256,
        "content_bytes": len(example.content.encode()),
        "created_at": example.created_at.isoformat() if example.created_at else None,
        "updated_at": example.updated_at.isoformat() if example.updated_at else None,
    }


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _datetime_or_none(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def _latest_datetime(*values: datetime | None) -> datetime | None:
    present_values = [value for value in values if value is not None]
    if not present_values:
        return None
    return max(present_values, key=_datetime_sort_key)


def _datetime_sort_key(value: datetime) -> float:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.timestamp()


def run_server(host: str, port: int) -> None:
    db.ensure_initialized()
    handler = create_handler()
    server = LocalThreadingHTTPServer((host, port), handler)
    try:
        server.serve_forever()
    finally:
        _close_server(server)


def _close_server(server: BaseServer) -> None:
    server.server_close()


def _content_type_for(filename: str) -> str:
    if filename.endswith(".css"):
        return "text/css; charset=utf-8"
    if filename.endswith(".js"):
        return "text/javascript; charset=utf-8"
    if filename.endswith(".svg"):
        return "image/svg+xml; charset=utf-8"
    return "application/octet-stream"
