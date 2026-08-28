from __future__ import annotations

import asyncio
import base64
import binascii
import gzip
import json
import logging
import re
import shlex
import shutil
import subprocess
import sys
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

from callumployed.agents.cover_letter import (
    ApplicantProfile,
    generate_cover_letter,
    strip_cover_letter_dash_punctuation,
)
from callumployed.agents.resume_feedback import evaluate_resume_feedback
from callumployed.agents.resume_tweaker import generate_resume_tweak
from callumployed.agents.role_chat import generate_role_chat, parse_role_chat_messages
from callumployed.central.client import CentralStoreClient, CentralStoreError
from callumployed.central.config import (
    get_central_api_url,
    get_central_client_id,
    get_central_passkey,
    set_central_api_url,
    set_central_passkey,
)
from callumployed.central.models import ResolveCompanyRequest
from callumployed.central.sync import pull_companies, resolve_unlinked_companies
from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    CoverLetterExample,
    ExperienceNote,
    MasterResume,
    Role,
    RoleListItem,
    RoleStatus,
    ScanStatus,
)
from callumployed.data.repositories import (
    REVIEW_LATER_EVENT_TYPE,
    add_company,
    add_company_career_page,
    add_cover_letter_example,
    add_experience_note,
    add_role,
    clear_resume_feedback_history,
    count_resume_feedback_history,
    deactivate_company,
    delete_company_career_page,
    finish_scan_run,
    get_company,
    get_company_scan_discovery_counts,
    get_config_value,
    get_location_filter,
    get_master_resume,
    get_role,
    get_tracking_stats,
    list_companies,
    list_company_career_pages,
    list_config_values,
    list_cover_letter_example_knowledge,
    list_cover_letter_examples,
    list_experience_notes,
    list_resume_feedback_knowledge,
    list_role_discovery_attempts,
    list_role_items,
    list_roles,
    list_scan_candidates,
    list_scan_pages,
    list_scan_runs,
    record_resume_feedback_history,
    record_role_review_later,
    set_company_central_link,
    set_company_central_sync_status,
    set_config_value,
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
    update_company,
    upsert_master_resume,
)
from callumployed.services.scan_workflow import rescan_role as run_rescan_role
from callumployed.services.scan_workflow import scan_company as run_scan_company
from callumployed.webscraping.profile_manager import BrowserProfileManager

STATIC_PACKAGE = "callumployed.web.static"
INSTALLER_SCRIPT_URL = (
    "https://raw.githubusercontent.com/CallumMackenzie/callumployed/master/scripts/install.sh"
)
LOGGER = logging.getLogger(__name__)
SCAN_ALL_COMPANY_TIMEOUT_SECONDS = 5 * 60
APPLICANT_FIRST_NAME_CONFIG_KEY = "applicant_first_name"
APPLICANT_LAST_NAME_CONFIG_KEY = "applicant_last_name"
APPLICANT_EMAIL_CONFIG_KEY = "applicant_email"
APPLICANT_INSTITUTION_CONFIG_KEY = "applicant_institution"
APPLICANT_DEGREE_CONFIG_KEY = "applicant_degree"
APPLICANT_PROFILE_TEXT_CONFIG_KEYS = {
    APPLICANT_EMAIL_CONFIG_KEY,
    APPLICANT_INSTITUTION_CONFIG_KEY,
    APPLICANT_DEGREE_CONFIG_KEY,
}
STATUS_LABELS: dict[str, str] = {
    RoleStatus.DISCOVERED.value: "discovered",
    RoleStatus.INTERESTED.value: "interested",
    RoleStatus.DISINTERESTED.value: "disinterested",
    RoleStatus.APPLIED.value: "applied",
    RoleStatus.OA.value: "oa",
    RoleStatus.INTERVIEW.value: "interview",
    RoleStatus.REJECTED.value: "rejected",
    RoleStatus.OFFER.value: "offer",
    RoleStatus.CLOSED.value: "closed",
    RoleStatus.ARCHIVED.value: "archived",
}


@dataclass(frozen=True)
class ScanCoordinatorFailure:
    company_id: int | None
    company_name: str
    error: str


@dataclass(frozen=True)
class ScanCoordinatorSnapshot:
    scanning: bool
    cancel_requested: bool
    started_at: datetime | None
    finished_at: datetime | None
    completed_companies: int
    total_companies: int
    failed_companies: int
    error: str | None
    failures: tuple[ScanCoordinatorFailure, ...]


class ScanCoordinator:
    def __init__(
        self,
        *,
        company_timeout_seconds: float = SCAN_ALL_COMPANY_TIMEOUT_SECONDS,
    ) -> None:
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._started_at: datetime | None = None
        self._finished_at: datetime | None = None
        self._completed_companies = 0
        self._total_companies = 0
        self._failed_companies = 0
        self._error: str | None = None
        self._failures: list[ScanCoordinatorFailure] = []
        self._cancel_requested = threading.Event()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._current_task: asyncio.Task[None] | None = None
        self._company_timeout_seconds = company_timeout_seconds

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
            self._failures = []
            self._cancel_requested.clear()
            self._loop = None
            self._current_task = None
            self._thread = threading.Thread(
                target=self._run,
                name="callumployed-scan-all",
                daemon=True,
            )
            self._thread.start()
            return True

    def cancel(self) -> bool:
        with self._lock:
            scanning = self._thread is not None and self._thread.is_alive()
            if not scanning:
                return False
            self._cancel_requested.set()
            self._error = "Scan cancellation requested."
            loop = self._loop
            current_task = self._current_task
        if loop is not None and current_task is not None:
            loop.call_soon_threadsafe(current_task.cancel)
        return True

    def snapshot(self) -> ScanCoordinatorSnapshot:
        with self._lock:
            scanning = self._thread is not None and self._thread.is_alive()
            return ScanCoordinatorSnapshot(
                scanning=scanning,
                cancel_requested=scanning and self._cancel_requested.is_set(),
                started_at=self._started_at,
                finished_at=self._finished_at,
                completed_companies=self._completed_companies,
                total_companies=self._total_companies,
                failed_companies=self._failed_companies,
                error=self._error,
                failures=tuple(self._failures),
            )

    def _run(self) -> None:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            with self._lock:
                self._loop = loop
            try:
                loop.run_until_complete(self._scan_all_companies())
            finally:
                loop.close()
        except Exception as error:
            with self._lock:
                self._error = str(error)
        finally:
            with self._lock:
                self._loop = None
                self._current_task = None
                self._finished_at = _now_utc()

    async def _scan_all_companies(self) -> None:
        with db.connect() as connection:
            companies = list_companies(connection)
        with self._lock:
            self._total_companies = len(companies)

        browser_profile_manager = BrowserProfileManager()
        for company in companies:
            if self._cancel_requested.is_set():
                LOGGER.info("Scan cancelled before scanning %s.", company.name)
                break
            try:
                task = asyncio.create_task(
                    run_scan_company(
                        company,
                        browser_profile_manager=browser_profile_manager,
                    )
                )
                with self._lock:
                    self._current_task = task
                await asyncio.wait_for(
                    task,
                    timeout=self._company_timeout_seconds,
                )
            except asyncio.CancelledError:
                error_message = f"Cancelled scan while scanning {company.name}."
                if company.id is not None:
                    _mark_latest_running_scan_failed(company.id, error_message)
                with self._lock:
                    self._error = error_message
                LOGGER.info(error_message)
                break
            except TimeoutError:
                error_message = (
                    f"Timed out scanning {company.name} after "
                    f"{self._company_timeout_seconds:g} seconds."
                )
                if company.id is not None:
                    _mark_latest_running_scan_failed(company.id, error_message)
                self._record_company_failure(company, error_message)
            except Exception as error:
                error_message = str(error) or error.__class__.__name__
                self._record_company_failure(company, error_message)
            finally:
                with self._lock:
                    if self._current_task is not None and self._current_task.done():
                        self._current_task = None
                    self._completed_companies += 1

    def _record_company_failure(self, company: Company, error_message: str) -> None:
        LOGGER.warning("Scan failed for %s: %s", company.name, error_message)
        failure = ScanCoordinatorFailure(
            company_id=company.id,
            company_name=company.name,
            error=error_message,
        )
        with self._lock:
            self._failed_companies += 1
            self._error = error_message
            self._failures.append(failure)
            self._failures = self._failures[-8:]


