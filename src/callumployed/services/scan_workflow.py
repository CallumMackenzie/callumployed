import logging
from typing import Any, Literal, TypedDict, cast
from urllib.parse import urlparse

from langgraph.graph import END, StateGraph

from callumployed.agents.posting_link_classifier import (
    ChatModelFactory,
    build_posting_link_agent_classifier,
)
from callumployed.central.metrics import publish_scan_metrics
from callumployed.config import LlmSettings
from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    Event,
    EventSource,
    Role,
    RoleDiscoveryAttempt,
    RoleDiscoveryStatus,
    RoleStatus,
    ScanCandidate,
    ScanPage,
    ScanRun,
    ScanStatus,
)
from callumployed.data.repositories import (
    add_event,
    add_role,
    add_role_discovery_attempt,
    add_scan_candidates,
    add_scan_page,
    create_scan_run,
    finish_scan_run,
    get_company,
    get_location_filter,
    get_role,
    get_role_by_company_url,
    get_scan_candidate,
    increase_company_browser_wait,
    list_company_career_pages,
    list_rejected_role_urls,
    list_role_discovery_attempts,
    list_roles,
    list_scan_candidates,
    list_scan_pages,
    set_role_status,
    should_include_graduate_degree_roles,
    should_include_hardware_roles,
    should_require_software_keywords,
    should_use_internship_mode,
    update_role,
    update_role_discovery_attempt_assessment,
)
from callumployed.services.company_scanners import ScannerOptions, scanner_for
from callumployed.services.scan_filters import (
    has_intern_keyword as _has_intern_keyword,
)
from callumployed.services.scan_filters import (
    has_software_keyword as _has_software_keyword,
)
from callumployed.services.scan_filters import (
    is_graduate_degree_role as _is_graduate_degree_role,
)
from callumployed.services.scan_filters import (
    is_hardware_only_role as _is_hardware_only_role,
)
from callumployed.services.scan_filters import (
    location_matches_filter as _location_matches_filter,
)
from callumployed.webscraping import browser
from callumployed.webscraping.classifier import (
    merge_discovered_links,
    prepare_candidates,
    score_candidates,
    select_ambiguous_candidates,
    select_heuristic_links,
)
from callumployed.webscraping.description_parser import clean_job_description
from callumployed.webscraping.errors import ClassificationError, NavigationError
from callumployed.webscraping.extraction import extract_link_candidates
from callumployed.webscraping.location_parser import parse_job_location
from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    LinkCandidate,
    RenderedPageState,
    RolePageAssessment,
    ScoredLinkCandidate,
)
from callumployed.webscraping.profile_manager import BrowserProfileManager
from callumployed.webscraping.role_page_classifier import assess_role_page

MIN_ROLE_CREATION_CONFIDENCE = 0.6
COMPANY_TIMEOUT_RETRY_INCREMENT_MS = 1_000
MAX_COMPANY_TIMEOUT_RETRIES_PER_SCAN = 3
ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS = browser.ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS
ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS = browser.ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS
ROLE_PAGE_CONTENT_SETTLE_POLL_MS = browser.ROLE_PAGE_CONTENT_SETTLE_POLL_MS
ROLE_PAGE_LAZY_SCROLL_STEP_DELAY_MS = browser.ROLE_PAGE_LAZY_SCROLL_STEP_DELAY_MS
render_careers_page = browser.render_careers_page
LOGGER = logging.getLogger(__name__)


class ScanWorkflowState(TypedDict, total=False):
    url: str
    company: Company | None
    career_page: CompanyCareerPage | None
    scan_run_id: int | None
    browser_profile_manager: BrowserProfileManager | None
    include_graduate_degree_roles: bool
    include_hardware_roles: bool
    require_software_keywords: bool
    internship_mode: bool
    location_filter: str
    existing_posting_urls: set[str]
    rejected_role_urls: set[str]
    retry_rejected_roles: bool
    browser_timeout_ms: int | None
    llm_settings: LlmSettings | None
    chat_model_factory: ChatModelFactory | None
    page: RenderedPageState
    raw_candidates: list[LinkCandidate]
    scored_candidates: list[ScoredLinkCandidate]
    ambiguous_candidates: list[ScoredLinkCandidate]
    heuristic_links: list[DiscoveredJobLink]
    agent_links: list[DiscoveredJobLink]
    links: list[DiscoveredJobLink]
    result: CareersPageScanResult
    scan_page: ScanPage
    stored_candidates: list[ScanCandidate]
    role_discovery_attempts: list[RoleDiscoveryAttempt]
    errors: list[str]


class CompanyScanResult(TypedDict):
    company: Company
    scan_run: ScanRun
    career_pages: list[CompanyCareerPage]
    results: list[CareersPageScanResult]
    role_discovery_attempts: list[RoleDiscoveryAttempt]
    include_graduate_degree_roles: bool
    include_hardware_roles: bool
    require_software_keywords: bool
    internship_mode: bool
    location_filter: str


class RoleRescanResult(TypedDict):
    previous_role: Role
    role: Role
    assessment: RolePageAssessment
    final_url: str


class RefilterAttemptResult(TypedDict):
    attempt_id: int
    company_id: int
    role_id: int | None
    url: str
    title: str | None
    previous_is_role: bool | None
    new_is_role: bool
    action: str
    reason: str | None


