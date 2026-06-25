import re
from collections.abc import Awaitable, Callable
from urllib.parse import urlparse

from callumployed.webscraping.models import (
    DiscoveredJobLink,
    LinkCandidate,
    RenderedPageState,
    ScoredLinkCandidate,
)

AgentCandidateClassifier = Callable[
    [list[ScoredLinkCandidate], RenderedPageState],
    Awaitable[list[DiscoveredJobLink]],
]
ScoreRuleResult = tuple[float, str]

JOB_BOARD_DOMAINS = (
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
POSITIVE_TERMS = (
    "apply",
    "career",
    "engineering",
    "intern",
    "internship",
    "job",
    "opening",
    "position",
    "role",
    "software",
)
JOB_DETAIL_HREF_PATTERNS = (
    "/careers/search/job/",
    "/details/",
    "/job",
    "/jobs",
    "/positions",
)
URL_PATTERNS = (
    "/apply",
    *JOB_DETAIL_HREF_PATTERNS,
    "/opening",
    "/requisition",
)
NEGATIVE_TERMS = (
    "about",
    "blog",
    "contact",
    "cookie",
    "facebook",
    "instagram",
    "legal",
    "login",
    "privacy",
    "signin",
    "terms",
    "twitter",
)
GENERIC_CAREERS_TEXT = {
    "careers",
    "careers at apple",
    "jobs at apple",
}
GENERIC_NAV_PATH_PATTERNS = (
    "/careers/choose-country-region",
    "/careers/ca",
    "/careers/us",
    "/careers/index",
    "/internships/",
)
JOB_ID_PATTERN = re.compile(r"\d{5,}")
MIN_DISCOVERY_CONFIDENCE = 0.35


async def classify_candidates(
    candidates: list[LinkCandidate],
    page: RenderedPageState,
    *,
    agent_classifier: AgentCandidateClassifier | None = None,
    existing_posting_urls: set[str] | None = None,
) -> list[DiscoveredJobLink]:
    prepared_candidates = prepare_candidates(candidates)
    scored_candidates = score_candidates(
        prepared_candidates,
        existing_posting_urls=existing_posting_urls,
    )
    heuristic_links = select_heuristic_links(scored_candidates)
    agent_links: list[DiscoveredJobLink] = []
    if agent_classifier is not None:
        agent_links = await agent_classifier(
            select_ambiguous_candidates(scored_candidates),
            page,
        )

    return merge_discovered_links(heuristic_links, agent_links)


def prepare_candidates(candidates: list[LinkCandidate]) -> list[LinkCandidate]:
    candidates_by_url: dict[str, LinkCandidate] = {}
    for candidate in candidates:
        existing = candidates_by_url.get(candidate.url)
        if existing is None or candidate_quality(candidate) > candidate_quality(existing):
            candidates_by_url[candidate.url] = candidate
    return list(candidates_by_url.values())


def score_candidates(
    candidates: list[LinkCandidate],
    *,
    existing_posting_urls: set[str] | None = None,
    rejected_role_urls: set[str] | None = None,
) -> list[ScoredLinkCandidate]:
    known_posting_urls = existing_posting_urls or set()
    known_rejected_urls = rejected_role_urls or set()
    scored = [
        _score_candidate(
            candidate,
            existing_posting_urls=known_posting_urls,
            rejected_role_urls=known_rejected_urls,
        )
        for candidate in candidates
    ]
    return sorted(scored, key=lambda candidate: candidate.confidence, reverse=True)


def select_heuristic_links(
    candidates: list[ScoredLinkCandidate],
    *,
    min_confidence: float = MIN_DISCOVERY_CONFIDENCE,
) -> list[DiscoveredJobLink]:
    links: list[DiscoveredJobLink] = []
    for candidate in candidates:
        if candidate.confidence < min_confidence:
            continue
        links.append(
            DiscoveredJobLink(
                url=candidate.url,
                source_url=candidate.source_url,
                text=candidate.text,
                confidence=candidate.confidence,
                discovery_method="heuristic",
                reasons=candidate.reasons,
            )
        )
    return links


def select_ambiguous_candidates(
    candidates: list[ScoredLinkCandidate],
) -> list[ScoredLinkCandidate]:
    return [
        candidate
        for candidate in candidates
        if 0.0 < candidate.confidence < MIN_DISCOVERY_CONFIDENCE
    ]


def merge_discovered_links(
    heuristic_links: list[DiscoveredJobLink],
    agent_links: list[DiscoveredJobLink],
) -> list[DiscoveredJobLink]:
    links_by_url = {link.url: link for link in heuristic_links}
    for agent_link in agent_links:
        existing = links_by_url.get(agent_link.url)
        if existing is None:
            links_by_url[agent_link.url] = agent_link
            continue
        links_by_url[agent_link.url] = existing.model_copy(
            update={
                "confidence": max(existing.confidence, agent_link.confidence),
                "discovery_method": "heuristic+agent",
                "reasons": [*existing.reasons, *agent_link.reasons],
            }
        )
    return sorted(links_by_url.values(), key=lambda link: link.confidence, reverse=True)


def candidate_quality(candidate: LinkCandidate) -> int:
    return sum(
        bool(value)
        for value in (
            candidate.text,
            candidate.css_id,
            candidate.css_classes,
            candidate.aria_label,
            candidate.title,
            candidate.surrounding_text,
        )
    )


def _score_candidate(
    candidate: LinkCandidate,
    *,
    existing_posting_urls: set[str],
    rejected_role_urls: set[str],
) -> ScoredLinkCandidate:
    parsed = urlparse(candidate.url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    haystack = " ".join(
        part
        for part in (
            candidate.text,
            candidate.css_id,
            " ".join(candidate.css_classes),
            candidate.aria_label,
            candidate.title,
            candidate.surrounding_text,
            candidate.url,
        )
        if part
    ).lower()
    link_text = " ".join(
        part
        for part in (candidate.text, candidate.aria_label, candidate.title)
        if part
    ).lower()

    rule_results = [
        result
        for result in (
            _score_known_job_board_domain(domain),
            _score_job_like_url_path(path),
            _score_generic_careers_navigation_path(path),
            _score_closed_role(path, haystack),
            _score_numeric_job_id(path),
            _score_generic_careers_navigation_text(link_text),
            _score_job_like_text(haystack),
            _score_rejected_text(haystack),
            _score_existing_posting(candidate.url, existing_posting_urls),
            _score_rejected_role(candidate.url, rejected_role_urls),
        )
        if result is not None
    ]

    score = sum(delta for delta, _reason in rule_results)
    reasons = [reason for _delta, reason in rule_results]

    confidence = max(0.0, min(score, 1.0))
    return ScoredLinkCandidate(**candidate.model_dump(), confidence=confidence, reasons=reasons)


def _score_known_job_board_domain(domain: str) -> ScoreRuleResult | None:
    if any(domain == board or domain.endswith(f".{board}") for board in JOB_BOARD_DOMAINS):
        return 0.45, "known job board domain"
    return None


def _score_job_like_url_path(path: str) -> ScoreRuleResult | None:
    if any(pattern in path for pattern in URL_PATTERNS):
        return 0.25, "job-like URL path"
    return None


def _score_generic_careers_navigation_path(path: str) -> ScoreRuleResult | None:
    if any(pattern in path for pattern in GENERIC_NAV_PATH_PATTERNS):
        return -0.3, "generic careers navigation path"
    return None


def _score_closed_role(path: str, haystack: str) -> ScoreRuleResult | None:
    if "closed" in path or "closed" in haystack:
        return -0.5, "closed role"
    return None


def _score_numeric_job_id(path: str) -> ScoreRuleResult | None:
    if JOB_ID_PATTERN.search(path):
        return 0.18, "numeric job id"
    return None


def _score_generic_careers_navigation_text(link_text: str) -> ScoreRuleResult | None:
    if link_text in GENERIC_CAREERS_TEXT:
        return -0.25, "generic careers navigation text"
    return None


def _score_job_like_text(haystack: str) -> ScoreRuleResult | None:
    matching_terms = [term for term in POSITIVE_TERMS if term in haystack]
    if matching_terms:
        return min(0.25, 0.08 * len(matching_terms)), (
            f"job-like text: {', '.join(matching_terms[:3])}"
        )
    return None


def _score_rejected_text(haystack: str) -> ScoreRuleResult | None:
    matching_negative_terms = [term for term in NEGATIVE_TERMS if term in haystack]
    if matching_negative_terms:
        return -min(0.45, 0.15 * len(matching_negative_terms)), (
            f"rejected text: {', '.join(matching_negative_terms[:3])}"
        )
    return None


def _score_existing_posting(url: str, existing_posting_urls: set[str]) -> ScoreRuleResult | None:
    if url in existing_posting_urls:
        return -999.0, "already in database"
    return None


def _score_rejected_role(url: str, rejected_role_urls: set[str]) -> ScoreRuleResult | None:
    if url in rejected_role_urls:
        return -999.0, "already rejected as non-role"
    return None
