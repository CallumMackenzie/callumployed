import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest
from bs4 import BeautifulSoup

from callumployed.config import BrowserSettings
from callumployed.services.scan_filters import has_software_keyword
from callumployed.webscraping.browser import (
    CONTENT_SETTLE_MIN_WAIT_MS,
    CONTENT_SETTLE_TIMEOUT_MS,
    DEFAULT_TIMEOUT_MS,
    PROFILE_DIR_NAME,
    ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS,
    ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS,
    PlaywrightTimeoutError,
    _browserbase_session_connect_url,
    _looks_like_blocked_page,
    _render_with_context,
    _render_with_playwright,
    browser_backend,
    managed_browser_profile_path,
    navigation_error_message,
)
from callumployed.webscraping.classifier import (
    classify_candidates,
    prepare_candidates,
    score_candidates,
    select_heuristic_links,
)
from callumployed.webscraping.description_parser import (
    clean_job_description,
    extract_job_description,
)
from callumployed.webscraping.errors import NavigationError
from callumployed.webscraping.extraction import extract_link_candidates
from callumployed.webscraping.location_parser import parse_job_location
from callumployed.webscraping.models import (
    DiscoveredJobLink,
    ExtractionConfidence,
    RenderedPageState,
    ScoredLinkCandidate,
)
from callumployed.webscraping.role_page_classifier import assess_role_page
from callumployed.webscraping.scanner import scan_careers_page

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_default_browser_timeout_is_at_least_20_seconds() -> None:
    assert DEFAULT_TIMEOUT_MS >= 20_000


def test_dynamic_content_settle_wait_is_bounded_for_responsive_scans() -> None:
    assert 2_000 <= CONTENT_SETTLE_MIN_WAIT_MS <= 5_000
    assert 5_000 <= CONTENT_SETTLE_TIMEOUT_MS <= 10_000


def test_role_page_content_settle_wait_is_shorter_than_career_page_scans() -> None:
    assert ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS < CONTENT_SETTLE_MIN_WAIT_MS
    assert ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS < CONTENT_SETTLE_TIMEOUT_MS


def test_browser_backend_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CALLUMPLOYED_BROWSER_BACKEND", "browserbase")

    assert browser_backend() == "browserbase"


def test_browserbase_session_connect_url_accepts_sdk_shapes() -> None:
    class SnakeCaseSession:
        connect_url = "wss://browserbase.example/snake"

    class CamelCaseSession:
        connectUrl = "wss://browserbase.example/camel"

    assert _browserbase_session_connect_url(SnakeCaseSession()) == "wss://browserbase.example/snake"
    assert _browserbase_session_connect_url(CamelCaseSession()) == "wss://browserbase.example/camel"
    assert (
        _browserbase_session_connect_url({"connectUrl": "wss://browserbase.example/dict"})
        == "wss://browserbase.example/dict"
    )


def test_browserbase_backend_falls_back_to_local_when_key_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    async def fake_render_with_managed_browser(
        playwright: object,
        url: str,
        **_options: object,
    ) -> RenderedPageState:
        calls.append(url)
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Local fallback",
            html="<html><body>Local fallback</body></html>",
        )

    monkeypatch.setattr(
        "callumployed.webscraping.browser._render_with_managed_browser",
        fake_render_with_managed_browser,
    )

    result = asyncio.run(
        _render_with_playwright(
            object(),  # type: ignore[arg-type]
            "https://example.com",
            settings=BrowserSettings.model_construct(
                backend="browserbase",
                headless=True,
                timeout_ms=30_000,
                browserbase_api_key=None,
            ),
            selected_backend="browserbase",
            external_browser_port=None,
            fallback_to_managed_browser=True,
            timeout_ms=1_000,
            blocked_types=set(),
            content_settle_min_wait_ms=1,
            content_settle_timeout_ms=1,
            content_settle_poll_ms=1,
            lazy_scroll_step_delay_ms=1,
        )
    )

    assert result.title == "Local fallback"
    assert calls == ["https://example.com"]


def test_browserbase_backend_falls_back_to_local_when_remote_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    async def fake_render_with_browserbase(*_args: object, **_options: object) -> RenderedPageState:
        raise NavigationError("Browserbase failed")

    async def fake_render_with_managed_browser(
        playwright: object,
        url: str,
        **_options: object,
    ) -> RenderedPageState:
        calls.append(url)
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Local fallback",
            html="<html><body>Local fallback</body></html>",
        )

    monkeypatch.setattr(
        "callumployed.webscraping.browser._render_with_browserbase",
        fake_render_with_browserbase,
    )
    monkeypatch.setattr(
        "callumployed.webscraping.browser._render_with_managed_browser",
        fake_render_with_managed_browser,
    )

    result = asyncio.run(
        _render_with_playwright(
            object(),  # type: ignore[arg-type]
            "https://example.com",
            settings=BrowserSettings.model_construct(
                backend="browserbase",
                headless=True,
                timeout_ms=30_000,
                browserbase_api_key="configured",
            ),
            selected_backend="browserbase",
            external_browser_port=None,
            fallback_to_managed_browser=True,
            timeout_ms=1_000,
            blocked_types=set(),
            content_settle_min_wait_ms=1,
            content_settle_timeout_ms=1,
            content_settle_poll_ms=1,
            lazy_scroll_step_delay_ms=1,
        )
    )

    assert result.title == "Local fallback"
    assert calls == ["https://example.com"]


def test_access_denied_body_is_treated_as_blocked_page() -> None:
    assert _looks_like_blocked_page(
        "Access Denied",
        "You don't have permission to access this server.",
    )


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


def test_extract_link_candidates_keeps_all_relative_hrefs_for_scoring() -> None:
    page = RenderedPageState(
        url="https://www.tesla.com/careers/search/?query=Software",
        final_url="https://www.tesla.com/careers/search/?query=Software",
        html="""
        <a href="/careers/search/job/software-engineer-intern-123">Software Intern</a>
        <a href="/careers">Careers</a>
        <a href="/about">About</a>
        """,
    )

    candidates = extract_link_candidates(page)
    urls = {candidate.url for candidate in candidates}

    assert urls == {
        "https://www.tesla.com/careers/search/job/software-engineer-intern-123",
        "https://www.tesla.com/careers",
        "https://www.tesla.com/about",
    }