class RefilterCollectedRolesResult(TypedDict):
    scanned_attempts: int
    changed_attempts: int
    roles_created: int
    roles_archived: int
    protected_roles: int
    dry_run: bool
    attempts: list[RefilterAttemptResult]


async def render_page_node(state: ScanWorkflowState) -> dict[str, RenderedPageState]:
    page = await _render_with_browser_profile_manager(
        state["url"],
        state=state,
    )
    return {"page": page}


def extract_candidates_node(state: ScanWorkflowState) -> dict[str, list[LinkCandidate]]:
    return {"raw_candidates": extract_link_candidates(state["page"])}


def score_candidates_node(
    state: ScanWorkflowState,
) -> dict[str, list[ScoredLinkCandidate] | list[DiscoveredJobLink]]:
    scored_candidates = score_candidates(
        prepare_candidates(state["raw_candidates"]),
        existing_posting_urls=state.get("existing_posting_urls"),
        rejected_role_urls=state.get("rejected_role_urls"),
    )
    return {
        "scored_candidates": scored_candidates,
        "ambiguous_candidates": select_ambiguous_candidates(scored_candidates),
        "heuristic_links": select_heuristic_links(scored_candidates),
    }


async def classify_ambiguous_node(
    state: ScanWorkflowState,
) -> dict[str, list[DiscoveredJobLink]]:
    company = state.get("company") or Company(name="Ad hoc scan")
    career_page = state.get("career_page") or CompanyCareerPage(
        company_id=company.id or 0,
        url=state["url"],
        label="Ad hoc",
    )
    classifier = build_posting_link_agent_classifier(
        company=company,
        career_page=career_page,
        scan_run_id=state.get("scan_run_id") or 0,
        settings=state.get("llm_settings"),
        chat_model_factory=state.get("chat_model_factory"),
    )
    try:
        agent_links = await classifier(
            state.get("ambiguous_candidates", []),
            state["page"],
        )
    except ClassificationError:
        raise
    except Exception as error:
        raise ClassificationError(_ai_classification_error_message(error)) from error
    return {
        "agent_links": agent_links
    }


def _ai_classification_error_message(error: Exception) -> str:
    message = str(error).strip()
    if not message:
        message = error.__class__.__name__
    return f"AI classification failed: {message}"


def build_result_node(state: ScanWorkflowState) -> dict[str, object]:
    links = merge_discovered_links(
        state.get("heuristic_links", []),
        state.get("agent_links", []),
    )
    if not state.get("include_graduate_degree_roles", False):
        links = [
            link
            for link in links
            if not _is_graduate_degree_role(link.text, " ".join(link.reasons))
        ]
    if not state.get("include_hardware_roles", False):
        links = [link for link in links if not _is_hardware_only_role(link.text)]
    if state.get("require_software_keywords", True):
        links = [
            link
            for link in links
            if _has_software_keyword(link.text, " ".join(link.reasons))
        ]
    if state.get("internship_mode", True):
        links = [
            link
            for link in links
            if _discovered_link_has_intern_evidence(link)
        ]
    page = state["page"]
    result = CareersPageScanResult(
        source_url=state["url"],
        final_url=page.final_url,
        title=page.title,
        candidates=state.get("scored_candidates", []),
        links=links,
        candidates_scanned=len(state.get("scored_candidates", [])),
        confidence=_result_confidence(links),
        errors=state.get("errors", []),
    )
    return {"links": links, "result": result}


async def persist_scan_node(state: ScanWorkflowState) -> dict[str, object]:
    scan_run_id = state.get("scan_run_id")
    result = state["result"]
    if scan_run_id is None:
        return {}

    career_page = state.get("career_page")
    with db.connect() as connection:
        scan_page = add_scan_page(
            connection,
            scan_run_id,
            result,
            company_career_page_id=career_page.id if career_page is not None else None,
        )
        if scan_page.id is None:
            raise RuntimeError("created scan page did not include an id")
        stored_candidates = add_scan_candidates(connection, scan_page.id, result.candidates, result)
        _touch_rediscovered_existing_roles(connection, state, result)
    return {"scan_page": scan_page, "stored_candidates": stored_candidates}


def _touch_rediscovered_existing_roles(
    connection: Any,
    state: ScanWorkflowState,
    result: CareersPageScanResult,
) -> None:
    company = state.get("company")
    if company is None or company.id is None:
        return

    rediscovered_urls = {
        candidate.url
        for candidate in result.candidates
        if "already in database" in candidate.reasons
    }
    for url in rediscovered_urls:
        existing_role = get_role_by_company_url(connection, company.id, url)
        if existing_role is not None and existing_role.id is not None:
            update_role(connection, existing_role.id, touch_last_seen=True)


