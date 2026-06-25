import re
from typing import Any
from urllib.parse import urlparse

import extruct  # type: ignore[import-untyped]
import trafilatura
from bs4 import BeautifulSoup

from callumployed.webscraping.models import RenderedPageState, RolePageAssessment

ATS_DOMAINS = (
    "ashbyhq.com",
    "bamboohr.com",
    "greenhouse.io",
    "jobs.ashbyhq.com",
    "jobs.lever.co",
    "lever.co",
    "myworkdayjobs.com",
    "smartrecruiters.com",
    "workable.com",
)
ROLE_PATH_TERMS = (
    "/apply",
    "/details/",
    "/job",
    "/jobs/",
    "/position",
    "/requisition",
    "/role",
)
LISTING_PATH_TERMS = (
    "/careers",
    "/jobs",
    "/search",
    "/open-roles",
)
ROLE_TEXT_TERMS = (
    "apply now",
    "employment type",
    "job description",
    "job id",
    "location",
    "responsibilities",
    "requirements",
)
CLOSED_TERMS = (
    "application closed",
    "applications are closed",
    "closed role",
    "job is closed",
    "no longer accepting applications",
    "not accepting applications",
    "position has been filled",
)
GENERIC_LISTING_TERMS = (
    "job search",
    "open positions",
    "search jobs",
    "view all jobs",
)
POSTING_ID_PATTERN = re.compile(r"\b(?:job|req|requisition)\s*(?:id|#)?\s*:?\s*([a-z0-9-]+)", re.I)


