from __future__ import annotations

import asyncio
import base64
import binascii
import json
import re
import shutil
import subprocess
import tempfile
import threading
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from io import BytesIO
from pathlib import Path, PurePosixPath
from socketserver import BaseServer
from typing import Any
from urllib.parse import parse_qs, urlparse
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from platformdirs import user_data_path

from callumployed.agents.cover_letter import generate_cover_letter
from callumployed.agents.resume_feedback import evaluate_resume_feedback
from callumployed.data import db
from callumployed.data.models import CoverLetterExample, MasterResume, RoleStatus
from callumployed.data.repositories import (
    add_cover_letter_example,
    clear_resume_feedback_history,
    count_resume_feedback_history,
    get_company,
    get_location_filter,
    get_master_resume,
    get_role,
    get_tracking_stats,
    list_companies,
    list_config_values,
    list_cover_letter_example_knowledge,
    list_cover_letter_examples,
    list_resume_feedback_knowledge,
    list_role_items,
    list_scan_runs,
    record_resume_feedback_history,
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
            path_parts = [part for part in PurePosixPath(parsed_url.path).parts if part != "/"]
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "prep-analysis"
            ):
                self._send_prep_analysis(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "cover-letter"
            ):
                self._send_cover_letter(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "cover-letter.pdf"
            ):
                self._send_cover_letter_pdf(path_parts[2])
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
                and path_parts[3] == "prep-feedback"
            ):
                self._accept_prep_feedback(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "prep-feedback-ignore"
            ):
                self._ignore_prep_feedback(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "resume-pdf"
            ):
                self._generate_resume_pdf(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "cover-letter"
            ):
                self._generate_cover_letter(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "resume-resources"
            ):
                self._upload_resume_resource(path_parts[2])
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
            if len(path_parts) == 2 and path_parts == ["api", "resume-resources"]:
                self._upload_resume_resource()
                return
            if len(path_parts) == 3 and path_parts == ["api", "scan", "all"]:
                self._start_scan_all()
                return
            if len(path_parts) == 2 and path_parts == ["api", "config"]:
                self._update_config()
                return
            if len(path_parts) == 3 and path_parts == [
                "api",
                "recommendation-history",
                "clear",
            ]:
                self._clear_recommendation_history()
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

        def _send_prep_analysis(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return

            try:
                with db.connect() as connection:
                    role = get_role(connection, role_id)
                    resume = get_master_resume(connection)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return

            analysis = build_prep_analysis(role.model_dump(mode="json"), resume)
            self._send_json(
                {
                    "analysis": analysis,
                    "resources": _list_role_resume_resources(role.id or role_id),
                }
            )

        def _accept_prep_feedback(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            feedback_index = payload.get("feedback_index")
            if not isinstance(feedback_index, int):
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected feedback_index")
                return
            try:
                with db.connect() as connection:
                    role = get_role(connection, role_id)
                    resume = get_master_resume(connection)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            if resume is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "No master resume stored")
                return
            feedback = payload.get("feedback_item")
            if not isinstance(feedback, dict):
                analysis = build_prep_analysis(role.model_dump(mode="json"), resume)
                feedback_items = analysis.get("feedback_items")
                if (
                    not isinstance(feedback_items, list)
                    or not 0 <= feedback_index < len(feedback_items)
                ):
                    self.send_error(HTTPStatus.BAD_REQUEST, "Invalid feedback_index")
                    return
                feedback = feedback_items[feedback_index]
            if not isinstance(feedback, dict):
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid feedback item")
                return
            resume_path = _apply_feedback_to_role_resume(role.id or role_id, resume, feedback)
            with db.connect() as connection:
                record_resume_feedback_history(
                    connection,
                    role=role,
                    feedback_index=feedback_index,
                    feedback=feedback,
                    response="accepted",
                    comment=_optional_comment(payload.get("comment")),
                )
                role = set_role_status(
                    connection,
                    role_id,
                    RoleStatus.PREPARED,
                    summary="Custom resume prepared from accepted AI feedback.",
                )
            self._send_json(
                {
                    "accepted": True,
                    "feedback_index": feedback_index,
                    "resume_path": str(resume_path),
                    "role": role.model_dump(mode="json"),
                }
            )

        def _ignore_prep_feedback(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            feedback_index = payload.get("feedback_index")
            feedback = payload.get("feedback_item")
            if not isinstance(feedback_index, int):
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected feedback_index")
                return
            if not isinstance(feedback, dict):
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid feedback item")
                return
            try:
                with db.connect() as connection:
                    role = get_role(connection, role_id)
                    history_id = record_resume_feedback_history(
                        connection,
                        role=role,
                        feedback_index=feedback_index,
                        feedback=feedback,
                        response="ignored",
                        comment=_optional_comment(payload.get("comment")),
                    )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            self._send_json(
                {
                    "ignored": True,
                    "feedback_index": feedback_index,
                    "history_id": history_id,
                }
            )

        def _generate_resume_pdf(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            try:
                with db.connect() as connection:
                    role = get_role(connection, role_id)
                    resume = get_master_resume(connection)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            if resume is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "No master resume stored")
                return
            try:
                pdf_path = _generate_role_resume_pdf(role.model_dump(mode="json"), resume)
            except RuntimeError as error:
                self._send_json_with_status(
                    {"error": str(error)},
                    HTTPStatus.SERVICE_UNAVAILABLE,
                )
                return
            self._send_json({"pdf_path": str(pdf_path)})

        def _generate_cover_letter(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            tweaks = _optional_cover_letter_tweaks(payload.get("tweaks"))
            try:
                with db.connect() as connection:
                    role = get_role(connection, role_id)
                    company = get_company(connection, role.company_id)
                    resume = get_master_resume(connection)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            if resume is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "No master resume stored")
                return
            role_payload = role.model_dump(mode="json")
            role_payload["company_name"] = company.name
            try:
                cover_letter = build_role_cover_letter(role_payload, resume, tweaks=tweaks)
            except RuntimeError as error:
                self._send_json_with_status(
                    {"error": str(error)},
                    HTTPStatus.SERVICE_UNAVAILABLE,
                )
                return
            self._send_json({"cover_letter": cover_letter})

        def _send_cover_letter(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            try:
                with db.connect() as connection:
                    get_role(connection, role_id)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            self._send_json({"cover_letter": _saved_role_cover_letter(role_id)})

        def _send_cover_letter_pdf(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            try:
                with db.connect() as connection:
                    get_role(connection, role_id)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            cover_letter_path = _role_cover_letter_tex_path(role_id)
            pdf_path = cover_letter_path.with_suffix(".pdf")
            pdf_is_stale = (
                pdf_path.exists()
                and cover_letter_path.exists()
                and pdf_path.stat().st_mtime < cover_letter_path.stat().st_mtime
            )
            if (not pdf_path.exists() or pdf_is_stale) and cover_letter_path.exists():
                try:
                    pdf_path, _ = _generate_cover_letter_pdf_preview(cover_letter_path)
                except RuntimeError as error:
                    self._send_json_with_status(
                        {"error": str(error)},
                        HTTPStatus.SERVICE_UNAVAILABLE,
                    )
                    return
            if not pdf_path.exists():
                self.send_error(HTTPStatus.NOT_FOUND, "Cover letter PDF not found")
                return
            self._send_pdf_file(pdf_path, filename=f"callumployed-role-{role_id}-cover-letter.pdf")

        def _upload_resume_resource(self, role_id_text: str | None = None) -> None:
            role_id: int | None = None
            if role_id_text is not None:
                try:
                    role_id = int(role_id_text)
                except ValueError:
                    self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                    return
            payload = self._read_json_body()
            if payload is None:
                return
            filename = payload.get("filename")
            content_base64 = payload.get("content_base64")
            if not isinstance(filename, str) or not isinstance(content_base64, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected filename and content_base64")
                return
            if role_id is not None:
                try:
                    with db.connect() as connection:
                        role = get_role(connection, role_id)
                        resume = get_master_resume(connection)
                except LookupError:
                    self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                    return
                if resume is not None:
                    _sync_resume_resources_to_role(role.id or role_id)
            try:
                saved_path = (
                    _save_role_resume_resource(role.id or role_id, filename, content_base64)
                    if role_id is not None
                    else _save_resume_resource(filename, content_base64)
                )
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return
            self._send_json(
                {
                    "resource": _resume_resource_summary(saved_path),
                    "resources": (
                        _list_role_resume_resources(role.id or role_id)
                        if role_id is not None
                        else _list_resume_resources()
                    ),
                }
            )

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
            content_base64 = payload.get("content_base64")
            if not isinstance(filename, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected filename")
                return
            try:
                extracted_content = _cover_letter_content_from_payload(
                    filename,
                    content=content,
                    content_base64=content_base64,
                )
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            try:
                with db.connect() as connection:
                    example = add_cover_letter_example(
                        connection,
                        filename=filename,
                        content=extracted_content,
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

        def _clear_recommendation_history(self) -> None:
            with db.connect() as connection:
                db.run_migrations(connection)
                deleted_count = clear_resume_feedback_history(connection)
            self._send_json(
                {
                    "cleared": True,
                    "deleted_count": deleted_count,
                    "config": build_config_payload(),
                }
            )

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

        def _send_pdf_file(self, path: Path, *, filename: str) -> None:
            body = path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Content-Disposition", f'inline; filename="{filename}"')
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
        recommendation_history_count = count_resume_feedback_history(connection)
    return {
        "values": values,
        "recommendation_history_count": recommendation_history_count,
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
                "description": "require intern evidence before tracking roles",
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


def build_prep_analysis(
    role: dict[str, Any],
    resume: MasterResume | None,
    *,
    use_agent: bool = True,
) -> dict[str, Any]:
    if use_agent and resume is not None:
        try:
            with db.connect() as connection:
                db.run_migrations(connection)
                knowledge_base = list_resume_feedback_knowledge(
                    connection,
                    role=role,
                    resume_content=resume.content,
                )
            response = asyncio.run(
                evaluate_resume_feedback(
                    role=role,
                    resume_content=resume.content,
                    knowledge_base=knowledge_base,
                )
            )
            payload = response.model_dump(mode="json")
            return {
                "role_id": role.get("id"),
                "source": "ai_resume_feedback",
                "recommendation_history_matches": len(knowledge_base),
                "matched_terms": [],
                "missing_terms": [],
                **payload,
            }
        except Exception:  # noqa: BLE001 - prep view should still work without LLM access.
            pass

    title = str(role.get("title") or "this role")
    description = str(role.get("description") or "")
    location = str(role.get("location") or "")
    resume_content = resume.content if resume is not None else ""
    role_terms = _prep_keywords(" ".join([title, description, location]))
    resume_terms = _prep_keywords(resume_content)
    matched_terms = sorted(role_terms & resume_terms)[:10]
    missing_terms = sorted(role_terms - resume_terms)[:10]

    if resume is None:
        overview = "no master resume is stored yet, so fit analysis is limited to the job text."
    elif not description.strip():
        overview = (
            "resume fit is hard to judge because this role does not have a saved job "
            "description yet."
        )
    elif matched_terms:
        overview = (
            f"resume has visible overlap with {title}, especially around "
            f"{', '.join(matched_terms[:4])}."
        )
    else:
        overview = (
            f"resume overlap with {title} is not obvious from the saved text; tailor the "
            "materials around the role's strongest requirements."
        )

    feedback_items: list[dict[str, str]] = []
    if resume is None:
        feedback_items.append(
            {
                "label": "setup",
                "title": "upload master resume",
                "detail": "add the current .tex resume before tailoring materials for this role.",
            }
        )
    if not description.strip():
        feedback_items.append(
            {
                "label": "refresh_context",
                "title": "refresh job context: saved description is missing",
                "detail": "rescan or open the role page so the prep view has full job context.",
            }
        )
    if matched_terms:
        feedback_items.append(
            {
                "label": "change_wording",
                "title": "change wording to align with posting: matched experience",
                "detail": (
                    f"rewrite an existing project or experience bullet to foreground "
                    f"{', '.join(matched_terms[:5])} using language from the posting."
                ),
            }
        )
    if missing_terms:
        feedback_items.append(
            {
                "label": "add_skills",
                "title": "add skills matching the posting: missing keywords",
                "detail": (
                    f"add {', '.join(missing_terms[:5])} only where they are honestly "
                    "supported by existing resume projects or experience."
                ),
            }
        )
    feedback_items.append(
        {
            "label": "move_emphasis",
            "title": "move emphasis earlier: strongest company-relevant project",
            "detail": "move the most relevant project or skill cluster higher in the resume.",
        }
    )

    verdict = "tweak" if feedback_items[:-1] else "ready_to_apply"
    if verdict == "ready_to_apply":
        overview = f"{title} looks ready to apply based on the saved resume and job context."
        feedback_items = []

    return {
        "role_id": role.get("id"),
        "source": "local_resume_job_analysis",
        "recommendation_history_matches": 0,
        "verdict": verdict,
        "overview": overview,
        "matched_terms": matched_terms,
        "missing_terms": missing_terms,
        "feedback_items": feedback_items,
    }


def build_role_cover_letter(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    tweaks: str | None = None,
) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")

    def search_cover_letters(query: str, *, limit: int = 3) -> list[dict[str, object]]:
        with db.connect() as connection:
            db.run_migrations(connection)
            return list_cover_letter_example_knowledge(
                connection,
                query=query,
                limit=limit,
            )

    try:
        draft = asyncio.run(
            generate_cover_letter(
                role=role,
                resume_content=resume.content,
                search_tool=search_cover_letters,
                tweaks=tweaks,
            )
        )
        latex = _normalize_cover_letter_latex(draft.latex)
        example_ids = draft.example_ids
        source = "ai_cover_letter"
    except Exception:  # noqa: BLE001 - prep should degrade when the LLM is unavailable.
        latex = _normalize_cover_letter_latex(_fallback_cover_letter_latex(role, resume))
        example_ids = []
        source = "local_cover_letter_fallback"
    summary = _cover_letter_display_summary(
        role,
        source=source,
        example_count=len(example_ids),
    )

    cover_letter_path = _role_cover_letter_tex_path(role_id)
    cover_letter_path.parent.mkdir(parents=True, exist_ok=True)
    cover_letter_path.write_text(latex)
    pdf_path, pdf_base64 = _generate_cover_letter_pdf_preview(cover_letter_path)
    return {
        "role_id": role_id,
        "source": source,
        "summary": summary,
        "latex": latex,
        "example_ids": example_ids,
        "tweaks": tweaks,
        "path": str(cover_letter_path),
        "pdf_path": str(pdf_path),
        "pdf_base64": pdf_base64,
    }


def _normalize_cover_letter_latex(latex: str) -> str:
    content = _normalize_cover_letter_text_characters(latex.strip())
    content = _strip_cover_letter_em_dashes(content)
    content = _strip_resume_pdf_compatibility_commands(content)
    content = _strip_generated_cover_letter_comments(content)
    content = _escape_unescaped_latex_percent(content)
    content = _escape_unescaped_latex_ampersands(content)
    content = _repair_single_cover_letter_line_breaks(content)
    content = _remove_cover_letter_website_header_lines(content)
    if "\\documentclass" not in content:
        content = (
            "\\documentclass[11pt]{letter}\n"
            "\\usepackage[margin=1in]{geometry}\n"
            "\\begin{document}\n"
            f"{content}\n"
            "\\end{document}\n"
        )
    content = _normalize_cover_letter_page_layout(content)
    content = _normalize_cover_letter_signature(content)
    content = _repair_broken_cover_letter_links(content)
    content = _normalize_manual_cover_letter_header(_left_align_cover_letter_header(content))
    return f"{content.rstrip()}\n"


def _strip_cover_letter_em_dashes(latex: str) -> str:
    return latex.replace("\u2014", " - ").replace("---", " - ")


def _normalize_cover_letter_text_characters(latex: str) -> str:
    content = (
        latex.replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\x19", "'")
    )
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x18\x1a-\x1f]", "", content)


def _strip_resume_pdf_compatibility_commands(latex: str) -> str:
    return re.sub(
        r"(?m)^.*(?:glyphtounicode|pdfgentounicode|pdfglyphtounicode).*\n?",
        "",
        latex,
    )


def _strip_generated_cover_letter_comments(latex: str) -> str:
    return re.sub(r"(?m)^\s*%.*\n?", "", latex)


def _escape_unescaped_latex_percent(latex: str) -> str:
    return re.sub(r"(?<!\\)%", r"\\%", latex)


def _escape_unescaped_latex_ampersands(latex: str) -> str:
    return re.sub(r"(?<!\\)&", r"\\&", latex)


def _remove_cover_letter_website_header_lines(latex: str) -> str:
    lines = []
    for line in latex.splitlines():
        normalized = line.lower()
        has_personal_site = "camackenzie.com" in normalized
        is_email = "@" in normalized or "mailto:" in normalized
        if has_personal_site and not is_email:
            if "[12pt]" in line and lines and lines[-1].rstrip().endswith("\\\\"):
                lines[-1] = f"{lines[-1].rstrip()}[12pt]"
            continue
        lines.append(line)
    return "\n".join(lines)


def _normalize_cover_letter_page_layout(latex: str) -> str:
    content = re.sub(
        r"\\usepackage(?:\[[^\]]*\])?\{"
        r"(?:fullpage|parskip|latexsym|titlesec|marvosym|color|verbatim|enumitem|fancyhdr)"
        r"\}\s*",
        "",
        latex,
    )
    content = re.sub(
        r"\\usepackage(?:\[[^\]]*\])?\{geometry\}",
        r"\\usepackage[margin=1in]{geometry}",
        content,
        count=1,
    )
    if "\\usepackage" not in content or "\\usepackage[margin=1in]{geometry}" not in content:
        content = re.sub(
            r"(\\documentclass(?:\[[^\]]*\])?\{[^}]+\}\s*)",
            lambda match: f"{match.group(1)}\\usepackage[margin=1in]{{geometry}}\n",
            content,
            count=1,
        )
    content = re.sub(r"\\setlength\{\\parskip\}\{[^}]*\}\s*", "", content)
    content = re.sub(r"\\setlength\{\\parindent\}\{[^}]*\}\s*", "", content)
    content = re.sub(r"\\linespread\{[^}]*\}\s*", "", content)
    content = re.sub(r"\\pagestyle\{[^}]*\}\s*", "", content)
    content = re.sub(r"\\fancyhf\{[^}]*\}\s*", "", content)
    content = re.sub(r"\\fancyfoot\{[^}]*\}\s*", "", content)
    content = re.sub(
        r"\\renewcommand\{\\(?:headrulewidth|footrulewidth)\}\{[^}]*\}\s*",
        "",
        content,
    )
    content = re.sub(r"\\addtolength\{\\[^}]+\}\{[^}]*\}\s*", "", content)
    content = re.sub(r"\\urlstyle\{[^}]*\}\s*", "", content)
    content = re.sub(r"\\ragged(?:bottom|right)\s*", "", content)
    content = re.sub(r"\\setlength\{\\tabcolsep\}\{[^}]*\}\s*", "", content)
    content = re.sub(r"\\titleformat\{\\section\}.*?\n", "", content)
    layout = (
        "\\setlength{\\parskip}{0.85em}\n"
        "\\setlength{\\parindent}{0pt}\n"
        "\\pagestyle{empty}\n"
    )
    if "\\begin{document}" in content:
        return content.replace("\\begin{document}", f"{layout}\\begin{{document}}", 1)
    return f"{layout}{content}"


def _repair_single_cover_letter_line_breaks(latex: str) -> str:
    return re.sub(
        r"(?m)(\S.*?)\s+\\$",
        lambda match: f"{match.group(1)}\\\\",
        latex,
    )


def _normalize_cover_letter_signature(latex: str) -> str:
    return re.sub(
        r"\\signature\{.*?(?=\\setlength\{\\parskip\}|\\begin\{document\})",
        lambda _match: "\\signature{Callum Mackenzie}\n",
        latex,
        count=1,
        flags=re.DOTALL,
    )


def _repair_broken_cover_letter_links(latex: str) -> str:
    return re.sub(
        r"\\href\{mailto:([^{}\s]+)(?=\s*(?:\\\\|\n\\end\{tabular\}))",
        r"\\href{mailto:\1}{\1}",
        latex,
    )


def _left_align_cover_letter_header(latex: str) -> str:
    address_match = re.search(r"\\address\{(?P<address>.*?)\}\s*", latex, flags=re.DOTALL)
    if address_match is None:
        return latex

    address = address_match.group("address").strip()
    content = latex[: address_match.start()] + latex[address_match.end() :]
    date_match = re.search(r"\\date\{(?P<date>.*?)\}\s*", content, flags=re.DOTALL)
    date_text = ""
    if date_match is not None:
        date_text = date_match.group("date").strip()
        content = content[: date_match.start()] + content[date_match.end() :]

    header_lines = _latex_header_lines(address)
    if date_text:
        header_lines.append(_escape_latex_header_line(date_text))
    header = (
        "\\noindent\\begin{tabular}{@{}l@{}}\n"
        + "\\\\\n".join(header_lines)
        + "\n\\end{tabular}\n\\vspace{1em}\n"
    )
    if "\\begin{letter}" in content:
        return content.replace("\\begin{letter}", f"{header}\\begin{{letter}}", 1)
    if "\\begin{document}" in content:
        return content.replace("\\begin{document}", f"\\begin{{document}}\n{header}", 1)
    return f"{header}{content}"


def _normalize_manual_cover_letter_header(latex: str) -> str:
    header_match = re.search(
        r"\\noindent\\begin\{minipage\}\{\\textwidth\}\n"
        r"(?P<header>.*?)\n"
        r"\\end\{minipage\}\n"
        r"\\vspace\{1em\}\n",
        latex,
        flags=re.DOTALL,
    )
    if header_match is None:
        return latex

    header_lines: list[str] = []
    for row in header_match.group("header").splitlines():
        header_lines.extend(_latex_header_lines(row))
    header = (
        "\\noindent\\begin{tabular}{@{}l@{}}\n"
        + "\\\\\n".join(header_lines)
        + "\n\\end{tabular}\n\\vspace{1em}\n"
    )
    return latex[: header_match.start()] + header + latex[header_match.end() :]


def _latex_header_lines(address: str) -> list[str]:
    lines = re.split(r"\\\\", address)
    return [_escape_latex_header_line(line.strip()) for line in lines if line.strip()]


def _escape_latex_header_line(line: str) -> str:
    return re.sub(r"(?<!\\)&", r"\\&", line)


def _generate_cover_letter_pdf_preview(cover_letter_path: Path) -> tuple[Path, str]:
    compiler = shutil.which("tectonic") or shutil.which("latexmk") or shutil.which("pdflatex")
    if compiler is None:
        raise RuntimeError("No LaTeX compiler found. Install tectonic, latexmk, or pdflatex.")

    cover_letter_dir = cover_letter_path.parent
    _copy_resume_resources_to_directory(cover_letter_dir)
    _remove_latex_compile_artifacts(cover_letter_path)
    compiler_name = Path(compiler).name
    if compiler_name == "tectonic":
        command = [compiler, "--keep-logs", "--keep-intermediates", cover_letter_path.name]
    elif compiler_name == "latexmk":
        command = [compiler, "-pdf", "-interaction=nonstopmode", cover_letter_path.name]
    else:
        command = [compiler, "-interaction=nonstopmode", cover_letter_path.name]
    completed = subprocess.run(
        command,
        cwd=cover_letter_dir,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("LaTeX failed to compile the role cover letter.")

    pdf_path = cover_letter_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"LaTeX did not produce {pdf_path.name}.")
    return pdf_path, base64.b64encode(pdf_path.read_bytes()).decode()


def _remove_latex_compile_artifacts(source_path: Path) -> None:
    for suffix in (".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".xdv"):
        source_path.with_suffix(suffix).unlink(missing_ok=True)


def _saved_role_cover_letter(role_id: int) -> dict[str, Any] | None:
    cover_letter_path = _role_cover_letter_tex_path(role_id)
    if not cover_letter_path.exists():
        return None
    saved_latex = cover_letter_path.read_text()
    normalized_latex = _normalize_cover_letter_latex(saved_latex)
    pdf_path = cover_letter_path.with_suffix(".pdf")
    pdf_is_stale = (
        pdf_path.exists() and pdf_path.stat().st_mtime < cover_letter_path.stat().st_mtime
    )
    if normalized_latex != saved_latex or not pdf_path.exists() or pdf_is_stale:
        cover_letter_path.write_text(normalized_latex)
        with suppress(RuntimeError):
            pdf_path, _ = _generate_cover_letter_pdf_preview(cover_letter_path)
    pdf_is_current = (
        pdf_path.exists() and pdf_path.stat().st_mtime >= cover_letter_path.stat().st_mtime
    )
    pdf_base64 = base64.b64encode(pdf_path.read_bytes()).decode() if pdf_is_current else None
    return {
        "role_id": role_id,
        "source": "saved_cover_letter",
        "summary": "Saved cover letter for this role.",
        "latex": normalized_latex,
        "example_ids": [],
        "path": str(cover_letter_path),
        "pdf_path": str(pdf_path) if pdf_is_current else None,
        "pdf_base64": pdf_base64,
    }


def _cover_letter_display_summary(
    role: dict[str, Any],
    *,
    source: str,
    example_count: int,
) -> str:
    title = str(role.get("title") or "this role").strip()
    company = str(role.get("company_name") or "this company").strip()
    role_label = f"{title} at {company}" if company else title
    if source == "local_cover_letter_fallback":
        return f"Drafted fallback cover letter for {role_label}; AI generation was unavailable."
    if example_count > 0:
        examples = f"{example_count} stored cover letter example"
        if example_count != 1:
            examples += "s"
        return (
            f"Drafted cover letter for {role_label} using resume, "
            f"job description, and {examples}."
        )
    return f"Drafted cover letter for {role_label} using resume and job description."


def _fallback_cover_letter_latex(role: dict[str, Any], resume: MasterResume) -> str:
    title = str(role.get("title") or "this role")
    company = str(role.get("company_name") or "your team")
    description = str(role.get("description") or "")
    resume_terms = sorted(_prep_keywords(resume.content))
    job_terms = sorted(_prep_keywords(" ".join([title, description])))
    matched_terms = ", ".join(sorted(set(resume_terms) & set(job_terms))[:5])
    match_sentence = (
        f"My background aligns especially around {matched_terms}."
        if matched_terms
        else "My resume includes software engineering experience relevant to this role."
    )
    return (
        "\\documentclass[11pt]{letter}\n"
        "\\usepackage[margin=1in]{geometry}\n"
        "\\begin{document}\n"
        f"\\begin{{letter}}{{{company}}}\n"
        "\\opening{Dear Hiring Team,}\n\n"
        f"I am excited to apply for the {title} position at {company}. "
        f"{match_sentence} "
        "I would welcome the opportunity to contribute to the team and tailor my "
        "experience to the needs of this posting.\n\n"
        "\\closing{Sincerely,\\\\Callum Mackenzie}\n"
        "\\end{letter}\n"
        "\\end{document}\n"
    )


def _prep_keywords(text: str) -> set[str]:
    ignored_terms = {
        "about",
        "and",
        "are",
        "for",
        "from",
        "intern",
        "internship",
        "role",
        "software",
        "the",
        "this",
        "with",
        "you",
        "your",
    }
    normalized = "".join(character.lower() if character.isalnum() else " " for character in text)
    return {
        word
        for word in normalized.split()
        if len(word) >= 4 and word not in ignored_terms
    }


def _optional_comment(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _optional_cover_letter_tweaks(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _prepared_resumes_root() -> Path:
    return user_data_path("callumployed", appauthor=False) / "prepared-resumes"


def _resume_resources_root() -> Path:
    return user_data_path("callumployed", appauthor=False) / "resume-resources"


def _role_resume_dir(role_id: int) -> Path:
    return _prepared_resumes_root() / f"role-{role_id}"


def _role_resume_tex_path(role_id: int) -> Path:
    return _role_resume_dir(role_id) / "resume.tex"


def _role_cover_letter_tex_path(role_id: int) -> Path:
    return _role_resume_dir(role_id) / "cover-letter.tex"


def _resume_resource_summary(path: Path) -> dict[str, Any]:
    return {
        "filename": path.name,
        "bytes": path.stat().st_size,
    }


def _list_resume_resources() -> list[dict[str, Any]]:
    resource_dir = _resume_resources_root()
    if not resource_dir.exists():
        return []
    return [
        _resume_resource_summary(path)
        for path in sorted(resource_dir.iterdir(), key=lambda item: item.name.lower())
        if path.is_file()
    ]


def _list_role_resume_resources(role_id: int) -> list[dict[str, Any]]:
    resume_dir = _role_resume_dir(role_id)
    if not resume_dir.exists():
        return []
    excluded_names = {
        "resume.tex",
        "resume.pdf",
        "resume-tectonic.tex",
        "resume-tectonic.pdf",
    }
    excluded_suffixes = {".aux", ".fls", ".fdb_latexmk", ".log", ".out", ".synctex.gz"}
    resources: list[dict[str, Any]] = []
    for path in sorted(resume_dir.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_file():
            continue
        if path.name in excluded_names or any(
            path.name.endswith(suffix) for suffix in excluded_suffixes
        ):
            continue
        resources.append(_resume_resource_summary(path))
    return resources


def _ensure_role_resume_copy(role_id: int, resume: MasterResume) -> Path:
    resume_dir = _role_resume_dir(role_id)
    resume_dir.mkdir(parents=True, exist_ok=True)
    resume_path = _role_resume_tex_path(role_id)
    if not resume_path.exists():
        resume_path.write_text(resume.content)
    _sync_resume_resources_to_role(role_id)
    return resume_path


def _sync_resume_resources_to_role(role_id: int) -> None:
    resource_dir = _resume_resources_root()
    if not resource_dir.exists():
        return
    resume_dir = _role_resume_dir(role_id)
    resume_dir.mkdir(parents=True, exist_ok=True)
    for resource_path in resource_dir.iterdir():
        if resource_path.is_file():
            shutil.copyfile(resource_path, resume_dir / resource_path.name)


def _save_resume_resource(filename: str, content_base64: str) -> Path:
    return _save_resource_file(_resume_resources_root(), filename, content_base64)


def _save_role_resume_resource(role_id: int, filename: str, content_base64: str) -> Path:
    return _save_resource_file(_role_resume_dir(role_id), filename, content_base64)


def _save_resource_file(root: Path, filename: str, content_base64: str) -> Path:
    safe_filename = _safe_resource_filename(filename)
    try:
        content = base64.b64decode(content_base64, validate=True)
    except binascii.Error as error:
        raise ValueError("Resource content must be valid base64") from error
    root.mkdir(parents=True, exist_ok=True)
    target_path = root / safe_filename
    target_path.write_bytes(content)
    return target_path


def _safe_resource_filename(filename: str) -> str:
    safe_filename = PurePosixPath(filename).name.strip()
    if not safe_filename or safe_filename in {".", ".."}:
        raise ValueError("Invalid resource filename")
    if safe_filename in {"resume.tex", "resume.pdf"}:
        raise ValueError("Resource filename is reserved")
    return safe_filename


def _apply_feedback_to_role_resume(
    role_id: int,
    resume: MasterResume,
    feedback: dict[str, Any],
) -> Path:
    resume_path = _ensure_role_resume_copy(role_id, resume)
    title = str(feedback.get("title") or "resume feedback")
    detail = str(feedback.get("detail") or "")
    marker = f"% callumployed accepted feedback: {title}"
    existing_content = resume_path.read_text()
    if marker in existing_content:
        return resume_path
    target_text = feedback.get("target_text")
    replacement_text = feedback.get("replacement_text")
    latex_addition = feedback.get("latex_addition")
    updated_content = existing_content

    if (
        isinstance(target_text, str)
        and target_text
        and isinstance(replacement_text, str)
        and replacement_text
        and target_text in updated_content
    ):
        updated_content = updated_content.replace(target_text, replacement_text, 1)
    elif isinstance(latex_addition, str) and latex_addition.strip():
        addition = "\n".join(
            [
                "",
                "% callumployed accepted prep feedback",
                marker,
                latex_addition.strip(),
                "",
            ]
        )
        if "\\end{document}" in updated_content:
            updated_content = updated_content.replace(
                "\\end{document}",
                f"{addition}\\end{{document}}",
                1,
            )
        else:
            updated_content = f"{updated_content.rstrip()}{addition}"
    else:
        updated_content = "\n".join(
            [
                updated_content.rstrip(),
                "",
                "% callumployed accepted prep feedback",
                marker,
                f"% {detail}",
                "",
            ]
        )

    if marker not in updated_content:
        updated_content = "\n".join([updated_content.rstrip(), "", marker, ""])
    resume_path.write_text(updated_content)
    return resume_path


def _generate_role_resume_pdf(role: dict[str, Any], resume: MasterResume) -> Path:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")
    compiler = shutil.which("tectonic") or shutil.which("latexmk") or shutil.which("pdflatex")
    if compiler is None:
        raise RuntimeError("No LaTeX compiler found. Install tectonic, latexmk, or pdflatex.")

    persistent_resume_path = _role_resume_tex_path(role_id)
    if persistent_resume_path.exists():
        _sync_resume_resources_to_role(role_id)
        return _compile_role_resume_pdf(
            role=role,
            role_id=role_id,
            compiler=compiler,
            resume_path=persistent_resume_path,
        )

    with tempfile.TemporaryDirectory(prefix=f"callumployed-role-{role_id}-") as temp_dir:
        temp_path = Path(temp_dir)
        resume_path = temp_path / "resume.tex"
        resume_path.write_text(resume.content)
        _copy_resume_resources_to_directory(temp_path)
        return _compile_role_resume_pdf(
            role=role,
            role_id=role_id,
            compiler=compiler,
            resume_path=resume_path,
        )


def _compile_role_resume_pdf(
    *,
    role: dict[str, Any],
    role_id: int,
    compiler: str,
    resume_path: Path,
) -> Path:
    resume_dir = resume_path.parent
    compiler_name = Path(compiler).name
    if compiler_name == "tectonic":
        compile_path = _write_tectonic_resume_input(resume_path)
        command = [compiler, "--keep-logs", "--keep-intermediates", compile_path.name]
        generated_pdf = resume_dir / f"{compile_path.stem}.pdf"
    elif compiler_name == "latexmk":
        generated_pdf = resume_dir / "resume.pdf"
        command = [compiler, "-pdf", "-interaction=nonstopmode", resume_path.name]
    else:
        generated_pdf = resume_dir / "resume.pdf"
        command = [compiler, "-interaction=nonstopmode", resume_path.name]
    completed = subprocess.run(
        command,
        cwd=resume_dir,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("LaTeX failed to compile the role resume.")

    if not generated_pdf.exists():
        raise RuntimeError(f"LaTeX did not produce {generated_pdf.name}.")

    downloads_dir = Path.home() / "Downloads"
    safe_title = _safe_filename(str(role.get("title") or f"role-{role_id}"))
    target_path = downloads_dir / f"callumployed-{role_id}-{safe_title}-resume.pdf"
    shutil.copyfile(generated_pdf, target_path)
    return target_path


def _copy_resume_resources_to_directory(target_dir: Path) -> None:
    resource_dir = _resume_resources_root()
    if not resource_dir.exists():
        return
    for resource_path in resource_dir.iterdir():
        if resource_path.is_file():
            shutil.copyfile(resource_path, target_dir / resource_path.name)


def _write_tectonic_resume_input(resume_path: Path) -> Path:
    content = resume_path.read_text()
    compatibility = (
        "% callumployed tectonic compatibility\n"
        "\\providecommand{\\pdfglyphtounicode}[2]{}\n"
        "\\ifdefined\\pdfgentounicode\\else\\newcount\\pdfgentounicode\\fi\n"
    )
    if (
        ("\\pdfglyphtounicode" in content or "\\pdfgentounicode" in content)
        and compatibility not in content
    ):
        content = content.replace("\\documentclass", f"{compatibility}\\documentclass", 1)
    compile_path = resume_path.with_name("resume-tectonic.tex")
    compile_path.write_text(content)
    return compile_path


def _safe_filename(value: str) -> str:
    cleaned = "".join(character.lower() if character.isalnum() else "-" for character in value)
    parts = [part for part in cleaned.split("-") if part]
    return "-".join(parts[:10]) or "role"


def _application_materials_payload(
    resume: MasterResume | None,
    examples: list[CoverLetterExample],
) -> dict[str, Any]:
    return {
        "master_resume": _master_resume_summary(resume) if resume else None,
        "cover_letter_examples": [
            _cover_letter_example_summary(example) for example in examples
        ],
        "resume_resources": _list_resume_resources(),
        "ui": {
            "default_collapsed": resume is not None and len(examples) >= 1,
            "has_master_resume": resume is not None,
            "cover_letter_example_count": len(examples),
            "resume_resource_count": len(_list_resume_resources()),
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


def _cover_letter_content_from_payload(
    filename: str,
    *,
    content: object,
    content_base64: object,
) -> str:
    if filename.lower().endswith(".docx"):
        if not isinstance(content_base64, str):
            raise ValueError("DOCX cover letter uploads require content_base64")
        try:
            document_bytes = base64.b64decode(content_base64, validate=True)
        except (binascii.Error, ValueError) as error:
            raise ValueError("DOCX cover letter content is not valid base64") from error
        return _extract_docx_text(document_bytes)
    if not isinstance(content, str):
        raise ValueError("Expected filename and content")
    return content


def _extract_docx_text(document_bytes: bytes) -> str:
    try:
        with ZipFile(BytesIO(document_bytes)) as archive:
            document_xml = archive.read("word/document.xml")
    except (BadZipFile, KeyError) as error:
        raise ValueError("DOCX cover letter content could not be read") from error

    try:
        document = ElementTree.fromstring(document_xml)
    except ElementTree.ParseError as error:
        raise ValueError("DOCX cover letter document XML could not be parsed") from error

    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    for paragraph in document.findall(".//w:p", namespace):
        parts: list[str] = []
        for node in paragraph.iter():
            if node.tag == f"{{{namespace['w']}}}t" and node.text:
                parts.append(node.text)
            elif node.tag == f"{{{namespace['w']}}}tab":
                parts.append("\t")
            elif node.tag == f"{{{namespace['w']}}}br":
                parts.append("\n")
        text = "".join(parts).strip()
        if text:
            paragraphs.append(text)
    extracted = "\n".join(paragraphs).strip()
    if not extracted:
        raise ValueError("DOCX cover letter content cannot be empty")
    return extracted


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _datetime_or_none(value: datetime | None) -> str | None:
    if value is None:
        return None
    value = value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
    return value.isoformat().replace("+00:00", "Z")


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
