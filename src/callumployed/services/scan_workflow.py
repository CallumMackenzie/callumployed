import re
from typing import Any, Literal, TypedDict, cast

from langgraph.graph import END, StateGraph

from callumployed.agents.posting_link_classifier import (
    ChatModelFactory,
    build_posting_link_agent_classifier,
)
from callumployed.config import LlmSettings
from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    Role,
    RoleDiscoveryAttempt,
    RoleDiscoveryStatus,
    ScanCandidate,
    ScanPage,
    ScanRun,
    ScanStatus,
)
from callumployed.data.repositories import (
    add_role,
    add_role_discovery_attempt,
    add_scan_candidates,
    add_scan_page,
    create_scan_run,
    finish_scan_run,
    get_company,
    get_default_external_browser_port,
    get_role_by_company_url,
    list_company_career_pages,
    list_role_discovery_attempts,
    list_roles,
    should_include_graduate_degree_roles,
)
from callumployed.webscraping.browser import (
    ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS,
    ROLE_PAGE_CONTENT_SETTLE_POLL_MS,
    ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS,
    ROLE_PAGE_LAZY_SCROLL_STEP_DELAY_MS,
    render_careers_page,
)
from callumployed.webscraping.classifier import (
    merge_discovered_links,
    prepare_candidates,
    score_candidates,
    select_ambiguous_candidates,
    select_heuristic_links,
)
from callumployed.webscraping.extraction import extract_link_candidates
from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    LinkCandidate,
    RenderedPageState,
    ScoredLinkCandidate,
)
from callumployed.webscraping.role_page_classifier import assess_role_page

MIN_ROLE_CREATION_CONFIDENCE = 0.6
GRADUATE_DEGREE_ROLE_PATTERN = re.compile(
    r"\b(?:ph\.?\s*d\.?|phd|doctorate|doctoral|master'?s|masters|m\.?\s*sc\.?)\b",
    re.I,
)


class ScanWorkflowState(TypedDict, total=False):
    url: str
    company: Company | None
    career_page: CompanyCareerPage | None
    scan_run_id: int | None
    external_browser_port: int | None
    include_graduate_degree_roles: bool
    existing_posting_urls: set[str]
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
    external_browser_port: int | None
    include_graduate_degree_roles: bool


async def render_page_node(state: ScanWorkflowState) -> dict[str, RenderedPageState]:
    page = await render_careers_page(
        state["url"],
        external_browser_port=state.get("external_browser_port"),
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
    return {
        "agent_links": await classifier(
            state.get("ambiguous_candidates", []),
            state["page"],
        )
    }


def build_result_node(state: ScanWorkflowState) -> dict[str, object]:
    links = merge_discovered_links(
        state.get("heuristic_links", []),
        state.get("agent_links", []),
    )
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
    return {"scan_page": scan_page, "stored_candidates": stored_candidates}


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
            page = await render_careers_page(
                candidate.url,
                external_browser_port=state.get("external_browser_port"),
                content_settle_min_wait_ms=ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS,
                content_settle_timeout_ms=ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS,
                content_settle_poll_ms=ROLE_PAGE_CONTENT_SETTLE_POLL_MS,
                lazy_scroll_step_delay_ms=ROLE_PAGE_LAZY_SCROLL_STEP_DELAY_MS,
            )
            assessment = assess_role_page(page)
            if (
                not state.get("include_graduate_degree_roles", False)
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


def _is_graduate_degree_role(title: str | None, description: str | None) -> bool:
    text = " ".join(part for part in (title, description) if part)
    return bool(GRADUATE_DEGREE_ROLE_PATTERN.search(text))


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
    external_browser_port: int | None = None,
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
                "external_browser_port": external_browser_port,
                "existing_posting_urls": existing_posting_urls or set(),
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
    external_browser_port: int | None = None,
    include_graduate_degree_roles: bool = False,
    existing_posting_urls: set[str] | None = None,
    llm_settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> CareersPageScanResult:
    graph = build_scan_graph()
    final_state = cast(
        ScanWorkflowState,
        await graph.ainvoke(
            {
                "url": career_page.url,
                "company": company,
                "career_page": career_page,
                "scan_run_id": scan_run_id,
                "external_browser_port": external_browser_port,
                "include_graduate_degree_roles": include_graduate_degree_roles,
                "existing_posting_urls": existing_posting_urls or set(),
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
    default_external_browser_port: int | None = None,
    llm_settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> CompanyScanResult | None:
    if company.id is None:
        raise RuntimeError("company did not include an id")

    with db.connect() as connection:
        career_pages = list_company_career_pages(connection, company.id)
        existing_posting_urls = {role.role_url for role in list_roles(connection)}
        include_graduate_degree_roles = should_include_graduate_degree_roles(connection)

    if not career_pages:
        return None

    external_browser_port = company.external_browser_port or default_external_browser_port

    with db.connect() as connection:
        scan_run = create_scan_run(connection, company.id)
    if scan_run.id is None:
        raise RuntimeError("created scan run did not include an id")

    results: list[CareersPageScanResult] = []
    role_discovery_attempts: list[RoleDiscoveryAttempt] = []
    try:
        for career_page in career_pages:
            result = await scan_career_page(
                company,
                career_page,
                scan_run_id=scan_run.id,
                external_browser_port=external_browser_port,
                include_graduate_degree_roles=include_graduate_degree_roles,
                existing_posting_urls=existing_posting_urls,
                llm_settings=llm_settings,
                chat_model_factory=chat_model_factory,
            )
            results.append(result)
    except Exception as error:
        with db.connect() as connection:
            finish_scan_run(connection, scan_run.id, ScanStatus.FAILED, error=str(error))
        raise

    with db.connect() as connection:
        scan_run = finish_scan_run(connection, scan_run.id, ScanStatus.SUCCEEDED)
        role_discovery_attempts = list_role_discovery_attempts(
            connection,
            scan_run_id=scan_run.id,
        )

    return {
        "company": company,
        "scan_run": scan_run,
        "career_pages": career_pages,
        "results": results,
        "role_discovery_attempts": role_discovery_attempts,
        "external_browser_port": external_browser_port,
        "include_graduate_degree_roles": include_graduate_degree_roles,
    }


async def scan_company_by_id(
    company_id: int,
    *,
    llm_settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> CompanyScanResult | None:
    with db.connect() as connection:
        company = get_company(connection, company_id)
        default_external_browser_port = get_default_external_browser_port(connection)
    return await scan_company(
        company,
        default_external_browser_port=default_external_browser_port,
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