def test_extract_link_candidates_sanitizes_maybe_link_text() -> None:
    page = RenderedPageState(
        url="https://www.janestreet.com/join-jane-street/",
        final_url="https://www.janestreet.com/join-jane-street/",
        html="""
        <a href="https://www.janestreet.com/join-jane-street/position/5869205002/
                 - Tools and Compilers Research and Development Internship New York">
          Tools and Compilers Research and Development Internship
        </a>
        <a href="/join-jane-street/position/12345/ - Software Engineering Internship">
          Software Engineering Internship
        </a>
        """,
    )

    candidates = extract_link_candidates(page)
    urls = {candidate.url for candidate in candidates}

    assert urls == {
        "https://www.janestreet.com/join-jane-street/position/5869205002/",
        "https://www.janestreet.com/join-jane-street/position/12345/",
    }


def test_extract_link_candidates_fixes_google_jobs_relative_results_paths() -> None:
    page = RenderedPageState(
        url=(
            "https://www.google.com/about/careers/applications/jobs/results"
            "?target_level=INTERN_AND_APPRENTICE"
        ),
        final_url=(
            "https://www.google.com/about/careers/applications/jobs/results"
            "?target_level=INTERN_AND_APPRENTICE"
        ),
        html="""
        <a href="jobs/results/120997883141857990-software-engineering-intern-summer-2027">
          Learn more about Software Engineering Intern, Summer 2027
        </a>
        """,
    )

    candidates = extract_link_candidates(page)

    assert candidates[0].url == (
        "https://www.google.com/about/careers/applications/jobs/results/"
        "120997883141857990-software-engineering-intern-summer-2027"
    )


def test_tesla_search_result_anchor_is_selected_when_present() -> None:
    page = RenderedPageState(
        url="https://www.tesla.com/careers/search/?type=intern&site=US&query=Software",
        final_url="https://www.tesla.com/careers/search/?type=intern&site=US&query=Software",
        title="Tesla Careers",
        html="""
        <a class="style_TitleLink__PepSM tds-text--h4 tds-link tds-link--secondary"
           href="/careers/search/job/internship-software-engineer-service-engineering-summer-2026-259221">
           Internship, <span class="style_highlighted__fVCzm">Software</span>
           Engineer, Service Engineering (Summer 2026)
        </a>
        """,
    )

    candidates = extract_link_candidates(page)
    links = asyncio.run(classify_candidates(candidates, page))

    assert links
    assert links[0].url.endswith(
        "/careers/search/job/internship-software-engineer-service-engineering-summer-2026-259221"
    )
    assert links[0].confidence >= 0.35


def test_collected_lazy_scroll_anchor_is_selected_after_dom_virtualization() -> None:
    page = RenderedPageState(
        url="https://www.tesla.com/careers/search/?type=intern&site=US&query=Software",
        final_url="https://www.tesla.com/careers/search/?type=intern&site=US&query=Software",
        title="Tesla Careers",
        html="""
        <div data-callumployed-collected-links="lazy-scroll" hidden>
          <a href="/careers/search/job/software-engineering-intern-summer-2026-111"
             data-callumployed-collected-link="lazy-scroll">
             Software Engineering Intern, Summer 2026
          </a>
        </div>
        """,
    )

    candidates = extract_link_candidates(page)
    links = asyncio.run(classify_candidates(candidates, page))

    assert links
    assert links[0].url.endswith("/careers/search/job/software-engineering-intern-summer-2026-111")
    assert links[0].confidence >= 0.35


def test_prepare_candidates_dedupes_by_best_extraction_quality() -> None:
    candidates = extract_link_candidates(_fixture_page())
    prepared_candidates = prepare_candidates(candidates)
    urls = [candidate.url for candidate in prepared_candidates]

    assert len([url for url in urls if url.endswith("/jobs/software-engineer-product")]) == 1


def test_prepare_candidates_prefers_role_title_over_generic_apply_link() -> None:
    page = RenderedPageState(
        url="https://fiverings.com/careers/",
        final_url="https://fiverings.com/careers/",
        title="Job Search - Five Rings",
        html="""
        <div class="gh-item">
          <div class="gh-item_buttons">
            <a href="https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008">
              Apply
            </a>
          </div>
          <div class="gh-item_heading">
            <a href="https://job-boards.greenhouse.io/fiveringsllc/jobs/5349707008">
              Summer Intern 2027 - Software Developer
            </a>
          </div>
        </div>
        """,
    )

    prepared_candidates = prepare_candidates(extract_link_candidates(page))

    assert len(prepared_candidates) == 1
    assert prepared_candidates[0].text == "Summer Intern 2027 - Software Developer"


def test_quant_trading_titles_count_as_relevant_role_keywords() -> None:
    assert has_software_keyword("Summer Intern 2027 - Quantitative Trader", None)
    assert has_software_keyword("Campus Full Time 2027 - Trading Operations Engineer", None)


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


def test_classify_candidates_accepts_numeric_job_ids_and_rejects_closed_roles() -> None:
    page = RenderedPageState(
        url="https://www.janestreet.com/join-jane-street/open-roles/?type=internship",
        final_url="https://www.janestreet.com/join-jane-street/open-roles/?type=internship",
        html="""
        <a href="/join-jane-street/position/5869205002/">
          Tools and Compilers Research and Development Internship
        </a>
        <a href="/join-jane-street/closed-internship/software-engineer-may-august-nyc/">
          Software Engineer (not currently accepting applications) Internship
        </a>
        <a href="/join-jane-street/internships/">INTERNSHIPS</a>
        """,
    )

    candidates = extract_link_candidates(page)
    links = asyncio.run(classify_candidates(candidates, page))
    urls = {link.url for link in links}

    assert "https://www.janestreet.com/join-jane-street/position/5869205002/" in urls
    assert (
        "https://www.janestreet.com/join-jane-street/closed-internship/"
        "software-engineer-may-august-nyc/"
    ) not in urls
    assert "https://www.janestreet.com/join-jane-street/internships/" not in urls


