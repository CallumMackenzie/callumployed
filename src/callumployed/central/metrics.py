import hashlib
from collections import Counter

import turso

from callumployed import __version__
from callumployed.central.client import CentralStoreClient
from callumployed.central.config import get_central_api_url, get_central_client_id
from callumployed.central.models import ScanMetricsRequest
from callumployed.data import db
from callumployed.data.models import Company, RoleDiscoveryStatus, ScanRun, ScanStatus
from callumployed.data.repositories import (
    list_company_career_pages,
    list_role_discovery_attempts,
    list_scan_candidates,
    list_scan_pages,
)
from callumployed.services.autoprep import ensure_autoprep_schema

_REJECTION_REASON_CATEGORIES = {
    "closed role filtered by app config": "closed_role",
    "deterministic evidence is weak; llm fallback recommended": "weak_evidence",
    "graduate-degree role filtered by app config": "graduate_degree_filter",
    "hardware-only role filtered by app config": "hardware_filter",
    "intern keyword requirement filtered by app config": "internship_filter",
    "location filtered by app config": "location_filter",
    "page looks like a careers search/listing page": "listing_page",
    "page rendered a transient error shell": "transient_page_error",
    "software keyword requirement filtered by app config": "software_keyword_filter",
}


def build_scan_metrics(
    connection: turso.Connection,
    company: Company,
    scan_run: ScanRun,
) -> ScanMetricsRequest:
    if scan_run.id is None or scan_run.started_at is None or scan_run.finished_at is None:
        raise ValueError("finished scan run must include an id and timestamps")

    client_id = get_central_client_id(connection)
    scan_event_id = hashlib.sha256(
        f"{client_id}:{scan_run.id}".encode()
    ).hexdigest()
    pages = list_scan_pages(connection, scan_run.id)
    candidates = [
        candidate
        for page in pages
        if page.id is not None
        for candidate in list_scan_candidates(connection, page.id)
    ]
    attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)
    duration_ms = max(
        int((scan_run.finished_at - scan_run.started_at).total_seconds() * 1000),
        0,
    )
    page_confidence_counts = Counter(page.confidence or "unknown" for page in pages)
    candidate_confidence_counts = Counter(
        _confidence_bucket(candidate.confidence) for candidate in candidates
    )
    candidate_selection_counts = Counter(
        "selected" if candidate.selected else "rejected" for candidate in candidates
    )
    candidate_discovery_method_counts = Counter(
        candidate.discovery_method or "unclassified" for candidate in candidates
    )
    verification_status_counts = Counter(attempt.status.value for attempt in attempts)
    verification_outcome_counts = Counter(_verification_outcome(attempt) for attempt in attempts)
    extraction_method_counts = Counter(
        attempt.assessment_extraction_method or "unknown" for attempt in attempts
    )
    rejection_reason_counts = Counter(
        _rejection_reason_category(attempt.assessment_rejection_reason)
        for attempt in attempts
        if attempt.assessment_is_role is not True or attempt.assessment_is_closed is True
    )
    role_status_counts = Counter(
        {
            str(row["role_status"]): int(row["count"])
            for row in connection.execute(
                """
                SELECT role_status, COUNT(*) AS count
                FROM roles
                WHERE role_status IN ('interested', 'disinterested', 'archived', 'applied')
                GROUP BY role_status
                """
            ).fetchall()
        }
    )
    ensure_autoprep_schema(connection)
    autoprep_outcome_counts = Counter(
        {
            str(row["outcome"]): int(row["count"])
            for row in connection.execute(
                """
                SELECT
                    CASE WHEN overall_status = 'ready' THEN 'success' ELSE 'failure' END AS outcome,
                    COUNT(*) AS count
                FROM autoprep_jobs
                WHERE overall_status IN ('ready', 'failed', 'partially_complete', 'interrupted')
                GROUP BY outcome
                """
            ).fetchall()
        }
    )

    return ScanMetricsRequest(
        client_id=client_id,
        scan_event_id=scan_event_id,
        global_company_id=company.central_company_id,
        company_name=company.name,
        scan_status=(
            "succeeded" if scan_run.scan_status is ScanStatus.SUCCEEDED else "failed"
        ),
        started_at=scan_run.started_at,
        finished_at=scan_run.finished_at,
        duration_ms=duration_ms,
        career_pages_total=len(list_company_career_pages(connection, company.id or 0)),
        pages_scanned=len(pages),
        candidates_scanned=sum(page.candidates_scanned for page in pages),
        potential_roles_discovered=sum(candidate.selected for candidate in candidates),
        role_verification_attempts=len(attempts),
        verified_open_roles=sum(
            attempt.status is RoleDiscoveryStatus.SUCCEEDED
            and attempt.assessment_is_role is True
            and attempt.assessment_is_closed is not True
            for attempt in attempts
        ),
        roles_saved=len({attempt.role_id for attempt in attempts if attempt.role_id is not None}),
        failed_role_visits=sum(
            attempt.status is RoleDiscoveryStatus.FAILED for attempt in attempts
        ),
        page_confidence_counts=dict(page_confidence_counts),
        candidate_confidence_counts=dict(candidate_confidence_counts),
        candidate_selection_counts=dict(candidate_selection_counts),
        candidate_discovery_method_counts=dict(candidate_discovery_method_counts),
        verification_status_counts=dict(verification_status_counts),
        verification_outcome_counts=dict(verification_outcome_counts),
        extraction_method_counts=dict(extraction_method_counts),
        rejection_reason_counts=dict(rejection_reason_counts),
        role_status_counts=dict(role_status_counts),
        autoprep_outcome_counts=dict(autoprep_outcome_counts),
        agent_trace_present=bool(scan_run.agent_trace),
        error_type="scan_failed" if scan_run.scan_status is ScanStatus.FAILED else None,
        app_version=__version__,
    )


def publish_scan_metrics(company: Company, scan_run: ScanRun) -> None:
    with db.connect() as connection:
        api_url = get_central_api_url(connection)
        if api_url is None:
            return
        metrics = build_scan_metrics(connection, company, scan_run)
    assert api_url is not None
    CentralStoreClient(api_url=api_url, timeout=3.0).submit_scan_metrics(metrics)


def _confidence_bucket(confidence: float) -> str:
    if confidence >= 0.8:
        return "high"
    if confidence >= 0.5:
        return "medium"
    return "low"


def _rejection_reason_category(reason: str | None) -> str:
    if reason is None or not reason.strip():
        return "unspecified"
    return _REJECTION_REASON_CATEGORIES.get(reason.strip().casefold(), "other")


def _verification_outcome(attempt: object) -> str:
    is_role = getattr(attempt, "assessment_is_role", None)
    is_closed = getattr(attempt, "assessment_is_closed", None)
    if is_role is True and is_closed is not True:
        return "open_role"
    if is_role is True and is_closed is True:
        return "closed_role"
    if is_role is False:
        return "not_a_role"
    return "indeterminate"
