import hashlib

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
        error_type="scan_failed" if scan_run.scan_status is ScanStatus.FAILED else None,
        app_version=__version__,
    )


def publish_scan_metrics(company: Company, scan_run: ScanRun) -> None:
    with db.connect() as connection:
        api_url = get_central_api_url(connection)
        if api_url is None:
            return
        metrics = build_scan_metrics(connection, company, scan_run)
    CentralStoreClient(api_url=api_url, timeout=3.0).submit_scan_metrics(metrics)