def test_score_candidates_includes_reasons() -> None:
    candidates = prepare_candidates(extract_link_candidates(_fixture_page()))
    scored = score_candidates(candidates)

    top = scored[0]
    assert top.confidence > 0.0
    assert top.reasons


def test_bytedance_search_job_id_links_clear_heuristic_threshold() -> None:
    page = RenderedPageState(
        url="https://joinbytedance.com/search",
        final_url="https://joinbytedance.com/search",
        html="""
        <a href="/search/7639884334834862341">
          Student Researcher (AI Foundation Models Infrastructure) Technology Project Intern
        </a>
        <a href="/search">Jobs</a>
        """,
    )
    scored = score_candidates(prepare_candidates(extract_link_candidates(page)))
    links = select_heuristic_links(scored)

    assert "https://joinbytedance.com/search/7639884334834862341" in {
        link.url for link in links
    }
    assert "https://joinbytedance.com/search" not in {link.url for link in links}


def test_score_candidates_hard_declines_existing_posting_urls() -> None:
    existing_url = "https://example.com/jobs/software-engineer-product"
    candidates = prepare_candidates(extract_link_candidates(_fixture_page()))

    scored = score_candidates(candidates, existing_posting_urls={existing_url})
    scored_by_url = {candidate.url: candidate for candidate in scored}

    assert scored_by_url[existing_url].confidence == 0.0
    assert "already in database" in scored_by_url[existing_url].reasons
    assert existing_url not in {link.url for link in select_heuristic_links(scored)}


def test_assess_role_page_prefers_schema_org_jobposting() -> None:
    page = RenderedPageState(
        url="https://example.com/jobs/backend-intern",
        final_url="https://example.com/jobs/backend-intern",
        title="Careers",
        html="""
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "JobPosting",
          "title": "Backend Engineering Intern",
          "description": "<p>Build internal platforms.</p>",
          "identifier": {"value": "REQ-123"},
          "jobLocation": {
            "@type": "Place",
            "address": {
              "@type": "PostalAddress",
              "addressLocality": "Vancouver",
              "addressRegion": "BC",
              "addressCountry": "CA"
            }
          }
        }
        </script>
        <h1>Careers</h1>
        """,
    )

    assessment = assess_role_page(page)

    assert assessment.is_role is True
    assert assessment.confidence == 0.95
    assert assessment.extraction_method == "jobposting_structured_data"
    assert assessment.title == "Backend Engineering Intern"
    assert assessment.location == "Vancouver, BC, Canada"
    assert assessment.posting_id == "REQ-123"


def test_assess_role_page_accepts_ats_role_without_structured_data() -> None:
    page = RenderedPageState(
        url="https://jobs.lever.co/acme/backend-intern",
        final_url="https://jobs.lever.co/acme/backend-intern",
        title="Backend Intern",
        html="""
        <h1>Backend Intern</h1>
        <div class="location">Toronto, ON</div>
        <section>Job description. Responsibilities. Requirements. Apply now.</section>
        """,
    )

    assessment = assess_role_page(page)

    assert assessment.is_role is True
    assert assessment.extraction_method == "ats_heuristic"
    assert assessment.title == "Backend Intern"
    assert assessment.location == "Toronto, ON"
    assert assessment.confidence >= 0.8


