from callumployed.webscraping.browser import render_careers_page
from callumployed.webscraping.classifier import (
    prepare_candidates,
    score_candidates,
    select_heuristic_links,
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
) -> CareersPageScanResult:
    page = await render_careers_page(
        url,
        external_browser_port=external_browser_port,
    )
    candidates = extract_link_candidates(page)
    scored_candidates = score_candidates(prepare_candidates(candidates))
    links = select_heuristic_links(scored_candidates)

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