async def visit_discovered_links_node(state: ScanWorkflowState) -> dict[str, object]:
    scan_run_id = state.get("scan_run_id")
    company = state.get("company")
    if scan_run_id is None or company is None or company.id is None:
        return {"role_discovery_attempts": []}

    attempts: list[RoleDiscoveryAttempt] = []
    for candidate in state.get("stored_candidates", []):
        if not candidate.selected or candidate.id is None:
            continue
        try:
            page = await _render_with_browser_profile_manager(
                candidate.url,
                state=state,
                content_settle_min_wait_ms=ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS,
                content_settle_timeout_ms=ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS,
                content_settle_poll_ms=ROLE_PAGE_CONTENT_SETTLE_POLL_MS,
                lazy_scroll_step_delay_ms=ROLE_PAGE_LAZY_SCROLL_STEP_DELAY_MS,
            )
            assessment = assess_role_page(
                page,
                title_hints=(
                    candidate.text,
                    candidate.title,
                    candidate.aria_label,
                    candidate.surrounding_text,
                ),
            )
            if (
                assessment.is_role
                and not state.get("include_graduate_degree_roles", False)
                and _is_graduate_degree_role(assessment.title, assessment.description)
            ):
                assessment = assessment.model_copy(
                    update={
                        "is_role": False,
                        "confidence": max(assessment.confidence, 0.8),
                        "rejection_reason": "graduate-degree role filtered by app config",
                        "reasons": [
                            *assessment.reasons,
                            "graduate-degree role filter",
                        ],
                    }
                )
            if (
                assessment.is_role
                and not state.get("include_hardware_roles", False)
                and _is_hardware_only_role(assessment.title)
            ):
                assessment = assessment.model_copy(
                    update={
                        "is_role": False,
                        "confidence": max(assessment.confidence, 0.8),
                        "rejection_reason": "hardware-only role filtered by app config",
                        "reasons": [
                            *assessment.reasons,
                            "hardware-only role filter",
                        ],
                    }
                )
            if (
                assessment.is_role
                and state.get("require_software_keywords", True)
                and not _has_software_keyword(assessment.title, assessment.description)
            ):
                assessment = assessment.model_copy(
                    update={
                        "is_role": False,
                        "confidence": max(assessment.confidence, 0.8),
                        "rejection_reason": "software keyword requirement filtered by app config",
                        "reasons": [
                            *assessment.reasons,
                            "software keyword requirement",
                        ],
                    }
                )
            if (
                assessment.is_role
                and not _location_matches_filter(
                    assessment.location,
                    state.get("location_filter", "all"),
                )
            ):
                assessment = assessment.model_copy(
                    update={
                        "is_role": False,
                        "confidence": max(assessment.confidence, 0.8),
                        "rejection_reason": "location filtered by app config",
                        "reasons": [
                            *assessment.reasons,
                            "location filter",
                        ],
                    }
                )
            if (
                assessment.is_role
                and state.get("internship_mode", True)
                and _intern_keyword_evidence_source(assessment, candidate, page) is None
            ):
                assessment = assessment.model_copy(
                    update={
                        "is_role": False,
                        "confidence": max(assessment.confidence, 0.8),
                        "rejection_reason": "intern keyword requirement filtered by app config",
                        "reasons": [
                            *assessment.reasons,
                            "intern keyword requirement",
                        ],
                    }
                )
            elif (
                assessment.is_role
                and state.get("internship_mode", True)
            ):
                intern_evidence_source = _intern_keyword_evidence_source(
                    assessment,
                    candidate,
                    page,
                )
                if (
                    intern_evidence_source is not None
                    and intern_evidence_source != "assessed title"
                ):
                    assessment = assessment.model_copy(
                        update={
                            "reasons": [
                                *assessment.reasons,
                                f"intern keyword evidence: {intern_evidence_source}",
                            ],
                        }
                    )
            role = _create_or_get_assessed_role(
                company_id=company.id,
                role_url=candidate.url,
                title=assessment.title or page.title,
                location=assessment.location,
                description=assessment.description,
                posting_id=assessment.posting_id,
                is_role=assessment.is_role,
                confidence=assessment.confidence,
            )
            attempt = RoleDiscoveryAttempt(
                scan_run_id=scan_run_id,
                scan_candidate_id=candidate.id,
                company_id=company.id,
                role_id=role.id if role is not None else None,
                url=candidate.url,
                final_url=page.final_url,
                title=assessment.title or page.title,
                visible_text_excerpt=_visible_text_excerpt(
                    assessment.description or page.visible_text
                ),
                assessment_is_role=assessment.is_role,
                assessment_is_closed=assessment.is_closed,
                assessment_confidence=assessment.confidence,
                assessment_location=assessment.location,
                assessment_description=assessment.description,
                assessment_posting_id=assessment.posting_id,
                assessment_extraction_method=assessment.extraction_method,
                assessment_rejection_reason=assessment.rejection_reason,
                assessment_reasons=assessment.reasons,
                status=RoleDiscoveryStatus.SUCCEEDED,
            )
        except Exception as error:
            attempt = RoleDiscoveryAttempt(
                scan_run_id=scan_run_id,
                scan_candidate_id=candidate.id,
                company_id=company.id,
                url=candidate.url,
                status=RoleDiscoveryStatus.FAILED,
                error=str(error),
            )

        with db.connect() as connection:
            attempts.append(add_role_discovery_attempt(connection, attempt))

    return {"role_discovery_attempts": attempts}