def test_parse_job_location_normalizes_geograpy_places(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_geograpy_context(text: str) -> SimpleNamespace:
        if "San Mateo" in text:
            return SimpleNamespace(
                cities=["San Mateo"],
                regions=[],
                countries=["United States of America", "Canada"],
                places=["San Mateo", "CA", "United States of America"],
            )
        if "Fremont" in text:
            return SimpleNamespace(
                cities=["Fremont"],
                regions=[],
                countries=["United States of America"],
                places=["Fremont", "California"],
            )
        return SimpleNamespace(
            cities=["Canada", "Location"],
            regions=[],
            countries=["Canada", "United States of America"],
            places=["Location", "BC", "Canada"],
        )

    monkeypatch.setattr(
        "callumployed.webscraping.location_parser._geograpy_context",
        fake_geograpy_context,
    )

    assert parse_job_location("Location: Vancouver, BC, CA") == "Vancouver, BC, Canada"
    assert parse_job_location("Remote - Canada") == "Remote; Canada"
    assert (
        parse_job_location("San Mateo, CA, United States")
        == "San Mateo, CA, United States"
    )
    assert (
        parse_job_location("Fremont, California Req. ID 271209 Job Type Intern")
        == "Fremont, CA"
    )
    assert (
        parse_job_location(
            "PALO ALTO, California Req. ID 270521 Job Type Intern/Apprentice "
            "What to Expect This position is expected to begin around August 2026"
        )
        == "PALO ALTO, CA"
    )
    assert (
        parse_job_location(
            "United States of America State - Select - Tesla © 2026 Privacy & Legal "
            "Help Us Improve Our Website with Cookies"
        )
        is None
    )
    assert parse_job_location("{'@type': 'Country', 'name': 'BR'}") == "Brazil"
    assert (
        parse_job_location("Hybrid; Hybrid; Hybrid; Hybrid; Hybrid; In-Office")
        == "Hybrid; In-office"
    )
    assert parse_job_location("and") is None
    jane_street_nav_location = (
        "S STREET VIEW PUZZLES DEPARTMENTS OPEN ROLES PROGRAMS; "
        "EVENTS INTERNSHIPS INTERVIEWING Join Jane Street Open roles"
    )
    jane_street_context = (
        "Accept All Reject All Software Engineer Internship, May-August "
        "LOCATION New York DEPARTMENT Technology TEAM Software Engineering Apply"
    )
    assert (
        parse_job_location(jane_street_nav_location, context_text=jane_street_context)
        == "New York"
    )
    hrt_nav_location = (
        "s Diversity & Inclusion Contact WHAT WE DO Tech Blog Liquidity Client "
        "Market Making Ventures Disclosures CAREERS Job Openings Work at HRT Life "
        "at HRT Student Opportunities AI & Machine Learning Talent Community "
        "NORTH AMERICA New York City Chicago Austin Boulder Boston Seattle Miami"
    )
    hrt_context = (
        "SKIP NAVIGATION AND JUMP TO CONTENT WHO WE ARE TRADE WITH US TECH BLOG "
        "JOIN OUR TEAM About This Role \ue01d Austin | Chicago | New York | "
        "Singapore \ue600 C++ | Python } Intern \ue608 Job ID: 570 # View All Positions"
    )
    assert (
        parse_job_location(hrt_nav_location, context_text=hrt_context)
        == "Austin; Chicago; New York; Singapore"
    )
    bytedance_nav_location = "s Early Careers Blog Jobs"
    bytedance_context = (
        "Life at ByteDance Teams How We Hire Locations Early Careers Blog Jobs Apply EN "
        "Student Researcher Location: San Jose Team: Technology Employment Type: Intern "
        "Job Code: A123 Requirements Build software."
    )
    assert (
        parse_job_location(bytedance_nav_location, context_text=bytedance_context)
        == "San Jose"
    )
    assert (
        parse_job_location(
            "business needs; market demand",
            context_text=(
                "[2027] Software Engineer, Early Career "
                "San Mateo, CA, United States Early Career"
            ),
        )
        == "San Mateo, CA, United States"
    )
    assert (
        parse_job_location(
            "and",
            context_text=(
                "[2027] Software Engineer, Early Career "
                "Communications San Mateo, CA, United States Early Career"
            ),
        )
        == "San Mateo, CA, United States"
    )
    assert (
        parse_job_location(
            "business needs; market demand",
            context_text="[Summer 2027] Software Engineer Intern San Mateo, CA, United States",
        )
        == "San Mateo, CA, United States"
    )


def test_assess_role_page_extracts_structured_country_object_location() -> None:
    page = RenderedPageState(
        url="https://apply.careers.microsoft.com/careers/job/1",
        final_url="https://apply.careers.microsoft.com/careers/job/1",
        title="Software Engineering INTERN",
        html="""
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "JobPosting",
          "title": "Software Engineering INTERN",
          "description": "Single Position Come build software.",
          "jobLocation": {
            "@type": "Country",
            "name": "BR"
          }
        }
        </script>
        """,
    )

    assessment = assess_role_page(page)

    assert assessment.location == "Brazil"
    assert assessment.description == "Come build software."


def test_assess_role_page_cleans_roblox_listing_title_metadata() -> None:
    page = RenderedPageState(
        url="https://careers.roblox.com/jobs/8072244",
        final_url="https://careers.roblox.com/jobs/8072244",
        title="View Job | Roblox",
        html="""
        <html>
          <body>
            <h1>[2027] Software Engineer, Early Career</h1>
            <a>Apply Now</a>
            <section>Location San Mateo, CA, United States</section>
          </body>
        </html>
        """,
        visible_text=(
            "[2027] Software Engineer, Early Career Communications "
            "San Mateo, CA, United States Early Career Apply Now"
        ),
    )

    assessment = assess_role_page(
        page,
        title_hints=(
            "[2027] Software Engineer, Early Career Communications "
            "San Mateo, CA, United States Early Career",
        ),
    )

    assert assessment.is_role
    assert assessment.title == "[2027] Software Engineer, Early Career"

    assessment = assess_role_page(
        page,
        title_hints=("[2027] Software Engineer, Early Career San Mateo, CA,",),
    )

    assert assessment.title == "[2027] Software Engineer, Early Career"


def test_assess_role_page_extracts_location_from_job_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "callumployed.webscraping.location_parser._geograpy_context",
        lambda text: SimpleNamespace(
            cities=["Toronto", "Waterloo", "Ontario"],
            regions=[],
            countries=["Canada", "United States of America"],
            places=["Toronto", "Waterloo", "Ontario"],
        ),
    )
    page = RenderedPageState(
        url="https://jobs.lever.co/acme/backend-intern",
        final_url="https://jobs.lever.co/acme/backend-intern",
        title="Backend Intern",
        html="""
        <h1>Backend Intern</h1>
        <section>
          This role is based in Toronto, ON or Waterloo, Ontario.
          Job description. Responsibilities. Requirements. Apply now.
        </section>
        """,
    )

    assessment = assess_role_page(page)

    assert assessment.is_role is True
    assert assessment.location == "Toronto, ON; Waterloo, ON"


def test_assess_role_page_cleans_google_rendered_job_card() -> None:
    page = RenderedPageState(
        url=(
            "https://www.google.com/about/careers/applications/jobs/results/"
            "85564713261245126-software-engineering-intern-bs-summer-2027"
        ),
        final_url=(
            "https://www.google.com/about/careers/applications/jobs/results/"
            "85564713261245126-software-engineering-intern-bs-summer-2027"
        ),
        title="Software Engineering Intern, BS, Summer 2027",
        html="""
        <main>
          Software Engineering Intern, BS, Summer 2027
          link Copy link
          email Email a friend
          corporate_fare Google place Mountain View, CA, USA ; Atlanta, GA, USA ;
          +29 more ; +28 more bar_chart Intern & Apprentice
          info_outline
          This posting is for students who want early consideration for our Summer 2027 roles.
          Applications will be reviewed on a rolling basis.
          Participation in the internship program requires that you are located in the United
          States for the duration of the internship program.
          ## Minimum qualifications
          Pursuing a Bachelor's degree or post secondary training experience.
          ## Preferred qualifications
          Returning to a degree program after completion of the internship.
          ## About the job
          Join us for a unique 12-14 week paid internship.
          Benefits for this role include medical coverage.
        </main>
        """,
    )

    assessment = assess_role_page(
        page,
        title_hints=("Learn more about Software Engineering Intern, BS, Summer 2027",),
    )

    assert assessment.is_role is True
    assert assessment.title == "Software Engineering Intern, BS, Summer 2027"
    assert assessment.location == (
        "Mountain View, CA, United States; Atlanta, GA, United States; Multiple locations"
    )
    assert assessment.description is not None
    assert assessment.description.startswith(
        "This posting is for students who want early consideration"
    )
    assert "Copy link" not in assessment.description
    assert "Email a friend" not in assessment.description
    assert "corporate_fare" not in assessment.description
    assert "Benefits for this role include" not in assessment.description


