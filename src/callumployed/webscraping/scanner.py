from callumployed.webscraping.browser import render_careers_page
from callumployed.webscraping.classifier import classify_candidates
from callumployed.webscraping.extraction import extract_link_candidates
from callumployed.webscraping.models import (
    CareersPageScanResult,
    ExtractionConfidence,
)


async def scan_careers_page(url: str) -> CareersPageScanResult:
    page = await render_careers_page(url)
    candidates = extract_link_candidates(page)
    links = await classify_candidates(candidates, page)

    return CareersPageScanResult(
        source_url=url,
        final_url=page.final_url,
        title=page.title,
        links=links,
        candidates_scanned=len(candidates),
        confidence=_result_confidence(links),
    )


def _result_confidence(links: object) -> ExtractionConfidence:
    link_count = len(links)  # type: ignore[arg-type]
    if link_count >= 3:
        return ExtractionConfidence.HIGH
    if link_count >= 1:
        return ExtractionConfidence.MEDIUM
    return ExtractionConfidence.LOW