def _mark_latest_running_scan_failed(company_id: int, error_message: str) -> None:
    with db.connect() as connection:
        latest_scan_runs = list_scan_runs(connection, company_id=company_id, limit=1)
        if not latest_scan_runs:
            return
        latest_scan = latest_scan_runs[0]
        if latest_scan.id is None or latest_scan.scan_status != ScanStatus.RUNNING:
            return
        finish_scan_run(connection, latest_scan.id, ScanStatus.FAILED, error=error_message)


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
        latest_scan_ids_by_company: dict[int, int] = {}
        latest_scan_role_ids_by_company: dict[int, set[int]] = {}
        latest_scan_role_urls_by_company: dict[int, set[str]] = {}
        for company_id in {role.company_id for role in roles}:
            latest_scan_runs = list_scan_runs(connection, company_id=company_id, limit=1)
            if not latest_scan_runs or latest_scan_runs[0].id is None:
                continue
            latest_scan_run = latest_scan_runs[0]
            latest_scan_ids_by_company[company_id] = latest_scan_run.id
            latest_scan_role_ids_by_company[company_id] = {
                attempt.role_id
                for attempt in list_role_discovery_attempts(
                    connection,
                    scan_run_id=latest_scan_run.id,
                )
                if attempt.role_id is not None
            }
            latest_scan_role_urls_by_company[company_id] = {
                candidate.url
                for page in list_scan_pages(connection, latest_scan_run.id)
                if page.id is not None
                for candidate in list_scan_candidates(connection, page.id)
            }

    grouped_roles: dict[str, list[dict[str, Any]]] = {status.value: [] for status in RoleStatus}
    for role in roles:
        payload = _role_payload(role)
        latest_scan_role_ids = latest_scan_role_ids_by_company.get(role.company_id, set())
        latest_scan_role_urls = latest_scan_role_urls_by_company.get(role.company_id, set())
        seen_in_latest_scan = (
            role.id in latest_scan_role_ids or role.role_url in latest_scan_role_urls
        )
        payload["updated_in_latest_scan"] = role.id in latest_scan_role_ids
        payload["missing_from_latest_scan"] = (
            role.role_status in {RoleStatus.DISCOVERED, RoleStatus.INTERESTED}
            and role.company_id in latest_scan_ids_by_company
            and not seen_in_latest_scan
        )
        payload["prep_started"] = (
            _role_has_prep_started(role.id) if isinstance(role.id, int) else False
        )
        grouped_roles[role.role_status.value].append(payload)
    grouped_roles[RoleStatus.INTERESTED.value].sort(
        key=lambda role: bool(role.get("prep_started")),
        reverse=True,
    )
    grouped_roles[RoleStatus.CLOSED.value].sort(
        key=lambda role: bool(role["updated_in_latest_scan"]),
        reverse=True,
    )

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