def test_extract_job_description_trims_boilerplate_and_duplicates() -> None:
    soup = BeautifulSoup(
        """
        <main>
          <h2>What to Expect</h2>
          <p>Build software for manufacturing systems.</p>
          <h2>What You'll Do</h2>
          <ul>
            <li>Build tools and automation.</li>
            <li>Build tools and automation.</li>
            <li>Inspect network protocols.</li>
          </ul>
          <h2>Benefits</h2>
          <p>Medical plans and dental plans.</p>
          <h2>Equal Opportunity</h2>
          <p>Tesla is an Equal Opportunity employer.</p>
        </main>
        """,
        "lxml",
    )

    description = extract_job_description(soup)

    assert description == "\n".join(
        [
            "## What to Expect",
            "Build software for manufacturing systems.",
            "## What You'll Do",
            "Build tools and automation.",
            "Inspect network protocols.",
        ]
    )


def test_extract_job_description_dedupes_inline_repeated_sections() -> None:
    repeated_core = (
        "Consider before submitting an application: This position is expected to "
        "start August or September 2026. Internship Programs at Tesla The Internship "
        "Recruiting Team is driven by the passion to recognize emerging talent. "
        "About the Team Manufacturing software is one of the most critical and "
        "innovative areas to work in at Tesla. What You'll Do Build tools, "
        "test-automation, and documentation. What You'll Bring Proficiency in Go, "
        "TCP/IP, Networking Programming, and related technologies. "
    )
    soup = BeautifulSoup(
        f"""
        <main>
          <div class="job-description">
            {repeated_core}
            Benefits As a full-time Tesla Intern, you will be eligible for medical plans.
            {repeated_core}
            Tesla is an Equal Opportunity employer.
          </div>
        </main>
        """,
        "lxml",
    )

    description = extract_job_description(soup)

    assert description is not None
    assert description.count("Consider before submitting an application") == 1
    assert "What You'll Do Build tools" in description
    assert "What You'll Bring Proficiency" in description
    assert "## What You'll Do" not in description
    assert "Benefits" not in description
    assert "Equal Opportunity" not in description


def test_extract_job_description_formats_real_heading_sections_only() -> None:
    soup = BeautifulSoup(
        """
        <main>
          <div class="job-description">
            <p>You will take responsibilities seriously in production systems.</p>
            <h2>Responsibilities</h2>
            <p>Build reliable services.</p>
            <p>The requirements vary by team and product area.</p>
            <h2>Requirements</h2>
            <ul>
              <li>Write clear software.</li>
            </ul>
          </div>
        </main>
        """,
        "lxml",
    )

    description = extract_job_description(soup)

    assert description == "\n".join(
        [
            "You will take responsibilities seriously in production systems.",
            "## Responsibilities",
            "Build reliable services.",
            "The requirements vary by team and product area.",
            "## Requirements",
            "Write clear software.",
        ]
    )


def test_extract_job_description_rejects_tesla_error_shell() -> None:
    soup = BeautifulSoup(
        """
        <main>
          <h1>Build your Career at Tesla</h1>
          <p>Tesla homepage Careers Skip to main content Explore Jobs Manufacturing AI
          Terafab Vehicle Software Internships About Us Profile US Build your Career at
          Tesla An error has occurred The website encountered an unexpected error.
          Please try again later.</p>
          <p>Internship, Charging Data Modeling, Machine Learning Engineer (Fall 2026)
          Job Category Vehicle Software Location PALO ALTO, California Req.</p>
          <p>ID 278249 Job Type Intern/Apprentice Apply Tesla © 2026 Privacy & Legal
          Tesla Connect Help Us Improve Our Website with Cookies We use cookies and
          process data from your device to analyze website performance.</p>
        </main>
        """,
        "lxml",
    )

    assert extract_job_description(soup) is None


def test_clean_job_description_trims_sig_privacy_policy() -> None:
    description = clean_job_description(
        """
        Toggle navigation
        What We Do
        Blog
        Bala Cynwyd (Philadelphia Area), Pennsylvania Technology - Software Engineering
        JOB_DESCRIPTION.SHARE.HTML
        Job Description
        Susquehanna is looking for highly motivated full-time students for our internship.
        Enrolled in a bachelor's or master's program in computer science.
        What's in it for you:
        Housing provided for duration of internship
        About Susquehanna
        Susquehanna is a global quantitative trading firm powered by scientific rigor.
        If you're a recruiting agency and want to partner with us, please reach out.
        This Website collects some Personal Data from its Users.
        Owner and Data Controller
        Types of Data collected
        """
    )

    assert description == "\n".join(
        [
            "## Job Description",
            "Susquehanna is looking for highly motivated full-time students for our internship.",
            "Enrolled in a bachelor's or master's program in computer science.",
            "## What's in it for you",
            "Housing provided for duration of internship",
            "## About Susquehanna",
            "Susquehanna is a global quantitative trading firm powered by scientific rigor.",
        ]
    )