async def rescan_role(
    role_id: int,
    *,
    browser_profile_manager: BrowserProfileManager | None = None,
    update_status: bool = False,
) -> RoleRescanResult:
    with db.connect() as connection:
        role = get_role(connection, role_id)

    page = await _render_with_browser_profile_manager(
        role.role_url,
        state={"browser_profile_manager": browser_profile_manager},
        content_settle_min_wait_ms=ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS,
        content_settle_timeout_ms=ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS,
        content_settle_poll_ms=ROLE_PAGE_CONTENT_SETTLE_POLL_MS,
        lazy_scroll_step_delay_ms=ROLE_PAGE_LAZY_SCROLL_STEP_DELAY_MS,
    )
    assessment = assess_role_page(page, title_hints=(role.title,))
    if _role_url_redirected_to_listing(role.role_url, page.final_url):
        assessment = assessment.model_copy(
            update={
                "is_role": False,
                "is_closed": False,
                "location": None,
                "description": None,
                "rejection_reason": "role URL redirected to a generic careers listing",
                "reasons": [
                    *assessment.reasons,
                    "role URL redirected to a generic careers listing",
                ],
            }
        )

    with db.connect() as connection:
        updated_role = role
        if assessment.is_role:
            updated_role = update_role(
                connection,
                role_id,
                title=assessment.title or role.title,
                location=assessment.location,
                description=assessment.description,
                posting_id=assessment.posting_id,
                touch_last_seen=True,
            )
        elif assessment.is_closed:
            updated_role = update_role(connection, role_id, touch_last_seen=True)

        if update_status and assessment.is_closed and role.role_status is not RoleStatus.CLOSED:
            updated_role = set_role_status(
                connection,
                role_id,
                RoleStatus.CLOSED,
                summary="Role marked closed after rescan.",
                source=EventSource.SCAN,
            )

        event_summary = _role_rescan_event_summary(assessment, updated_role)
        add_event(
            connection,
            Event(
                company_id=role.company_id,
                role_id=role_id,
                event_type="role_rescanned",
                source=EventSource.SCAN,
                summary=event_summary,
            ),
        )

    return {
        "previous_role": role,
        "role": updated_role,
        "assessment": assessment,
        "final_url": page.final_url,
    }


FILTER_REJECTION_REASONS = {
    "graduate-degree role filtered by app config",
    "hardware-only role filtered by app config",
    "software keyword requirement filtered by app config",
    "intern keyword requirement filtered by app config",
    "intern keyword requirement filtered by source config",
    "location filtered by app config",
}


def refilter_collected_roles(
    *,
    company_id: int | None = None,
    scan_run_id: int | None = None,
    apply: bool = False,
) -> RefilterCollectedRolesResult:
    """Replay current role filters against stored scan attempts without scraping."""
    with db.connect() as connection:
        include_graduate_degree_roles = should_include_graduate_degree_roles(connection)
        include_hardware_roles = should_include_hardware_roles(connection)
        require_software_keywords = should_require_software_keywords(connection)
        internship_mode = should_use_internship_mode(connection)
        location_filter = get_location_filter(connection)
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run_id)

    filtered_attempts = [
        attempt
        for attempt in attempts
        if attempt.status is RoleDiscoveryStatus.SUCCEEDED
        and (company_id is None or attempt.company_id == company_id)
    ]
    results: list[RefilterAttemptResult] = []
    roles_created = 0
    roles_archived = 0
    protected_roles = 0

    for attempt in filtered_attempts:
        if attempt.id is None:
            continue
        with db.connect() as connection:
            candidate = get_scan_candidate(connection, attempt.scan_candidate_id)

        assessment = _assessment_from_stored_attempt(attempt)
        assessment = _apply_role_filters(
            assessment,
            include_graduate_degree_roles=include_graduate_degree_roles,
            include_hardware_roles=include_hardware_roles,
            require_software_keywords=require_software_keywords,
            location_filter=location_filter,
        )
        page = _stored_page_from_attempt(attempt)
        if assessment.is_role and internship_mode:
            intern_evidence_source = _intern_keyword_evidence_source(
                assessment,
                candidate,
                page,
            )
            if intern_evidence_source is None:
                assessment = assessment.model_copy(
                    update={
                        "is_role": False,
                        "confidence": max(assessment.confidence, 0.8),
                        "rejection_reason": "intern keyword requirement filtered by app config",
                        "reasons": [
                            *assessment.reasons,
                            "intern keyword requirement",
                        ],
                    }
                )
            elif intern_evidence_source != "assessed title":
                evidence_reason = f"intern keyword evidence: {intern_evidence_source}"
                if evidence_reason not in assessment.reasons:
                    assessment = assessment.model_copy(
                        update={"reasons": [*assessment.reasons, evidence_reason]}
                    )

        action = "unchanged"
        role_id = attempt.role_id
        if assessment.is_role and role_id is None:
            action = "create_role"
            if apply:
                role = _create_or_get_assessed_role(
                    company_id=attempt.company_id,
                    role_url=attempt.url,
                    title=attempt.title,
                    location=attempt.assessment_location,
                    description=attempt.assessment_description,
                    posting_id=attempt.assessment_posting_id,
                    is_role=assessment.is_role,
                    confidence=assessment.confidence,
                )
                role_id = role.id if role is not None else None
                if role_id is not None:
                    roles_created += 1
        elif not assessment.is_role and role_id is not None:
            with db.connect() as connection:
                role = get_role(connection, role_id)
            if role.role_status is RoleStatus.DISCOVERED:
                action = "archive_role"
                if apply:
                    with db.connect() as connection:
                        set_role_status(
                            connection,
                            role_id,
                            RoleStatus.ARCHIVED,
                            summary=(
                                "Role archived after stored scan re-filter: "
                                f"{assessment.rejection_reason or 'no longer passes filters'}."
                            ),
                            source=EventSource.SCAN,
                        )
                    roles_archived += 1
            else:
                action = "protected_role"
                protected_roles += 1

        changed = (
            attempt.assessment_is_role != assessment.is_role
            or attempt.assessment_rejection_reason != assessment.rejection_reason
            or attempt.assessment_location != assessment.location
            or attempt.assessment_description != assessment.description
            or attempt.role_id != role_id
        )
        if changed and action == "unchanged":
            action = "refresh_fields"
        if role_id is not None and apply:
            with db.connect() as connection:
                role = get_role(connection, role_id)
                if (
                    (assessment.location is not None and role.location != assessment.location)
                    or (
                        assessment.description is not None
                        and role.description != assessment.description
                    )
                ):
                    update_role(
                        connection,
                        role_id,
                        location=assessment.location,
                        description=assessment.description,
                    )
        if changed and apply:
            with db.connect() as connection:
                update_role_discovery_attempt_assessment(
                    connection,
                    attempt.id,
                    role_id=role_id,
                    assessment_is_role=assessment.is_role,
                    assessment_confidence=assessment.confidence,
                    assessment_location=assessment.location,
                    assessment_description=assessment.description,
                    assessment_rejection_reason=assessment.rejection_reason,
                    assessment_reasons=assessment.reasons,
                )

        if changed or action != "unchanged":
            results.append(
                {
                    "attempt_id": attempt.id,
                    "company_id": attempt.company_id,
                    "role_id": role_id,
                    "url": attempt.url,
                    "title": attempt.title,
                    "previous_is_role": attempt.assessment_is_role,
                    "new_is_role": assessment.is_role,
                    "action": action,
                    "reason": assessment.rejection_reason,
                }
            )

    return {
        "scanned_attempts": len(filtered_attempts),
        "changed_attempts": sum(
            1
            for result in results
            if result["previous_is_role"] != result["new_is_role"]
            or result["action"] in {"create_role", "archive_role", "refresh_fields"}
        ),
        "roles_created": roles_created,
        "roles_archived": roles_archived,
        "protected_roles": protected_roles,
        "dry_run": not apply,
        "attempts": results,
    }


