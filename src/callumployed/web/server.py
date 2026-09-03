from __future__ import annotations

import asyncio
import base64
import binascii
import ctypes
import gzip
import json
import logging
import mimetypes
import os
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import unicodedata
from collections import Counter
from contextlib import nullcontext, suppress
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from io import BytesIO
from pathlib import Path, PurePosixPath
from socketserver import BaseServer
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from platformdirs import user_data_path
from pypdf import PdfReader

from callumployed.agents.applicant_profile_extractor import extract_applicant_profile
from callumployed.agents.cover_letter import (
    ApplicantProfile,
    find_named_hiring_contact,
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
from callumployed.config import LlmSettings
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
    LOCATION_FILTER_VALUES,
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
    delete_cover_letter_example,
    delete_experience_note,
    finish_scan_run,
    get_company,
    get_company_scan_discovery_counts,
    get_config_value,
    get_cover_letter_example,
    get_experience_note,
    get_latest_scan_role_presence,
    get_location_filter,
    get_master_resume,
    get_role,
    get_tracking_stats,
    list_companies,
    list_company_career_pages,
    list_company_career_pages_by_company,
    list_config_values,
    list_cover_letter_example_knowledge,
    list_cover_letter_examples,
    list_experience_notes,
    list_resume_feedback_knowledge,
    list_role_items,
    list_roles,
    list_scan_runs,
    record_resume_feedback_history,
    record_role_review_later,
    retrieve_role_context,
    set_company_central_link,
    set_company_central_sync_status,
    set_config_value,
    set_include_graduate_degree_roles,
    set_include_hardware_roles,
    set_internship_mode,
    set_location_filter,
    set_require_software_keywords,
    set_role_status,
    set_role_status_if_changed,
    should_include_graduate_degree_roles,
    should_include_hardware_roles,
    should_require_software_keywords,
    should_use_internship_mode,
    sync_role_context_vectors,
    update_company,
    upsert_master_resume,
)
from callumployed.services.app_settings import (
    APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY,
    schedule_applicant_profile_reprep,
)
from callumployed.services.app_settings import (
    configured_llm_settings as build_configured_llm_settings,
)
from callumployed.services.application_generation import (
    build_application_prompt,
)
from callumployed.services.autoprep import (
    AutoprepConflictError,
    AutoprepCoordinator,
    clear_autoprep_instruction,
    complete_application_answer,
    create_application_answer,
    delete_application_answer,
    enqueue_autoprep_jobs,
    ensure_autoprep_schema,
    fail_application_answer,
    finish_autoprep_worker,
    get_autoprep_job,
    get_autoprep_resume_latex,
    get_latest_bulk_cover_letter_regeneration,
    get_role_autoprep_job,
    list_application_answers,
    list_autoprep_jobs,
    list_interested_autoprep_roles,
    mark_autoprep_document,
    queue_all_prepped_cover_letter_regenerations,
    queue_application_answer_regeneration,
    queue_autoprep_regeneration,
    recover_interrupted_application_answers,
    recover_interrupted_autoprep_jobs,
    retry_autoprep_document,
)
from callumployed.services.material_index import (
    build_material_index,
    get_material_index_status,
    retrieve_indexed_materials,
    split_experience_note,
)
from callumployed.services.scan_schedule import (
    DEFAULT_SCAN_SCHEDULE_ENABLED,
    DEFAULT_SCAN_SCHEDULE_TIME,
    SCAN_SCHEDULE_ENABLED_CONFIG_KEY,
    SCAN_SCHEDULE_LAST_RUN_DATE_CONFIG_KEY,
    SCAN_SCHEDULE_TIME_CONFIG_KEY,
    clean_scan_schedule_time,
    get_scan_schedule,
    is_daily_scan_due,
    set_scan_schedule_enabled,
    set_scan_schedule_time,
)
from callumployed.services.scan_workflow import CompanyScanResult
from callumployed.services.scan_workflow import rescan_role as run_rescan_role
from callumployed.services.scan_workflow import scan_company as run_scan_company
from callumployed.webscraping.profile_manager import BrowserProfileManager