def test_clean_job_description_splits_inline_section_headings_and_dash_bullets() -> None:
    description = clean_job_description(
        "Software Engineer – Intern (US) New York, Miami Job Description At Citadel "
        "Securities, engineers work in small teams. Your Objectives: - Create tools "
        "that bring trading strategies to life - Develop high-performance research "
        "platforms - Work in small teams to build the future of finance Your Skills "
        "& Talents: - Exceptional programming and design skills - Strong analytical "
        "skills About Citadel Securities Citadel Securities is a technology-driven "
        "market maker."
    )

    assert description == "\n".join(
        [
            "## Job Description",
            "At Citadel Securities, engineers work in small teams.",
            "## Your Objectives",
            "Create tools that bring trading strategies to life",
            "Develop high-performance research platforms",
            "Work in small teams to build the future of finance",
            "## Your Skills & Talents",
            "Exceptional programming and design skills",
            "Strong analytical skills",
            "## About Citadel Securities",
            "Citadel Securities is a technology-driven market maker.",
        ]
    )


def test_clean_job_description_formats_known_line_start_section_labels() -> None:
    description = clean_job_description(
        "\n".join(
            [
                "Consider before submitting an application:",
                "Read timing details before applying.",
                "About the Team:",
                "Build charging infrastructure models.",
                "Job Responsibilities:",
                "Translate internal documents.",
                "Minimum Qualifications:",
                "Strong programming skills.",
                "Preferred Qualifications:",
                "Experience with time-series datasets.",
            ]
        )
    )

    assert description == "\n".join(
        [
            "Consider before submitting an application:",
            "Read timing details before applying.",
            "## About the Team",
            "Build charging infrastructure models.",
            "## Job Responsibilities",
            "Translate internal documents.",
            "## Minimum Qualifications",
            "Strong programming skills.",
            "## Preferred Qualifications",
            "Experience with time-series datasets.",
        ]
    )


def test_assess_role_page_cleans_tesla_style_description() -> None:
    page = RenderedPageState(
        url="https://www.tesla.com/careers/search/job/internship-software-engineer-it-apps",
        final_url="https://www.tesla.com/careers/search/job/internship-software-engineer-it-apps",
        title="Internship, Software Engineer, IT Apps",
        html="""
        <main>
          <h1>Internship, Software Engineer, IT Apps</h1>
          <div class="tds-content_container">
            <p>Fremont, California</p>
            <p>Req. ID 271209</p>
            <h2>What to Expect</h2>
            <p>Consider before submitting an application.</p>
            <h2>What You'll Do</h2>
            <p>Build tools, test-automation, and documentation.</p>
            <h2>What You'll Bring</h2>
            <p>Proficiency in Go, TCP/IP, and related technologies.</p>
            <h2>Benefits</h2>
            <p>Medical plans and family-building benefits.</p>
            <h2>Equal Opportunity</h2>
            <p>Tesla is an Equal Opportunity employer.</p>
            <h2>What to Expect</h2>
            <p>Consider before submitting an application.</p>
          </div>
        </main>
        """,
        visible_text=(
            "Fremont, California Req. ID 271209 What to Expect Consider before "
            "submitting an application. What You'll Do Build tools, test-automation, "
            "and documentation. Benefits Medical plans."
        ),
    )

    assessment = assess_role_page(page)

    assert assessment.is_role is True
    assert assessment.description == "\n".join(
        [
            "## What to Expect",
            "Consider before submitting an application.",
            "## What You'll Do",
            "Build tools, test-automation, and documentation.",
            "## What You'll Bring",
            "Proficiency in Go, TCP/IP, and related technologies.",
        ]
    )
    assert "Equal Opportunity" not in assessment.description
    assert "Medical plans" not in assessment.description


def test_assess_role_page_accepts_common_job_section_signals() -> None:
    page = RenderedPageState(
        url=(
            "https://jobs.apple.com/en-ca/details/200664780-3810/"
            "machine-learning-and-artificial-intelligence-undergrad-internships?team=STDNT"
        ),
        final_url=(
            "https://jobs.apple.com/en-ca/details/200664780-3810/"
            "machine-learning-and-artificial-intelligence-undergrad-internships?team=STDNT"
        ),
        title="Machine Learning and Artificial Intelligence Undergrad Internships",
        html="""
        <h1>Machine Learning and Artificial Intelligence Undergrad Internships</h1>
        <section>Description</section>
        <section>Minimum Qualifications</section>
        <section>Pay & Benefits</section>
        <section>Compensation</section>
        """,
    )

    assessment = assess_role_page(page)

    assert assessment.is_role is True
    assert assessment.extraction_method == "html_heuristic"
    assert assessment.confidence == 0.66
    assert "description" in assessment.reasons
    assert "qualifications" in assessment.reasons


def test_assess_role_page_uses_url_slug_when_dom_title_is_noisy() -> None:
    page = RenderedPageState(
        url=(
            "https://www.tesla.com/careers/search/job/"
            "internship-software-engineer-vehicle-ui-development-fall-2026-270063"
        ),
        final_url=(
            "https://www.tesla.com/careers/search/job/"
            "internship-software-engineer-vehicle-ui-development-fall-2026-270063"
        ),
        title="Tesla homepage Careers Skip to main content",
        html="""
        <h1>Tesla homepage Careers Skip to main content</h1>
        <section>Job description. Responsibilities. Requirements. Apply now.</section>
        """,
    )

    assessment = assess_role_page(page)

    assert assessment.is_role is True
    assert assessment.title == "Internship Software Engineer Vehicle UI Development Fall 2026"
    assert assessment.posting_id == "270063"
    assert "title: URL slug" in assessment.reasons


