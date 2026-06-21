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
)
MIN_DISCOVERY_CONFIDENCE = 0.35


async def classify_candidates(
    candidates: list[LinkCandidate],
    page: RenderedPageState,
    *,
    agent_classifier: AgentCandidateClassifier | None = None,
) -> list[DiscoveredJobLink]:
    prepared_candidates = prepare_candidates(candidates)
    scored_candidates = score_candidates(prepared_candidates)
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


def score_candidates(candidates: list[LinkCandidate]) -> list[ScoredLinkCandidate]:
    scored = [_score_candidate(candidate) for candidate in candidates]
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


def _score_candidate(candidate: LinkCandidate) -> ScoredLinkCandidate:
    score = 0.0
    reasons: list[str] = []
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

    if any(domain == board or domain.endswith(f".{board}") for board in JOB_BOARD_DOMAINS):
        score += 0.45
        reasons.append("known job board domain")

    if any(pattern in path for pattern in URL_PATTERNS):
        score += 0.25
        reasons.append("job-like URL path")

    if any(pattern in path for pattern in GENERIC_NAV_PATH_PATTERNS):
        score -= 0.3
        reasons.append("generic careers navigation path")

    link_text = " ".join(
        part
        for part in (candidate.text, candidate.aria_label, candidate.title)
        if part
    ).lower()
    if link_text in GENERIC_CAREERS_TEXT:
        score -= 0.25
        reasons.append("generic careers navigation text")

    matching_terms = [term for term in POSITIVE_TERMS if term in haystack]
    if matching_terms:
        score += min(0.25, 0.08 * len(matching_terms))
        reasons.append(f"job-like text: {', '.join(matching_terms[:3])}")

    matching_negative_terms = [term for term in NEGATIVE_TERMS if term in haystack]
    if matching_negative_terms:
        score -= min(0.45, 0.15 * len(matching_negative_terms))
        reasons.append(f"rejected text: {', '.join(matching_negative_terms[:3])}")

    confidence = max(0.0, min(score, 1.0))
    return ScoredLinkCandidate(**candidate.model_dump(), confidence=confidence, reasons=reasons)
