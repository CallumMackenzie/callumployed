from callumployed.webscraping.browser import render_careers_page
from callumployed.webscraping.classifier import (
    AgentCandidateClassifier,
    classify_candidates,
    prepare_candidates,
    score_candidates,
)
from callumployed.webscraping.extraction import extract_link_candidates
from callumployed.webscraping.models import (
    CareersPageScanResult,
    ExtractionConfidence,
)


async def scan_careers_page(
    url: str,
    *,
    external_browser_port: int | None = None,
    existing_posting_urls: set[str] | None = None,
    agent_classifier: AgentCandidateClassifier | None = None,
) -> CareersPageScanResult:
    page = await render_careers_page(
        url,
        external_browser_port=external_browser_port,
    )
    candidates = extract_link_candidates(page)
    scored_candidates = score_candidates(
        prepare_candidates(candidates),
        existing_posting_urls=existing_posting_urls,
    )
    links = await classify_candidates(
        candidates,
        page,
        agent_classifier=agent_classifier,
        existing_posting_urls=existing_posting_urls,
    )

    return CareersPageScanResult(
        source_url=url,
        final_url=page.final_url,
        title=page.title,
        candidates=scored_candidates,
        links=links,
        candidates_scanned=len(scored_candidates),
        confidence=_result_confidence(links),
    )


def _result_confidence(links: object) -> ExtractionConfidence:
    link_count = len(links)  # type: ignore[arg-type]
    if link_count >= 3:
        return ExtractionConfidence.HIGH
    if link_count >= 1:
        return ExtractionConfidence.MEDIUM
    return ExtractionConfidence.LOW