def test_assess_role_page_rejects_tesla_error_shell() -> None:
    page = RenderedPageState(
        url=(
            "https://www.tesla.com/careers/search/job/"
            "internship-charging-data-modeling-machine-learning-engineer-fall-2026-278249"
        ),
        final_url=(
            "https://www.tesla.com/careers/search/job/"
            "internship-charging-data-modeling-machine-learning-engineer-fall-2026-278249"
        ),
        title="Tesla homepage Careers Skip to main content",
        html="""
        <main>
          <h1>Tesla homepage Careers Skip to main content</h1>
          <p>Build your Career at Tesla An error has occurred The website encountered
          an unexpected error. Please try again later.</p>
          <p>Internship, Charging Data Modeling, Machine Learning Engineer (Fall 2026)
          Job Category Vehicle Software Location PALO ALTO, California Req.</p>
          <p>ID 278249 Job Type Intern/Apprentice Apply Tesla © 2026 Privacy & Legal
          Help Us Improve Our Website with Cookies.</p>
        </main>
        """,
    )

    assessment = assess_role_page(
        page,
        title_hints=("Internship, Charging Data Modeling, Machine Learning Engineer (Fall 2026)",),
    )

    assert assessment.is_role is False
    assert assessment.description is None
    assert assessment.rejection_reason == "page rendered a transient error shell"
    assert assessment.posting_id == "278249"


def test_assess_role_page_prefers_selected_link_title_hint_over_generic_h1() -> None:
    page = RenderedPageState(
        url="https://example.com/careers/search/job/software-engineer-intern-12345",
        final_url="https://example.com/careers/search/job/software-engineer-intern-12345",
        title="Careers",
        html="""
        <h1>Careers</h1>
        <section>Job description. Responsibilities. Requirements. Apply now.</section>
        """,
    )

    assessment = assess_role_page(page, title_hints=("Backend Platform Intern",))

    assert assessment.is_role is True
    assert assessment.title == "Backend Platform Intern"
    assert assessment.posting_id == "12345"
    assert "title: selected link text" in assessment.reasons


def test_assess_role_page_ignores_amazon_search_location_chrome() -> None:
    page = RenderedPageState(
        url="https://www.amazon.jobs/jobs/3116030",
        final_url=(
            "https://www.amazon.jobs/en/jobs/3116030/"
            "software-development-engineer-internship-fall-2026-us"
        ),
        title="Software Development Engineer Internship - Amazon Jobs",
        html="""
        <header>
          <div class="location-search">Search for jobs by title; keyword search job by location</div>
        </header>
        <main>
          <h1>Software Development Engineer Internship</h1>
          <p>Fall 2026 (US)</p>
          <p>Job ID: 3116030 | Amazon.com Services LLC</p>
          <p>Apply now</p>
          <section>Description</section>
          <p>Build software systems for production services.</p>
          <section>Basic Qualifications</section>
        </main>
        """,
        visible_text=(
            "Search for jobs by title; keyword search job by location "
            "Software Development Engineer Internship Fall 2026 (US) "
            "Job ID: 3116030 | Amazon.com Services LLC Apply now "
            "Description Build software systems for production services."
        ),
    )

    assessment = assess_role_page(
        page,
        title_hints=("Software Development Engineer Internship - Fall 2026 (US)",),
    )

    assert assessment.is_role is True
    assert assessment.location == "United States"
    assert assessment.posting_id == "3116030"


def test_parse_job_location_trims_amazon_posted_metadata() -> None:
    assert (
        parse_job_location(
            "United States, WA, Seattle Posted: August 1, 2026 "
            "(Updated about 1 hour ago) Software Development Engineer II, SKG"
        )
        == "United States, WA, Seattle"
    )


def test_assess_role_page_cleans_job_card_title_hint_suffixes() -> None:
    page = RenderedPageState(
        url="https://www.jumptrading.com/hr/job?gh_jid=8002989",
        final_url="https://www.jumptrading.com/hr/job?gh_jid=8002989",
        title="job",
        html="""
        <section>Job description. Responsibilities. Requirements. Apply now.</section>
        """,
    )

    assessment = assess_role_page(
        page,
        title_hints=("Campus Software Engineer (Intern) Chicago Apply",),
    )

    assert assessment.is_role is True
    assert assessment.title == "Campus Software Engineer (Intern)"


def test_assess_role_page_cleans_greenhouse_listing_card_title_hint() -> None:
    page = RenderedPageState(
        url="https://boards.greenhouse.io/cloudflare/jobs/8066589?gh_jid=8066589",
        final_url="https://job-boards.greenhouse.io/cloudflare/jobs/8066589?gh_jid=8066589",
        title="Job Application for Distributed Systems Engineer at Cloudflare",
        html="""
        <section>Job description. Responsibilities. Requirements. Apply now.</section>
        """,
    )

    assessment = assess_role_page(
        page,
        title_hints=(
            "Distributed Systems Engineer Engineering - Bengaluru, India "
            "Posted Jul 16, 2026 View role",
        ),
    )

    assert assessment.is_role is True
    assert assessment.title == "Distributed Systems Engineer"


def test_assess_role_page_cleans_jane_street_listing_card_title_hint() -> None:
    page = RenderedPageState(
        url="https://www.janestreet.com/join-jane-street/position/8599644002/",
        final_url="https://www.janestreet.com/join-jane-street/position/8599644002/",
        title="Software Engineer, New York :: Jane Street",
        html="""
        <section>Job description. Responsibilities. Requirements. Apply now.</section>
        """,
    )

    assessment = assess_role_page(
        page,
        title_hints=("Software Engineer Internship New York Technology May-August",),
    )

    assert assessment.is_role is True
    assert assessment.title == "Software Engineer Internship"


def test_assess_role_page_rejects_generic_careers_listing() -> None:
    page = RenderedPageState(
        url="https://example.com/careers/search",
        final_url="https://example.com/careers/search",
        title="Careers",
        html="""
        <h1>Open positions</h1>
        <p>Search jobs across teams and view all jobs.</p>
        <a href="/jobs/backend-intern">Backend Intern</a>
        """,
    )

    assessment = assess_role_page(page)

    assert assessment.is_role is False
    assert assessment.extraction_method == "html_heuristic"
    assert assessment.rejection_reason == "page looks like a careers search/listing page"