STATIC_PACKAGE = "callumployed.web.static"
INSTALLER_SCRIPT_URL = (
    "https://raw.githubusercontent.com/CallumMackenzie/callumployed/master/scripts/install.sh"
)
LOGGER = logging.getLogger(__name__)
SCAN_ALL_COMPANY_TIMEOUT_SECONDS = 5 * 60
COMPANY_TIER_GUIDE_OPEN_CONFIG_KEY = "ui_company_tier_guide_open"
APPLICANT_FIRST_NAME_CONFIG_KEY = "applicant_first_name"
APPLICANT_LAST_NAME_CONFIG_KEY = "applicant_last_name"
APPLICANT_EMAIL_CONFIG_KEY = "applicant_email"
APPLICANT_PHONE_CONFIG_KEY = "applicant_phone"
APPLICANT_INSTITUTION_CONFIG_KEY = "applicant_institution"
APPLICANT_DEGREE_CONFIG_KEY = "applicant_degree"
APPLICANT_PROFILE_CONFIG_KEYS = (
    APPLICANT_FIRST_NAME_CONFIG_KEY,
    APPLICANT_LAST_NAME_CONFIG_KEY,
    APPLICANT_EMAIL_CONFIG_KEY,
    APPLICANT_PHONE_CONFIG_KEY,
    APPLICANT_INSTITUTION_CONFIG_KEY,
    APPLICANT_DEGREE_CONFIG_KEY,
)
COVER_LETTER_MODEL_CONFIG_KEY = "cover_letter_model"
AUTOPREP_TAILOR_RESUME_CONFIG_KEY = "autoprep_tailor_resume"
AUTOPREP_RESUME_PROMPT_CONFIG_KEY = "autoprep_resume_prompt"
AUTOPREP_COVER_LETTER_PROMPT_CONFIG_KEY = "autoprep_cover_letter_prompt"
LLM_PROVIDER_CONFIG_KEY = "llm_provider"
SCAN_HEADLESS_CONFIG_KEY = "scan_headless"
DEFAULT_LLM_PROVIDER = "openai"
DEFAULT_COVER_LETTER_MODEL = "gpt-4.1-mini"
DEFAULT_AUTOPREP_TAILOR_RESUME = True
DEFAULT_AUTOPREP_RESUME_PROMPT = (
    "Tailor this resume truthfully for the saved role context. Preserve every employer, "
    "project, education entry, date, and link while actively improving the wording. "
    "Budget the content for one page before drafting. Lead bullets with strong action verbs, "
    "emphasize source-supported accomplishments, and quantify only when the source provides "
    "the number. Do not invent claims or awkwardly combine unrelated experiences."
)
DEFAULT_AUTOPREP_COVER_LETTER_PROMPT = (
    "Review the indexed application materials as well as the resume and job description. "
    "Write a concise, company-specific cover letter using the strongest 2-3 source-supported "
    "examples. Explain the task or problem, action taken, and result delivered; demonstrate "
    "relevant soft skills through evidence rather than generic claims. For AI-related roles, "
    "use a source-supported, independently directed AI application and its outcome when "
    "available, naming Hermes when the source supports it. Close by thanking the reader and "
    "inviting an interview. Use three short body paragraphs by default, target roughly 200-300 "
    "words, and never pad the letter to fill the page. The letter must be at most one page. Do "
    "not invent experience, referrals, company research, outcomes, or metrics."
)
DEFAULT_SCAN_HEADLESS = False
LLM_PROVIDER_OPTIONS = (
    ("openai", "OpenAI API key"),
    ("codex", "Codex subscription (local CLI)"),
)
SUPPORTED_LLM_PROVIDERS = frozenset(value for value, _label in LLM_PROVIDER_OPTIONS)
COVER_LETTER_MODEL_OPTIONS = (
    ("gpt-5.6-terra", "Terra"),
    ("gpt-5.6-luna", "Luna"),
    ("gpt-5.6-sol", "Sol"),
    ("gpt-4.1-mini", "GPT-4.1 mini"),
)
SUPPORTED_COVER_LETTER_MODELS = frozenset(value for value, _label in COVER_LETTER_MODEL_OPTIONS)
SUPPORTED_COMPANY_TIERS = frozenset(str(tier) for tier in range(8))
AUTOPREP_COORDINATOR: AutoprepCoordinator | None = None
CURRENTLY_APPLYING_LOCK = threading.Lock()
APPLICANT_PROFILE_TEXT_CONFIG_KEYS = {
    APPLICANT_EMAIL_CONFIG_KEY,
    APPLICANT_PHONE_CONFIG_KEY,
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
        self._current_task: asyncio.Task[CompanyScanResult | None] | None = None
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
        llm_settings = LlmSettings()
        with db.connect() as connection:
            companies = list_companies(connection)
            llm_settings = build_configured_llm_settings(connection)
        with self._lock:
            self._total_companies = len(companies)

        browser_profile_manager = _configured_browser_profile_manager()
        for company in companies:
            if self._cancel_requested.is_set():
                LOGGER.info("Scan cancelled before scanning %s.", company.name)
                break
            try:
                task = asyncio.create_task(
                    run_scan_company(
                        company,
                        browser_profile_manager=browser_profile_manager,
                        llm_settings=llm_settings,
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


class DebouncedAction:
    """Run one background action after changes have been quiet for a fixed window."""

    def __init__(self, callback: Any, *, delay_seconds: float) -> None:
        self._callback = callback
        self._delay_seconds = delay_seconds
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None
        self._generation = 0
        self._closed = False

    def schedule(self) -> None:
        with self._lock:
            if self._closed:
                return
            if self._timer is not None:
                self._timer.cancel()
            self._generation += 1
            generation = self._generation
            self._timer = threading.Timer(
                self._delay_seconds,
                lambda: self._run(generation),
            )
            self._timer.daemon = True
            self._timer.start()

    def cancel(self) -> None:
        with self._lock:
            self._generation += 1
            timer = self._timer
            self._timer = None
        if timer is not None:
            timer.cancel()

    def close(self) -> None:
        with self._lock:
            self._closed = True
            self._generation += 1
            timer = self._timer
            self._timer = None
        if timer is not None:
            timer.cancel()

    def _run(self, generation: int) -> None:
        with self._lock:
            if self._closed or generation != self._generation:
                return
            self._timer = None
        try:
            self._callback()
        except Exception:
            LOGGER.exception("Debounced background action failed")


class DailyScanScheduler:
    def __init__(self) -> None:
        self._stop = threading.Event()
        self._wake = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="callumployed-daily-scan-scheduler",
            daemon=True,
        )
        self._thread.start()

    def wake(self) -> None:
        self._wake.set()

    def stop(self) -> None:
        self._stop.set()
        self._wake.set()
        if self._thread is not None:
            self._thread.join(timeout=5)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                self._run_if_due()
            except Exception:
                LOGGER.exception("Daily scan scheduler check failed")
            self._wake.wait(timeout=30)
            self._wake.clear()

    def _run_if_due(self) -> None:
        now = datetime.now().astimezone()
        today = now.date().isoformat()
        with db.connect() as connection:
            enabled, scheduled_time, last_run_date = get_scan_schedule(connection)
            if not is_daily_scan_due(
                now=now,
                enabled=enabled,
                scheduled_time=scheduled_time,
                last_run_date=last_run_date,
            ):
                return
            if not SCAN_COORDINATOR.start():
                return
            set_config_value(connection, SCAN_SCHEDULE_LAST_RUN_DATE_CONFIG_KEY, today)
        LOGGER.info("Started scheduled daily scan for %s at %s", today, scheduled_time)


SCAN_SCHEDULER = DailyScanScheduler()


class LocalThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True

    def server_bind(self) -> None:
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        host, port = self.socket.getsockname()[:2]
        self.server_address = (host, port)
        self.server_name = str(host)
        self.server_port = int(port)


def build_tracker_payload(query: str | None = None) -> dict[str, Any]:
    is_search = bool(query and query.strip())
    autoprep_status_by_role_id: dict[int, str | None] = {}
    with db.connect() as connection:
        stats = get_tracking_stats(connection)
        roles = list_role_items(connection, query=query)
        ensure_autoprep_schema(connection)
        autoprep_status_by_role_id = {
            int(role["id"]): role.get("preparation_status")
            for role in list_interested_autoprep_roles(connection)
            if isinstance(role.get("id"), int)
        }
        disinterested_cutoff = (datetime.now(UTC) - timedelta(days=2)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        recently_disinterested_role_ids = {
            int(row["role_id"])
            for row in connection.execute(
                """
                SELECT DISTINCT role_id
                FROM events
                WHERE event_type = 'status_changed'
                  AND new_status = ?
                  AND role_id IS NOT NULL
                  AND created_at >= ?
                """,
                (RoleStatus.DISINTERESTED.value, disinterested_cutoff),
            ).fetchall()
        }
        active_roles = [role for role in roles if role.role_status is not RoleStatus.ARCHIVED]
        latest_scan_presence = get_latest_scan_role_presence(
            connection,
            {role.company_id for role in active_roles},
        )

    latest_scan_ids_by_company = {
        company_id: presence[0] for company_id, presence in latest_scan_presence.items()
    }
    latest_scan_role_ids_by_company = {
        company_id: presence[1] for company_id, presence in latest_scan_presence.items()
    }
    latest_scan_role_urls_by_company = {
        company_id: presence[2] for company_id, presence in latest_scan_presence.items()
    }

    grouped_roles: dict[str, list[dict[str, Any]]] = {status.value: [] for status in RoleStatus}
    for role in active_roles:
        if (
            not is_search
            and role.role_status is RoleStatus.DISINTERESTED
            and role.id not in recently_disinterested_role_ids
        ):
            continue
        payload = _role_payload(role)
        if role.role_status in {
            RoleStatus.APPLIED,
            RoleStatus.REJECTED,
            RoleStatus.CLOSED,
        }:
            payload.pop("description", None)
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
        autoprep_status = (
            autoprep_status_by_role_id.get(role.id) if isinstance(role.id, int) else None
        )
        payload["autoprep_started"] = autoprep_status is not None
        payload["autoprep_status"] = autoprep_status
        grouped_roles[role.role_status.value].append(payload)
    if not is_search:
        grouped_roles[RoleStatus.REJECTED.value] = grouped_roles[RoleStatus.REJECTED.value][:10]
        grouped_roles[RoleStatus.CLOSED.value] = grouped_roles[RoleStatus.CLOSED.value][:10]
    grouped_roles[RoleStatus.INTERESTED.value].sort(
        key=lambda role: bool(role.get("prep_started")),
        reverse=True,
    )
    grouped_roles[RoleStatus.CLOSED.value].sort(
        key=lambda role: bool(role["updated_in_latest_scan"]),
        reverse=True,
    )

    role_counts = Counter(role.role_status.value for role in roles)
    statuses = [
        {
            "key": status.value,
            "label": STATUS_LABELS[status.value],
            "count": role_counts[status.value],
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
        db.run_migrations(connection)
        companies = list_companies(connection)
        scan_discovery_counts = get_company_scan_discovery_counts(connection)
        career_pages_by_company_id = list_company_career_pages_by_company(connection)
        company_tier_guide_open = (
            get_config_value(connection, COMPANY_TIER_GUIDE_OPEN_CONFIG_KEY) == "true"
        )
    return {
        "company_tier_guide_open": company_tier_guide_open,
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
            if parsed_url.path == "/api/autoprep/interested":
                self._send_json(build_autoprep_interested_payload())
                return
            if parsed_url.path == "/api/autoprep/jobs":
                self._send_json(build_prepped_roles_payload())
                return
            path_parts = [part for part in PurePosixPath(parsed_url.path).parts if part != "/"]
            if (
                len(path_parts) == 3
                and path_parts[0] == "api"
                and path_parts[1] in {"cover-letter-examples", "experience-notes"}
            ):
                self._send_application_material(path_parts[1], path_parts[2])
                return
            if (
                len(path_parts) == 3
                and path_parts[0] == "api"
                and path_parts[1] == "resume-resources"
            ):
                self._send_resume_resource(path_parts[2])
                return
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
            if (
                len(path_parts) == 5
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "application-answers"
            ):
                self._list_application_answers(path_parts[3])
                return
            if (
                len(path_parts) == 6
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "documents"
            ):
                self._send_autoprep_document(path_parts[3], path_parts[5])
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
            if path_parts == ["api", "autoprep", "cover-letters", "regenerate"]:
                self._regenerate_all_prepped_cover_letters()
                return
            if path_parts == ["api", "autoprep", "jobs"]:
                self._enqueue_autoprep()
                return

            if path_parts == ["api", "autoprep", "currently-applying", "open"]:
                self._open_currently_applying_folder()
                return

            if (
                len(path_parts) == 5
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "currently-applying"
            ):
                self._select_currently_applying_role(path_parts[3])
                return
            if (
                len(path_parts) == 5
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "application-answers"
            ):
                self._create_application_answer(path_parts[3])
                return
            if (
                len(path_parts) == 7
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "application-answers"
                and path_parts[6] == "regenerate"
            ):
                self._regenerate_application_answer(path_parts[3], path_parts[5])
                return
            if (
                len(path_parts) == 6
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "retry"
            ):
                self._retry_autoprep_document(path_parts[3], path_parts[5])
                return
            if (
                len(path_parts) == 6
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "regenerate"
            ):
                self._regenerate_autoprep_document(path_parts[3], path_parts[5])
                return
            if (
                len(path_parts) == 5
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "open-folder"
            ):
                self._open_autoprep_folder(path_parts[3])
                return
            if path_parts == ["api", "application-materials", "index", "open"]:
                self._open_application_material_index()
                return
            if (
                len(path_parts) == 5
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "applied"
            ):
                self._mark_autoprep_applied(path_parts[3])
                return
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
            if len(path_parts) == 3 and path_parts == ["api", "application-materials", "index"]:
                self._index_application_materials()
                return
            if len(path_parts) == 2 and path_parts == ["api", "companies"]:
                self._add_company()
                return
            if path_parts == ["api", "ui-state", "company-tier-guide"]:
                self._update_company_tier_guide_state()
                return
            if len(path_parts) == 2 and path_parts == ["api", "roles"]:
                self._add_role()
                return
            if len(path_parts) == 3 and path_parts[0] == "api" and path_parts[1] == "companies":
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
            if path_parts == ["api", "config", "extract-profile"]:
                self._extract_applicant_profile()
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
                len(path_parts) == 6
                and path_parts[:3] == ["api", "autoprep", "roles"]
                and path_parts[4] == "application-answers"
            ):
                self._delete_application_answer(path_parts[3], path_parts[5])
                return
            if (
                len(path_parts) == 3
                and path_parts[0] == "api"
                and path_parts[1]
                in {"cover-letter-examples", "experience-notes", "resume-resources"}
            ):
                self._delete_application_material(path_parts[1], path_parts[2])
                return
            if len(path_parts) == 3 and path_parts[0] == "api" and path_parts[1] == "companies":
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

        def _send_application_material(self, material_type: str, material_id_text: str) -> None:
            try:
                material_id = int(material_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid material id")
                return
            material = None
            with db.connect() as connection:
                material = (
                    get_cover_letter_example(connection, material_id)
                    if material_type == "cover-letter-examples"
                    else get_experience_note(connection, material_id)
                )
            if material is None:
                self.send_error(HTTPStatus.NOT_FOUND, "Application material not found")
                return
            content = material.content
            preview_warning = None
            if content.lstrip().startswith("%PDF-"):
                preview_warning = (
                    "This legacy PDF was stored before readable-text extraction was added. "
                    "Remove it and upload the PDF again to preview and use its extracted text."
                )
                content = preview_warning
            self._send_json(
                {
                    "id": material.id,
                    "filename": material.filename,
                    "content": content,
                    "preview_warning": preview_warning,
                    "content_sha256": material.content_sha256,
                    "updated_at": material.updated_at.isoformat() if material.updated_at else None,
                }
            )

        def _send_resume_resource(self, filename_text: str) -> None:
            path = _safe_resume_resource_path(filename_text)
            if path is None or not path.is_file():
                self.send_error(HTTPStatus.NOT_FOUND, "Resume resource not found")
                return
            body = path.read_bytes()
            content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Content-Disposition", "inline")
            self.end_headers()
            self.wfile.write(body)

        def _delete_application_material(self, material_type: str, identifier: str) -> None:
            if material_type == "resume-resources":
                path = _safe_resume_resource_path(identifier)
                if path is None or not path.is_file():
                    self.send_error(HTTPStatus.NOT_FOUND, "Resume resource not found")
                    return
                path.unlink()
            else:
                try:
                    material_id = int(identifier)
                except ValueError:
                    self.send_error(HTTPStatus.BAD_REQUEST, "Invalid material id")
                    return
                with db.connect() as connection:
                    deleted = (
                        delete_cover_letter_example(connection, material_id)
                        if material_type == "cover-letter-examples"
                        else delete_experience_note(connection, material_id)
                    )
                if not deleted:
                    self.send_error(HTTPStatus.NOT_FOUND, "Application material not found")
                    return
            _refresh_application_material_index()
            self._send_json(build_application_materials_payload())

        def _enqueue_autoprep(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return
            role_ids_value = payload.get("role_ids")
            idempotency_key = payload.get("idempotency_key")
            if not isinstance(role_ids_value, list) or not all(
                isinstance(role_id, int) for role_id in role_ids_value
            ):
                self.send_error(HTTPStatus.BAD_REQUEST, "role_ids must be a list of integers")
                return
            if not isinstance(idempotency_key, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "idempotency_key is required")
                return
            try:
                with db.connect() as connection:
                    ensure_autoprep_schema(connection)
                    jobs = enqueue_autoprep_jobs(
                        connection,
                        role_ids_value,
                        idempotency_key=idempotency_key,
                    )
            except AutoprepConflictError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.CONFLICT)
                return
            except ValueError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.BAD_REQUEST)
                return
            _wake_autoprep_coordinator()
            self._send_json_with_status({"accepted": True, "jobs": jobs}, HTTPStatus.ACCEPTED)

        def _regenerate_all_prepped_cover_letters(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return
            idempotency_key = payload.get("idempotency_key")
            if not isinstance(idempotency_key, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "idempotency_key is required")
                return
            result: dict[str, Any] = {}
            try:
                with db.connect() as connection:
                    ensure_autoprep_schema(connection)
                    result = queue_all_prepped_cover_letter_regenerations(
                        connection,
                        idempotency_key=idempotency_key,
                    )
            except ValueError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.BAD_REQUEST)
                return
            if result["queued_count"]:
                _wake_autoprep_coordinator()
            result["accepted"] = bool(result["queued_count"])
            status = HTTPStatus.ACCEPTED if result["accepted"] else HTTPStatus.OK
            self._send_json_with_status(result, status)

        def _retry_autoprep_document(self, role_id_text: str, document_kind: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            if document_kind not in {"resume", "cover-letter"}:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid document kind")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            idempotency_key = payload.get("idempotency_key")
            if not isinstance(idempotency_key, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "idempotency_key is required")
                return
            try:
                with db.connect() as connection:
                    ensure_autoprep_schema(connection)
                    job = retry_autoprep_document(
                        connection,
                        role_id,
                        "cover_letter" if document_kind == "cover-letter" else "resume",
                        idempotency_key=idempotency_key,
                    )
            except AutoprepConflictError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.CONFLICT)
                return
            except ValueError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.BAD_REQUEST)
                return
            _wake_autoprep_coordinator()
            self._send_json_with_status({"accepted": True, "job": job}, HTTPStatus.ACCEPTED)

        def _regenerate_autoprep_document(self, role_id_text: str, document_kind: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            if document_kind not in {"resume", "cover-letter"}:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid document kind")
                return
            payload = self._read_json_body()
            if payload is None:
                return
            comments = payload.get("comments")
            idempotency_key = payload.get("idempotency_key")
            if not isinstance(comments, str) or not isinstance(idempotency_key, str):
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    "comments and idempotency_key are required",
                )
                return
            try:
                with db.connect() as connection:
                    ensure_autoprep_schema(connection)
                    job = queue_autoprep_regeneration(
                        connection,
                        role_id,
                        "cover_letter" if document_kind == "cover-letter" else "resume",
                        instruction=comments,
                        idempotency_key=idempotency_key,
                    )
            except AutoprepConflictError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.CONFLICT)
                return
            except ValueError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.BAD_REQUEST)
                return
            _wake_autoprep_coordinator()
            self._send_json_with_status({"accepted": True, "job": job}, HTTPStatus.ACCEPTED)

        def _list_application_answers(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
                with db.connect() as connection:
                    db.run_migrations(connection)
                    ensure_autoprep_schema(connection)
                    get_role(connection, role_id)
                    answers = list_application_answers(connection, role_id)
            except (TypeError, ValueError) as error:
                self.send_error(HTTPStatus.NOT_FOUND, str(error))
                return
            self._send_json({"answers": answers})

        def _create_application_answer(self, role_id_text: str) -> None:
            payload = self._read_json_body()
            if payload is None:
                return
            try:
                role_id = int(role_id_text)
                question = payload.get("question")
                if not isinstance(question, str):
                    raise ValueError("An application question is required.")
                with db.connect() as connection:
                    db.run_migrations(connection)
                    ensure_autoprep_schema(connection)
                    pending = create_application_answer(
                        connection, role_id, question=question, backend="openai"
                    )
                try:
                    result = generate_saved_application_answer(role_id, question=question.strip())
                    with db.connect() as connection:
                        answer = complete_application_answer(
                            connection,
                            int(pending["id"]),
                            answer=result["answer"],
                            sources=result.get("sources"),
                            research=result.get("research"),
                        )
                except Exception as error:
                    with db.connect() as connection:
                        answer = fail_application_answer(
                            connection, int(pending["id"]), error=_autoprep_error(error)
                        )
                    self._send_json_with_status({"answer": answer}, HTTPStatus.SERVICE_UNAVAILABLE)
                    return
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return
            self._send_json_with_status({"answer": answer}, HTTPStatus.CREATED)

        def _regenerate_application_answer(
            self, role_id_text: str, answer_id_text: str
        ) -> None:
            try:
                role_id = int(role_id_text)
                answer_id = int(answer_id_text)
                with db.connect() as connection:
                    db.run_migrations(connection)
                    ensure_autoprep_schema(connection)
                    get_role(connection, role_id)
                    pending = queue_application_answer_regeneration(
                        connection,
                        role_id,
                        answer_id,
                        backend="openai",
                    )
            except AutoprepConflictError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.CONFLICT)
                return
            except (TypeError, ValueError) as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.BAD_REQUEST)
                return

            try:
                result = generate_saved_application_answer(
                    role_id,
                    question=str(pending["question"]).strip(),
                )
                with db.connect() as connection:
                    answer = complete_application_answer(
                        connection,
                        answer_id,
                        answer=result["answer"],
                        sources=result.get("sources"),
                        research=result.get("research"),
                    )
            except Exception as error:
                with db.connect() as connection:
                    answer = fail_application_answer(
                        connection,
                        answer_id,
                        error=_autoprep_error(error),
                    )
                self._send_json_with_status(
                    {"answer": answer}, HTTPStatus.SERVICE_UNAVAILABLE
                )
                return
            self._send_json({"answer": answer})

        def _delete_application_answer(
            self, role_id_text: str, answer_id_text: str
        ) -> None:
            try:
                role_id = int(role_id_text)
                answer_id = int(answer_id_text)
                with db.connect() as connection:
                    db.run_migrations(connection)
                    ensure_autoprep_schema(connection)
                    deleted = delete_application_answer(connection, role_id, answer_id)
            except AutoprepConflictError as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.CONFLICT)
                return
            except (TypeError, ValueError) as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.NOT_FOUND)
                return
            self._send_json({"deleted_id": deleted["id"]})


        def _send_autoprep_document(self, role_id_text: str, document_name: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            document_paths = {
                "resume.pdf": "resume_artifact_path",
                "cover-letter.pdf": "cover_letter_artifact_path",
            }
            document_field = document_paths.get(document_name)
            if document_field is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid document kind")
                return
            with db.connect() as connection:
                ensure_autoprep_schema(connection)
                job = get_role_autoprep_job(connection, role_id)
            if job is None:
                self.send_error(HTTPStatus.NOT_FOUND, "Autoprep role not found")
                return
            path_value = job.get(document_field)
            directory_value = job.get("artifact_directory")
            if not isinstance(path_value, str) or not isinstance(directory_value, str):
                self.send_error(HTTPStatus.NOT_FOUND, "Prepared document is not available")
                return
            path = Path(path_value).resolve()
            directory = Path(directory_value).resolve()
            if path.parent != directory or path.suffix.lower() != ".pdf" or not path.is_file():
                self.send_error(HTTPStatus.NOT_FOUND, "Prepared document is not available")
                return
            self._send_pdf_file(path, filename=path.name)

        def _open_autoprep_folder(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            with db.connect() as connection:
                ensure_autoprep_schema(connection)
                job = get_role_autoprep_job(connection, role_id)
            if job is None:
                self.send_error(HTTPStatus.NOT_FOUND, "Autoprep role not found")
                return
            directory_value = job.get("artifact_directory")
            if not isinstance(directory_value, str) or not Path(directory_value).is_dir():
                self.send_error(HTTPStatus.NOT_FOUND, "Documents folder is not available")
                return
            try:
                subprocess.run(["open", directory_value], check=True, timeout=10)
            except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                LOGGER.exception("Could not open Autoprep documents folder %s", directory_value)
                self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Could not open documents folder")
                return
            self._send_json({"opened": True, "path": directory_value})

        def _select_currently_applying_role(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            with db.connect() as connection:
                ensure_autoprep_schema(connection)
                job = get_role_autoprep_job(connection, role_id)
            if job is None:
                self.send_error(HTTPStatus.NOT_FOUND, "Autoprep role not found")
                return
            try:
                result = _sync_currently_applying_folder(job)
            except (FileNotFoundError, ValueError) as error:
                self._send_json_with_status({"error": str(error)}, HTTPStatus.CONFLICT)
                return
            except (OSError, RuntimeError):
                LOGGER.exception("Could not refresh Currently Applying for role %s", role_id)
                self.send_error(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    "Could not refresh the Currently Applying folder",
                )
                return
            self._send_json({"updated": True, **result})

        def _open_currently_applying_folder(self) -> None:
            directory = _currently_applying_directory()
            root = _prepared_applications_root().resolve()
            resolved = directory.resolve()
            if (
                resolved.parent != root
                or resolved.name != "currently-applying"
                or not resolved.is_dir()
            ):
                self.send_error(HTTPStatus.NOT_FOUND, "Currently Applying folder is not available")
                return
            try:
                subprocess.run(["open", str(resolved)], check=True, timeout=10)
            except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                LOGGER.exception("Could not open Currently Applying folder %s", resolved)
                self.send_error(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    "Could not open the Currently Applying folder",
                )
                return
            self._send_json({"opened": True, "path": str(resolved)})

        def _open_application_material_index(self) -> None:
            notes: list[ExperienceNote] = []
            with db.connect() as connection:
                db.run_migrations(connection)
                notes = list_experience_notes(connection)
            status = get_material_index_status(
                [_experience_note_index_source(note) for note in notes]
            )
            index_path = Path(str(status["index_path"]))
            if status["status"] != "ready" or not index_path.is_file():
                self.send_error(HTTPStatus.NOT_FOUND, "Application material index is not available")
                return
            try:
                subprocess.run(["open", "-R", str(index_path)], check=True, timeout=10)
            except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                LOGGER.exception("Could not reveal application material index %s", index_path)
                self.send_error(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    "Could not open application material index",
                )
                return
            self._send_json({"opened": True, "path": str(index_path)})

        def _mark_autoprep_applied(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return
            try:
                with db.connect() as connection:
                    ensure_autoprep_schema(connection)
                    job = get_role_autoprep_job(connection, role_id)
                    if job is None:
                        raise LookupError
                    if job["overall_status"] != "ready":
                        self._send_json_with_status(
                            {"error": "Both documents must be ready before marking Applied."},
                            HTTPStatus.CONFLICT,
                        )
                        return
                    role = set_role_status_if_changed(
                        connection,
                        role_id,
                        RoleStatus.APPLIED,
                        summary="Marked Applied from Prepped Roles.",
                    )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Autoprep role not found")
                return
            self._send_json({"applied": True, "role": _role_payload(role)})

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

            autoprep_job: dict[str, Any] | None = None
            role: Role | None = None
            try:
                with db.connect() as connection:
                    if status is RoleStatus.DISINTERESTED:
                        ensure_autoprep_schema(connection)
                        connection.execute("BEGIN IMMEDIATE")
                        active_job = get_role_autoprep_job(connection, role_id)
                        if active_job is not None and active_job["worker_state"] != "idle":
                            connection.rollback()
                            self._send_json_with_status(
                                {
                                    "error": (
                                        "Wait for this role's active preparation to finish "
                                        "before moving it to Disinterested."
                                    )
                                },
                                HTTPStatus.CONFLICT,
                            )
                            return
                    previous_role = get_role(connection, role_id)
                    role = set_role_status(
                        connection,
                        role_id,
                        status,
                        summary="Status updated from tracker.",
                    )
                    if status is RoleStatus.INTERESTED:
                        ensure_autoprep_schema(connection)
                        autoprep_job = enqueue_autoprep_jobs(
                            connection,
                            [role_id],
                            idempotency_key=f"interested-role-{role_id}",
                        )[0]
                        if (
                            previous_role.role_status is not RoleStatus.INTERESTED
                            and autoprep_job["worker_state"] == "idle"
                        ):
                            for document_kind in ("resume", "cover_letter"):
                                status_key = f"{document_kind}_status"
                                if autoprep_job[status_key] not in {"failed", "interrupted"}:
                                    continue
                                attempt = int(autoprep_job[f"{document_kind}_attempt"])
                                autoprep_job = retry_autoprep_document(
                                    connection,
                                    role_id,
                                    document_kind,
                                    idempotency_key=(
                                        f"interested-role-{role_id}-{document_kind}-{attempt}"
                                    ),
                                )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            except (AutoprepConflictError, ValueError) as error:
                self.send_error(HTTPStatus.CONFLICT, str(error))
                return

            if role is None:
                self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Role status was not updated")
                return
            if autoprep_job is not None:
                _wake_autoprep_coordinator()
            self._send_json({"role": _role_payload(role), "autoprep_job": autoprep_job})

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
            role: Role | None = None
            autoprep_job: dict[str, Any] | None = None
            scan_error = None
            claim_barrier = (
                AUTOPREP_COORDINATOR.defer_claiming()
                if AUTOPREP_COORDINATOR is not None
                else nullcontext()
            )
            with claim_barrier:
                try:
                    with db.connect() as connection:
                        company = get_company(connection, company_id)
                        if not company.is_active:
                            self.send_error(HTTPStatus.BAD_REQUEST, "Company is deactivated")
                            return
                        ensure_autoprep_schema(connection)
                        connection.execute("BEGIN IMMEDIATE")
                        try:
                            role = add_role(
                                connection,
                                Role(
                                    company_id=company_id,
                                    title=_role_title_from_url(role_url),
                                    role_url=role_url,
                                    role_status=RoleStatus.INTERESTED,
                                ),
                                commit=False,
                            )
                            if role.id is None:
                                raise RuntimeError("Role was not created")
                            autoprep_job = enqueue_autoprep_jobs(
                                connection,
                                [role.id],
                                idempotency_key=f"explicit-role-{role.id}",
                                manage_transaction=False,
                            )[0]
                            connection.commit()
                        except Exception:
                            connection.rollback()
                            raise
                except LookupError:
                    self.send_error(HTTPStatus.NOT_FOUND, "Company not found")
                    return
                except RuntimeError as error:
                    self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                    return
                except Exception:
                    self.send_error(
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        "Could not create and queue the role",
                    )
                    return

                if role is None or role.id is None:
                    self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Role was not created")
                    return
                role_id = role.id
                try:
                    scan = asyncio.run(
                        run_rescan_role(
                            role_id,
                            browser_profile_manager=_configured_browser_profile_manager(),
                            update_status=False,
                        )
                    )
                    scanned_role = scan.get("role")
                    if isinstance(scanned_role, Role):
                        role = scanned_role
                except Exception as error:
                    scan_error = str(error)

                with db.connect() as connection:
                    interested_role = get_role(connection, role_id)
                    role = role.model_copy(
                        update={
                            "role_status": interested_role.role_status,
                            "updated_at": interested_role.updated_at,
                        }
                    )

            _wake_autoprep_coordinator()

            self._send_json(
                {
                    "role": _role_payload(role),
                    "tracker": build_tracker_payload(),
                    "scan_error": scan_error,
                    "autoprep_job": autoprep_job,
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
                self.send_error(HTTPStatus.BAD_REQUEST, "Company tier must be 0-7")
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

        def _update_company_tier_guide_state(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return
            if set(payload) != {"open"} or not isinstance(payload["open"], bool):
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected boolean open state")
                return
            open_state = payload["open"]
            with db.connect() as connection:
                db.run_migrations(connection)
                set_config_value(
                    connection,
                    COMPANY_TIER_GUIDE_OPEN_CONFIG_KEY,
                    "true" if open_state else "false",
                )
            self._send_json({"company_tier_guide_open": open_state})

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
                self.send_error(HTTPStatus.BAD_REQUEST, "Company tier must be 0-7")
                return
            try:
                with db.connect() as connection:
                    existing_company = get_company(connection, company_id)
                    company = update_company(
                        connection,
                        company_id,
                        notes=notes,
                        prestige_tier=prestige_tier,
                    )
                    if prestige_tier != existing_company.prestige_tier:
                        _try_resolve_company_with_central_store(
                            connection,
                            company,
                            career_page_urls=[
                                page.url
                                for page in list_company_career_pages(connection, company_id)
                            ],
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
                if not isinstance(feedback_items, list) or not 0 <= feedback_index < len(
                    feedback_items
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
                    company = get_company(connection, role.company_id)
                    resume = get_master_resume(connection)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return
            if resume is None:
                self.send_error(HTTPStatus.BAD_REQUEST, "No master resume stored")
                return
            try:
                role_payload = role.model_dump(mode="json")
                role_payload["company_name"] = company.name
                pdf_path = _generate_role_resume_pdf(role_payload, resume)
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
                    required_page_count=1,
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
                        employment_history_context=chat_context["employment_history_context"],
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
            resume_payload = _saved_role_resume(
                role_payload,
                resume,
                ensure_copy=True,
            )
            pdf_path_text = resume_payload.get("pdf_path")
            if not isinstance(pdf_path_text, str):
                self.send_error(HTTPStatus.NOT_FOUND, "Resume PDF not found")
                return
            self._send_pdf_file(
                Path(pdf_path_text),
                filename=_role_material_pdf_filename(role_payload, kind="resume"),
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
                    role = get_role(connection, role_id)
                    company = get_company(connection, role.company_id)
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
                filename=_role_material_pdf_filename(
                    {
                        **role.model_dump(mode="json"),
                        "company_name": company.name,
                    },
                    kind="cover_letter",
                ),
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
            _refresh_application_material_index()
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
            _refresh_application_material_index()
            _schedule_master_resume_profile_extraction()
            self._send_json(
                {
                    "master_resume": _master_resume_summary(resume),
                    "interested_resumes_updated": updated_count,
                    "profile_extraction_scheduled": True,
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

            _refresh_application_material_index()
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
            content_base64 = payload.get("content_base64")
            if not isinstance(filename, str):
                self.send_error(HTTPStatus.BAD_REQUEST, "Expected filename")
                return
            try:
                extracted_content = _experience_note_content_from_payload(
                    filename,
                    content=content,
                    content_base64=content_base64,
                )
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            try:
                with db.connect() as connection:
                    note = add_experience_note(
                        connection,
                        filename=filename,
                        content=extracted_content,
                    )
                    notes = list_experience_notes(connection)
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            _refresh_application_material_index()
            self._send_json(
                {
                    "experience_note": _experience_note_summary(note),
                    "experience_notes": [_experience_note_summary(item) for item in notes],
                }
            )

        def _index_application_materials(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return
            notes: list[ExperienceNote] = []
            try:
                with db.connect() as connection:
                    notes = list_experience_notes(connection)
                if not notes:
                    raise ValueError("Upload project or employment-history notes before indexing.")
                material_index = build_material_index(
                    [_experience_note_index_source(note) for note in notes]
                )
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return
            except OSError:
                LOGGER.exception("Application material indexing failed")
                self._send_json_with_status(
                    {"error": "Application material indexing failed."},
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )
                return
            self._send_json({"material_index": material_index})

        def _start_scan_all(self) -> None:
            started = SCAN_COORDINATOR.start()
            status = HTTPStatus.ACCEPTED if started else HTTPStatus.CONFLICT
            self._send_json_with_status(build_scan_status_payload(), status)

        def _cancel_scan_all(self) -> None:
            cancelled = SCAN_COORDINATOR.cancel()
            status = HTTPStatus.ACCEPTED if cancelled else HTTPStatus.CONFLICT
            self._send_json_with_status(build_scan_status_payload(), status)

        def _extract_applicant_profile(self) -> None:
            populated = _populate_missing_applicant_profile_from_resume()
            self._send_json(
                {
                    "populated": sorted(populated),
                    "config": build_config_payload(),
                }
            )

        def _update_config(self) -> None:
            payload = self._read_json_body()
            if payload is None:
                return

            allowed_keys = {
                APPLICANT_FIRST_NAME_CONFIG_KEY,
                APPLICANT_LAST_NAME_CONFIG_KEY,
                *APPLICANT_PROFILE_TEXT_CONFIG_KEYS,
                COVER_LETTER_MODEL_CONFIG_KEY,
                AUTOPREP_TAILOR_RESUME_CONFIG_KEY,
                AUTOPREP_RESUME_PROMPT_CONFIG_KEY,
                AUTOPREP_COVER_LETTER_PROMPT_CONFIG_KEY,
                LLM_PROVIDER_CONFIG_KEY,
                SCAN_HEADLESS_CONFIG_KEY,
                SCAN_SCHEDULE_ENABLED_CONFIG_KEY,
                SCAN_SCHEDULE_TIME_CONFIG_KEY,
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
                SCAN_HEADLESS_CONFIG_KEY,
                SCAN_SCHEDULE_ENABLED_CONFIG_KEY,
                AUTOPREP_TAILOR_RESUME_CONFIG_KEY,
            }
            if not all(
                isinstance(value, bool) if key in bool_keys else isinstance(value, str)
                for key, value in payload.items()
            ):
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid config value type")
                return

            try:
                validated_payload = dict(payload)
                if APPLICANT_FIRST_NAME_CONFIG_KEY in payload:
                    validated_payload[APPLICANT_FIRST_NAME_CONFIG_KEY] = _clean_applicant_name_part(
                        payload[APPLICANT_FIRST_NAME_CONFIG_KEY]
                    )
                if APPLICANT_LAST_NAME_CONFIG_KEY in payload:
                    validated_payload[APPLICANT_LAST_NAME_CONFIG_KEY] = _clean_applicant_name_part(
                        payload[APPLICANT_LAST_NAME_CONFIG_KEY]
                    )
                for key in APPLICANT_PROFILE_TEXT_CONFIG_KEYS:
                    if key in payload:
                        validated_payload[key] = _clean_applicant_profile_text(
                            key,
                            payload[key],
                        )
                if COVER_LETTER_MODEL_CONFIG_KEY in payload:
                    validated_payload[COVER_LETTER_MODEL_CONFIG_KEY] = _clean_cover_letter_model(
                        payload[COVER_LETTER_MODEL_CONFIG_KEY]
                    )
                if LLM_PROVIDER_CONFIG_KEY in payload:
                    validated_payload[LLM_PROVIDER_CONFIG_KEY] = _clean_llm_provider(
                        payload[LLM_PROVIDER_CONFIG_KEY]
                    )

                if SCAN_SCHEDULE_TIME_CONFIG_KEY in payload:
                    validated_payload[SCAN_SCHEDULE_TIME_CONFIG_KEY] = clean_scan_schedule_time(
                        payload[SCAN_SCHEDULE_TIME_CONFIG_KEY]
                    )
                for key in (
                    AUTOPREP_RESUME_PROMPT_CONFIG_KEY,
                    AUTOPREP_COVER_LETTER_PROMPT_CONFIG_KEY,
                ):
                    if key in payload:
                        validated_payload[key] = _clean_autoprep_prompt(payload[key])
                if "location_filter" in payload:
                    location_filter = payload["location_filter"].strip().lower().replace("-", "_")
                    if location_filter not in LOCATION_FILTER_VALUES:
                        expected_values = ", ".join(sorted(LOCATION_FILTER_VALUES))
                        raise ValueError(f"location_filter must be one of: {expected_values}")
                    validated_payload["location_filter"] = location_filter
                if "central_api_url" in payload:
                    central_api_url = payload["central_api_url"].strip().rstrip("/")
                    if not central_api_url:
                        raise ValueError("central API URL cannot be empty")
                    validated_payload["central_api_url"] = central_api_url
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return

            payload = validated_payload
            applicant_profile_changed = False
            try:
                with db.connect() as connection:
                    db.run_migrations(connection)
                    applicant_profile_changed = any(
                        key in payload and (get_config_value(connection, key) or "") != payload[key]
                        for key in APPLICANT_PROFILE_CONFIG_KEYS
                    )
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
                            _clean_applicant_name_part(payload[APPLICANT_FIRST_NAME_CONFIG_KEY]),
                        )
                    if APPLICANT_LAST_NAME_CONFIG_KEY in payload:
                        set_config_value(
                            connection,
                            APPLICANT_LAST_NAME_CONFIG_KEY,
                            _clean_applicant_name_part(payload[APPLICANT_LAST_NAME_CONFIG_KEY]),
                        )
                    for key in APPLICANT_PROFILE_TEXT_CONFIG_KEYS:
                        if key in payload:
                            set_config_value(
                                connection,
                                key,
                                _clean_applicant_profile_text(key, payload[key]),
                            )
                    if COVER_LETTER_MODEL_CONFIG_KEY in payload:
                        set_config_value(
                            connection,
                            COVER_LETTER_MODEL_CONFIG_KEY,
                            _clean_cover_letter_model(payload[COVER_LETTER_MODEL_CONFIG_KEY]),
                        )
                    if AUTOPREP_TAILOR_RESUME_CONFIG_KEY in payload:
                        set_config_value(
                            connection,
                            AUTOPREP_TAILOR_RESUME_CONFIG_KEY,
                            "true" if payload[AUTOPREP_TAILOR_RESUME_CONFIG_KEY] else "false",
                        )
                    for key in (
                        AUTOPREP_RESUME_PROMPT_CONFIG_KEY,
                        AUTOPREP_COVER_LETTER_PROMPT_CONFIG_KEY,
                    ):
                        if key in payload:
                            set_config_value(connection, key, _clean_autoprep_prompt(payload[key]))
                    if LLM_PROVIDER_CONFIG_KEY in payload:
                        set_config_value(
                            connection,
                            LLM_PROVIDER_CONFIG_KEY,
                            _clean_llm_provider(payload[LLM_PROVIDER_CONFIG_KEY]),
                        )

                    if SCAN_HEADLESS_CONFIG_KEY in payload:
                        set_config_value(
                            connection,
                            SCAN_HEADLESS_CONFIG_KEY,
                            "true" if payload[SCAN_HEADLESS_CONFIG_KEY] else "false",
                        )
                    if SCAN_SCHEDULE_ENABLED_CONFIG_KEY in payload:
                        set_scan_schedule_enabled(
                            connection, payload[SCAN_SCHEDULE_ENABLED_CONFIG_KEY]
                        )
                    if SCAN_SCHEDULE_TIME_CONFIG_KEY in payload:
                        set_scan_schedule_time(connection, payload[SCAN_SCHEDULE_TIME_CONFIG_KEY])
                    if "central_api_url" in payload:
                        set_central_api_url(connection, payload["central_api_url"])
                    central_passkey = _optional_text(payload.get("central_passkey"))
                    if central_passkey is not None:
                        set_central_passkey(central_passkey)
                    if applicant_profile_changed:
                        schedule_applicant_profile_reprep(connection)
            except ValueError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
                return
            except Exception as error:
                self.send_error(HTTPStatus.SERVICE_UNAVAILABLE, str(error))
                return
            SCAN_SCHEDULER.wake()
            if applicant_profile_changed:
                _schedule_applicant_profile_reprep()

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
        scan for scan in latest_scan_runs if scan.scan_status == ScanStatus.FAILED and scan.error
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


def _populate_missing_applicant_profile_from_resume() -> dict[str, str]:
    """Fill blank applicant settings from the master resume without overwriting user data."""
    with db.connect() as connection:
        db.run_migrations(connection)
        resume = get_master_resume(connection)
        missing_keys = {
            key for key in APPLICANT_PROFILE_CONFIG_KEYS if not get_config_value(connection, key)
        }
        if resume is None or not missing_keys:
            return {}
        resume_content = resume.content
        llm_settings = _llm_settings_for_generation(connection)

    try:
        extracted = asyncio.run(
            extract_applicant_profile(
                resume_content=resume_content,
                settings=llm_settings,
            )
        )
    except Exception:
        LOGGER.warning("Applicant profile extraction from resume failed", exc_info=True)
        return {}

    extracted_values = extracted.model_dump()
    config_to_field = {
        APPLICANT_FIRST_NAME_CONFIG_KEY: "first_name",
        APPLICANT_LAST_NAME_CONFIG_KEY: "last_name",
        APPLICANT_EMAIL_CONFIG_KEY: "email",
        APPLICANT_PHONE_CONFIG_KEY: "phone",
        APPLICANT_INSTITUTION_CONFIG_KEY: "institution",
        APPLICANT_DEGREE_CONFIG_KEY: "degree",
    }
    populated: dict[str, str] = {}
    with db.connect() as connection:
        db.run_migrations(connection)
        for key in missing_keys:
            if get_config_value(connection, key):
                continue
            raw_value = extracted_values[config_to_field[key]]
            try:
                value = (
                    _clean_applicant_name_part(raw_value)
                    if key in {APPLICANT_FIRST_NAME_CONFIG_KEY, APPLICANT_LAST_NAME_CONFIG_KEY}
                    else _clean_applicant_profile_text(key, raw_value)
                )
            except ValueError:
                LOGGER.warning("Ignoring invalid extracted applicant profile value for %s", key)
                continue
            if value:
                set_config_value(connection, key, value)
                populated[key] = value
        if populated:
            schedule_applicant_profile_reprep(connection)
    if populated:
        _schedule_applicant_profile_reprep()
    return populated


def _schedule_master_resume_profile_extraction() -> None:
    """Populate blank profile fields after an upload without delaying its response."""

    def populate() -> None:
        try:
            _populate_missing_applicant_profile_from_resume()
        except Exception:
            LOGGER.warning("Background applicant profile extraction failed", exc_info=True)

    threading.Thread(
        target=populate,
        name="callumployed-profile-extraction",
        daemon=True,
    ).start()


def _queue_applicant_profile_reprep() -> None:
    """Refresh every ready cover letter so it uses the latest applicant profile."""
    idempotency_key = f"applicant-profile-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%f')}"
    with db.connect() as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        result = queue_all_prepped_cover_letter_regenerations(
            connection,
            idempotency_key=idempotency_key,
        )
    if result["queued_count"]:
        LOGGER.info(
            "Queued %s cover letters after applicant profile changes",
            result["queued_count"],
        )
        _wake_autoprep_coordinator()


APPLICANT_PROFILE_REPREP_SCHEDULER = DebouncedAction(
    _queue_applicant_profile_reprep,
    delay_seconds=30,
)


def _schedule_applicant_profile_reprep() -> None:
    if AUTOPREP_COORDINATOR is not None:
        APPLICANT_PROFILE_REPREP_SCHEDULER.schedule()


def build_config_payload() -> dict[str, Any]:
    configured_llm_provider = LlmSettings().provider
    try:
        configured_llm_provider = _clean_llm_provider(configured_llm_provider)
    except ValueError:
        configured_llm_provider = DEFAULT_LLM_PROVIDER
    llm_provider = configured_llm_provider
    cover_letter_model = DEFAULT_COVER_LETTER_MODEL
    autoprep_tailor_resume = DEFAULT_AUTOPREP_TAILOR_RESUME
    autoprep_resume_prompt = DEFAULT_AUTOPREP_RESUME_PROMPT
    autoprep_cover_letter_prompt = DEFAULT_AUTOPREP_COVER_LETTER_PROMPT
    scan_headless = DEFAULT_SCAN_HEADLESS
    with db.connect() as connection:
        db.run_migrations(connection)
        values = list_config_values(connection)
        values.pop(APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY, None)
        values.pop("application_generation_backend", None)
        try:
            llm_provider = _clean_llm_provider(
                get_config_value(connection, LLM_PROVIDER_CONFIG_KEY) or configured_llm_provider
            )
        except ValueError:
            llm_provider = DEFAULT_LLM_PROVIDER
        include_graduate_degree_roles = should_include_graduate_degree_roles(connection)
        include_hardware_roles = should_include_hardware_roles(connection)
        require_software_keywords = should_require_software_keywords(connection)
        internship_mode = should_use_internship_mode(connection)
        location_filter = get_location_filter(connection)
        applicant_first_name = (
            get_config_value(
                connection,
                APPLICANT_FIRST_NAME_CONFIG_KEY,
            )
            or ""
        )
        applicant_last_name = (
            get_config_value(
                connection,
                APPLICANT_LAST_NAME_CONFIG_KEY,
            )
            or ""
        )
        applicant_email = get_config_value(connection, APPLICANT_EMAIL_CONFIG_KEY) or ""
        applicant_phone = get_config_value(connection, APPLICANT_PHONE_CONFIG_KEY) or ""
        applicant_institution = get_config_value(connection, APPLICANT_INSTITUTION_CONFIG_KEY) or ""
        applicant_degree = get_config_value(connection, APPLICANT_DEGREE_CONFIG_KEY) or ""
        try:
            cover_letter_model = _clean_cover_letter_model(
                get_config_value(connection, COVER_LETTER_MODEL_CONFIG_KEY)
                or DEFAULT_COVER_LETTER_MODEL
            )
        except ValueError:
            cover_letter_model = DEFAULT_COVER_LETTER_MODEL
        autoprep_tailor_resume = _config_bool(
            get_config_value(connection, AUTOPREP_TAILOR_RESUME_CONFIG_KEY),
            default=DEFAULT_AUTOPREP_TAILOR_RESUME,
        )
        autoprep_resume_prompt = (
            get_config_value(connection, AUTOPREP_RESUME_PROMPT_CONFIG_KEY)
            or DEFAULT_AUTOPREP_RESUME_PROMPT
        )
        autoprep_cover_letter_prompt = (
            get_config_value(connection, AUTOPREP_COVER_LETTER_PROMPT_CONFIG_KEY)
            or DEFAULT_AUTOPREP_COVER_LETTER_PROMPT
        )
        scan_headless = _config_bool(
            get_config_value(connection, SCAN_HEADLESS_CONFIG_KEY),
            default=DEFAULT_SCAN_HEADLESS,
        )
        scan_schedule_enabled, scan_schedule_time, _ = get_scan_schedule(connection)
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
                "key": APPLICANT_PHONE_CONFIG_KEY,
                "label": "phone number",
                "description": "shown below the email in the cover letter sender block",
                "control": "text",
                "input_type": "tel",
                "autocomplete": "tel",
                "value": applicant_phone,
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
                "key": LLM_PROVIDER_CONFIG_KEY,
                "label": "scan AI provider",
                "description": (
                    "used for job scanning and classification only; application documents and "
                    "saved Q&A always use OpenAI"
                ),
                "control": "select",
                "value": llm_provider,
                "default": DEFAULT_LLM_PROVIDER,
                "editable": True,
                "options": [
                    {"value": value, "label": label} for value, label in LLM_PROVIDER_OPTIONS
                ],
            },
            {
                "key": COVER_LETTER_MODEL_CONFIG_KEY,
                "label": "cover letter model",
                "description": "model used only for cover letter generation",
                "control": "select",
                "value": cover_letter_model,
                "default": DEFAULT_COVER_LETTER_MODEL,
                "editable": True,
                "options": [
                    {"value": value, "label": label} for value, label in COVER_LETTER_MODEL_OPTIONS
                ],
            },
            {
                "key": AUTOPREP_TAILOR_RESUME_CONFIG_KEY,
                "label": "tailor resumes",
                "description": (
                    "when off, Autoprep copies the master resume and only tailors the cover letter"
                ),
                "control": "toggle",
                "value": autoprep_tailor_resume,
                "default": DEFAULT_AUTOPREP_TAILOR_RESUME,
                "editable": True,
            },
            {
                "key": AUTOPREP_RESUME_PROMPT_CONFIG_KEY,
                "label": "resume prompt",
                "description": "base instructions used whenever Autoprep tailors a resume",
                "control": "textarea",
                "value": autoprep_resume_prompt,
                "default": DEFAULT_AUTOPREP_RESUME_PROMPT,
                "editable": True,
            },
            {
                "key": AUTOPREP_COVER_LETTER_PROMPT_CONFIG_KEY,
                "label": "cover letter prompt",
                "description": (
                    "base instructions used for Autoprep cover letters; indexed material is "
                    "retrieved separately and supplied to the generator"
                ),
                "control": "textarea",
                "value": autoprep_cover_letter_prompt,
                "default": DEFAULT_AUTOPREP_COVER_LETTER_PROMPT,
                "editable": True,
            },
            {
                "key": SCAN_HEADLESS_CONFIG_KEY,
                "label": "headless job scanning",
                "description": "run scan browsers without opening visible browser windows",
                "control": "toggle",
                "value": scan_headless,
                "default": DEFAULT_SCAN_HEADLESS,
                "editable": True,
            },
            {
                "key": SCAN_SCHEDULE_ENABLED_CONFIG_KEY,
                "label": "daily scan schedule",
                "description": (
                    "run one full scan each day at the configured local time; missed runs "
                    "are not started later"
                ),
                "control": "toggle",
                "value": scan_schedule_enabled,
                "default": DEFAULT_SCAN_SCHEDULE_ENABLED,
                "editable": True,
            },
            {
                "key": SCAN_SCHEDULE_TIME_CONFIG_KEY,
                "label": "daily scan time",
                "description": "local time for the automatic daily scan",
                "control": "text",
                "input_type": "time",
                "autocomplete": "off",
                "value": scan_schedule_time,
                "default": DEFAULT_SCAN_SCHEDULE_TIME,
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
                    "only applies while scanning; existing roles are unaffected unless re-filtered"
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
        agent_assisted_scan_runs = _query_count(
            connection,
            """
            SELECT COUNT(*) AS count
            FROM (
                SELECT scan_pages.scan_run_id
                FROM scan_candidates
                JOIN scan_pages ON scan_pages.id = scan_candidates.scan_page_id
                WHERE scan_candidates.discovery_method IN ('agent', 'heuristic+agent')
                UNION
                SELECT scan_run_id
                FROM role_discovery_attempts
                WHERE assessment_extraction_method = 'llm'
                UNION
                SELECT id AS scan_run_id
                FROM scan_runs
                WHERE agent_trace IS NOT NULL AND TRIM(agent_trace) != ''
            ) AS assisted_scan_runs
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
            _metric("agent-assisted scan runs", agent_assisted_scan_runs),
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
                    _metric("agent-assisted scan runs", agent_assisted_scan_runs),
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

    ordered_statuses: list[str] = [
        status.value for status in RoleStatus if status.value in node_statuses
    ]
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
        "cover_letter_examples": [_cover_letter_example_summary(example) for example in examples]
    }


def build_experience_notes_payload() -> dict[str, Any]:
    with db.connect() as connection:
        notes = list_experience_notes(connection)
    return {"experience_notes": [_experience_note_summary(note) for note in notes]}


def build_application_materials_payload() -> dict[str, Any]:
    resume: MasterResume | None = None
    examples: list[CoverLetterExample] = []
    notes: list[ExperienceNote] = []
    with db.connect() as connection:
        resume = get_master_resume(connection)
        examples = list_cover_letter_examples(connection)
        notes = list_experience_notes(connection)
    payload = _application_materials_payload(resume, examples, notes)
    # Existing material libraries created before automatic refresh are repaired on
    # their next read, so the UI never leaves the user with a manual index task.
    if payload["material_index"]["needs_index"]:
        _refresh_application_material_index()
        payload = _application_materials_payload(resume, examples, notes)
    return payload


def _refresh_application_material_index() -> dict[str, Any]:
    """Atomically refresh the local material index after any source mutation."""
    notes: list[ExperienceNote] = []
    with db.connect() as connection:
        notes = list_experience_notes(connection)
    return build_material_index([_experience_note_index_source(note) for note in notes])


def build_autoprep_interested_payload() -> dict[str, Any]:
    with db.connect() as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        roles = list_interested_autoprep_roles(connection)
    for role in roles:
        role_id = role.get("id")
        role["manual_prep_started"] = bool(
            isinstance(role_id, int) and _role_has_prep_started(role_id)
        )
        role["selectable"] = role.get("preparation_status") is None
    return {"roles": roles}


def build_prepped_roles_payload() -> dict[str, Any]:
    jobs: list[dict[str, Any]] = []
    bulk_regeneration: dict[str, Any] | None = None
    with db.connect() as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        jobs = list_autoprep_jobs(connection)
        for job in jobs:
            role = get_role(connection, int(job["role_id"]))
            role_payload = role.model_dump(mode="json")
            role_payload["company_name"] = str(job.get("company_name") or "")
            resolved_role = _role_with_effective_company(role_payload)
            job["company_name"] = resolved_role["company_name"]
            job["title"] = resolved_role["title"]
            job["location"] = resolved_role["location"]
        bulk_regeneration = get_latest_bulk_cover_letter_regeneration(connection)
    return {
        "jobs": jobs,
        "bulk_cover_letter_regeneration": bulk_regeneration,
    }


def _wake_autoprep_coordinator() -> None:
    if AUTOPREP_COORDINATOR is not None:
        AUTOPREP_COORDINATOR.wake()


def _process_autoprep_job(job_id: int) -> None:
    with db.connect() as connection:
        ensure_autoprep_schema(connection)
        job = get_autoprep_job(connection, job_id)
        role = get_role(connection, int(job["role_id"]))
        company = get_company(connection, role.company_id)
        resume = get_master_resume(connection)
    if resume is None:
        raise RuntimeError("No master resume is stored.")
    role_payload = role.model_dump(mode="json")
    role_payload["company_name"] = company.name
    role_payload = _role_with_effective_company(role_payload)

    if job["resume_status"] == "queued":
        try:
            _prepare_autoprep_resume(job_id, role, role_payload, resume)
        except Exception as error:  # noqa: BLE001 - keep cover-letter work independent.
            LOGGER.exception("Autoprep resume failed for role %s", role.id)
            with db.connect() as connection:
                mark_autoprep_document(
                    connection,
                    job_id,
                    "resume",
                    "failed",
                    error=_autoprep_error(error),
                )

    with db.connect() as connection:
        job = get_autoprep_job(connection, job_id)
    if job["cover_letter_status"] == "queued":
        try:
            _prepare_autoprep_cover_letter(job_id, role_payload, resume)
        except Exception as error:  # noqa: BLE001 - preserve a completed resume.
            LOGGER.exception("Autoprep cover letter failed for role %s", role.id)
            with db.connect() as connection:
                mark_autoprep_document(
                    connection,
                    job_id,
                    "cover_letter",
                    "failed",
                    error=_autoprep_error(error),
                )
    with db.connect() as connection:
        finish_autoprep_worker(connection, job_id)


def generate_saved_application_answer(role_id: int, *, question: str) -> dict[str, Any]:
    role: dict[str, Any] = {}
    with db.connect() as connection:
        db.run_migrations(connection)
        ensure_autoprep_schema(connection)
        role_model = get_role(connection, role_id)
        company = get_company(connection, role_model.company_id)
        role = role_model.model_dump(mode="json")
        role["company_name"] = company.name
        role = _role_with_effective_company(role)
        effective_company_name = str(role["company_name"])
        resume = get_master_resume(connection)
        notes = list_experience_notes(connection)
        examples = list_cover_letter_examples(connection)
        sync_role_context_vectors(connection, role=role_model, company_name=effective_company_name)
        role_context = retrieve_role_context(
            connection,
            role_id=role_id,
            query=f"{role_model.title} {effective_company_name} {question}",
            limit=20,
        )
        llm_settings = _llm_settings_for_generation(connection)
        job = get_role_autoprep_job(connection, role_id)
    if resume is None:
        raise RuntimeError("No master resume is stored.")
    tailored_resume = str((job or {}).get("resume_latex") or "") or None
    saved_cover_letter = _saved_role_cover_letter(role_id)
    cover_letter = str((saved_cover_letter or {}).get("latex") or "") or None
    experience_sections = [
        {
            "source_id": section.source_id,
            "source_filename": section.source_filename,
            "title": section.title,
            "content": section.content,
        }
        for note in notes
        for section in split_experience_note(note.model_dump(mode="json"))
    ]
    prompt = build_application_prompt(
        task="answer_question",
        role=role,
        question=question,
        master_resume=resume.content,
        tailored_resume=tailored_resume,
        cover_letter=cover_letter,
        cover_letter_examples=[example.model_dump(mode="json") for example in examples],
        experience_sections=experience_sections,
        role_context=role_context,
    )
    response = asyncio.run(
        generate_role_chat(
            role=role,
            resume_content=tailored_resume or resume.content,
            cover_letter_content=cover_letter,
            employment_history_context=experience_sections,
            messages=parse_role_chat_messages([{"role": "user", "content": prompt}]),
            settings=llm_settings,
        )
    )
    return {
        "answer": response.answer,
        "sources": [
            {
                "kind": "saved_material",
                "title": "Callumployed saved application materials",
                "url": None,
            }
        ],
        "research": {"used_web": False, "policy": "saved-material facts only"},
    }


def _prepare_autoprep_resume(
    job_id: int,
    role: Role,
    role_payload: dict[str, Any],
    resume: MasterResume,
) -> None:
    """Tailor the resume or publish the unchanged master copy, according to Settings."""
    instruction = ""
    previous_latex: str | None = None
    current_job: dict[str, Any] = {}
    tailor_resume = DEFAULT_AUTOPREP_TAILOR_RESUME
    configured_prompt = DEFAULT_AUTOPREP_RESUME_PROMPT
    with db.connect() as connection:
        current_job = get_autoprep_job(connection, job_id)
        instruction = str(current_job.get("resume_instruction") or "").strip()
        previous_latex = get_autoprep_resume_latex(connection, job_id)
        tailor_resume = _config_bool(
            get_config_value(connection, AUTOPREP_TAILOR_RESUME_CONFIG_KEY),
            default=DEFAULT_AUTOPREP_TAILOR_RESUME,
        )
        configured_prompt = (
            get_config_value(connection, AUTOPREP_RESUME_PROMPT_CONFIG_KEY) or configured_prompt
        )
        mark_autoprep_document(
            connection,
            job_id,
            "resume",
            "regenerating" if instruction else "generating_tweaks",
        )
    if tailor_resume:
        tweaks = _autoprep_generation_prompt(configured_prompt, instruction)
        generated = build_role_resume(
            role_payload,
            resume,
            tweaks=tweaks,
            previous_latex=previous_latex if instruction else None,
            required_page_count=1,
        )
    else:
        generated = save_role_resume(
            role_payload,
            resume,
            resume.content,
            required_page_count=1,
        )
    source_pdf = _required_generated_pdf(generated, "resume")
    artifact_directory, artifact_path = _copy_autoprep_pdf(
        role_payload,
        source_pdf,
        kind="resume",
        existing_job=current_job,
    )
    counterpart = _copy_autoprep_counterpart(
        role_payload,
        current_job,
        artifact_directory,
        generated_kind="resume",
    )
    latex = str(generated.get("latex") or "")
    with db.connect() as connection:
        if counterpart is not None:
            _, counterpart_path = counterpart
            mark_autoprep_document(
                connection,
                job_id,
                "cover_letter",
                "ready",
                artifact_path=counterpart_path,
                artifact_directory=str(artifact_directory),
                commit=False,
            )
        mark_autoprep_document(
            connection,
            job_id,
            "resume",
            "ready",
            artifact_path=str(artifact_path),
            artifact_directory=str(artifact_directory),
            resume_latex=latex or None,
        )
        clear_autoprep_instruction(connection, job_id, "resume")


def _prepare_autoprep_cover_letter(
    job_id: int,
    role_payload: dict[str, Any],
    resume: MasterResume,
) -> None:
    """Generate through Callumployed's configured LangChain provider only.

    Role requirements enter the generator only through the documented, local
    role-context retrieval projection in ``build_role_cover_letter``.
    """
    instruction = ""
    tailored_resume_latex: str | None = None
    current_job: dict[str, Any] = {}
    configured_prompt = DEFAULT_AUTOPREP_COVER_LETTER_PROMPT
    with db.connect() as connection:
        current_job = get_autoprep_job(connection, job_id)
        instruction = str(current_job.get("cover_letter_instruction") or "").strip()
        tailored_resume_latex = get_autoprep_resume_latex(connection, job_id)
        configured_prompt = (
            get_config_value(connection, AUTOPREP_COVER_LETTER_PROMPT_CONFIG_KEY)
            or configured_prompt
        )
        mark_autoprep_document(connection, job_id, "cover_letter", "generating")
    role_id = int(role_payload["id"])
    resume_for_generation = MasterResume(
        filename=resume.filename,
        content=tailored_resume_latex or resume.content,
        content_sha256=resume.content_sha256,
    )
    previous_cover_letter = _saved_role_cover_letter(role_id) if instruction else None
    generated = build_role_cover_letter(
        role_payload,
        resume_for_generation,
        tweaks=_autoprep_generation_prompt(configured_prompt, instruction),
        previous_cover_letter_latex=(str((previous_cover_letter or {}).get("latex") or "") or None),
        allow_local_fallback=True,
        required_page_count=1,
    )
    source_pdf = _required_generated_pdf(generated, "cover letter")
    page_count = len(PdfReader(str(source_pdf)).pages)
    if page_count != 1:
        raise RuntimeError(
            f"Generated cover letter did not fit exactly one PDF page ({page_count} pages)."
        )
    artifact_directory, artifact_path = _copy_autoprep_pdf(
        role_payload,
        source_pdf,
        kind="cover-letter",
        existing_job=current_job,
    )
    counterpart = _copy_autoprep_counterpart(
        role_payload,
        current_job,
        artifact_directory,
        generated_kind="cover-letter",
    )
    with db.connect() as connection:
        if counterpart is not None:
            _, counterpart_path = counterpart
            mark_autoprep_document(
                connection,
                job_id,
                "resume",
                "ready",
                artifact_path=counterpart_path,
                artifact_directory=str(artifact_directory),
                commit=False,
            )
        mark_autoprep_document(
            connection,
            job_id,
            "cover_letter",
            "ready",
            artifact_path=str(artifact_path),
            artifact_directory=str(artifact_directory),
        )
        clear_autoprep_instruction(connection, job_id, "cover_letter")
    LOGGER.info(
        "Autoprep cover letter completed through direct LangChain generation for role %s",
        role_id,
    )


def _cover_letter_examples_for_prompt(
    role: dict[str, Any],
    resume_content: str,
    experience_context: list[dict[str, object]],
) -> list[dict[str, object]]:
    experience_text = " ".join(str(item.get("content") or "") for item in experience_context)
    queries = [
        " ".join(
            [
                str(role.get("title") or ""),
                str(role.get("description") or ""),
                resume_content,
                experience_text,
            ]
        ),
        " ".join(
            [
                str(role.get("title") or ""),
                str(role.get("company_name") or ""),
                str(role.get("location") or ""),
            ]
        ),
    ]
    examples_by_id: dict[int, dict[str, object]] = {}
    with db.connect() as connection:
        for query in queries:
            for example in list_cover_letter_example_knowledge(connection, query=query, limit=3):
                example_id = example.get("id")
                if isinstance(example_id, int):
                    examples_by_id[example_id] = example
    return list(examples_by_id.values())


def _required_generated_pdf(generated: dict[str, Any], label: str) -> Path:
    pdf_value = generated.get("pdf_path")
    if not isinstance(pdf_value, str):
        raise RuntimeError(f"Generated {label} did not include a PDF.")
    pdf_path = Path(pdf_value)
    if not pdf_path.is_file() or pdf_path.stat().st_size <= 0:
        raise RuntimeError(f"Generated {label} PDF could not be verified.")
    return pdf_path


def _copy_autoprep_pdf(
    role: dict[str, Any],
    source_pdf: Path,
    *,
    kind: str,
    existing_job: dict[str, Any] | None = None,
) -> tuple[Path, Path]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Autoprep role did not include an ID.")
    company = _safe_filename(_effective_role_company_name(role))
    title = _safe_filename(str(role.get("title") or "role"))
    directory = _existing_autoprep_directory(existing_job or {}, role_id)
    if directory is None:
        directory = _prepared_applications_root() / f"{company}-{title}-role-{role_id}"
    directory.mkdir(parents=True, exist_ok=True)
    suffix = "resume" if kind == "resume" else "cover-letter"
    artifact_field = "resume_artifact_path" if kind == "resume" else "cover_letter_artifact_path"
    existing_artifact = (existing_job or {}).get(artifact_field)
    target = directory / f"{company}-{title}-{suffix}.pdf"
    if isinstance(existing_artifact, str):
        candidate = Path(existing_artifact).resolve()
        if candidate.parent == directory.resolve() and candidate.suffix.lower() == ".pdf":
            target = candidate
    _atomic_copy_verified_pdf(source_pdf, target)
    return directory, target


def _prepared_applications_root() -> Path:
    return user_data_path("callumployed", appauthor=False) / "prepared-applications"


def _currently_applying_directory() -> Path:
    return _prepared_applications_root() / "currently-applying"


def _existing_autoprep_directory(job: dict[str, Any], role_id: int) -> Path | None:
    directory_value = job.get("artifact_directory")
    if not isinstance(directory_value, str):
        return None
    directory = Path(directory_value).resolve()
    root = _prepared_applications_root().resolve()
    if (
        directory.parent != root
        or not directory.name.endswith(f"-role-{role_id}")
        or not directory.is_dir()
    ):
        return None
    return directory


def _atomic_copy_verified_pdf(source_pdf: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, suffix=".pdf", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        shutil.copyfile(source_pdf, temporary_path)
        try:
            valid_pdf = temporary_path.stat().st_size > 0 and bool(
                PdfReader(str(temporary_path)).pages
            )
        except Exception as error:
            raise RuntimeError("Prepared PDF copy could not be verified.") from error
        if not valid_pdf:
            raise RuntimeError("Prepared PDF copy could not be verified.")
        temporary_path.replace(target)
        if not target.is_file() or target.stat().st_size <= 0 or not PdfReader(str(target)).pages:
            raise RuntimeError("Prepared PDF could not be verified after its atomic write.")
    finally:
        temporary_path.unlink(missing_ok=True)


def _copy_autoprep_counterpart(
    role: dict[str, Any],
    job: dict[str, Any],
    directory: Path,
    *,
    generated_kind: str,
) -> tuple[str, str] | None:
    counterpart_kind = "cover_letter" if generated_kind == "resume" else "resume"
    if job.get(f"{counterpart_kind}_status") != "ready":
        return None
    source_value = job.get(f"{counterpart_kind}_artifact_path")
    if not isinstance(source_value, str):
        return None
    source = Path(source_value)
    if not source.is_file():
        return None
    if source.resolve().parent == directory.resolve():
        target = source.resolve()
    else:
        company = _safe_filename(_effective_role_company_name(role))
        title = _safe_filename(str(role.get("title") or "role"))
        suffix = "cover-letter" if counterpart_kind == "cover_letter" else "resume"
        target = directory / f"{company}-{title}-{suffix}.pdf"
    if source.resolve() != target.resolve():
        _atomic_copy_verified_pdf(source, target)
    return counterpart_kind, str(target)


def _ready_autoprep_document_pair(job: dict[str, Any]) -> tuple[int, Path, Path]:
    role_id = job.get("role_id")
    if not isinstance(role_id, int):
        raise ValueError("Prepared role does not have a valid ID.")
    if job.get("resume_status") != "ready" or job.get("cover_letter_status") != "ready":
        raise ValueError("Both documents must be ready before selecting this role.")
    directory = _existing_autoprep_directory(job, role_id)
    if directory is None:
        raise FileNotFoundError("The selected role's documents folder is not available.")
    paths: list[Path] = []
    for field, label in (
        ("resume_artifact_path", "resume"),
        ("cover_letter_artifact_path", "cover letter"),
    ):
        value = job.get(field)
        if not isinstance(value, str):
            raise FileNotFoundError(f"The selected role's {label} is not available.")
        path = Path(value).resolve()
        if path.parent != directory or path.suffix.lower() != ".pdf" or not path.is_file():
            raise FileNotFoundError(f"The selected role's {label} is not available.")
        if path.stat().st_size <= 0 or not PdfReader(str(path)).pages:
            raise RuntimeError(f"The selected role's {label} PDF is invalid.")
        paths.append(path)
    if paths[0].name == paths[1].name:
        raise RuntimeError("Prepared document filenames must be distinct.")
    return role_id, paths[0], paths[1]


def _exchange_directories_atomically(first: Path, second: Path) -> None:
    """Atomically exchange two directories on supported local platforms."""
    library = ctypes.CDLL(None, use_errno=True)
    first_bytes = os.fsencode(first)
    second_bytes = os.fsencode(second)
    if sys.platform == "darwin":
        renamex_np = library.renamex_np
        renamex_np.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        renamex_np.restype = ctypes.c_int
        result = renamex_np(first_bytes, second_bytes, 0x00000002)
    elif sys.platform.startswith("linux") and hasattr(library, "renameat2"):
        renameat2 = library.renameat2
        renameat2.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        renameat2.restype = ctypes.c_int
        result = renameat2(-100, first_bytes, -100, second_bytes, 0x00000002)
    else:
        raise RuntimeError("Atomic directory exchange is not supported on this platform.")
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), str(first), str(second))


def _sync_currently_applying_folder(job: dict[str, Any]) -> dict[str, object]:
    root = _prepared_applications_root()
    root.mkdir(parents=True, exist_ok=True)
    destination = _currently_applying_directory()
    with CURRENTLY_APPLYING_LOCK:
        backup = root / ".currently-applying-previous"
        if backup.exists() and not destination.exists():
            if not backup.is_dir() or backup.is_symlink():
                raise RuntimeError("Currently Applying recovery path is not a directory.")
            backup.replace(destination)
        role_id, resume, cover_letter = _ready_autoprep_document_pair(job)
        temporary = Path(tempfile.mkdtemp(prefix=".currently-applying-", dir=root))
        try:
            _atomic_copy_verified_pdf(resume, temporary / resume.name)
            _atomic_copy_verified_pdf(cover_letter, temporary / cover_letter.name)
            if len(list(temporary.iterdir())) != 2:
                raise RuntimeError("Currently Applying must contain exactly two documents.")
            if destination.exists():
                if not destination.is_dir() or destination.is_symlink():
                    raise RuntimeError("Currently Applying path is not a safe directory.")
                _exchange_directories_atomically(destination, temporary)
            else:
                temporary.replace(destination)
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)
    return {
        "role_id": role_id,
        "path": str(destination.resolve()),
        "filenames": [resume.name, cover_letter.name],
    }


_SELF_IDENTIFIED_EMPLOYER_PATTERNS = (
    re.compile(
        r"(?im)^\s*(?:who are we\??|about us)\s*:?\s*(?:\r?\n)+\s*"
        r"(?P<name>[A-Z][A-Za-z0-9&.'’+\-/]*(?:[ \t]+[A-Z][A-Za-z0-9&.'’+\-/]*){0,5})"
        r"\s+(?:is|are)\b"
    ),
    re.compile(
        r"(?im)^\s*about\s+"
        r"(?P<name>[A-Z][A-Za-z0-9&.'’+\-/]*(?:[ \t]+[A-Z][A-Za-z0-9&.'’+\-/]*){0,5})"
        r"\s*:?\s*(?:\r?\n)+\s*(?P=name)\s+(?:is|are)\b"
    ),
)


def _effective_role_company_name(role: dict[str, Any]) -> str:
    """Resolve only explicit employer self-identification in approved role text."""
    fallback = str(role.get("company_name") or "company").strip() or "company"
    description = role.get("description")
    if not isinstance(description, str) or not description.strip():
        return fallback
    for pattern in _SELF_IDENTIFIED_EMPLOYER_PATTERNS:
        match = pattern.search(description[:4000])
        if match is None:
            continue
        candidate = " ".join(match.group("name").split()).strip(" .,:;–—-")
        generic_headings = {
            "we",
            "us",
            "the company",
            "our company",
            "the role",
            "this role",
            "the job",
            "this job",
            "the team",
            "this team",
            "engineering",
            "product",
            "sales",
            "marketing",
            "technology",
            "the opportunity",
            "the position",
            "you",
        }
        if candidate.casefold() not in generic_headings:
            return candidate
    return fallback


def _explicit_posting_title_and_location(role: dict[str, Any]) -> tuple[str | None, str | None]:
    description = role.get("description")
    if not isinstance(description, str) or not description.strip():
        return None, None
    lines = description.splitlines()
    title: str | None = None
    location: str | None = None
    for index, line in enumerate(lines):
        title_match = re.match(r"(?i)^\s*position title\s*:\s*(.+?)\s*$", line)
        if title_match is not None:
            title_parts = [
                re.split(
                    r"(?i)\s+(?=(?:location|responsibilities|anticipated start date|"
                    r"contract duration|work hours)\s*:)",
                    title_match.group(1),
                    maxsplit=1,
                )[0]
            ]
            if index + 2 < len(lines) and re.match(
                r"(?i)^\s*location\s*:",
                lines[index + 2],
            ):
                continuation = lines[index + 1].strip()
                if continuation and not continuation.startswith("#") and ":" not in continuation:
                    title_parts.append(continuation)
            title = " ".join(" ".join(title_parts).split())
        location_match = re.match(r"(?i)^\s*location\s*:\s*(.+?)\s*$", line)
        if location_match is not None:
            location = " ".join(location_match.group(1).split())
    return title, location


def _role_with_effective_company(role: dict[str, Any]) -> dict[str, Any]:
    resolved = dict(role)
    resolved["company_name"] = _effective_role_company_name(role)
    resolved["title"] = unquote(str(role.get("title") or "this role"))
    explicit_title, explicit_location = _explicit_posting_title_and_location(role)
    if explicit_title:
        resolved["title"] = explicit_title
    if explicit_location:
        resolved["location"] = explicit_location
    return resolved


def _autoprep_error(error: Exception) -> str:
    detail = " ".join(str(error).strip().split())
    return (detail or "Autoprep generation failed.")[-1000:]


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

    feedback_items: list[dict[str, str | None]] = []
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


def _publish_reliable_cover_letter_fallback(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    applicant_profile: ApplicantProfile,
    experience_context: list[dict[str, object]],
    tweaks: str | None,
    required_page_count: int | None,
) -> dict[str, Any]:
    role_id = role.get("id")
    fallback_latex = _normalize_cover_letter_latex(
        _fallback_cover_letter_latex(
            role,
            resume,
            applicant_profile=applicant_profile,
            other_experience_context=experience_context,
        ),
        hiring_contact=find_named_hiring_contact(role.get("description")),
        role_title=str(role.get("title") or ""),
    )
    try:
        return _write_role_cover_letter(
            role,
            fallback_latex,
            source="local_cover_letter_fallback",
            example_ids=[],
            tweaks=tweaks,
            required_page_count=required_page_count,
            minimum_page_fill_ratio=None,
            minimum_body_word_count=None,
            maximum_body_word_count=300,
        )
    except Exception:
        existing = _existing_one_page_cover_letter_fallback(role, tweaks=tweaks)
        if existing is not None:
            LOGGER.exception(
                "Cover letter fallback failed for role %s; retaining prior artifact",
                role_id,
            )
            return existing
        raise


def build_role_cover_letter(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    tweaks: str | None = None,
    previous_cover_letter_latex: str | None = None,
    allow_local_fallback: bool = True,
    required_page_count: int | None = 1,
) -> dict[str, Any]:
    """Generate with the configured LangChain provider and role-local SQLite retrieval."""
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")

    applicant_profile = ApplicantProfile()
    experience_notes: list[ExperienceNote] = []
    experience_context: list[dict[str, object]] = []
    role_context: list[dict[str, object]] = []
    cover_letter_model = DEFAULT_COVER_LETTER_MODEL
    llm_settings = LlmSettings(model=cover_letter_model)
    fallback_role = _role_with_effective_company(role)
    role_for_prompt = dict(fallback_role)
    role_for_prompt.pop("description", None)

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
            authoritative_role = get_role(connection, role_id)
            company = get_company(connection, authoritative_role.company_id)
            fallback_role = authoritative_role.model_dump(mode="json")
            fallback_role["company_name"] = company.name
            fallback_role = _role_with_effective_company(fallback_role)
            sync_role_context_vectors(
                connection,
                role=authoritative_role,
                company_name=company.name,
            )
            role_context = retrieve_role_context(
                connection,
                role_id=role_id,
                query=" ".join(
                    filter(
                        None,
                        [
                            str(role_for_prompt.get("title") or ""),
                            str(role_for_prompt.get("company_name") or company.name),
                            str(role_for_prompt.get("location") or ""),
                            str(tweaks or ""),
                        ],
                    )
                ),
                limit=4,
            )
            experience_notes = list_experience_notes(connection)
            applicant_profile = _load_applicant_profile(connection)
            try:
                cover_letter_model = _clean_cover_letter_model(
                    get_config_value(connection, COVER_LETTER_MODEL_CONFIG_KEY)
                    or DEFAULT_COVER_LETTER_MODEL
                )
            except ValueError:
                cover_letter_model = DEFAULT_COVER_LETTER_MODEL
            llm_settings = _llm_settings_for_generation(
                connection,
                model=cover_letter_model,
            )
        experience_context = _generation_experience_context(
            experience_notes,
            role=role_for_prompt,
            tweaks=tweaks,
        )
        draft = asyncio.run(
            generate_cover_letter(
                role=role_for_prompt,
                resume_content=resume.content,
                search_tool=search_cover_letters,
                applicant_profile=applicant_profile,
                other_experience_context=experience_context,
                role_context=role_context,
                tweaks=tweaks,
                previous_cover_letter_latex=previous_cover_letter_latex,
                settings=llm_settings,
            )
        )
        latex = _normalize_cover_letter_latex(
            draft.latex,
            hiring_contact=find_named_hiring_contact(role_for_prompt.get("description")),
            role_title=str(role_for_prompt.get("title") or ""),
        )
        example_ids = draft.example_ids
        source = "ai_cover_letter"
    except Exception:
        if not allow_local_fallback:
            raise
        LOGGER.exception("AI cover letter generation failed for role %s", role_id)
        return _publish_reliable_cover_letter_fallback(
            fallback_role,
            resume,
            applicant_profile=applicant_profile,
            experience_context=experience_context,
            tweaks=tweaks,
            required_page_count=required_page_count,
        )

    for attempt in range(3):
        try:
            written = _write_role_cover_letter(
                role_for_prompt,
                latex,
                source=source,
                example_ids=example_ids,
                tweaks=tweaks,
                required_page_count=required_page_count,
                minimum_page_fill_ratio=None,
                minimum_body_word_count=None,
                maximum_body_word_count=300,
            )
            return written
        except Exception as error:  # noqa: BLE001 - generated output must fall back safely.
            if attempt == 2 or source != "ai_cover_letter":
                return _publish_reliable_cover_letter_fallback(
                    fallback_role,
                    resume,
                    applicant_profile=applicant_profile,
                    experience_context=experience_context,
                    tweaks=tweaks,
                    required_page_count=required_page_count,
                )
            if isinstance(error, GeneratedDocumentLengthError):
                retry_tweaks = (
                    f"{tweaks or ''}\n\n"
                    f"The cover letter body was {error.word_count} words. Tighten the smooth, "
                    "source-supported prose to no more than 300 words. "
                    "Do not add filler, dump resume bullets, combine unrelated experiences, or "
                    "invent facts."
                )
            elif isinstance(error, GeneratedDocumentLayoutError):
                retry_tweaks = (
                    f"{tweaks or ''}\n\n"
                    "The compiled cover letter layout could not be validated. Keep it concise and "
                    "complete without adding filler, dumping resume bullets, or combining "
                    "unrelated work."
                )
            elif isinstance(error, GeneratedDocumentPageCountError):
                retry_tweaks = (
                    f"{tweaks or ''}\n\n"
                    "The compiled cover letter exceeded one page. Return a complete letter that "
                    "fits within one PDF page. Preserve all applicant facts and the role-specific "
                    "rationale. Tighten prose and remove repetition only; never truncate text or "
                    "invent facts."
                )
            elif isinstance(error, GeneratedDocumentQualityError):
                retry_tweaks = (
                    f"{tweaks or ''}\n\n"
                    "The previous draft exposed internal evidence-index metadata. Rewrite it as "
                    "natural first-person applicant prose. Never include labels such as Tools, "
                    "Useful attributes, Evidence, Repository-verified, or User-confirmed."
                )
            else:
                retry_tweaks = (
                    f"{tweaks or ''}\n\n"
                    "The previous LaTeX draft did not compile or publish correctly. Return a "
                    "complete document using the exact supplied scaffold, valid escaped text, and "
                    "no unsupported packages or commands. Keep it concise and at most one page."
                )
            try:
                draft = asyncio.run(
                    generate_cover_letter(
                        role=role_for_prompt,
                        resume_content=resume.content,
                        search_tool=search_cover_letters,
                        applicant_profile=applicant_profile,
                        other_experience_context=experience_context,
                        role_context=role_context,
                        tweaks=retry_tweaks,
                        previous_cover_letter_latex=latex,
                        settings=llm_settings,
                    )
                )
                draft_latex = draft.latex
                example_ids = draft.example_ids
            except Exception:
                LOGGER.exception("AI cover letter repair failed for role %s", role_id)
                return _publish_reliable_cover_letter_fallback(
                    fallback_role,
                    resume,
                    applicant_profile=applicant_profile,
                    experience_context=experience_context,
                    tweaks=tweaks,
                    required_page_count=required_page_count,
                )
            latex = _normalize_cover_letter_latex(
                draft_latex,
                hiring_contact=find_named_hiring_contact(role_for_prompt.get("description")),
                role_title=str(role_for_prompt.get("title") or ""),
            )
    raise AssertionError("bounded cover letter generation loop did not return")


def _load_applicant_profile(connection: Any) -> ApplicantProfile:
    return ApplicantProfile(
        first_name=get_config_value(connection, APPLICANT_FIRST_NAME_CONFIG_KEY) or "",
        last_name=get_config_value(connection, APPLICANT_LAST_NAME_CONFIG_KEY) or "",
        email=get_config_value(connection, APPLICANT_EMAIL_CONFIG_KEY) or "",
        phone=get_config_value(connection, APPLICANT_PHONE_CONFIG_KEY) or "",
        institution=get_config_value(connection, APPLICANT_INSTITUTION_CONFIG_KEY) or "",
        degree=get_config_value(connection, APPLICANT_DEGREE_CONFIG_KEY) or "",
    )


def save_role_cover_letter(role: dict[str, Any], latex: str) -> dict[str, Any]:
    return _write_role_cover_letter(
        role,
        _normalize_cover_letter_latex(
            latex,
            hiring_contact=find_named_hiring_contact(role.get("description")),
            role_title=str(role.get("title") or ""),
        ),
        source="edited_cover_letter",
        example_ids=[],
        tweaks=None,
    )


class GeneratedDocumentPageCountError(RuntimeError):
    pass


class GeneratedDocumentLayoutError(RuntimeError):
    pass


class GeneratedDocumentLengthError(RuntimeError):
    def __init__(self, word_count: int, minimum: int, maximum: int) -> None:
        self.word_count = word_count
        self.minimum = minimum
        self.maximum = maximum
        super().__init__(
            f"Generated cover letter body was {word_count} words; "
            f"required range: {minimum}-{maximum}."
        )


class GeneratedDocumentQualityError(RuntimeError):
    pass


_COVER_LETTER_INTERNAL_METADATA_PATTERNS = (
    re.compile(r"(?i)\b(?:I\s+)?tools\s*:"),
    re.compile(r"(?i)\b(?:I\s+)?useful attributes\s*:"),
    re.compile(r"(?im)^\s*(?:I\s+)?evidence\s*:"),
    re.compile(r"(?i)\brepository-verified\s*:"),
    re.compile(r"(?i)\buser-confirmed\s*:"),
)


def _validate_cover_letter_quality(latex: str) -> None:
    plain_text = _plain_text_from_latex(latex)
    if any(
        pattern.search(candidate)
        for pattern in _COVER_LETTER_INTERNAL_METADATA_PATTERNS
        for candidate in (latex, plain_text)
    ):
        raise GeneratedDocumentQualityError(
            "Generated cover letter leaked internal evidence metadata into applicant prose."
        )


def _validate_cover_letter_quality_for_source(latex: str, *, source: str) -> None:
    if source != "edited_cover_letter":
        _validate_cover_letter_quality(latex)


def _pdf_page_fill_ratio(pdf_path: Path) -> float | None:
    reader = PdfReader(str(pdf_path))
    if len(reader.pages) != 1:
        return None
    page = reader.pages[0]
    weighted_text_y_positions: list[float] = []

    def collect_text_position(
        text: str,
        current_transform: list[float],
        text_transform: list[float],
        _font: Any,
        _font_size: float,
    ) -> None:
        visible_text = text.strip()
        if visible_text:
            text_x = float(text_transform[4])
            text_y = float(text_transform[5])
            transformed_y = (
                text_x * float(current_transform[1])
                + text_y * float(current_transform[3])
                + float(current_transform[5])
            )
            weighted_text_y_positions.extend([transformed_y] * len(visible_text))

    page.extract_text(visitor_text=collect_text_position)
    if len(weighted_text_y_positions) < 2:
        return None
    page_height = float(page.mediabox.height)
    if page_height <= 0:
        return None
    ordered_positions = sorted(weighted_text_y_positions)
    last_index = len(ordered_positions) - 1
    lower_y = ordered_positions[int(last_index * 0.01)]
    upper_y = ordered_positions[int(last_index * 0.99)]
    return min(1.0, max(0.0, (upper_y - lower_y) / page_height))


def _latex_command_arguments(
    latex: str,
    command: str,
    argument_count: int,
) -> list[tuple[str, ...]]:
    results: list[tuple[str, ...]] = []
    marker = f"\\{command}"
    cursor = 0
    while (start := latex.find(marker, cursor)) >= 0:
        position = start + len(marker)
        arguments: list[str] = []
        for _ in range(argument_count):
            while position < len(latex) and latex[position].isspace():
                position += 1
            if position >= len(latex) or latex[position] != "{":
                break
            depth = 1
            argument_start = position + 1
            position += 1
            while position < len(latex) and depth:
                if latex[position] == "{" and latex[position - 1] != "\\":
                    depth += 1
                elif latex[position] == "}" and latex[position - 1] != "\\":
                    depth -= 1
                position += 1
            if depth:
                break
            arguments.append(latex[argument_start : position - 1])
        if len(arguments) == argument_count:
            results.append(tuple(arguments))
        cursor = start + len(marker)
    return results


def _normalized_latex_arguments(arguments: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(re.sub(r"\s+", " ", argument).strip() for argument in arguments)


def _missing_source_resume_entries(source_latex: str, candidate_latex: str) -> list[str]:
    """Protect experience identities while deliberately allowing stronger rewritten bullets."""
    missing: list[str] = []
    for command, argument_count in (
        ("section", 1),
        ("resumeProjectHeading", 2),
        ("resumeSubheading", 4),
        ("resumeSubSubheading", 2),
    ):
        source_units = Counter(
            _normalized_latex_arguments(arguments)
            for arguments in _latex_command_arguments(source_latex, command, argument_count)
        )
        candidate_units = Counter(
            _normalized_latex_arguments(arguments)
            for arguments in _latex_command_arguments(candidate_latex, command, argument_count)
        )
        for arguments, count in (source_units - candidate_units).items():
            missing.extend([f"\\{command}{{{arguments[0]}}}"] * count)
    for command, argument_count in (("href", 2), ("url", 1)):
        source_links = Counter(
            _normalized_latex_arguments((arguments[0],))
            for arguments in _latex_command_arguments(source_latex, command, argument_count)
        )
        candidate_links = Counter(
            _normalized_latex_arguments((arguments[0],))
            for arguments in _latex_command_arguments(candidate_latex, command, argument_count)
        )
        for arguments, count in (source_links - candidate_links).items():
            missing.extend([f"\\{command}{{{arguments}}}"] * count)
    return missing


def _commit_resume_artifact_pair(
    *,
    staged_tex: Path,
    staged_pdf: Path,
    target_tex: Path,
    target_pdf: Path,
    backup_dir: Path,
) -> None:
    backup_tex = backup_dir / "previous.tex"
    backup_pdf = backup_dir / "previous.pdf"
    backups: list[tuple[Path, Path]] = []
    installed: list[Path] = []
    try:
        for target, backup in ((target_tex, backup_tex), (target_pdf, backup_pdf)):
            if target.exists():
                os.replace(target, backup)
                backups.append((target, backup))
        os.replace(staged_tex, target_tex)
        installed.append(target_tex)
        os.replace(staged_pdf, target_pdf)
        installed.append(target_pdf)
    except Exception:
        for target in reversed(installed):
            target.unlink(missing_ok=True)
        for target, backup in reversed(backups):
            if backup.exists():
                os.replace(backup, target)
        raise
    finally:
        staged_tex.unlink(missing_ok=True)
        staged_pdf.unlink(missing_ok=True)
        backup_tex.unlink(missing_ok=True)
        backup_pdf.unlink(missing_ok=True)


def _one_page_resume_candidates(latex: str) -> list[str]:
    modest_profile = (
        "\\addtolength{\\topmargin}{-0.12in}\n"
        "\\addtolength{\\textheight}{0.28in}\n"
        "\\setlength{\\parskip}{0pt}\n"
    )
    compact = (
        latex.replace("\\fontsize{9.5pt}{11pt}", "\\fontsize{9pt}{10pt}")
        .replace("\\fontsize{10pt}{11.5pt}", "\\fontsize{9.5pt}{10.5pt}")
        .replace("\\vspace{-2pt}", "\\vspace{-3pt}")
    )
    compact_profile = (
        "\\addtolength{\\topmargin}{-0.18in}\n"
        "\\addtolength{\\textheight}{0.42in}\n"
        "\\setlength{\\parskip}{0pt}\n"
    )
    aggressive = (
        latex.replace("letterpaper,11pt", "letterpaper,10pt")
        .replace("\\fontsize{9.5pt}{11pt}", "\\fontsize{8.5pt}{9.5pt}")
        .replace("\\fontsize{10pt}{11.5pt}", "\\fontsize{9pt}{10pt}")
        .replace("\\vspace{-2pt}", "\\vspace{-4pt}")
    )
    aggressive_profile = (
        "\\addtolength{\\topmargin}{-0.24in}\n"
        "\\addtolength{\\textheight}{0.58in}\n"
        "\\setlength{\\parskip}{0pt}\n"
        "\\linespread{0.94}\\selectfont\n"
    )

    candidates = [latex]
    for content, profile in (
        (latex, modest_profile),
        (compact, compact_profile),
        (aggressive, aggressive_profile),
    ):
        if "\\begin{document}" in content:
            candidate = content.replace("\\begin{document}", f"{profile}\\begin{{document}}", 1)
        else:
            candidate = f"{profile}{content}"
        if candidate not in candidates:
            candidates.append(candidate)
    emergency = _emergency_one_page_resume_candidate(aggressive)
    if emergency not in candidates:
        candidates.append(emergency)
    return candidates


def _emergency_one_page_resume_candidate(latex: str) -> str:
    """Keep all source content while applying one final bounded whole-page fit."""
    begin_marker = "\\begin{document}"
    end_marker = "\\end{document}"
    if begin_marker not in latex or end_marker not in latex:
        return latex
    preamble, document = latex.split(begin_marker, 1)
    body, suffix = document.rsplit(end_marker, 1)
    if "\\usepackage{graphicx}" not in preamble:
        documentclass = re.search(r"\\documentclass(?:\[[^\]]*\])?\{[^}]+\}", preamble)
        if documentclass is not None:
            insert_at = documentclass.end()
            preamble = (
                f"{preamble[:insert_at]}\n\\usepackage{{graphicx}}"
                f"{preamble[insert_at:]}"
            )
    fitted_body = (
        "\n% callumployed emergency one-page fit\n"
        "\\pagestyle{empty}\n"
        "\\noindent\\raisebox{0pt}[0pt][0pt]{%\n"
        "\\resizebox{\\textwidth}{0.90\\textheight}{%\n"
        "\\begin{minipage}{\\textwidth}\n"
        f"{body.strip()}\n"
        "\\end{minipage}%\n"
        "}}\\par\n"
        "\\vspace*{0.90\\textheight}\n"
    )
    return f"{preamble}{begin_marker}{fitted_body}{end_marker}{suffix}"


def save_role_resume(
    role: dict[str, Any],
    resume: MasterResume,
    latex: str,
    *,
    required_page_count: int | None = None,
    minimum_page_fill_ratio: float | None = None,
) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")
    resume_path = _role_resume_tex_path(role_id)
    resume_path.parent.mkdir(parents=True, exist_ok=True)
    compiler = shutil.which("tectonic") or shutil.which("latexmk") or shutil.which("pdflatex")
    if compiler is None:
        raise RuntimeError("No LaTeX compiler found. Install tectonic, latexmk, or pdflatex.")

    with tempfile.TemporaryDirectory(
        prefix=f".callumployed-resume-{role_id}-",
        dir=resume_path.parent,
    ) as temp_dir:
        candidate_path = Path(temp_dir) / "resume.tex"
        _copy_resume_resources_to_directory(candidate_path.parent)
        selected_latex: str | None = None
        selected_pdf: Path | None = None
        page_counts: list[int] = []
        page_fill_ratios: list[float | None] = []
        candidates = _one_page_resume_candidates(latex) if required_page_count == 1 else [latex]
        for candidate_latex in candidates:
            candidate_path.write_text(candidate_latex)
            candidate_pdf = _compile_role_resume_pdf(
                role=role,
                role_id=role_id,
                compiler=compiler,
                resume_path=candidate_path,
                copy_to_downloads=False,
            )
            pages = PdfReader(str(candidate_pdf)).pages if candidate_pdf.is_file() else []
            page_count = len(pages)
            page_counts.append(page_count)
            page_fill_ratio = _pdf_page_fill_ratio(candidate_pdf) if page_count == 1 else None
            page_fill_ratios.append(page_fill_ratio)
            if page_count and (required_page_count is None or page_count == required_page_count):
                if minimum_page_fill_ratio is not None and (
                    page_fill_ratio is None or page_fill_ratio < minimum_page_fill_ratio
                ):
                    continue
                selected_latex = candidate_latex
                selected_pdf = candidate_pdf
                break
        if selected_latex is None or selected_pdf is None:
            one_page_attempted = 1 in page_counts
            if minimum_page_fill_ratio is not None and one_page_attempted:
                measured_fill_ratios = [ratio for ratio in page_fill_ratios if ratio is not None]
                if not measured_fill_ratios:
                    raise GeneratedDocumentLayoutError(
                        "Generated resume page fill could not be measured; refusing to publish."
                    )
                raise GeneratedDocumentLayoutError(
                    "Generated resume was materially underfilled "
                    f"(page fill attempts: {[round(ratio, 3) for ratio in measured_fill_ratios]}; "
                    f"minimum: {minimum_page_fill_ratio:.3f})."
                )
            if required_page_count is not None:
                raise GeneratedDocumentPageCountError(
                    "Generated resume did not fit exactly "
                    f"{required_page_count} PDF page (attempts: {page_counts})."
                )
            raise RuntimeError("Generated role resume PDF could not be verified.")

        staged_tex = Path(temp_dir) / "selected.tex"
        staged_pdf = Path(temp_dir) / "selected.pdf"
        staged_tex.write_text(selected_latex)
        shutil.copyfile(selected_pdf, staged_pdf)
        _commit_resume_artifact_pair(
            staged_tex=staged_tex,
            staged_pdf=staged_pdf,
            target_tex=resume_path,
            target_pdf=resume_path.with_suffix(".pdf"),
            backup_dir=Path(temp_dir),
        )
    _sync_resume_resources_to_role(role_id)
    return _saved_role_resume(role, resume)


def _source_resume_fallback(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    required_page_count: int,
    tweaks: str,
    summary: str,
) -> dict[str, Any]:
    try:
        generated = save_role_resume(
            role,
            resume,
            resume.content,
            required_page_count=required_page_count,
        )
    except Exception:
        role_id = role.get("id")
        if not isinstance(role_id, int):
            raise
        resume_path = _role_resume_tex_path(role_id)
        pdf_path = _current_role_resume_pdf_path(resume_path)
        if (
            not resume_path.is_file()
            or pdf_path is None
            or not _artifact_pair_is_current_page_count(
                resume_path,
                pdf_path,
                required_page_count=required_page_count,
            )
        ):
            raise
        LOGGER.exception(
            "Source resume fallback failed for role %s; retaining last one-page artifact",
            role_id,
        )
        return {
            "role_id": role_id,
            "source": "existing_resume_fallback",
            "summary": "Retained the last verified one-page resume after generation failed.",
            "latex": resume_path.read_text(),
            "tweaks": tweaks,
            "path": str(resume_path),
            "pdf_path": str(pdf_path),
            "pdf_base64": base64.b64encode(pdf_path.read_bytes()).decode(),
        }
    return {
        **generated,
        "source": "source_resume_fallback",
        "summary": summary,
        "tweaks": tweaks,
    }


def _artifact_pair_is_current_page_count(
    tex_path: Path,
    pdf_path: Path,
    *,
    required_page_count: int,
) -> bool:
    try:
        return (
            tex_path.is_file()
            and pdf_path.is_file()
            and pdf_path.stat().st_mtime_ns >= tex_path.stat().st_mtime_ns
            and len(PdfReader(str(pdf_path)).pages) == required_page_count
        )
    except Exception:  # noqa: BLE001 - unreadable artifacts cannot be trusted as fallbacks.
        return False


def _existing_one_page_cover_letter_fallback(
    role: dict[str, Any],
    *,
    tweaks: str | None,
) -> dict[str, Any] | None:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        return None
    cover_letter_path = _role_cover_letter_tex_path(role_id)
    pdf_path = cover_letter_path.with_suffix(".pdf")
    if not _artifact_pair_is_current_page_count(
        cover_letter_path,
        pdf_path,
        required_page_count=1,
    ):
        return None
    return {
        "role_id": role_id,
        "source": "existing_cover_letter_fallback",
        "summary": "Retained the last verified one-page cover letter after generation failed.",
        "latex": cover_letter_path.read_text(),
        "example_ids": [],
        "tweaks": tweaks,
        "path": str(cover_letter_path),
        "pdf_path": str(pdf_path),
        "pdf_base64": base64.b64encode(pdf_path.read_bytes()).decode(),
    }


def build_role_resume(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    tweaks: str,
    previous_latex: str | None = None,
    required_page_count: int = 1,
) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")
    source_latex = previous_latex or _ensure_role_resume_copy(role_id, resume).read_text()
    authoritative_latex = resume.content
    experience_notes: list[ExperienceNote] = []
    llm_settings = LlmSettings()
    with db.connect() as connection:
        db.run_migrations(connection)
        experience_notes = list_experience_notes(connection)
        llm_settings = _llm_settings_for_generation(connection)
    experience_context = _generation_experience_context(
        experience_notes,
        role=role,
        tweaks=tweaks,
    )
    candidate_source = source_latex
    candidate_tweaks = tweaks
    for attempt in range(3):
        try:
            draft = asyncio.run(
                generate_resume_tweak(
                    role=role,
                    resume_content=candidate_source,
                    tweaks=candidate_tweaks,
                    other_experience_context=experience_context,
                    settings=llm_settings,
                )
            )
        except Exception:  # noqa: BLE001 - always publish a bounded source-based artifact.
            LOGGER.exception("AI resume generation failed for role %s", role_id)
            return _source_resume_fallback(
                role,
                resume,
                required_page_count=required_page_count,
                tweaks=tweaks,
                summary=(
                    "Preserved and fitted the complete source resume because AI generation "
                    "was unavailable."
                ),
            )

        missing_experience = _missing_source_resume_entries(
            authoritative_latex,
            draft.latex,
        )
        if missing_experience:
            if attempt == 2:
                return _source_resume_fallback(
                    role,
                    resume,
                    required_page_count=required_page_count,
                    tweaks=tweaks,
                    summary=(
                        "Preserved and fitted the complete source resume because the generated "
                        "draft omitted an employer, project, education entry, date, or section."
                    ),
                )
            candidate_source = authoritative_latex
            candidate_tweaks = (
                f"{tweaks}\n\n"
                "The previous draft was rejected because it removed a source employer, project, "
                "education entry, date, or section. Keep every source entry and identity, but "
                "actively rewrite its bullets for relevance, clarity, and smoothness. Select the "
                "strongest source-supported accomplishments without inventing facts or awkwardly "
                "combining unrelated experiences. Use balanced writing and layout to fill one page."
            )
            continue

        try:
            generated = save_role_resume(
                role,
                resume,
                draft.latex,
                required_page_count=required_page_count,
            )
        except Exception:
            if attempt == 2:
                return _source_resume_fallback(
                    role,
                    resume,
                    required_page_count=required_page_count,
                    tweaks=tweaks,
                    summary=(
                        "Preserved and fitted the complete source resume because the tailored "
                        "draft did not fit one page without content loss."
                    ),
                )
            candidate_source = authoritative_latex
            candidate_tweaks = (
                f"{tweaks}\n\n"
                "The generated resume failed one-page layout validation. Keep every employer, "
                "project, education entry, date, and section, while rewriting bullets naturally. "
                "If sparse, add useful source-supported specificity and improve readable spacing. "
                "If crowded, tighten wording within each experience. Never invent facts or combine "
                "unrelated experiences merely to fit the page."
            )
            continue
        return {
            **generated,
            "summary": draft.summary or "Regenerated resume with tweaks.",
            "tweaks": tweaks,
        }
    raise AssertionError("bounded resume generation loop did not return")


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
        "employment_history_context": [_experience_note_context(note) for note in experience_notes],
    }


def _one_page_cover_letter_candidates(latex: str) -> list[str]:
    candidates = [latex]
    for margin, parskip, font_size, line_spread in (
        ("1in", "1.05em", None, "1.08"),
        ("1in", "1.2em", None, "1.12"),
        ("0.85in", "0.7em", None, None),
        ("0.75in", "0.55em", "10pt", None),
    ):
        candidate = re.sub(
            r"\\usepackage\[margin=[^\]]+\]\{geometry\}",
            rf"\\usepackage[margin={margin}]{{geometry}}",
            latex,
            count=1,
        )
        candidate = re.sub(
            r"\\setlength\{\\parskip\}\{[^}]+\}",
            rf"\\setlength{{\\parskip}}{{{parskip}}}",
            candidate,
            count=1,
        )
        if font_size is not None:
            candidate = re.sub(
                r"\\documentclass(?:\[[^\]]*\])?\{letter\}",
                rf"\\documentclass[{font_size}]{{letter}}",
                candidate,
                count=1,
            )
        if line_spread is not None:
            candidate = candidate.replace(
                "\\begin{document}",
                f"\\linespread{{{line_spread}}}\\selectfont\n\\begin{{document}}",
                1,
            )
        if candidate not in candidates:
            candidates.append(candidate)
    return candidates


def _cover_letter_body_word_count(latex: str) -> int:
    if "\\begin{document}" not in latex or "\\end{document}" not in latex:
        return 0
    document = latex.split("\\begin{document}", 1)[1].split("\\end{document}", 1)[0]
    salutation = re.search(
        r"(?im)^\s*(?:"
        r"\\opening\{Dear\s+[^{}\n]+,?\}"
        r"|(?:\\noindent\s+)?Dear\s+[^,\n]+,\s*(?:\\par)?"
        r")\s*",
        document,
    )
    if salutation is None:
        return 0
    body = document[salutation.end() :]
    closing = re.search(
        r"(?im)^\s*(?:"
        r"\\closing\{(?:Sincerely|Best regards|Regards|Respectfully|Warm regards)[,:]?\}"
        r"|(?:\\noindent\s+)?"
        r"(?:Sincerely|Best regards|Regards|Respectfully|Warm regards)[,:]?"
        r")\s*",
        body,
    )
    if closing is None:
        return 0
    body = body[: closing.start()]
    body = re.sub(r"(?m)(?<!\\)%.*$", "", body)
    body = re.sub(r"\\(?:vspace|hspace)\*?\{[^{}]*\}", " ", body)
    body = re.sub(r"\\[A-Za-z@]+(?:\[[^\]]*\])?", " ", body)
    body = re.sub(r"\\([%&#_$])", r"\1", body)
    return len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", body))


def _write_role_cover_letter(
    role: dict[str, Any],
    latex: str,
    *,
    source: str,
    example_ids: list[int],
    tweaks: str | None,
    required_page_count: int | None = None,
    minimum_page_fill_ratio: float | None = None,
    minimum_body_word_count: int | None = None,
    maximum_body_word_count: int | None = None,
) -> dict[str, Any]:
    role_id = role.get("id")
    if not isinstance(role_id, int):
        raise RuntimeError("Role did not include an ID")
    summary = _cover_letter_display_summary(
        role,
        source=source,
        example_count=len(example_ids),
    )
    _validate_cover_letter_quality_for_source(latex, source=source)
    body_word_count = _cover_letter_body_word_count(latex)
    too_short = minimum_body_word_count is not None and body_word_count < minimum_body_word_count
    too_long = maximum_body_word_count is not None and body_word_count > maximum_body_word_count
    if too_short or too_long:
        raise GeneratedDocumentLengthError(
            body_word_count,
            minimum_body_word_count or 0,
            maximum_body_word_count or body_word_count,
        )

    cover_letter_path = _role_cover_letter_tex_path(role_id)
    cover_letter_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".callumployed-cover-letter-{role_id}-",
        dir=cover_letter_path.parent,
    ) as temp_dir:
        candidate_path = Path(temp_dir) / "cover-letter.tex"
        selected_latex: str | None = None
        selected_pdf: Path | None = None
        selected_pdf_base64 = ""
        page_counts: list[int] = []
        page_fill_ratios: list[float | None] = []
        candidates = (
            _one_page_cover_letter_candidates(latex) if required_page_count == 1 else [latex]
        )
        for candidate_latex in candidates:
            candidate_path.write_text(candidate_latex)
            candidate_pdf, pdf_base64 = _generate_cover_letter_pdf_preview(candidate_path)
            page_count = len(PdfReader(str(candidate_pdf)).pages)
            page_counts.append(page_count)
            page_fill_ratio = _pdf_page_fill_ratio(candidate_pdf) if page_count == 1 else None
            page_fill_ratios.append(page_fill_ratio)
            if required_page_count is None or page_count == required_page_count:
                if minimum_page_fill_ratio is not None and (
                    page_fill_ratio is None or page_fill_ratio < minimum_page_fill_ratio
                ):
                    continue
                selected_latex = candidate_latex
                selected_pdf = candidate_pdf
                selected_pdf_base64 = pdf_base64
                break
        if selected_latex is None or selected_pdf is None:
            one_page_fill_ratios = [
                ratio
                for page_count, ratio in zip(page_counts, page_fill_ratios, strict=True)
                if page_count == 1 and ratio is not None
            ]
            if minimum_page_fill_ratio is not None and 1 in page_counts:
                raise GeneratedDocumentLayoutError(
                    "Generated cover letter was materially underfilled "
                    f"(page fill attempts: {[round(ratio, 3) for ratio in one_page_fill_ratios]}; "
                    f"minimum: {minimum_page_fill_ratio:.3f})."
                )
            raise GeneratedDocumentPageCountError(
                "Generated cover letter did not fit exactly "
                f"{required_page_count} PDF page (attempts: {page_counts})."
            )

        staged_tex = Path(temp_dir) / "selected.tex"
        staged_pdf = Path(temp_dir) / "selected.pdf"
        staged_tex.write_text(selected_latex)
        shutil.copyfile(selected_pdf, staged_pdf)
        _commit_resume_artifact_pair(
            staged_tex=staged_tex,
            staged_pdf=staged_pdf,
            target_tex=cover_letter_path,
            target_pdf=cover_letter_path.with_suffix(".pdf"),
            backup_dir=Path(temp_dir),
        )
    pdf_path = cover_letter_path.with_suffix(".pdf")
    return {
        "role_id": role_id,
        "source": source,
        "summary": summary,
        "latex": selected_latex,
        "example_ids": example_ids,
        "tweaks": tweaks,
        "path": str(cover_letter_path),
        "pdf_path": str(pdf_path),
        "pdf_base64": selected_pdf_base64,
    }


def _normalize_cover_letter_latex(
    latex: str,
    *,
    hiring_contact: str | None = None,
    role_title: str | None = None,
) -> str:
    content = _normalize_cover_letter_text_characters(latex.strip())
    content = _strip_cover_letter_em_dashes(content)
    content = _strip_resume_pdf_compatibility_commands(content)
    content = _strip_generated_cover_letter_comments(content)
    content = _escape_unescaped_latex_percent(content)
    content = _escape_unescaped_latex_ampersands(content)
    content = _repair_single_cover_letter_line_breaks(content)
    content = _normalize_cover_letter_salutation(content, hiring_contact=hiring_contact)
    content = re.sub(
        r"(?:\\vspace\{0\.35em\}\s*){2,}",
        "\\\\vspace{0.35em}\n\n",
        content,
    )
    content = _normalize_cover_letter_closing(content)
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
    content = _ensure_cover_letter_role_title_header(content, role_title=role_title)
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
            marker in normalized for marker in ("http://", "https://", r"\url{", r"\href{http")
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
    content = re.sub(r"\\(?:ex)?hyphenpenalty\s*=\s*\d+\s*", "", content)
    content = re.sub(r"\\setlength\{\\emergencystretch\}\{[^}]*\}\s*", "", content)
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
        "\\setlength{\\parskip}{0.55em}\n"
        "\\setlength{\\parindent}{1.5em}\n"
        "\\hyphenpenalty=10000\n"
        "\\exhyphenpenalty=10000\n"
        "\\setlength{\\emergencystretch}{2em}\n"
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


def _normalize_cover_letter_salutation(latex: str, *, hiring_contact: str | None = None) -> str:
    resolved_contact = hiring_contact or "Hiring Manager"
    content = re.sub(
        r"\\opening\{Dear\s+[^{}]+,?\}",
        lambda _match: f"\\opening{{Dear {resolved_contact},}}",
        latex,
        count=1,
        flags=re.IGNORECASE,
    )
    salutation_pattern = re.compile(
        r"(?m)^[ \t]*(?:\\noindent[ \t]+)?"
        r"(?P<salutation>Dear[ \t]+[^,\n{}]{1,100})"
        r"(?:[,;:](?:[ \t]*\\par)?[ \t]*(?P<body>[^\n]*)|[ \t]*(?=$))",
        flags=re.IGNORECASE,
    )

    def replace_salutation(match: re.Match[str]) -> str:
        salutation = f"Dear {resolved_contact}"
        rendered = f"\\noindent {salutation},\\par\n\\vspace{{0.35em}}"
        body = (match.group("body") or "").strip()
        return f"{rendered}\n\n{body}" if body else rendered

    return salutation_pattern.sub(replace_salutation, content, count=1)


def _normalize_cover_letter_closing(latex: str) -> str:
    return re.sub(
        r"(?mi)^[ \t]*(?:\\noindent[ \t]+)?(Sincerely|Best regards|Kind regards),",
        r"\\noindent \1,",
        latex,
        count=1,
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


def _ensure_cover_letter_role_title_header(latex: str, *, role_title: str | None) -> str:
    title = " ".join(str(role_title or "").split())
    if not title:
        return latex

    escaped_title = _escape_latex_role_title(title)
    document_start = latex.find("\\begin{document}")
    salutation_match = re.search(r"(?:\\noindent\s+)?Dear\s+|\\opening\{", latex)
    header_end = salutation_match.start() if salutation_match is not None else len(latex)
    header_start = document_start if document_start >= 0 else 0

    date_pattern = re.compile(
        r"(?m)^(?P<indent>[ \t]*)(?P<date>"
        r"(?:(?:January|February|March|April|May|June|July|August|September|October|"
        r"November|December)\s+\d{1,2},\s+\d{4}|\\today)"
        r"(?P<suffix>\\par)?[ \t]*)$"
    )
    date_matches = list(date_pattern.finditer(latex, header_start, header_end))
    if not date_matches:
        return latex
    date_match = date_matches[-1]
    recipient_start = max(
        header_start,
        latex.rfind("\\vspace", header_start, date_match.start()),
        latex.rfind("\\noindent", header_start, date_match.start()),
        latex.rfind("\\begin{tabular}", header_start, date_match.start()),
    )
    if escaped_title in latex[recipient_start : date_match.start()]:
        return latex

    title_line = f"{date_match.group('indent')}{escaped_title}\\\\\n"
    return latex[: date_match.start()] + title_line + latex[date_match.start() :]


def _escape_latex_role_title(value: str) -> str:
    escaped = value.replace("\\", r"\textbackslash{}")
    for character, replacement in (
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
    ):
        escaped = escaped.replace(character, replacement)
    return escaped


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
        _ensure_role_resume_copy(role_id, resume) if ensure_copy else _role_resume_tex_path(role_id)
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


def _publish_saved_cover_letter_pair(
    cover_letter_path: Path,
    latex: str,
) -> None:
    with tempfile.TemporaryDirectory(
        prefix=f".{cover_letter_path.stem}-refresh-",
        dir=cover_letter_path.parent,
    ) as temp_dir:
        staged_tex = Path(temp_dir) / "selected.tex"
        staged_tex.write_text(latex)
        staged_pdf, _ = _generate_cover_letter_pdf_preview(staged_tex)
        _commit_resume_artifact_pair(
            staged_tex=staged_tex,
            staged_pdf=staged_pdf,
            target_tex=cover_letter_path,
            target_pdf=cover_letter_path.with_suffix(".pdf"),
            backup_dir=Path(temp_dir),
        )


def _saved_role_cover_letter(role_id: int) -> dict[str, Any] | None:
    cover_letter_path = _role_cover_letter_tex_path(role_id)
    if not cover_letter_path.exists():
        return None
    saved_latex = cover_letter_path.read_text()
    normalized_latex = _normalize_cover_letter_latex(saved_latex)
    pdf_path = cover_letter_path.with_suffix(".pdf")
    pdf_is_stale = (
        pdf_path.exists() and pdf_path.stat().st_mtime_ns < cover_letter_path.stat().st_mtime_ns
    )
    if normalized_latex != saved_latex or not pdf_path.exists() or pdf_is_stale:
        with suppress(Exception):
            _publish_saved_cover_letter_pair(cover_letter_path, normalized_latex)
    current_latex = cover_letter_path.read_text()
    pdf_is_current = (
        pdf_path.exists() and pdf_path.stat().st_mtime_ns >= cover_letter_path.stat().st_mtime_ns
    )
    pdf_base64 = base64.b64encode(pdf_path.read_bytes()).decode() if pdf_is_current else None
    return {
        "role_id": role_id,
        "source": "saved_cover_letter",
        "summary": "Saved cover letter for this role.",
        "latex": current_latex,
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
        return (
            f"Drafted reliable fallback cover letter for {role_label}; "
            "the generated draft could not be published."
        )
    if source == "edited_cover_letter":
        return f"Saved edited cover letter for {role_label}."
    if example_count > 0:
        examples = f"{example_count} stored cover letter example"
        if example_count != 1:
            examples += "s"
        return (
            f"Drafted cover letter for {role_label} using resume, job description, and {examples}."
        )
    return f"Drafted cover letter for {role_label} using resume and job description."


_FALLBACK_CAPABILITIES = (
    (
        "enterprise AI products",
        ("enterprise ai", "machine learning", "nlp", "foundation model", "ai models"),
    ),
    ("an API platform", ("api", "apis")),
    (
        "scalable services and infrastructure",
        ("scalable", "infrastructure", "scaling", "distributed", "cloud"),
    ),
    ("data pipelines", ("data pipeline", "pipelines", "data processing")),
    ("security", ("security", "secure", "authentication", "authorization", "oidc")),
    ("developer tooling and CI/CD", ("tooling", "ci/cd", "developer tools", "utilities")),
    ("testing and reliability", ("testing", "tests", "reliability", "performance")),
    ("frontend and backend product development", ("frontend", "backend", "full-stack")),
)


def _plain_text_from_latex(value: str) -> str:
    text = value
    text = re.sub(r"\\href\{[^{}]*\}\{([^{}]*)\}", r"\1", text)
    for _ in range(4):
        updated = re.sub(
            r"\\(?:textbf|textit|underline|emph|small)\{([^{}]*)\}",
            r"\1",
            text,
        )
        if updated == text:
            break
        text = updated
    text = re.sub(r"\\[A-Za-z@]+(?:\[[^\]]*\])?", " ", text)
    text = text.replace(r"\%", "%").replace(r"\&", "&").replace("--", "-")
    text = text.replace("{", " ").replace("}", " ")
    return " ".join(text.split()).strip(" -;,")


def _fallback_role_priorities(role: dict[str, Any]) -> list[str]:
    role_text = " ".join(
        str(role.get(key) or "") for key in ("title", "description")
    ).casefold()
    return [
        label
        for label, patterns in _FALLBACK_CAPABILITIES
        if any(pattern in role_text for pattern in patterns)
    ]


_FALLBACK_EVIDENCE_START_PATTERN = re.compile(
    r"(?i)^(?:I|My)\b|^(?:"
    r"Added|Architected|Automated|Built|Collaborated|Configured|Contributed|Created|"
    r"Delivered|Deployed|Designed|Developed|Diagnosed|Ensured|Implemented|Improved|"
    r"Increased|Integrated|Led|Maintained|Managed|Migrated|Optimized|Owned|Reduced|"
    r"Refactored|Resolved|Strengthened|Supported|Tested|Worked"
    r")\b"
)


def _is_fallback_evidence_candidate(candidate: str) -> bool:
    return (
        40 <= len(candidate) <= 320
        and candidate.endswith((".", "!", "?"))
        and bool(_FALLBACK_EVIDENCE_START_PATTERN.match(candidate))
        and not any(
            pattern.search(candidate)
            for pattern in _COVER_LETTER_INTERNAL_METADATA_PATTERNS
        )
    )


def _fallback_source_evidence_sentences(content: str) -> list[str]:
    source_marker = "## Source details"
    if source_marker in content:
        content = content.split(source_marker, 1)[1]
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", content) if part.strip()]
    sentences: list[str] = []
    for paragraph in paragraphs:
        if paragraph.lstrip().startswith("#"):
            continue
        reflowed = " ".join(
            line.lstrip("#-* ").strip() for line in paragraph.splitlines() if line.strip()
        )
        for sentence in re.split(r"(?<=[.!?])\s+", reflowed):
            candidate = " ".join(sentence.split()).strip()
            if _is_fallback_evidence_candidate(candidate):
                sentences.append(candidate)
    return sentences


def _fallback_cover_letter_evidence(
    role: dict[str, Any],
    resume: MasterResume,
    other_experience_context: list[dict[str, Any]] | None,
) -> list[str]:
    candidates = [
        _plain_text_from_latex(arguments[0])
        for arguments in _latex_command_arguments(resume.content, "resumeItem", 1)
    ]
    for item in other_experience_context or []:
        candidates.extend(
            _fallback_source_evidence_sentences(str(item.get("content") or ""))
        )
    candidates = list(
        dict.fromkeys(
            candidate
            for candidate in candidates
            if candidate and _is_fallback_evidence_candidate(candidate)
        )
    )
    role_terms = _prep_keywords(
        " ".join(str(role.get(key) or "") for key in ("title", "description"))
    )
    active_capabilities = [
        patterns
        for label, patterns in _FALLBACK_CAPABILITIES
        if label in _fallback_role_priorities(role)
    ]

    def score(candidate: str) -> tuple[int, int]:
        candidate_text = candidate.casefold()
        overlap = len(role_terms & _prep_keywords(candidate))
        capability_matches = sum(
            1
            for patterns in active_capabilities
            if any(pattern in candidate_text for pattern in patterns)
        )
        return (overlap * 2 + capability_matches * 5, -len(candidate))

    ranked = sorted(
        enumerate(candidates),
        key=lambda item: (score(item[1]), -item[0]),
        reverse=True,
    )
    relevant = [candidate for _index, candidate in ranked if score(candidate)[0] > 0]
    if len(relevant) < 4:
        relevant.extend(candidate for candidate in candidates if candidate not in relevant)
    return relevant[:4]


def _first_person_evidence_sentence(value: str) -> str:
    sentence = value.strip().rstrip(".!?")
    if not sentence:
        return "I have delivered source-supported software engineering work"
    if re.match(r"(?i)^(?:I|My)\b", sentence):
        return sentence
    return f"I {sentence[0].lower()}{sentence[1:]}"


def _joined_priority_text(priorities: list[str]) -> str:
    selected = priorities[:3]
    if not selected:
        return "reliable, user-focused software engineering"
    if len(selected) == 1:
        return selected[0]
    if len(selected) == 2:
        return f"{selected[0]} and {selected[1]}"
    return f"{selected[0]}, {selected[1]}, and {selected[2]}"


def _fallback_cover_letter_latex(
    role: dict[str, Any],
    resume: MasterResume,
    *,
    applicant_profile: ApplicantProfile,
    other_experience_context: list[dict[str, Any]] | None = None,
) -> str:
    title = str(role.get("title") or "this role")
    company = str(role.get("company_name") or "your team")
    location = str(role.get("location") or "").strip()
    location_line = f"{location}\\\\\n" if location else ""
    priorities = _fallback_role_priorities(role)
    priority_text = _joined_priority_text(priorities)
    evidence = _fallback_cover_letter_evidence(role, resume, other_experience_context)
    evidence_sentences = [_first_person_evidence_sentence(item) for item in evidence]
    primary_evidence = ". ".join(evidence_sentences[:2])
    if primary_evidence:
        primary_evidence += "."
    else:
        primary_evidence = (
            "My application is grounded only in the experience documented in my resume."
        )
    secondary_evidence = ". ".join(evidence_sentences[2:4])
    if secondary_evidence:
        secondary_evidence += ". "
    return (
        "\\documentclass[letterpaper,11pt]{article}\n"
        "\\usepackage[margin=1in]{geometry}\n"
        "\\usepackage[hidelinks]{hyperref}\n"
        "\\setlength{\\parskip}{0.55em}\n"
        "\\setlength{\\parindent}{1.5em}\n"
        "\\pagestyle{empty}\n"
        "\\begin{document}\n"
        f"\\noindent {applicant_profile.latex_sender_block}\\par\n"
        "\\vspace{1.1em}\n"
        f"\\noindent {company}\\\\\n"
        f"{location_line}"
        f"{title}\\\\\n"
        "\\today\\par\n"
        "\\vspace{1.1em}\n\n"
        "\\noindent Dear Hiring Manager,\\par\n"
        "\\vspace{0.35em}\n\n"
        f"I am applying for the {title} position at {company}. The opportunity to work on "
        f"{priority_text} is a strong match for the concrete engineering work documented in my "
        "resume. I would bring hands-on experience building, testing, and improving production "
        "software across those areas.\n\n"
        f"{primary_evidence} These projects required me to turn "
        "specific product and platform requirements into maintainable implementations while "
        "checking the resulting behavior and reliability.\n\n"
        f"{secondary_evidence}I would apply the same practical, "
        f"evidence-driven approach to {company}'s work across {priority_text}. Thank you for "
        "considering my "
        "application. I would welcome an interview to discuss how this experience can contribute "
        "to the team.\n\n"
        "\\vspace{0.35em}\n"
        "\\noindent Sincerely,\\\\[12pt]\n"
        f"{applicant_profile.full_name}\n"
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
        if len(word) >= 4
        and any(character.isalpha() for character in word)
        and word not in ignored_terms
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


def _config_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _llm_settings_for_generation(
    _connection: Any,
    *,
    model: str | None = None,
) -> LlmSettings:
    environment_settings = LlmSettings()
    return LlmSettings(
        provider="openai",
        model=model or environment_settings.model,
        codex_model=environment_settings.codex_model,
        openai_api_key=environment_settings.openai_api_key,
    )


def _clean_llm_provider(value: object) -> str:
    provider = str(value or "").strip().lower()
    if provider not in SUPPORTED_LLM_PROVIDERS:
        expected = ", ".join(sorted(SUPPORTED_LLM_PROVIDERS))
        raise ValueError(f"llm_provider must be one of: {expected}")
    return provider


def _clean_cover_letter_model(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("Cover letter model must be text")
    cleaned = value.strip()
    if cleaned not in SUPPORTED_COVER_LETTER_MODELS:
        raise ValueError("Choose a supported cover letter model")
    return cleaned


def _clean_autoprep_prompt(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("Autoprep prompts must be text")
    cleaned = value.strip()
    if len(cleaned) > 8_000:
        raise ValueError("Autoprep prompts must be 8,000 characters or fewer")
    return cleaned


def _autoprep_generation_prompt(base_prompt: str, feedback: str) -> str:
    cleaned_base = _clean_autoprep_prompt(base_prompt)
    cleaned_feedback = feedback.strip()
    if not cleaned_feedback:
        return cleaned_base
    return (
        f"{cleaned_base}\n\nUser feedback for this specific document version:\n{cleaned_feedback}"
    )


def _configured_browser_profile_manager() -> BrowserProfileManager:
    headless = DEFAULT_SCAN_HEADLESS
    with db.connect() as connection:
        db.run_migrations(connection)
        headless = _config_bool(
            get_config_value(connection, SCAN_HEADLESS_CONFIG_KEY),
            default=DEFAULT_SCAN_HEADLESS,
        )
    return BrowserProfileManager(headless=headless)


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
    if key == APPLICANT_PHONE_CONFIG_KEY and cleaned:
        if re.search(r"[^0-9+().\- ]", cleaned):
            raise ValueError("Applicant phone number contains unsupported characters")
        digit_count = sum(character.isdigit() for character in cleaned)
        if not 7 <= digit_count <= 15:
            raise ValueError("Applicant phone number must contain 7 to 15 digits")
    return cleaned


def _is_valid_company_tier(value: str | None) -> bool:
    return value is None or value in SUPPORTED_COMPANY_TIERS


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


def _safe_resume_resource_path(filename_text: str) -> Path | None:
    decoded = unquote(filename_text)
    filename = Path(decoded).name
    if not filename or filename != decoded or "\x00" in filename:
        return None
    root = _resume_resources_root().resolve()
    candidate = (root / filename).resolve()
    return candidate if candidate.parent == root else None


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
    target_path = downloads_dir / _role_material_pdf_filename(role, kind="resume")
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
        "\\pdfglyphtounicode" in content or "\\pdfgentounicode" in content
    ) and compatibility not in content:
        content = content.replace("\\documentclass", f"{compatibility}\\documentclass", 1)
    compile_path = resume_path.with_name("resume-tectonic.tex")
    compile_path.write_text(content)
    return compile_path


def _safe_filename(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    cleaned = "".join(character.lower() if character.isalnum() else "-" for character in normalized)
    parts = [part for part in cleaned.split("-") if part]
    return "-".join(parts[:10]) or "role"


def _role_material_pdf_filename(role: dict[str, Any], *, kind: str) -> str:
    company_name = _effective_role_company_name(role)
    role_title = role.get("title")
    role_id = role.get("id")
    context_parts = [
        _safe_filename(value)
        for value in (company_name, role_title)
        if isinstance(value, str) and value.strip()
    ]
    if not context_parts:
        context_parts.append(f"role-{role_id}" if isinstance(role_id, int) else "role")
    suffix = "resume" if kind == "resume" else "cover-letter"
    return "-".join([_applicant_pdf_filename_prefix(), *context_parts, suffix]) + ".pdf"


def _applicant_pdf_filename_prefix() -> str:
    try:
        with db.connect() as connection:
            db.run_migrations(connection)
            first_name = get_config_value(connection, APPLICANT_FIRST_NAME_CONFIG_KEY) or ""
            last_name = get_config_value(connection, APPLICANT_LAST_NAME_CONFIG_KEY) or ""
    except Exception:  # noqa: BLE001 - filename generation should not block PDF serving.
        first_name = ""
        last_name = ""
    prefix = _clean_applicant_name_part(first_name) + _clean_applicant_name_part(last_name)
    return prefix or "Applicant"


def _application_materials_payload(
    resume: MasterResume | None,
    examples: list[CoverLetterExample],
    notes: list[ExperienceNote],
) -> dict[str, Any]:
    resume_resources = _list_resume_resources()
    index_sources = [_experience_note_index_source(note) for note in notes]
    has_missing_required_materials = resume is None or len(examples) == 0 or len(notes) == 0
    return {
        "master_resume": _master_resume_summary(resume) if resume else None,
        "cover_letter_examples": [_cover_letter_example_summary(example) for example in examples],
        "experience_notes": [_experience_note_summary(note) for note in notes],
        "material_index": get_material_index_status(index_sources),
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


def _experience_note_index_source(note: ExperienceNote) -> dict[str, object]:
    return {
        "id": note.id,
        "filename": note.filename,
        "content": note.content,
        "content_sha256": note.content_sha256,
        "updated_at": note.updated_at.isoformat() if note.updated_at else None,
    }


def _generation_experience_context(
    notes: list[ExperienceNote],
    *,
    role: dict[str, Any],
    tweaks: str | None,
    total_content_limit: int = 16_000,
) -> list[dict[str, object]]:
    sources = [_experience_note_index_source(note) for note in notes]
    query = " ".join(
        str(value or "")
        for value in (
            role.get("title"),
            role.get("company_name"),
            role.get("location"),
            role.get("description"),
            tweaks,
        )
    )
    ai_role = _role_requests_ai_experience(role)
    ai_project_context = _ai_project_experience_context(notes) if ai_role else None
    if ai_role:
        query = (
            f"{query} independently directed AI-assisted projects "
            "Hermes AI application product architecture testing outcome"
        )
    retrieval_content_limit = max(
        1,
        total_content_limit - len(str(ai_project_context.get("content") or ""))
        if ai_project_context
        else total_content_limit,
    )
    indexed = retrieve_indexed_materials(
        sources,
        query=query,
        total_content_limit=retrieval_content_limit,
    )
    if indexed:
        return [*indexed, ai_project_context] if ai_project_context else indexed

    if not notes:
        return []
    per_note_limit = max(1, retrieval_content_limit // min(len(notes), 5))
    bounded: list[dict[str, object]] = []
    for note in notes[:5]:
        content = _bounded_experience_text(note.content, per_note_limit)
        bounded.append(
            {
                "filename": note.filename,
                "content": content,
                "updated_at": note.updated_at.isoformat() if note.updated_at else None,
            }
        )
    if ai_project_context:
        bounded.append(ai_project_context)
    return bounded


def _role_requests_ai_experience(role: dict[str, Any]) -> bool:
    role_text = " ".join(str(role.get(key) or "") for key in ("title", "description"))
    return bool(
        re.search(
            r"(?i)\b(?:ai|artificial intelligence|machine learning|ml platform|llm|"
            r"generative ai)\b",
            role_text,
        )
    )


def _ai_project_experience_context(
    notes: list[ExperienceNote],
    *,
    limit: int = 6_000,
) -> dict[str, object] | None:
    preferred_patterns = (
        r"(?im)^#{1,3}\s+.*independently directed AI-assisted projects.*$",
        r"(?im)^#{1,3}\s+.*AI-enabled application.*$",
        r"(?i)\bHermes Agent\b",
    )
    for pattern in preferred_patterns:
        for note in notes:
            match = re.search(pattern, note.content)
            if match is None:
                continue
            content = note.content[match.start() : match.start() + limit].strip()
            if content:
                return {
                    "filename": f"{note.filename} — AI project evidence",
                    "content": content,
                    "updated_at": note.updated_at.isoformat() if note.updated_at else None,
                }
    return None


def _bounded_experience_text(content: str, limit: int) -> str:
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", content)
    if len(cleaned) <= limit:
        return cleaned
    marker = "\n...[experience note truncated; create an index for targeted retrieval]...\n"
    if limit <= len(marker):
        return cleaned[:limit]
    available = limit - len(marker)
    head_length = available * 2 // 3
    return f"{cleaned[:head_length]}{marker}{cleaned[-(available - head_length) :]}"


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


def _experience_note_content_from_payload(
    filename: str,
    *,
    content: object,
    content_base64: object,
) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".pdf", ".docx"}:
        if not isinstance(content_base64, str):
            raise ValueError(f"{suffix.upper().removeprefix('.')} uploads require content_base64")
        try:
            document_bytes = base64.b64decode(content_base64, validate=True)
        except (binascii.Error, ValueError) as error:
            raise ValueError("Experience note content is not valid base64") from error
        if suffix == ".pdf":
            return _extract_pdf_text(document_bytes)
        return _extract_docx_text(document_bytes)
    if not isinstance(content, str):
        raise ValueError("Expected filename and content")
    return content


def _extract_pdf_text(document_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(document_bytes))
        pages = [page.extract_text(extraction_mode="layout") or "" for page in reader.pages]
    except Exception as error:  # noqa: BLE001 - pypdf exposes several parser errors.
        raise ValueError("PDF experience note content could not be read") from error
    extracted = "\n\f\n".join(pages).strip()
    if not extracted:
        raise ValueError("PDF experience note content cannot be empty")
    return _infer_pdf_markdown_sections(extracted)


def _infer_pdf_markdown_sections(content: str) -> str:
    lines = content.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    rendered: list[str] = []
    first_heading = True
    for index, line in enumerate(lines):
        stripped = re.sub(r"\s+", " ", line).strip()
        previous_blank = index == 0 or not lines[index - 1].strip()
        next_blank = index + 1 >= len(lines) or not lines[index + 1].strip()
        next_text = ""
        for candidate in lines[index + 1 :]:
            if candidate.strip():
                next_text = candidate.strip()
                break
        is_numbered_heading = bool(re.fullmatch(r"\d+\.\s+[^.!?]{3,100}", stripped))
        is_standalone_heading = (
            previous_blank
            and next_blank
            and 2 <= len(stripped.split()) <= 14
            and len(stripped) <= 110
            and stripped[:1].isupper()
            and not stripped.endswith((".", "!", "?", ":", ";", ","))
            and not stripped.startswith(("-", "•"))
            and bool(next_text)
        )
        if (
            stripped
            and not stripped.startswith("#")
            and (is_numbered_heading or is_standalone_heading)
        ):
            prefix = "#" if first_heading else "##"
            rendered.append(f"{prefix} {stripped}")
            first_heading = False
        else:
            rendered.append(line.rstrip())
    return "\n".join(rendered).strip()


def _cover_letter_content_from_payload(
    filename: str,
    *,
    content: object,
    content_base64: object,
) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".pdf", ".docx"}:
        if not isinstance(content_base64, str):
            document_type = suffix.upper().removeprefix(".")
            raise ValueError(f"{document_type} cover letter uploads require content_base64")
        try:
            document_bytes = base64.b64decode(content_base64, validate=True)
        except (binascii.Error, ValueError) as error:
            raise ValueError("Cover letter content is not valid base64") from error
        if suffix == ".pdf":
            return _extract_pdf_text(document_bytes)
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
    candidate = path_parts[-1]
    if candidate.isdigit() and len(path_parts) > 1:
        candidate = path_parts[-2]
    slug = re.sub(r"[-_]+", " ", unquote(candidate))
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
    global AUTOPREP_COORDINATOR
    db.ensure_initialized()
    with db.connect() as connection:
        ensure_autoprep_schema(connection)
        interrupted_count = recover_interrupted_autoprep_jobs(connection)
        interrupted_answer_count = recover_interrupted_application_answers(connection)
    if interrupted_count:
        LOGGER.warning("Marked %s unfinished Autoprep jobs interrupted", interrupted_count)
    if interrupted_answer_count:
        LOGGER.warning(
            "Marked %s unfinished application answers interrupted", interrupted_answer_count
        )
    AUTOPREP_COORDINATOR = AutoprepCoordinator(_process_autoprep_job, max_workers=2)
    AUTOPREP_COORDINATOR.start()
    SCAN_SCHEDULER.start()
    handler = create_handler()
    server = LocalThreadingHTTPServer((host, port), handler)
    try:
        server.serve_forever()
    finally:
        AUTOPREP_COORDINATOR.stop_claiming()
        APPLICANT_PROFILE_REPREP_SCHEDULER.close()
        SCAN_SCHEDULER.stop()
        AUTOPREP_COORDINATOR.wait_for_workers()
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