def _role_url_redirected_to_listing(role_url: str, final_url: str) -> bool:
    original_path = urlparse(role_url).path.rstrip("/")
    final_path = urlparse(final_url).path.rstrip("/")
    return "/job/" in original_path and "/job/" not in final_path


def _assessment_from_stored_attempt(attempt: RoleDiscoveryAttempt) -> RolePageAssessment:
    base_is_role = attempt.assessment_is_role is True or (
        attempt.assessment_rejection_reason in FILTER_REJECTION_REASONS
    )
    description = clean_job_description(attempt.assessment_description)
    location = _normalize_stored_location(
        attempt.assessment_location,
        context_text=" ".join(
            part
            for part in (attempt.visible_text_excerpt, description)
            if part
        ),
    )
    return RolePageAssessment(
        is_role=base_is_role,
        is_closed=attempt.assessment_is_closed is True,
        confidence=attempt.assessment_confidence or 0.0,
        title=attempt.title,
        location=location,
        description=description,
        posting_id=attempt.assessment_posting_id,
        extraction_method=attempt.assessment_extraction_method or "html_heuristic",
        rejection_reason=None if base_is_role else attempt.assessment_rejection_reason,
        reasons=_base_assessment_reasons(attempt.assessment_reasons),
    )


def _normalize_stored_location(
    location: str | None,
    *,
    context_text: str | None = None,
) -> str | None:
    if location is None:
        return None
    return parse_job_location(location, context_text=context_text) or location


def _base_assessment_reasons(reasons: list[str]) -> list[str]:
    filtered_reasons = {
        "graduate-degree role filter",
        "hardware-only role filter",
        "software keyword requirement",
        "intern keyword requirement",
    }
    return [
        reason
        for reason in reasons
        if reason not in filtered_reasons
        and not reason.startswith("intern keyword evidence:")
    ]


def _stored_page_from_attempt(attempt: RoleDiscoveryAttempt) -> RenderedPageState:
    return RenderedPageState(
        url=attempt.url,
        final_url=attempt.final_url or attempt.url,
        title=attempt.title,
        html="",
        visible_text=attempt.visible_text_excerpt,
    )


def _role_rescan_event_summary(assessment: RolePageAssessment, role: Role) -> str:
    if assessment.is_role:
        return f"Role rescan refreshed extracted fields for {role.title}."
    if assessment.is_closed:
        return "Role rescan found a closed or unavailable posting page."
    reason = assessment.rejection_reason or "weak role-page evidence"
    return f"Role rescan did not update extracted fields: {reason}."


async def _render_with_browser_profile_manager(
    url: str,
    *,
    state: ScanWorkflowState,
    **render_options: Any,
) -> RenderedPageState:
    if "timeout_ms" not in render_options and state.get("browser_timeout_ms") is not None:
        render_options["timeout_ms"] = state["browser_timeout_ms"]
    profile_manager = state.get("browser_profile_manager")
    if profile_manager is not None and hasattr(profile_manager, "headless"):
        render_options.setdefault("headless", profile_manager.headless)
    if browser.browser_backend() == "browserbase":
        try:
            return await render_careers_page(
                url,
                **render_options,
            )
        except NavigationError:
            if profile_manager is None:
                raise
            profile_page = await _try_render_with_browser_profile_manager(
                profile_manager,
                url,
                render_options=render_options,
            )
            if profile_page is None:
                raise
            return profile_page
    if profile_manager is not None:
        profile_page = await _try_render_with_browser_profile_manager(
            profile_manager,
            url,
            render_options=render_options,
        )
        if profile_page is not None:
            return profile_page
    return await render_careers_page(
        url,
        **render_options,
    )