def test_scan_careers_page_orchestrates_render_extract_and_score(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rendered_external_browser_ports: list[int | None] = []

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
    ) -> RenderedPageState:
        rendered_external_browser_ports.append(external_browser_port)
        page = _fixture_page()
        return page.model_copy(update={"url": url})

    monkeypatch.setattr(
        "callumployed.webscraping.scanner.render_careers_page",
        fake_render_careers_page,
    )

    result = asyncio.run(
        scan_careers_page(
            "https://example.com/careers",
            external_browser_port=9222,
        )
    )

    assert rendered_external_browser_ports == [9222]
    assert result.source_url == "https://example.com/careers"
    assert result.final_url == "https://example.com/careers"
    assert result.title == "Example Careers"
    assert result.candidates_scanned >= 3
    assert len(result.candidates) == result.candidates_scanned
    assert len(result.links) == 3
    assert result.confidence is ExtractionConfidence.HIGH


def test_scan_careers_page_merges_agent_classified_ambiguous_links(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
    ) -> RenderedPageState:
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Example Careers",
            html="""
            <a href="/openings/software-intern">Software Intern</a>
            <a href="/about">About</a>
            """,
        )

    agent_candidate_urls: list[str] = []

    async def fake_agent_classifier(
        candidates: list[ScoredLinkCandidate],
        page: RenderedPageState,
    ) -> list[DiscoveredJobLink]:
        agent_candidate_urls.extend(candidate.url for candidate in candidates)
        return [
            DiscoveredJobLink(
                url="https://example.com/openings/software-intern",
                source_url=page.final_url,
                text="Software Intern",
                confidence=0.91,
                discovery_method="agent",
                reasons=["Specific role page."],
            )
        ]

    monkeypatch.setattr(
        "callumployed.webscraping.scanner.render_careers_page",
        fake_render_careers_page,
    )

    result = asyncio.run(
        scan_careers_page(
            "https://example.com/careers",
            agent_classifier=fake_agent_classifier,
        )
    )

    assert "https://example.com/openings/software-intern" in agent_candidate_urls
    assert len(result.links) == 1
    assert result.links[0].discovery_method == "agent"
    assert result.confidence is ExtractionConfidence.MEDIUM


def test_render_with_context_closes_page_after_snapshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeResponse:
        status = 200

    class FakeBodyLocator:
        async def inner_text(self, *, timeout: int) -> str:
            return "Example Careers"

    class FakePage:
        url = "https://example.com/careers"

        def __init__(self) -> None:
            self.closed = False

        async def goto(self, url: str, *, wait_until: str, timeout: int) -> FakeResponse:
            return FakeResponse()

        async def wait_for_load_state(self, state: str, *, timeout: int) -> None:
            return None

        async def title(self) -> str:
            return "Example Careers"

        async def content(self) -> str:
            return "<html><body>Example Careers</body></html>"

        def locator(self, selector: str) -> FakeBodyLocator:
            return FakeBodyLocator()

        async def close(self) -> None:
            self.closed = True

    class FakeContext:
        def __init__(self) -> None:
            self.page = FakePage()

        def set_default_timeout(self, timeout: int) -> None:
            return None

        def set_default_navigation_timeout(self, timeout: int) -> None:
            return None

        async def route(self, pattern: str, handler: object) -> None:
            return None

        async def new_page(self) -> FakePage:
            return self.page

    async def fake_wait_for_dynamic_content(
        page: object,
        *,
        timeout_ms: int,
        **_settle_options: object,
    ) -> None:
        return None

    monkeypatch.setattr(
        "callumployed.webscraping.browser._wait_for_dynamic_content",
        fake_wait_for_dynamic_content,
    )
    context = FakeContext()

    result = asyncio.run(
        _render_with_context(
            context,  # type: ignore[arg-type]
            "https://example.com/careers",
            timeout_ms=1_000,
            blocked_types=set(),
        )
    )

    assert result.final_url == "https://example.com/careers"
    assert context.page.closed is True


def test_render_with_context_tolerates_networkidle_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeResponse:
        status = 200

    class FakeBodyLocator:
        async def inner_text(self, *, timeout: int) -> str:
            return "Software Engineer Intern"

    class FakePage:
        url = "https://example.com/careers"

        def __init__(self) -> None:
            self.closed = False

        async def goto(self, url: str, *, wait_until: str, timeout: int) -> FakeResponse:
            return FakeResponse()

        async def wait_for_load_state(self, state: str, *, timeout: int) -> None:
            raise PlaywrightTimeoutError("networkidle timeout")

        async def title(self) -> str:
            return "Example Careers"

        async def content(self) -> str:
            return "<html><body><a href='/jobs/1'>Software Engineer Intern</a></body></html>"

        def locator(self, selector: str) -> FakeBodyLocator:
            return FakeBodyLocator()

        async def close(self) -> None:
            self.closed = True

    class FakeContext:
        def __init__(self) -> None:
            self.page = FakePage()

        def set_default_timeout(self, timeout: int) -> None:
            return None

        def set_default_navigation_timeout(self, timeout: int) -> None:
            return None

        async def route(self, pattern: str, handler: object) -> None:
            return None

        async def new_page(self) -> FakePage:
            return self.page

    async def fake_wait_for_dynamic_content(
        page: object,
        *,
        timeout_ms: int,
        **_settle_options: object,
    ) -> None:
        return None

    monkeypatch.setattr(
        "callumployed.webscraping.browser._wait_for_dynamic_content",
        fake_wait_for_dynamic_content,
    )
    context = FakeContext()

    result = asyncio.run(
        _render_with_context(
            context,  # type: ignore[arg-type]
            "https://example.com/careers",
            timeout_ms=1_000,
            blocked_types=set(),
        )
    )

    assert result.title == "Example Careers"
    assert "Software Engineer Intern" in result.html
    assert context.page.closed is True


def test_managed_browser_profile_path_uses_app_data_dir() -> None:
    profile_path = managed_browser_profile_path()

    assert profile_path.name == PROFILE_DIR_NAME
    assert "callumployed" in profile_path.parts


def test_navigation_error_message_for_403_recommends_external_browser() -> None:
    message = navigation_error_message("https://example.com", 403)

    assert "managed browser profile" in message