def assess_role_page(page: RenderedPageState) -> RolePageAssessment:
    structured_posting = _extract_structured_job_posting(page)
    if structured_posting is not None:
        title = _first_string(structured_posting.get("title"), structured_posting.get("name"))
        description = _clean_text(_first_string(structured_posting.get("description")))
        return RolePageAssessment(
            is_role=True,
            is_closed=_is_closed_page(page, description),
            confidence=0.95,
            title=title or page.title,
            location=_extract_job_location(structured_posting),
            description=description or _extract_main_text(page),
            posting_id=_extract_posting_id(structured_posting, page),
            extraction_method="jobposting_structured_data",
            reasons=["schema.org JobPosting structured data"],
        )

    parsed = urlparse(page.final_url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    soup = BeautifulSoup(page.html, "lxml")
    title = _extract_dom_title(soup) or page.title
    description = _extract_main_text(page)
    visible_text = _clean_text(" ".join(part for part in (page.visible_text, description) if part))
    is_closed = _is_closed_page(page, visible_text)

    if _is_ats_role_page(domain, path, visible_text):
        return RolePageAssessment(
            is_role=True,
            is_closed=is_closed,
            confidence=0.82 if not is_closed else 0.72,
            title=title,
            location=_extract_dom_location(soup, visible_text),
            description=description,
            posting_id=_extract_posting_id({}, page),
            extraction_method="ats_heuristic",
            reasons=[
                "known ATS/job-board URL",
                *_matching_terms(visible_text, ROLE_TEXT_TERMS)[:3],
            ],
        )

    if _looks_like_listing_page(path, visible_text):
        return RolePageAssessment(
            is_role=False,
            is_closed=is_closed,
            confidence=0.78,
            title=title,
            description=description,
            extraction_method="html_heuristic",
            rejection_reason="page looks like a careers search/listing page",
            reasons=["listing/search page signals"],
        )

    role_text_matches = _matching_terms(visible_text, ROLE_TEXT_TERMS)
    if title and role_text_matches:
        return RolePageAssessment(
            is_role=True,
            is_closed=is_closed,
            confidence=0.66 if not is_closed else 0.58,
            title=title,
            location=_extract_dom_location(soup, visible_text),
            description=description,
            posting_id=_extract_posting_id({}, page),
            extraction_method="html_heuristic",
            reasons=["job-like page title", *role_text_matches[:3]],
        )

    return RolePageAssessment(
        is_role=False,
        is_closed=is_closed,
        confidence=0.35,
        title=title,
        description=description,
        extraction_method="html_heuristic",
        rejection_reason="deterministic evidence is weak; LLM fallback recommended",
        reasons=["no structured JobPosting and weak page signals"],
    )


def _extract_structured_job_posting(page: RenderedPageState) -> dict[str, Any] | None:
    data = extruct.extract(
        page.html,
        base_url=page.final_url,
        syntaxes=["json-ld", "microdata", "rdfa"],
        uniform=True,
    )
    for item in _walk_structured_items(data):
        types = item.get("@type") or item.get("type")
        type_values = types if isinstance(types, list) else [types]
        if any(str(value).lower().endswith("jobposting") for value in type_values if value):
            return item
    return None


def _walk_structured_items(value: Any) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if isinstance(value, dict):
        items.append(value)
        graph = value.get("@graph")
        if graph is not None:
            items.extend(_walk_structured_items(graph))
        for nested in value.values():
            if isinstance(nested, dict | list):
                items.extend(_walk_structured_items(nested))
    elif isinstance(value, list):
        for item in value:
            items.extend(_walk_structured_items(item))
    return items


def _extract_main_text(page: RenderedPageState) -> str | None:
    extracted = trafilatura.extract(
        page.html,
        url=page.final_url,
        include_comments=False,
        include_tables=False,
    )
    if extracted:
        return _clean_text(extracted)
    if page.visible_text:
        return _clean_text(page.visible_text)
    soup = BeautifulSoup(page.html, "lxml")
    return _clean_text(soup.get_text(" ", strip=True))


def _extract_dom_title(soup: BeautifulSoup) -> str | None:
    selectors = (
        "h1",
        "[data-testid*=job][data-testid*=title]",
        "[class*=job-title]",
        "[class*=position-title]",
    )
    for selector in selectors:
        element = soup.select_one(selector)
        if element is not None:
            text = _clean_text(element.get_text(" ", strip=True))
            if text:
                return text
    return None


def _extract_dom_location(soup: BeautifulSoup, visible_text: str | None) -> str | None:
    selectors = (
        "[data-testid*=location]",
        "[class*=location]",
        "[class*=job-location]",
    )
    for selector in selectors:
        element = soup.select_one(selector)
        if element is not None:
            text = _clean_text(element.get_text(" ", strip=True))
            if text:
                return text
    if not visible_text:
        return None
    match = re.search(r"\b(?:location|office)\s*:?\s*([^\n|]+)", visible_text, re.I)
    return _clean_text(match.group(1)) if match else None


def _extract_job_location(posting: dict[str, Any]) -> str | None:
    location = posting.get("jobLocation") or posting.get("applicantLocationRequirements")
    if isinstance(location, list):
        return "; ".join(filter(None, (_stringify_location(item) for item in location))) or None
    return _stringify_location(location)


def _stringify_location(location: Any) -> str | None:
    if isinstance(location, str):
        return _clean_text(location)
    if not isinstance(location, dict):
        return None
    address = location.get("address")
    if isinstance(address, dict):
        parts = (
            address.get("addressLocality"),
            address.get("addressRegion"),
            address.get("addressCountry"),
        )
        return _clean_text(", ".join(str(part) for part in parts if part))
    return _first_string(location.get("name"), location.get("address"))


def _extract_posting_id(posting: dict[str, Any], page: RenderedPageState) -> str | None:
    identifier = posting.get("identifier")
    if isinstance(identifier, dict):
        posting_id = _first_string(identifier.get("value"), identifier.get("name"))
        if posting_id:
            return posting_id
    if isinstance(identifier, str):
        return _clean_text(identifier)
    haystack = " ".join(part for part in (page.final_url, page.title, page.visible_text) if part)
    match = POSTING_ID_PATTERN.search(haystack)
    if match:
        return match.group(1)
    return None


def _is_ats_role_page(domain: str, path: str, visible_text: str | None) -> bool:
    if not any(domain == ats or domain.endswith(f".{ats}") for ats in ATS_DOMAINS):
        return False
    return any(term in path for term in ROLE_PATH_TERMS) or bool(
        visible_text and _matching_terms(visible_text, ROLE_TEXT_TERMS)
    )


def _looks_like_listing_page(path: str, visible_text: str | None) -> bool:
    if not visible_text:
        return False
    has_listing_path = any(term in path for term in LISTING_PATH_TERMS)
    has_listing_text = bool(_matching_terms(visible_text, GENERIC_LISTING_TERMS))
    has_role_text = bool(_matching_terms(visible_text, ROLE_TEXT_TERMS))
    return has_listing_path and has_listing_text and not has_role_text


def _is_closed_page(page: RenderedPageState, text: str | None) -> bool:
    haystack = " ".join(
        part for part in (page.final_url, page.title, page.visible_text, text) if part
    )
    return bool(_matching_terms(haystack, CLOSED_TERMS))


def _matching_terms(text: str | None, terms: tuple[str, ...]) -> list[str]:
    if not text:
        return []
    lowered = text.lower()
    return [term for term in terms if term in lowered]


def _first_string(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, str):
            cleaned = _clean_text(value)
            if cleaned:
                return cleaned
    return None


def _clean_text(text: str | None) -> str | None:
    if text is None:
        return None
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned or None