async def _try_render_with_browser_profile_manager(
    profile_manager: BrowserProfileManager,
    url: str,
    *,
    render_options: dict[str, Any],
) -> RenderedPageState | None:
    try:
        return await profile_manager.render(
            render_careers_page,
            url,
            render_options=render_options,
        )
    except (FileNotFoundError, ValueError):
        return None
    except RuntimeError as error:
        if _is_managed_browser_unavailable_error(error):
            return None
        raise


def _is_managed_browser_unavailable_error(error: RuntimeError) -> bool:
    message = str(error)
    return (
        "no available managed browser profiles" in message
        or "browser process exited before CDP was ready" in message
        or "timed out waiting for browser CDP" in message
    )


def _create_or_get_assessed_role(
    *,
    company_id: int,
    role_url: str,
    title: str | None,
    location: str | None,
    description: str | None,
    posting_id: str | None,
    is_role: bool,
    confidence: float,
) -> Role | None:
    if not is_role or confidence < MIN_ROLE_CREATION_CONFIDENCE or title is None:
        return None

    with db.connect() as connection:
        existing_role = get_role_by_company_url(connection, company_id, role_url)
        if existing_role is not None:
            return existing_role
        role = add_role(
            connection,
            Role(
                company_id=company_id,
                title=title,
                role_url=role_url,
                location=location,
                description=description,
                posting_id=posting_id,
            ),
        )
    return role


def _apply_role_filters(
    assessment: RolePageAssessment,
    *,
    include_graduate_degree_roles: bool,
    include_hardware_roles: bool,
    require_software_keywords: bool,
    location_filter: str = "all",
) -> RolePageAssessment:
    if (
        assessment.is_role
        and not include_graduate_degree_roles
        and _is_graduate_degree_role(assessment.title, assessment.description)
    ):
        return assessment.model_copy(
            update={
                "is_role": False,
                "confidence": max(assessment.confidence, 0.8),
                "rejection_reason": "graduate-degree role filtered by app config",
                "reasons": [
                    *assessment.reasons,
                    "graduate-degree role filter",
                ],
            }
        )
    if (
        assessment.is_role
        and not include_hardware_roles
        and _is_hardware_only_role(assessment.title)
    ):
        return assessment.model_copy(
            update={
                "is_role": False,
                "confidence": max(assessment.confidence, 0.8),
                "rejection_reason": "hardware-only role filtered by app config",
                "reasons": [
                    *assessment.reasons,
                    "hardware-only role filter",
                ],
            }
        )
    if (
        assessment.is_role
        and require_software_keywords
        and not _has_software_keyword(assessment.title, assessment.description)
    ):
        return assessment.model_copy(
            update={
                "is_role": False,
                "confidence": max(assessment.confidence, 0.8),
                "rejection_reason": "software keyword requirement filtered by app config",
                "reasons": [
                    *assessment.reasons,
                    "software keyword requirement",
                ],
            }
        )
    if assessment.is_role and not _location_matches_filter(
        assessment.location,
        location_filter,
    ):
        return assessment.model_copy(
            update={
                "is_role": False,
                "confidence": max(assessment.confidence, 0.8),
                "rejection_reason": "location filtered by app config",
                "reasons": [
                    *assessment.reasons,
                    "location filter",
                ],
            }
        )
    return assessment


def _discovered_link_has_intern_evidence(link: DiscoveredJobLink) -> bool:
    return _has_intern_keyword(
        " ".join(part for part in (link.text, link.url, " ".join(link.reasons)) if part)
    )


def _intern_keyword_evidence_source(
    assessment: RolePageAssessment,
    candidate: ScanCandidate,
    page: RenderedPageState,
) -> str | None:
    evidence = (
        ("assessed title", assessment.title),
        ("selected link text", candidate.text),
        ("selected link title", candidate.title),
        ("selected link aria-label", candidate.aria_label),
        ("role URL", candidate.url),
        ("final role URL", page.final_url),
    )
    for source, text in evidence:
        if _has_intern_keyword(text):
            return source
    return None


def should_classify(state: ScanWorkflowState) -> Literal["classify", "skip"]:
    if state.get("ambiguous_candidates"):
        return "classify"
    return "skip"


def build_scan_graph() -> Any:
    graph = StateGraph(ScanWorkflowState)
    graph.add_node("render_page", render_page_node)
    graph.add_node("extract_candidates", extract_candidates_node)
    graph.add_node("score_candidates", score_candidates_node)
    graph.add_node("classify_ambiguous", classify_ambiguous_node)
    graph.add_node("build_result", build_result_node)
    graph.add_node("persist_scan", persist_scan_node)
    graph.add_node("visit_discovered_links", visit_discovered_links_node)

    graph.set_entry_point("render_page")
    graph.add_edge("render_page", "extract_candidates")
    graph.add_edge("extract_candidates", "score_candidates")
    graph.add_conditional_edges(
        "score_candidates",
        should_classify,
        {
            "classify": "classify_ambiguous",
            "skip": "build_result",
        },
    )
    graph.add_edge("classify_ambiguous", "build_result")
    graph.add_edge("build_result", "persist_scan")
    graph.add_edge("persist_scan", "visit_discovered_links")
    graph.add_edge("visit_discovered_links", END)
    return graph.compile()


