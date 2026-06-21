import asyncio
from pathlib import Path

import pytest

from callumployed.webscraping.classifier import (
    classify_candidates,
    prepare_candidates,
    score_candidates,
)
from callumployed.webscraping.extraction import extract_link_candidates
from callumployed.webscraping.models import ExtractionConfidence, RenderedPageState
from callumployed.webscraping.scanner import scan_careers_page

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def _fixture_page() -> RenderedPageState:
    html = (FIXTURE_DIR / "careers_page.html").read_text(encoding="utf-8")
    return RenderedPageState(
        url="https://example.com/careers",
        final_url="https://example.com/careers",
        title="Example Careers",
        html=html,
        visible_text=None,
    )


def _fixture_page_from_file(filename: str, url: str) -> RenderedPageState:
    html = (FIXTURE_DIR / filename).read_text(encoding="utf-8")
    return RenderedPageState(
        url=url,
        final_url=url,
        title=None,
        html=html,
        visible_text=None,
    )


def test_extract_link_candidates_normalizes_urls_without_deduping() -> None:
    candidates = extract_link_candidates(_fixture_page())
    urls = [candidate.url for candidate in candidates]

    assert "https://example.com/jobs/software-engineer-product" in urls
    assert "https://jobs.lever.co/example/infra-intern" in urls
    assert "https://example.com/positions/data-platform-engineer" in urls
    assert len([url for url in urls if url.endswith("/jobs/software-engineer-product")]) == 2


def test_prepare_candidates_dedupes_by_best_extraction_quality() -> None:
    candidates = extract_link_candidates(_fixture_page())
    prepared_candidates = prepare_candidates(candidates)
    urls = [candidate.url for candidate in prepared_candidates]

    assert len([url for url in urls if url.endswith("/jobs/software-engineer-product")]) == 1


def test_classify_candidates_scores_jobs_and_rejects_nav_links() -> None:
    candidates = extract_link_candidates(_fixture_page())
    links = asyncio.run(classify_candidates(candidates, _fixture_page()))
    urls = {link.url for link in links}

    assert "https://example.com/jobs/software-engineer-product" in urls
    assert "https://jobs.lever.co/example/infra-intern" in urls
    assert "https://example.com/positions/data-platform-engineer" in urls
    assert "https://example.com/about" not in urls
    assert "https://example.com/privacy" not in urls
    assert all(link.discovery_method == "heuristic" for link in links)


def test_classify_candidates_prefers_apple_detail_links_over_generic_careers_nav() -> None:
    page = _fixture_page_from_file(
        "apple_search_results.html",
        "https://jobs.apple.com/en-ca/search?search=Software",
    )
    candidates = extract_link_candidates(page)
    links = asyncio.run(classify_candidates(candidates, page))
    urls = {link.url for link in links}

    assert "https://jobs.apple.com/en-ca/details/200606937/software-engineering-internships" in urls
    assert "https://jobs.apple.com/en-ca/details/200607111/machine-learning-research-intern" in urls
    assert "https://www.apple.com/careers/ca" not in urls
    assert "https://jobs.apple.com/careers/ca/index/index.html" not in urls
    assert "https://jobs.apple.com/careers/choose-country-region.html" not in urls


def test_score_candidates_includes_reasons() -> None:
    candidates = prepare_candidates(extract_link_candidates(_fixture_page()))
    scored = score_candidates(candidates)

    top = scored[0]
    assert top.confidence > 0.0
    assert top.reasons


def test_scan_careers_page_orchestrates_render_extract_and_score(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_render_careers_page(url: str) -> RenderedPageState:
        page = _fixture_page()
        return page.model_copy(update={"url": url})

    monkeypatch.setattr(
        "callumployed.webscraping.scanner.render_careers_page",
        fake_render_careers_page,
    )

    result = asyncio.run(scan_careers_page("https://example.com/careers"))

    assert result.source_url == "https://example.com/careers"
    assert result.final_url == "https://example.com/careers"
    assert result.title == "Example Careers"
    assert result.candidates_scanned >= 3
    assert len(result.links) == 3
    assert result.confidence is ExtractionConfidence.HIGH
