import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

import extruct  # type: ignore[import-untyped]
import trafilatura  # type: ignore[import-untyped]
from bs4 import BeautifulSoup

from callumployed.webscraping.description_parser import extract_job_description
from callumployed.webscraping.location_parser import parse_job_location
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
    "apply",
    "employment type",
    "job description",
    "description",
    "job id",
    "location",
    "responsibilities",
    "requirements",
    "qualifications",
    "minimum qualifications",
    "preferred qualifications",
    "compensation",
    "pay",
    "pay range",
    "base pay",
    "base salary",
    "salary",
    "hourly",
    "hourly rate",
    "benefits",
    "pay & benefits",
    "about the role",
    "about this role",
    "about the job",
    "what you'll do",
    "what you will do",
    "who you are",
    "equal opportunity",
    "reasonable accommodation",
    "accommodation",
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
    "careers",
    "job search",
    "jobs",
    "open positions",
    "search jobs",
    "view all jobs",
)
POSTING_ID_PATTERN = re.compile(
    r"\b(?:job\s*(?:id|#)|req(?:uisition)?\s*(?:id|#)?)\s*:?\s*([a-z0-9-]+)",
    re.I,
)
POSTING_ID_URL_PATTERN = re.compile(r"-(\d{4,})(?:[/#?]|$)")
ROLE_TITLE_TERMS = (
    "analyst",
    "architect",
    "associate",
    "backend",
    "coordinator",
    "data",
    "developer",
    "designer",
    "engineer",
    "frontend",
    "full stack",
    "intern",
    "internship",
    "manager",
    "mobile",
    "product",
    "program",
    "research",
    "scientist",
    "security",
    "software",
    "specialist",
)
TITLE_NOISE_TERMS = (
    "apply",
    "career",
    "careers",
    "cookie",
    "homepage",
    "job alert",
    "job search",
    "login",
    "privacy",
    "search jobs",
    "sign in",
    "skip to main content",
    "view role",
    "view all jobs",
)
TITLE_SEPARATOR_PATTERN = re.compile(r"\s+(?:[-|–—•·]|::)\s+")
TITLE_ACTION_SUFFIX_PATTERN = re.compile(
    r"\s+(?:apply(?:\s+now)?|view\s+role)\s*$",
    re.I,
)
TITLE_POSTED_SUFFIX_PATTERN = re.compile(
    r"\s+posted\s+[a-z]{3,9}\s+\d{1,2},\s+\d{4}\b.*$",
    re.I,
)
TITLE_LOCATION_PATTERN = re.compile(
    r"\b(?:"
    r"amsterdam|austin|bengaluru|carrollton|chicago|hong kong|lisbon|london|"
    r"mumbai|new york(?: city)?|singapore|shanghai|sydney|washington dc|"
    r"ny|nyc|tx|us|united states|portugal|india"
    r")\b",
    re.I,
)
TITLE_SEASON_PATTERN = re.compile(
    r"(?:fall|spring|summer|winter|may-august|june-september|flexible)\b",
    re.I,
)
TITLE_DEPARTMENT_SUFFIXES = {
    "business",
    "communications",
    "design",
    "engineering",
    "finance",
    "legal",
    "marketing",
    "operations",
    "product",
    "research",
    "sales",
    "security",
    "technology",
}
TITLE_CITY_REGION_COUNTRY_PATTERN = re.compile(
    r"\b([A-Z][A-Za-z .'-]{1,80}),\s*"
    r"(?:AB|BC|MB|NB|NL|NS|NT|NU|ON|PE|QC|SK|YT|CA|NY|WA|TX|IL|FL|"
    r"California|New York|Washington|Texas|Illinois|Florida),\s*"
    r"(?:Canada|United States(?: of America)?)\b"
)
TITLE_CITY_REGION_SUFFIX_PATTERN = re.compile(
    r"\b([A-Z][A-Za-z .'-]{1,80}),\s*"
    r"(?:AB|BC|MB|NB|NL|NS|NT|NU|ON|PE|QC|SK|YT|CA|NY|WA|TX|IL|FL|"
    r"California|New York|Washington|Texas|Illinois|Florida),?\s*$"
)

@dataclass(frozen=True)
class TitleCandidate:
    text: str
    source: str
    score: int