async def scan_url(
    url: str,
    *,
    browser_profile_manager: BrowserProfileManager | None = None,
    existing_posting_urls: set[str] | None = None,
    llm_settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> CareersPageScanResult:
    graph = build_scan_graph()
    final_state = cast(
        ScanWorkflowState,
        await graph.ainvoke(
            {
                "url": url,
                "browser_profile_manager": browser_profile_manager,
                "existing_posting_urls": existing_posting_urls or set(),
                "rejected_role_urls": set(),
                "retry_rejected_roles": False,
                "llm_settings": llm_settings,
                "chat_model_factory": chat_model_factory,
                "agent_links": [],
                "stored_candidates": [],
                "errors": [],
            }
        ),
    )
    return final_state["result"]


async def scan_career_page(
    company: Company,
    career_page: CompanyCareerPage,
    *,
    scan_run_id: int | None = None,
    browser_profile_manager: BrowserProfileManager | None = None,
    include_graduate_degree_roles: bool = False,
    include_hardware_roles: bool = False,
    require_software_keywords: bool = True,
    internship_mode: bool = True,
    location_filter: str = "all",
    existing_posting_urls: set[str] | None = None,
    rejected_role_urls: set[str] | None = None,
    retry_rejected_roles: bool = False,
    browser_timeout_ms: int | None = None,
    llm_settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> CareersPageScanResult:
    custom_scanner = scanner_for(company, career_page)
    if custom_scanner is not None:
        return await custom_scanner.scan(
            company,
            career_page,
            ScannerOptions(
                scan_run_id=scan_run_id,
                include_graduate_degree_roles=include_graduate_degree_roles,
                include_hardware_roles=include_hardware_roles,
                require_software_keywords=require_software_keywords,
                internship_mode=internship_mode,
                location_filter=location_filter,
                existing_posting_urls=existing_posting_urls or set(),
                retry_rejected_roles=retry_rejected_roles,
            ),
        )

    graph = build_scan_graph()
    final_state = cast(
        ScanWorkflowState,
        await graph.ainvoke(
            {
                "url": career_page.url,
                "company": company,
                "career_page": career_page,
                "scan_run_id": scan_run_id,
                "browser_profile_manager": browser_profile_manager,
                "include_graduate_degree_roles": include_graduate_degree_roles,
                "include_hardware_roles": include_hardware_roles,
                "require_software_keywords": require_software_keywords,
                "internship_mode": internship_mode,
                "location_filter": location_filter,
                "existing_posting_urls": existing_posting_urls or set(),
                "rejected_role_urls": (
                    set() if retry_rejected_roles else rejected_role_urls or set()
                ),
                "retry_rejected_roles": retry_rejected_roles,
                "browser_timeout_ms": browser_timeout_ms,
                "llm_settings": llm_settings,
                "chat_model_factory": chat_model_factory,
                "agent_links": [],
                "stored_candidates": [],
                "errors": [],
            }
        ),
    )
    return final_state["result"]


async def scan_company(
    company: Company,
    *,
    browser_profile_manager: BrowserProfileManager | None = None,
    retry_rejected_roles: bool = False,
    llm_settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> CompanyScanResult | None:
    if company.id is None:
        raise RuntimeError("company did not include an id")

    with db.connect() as connection:
        career_pages = list_company_career_pages(connection, company.id)
        existing_posting_urls = {role.role_url for role in list_roles(connection)}
        rejected_role_urls = (
            set() if retry_rejected_roles else list_rejected_role_urls(connection, company.id)
        )
        include_graduate_degree_roles = should_include_graduate_degree_roles(connection)
        include_hardware_roles = should_include_hardware_roles(connection)
        require_software_keywords = should_require_software_keywords(connection)
        internship_mode = should_use_internship_mode(connection)
        location_filter = get_location_filter(connection)

    if not career_pages:
        return None

    with db.connect() as connection:
        scan_run = create_scan_run(connection, company.id)
    if scan_run.id is None:
        raise RuntimeError("created scan run did not include an id")

    current_company = company
    timeout_retries_remaining = MAX_COMPANY_TIMEOUT_RETRIES_PER_SCAN
    results: list[CareersPageScanResult] = []
    role_discovery_attempts: list[RoleDiscoveryAttempt] = []
    try:
        for career_page in career_pages:
            (
                result,
                current_company,
                timeout_retries_used,
            ) = await _scan_career_page_with_timeout_retry(
                current_company,
                career_page,
                scan_run_id=scan_run.id,
                timeout_retries_remaining=timeout_retries_remaining,
                browser_profile_manager=browser_profile_manager,
                include_graduate_degree_roles=include_graduate_degree_roles,
                include_hardware_roles=include_hardware_roles,
                require_software_keywords=require_software_keywords,
                internship_mode=internship_mode,
                location_filter=location_filter,
                existing_posting_urls=existing_posting_urls,
                rejected_role_urls=rejected_role_urls,
                retry_rejected_roles=retry_rejected_roles,
                llm_settings=llm_settings,
                chat_model_factory=chat_model_factory,
            )
            timeout_retries_remaining -= timeout_retries_used
            results.append(result)
    except Exception as error:
        with db.connect() as connection:
            failed_scan_run = finish_scan_run(
                connection,
                scan_run.id,
                ScanStatus.FAILED,
                error=str(error),
            )
        _publish_scan_metrics_safely(current_company, failed_scan_run)
        raise

    with db.connect() as connection:
        scan_run = finish_scan_run(connection, scan_run.id, ScanStatus.SUCCEEDED)
        role_discovery_attempts = list_role_discovery_attempts(
            connection,
            scan_run_id=scan_run.id,
        )
        _close_missing_disinterested_roles(
            connection,
            company_id=company.id,
            scan_run_id=scan_run.id,
            role_discovery_attempts=role_discovery_attempts,
        )

    _publish_scan_metrics_safely(current_company, scan_run)

    return {
        "company": current_company,
        "scan_run": scan_run,
        "career_pages": career_pages,
        "results": results,
        "role_discovery_attempts": role_discovery_attempts,
        "include_graduate_degree_roles": include_graduate_degree_roles,
        "include_hardware_roles": include_hardware_roles,
        "require_software_keywords": require_software_keywords,
        "internship_mode": internship_mode,
        "location_filter": location_filter,
    }


def _publish_scan_metrics_safely(company: Company, scan_run: ScanRun) -> None:
    try:
        publish_scan_metrics(company, scan_run)
    except Exception as error:  # noqa: BLE001 - metrics must never fail a completed scan.
        LOGGER.warning("Could not publish scan metrics: %s", error)


def _close_missing_disinterested_roles(
    connection: Any,
    *,
    company_id: int,
    scan_run_id: int,
    role_discovery_attempts: list[RoleDiscoveryAttempt],
) -> None:
    seen_role_ids = {
        attempt.role_id for attempt in role_discovery_attempts if attempt.role_id is not None
    }
    seen_role_urls = {
        candidate.url
        for page in list_scan_pages(connection, scan_run_id)
        if page.id is not None
        for candidate in list_scan_candidates(connection, page.id)
    }
    for role in list_roles(connection):
        if (
            role.id is None
            or role.company_id != company_id
            or role.role_status is not RoleStatus.DISINTERESTED
        ):
            continue
        if role.id in seen_role_ids or role.role_url in seen_role_urls:
            continue
        set_role_status(
            connection,
            role.id,
            RoleStatus.CLOSED,
            summary="Disinterested role marked closed after it was missing from scan.",
            source=EventSource.SCAN,
        )


async def _scan_career_page_with_timeout_retry(
    company: Company,
    career_page: CompanyCareerPage,
    *,
    scan_run_id: int,
    timeout_retries_remaining: int,
    browser_profile_manager: BrowserProfileManager | None,
    include_graduate_degree_roles: bool,
    include_hardware_roles: bool,
    require_software_keywords: bool,
    internship_mode: bool,
    location_filter: str,
    existing_posting_urls: set[str],
    rejected_role_urls: set[str],
    retry_rejected_roles: bool,
    llm_settings: LlmSettings | None,
    chat_model_factory: ChatModelFactory | None,
) -> tuple[CareersPageScanResult, Company, int]:
    current_company = company
    timeout_retries_used = 0
    while True:
        try:
            return (
                await scan_career_page(
                    current_company,
                    career_page,
                    scan_run_id=scan_run_id,
                    browser_profile_manager=browser_profile_manager,
                    include_graduate_degree_roles=include_graduate_degree_roles,
                    include_hardware_roles=include_hardware_roles,
                    require_software_keywords=require_software_keywords,
                    internship_mode=internship_mode,
                    location_filter=location_filter,
                    existing_posting_urls=existing_posting_urls,
                    rejected_role_urls=rejected_role_urls,
                    retry_rejected_roles=retry_rejected_roles,
                    browser_timeout_ms=_company_browser_timeout_ms(current_company),
                    llm_settings=llm_settings,
                    chat_model_factory=chat_model_factory,
                ),
                current_company,
                timeout_retries_used,
            )
        except NavigationError as error:
            if (
                not _is_navigation_timeout(error)
                or timeout_retries_used >= timeout_retries_remaining
            ):
                raise

        with db.connect() as connection:
            current_company = increase_company_browser_wait(
                connection,
                current_company.id or career_page.company_id,
                increment_ms=COMPANY_TIMEOUT_RETRY_INCREMENT_MS,
            )
        timeout_retries_used += 1


def _company_browser_timeout_ms(company: Company) -> int | None:
    extra_wait_ms = max(company.browser_extra_wait_ms, 0)
    if extra_wait_ms == 0:
        return None
    return browser.DEFAULT_TIMEOUT_MS + extra_wait_ms


def _is_navigation_timeout(error: NavigationError) -> bool:
    return str(error).startswith("Timed out while navigating to ")


async def scan_company_by_id(
    company_id: int,
    *,
    llm_settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> CompanyScanResult | None:
    with db.connect() as connection:
        company = get_company(connection, company_id)
    return await scan_company(
        company,
        retry_rejected_roles=False,
        llm_settings=llm_settings,
        chat_model_factory=chat_model_factory,
    )


def _result_confidence(links: object) -> ExtractionConfidence:
    link_count = len(links)  # type: ignore[arg-type]
    if link_count >= 3:
        return ExtractionConfidence.HIGH
    if link_count >= 1:
        return ExtractionConfidence.MEDIUM
    return ExtractionConfidence.LOW


def _visible_text_excerpt(visible_text: str | None, *, max_chars: int = 4000) -> str | None:
    if visible_text is None:
        return None
    normalized = " ".join(visible_text.split())
    if not normalized:
        return None
    return normalized[:max_chars]
