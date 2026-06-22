import re
from urllib.parse import ParseResult

from bs4 import BeautifulSoup, Tag

from callumployed.webscraping.errors import ExtractionError
from callumployed.webscraping.models import LinkCandidate, RenderedPageState

MAX_TEXT_LENGTH = 180
MAX_SURROUNDING_TEXT_LENGTH = 240
ABSOLUTE_URL_PATTERN = re.compile(r"https?://[^\s<>'\"]+", re.IGNORECASE)
TRAILING_URL_PUNCTUATION = ".,;:)]}"


def extract_link_candidates(page: RenderedPageState) -> list[LinkCandidate]:
    try:
        soup = BeautifulSoup(page.html, "lxml")
    except Exception as exc:  # pragma: no cover - BeautifulSoup rarely raises predictably
        raise ExtractionError(f"Could not parse HTML from {page.final_url}") from exc

    candidates: list[LinkCandidate] = []
    for element in soup.find_all(["a", "button"]):
        if not isinstance(element, Tag):
            continue

        href = _candidate_href(element)
        if href is None:
            continue

        normalized_url = _normalize_url(href, page.final_url)
        if normalized_url is None:
            continue

        text = _clean_text(element.get_text(" ", strip=True))
        aria_label = _clean_text(_attr_string(element.get("aria-label")))
        title = _clean_text(_attr_string(element.get("title")))
        css_id = _clean_text(_attr_string(element.get("id")))
        css_classes = tuple(
            item for item in element.get("class", []) if isinstance(item, str) and item.strip()
        )
        surrounding_text = _surrounding_text(element)

        candidates.append(
            LinkCandidate(
                url=normalized_url,
                source_url=page.final_url,
                text=text or aria_label or title,
                tag=element.name,  # type: ignore[arg-type]
                css_id=css_id,
                css_classes=css_classes,
                aria_label=aria_label,
                title=title,
                surrounding_text=surrounding_text,
            )
        )

    return candidates


def _candidate_href(element: Tag) -> str | None:
    if element.name == "a":
        return _attr_string(element.get("href"))

    for attr in ("data-href", "data-url", "formaction"):
        value = _attr_string(element.get(attr))
        if value:
            return value
    return None


def _normalize_url(href: str, base_url: str) -> str | None:
    from urllib.parse import urldefrag, urljoin, urlparse, urlunparse

    href = _extract_url_like_href(href)
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None

    normalized, _fragment = urldefrag(urljoin(base_url, href))
    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    parsed = _fix_known_relative_urljoin_artifacts(parsed)
    normalized = urlunparse(parsed)
    return normalized


def _fix_known_relative_urljoin_artifacts(parsed: ParseResult) -> ParseResult:
    if parsed.netloc == "www.google.com":
        parsed = parsed._replace(
            path=parsed.path.replace(
                "/about/careers/applications/jobs/jobs/results/",
                "/about/careers/applications/jobs/results/",
            )
        )
    return parsed


def _extract_url_like_href(href: str) -> str:
    href = href.strip()
    absolute_match = ABSOLUTE_URL_PATTERN.search(href)
    if absolute_match is not None:
        return absolute_match.group(0).rstrip(TRAILING_URL_PUNCTUATION)

    if href.startswith(("/", "./", "../")):
        return href.split()[0].rstrip(TRAILING_URL_PUNCTUATION)

    return href


def _attr_string(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _clean_text(value: str | None, *, max_length: int = MAX_TEXT_LENGTH) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.split())
    if not cleaned:
        return None
    return cleaned[:max_length]


def _surrounding_text(element: Tag) -> str | None:
    parent = element.parent
    if not isinstance(parent, Tag):
        return None
    return _clean_text(parent.get_text(" ", strip=True), max_length=MAX_SURROUNDING_TEXT_LENGTH)