def assess_role_page(
    page: RenderedPageState,
    *,
    title_hints: tuple[str | None, ...] = (),
) -> RolePageAssessment:
    structured_posting = _extract_structured_job_posting(page)
    soup = BeautifulSoup(page.html, "lxml")
    if structured_posting is not None:
        title, title_source = _select_role_title(
            page,
            soup,
            structured_title=_first_string(
                structured_posting.get("title"), structured_posting.get("name")
            ),
            title_hints=title_hints,
        )
        description = extract_job_description(
            soup,
            structured_description=_first_string(structured_posting.get("description")),
            fallback_text=_extract_main_text(page),
        )
        return RolePageAssessment(
            is_role=True,
            is_closed=_is_closed_page(page, description),
            confidence=0.95,
            title=title or page.title,
            location=parse_job_location(
                _extract_job_location(structured_posting),
                context_text=_location_context(page, description),
            ),
            description=description,
            posting_id=_extract_posting_id(structured_posting, page),
            extraction_method="jobposting_structured_data",
            reasons=[
                "schema.org JobPosting structured data",
                *(
                    [f"title: {title_source}"]
                    if title_source != "schema.org title"
                    else []
                ),
            ],
        )

    parsed = urlparse(page.final_url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    title, title_source = _select_role_title(page, soup, title_hints=title_hints)
    raw_text_parts = (page.visible_text, _extract_main_text(page), soup.get_text(" ", strip=True))
    raw_page_text = _clean_text(
        " ".join(
            part
            for part in raw_text_parts
            if part
        )
    )
    description = extract_job_description(
        soup,
        fallback_text=raw_page_text,
    )
    visible_text = _clean_text(" ".join(part for part in (raw_page_text, description) if part))
    is_closed = _is_closed_page(page, visible_text)

    if description is None and _is_transient_error_shell(visible_text):
        return RolePageAssessment(
            is_role=False,
            is_closed=False,
            confidence=0.82,
            title=title,
            description=None,
            posting_id=_extract_posting_id({}, page),
            extraction_method="html_heuristic",
            rejection_reason="page rendered a transient error shell",
            reasons=["transient page error", f"title: {title_source}"],
        )

    if _is_ats_role_page(domain, path, visible_text):
        return RolePageAssessment(
            is_role=True,
            is_closed=is_closed,
            confidence=0.82 if not is_closed else 0.72,
            title=title,
            location=parse_job_location(
                _extract_dom_location(soup, visible_text),
                context_text=visible_text,
            ),
            description=description,
            posting_id=_extract_posting_id({}, page),
            extraction_method="ats_heuristic",
            reasons=[
                "known ATS/job-board URL",
                f"title: {title_source}",
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
            reasons=["listing/search page signals", f"title: {title_source}"],
        )

    role_text_matches = _matching_terms(visible_text, ROLE_TEXT_TERMS)
    if title and role_text_matches:
        return RolePageAssessment(
            is_role=True,
            is_closed=is_closed,
            confidence=0.66 if not is_closed else 0.58,
            title=title,
            location=parse_job_location(
                _extract_dom_location(soup, visible_text),
                context_text=visible_text,
            ),
            description=description,
            posting_id=_extract_posting_id({}, page),
            extraction_method="html_heuristic",
            reasons=["job-like page title", f"title: {title_source}", *role_text_matches[:3]],
        )

    return RolePageAssessment(
        is_role=False,
        is_closed=is_closed,
        confidence=0.35,
        title=title,
        description=description,
        extraction_method="html_heuristic",
        rejection_reason="deterministic evidence is weak; LLM fallback recommended",
        reasons=["no structured JobPosting and weak page signals", f"title: {title_source}"],
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


def _is_transient_error_shell(text: str | None) -> bool:
    if not text:
        return False
    return bool(
        re.search(
            r"\b(?:an error has occurred|website encountered an unexpected error|"
            r"please try again later)\b",
            text,
            re.I,
        )
    )


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


def _location_context(page: RenderedPageState, description: str | None) -> str | None:
    return _clean_text(" ".join(part for part in (page.visible_text, description) if part))


def _select_role_title(
    page: RenderedPageState,
    soup: BeautifulSoup,
    *,
    structured_title: str | None = None,
    title_hints: tuple[str | None, ...] = (),
) -> tuple[str | None, str]:
    candidates: list[TitleCandidate] = []
    _add_title_candidate(candidates, structured_title, "schema.org title", 100)
    for hint in title_hints:
        _add_title_candidate(candidates, hint, "selected link text", 88)
    for text, source, score in _extract_dom_title_candidates(soup):
        _add_title_candidate(candidates, text, source, score)
    for text in _page_title_candidates(page.title):
        _add_title_candidate(candidates, text, "browser title", 45)
    _add_title_candidate(candidates, _title_from_url_slug(page.final_url), "URL slug", 62)

    best: TitleCandidate | None = None
    for candidate in candidates:
        score = _score_title_candidate(candidate)
        if score < 25:
            continue
        scored = TitleCandidate(text=candidate.text, source=candidate.source, score=score)
        if best is None or scored.score > best.score:
            best = scored

    if best is None:
        fallback = _clean_text(page.title)
        return fallback, "browser title" if fallback else "none"
    return best.text, best.source


def _add_title_candidate(
    candidates: list[TitleCandidate],
    text: str | None,
    source: str,
    score: int,
) -> None:
    cleaned = _clean_title(text)
    if cleaned and cleaned not in {candidate.text for candidate in candidates}:
        candidates.append(TitleCandidate(text=cleaned, source=source, score=score))


def _extract_dom_title_candidates(soup: BeautifulSoup) -> list[tuple[str | None, str, int]]:
    selectors = (
        ("[data-testid*=job][data-testid*=title]", "job title selector", 82),
        ("[class*=job-title]", "job title selector", 82),
        ("[class*=position-title]", "position title selector", 82),
        ("[class*=posting-title]", "posting title selector", 82),
        ("[class*=jobTitle]", "job title selector", 82),
        ("meta[property='og:title']", "Open Graph title", 58),
        ("meta[name='twitter:title']", "Twitter title", 56),
        ("h1", "h1", 64),
    )
    candidates: list[tuple[str | None, str, int]] = []
    for selector, source, score in selectors:
        element = soup.select_one(selector)
        if element is not None:
            content = element.get("content")
            text = (
                _clean_text(content if isinstance(content, str) else None)
                if element.name == "meta"
                else _clean_text(element.get_text(" ", strip=True))
            )
            candidates.append((text, source, score))
    return candidates


def _page_title_candidates(title: str | None) -> list[str]:
    cleaned = _clean_title(title)
    if not cleaned:
        return []
    candidates = [cleaned]
    candidates.extend(
        part
        for part in (_clean_title(part) for part in TITLE_SEPARATOR_PATTERN.split(cleaned))
        if part
    )
    return candidates


def _score_title_candidate(candidate: TitleCandidate) -> int:
    lowered = candidate.text.lower()
    score = candidate.score
    if _matching_terms(lowered, ROLE_TITLE_TERMS):
        score += 24
    if _matching_terms(lowered, TITLE_NOISE_TERMS):
        score -= 40
    if lowered in GENERIC_LISTING_TERMS:
        score -= 55
    if len(candidate.text) > 100:
        score -= 20
    if len(candidate.text.split()) > 14:
        score -= 15
    if not re.search(r"[A-Za-z]", candidate.text):
        score -= 40
    return score


def _title_from_url_slug(url: str) -> str | None:
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]
    for raw_part in reversed(path_parts):
        part = re.sub(r"\.(?:html?|php|aspx?)$", "", raw_part, flags=re.I)
        part = re.sub(r"^\d{8,}[-_]", "", part)
        part = re.sub(r"[-_]\d{5,}$", "", part).strip("-_/ ")
        if not part or part.lower() in {"apply", "details", "job", "jobs", "search"}:
            continue
        words = [word for word in re.split(r"(?:[-_+]|%20)+", part) if word]
        if len(words) < 2:
            continue
        return _clean_title(_title_case_slug_words(words))
    return None


def _title_case_slug_words(words: list[str]) -> str:
    acronyms = {
        "ai": "AI",
        "api": "API",
        "bs": "BS",
        "ios": "iOS",
        "ml": "ML",
        "ms": "MS",
        "ui": "UI",
        "ux": "UX",
    }
    return " ".join(acronyms.get(word.lower(), word.capitalize()) for word in words)


def _clean_title(text: str | None) -> str | None:
    cleaned = _clean_text(text)
    if cleaned is None:
        return None
    cleaned = re.sub(r"^\s*learn\s+more\s+about\s+", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*\(\s*(?:m/f/d|f/m/d|m/w/d)\s*\)\s*$", "", cleaned, flags=re.I)
    cleaned = TITLE_ACTION_SUFFIX_PATTERN.sub("", cleaned)
    cleaned = TITLE_POSTED_SUFFIX_PATTERN.sub("", cleaned)
    cleaned = _strip_title_listing_metadata(cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -|–—•·")
    return cleaned or None


def _strip_title_listing_metadata(title: str) -> str:
    without_explicit_location = _strip_explicit_title_location(title)
    if without_explicit_location != title:
        return without_explicit_location

    if " - " in title:
        prefix, suffix = title.rsplit(" - ", 1)
        prefix_words = prefix.split()
        if (
            len(prefix_words) >= 3
            and TITLE_LOCATION_PATTERN.search(suffix)
            and not _matching_terms(suffix, ROLE_TITLE_TERMS)
        ):
            if prefix_words[-1].lower() in TITLE_DEPARTMENT_SUFFIXES:
                return " ".join(prefix_words[:-1]).strip()
            return prefix

    words = title.split()
    for index in range(len(words) - 1, 1, -1):
        suffix = " ".join(words[index:])
        suffix_has_location = TITLE_LOCATION_PATTERN.search(suffix)
        suffix_has_season = TITLE_SEASON_PATTERN.search(suffix)
        if suffix_has_location or suffix_has_season:
            candidate = " ".join(words[:index]).strip(" -|–—•·")
            if (
                _matching_terms(candidate, ROLE_TITLE_TERMS)
                and (suffix_has_location or TITLE_LOCATION_PATTERN.search(candidate))
            ):
                return _strip_title_listing_metadata(candidate)
    return title


def _strip_explicit_title_location(title: str) -> str:
    for pattern in (TITLE_CITY_REGION_COUNTRY_PATTERN, TITLE_CITY_REGION_SUFFIX_PATTERN):
        stripped = _strip_title_location_match(title, pattern)
        if stripped != title:
            return stripped
    return title


def _strip_title_location_match(title: str, pattern: re.Pattern[str]) -> str:
    for match in pattern.finditer(title):
        city = _strip_title_location_prefix(match.group(1))
        if not city:
            continue
        city_index = title.lower().rfind(city.lower(), 0, match.end())
        if city_index == -1:
            continue
        candidate = title[:city_index].strip(" -|:;,")
        candidate = _strip_trailing_title_department(candidate)
        if _matching_terms(candidate, ROLE_TITLE_TERMS):
            return candidate
    return title


def _strip_title_location_prefix(text: str) -> str | None:
    cleaned = _clean_text(text)
    if not cleaned:
        return None
    cleaned = re.sub(
        r"^.*\b(?:early\s+career|interns?|internships?|new\s+grad(?:uate)?|student)\s+",
        "",
        cleaned,
        flags=re.I,
    )
    return cleaned.strip(" -|:;,") or None


def _strip_trailing_title_department(title: str) -> str:
    words = title.split()
    while words and words[-1].lower().strip(" -|:;,") in TITLE_DEPARTMENT_SUFFIXES:
        words.pop()
    return " ".join(words).strip(" -|:;,")


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
            if text and len(text) <= 180:
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
            _stringify_location(address.get("addressCountry"))
            or address.get("addressCountry"),
        )
        return _clean_text(", ".join(str(part) for part in parts if part))
    if location.get("@type") == "Country" or location.get("type") == "Country":
        return _first_string(location.get("name"))
    return _first_string(location.get("name"), location.get("address"))


def _extract_posting_id(posting: dict[str, Any], page: RenderedPageState) -> str | None:
    identifier = posting.get("identifier")
    if isinstance(identifier, dict):
        posting_id = _first_string(identifier.get("value"), identifier.get("name"))
        if posting_id:
            return posting_id
    if isinstance(identifier, str):
        return _clean_text(identifier)
    url_match = POSTING_ID_URL_PATTERN.search(page.final_url)
    if url_match:
        return url_match.group(1)
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