def build_companies_payload() -> dict[str, Any]:
    with db.connect() as connection:
        companies = list_companies(connection)
        scan_discovery_counts = get_company_scan_discovery_counts(connection)
        career_pages_by_company_id = {
            company.id: list_company_career_pages(connection, company.id)
            for company in companies
            if company.id is not None
        }
    return {
        "companies": [
            _company_payload(
                company,
                career_pages_by_company_id.get(company.id, []) if company.id is not None else [],
                scan_discovery_counts.get(company.id, (0, 0)) if company.id is not None else (0, 0),
            )
            for company in companies
        ]
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
            if parsed_url.path == "/api/metrics":
                self._send_json(build_metrics_payload())
                return
            if parsed_url.path == "/api/role-sankey":
                self._send_json(build_role_sankey_payload())
                return
            if parsed_url.path == "/api/companies":
                self._send_json(build_companies_payload())
                return
            if parsed_url.path == "/api/master-resume":
                self._send_json(build_master_resume_payload())
                return
            if parsed_url.path == "/api/cover-letter-examples":
                self._send_json(build_cover_letter_examples_payload())
                return
            if parsed_url.path == "/api/experience-notes":
                self._send_json(build_experience_notes_payload())
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
                and path_parts[3] == "resume"
            ):
                self._send_resume(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "resume.pdf"
            ):
                self._send_resume_pdf(path_parts[2])
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
                asset_path = parsed_url.path.removeprefix("/assets/")
                asset_parts = PurePosixPath(asset_path).parts
                if not asset_parts or any(part in {"", ".", ".."} for part in asset_parts):
                    self.send_error(HTTPStatus.NOT_FOUND)
                    return
                relative_path = "/".join(asset_parts)
                content_type = _content_type_for(relative_path)
                self._send_static_file(relative_path, content_type)
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
                and path_parts[3] == "resume"
            ):
                self._generate_resume(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "chat"
            ):
                self._chat_about_role(path_parts[2])
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
                len(path_parts) == 5
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "resume"
                and path_parts[4] == "save"
            ):
                self._save_resume(path_parts[2])
                return
            if (
                len(path_parts) == 5
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "cover-letter"
                and path_parts[4] == "save"
            ):
                self._save_cover_letter(path_parts[2])
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
            if len(path_parts) == 2 and path_parts == ["api", "experience-notes"]:
                self._add_experience_note()
                return
            if len(path_parts) == 2 and path_parts == ["api", "companies"]:
                self._add_company()
                return
            if len(path_parts) == 2 and path_parts == ["api", "roles"]:
                self._add_role()
                return
            if (
                len(path_parts) == 3
                and path_parts[0] == "api"
                and path_parts[1] == "companies"
            ):
                self._update_company(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "companies"
                and path_parts[3] == "career-pages"
            ):
                self._add_company_career_page(path_parts[2])
                return
            if len(path_parts) == 2 and path_parts == ["api", "resume-resources"]:
                self._upload_resume_resource()
                return
            if len(path_parts) == 3 and path_parts == ["api", "scan", "all"]:
                self._start_scan_all()
                return
            if len(path_parts) == 3 and path_parts == ["api", "scan", "cancel"]:
                self._cancel_scan_all()
                return
            if len(path_parts) == 3 and path_parts == ["api", "central", "resolve-companies"]:
                self._resolve_central_companies()
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
            if len(path_parts) == 3 and path_parts == ["api", "app", "update"]:
                self._update_and_restart_app()
                return
            self.send_error(HTTPStatus.NOT_FOUND)

        def do_DELETE(self) -> None:
            parsed_url = urlparse(self.path)
            path_parts = [part for part in PurePosixPath(parsed_url.path).parts if part != "/"]
            if (
                len(path_parts) == 3
                and path_parts[0] == "api"
                and path_parts[1] == "companies"
            ):
                self._delete_company(path_parts[2])
                return
            if (
                len(path_parts) == 3
                and path_parts[0] == "api"
                and path_parts[1] == "company-career-pages"
            ):
                self._delete_company_career_page(path_parts[2])
                return
            self.send_error(HTTPStatus.NOT_FOUND)

        def log_message(self, format: str, *args: object) -> None:
            return

        def _send_json(self, payload: dict[str, Any]) -> None:
            self._send_json_with_status(payload, HTTPStatus.OK)

        def _send_json_with_status(self, payload: dict[str, Any], status: HTTPStatus) -> None:
            body = json.dumps(payload).encode()
            accepts_gzip = "gzip" in self.headers.get("Accept-Encoding", "").lower()
            if accepts_gzip:
                body = gzip.compress(body, compresslevel=5)
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Vary", "Accept-Encoding")
            if accepts_gzip:
                self.send_header("Content-Encoding", "gzip")
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

            self._send_json({"role": _role_payload(role)})

        def _record_review_later(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return

            try:
                with db.connect() as connection:
                    role = record_role_review_later(connection, role_id)
                    review_later_count = _role_review_later_count(connection, role_id)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return

            role_payload = _role_payload(role)
            role_payload["review_later_count"] = review_later_count
            self._send_json({"role": role_payload})

        def _add_role(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return
            try:
                raw_company_id = payload.get("company_id")
                if raw_company_id is None:
                    raise TypeError
                company_id = int(raw_company_id)
            except (TypeError, ValueError):
                self.send_error(HTTPStatus.BAD_REQUEST, "Company is required")
                return
            role_url = _optional_text(payload.get("role_url"))
            if role_url is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "Role URL is required")
                return
            try:
                with db.connect() as connection:
                    company = get_company(connection, company_id)
                    if not company.is_active:
                        self.send_error(HTTPStatus.BAD_REQUEST, "Company is deactivated")
                        return
                    role = add_role(
                        connection,
                        Role(
                            company_id=company_id,
                            title=_role_title_from_url(role_url),
                            role_url=role_url,
                        ),
                    )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Company not found")
                return
            except RuntimeError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            scan_error = None
            if role.id is not None:
                try:
                    scan = asyncio.run(
                        run_rescan_role(
                            role.id,
                            browser_profile_manager=BrowserProfileManager(),
                            update_status=True,
                        )
                    )
                    scanned_role = scan.get("role")
                    if isinstance(scanned_role, Role):
                        role = scanned_role
                except Exception as error:
                    scan_error = str(error)

            self._send_json(
                {
                    "role": _role_payload(role),
                    "tracker": build_tracker_payload(),
                    "scan_error": scan_error,
                }
            )

        def _add_company(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return
            name = _optional_text(payload.get("name"))
            if name is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "Company name is required")
                return
            notes = _optional_text(payload.get("notes"))
            prestige_tier = _optional_text(payload.get("prestige_tier"))
            if not _is_valid_company_tier(prestige_tier):
                self.send_error(HTTPStatus.BAD_REQUEST, "Company tier must be 0-4")
                return
            career_url = _optional_text(payload.get("career_url"))
            career_label = _optional_text(payload.get("career_label")) or "Main"
            with db.connect() as connection:
                company = add_company(
                    connection,
                    Company(name=name, notes=notes, prestige_tier=prestige_tier),
                )
                if career_url is not None:
                    if company.id is None:
                        raise RuntimeError("created company did not include an id")
                    add_company_career_page(
                        connection,
                        CompanyCareerPage(
                            company_id=company.id,
                            url=career_url,
                            label=career_label,
                        ),
                    )
                _try_resolve_company_with_central_store(
                    connection,
                    company,
                    career_page_urls=[career_url] if career_url is not None else [],
                )
            self._send_json(build_companies_payload())

        def _update_company(self, company_id_text: str) -> None:
            try:
                company_id = int(company_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid company ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            notes = _optional_text(payload.get("notes"))
            prestige_tier = _optional_text(payload.get("prestige_tier"))
            if not _is_valid_company_tier(prestige_tier):
                self.send_error(HTTPStatus.BAD_REQUEST, "Company tier must be 0-4")
                return
            try:
                with db.connect() as connection:
                    update_company(
                        connection,
                        company_id,
                        notes=notes,
                        prestige_tier=prestige_tier,
                    )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Company not found")
                return
            self._send_json(build_companies_payload())

        def _add_company_career_page(self, company_id_text: str) -> None:
            try:
                company_id = int(company_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid company ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            url = _optional_text(payload.get("url"))
            if url is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "Career page URL is required")
                return
            label = _optional_text(payload.get("label"))
            try:
                with db.connect() as connection:
                    get_company(connection, company_id)
                    add_company_career_page(
                        connection,
                        CompanyCareerPage(company_id=company_id, url=url, label=label),
                    )
                    company = get_company(connection, company_id)
                    _try_resolve_company_with_central_store(
                        connection,
                        company,
                        career_page_urls=[
                            page.url for page in list_company_career_pages(connection, company_id)
                        ],
                    )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Company not found")
                return
            self._send_json(build_companies_payload())

        def _delete_company(self, company_id_text: str) -> None:
            try:
                company_id = int(company_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid company ID")
                return
            try:
                with db.connect() as connection:
                    deactivate_company(connection, company_id)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Company not found")
                return
            self._send_json(build_companies_payload())

        def _delete_company_career_page(self, career_page_id_text: str) -> None:
            try:
                career_page_id = int(career_page_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid career page ID")
                return
            try:
                with db.connect() as connection:
                    delete_company_career_page(connection, career_page_id)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Career page not found")
                return
            self._send_json(build_companies_payload())

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
            feedback = payload.get("feedback_item")
            if not isinstance(feedback, dict):
                if resume is None:
                    self.send_error(HTTPStatus.BAD_REQUEST, "No master resume stored")
                    return
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
            tweak_prompt = _feedback_tweak_prompt(feedback)
            if not tweak_prompt:
                self.send_error(HTTPStatus.BAD_REQUEST, "Feedback has no actionable tweak prompt")
                return
            with db.connect() as connection:
                record_resume_feedback_history(
                    connection,
                    role=role,
                    feedback_index=feedback_index,
                    feedback=feedback,
                    response="accepted",
                    comment=_optional_comment(payload.get("comment")),
                )
            self._send_json(
                {
                    "accepted": True,
                    "feedback_index": feedback_index,
                    "tweak_prompt": tweak_prompt,
                    "role": _role_payload(role),
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

        def _send_resume(self, role_id_text: str) -> None:
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
            self._send_json(
                {
                    "resume": _saved_role_resume(
                        role.model_dump(mode="json"),
                        resume,
                        ensure_copy=True,
                    )
                }
            )

        def _save_resume(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            try:
                latex = _required_resume_latex(payload.get("latex"))
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
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
            self._send_json(
                {"resume": save_role_resume(role.model_dump(mode="json"), resume, latex)}
            )

        def _generate_resume(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            tweaks = _optional_resume_tweaks(payload.get("tweaks"))
            if tweaks is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "Resume tweaks are required")
                return
            previous_latex = _optional_resume_latex(payload.get("previous_latex"))
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
                generated_resume = build_role_resume(
                    role_payload,
                    resume,
                    tweaks=tweaks,
                    previous_latex=previous_latex,
                )
            except RuntimeError as error:
                self._send_json_with_status(
                    {"error": str(error)},
                    HTTPStatus.SERVICE_UNAVAILABLE,
                )
                return
            self._send_json({"resume": generated_resume})

        def _chat_about_role(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            try:
                messages = parse_role_chat_messages(payload.get("messages"))
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return
            try:
                chat_context = build_role_chat_context(role_id)
                response = asyncio.run(
                    generate_role_chat(
                        role=chat_context["role"],
                        resume_content=chat_context["resume_content"],
                        cover_letter_content=chat_context["cover_letter_content"],
                        employment_history_context=chat_context[
                            "employment_history_context"
                        ],
                        messages=messages,
                    )
                )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            except Exception as error:  # noqa: BLE001 - chat should fail cleanly.
                self._send_json_with_status(
                    {"error": str(error) or "Role chat unavailable"},
                    HTTPStatus.SERVICE_UNAVAILABLE,
                )
                return
            self._send_json({"message": {"role": "assistant", "content": response.answer}})

        def _send_resume_pdf(self, role_id_text: str) -> None:
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
            resume_payload = _saved_role_resume(
                role.model_dump(mode="json"),
                resume,
                ensure_copy=True,
            )
            pdf_path_text = resume_payload.get("pdf_path")
            if not isinstance(pdf_path_text, str):
                self.send_error(HTTPStatus.NOT_FOUND, "Resume PDF not found")
                return
            self._send_pdf_file(
                Path(pdf_path_text),
                filename=_role_material_pdf_filename(role_id, kind="resume"),
            )

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
            previous_latex = None
            if tweaks:
                previous_latex = _optional_cover_letter_latex(payload.get("previous_latex"))
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
                cover_letter = build_role_cover_letter(
                    role_payload,
                    resume,
                    tweaks=tweaks,
                    previous_cover_letter_latex=previous_latex,
                )
            except RuntimeError as error:
                self._send_json_with_status(
                    {"error": str(error)},
                    HTTPStatus.SERVICE_UNAVAILABLE,
                )
                return
            self._send_json({"cover_letter": cover_letter})

        def _save_cover_letter(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            try:
                latex = _required_cover_letter_latex(payload.get("latex"))
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return
            try:
                with db.connect() as connection:
                    role = get_role(connection, role_id)
                    company = get_company(connection, role.company_id)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            role_payload = role.model_dump(mode="json")
            role_payload["company_name"] = company.name
            try:
                cover_letter = save_role_cover_letter(role_payload, latex)
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
            self._send_pdf_file(
                pdf_path,
                filename=_role_material_pdf_filename(role_id, kind="cover_letter"),
            )

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
                    interested_roles = list_roles(
                        connection,
                        role_status=RoleStatus.INTERESTED,
                    )
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            updated_count = _replace_role_resumes(interested_roles, resume)
            self._send_json(
                {
                    "master_resume": _master_resume_summary(resume),
                    "interested_resumes_updated": updated_count,
                }
            )

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

        def _add_experience_note(self) -> None:
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
                    note = add_experience_note(
                        connection,
                        filename=filename,
                        content=content,
                    )
                    notes = list_experience_notes(connection)
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            self._send_json(
                {
                    "experience_note": _experience_note_summary(note),
                    "experience_notes": [_experience_note_summary(item) for item in notes],
                }
            )

        def _start_scan_all(self) -> None:
            started = SCAN_COORDINATOR.start()
            status = HTTPStatus.ACCEPTED if started else HTTPStatus.CONFLICT
            self._send_json_with_status(build_scan_status_payload(), status)

        def _cancel_scan_all(self) -> None:
            cancelled = SCAN_COORDINATOR.cancel()
            status = HTTPStatus.ACCEPTED if cancelled else HTTPStatus.CONFLICT
            self._send_json_with_status(build_scan_status_payload(), status)

        def _update_config(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return

            allowed_keys = {
                APPLICANT_FIRST_NAME_CONFIG_KEY,
                APPLICANT_LAST_NAME_CONFIG_KEY,
                *APPLICANT_PROFILE_TEXT_CONFIG_KEYS,
                "central_api_url",
                "central_passkey",
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
                    db.run_migrations(connection)
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
                    if APPLICANT_FIRST_NAME_CONFIG_KEY in payload:
                        set_config_value(
                            connection,
                            APPLICANT_FIRST_NAME_CONFIG_KEY,
                            _clean_applicant_name_part(
                                payload[APPLICANT_FIRST_NAME_CONFIG_KEY]
                            ),
                        )
                    if APPLICANT_LAST_NAME_CONFIG_KEY in payload:
                        set_config_value(
                            connection,
                            APPLICANT_LAST_NAME_CONFIG_KEY,
                            _clean_applicant_name_part(
                                payload[APPLICANT_LAST_NAME_CONFIG_KEY]
                            ),
                        )
                    for key in APPLICANT_PROFILE_TEXT_CONFIG_KEYS:
                        if key in payload:
                            set_config_value(
                                connection,
                                key,
                                _clean_applicant_profile_text(key, payload[key]),
                            )
                    if "central_api_url" in payload:
                        set_central_api_url(connection, payload["central_api_url"])
                    central_passkey = _optional_text(payload.get("central_passkey"))
                    if central_passkey is not None:
                        set_central_passkey(central_passkey)
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return
            except Exception as error:
                self.send_error(HTTPStatus.SERVICE_UNAVAILABLE, str(error))
                return

            self._send_json(build_config_payload())

        def _resolve_central_companies(self) -> None:
            try:
                with db.connect() as connection:
                    client = _central_client_from_web_config(connection)
                    result = resolve_unlinked_companies(connection, client)
                    pulled_companies = (
                        pull_companies(connection, client)
                        if get_central_passkey() is not None
                        else None
                    )
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return
            except CentralStoreError as error:
                self.send_error(HTTPStatus.SERVICE_UNAVAILABLE, str(error))
                return
            self._send_json(
                {
                    "result": {
                        "linked": result.linked,
                        "created": result.created,
                        "needs_review": result.needs_review,
                        "failed": result.failed,
                    },
                    "pulled_companies": (
                        {
                            "created": pulled_companies.companies_created,
                            "linked": pulled_companies.companies_linked,
                            "existing": pulled_companies.companies_existing,
                        }
                        if pulled_companies is not None
                        else None
                    ),
                    "config": build_config_payload(),
                    "companies": build_companies_payload(),
                }
            )

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

        def _update_and_restart_app(self) -> None:
            host = str(getattr(self.server, "server_name", "127.0.0.1"))
            port = int(getattr(self.server, "server_port", 8765))
            try:
                _start_update_and_restart(host=host, port=port)
            except OSError:
                self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Could not start updater")
                return
            self._send_json_with_status(
                {"message": "update started; callumployed will restart shortly"},
                HTTPStatus.ACCEPTED,
            )
            threading.Thread(target=_shutdown_server, args=(self.server,), daemon=True).start()

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
        latest_scan_runs = list_scan_runs(connection, limit=8)
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
    recent_failed_scans = [
        scan
        for scan in latest_scan_runs
        if scan.scan_status == ScanStatus.FAILED and scan.error
    ][:5]
    return {
        "scanning": snapshot.scanning,
        "cancel_requested": snapshot.cancel_requested,
        "started_at": _datetime_or_none(snapshot.started_at),
        "finished_at": _datetime_or_none(snapshot.finished_at),
        "last_scan_at": _datetime_or_none(last_scan_at),
        "completed_companies": snapshot.completed_companies,
        "total_companies": snapshot.total_companies,
        "failed_companies": snapshot.failed_companies,
        "error": snapshot.error,
        "failures": [
            {
                "company_id": failure.company_id,
                "company_name": failure.company_name,
                "error": failure.error,
            }
            for failure in snapshot.failures
        ]
        or [
            {
                "company_id": scan.company_id,
                "company_name": scan.company_name,
                "error": scan.error,
            }
            for scan in recent_failed_scans
        ],
        "latest_scan": (
            {
                "id": latest_scan.id,
                "company_id": latest_scan.company_id,
                "company_name": latest_scan.company_name,
                "scan_status": latest_scan_status.value if latest_scan_status else None,
                "started_at": _datetime_or_none(latest_started_at),
                "finished_at": _datetime_or_none(latest_finished_at),
                "error": latest_scan.error,
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
        applicant_first_name = get_config_value(
            connection,
            APPLICANT_FIRST_NAME_CONFIG_KEY,
        ) or ""
        applicant_last_name = get_config_value(
            connection,
            APPLICANT_LAST_NAME_CONFIG_KEY,
        ) or ""
        applicant_email = get_config_value(connection, APPLICANT_EMAIL_CONFIG_KEY) or ""
        applicant_institution = (
            get_config_value(connection, APPLICANT_INSTITUTION_CONFIG_KEY) or ""
        )
        applicant_degree = get_config_value(connection, APPLICANT_DEGREE_CONFIG_KEY) or ""
        recommendation_history_count = count_resume_feedback_history(connection)
        central_api_url = get_central_api_url(connection)
        companies = list_companies(connection, include_inactive=True)
    passkey_configured = get_central_passkey() is not None
    central_linked_count = sum(company.central_company_id is not None for company in companies)
    central_unlinked_count = sum(company.central_company_id is None for company in companies)
    central_needs_review_count = sum(
        company.central_sync_status == "needs_review" for company in companies
    )
    central_failed_count = sum(company.central_sync_status == "failed" for company in companies)
    return {
        "values": values,
        "recommendation_history_count": recommendation_history_count,
        "central": {
            "api_url": central_api_url,
            "passkey_configured": passkey_configured,
            "companies_linked": central_linked_count,
            "companies_unlinked": central_unlinked_count,
            "companies_needs_review": central_needs_review_count,
            "companies_failed": central_failed_count,
        },
        "settings": [
            {
                "key": APPLICANT_FIRST_NAME_CONFIG_KEY,
                "label": "first name",
                "description": "used in generated documents and saved PDF filenames",
                "control": "text",
                "value": applicant_first_name,
                "default": "",
                "editable": True,
            },
            {
                "key": APPLICANT_LAST_NAME_CONFIG_KEY,
                "label": "last name",
                "description": "used in generated documents and saved PDF filenames",
                "control": "text",
                "value": applicant_last_name,
                "default": "",
                "editable": True,
            },
            {
                "key": APPLICANT_EMAIL_CONFIG_KEY,
                "label": "email",
                "description": "used in the cover letter sender block",
                "control": "text",
                "input_type": "email",
                "autocomplete": "email",
                "value": applicant_email,
                "default": "",
                "editable": True,
            },
            {
                "key": APPLICANT_INSTITUTION_CONFIG_KEY,
                "label": "institution",
                "description": "school or university used in cover letters",
                "control": "text",
                "autocomplete": "organization",
                "value": applicant_institution,
                "default": "",
                "editable": True,
            },
            {
                "key": APPLICANT_DEGREE_CONFIG_KEY,
                "label": "degree / program",
                "description": "education description used in cover letters",
                "control": "text",
                "autocomplete": "off",
                "value": applicant_degree,
                "default": "",
                "editable": True,
            },
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


def build_metrics_payload() -> dict[str, Any]:
    with db.connect() as connection:
        db.run_migrations(connection)
        tracking_stats = get_tracking_stats(connection)
        company_counts = _query_count_by_value(
            connection,
            "SELECT is_active AS value, COUNT(*) AS count FROM companies GROUP BY is_active",
        )
        scan_status_counts = _query_count_by_value(
            connection,
            "SELECT scan_status AS value, COUNT(*) AS count FROM scan_runs GROUP BY scan_status",
        )
        candidate_selected_counts = _query_count_by_value(
            connection,
            "SELECT selected AS value, COUNT(*) AS count FROM scan_candidates GROUP BY selected",
        )
        candidate_method_counts = _query_count_by_value(
            connection,
            """
            SELECT COALESCE(discovery_method, 'rejected') AS value, COUNT(*) AS count
            FROM scan_candidates
            GROUP BY COALESCE(discovery_method, 'rejected')
            """,
        )
        attempt_status_counts = _query_count_by_value(
            connection,
            """
            SELECT status AS value, COUNT(*) AS count
            FROM role_discovery_attempts
            GROUP BY status
            """,
        )
        extraction_method_counts = _query_count_by_value(
            connection,
            """
            SELECT COALESCE(assessment_extraction_method, 'unknown') AS value, COUNT(*) AS count
            FROM role_discovery_attempts
            GROUP BY COALESCE(assessment_extraction_method, 'unknown')
            """,
        )
        latest_scan_runs = list_scan_runs(connection, limit=8)

        scan_pages_total = _query_count(connection, "SELECT COUNT(*) AS count FROM scan_pages")
        candidates_total = _query_count(
            connection,
            "SELECT COUNT(*) AS count FROM scan_candidates",
        )
        candidates_scanned_total = _query_count(
            connection,
            "SELECT COALESCE(SUM(candidates_scanned), 0) AS count FROM scan_pages",
        )
        role_attempts_total = _query_count(
            connection,
            "SELECT COUNT(*) AS count FROM role_discovery_attempts",
        )
        role_attempts_accepted = _query_count(
            connection,
            """
            SELECT COUNT(*) AS count
            FROM role_discovery_attempts
            WHERE assessment_is_role = 1 AND COALESCE(assessment_is_closed, 0) = 0
            """,
        )
        role_attempts_rejected = _query_count(
            connection,
            """
            SELECT COUNT(*) AS count
            FROM role_discovery_attempts
            WHERE assessment_is_role = 0 OR assessment_is_closed = 1
            """,
        )
        visit_failures = _query_count(
            connection,
            "SELECT COUNT(*) AS count FROM role_discovery_attempts WHERE status = 'failed'",
        )
        llm_link_classifications = _query_count(
            connection,
            """
            SELECT COUNT(*) AS count
            FROM scan_candidates
            WHERE discovery_method IN ('agent', 'heuristic+agent')
            """,
        )
        llm_role_assessments = _query_count(
            connection,
            """
            SELECT COUNT(*) AS count
            FROM role_discovery_attempts
            WHERE assessment_extraction_method = 'llm'
            """,
        )
        scan_runs_with_agent_trace = _query_count(
            connection,
            """
            SELECT COUNT(*) AS count
            FROM scan_runs
            WHERE agent_trace IS NOT NULL AND TRIM(agent_trace) != ''
            """,
        )
        resume_feedback_decisions = count_resume_feedback_history(connection)
        average_candidate_confidence = _query_float(
            connection,
            "SELECT AVG(confidence) AS value FROM scan_candidates",
        )
        average_assessment_confidence = _query_float(
            connection,
            "SELECT AVG(assessment_confidence) AS value FROM role_discovery_attempts",
        )

    accepted_links = candidate_selected_counts.get("1", 0)
    rejected_links = candidate_selected_counts.get("0", 0)
    total_scan_runs = sum(scan_status_counts.values())
    failed_scan_runs = scan_status_counts.get(ScanStatus.FAILED.value, 0)
    succeeded_scan_runs = scan_status_counts.get(ScanStatus.SUCCEEDED.value, 0)
    running_scan_runs = scan_status_counts.get(ScanStatus.RUNNING.value, 0)
    ai_total = llm_link_classifications + llm_role_assessments + scan_runs_with_agent_trace

    return {
        "updated_at": _datetime_or_none(datetime.now(UTC)),
        "overview": [
            _metric("active companies", tracking_stats["companies_total"]),
            _metric("inactive companies", company_counts.get("0", 0)),
            _metric("tracked roles", tracking_stats["jobs_total"]),
            _metric("applications", tracking_stats["applications_total"]),
            _metric("scan runs", total_scan_runs),
            _metric("accepted links", accepted_links),
            _metric("rejected links", rejected_links),
            _metric("ai-assisted items", ai_total),
        ],
        "sections": [
            {
                "title": "scan runs",
                "metrics": [
                    _metric("total", total_scan_runs),
                    _metric("succeeded", succeeded_scan_runs),
                    _metric("failed", failed_scan_runs),
                    _metric("running", running_scan_runs),
                    _metric("pages scanned", scan_pages_total),
                    _metric("candidate observations", candidates_scanned_total),
                ],
            },
            {
                "title": "candidate links",
                "metrics": [
                    _metric("stored candidates", candidates_total),
                    _metric("accepted", accepted_links),
                    _metric("rejected", rejected_links),
                    _metric("avg confidence", average_candidate_confidence, kind="ratio"),
                ],
            },
            {
                "title": "role visits",
                "metrics": [
                    _metric("attempts", role_attempts_total),
                    _metric("accepted roles", role_attempts_accepted),
                    _metric("rejected after visit", role_attempts_rejected),
                    _metric("visit failures", visit_failures),
                    _metric(
                        "avg assessment confidence",
                        average_assessment_confidence,
                        kind="ratio",
                    ),
                ],
            },
            {
                "title": "ai usage",
                "metrics": [
                    _metric("agent-selected links", llm_link_classifications),
                    _metric("llm role assessments", llm_role_assessments),
                    _metric("scan runs with agent trace", scan_runs_with_agent_trace),
                    _metric("feedback decisions saved", resume_feedback_decisions),
                ],
            },
            {
                "title": "role statuses",
                "metrics": [
                    _metric(STATUS_LABELS.get(status, status), count)
                    for status, count in dict(tracking_stats["jobs_by_status"]).items()
                ],
            },
            {
                "title": "application statuses",
                "metrics": [
                    _metric(STATUS_LABELS.get(status, status), count)
                    for status, count in dict(tracking_stats["applications_by_status"]).items()
                ],
            },
            {
                "title": "candidate methods",
                "metrics": [
                    _metric(method, count)
                    for method, count in sorted(candidate_method_counts.items())
                ],
            },
            {
                "title": "assessment methods",
                "metrics": [
                    _metric(method, count)
                    for method, count in sorted(extraction_method_counts.items())
                ],
            },
            {
                "title": "attempt statuses",
                "metrics": [
                    _metric(status, count)
                    for status, count in sorted(attempt_status_counts.items())
                ],
            },
        ],
        "recent_scans": [
            {
                "id": scan.id,
                "company_id": scan.company_id,
                "company_name": scan.company_name,
                "scan_status": scan.scan_status.value,
                "started_at": _datetime_or_none(scan.started_at),
                "finished_at": _datetime_or_none(scan.finished_at),
                "error": scan.error,
            }
            for scan in latest_scan_runs
        ],
    }


def build_role_sankey_payload() -> dict[str, Any]:
    with db.connect() as connection:
        db.run_migrations(connection)
        role_rows = connection.execute(
            """
            SELECT
                roles.id,
                roles.title,
                roles.role_status,
                companies.name AS company_name
            FROM roles
            JOIN companies ON companies.id = roles.company_id
            WHERE roles.role_status != 'archived'
            ORDER BY roles.updated_at DESC, roles.id DESC
            """
        ).fetchall()
        event_rows = connection.execute(
            """
            SELECT role_id, old_status, new_status, created_at, id
            FROM events
            WHERE event_type = 'status_changed'
                AND role_id IS NOT NULL
                AND new_status IS NOT NULL
            ORDER BY role_id, created_at, id
            """
        ).fetchall()

    events_by_role_id: dict[int, list[dict[str, Any]]] = {}
    for row in event_rows:
        role_id = int(row["role_id"])
        events_by_role_id.setdefault(role_id, []).append(dict(row))

    link_counts: dict[tuple[str, str], int] = {}
    path_counts: dict[tuple[str, ...], int] = {}
    status_counts: dict[str, int] = {}
    history_status_counts: dict[str, int] = {}
    paths: list[dict[str, Any]] = []
    for row in role_rows:
        role_id = int(row["id"])
        current_status = str(row["role_status"])
        status_counts[current_status] = status_counts.get(current_status, 0) + 1
        history = _role_status_history(
            events_by_role_id.get(role_id, []),
            current_status=current_status,
        )
        collapsed_history = _collapse_status_loops(history)
        for status in set(collapsed_history):
            history_status_counts[status] = history_status_counts.get(status, 0) + 1
        path_key = tuple(collapsed_history)
        path_counts[path_key] = path_counts.get(path_key, 0) + 1
        for source, target in zip(collapsed_history, collapsed_history[1:], strict=False):
            link_counts[(source, target)] = link_counts.get((source, target), 0) + 1
        paths.append(
            {
                "role_id": role_id,
                "company_name": row["company_name"],
                "title": row["title"],
                "current_status": current_status,
                "path": collapsed_history,
                "loops_collapsed": max(0, len(history) - len(collapsed_history)),
            }
        )

    node_statuses = set(status_counts)
    for source, target in link_counts:
        node_statuses.add(source)
        node_statuses.add(target)

    ordered_statuses = [status.value for status in RoleStatus if status.value in node_statuses]
    ordered_statuses.extend(sorted(node_statuses.difference(ordered_statuses)))

    return {
        "updated_at": _datetime_or_none(datetime.now(UTC)),
        "role_count": len(role_rows),
        "nodes": [
            {
                "id": status,
                "label": STATUS_LABELS.get(status, status),
                "current_count": status_counts.get(status, 0),
                "history_count": history_status_counts.get(status, 0),
            }
            for status in ordered_statuses
        ],
        "links": [
            {"source": source, "target": target, "value": count}
            for (source, target), count in sorted(
                link_counts.items(),
                key=lambda item: (
                    ordered_statuses.index(item[0][0])
                    if item[0][0] in ordered_statuses
                    else len(ordered_statuses),
                    ordered_statuses.index(item[0][1])
                    if item[0][1] in ordered_statuses
                    else len(ordered_statuses),
                ),
            )
        ],
        "path_counts": [
            {"path": list(path), "value": count}
            for path, count in sorted(
                path_counts.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ],
        "paths": paths[:12],
    }


def _role_status_history(
    events: list[dict[str, Any]],
    *,
    current_status: str,
) -> list[str]:
    if not events:
        return [current_status]
    first_old_status = events[0].get("old_status")
    history = [str(first_old_status)] if first_old_status else []
    for event in events:
        new_status = event.get("new_status")
        if new_status is not None:
            history.append(str(new_status))
    if not history or history[-1] != current_status:
        history.append(current_status)
    return history


def _collapse_status_loops(history: list[str]) -> list[str]:
    collapsed: list[str] = []
    seen_indexes: dict[str, int] = {}
    for status in history:
        if status in seen_indexes:
            loop_start = seen_indexes[status]
            for removed_status in collapsed[loop_start + 1 :]:
                seen_indexes.pop(removed_status, None)
            collapsed = collapsed[: loop_start + 1]
            continue
        seen_indexes[status] = len(collapsed)
        collapsed.append(status)
    return collapsed


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


def build_experience_notes_payload() -> dict[str, Any]:
    with db.connect() as connection:
        notes = list_experience_notes(connection)
    return {"experience_notes": [_experience_note_summary(note) for note in notes]}


def build_application_materials_payload() -> dict[str, Any]:
    with db.connect() as connection:
        resume = get_master_resume(connection)
        examples = list_cover_letter_examples(connection)
        notes = list_experience_notes(connection)
    return _application_materials_payload(resume, examples, notes)


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
                experience_notes = list_experience_notes(connection)
            response = asyncio.run(
                evaluate_resume_feedback(
                    role=role,
                    resume_content=resume.content,
                    knowledge_base=knowledge_base,
                    other_experience_context=[
                        _experience_note_context(note) for note in experience_notes
                    ],
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
                "tweak_prompt": None,
            }
        )
    if not description.strip():
        feedback_items.append(
            {
                "label": "refresh_context",
                "title": "refresh job context: saved description is missing",
                "detail": "rescan or open the role page so the prep view has full job context.",
                "tweak_prompt": None,
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
                "tweak_prompt": (
                    "Revise the resume to foreground the existing experience that supports "
                    f"{', '.join(matched_terms[:5])} for this role. Keep the current LaTeX "
                    "structure and do not add unsupported claims."
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
                "tweak_prompt": None,
            }
        )
    feedback_items.append(
        {
            "label": "move_emphasis",
            "title": "move emphasis earlier: strongest company-relevant project",
            "detail": "move the most relevant project or skill cluster higher in the resume.",
            "tweak_prompt": (
                "If a project or experience already in the resume is clearly the strongest "
                "match for this role, move that emphasis earlier while preserving the current "
                "section style."
            )
            if resume is not None and description.strip()
            else None,
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
    previous_cover_letter_latex: str | None = None,
) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")

    applicant_profile = ApplicantProfile()
    experience_notes: list[ExperienceNote] = []

    def search_cover_letters(query: str, *, limit: int = 3) -> list[dict[str, object]]:
        with db.connect() as connection:
            db.run_migrations(connection)
            matches = list_cover_letter_example_knowledge(
                connection,
                query=query,
                limit=limit,
            )
        return matches

    try:
        with db.connect() as connection:
            db.run_migrations(connection)
            experience_notes = list_experience_notes(connection)
            applicant_profile = _load_applicant_profile(connection)
        draft = asyncio.run(
            generate_cover_letter(
                role=role,
                resume_content=resume.content,
                search_tool=search_cover_letters,
                applicant_profile=applicant_profile,
                other_experience_context=[
                    _experience_note_context(note) for note in experience_notes
                ],
                tweaks=tweaks,
                previous_cover_letter_latex=previous_cover_letter_latex,
            )
        )
        latex = _normalize_cover_letter_latex(draft.latex)
        example_ids = draft.example_ids
        source = "ai_cover_letter"
    except Exception:  # noqa: BLE001 - prep should degrade when the LLM is unavailable.
        latex = _normalize_cover_letter_latex(
            _fallback_cover_letter_latex(
                role,
                resume,
                applicant_profile=applicant_profile,
                other_experience_context=[
                    _experience_note_context(note) for note in experience_notes
                ],
            )
        )
        example_ids = []
        source = "local_cover_letter_fallback"

    return _write_role_cover_letter(
        role,
        latex,
        source=source,
        example_ids=example_ids,
        tweaks=tweaks,
    )


def _load_applicant_profile(connection: Any) -> ApplicantProfile:
    return ApplicantProfile(
        first_name=get_config_value(connection, APPLICANT_FIRST_NAME_CONFIG_KEY) or "",
        last_name=get_config_value(connection, APPLICANT_LAST_NAME_CONFIG_KEY) or "",
        email=get_config_value(connection, APPLICANT_EMAIL_CONFIG_KEY) or "",
        institution=get_config_value(connection, APPLICANT_INSTITUTION_CONFIG_KEY) or "",
        degree=get_config_value(connection, APPLICANT_DEGREE_CONFIG_KEY) or "",
    )


def save_role_cover_letter(role: dict[str, Any], latex: str) -> dict[str, Any]:
    return _write_role_cover_letter(
        role,
        _normalize_cover_letter_latex(latex),
        source="edited_cover_letter",
        example_ids=[],
        tweaks=None,
    )


def save_role_resume(role: dict[str, Any], resume: MasterResume, latex: str) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")
    resume_path = _ensure_role_resume_copy(role_id, resume)
    resume_path.write_text(latex)
    _sync_resume_resources_to_role(role_id)
    with suppress(RuntimeError):
        _generate_role_resume_pdf(role, resume, copy_to_downloads=False)
    return _saved_role_resume(role, resume)


def build_role_resume(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    tweaks: str,
    previous_latex: str | None = None,
) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")
    source_latex = previous_latex or _ensure_role_resume_copy(role_id, resume).read_text()
    try:
        with db.connect() as connection:
            db.run_migrations(connection)
            experience_notes = list_experience_notes(connection)
        draft = asyncio.run(
            generate_resume_tweak(
                role=role,
                resume_content=source_latex,
                tweaks=tweaks,
                other_experience_context=[
                    _experience_note_context(note) for note in experience_notes
                ],
            )
        )
    except Exception as error:  # noqa: BLE001 - surface a concise UI failure.
        raise RuntimeError("AI resume regeneration was unavailable.") from error
    generated = save_role_resume(role, resume, draft.latex)
    return {
        **generated,
        "summary": draft.summary or "Regenerated resume with tweaks.",
        "tweaks": tweaks,
    }


def build_role_chat_context(role_id: int) -> dict[str, Any]:
    with db.connect() as connection:
        role = get_role(connection, role_id)
        company = get_company(connection, role.company_id)
        resume = get_master_resume(connection)
        experience_notes = list_experience_notes(connection)

    role_payload = role.model_dump(mode="json")
    role_payload["company_name"] = company.name
    resume_content = ""
    if resume is not None:
        role_resume_path = _role_resume_tex_path(role_id)
        resume_content = (
            role_resume_path.read_text() if role_resume_path.exists() else resume.content
        )
    cover_letter_path = _role_cover_letter_tex_path(role_id)
    cover_letter_content = cover_letter_path.read_text() if cover_letter_path.exists() else ""
    return {
        "role": role_payload,
        "resume_content": resume_content,
        "cover_letter_content": cover_letter_content,
        "employment_history_context": [
            _experience_note_context(note) for note in experience_notes
        ],
    }


def _write_role_cover_letter(
    role: dict[str, Any],
    latex: str,
    *,
    source: str,
    example_ids: list[int],
    tweaks: str | None,
) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")
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
    return strip_cover_letter_dash_punctuation(latex)


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
    lines: list[str] = []
    for line in latex.splitlines():
        normalized = line.lower()
        has_personal_site = any(
            marker in normalized
            for marker in ("http://", "https://", r"\url{", r"\href{http")
        )
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
        r"\\signature\{(?P<name>[^{}]*)\}.*?"
        r"(?=\\setlength\{\\parskip\}|\\begin\{document\})",
        lambda match: f"\\signature{{{match.group('name').strip()}}}\n",
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


def _saved_role_resume(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    ensure_copy: bool = False,
) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")
    resume_path = (
        _ensure_role_resume_copy(role_id, resume)
        if ensure_copy
        else _role_resume_tex_path(role_id)
    )
    if not resume_path.exists():
        return {
            "role_id": role_id,
            "source": "role_resume",
            "summary": "No role resume saved yet.",
            "latex": "",
            "path": str(resume_path),
            "pdf_path": None,
            "pdf_base64": None,
        }
    _sync_resume_resources_to_role(role_id)
    pdf_path = _current_role_resume_pdf_path(resume_path)
    pdf_is_stale = bool(pdf_path and pdf_path.stat().st_mtime < resume_path.stat().st_mtime)
    if pdf_path is None or pdf_is_stale:
        with suppress(RuntimeError):
            pdf_path = _generate_role_resume_pdf(role, resume, copy_to_downloads=False)
    pdf_is_current = bool(
        pdf_path and pdf_path.exists() and pdf_path.stat().st_mtime >= resume_path.stat().st_mtime
    )
    return {
        "role_id": role_id,
        "source": "role_resume",
        "summary": "Saved resume for this role.",
        "latex": resume_path.read_text(),
        "path": str(resume_path),
        "pdf_path": str(pdf_path) if pdf_is_current else None,
        "pdf_base64": (
            base64.b64encode(pdf_path.read_bytes()).decode()
            if pdf_is_current and pdf_path
            else None
        ),
    }


def _role_has_prep_started(role_id: int) -> bool:
    return _role_prep_file_has_content(_role_resume_tex_path(role_id)) or (
        _role_prep_file_has_content(_role_cover_letter_tex_path(role_id))
    )


def _role_prep_file_has_content(path: Path) -> bool:
    try:
        return path.exists() and bool(path.read_text().strip())
    except OSError:
        return False


def _current_role_resume_pdf_path(resume_path: Path) -> Path | None:
    candidates = [
        resume_path.with_suffix(".pdf"),
        resume_path.with_name("resume-tectonic.pdf"),
    ]
    existing = [path for path in candidates if path.exists()]
    if not existing:
        return None
    return max(existing, key=lambda path: path.stat().st_mtime)


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
    if source == "edited_cover_letter":
        return f"Saved edited cover letter for {role_label}."
    if example_count > 0:
        examples = f"{example_count} stored cover letter example"
        if example_count != 1:
            examples += "s"
        return (
            f"Drafted cover letter for {role_label} using resume, "
            f"job description, and {examples}."
        )
    return f"Drafted cover letter for {role_label} using resume and job description."


def _fallback_cover_letter_latex(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    applicant_profile: ApplicantProfile,
    other_experience_context: list[dict[str, Any]] | None = None,
) -> str:
    title = str(role.get("title") or "this role")
    company = str(role.get("company_name") or "your team")
    description = str(role.get("description") or "")
    experience_text = " ".join(
        str(item.get("content") or "") for item in other_experience_context or []
    )
    resume_terms = sorted(_prep_keywords(" ".join([resume.content, experience_text])))
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
        f"{applicant_profile.latex_sender_block}\\\\[12pt]\n"
        f"\\begin{{letter}}{{{company}}}\n"
        "\\opening{Dear Hiring Team,}\n\n"
        f"I am excited to apply for the {title} position at {company}. "
        f"{match_sentence} "
        "I would welcome the opportunity to contribute to the team and tailor my "
        "experience to the needs of this posting.\n\n"
        f"\\closing{{Sincerely,\\\\{applicant_profile.full_name}}}\n"
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


def _optional_text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _clean_applicant_name_part(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("Applicant name values must be text")
    cleaned = re.sub(r"[^A-Za-z]", "", value)
    if len(cleaned) > 80:
        raise ValueError("Applicant name values are too long")
    return cleaned


def _clean_applicant_profile_text(key: str, value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("Applicant profile values must be text")
    cleaned = " ".join(value.split())
    if len(cleaned) > 300:
        raise ValueError("Applicant profile values are too long")
    if key == APPLICANT_EMAIL_CONFIG_KEY and cleaned:
        local_part, separator, domain = cleaned.partition("@")
        if not separator or not local_part or "." not in domain:
            raise ValueError("Applicant email must be a valid email address")
    return cleaned


def _is_valid_company_tier(value: str | None) -> bool:
    return value is None or value in {"0", "1", "2", "3", "4"}


def _optional_cover_letter_tweaks(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _optional_cover_letter_latex(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _optional_resume_tweaks(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _optional_resume_latex(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _required_cover_letter_latex(value: object) -> str:
    latex = _optional_cover_letter_latex(value)
    if latex is None:
        raise ValueError("Expected cover letter LaTeX")
    return latex


def _required_resume_latex(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected resume LaTeX")
    return value


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


def _replace_role_resumes(roles: list[Role], resume: MasterResume) -> int:
    updated_count = 0
    for role in roles:
        if role.id is None:
            continue
        resume_dir = _role_resume_dir(role.id)
        resume_dir.mkdir(parents=True, exist_ok=True)
        _role_resume_tex_path(role.id).write_text(resume.content)
        _sync_resume_resources_to_role(role.id)
        updated_count += 1
    return updated_count


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


def _feedback_tweak_prompt(feedback: dict[str, Any]) -> str | None:
    tweak_prompt = feedback.get("tweak_prompt")
    if not isinstance(tweak_prompt, str):
        return None
    stripped = tweak_prompt.strip()
    return stripped or None


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


def _generate_role_resume_pdf(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    copy_to_downloads: bool = True,
) -> Path:
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
            copy_to_downloads=copy_to_downloads,
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
            copy_to_downloads=copy_to_downloads,
        )


def _compile_role_resume_pdf(
    *,
    role: dict[str, Any],
    role_id: int,
    compiler: str,
    resume_path: Path,
    copy_to_downloads: bool = True,
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

    if not copy_to_downloads:
        return generated_pdf

    downloads_dir = Path.home() / "Downloads"
    target_path = downloads_dir / _role_material_pdf_filename(role_id, kind="resume")
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


def _role_material_pdf_filename(role_id: int, *, kind: str) -> str:
    suffix = "Resume" if kind == "resume" else "CL"
    return f"{_applicant_pdf_filename_prefix()}{suffix}{role_id}.pdf"


def _applicant_pdf_filename_prefix() -> str:
    try:
        with db.connect() as connection:
            db.run_migrations(connection)
            first_name = get_config_value(connection, APPLICANT_FIRST_NAME_CONFIG_KEY) or ""
            last_name = get_config_value(connection, APPLICANT_LAST_NAME_CONFIG_KEY) or ""
    except Exception:  # noqa: BLE001 - filename generation should not block PDF serving.
        first_name = ""
        last_name = ""
    prefix = (
        _clean_applicant_name_part(first_name)
        + _clean_applicant_name_part(last_name)
    )
    return prefix or "Applicant"


def _application_materials_payload(
    resume: MasterResume | None,
    examples: list[CoverLetterExample],
    notes: list[ExperienceNote],
) -> dict[str, Any]:
    resume_resources = _list_resume_resources()
    has_missing_required_materials = (
        resume is None or len(examples) == 0 or len(notes) == 0
    )
    return {
        "master_resume": _master_resume_summary(resume) if resume else None,
        "cover_letter_examples": [
            _cover_letter_example_summary(example) for example in examples
        ],
        "experience_notes": [_experience_note_summary(note) for note in notes],
        "resume_resources": resume_resources,
        "ui": {
            "default_collapsed": not has_missing_required_materials,
            "has_missing_required_materials": has_missing_required_materials,
            "has_master_resume": resume is not None,
            "cover_letter_example_count": len(examples),
            "experience_note_count": len(notes),
            "resume_resource_count": len(resume_resources),
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


def _experience_note_summary(note: ExperienceNote) -> dict[str, Any]:
    return {
        "id": note.id,
        "filename": note.filename,
        "content_sha256": note.content_sha256,
        "content_bytes": len(note.content.encode()),
        "created_at": note.created_at.isoformat() if note.created_at else None,
        "updated_at": note.updated_at.isoformat() if note.updated_at else None,
    }


def _experience_note_context(note: ExperienceNote) -> dict[str, Any]:
    return {
        "filename": note.filename,
        "content": note.content,
        "updated_at": note.updated_at.isoformat() if note.updated_at else None,
    }


def _company_payload(
    company: Company,
    career_pages: list[CompanyCareerPage],
    scan_discovery_counts: tuple[int, int],
) -> dict[str, Any]:
    scan_count, discovered_role_count = scan_discovery_counts
    return {
        "id": company.id,
        "name": company.name,
        "notes": company.notes,
        "prestige_tier": company.prestige_tier,
        "is_active": company.is_active,
        "browser_extra_wait_ms": company.browser_extra_wait_ms,
        "central_company_id": company.central_company_id,
        "central_sync_status": company.central_sync_status,
        "central_sync_error": company.central_sync_error,
        "central_matched_at": company.central_matched_at.isoformat()
        if company.central_matched_at
        else None,
        "created_at": company.created_at.isoformat() if company.created_at else None,
        "updated_at": company.updated_at.isoformat() if company.updated_at else None,
        "scan_count": scan_count,
        "discovered_role_count": discovered_role_count,
        "career_pages": [_company_career_page_payload(page) for page in career_pages],
    }


def _company_career_page_payload(career_page: CompanyCareerPage) -> dict[str, Any]:
    return {
        "id": career_page.id,
        "company_id": career_page.company_id,
        "url": career_page.url,
        "label": career_page.label,
        "created_at": career_page.created_at.isoformat() if career_page.created_at else None,
        "updated_at": career_page.updated_at.isoformat() if career_page.updated_at else None,
    }


def _central_client_from_web_config(connection: Any) -> CentralStoreClient:
    api_url = get_central_api_url(connection)
    if api_url is None:
        raise ValueError("Central API URL is not configured")
    return CentralStoreClient(api_url=api_url, passkey=get_central_passkey())


def _try_resolve_company_with_central_store(
    connection: Any,
    company: Company,
    *,
    career_page_urls: list[str],
) -> None:
    if company.id is None:
        return
    api_url = get_central_api_url(connection)
    if api_url is None:
        return

    client = CentralStoreClient(api_url=api_url, passkey=get_central_passkey())
    try:
        response = client.resolve_company(
            ResolveCompanyRequest(
                name=company.name,
                career_page_urls=career_page_urls,
                prestige_tier=company.prestige_tier,
                tier_source_id=get_central_client_id(connection),
            )
        )
    except CentralStoreError as error:
        set_company_central_sync_status(
            connection,
            company.id,
            status="failed",
            error=str(error),
        )
        return

    if response.action == "needs_review" or response.global_company_id is None:
        set_company_central_sync_status(connection, company.id, status="needs_review")
        return

    set_company_central_link(
        connection,
        company.id,
        central_company_id=response.global_company_id,
        canonical_domain=response.canonical_domain,
        normalized_name=response.normalized_name,
        prestige_tier=response.default_tier,
    )


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


def _metric(label: str, value: object, *, kind: str = "count") -> dict[str, object]:
    return {
        "label": label,
        "value": value,
        "kind": kind,
    }


def _query_count(connection: Any, sql: str) -> int:
    row = connection.execute(sql).fetchone()
    return int(row["count"]) if row is not None and row["count"] is not None else 0


def _query_float(connection: Any, sql: str) -> float | None:
    row = connection.execute(sql).fetchone()
    if row is None or row["value"] is None:
        return None
    return float(row["value"])


def _query_count_by_value(connection: Any, sql: str) -> dict[str, int]:
    rows = connection.execute(sql).fetchall()
    return {str(row["value"]): int(row["count"]) for row in rows}


def _role_review_later_count(connection: Any, role_id: int) -> int:
    row = connection.execute(
        """
        SELECT COUNT(*) AS count
        FROM events
        WHERE role_id = ? AND event_type = ?
        """,
        (role_id, REVIEW_LATER_EVENT_TYPE),
    ).fetchone()
    return int(row["count"]) if row is not None and row["count"] is not None else 0


def _role_payload(role: Role | RoleListItem) -> dict[str, Any]:
    payload = role.model_dump(mode="json")
    for key in ("first_seen_at", "last_seen_at", "created_at", "updated_at"):
        payload[key] = _datetime_or_none(getattr(role, key))
    return payload


def _role_title_from_url(role_url: str) -> str:
    parsed = urlparse(role_url)
    path_parts = [part for part in parsed.path.split("/") if part]
    if not path_parts:
        return "Manually added role"
    slug = re.sub(r"[-_]+", " ", path_parts[-1])
    slug = re.sub(r"\s+", " ", slug).strip()
    return slug or "Manually added role"


def _latest_datetime(*values: datetime | None) -> datetime | None:
    present_values = [value for value in values if value is not None]
    if not present_values:
        return None
    return max(present_values, key=_datetime_sort_key)


def _datetime_sort_key(value: datetime) -> float:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.timestamp()


def _start_update_and_restart(*, host: str, port: int) -> None:
    subprocess.Popen(
        ["bash", "-lc", _update_restart_script(host=host, port=port)],
        cwd=Path.cwd(),
        start_new_session=True,
    )


def _update_restart_script(*, host: str, port: int) -> str:
    executable = _current_callumployed_executable()
    update_log_path = Path("/tmp/callumployed-web-update.log")
    serve_log_path = Path("/tmp/callumployed-tmux.log")
    return "\n".join(
        [
            "set -eu",
            "sleep 3",
            f"cd {shlex.quote(str(Path.cwd()))}",
            f"echo '--- update started '$(date) >> {shlex.quote(str(update_log_path))}",
            (
                f"curl -fsSL {shlex.quote(INSTALLER_SCRIPT_URL)} | bash "
                f">> {shlex.quote(str(update_log_path))} 2>&1"
            ),
            f"echo '--- restart started '$(date) >> {shlex.quote(str(update_log_path))}",
            (
                f"exec {shlex.quote(str(executable))} serve "
                f"--host {shlex.quote(host)} --port {port} "
                f">> {shlex.quote(str(serve_log_path))} 2>&1"
            ),
        ]
    )


def _current_callumployed_executable() -> Path:
    command_path = Path(sys.argv[0]).resolve()
    if command_path.exists():
        return command_path
    path_command = shutil.which(sys.argv[0]) or shutil.which("callumployed")
    if path_command:
        return Path(path_command).resolve()
    return command_path


def _shutdown_server(server: BaseServer) -> None:
    server.shutdown()


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
    if filename.endswith(".png"):
        return "image/png"
    if filename.endswith(".webmanifest"):
        return "application/manifest+json; charset=utf-8"
    return "application/octet-stream"
