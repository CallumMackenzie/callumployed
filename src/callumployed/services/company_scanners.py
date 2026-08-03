from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    Role,
    RoleDiscoveryAttempt,
    RoleDiscoveryStatus,
)
from callumployed.data.repositories import (
    add_role,
    add_role_discovery_attempt,
    add_scan_candidates,
    add_scan_page,
    get_role_by_company_url,
)
from callumployed.services.scan_filters import (
    has_intern_keyword,
    has_software_keyword,
    is_graduate_degree_role,
    is_hardware_only_role,
    location_matches_filter,
)
from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    RenderedPageState,
    RolePageAssessment,
    ScoredLinkCandidate,
)
from callumployed.webscraping.role_page_classifier import assess_role_page

ASHBY_JOB_URL_PATTERN = re.compile(r"https://jobs\.ashbyhq\.com/([a-zA-Z0-9_-]+)(?:/|[\"?#])")
ASHBY_JOB_BOARD_QUERY = """
query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
  jobBoardWithTeams(organizationHostedJobsPageName: $organizationHostedJobsPageName) {
    jobPostings {
      id
      title
      employmentType
      locationName
    }
  }
}
"""
GREENHOUSE_JOB_BOARD_PATTERN = re.compile(
    r"https://(?:job-boards|boards)\.greenhouse\.io/([a-zA-Z0-9_-]+)(?:/|[\"?#])"
)
GREENHOUSE_API_PATTERN = re.compile(
    r"https://(?:boards-api|api)\.greenhouse\.io/v1/boards/([a-zA-Z0-9_-]+)/jobs"
)


@dataclass(frozen=True)
class ScannerOptions:
    scan_run_id: int | None
    include_graduate_degree_roles: bool
    include_hardware_roles: bool
    require_software_keywords: bool
    internship_mode: bool
    location_filter: str
    existing_posting_urls: set[str]
    retry_rejected_roles: bool = False


class CompanyScanner(Protocol):
    def supports(self, company: Company, career_page: CompanyCareerPage) -> bool: ...

    async def scan(
        self,
        company: Company,
        career_page: CompanyCareerPage,
        options: ScannerOptions,
    ) -> CareersPageScanResult: ...


class ByteDanceApiScanner:
    api_url = "https://jobs.bytedance.com/api/v1/public/supplier/search/job/posts"
    headers = {
        "content-type": "application/json",
        "accept-language": "en-US",
        "website-path": "en",
        "x-tt-env": "boe_epam_api",
    }
    limit = 100

    def supports(self, company: Company, career_page: CompanyCareerPage) -> bool:
        haystack = " ".join(
            part
            for part in (company.name, company.canonical_domain, career_page.url)
            if part
        ).lower()
        return "bytedance" in haystack or "joinbytedance.com" in haystack

    async def scan(
        self,
        company: Company,
        career_page: CompanyCareerPage,
        options: ScannerOptions,
    ) -> CareersPageScanResult:
        posts = self._fetch_all_posts(career_page)
        candidates: list[ScoredLinkCandidate] = []
        links: list[DiscoveredJobLink] = []
        assessments: dict[str, dict[str, object]] = {}

        for post in posts:
            title = str(post.get("title") or "")
            description = _description_for(post)
            location = _location_for(post)
            url = _role_url(post)
            reasons = ["bytedance API", f"job code: {post.get('code') or post.get('id')}"]
            rejection_reason = _rejection_reason(
                title=title,
                description=description,
                location=location,
                url=url,
                options=options,
            )
            confidence = 0.0 if rejection_reason else 1.0
            candidate = ScoredLinkCandidate(
                url=url,
                source_url=career_page.url,
                text=title,
                confidence=confidence,
                reasons=[*reasons, *([rejection_reason] if rejection_reason else [])],
            )
            candidates.append(candidate)
            if rejection_reason:
                continue
            link = DiscoveredJobLink(
                url=url,
                source_url=career_page.url,
                text=title,
                confidence=1.0,
                discovery_method="heuristic",
                reasons=reasons,
            )
            links.append(link)
            assessments[url] = {
                "title": title,
                "location": location,
                "description": description,
                "posting_id": post.get("code") or post.get("id"),
                "confidence": 1.0,
                "extraction_method": "html_heuristic",
                "reasons": reasons,
            }

        result = CareersPageScanResult(
            source_url=career_page.url,
            final_url=career_page.url,
            title="ByteDance API",
            candidates=candidates,
            links=links,
            candidates_scanned=len(candidates),
            confidence=ExtractionConfidence.HIGH if links else ExtractionConfidence.LOW,
        )
        if options.scan_run_id is not None and company.id is not None:
            _persist_scan_result(company, career_page, options.scan_run_id, result, assessments)
        return result

    def _fetch_all_posts(self, career_page: CompanyCareerPage) -> list[dict[str, object]]:
        first = self._fetch_page(career_page, offset=0)
        total = int(first["data"]["count"])
        posts = list(first["data"]["job_post_list"])
        for offset in range(self.limit, total, self.limit):
            posts.extend(self._fetch_page(career_page, offset=offset)["data"]["job_post_list"])
        seen: set[str] = set()
        deduped = []
        for post in posts:
            post_id = str(post.get("id") or "")
            if not post_id or post_id in seen:
                continue
            seen.add(post_id)
            deduped.append(post)
        return deduped

    def _fetch_page(self, career_page: CompanyCareerPage, *, offset: int) -> dict[str, object]:
        payload = {
            **_payload_from_url(career_page.url),
            "limit": self.limit,
            "offset": offset,
        }
        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode(),
            headers=self.headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode())


@dataclass(frozen=True)
class AshbyJobBoardScanner:
    board_url: str | None = None

    @classmethod
    def from_career_page(
        cls,
        company: Company,
        career_page: CompanyCareerPage,
    ) -> AshbyJobBoardScanner | None:
        _ = company
        direct_board_url = _direct_ashby_board_url(career_page.url)
        if direct_board_url is not None:
            return cls(board_url=direct_board_url)
        detected_board_url = cls()._detect_board_url(career_page.url)
        if detected_board_url is not None:
            return cls(board_url=detected_board_url)
        return None

    def supports(self, company: Company, career_page: CompanyCareerPage) -> bool:
        return self.from_career_page(company, career_page) is not None

    async def scan(
        self,
        company: Company,
        career_page: CompanyCareerPage,
        options: ScannerOptions,
    ) -> CareersPageScanResult:
        board_url = self.board_url or _direct_ashby_board_url(career_page.url)
        if board_url is None:
            board_url = self._detect_board_url(career_page.url)
        if board_url is None:
            raise RuntimeError(f"No Ashby board detected for {career_page.url}")
        html = self._fetch_html(board_url)
        app_data = _extract_ashby_app_data(html)
        postings = _ashby_postings(app_data)
        if not postings:
            postings = self._fetch_graphql_postings(board_url)
        candidates: list[ScoredLinkCandidate] = []
        links: list[DiscoveredJobLink] = []
        assessments: dict[str, dict[str, object]] = {}

        for posting in postings:
            posting_id = _optional_string(posting.get("id"))
            title = _optional_string(posting.get("title")) or ""
            if not posting_id:
                continue
            url = _ashby_posting_url(board_url, posting_id)
            reasons = ["ashby embedded job board data", f"posting id: {posting_id}"]
            if options.internship_mode and not has_intern_keyword(
                " ".join([title, url, _optional_string(posting.get("employmentType")) or ""])
            ):
                candidates.append(
                    _candidate(
                        url=url,
                        source_url=career_page.url,
                        title=title,
                        confidence=0.0,
                        reasons=[*reasons, "intern keyword requirement filtered by app config"],
                    )
                )
                continue

            assessment = self._assess_posting(url, title)
            rejection_reason = (
                "closed role filtered by app config"
                if assessment.is_closed
                else _rejection_reason(
                    title=assessment.title or title,
                    description=assessment.description,
                    location=assessment.location,
                    url=url,
                    options=options,
                )
            )
            confidence = 0.0 if rejection_reason else assessment.confidence
            candidates.append(
                _candidate(
                    url=url,
                    source_url=career_page.url,
                    title=assessment.title or title,
                    confidence=confidence,
                    reasons=[
                        *reasons,
                        *assessment.reasons,
                        *([rejection_reason] if rejection_reason else []),
                    ],
                )
            )
            if rejection_reason:
                continue
            links.append(
                DiscoveredJobLink(
                    url=url,
                    source_url=career_page.url,
                    text=assessment.title or title,
                    confidence=confidence,
                    discovery_method="heuristic",
                    reasons=[*reasons, *assessment.reasons],
                )
            )
            assessments[url] = {
                "title": assessment.title or title,
                "location": assessment.location,
                "description": assessment.description,
                "posting_id": assessment.posting_id or posting_id,
                "confidence": assessment.confidence,
                "extraction_method": assessment.extraction_method,
                "reasons": [*reasons, *assessment.reasons],
            }

        result = CareersPageScanResult(
            source_url=career_page.url,
            final_url=career_page.url,
            title=_optional_string(_nested_get(app_data, "organization", "name")) or "Ashby API",
            candidates=candidates,
            links=links,
            candidates_scanned=len(candidates),
            confidence=ExtractionConfidence.HIGH if links else ExtractionConfidence.LOW,
        )
        if options.scan_run_id is not None and company.id is not None:
            _persist_scan_result(company, career_page, options.scan_run_id, result, assessments)
        return result

    def _fetch_html(self, url: str) -> str:
        request = urllib.request.Request(url, headers={"user-agent": "callumployed"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode()

    def _fetch_json(self, url: str, payload: dict[str, object]) -> dict[str, object]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"content-type": "application/json", "user-agent": "callumployed"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode())
        return data if isinstance(data, dict) else {}

    def _fetch_graphql_postings(self, board_url: str) -> list[dict[str, object]]:
        slug = _ashby_slug(urlparse(board_url).path)
        if slug is None:
            return []
        data = self._fetch_json(
            "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams",
            {
                "operationName": "ApiJobBoardWithTeams",
                "variables": {"organizationHostedJobsPageName": slug},
                "query": ASHBY_JOB_BOARD_QUERY,
            },
        )
        postings = _nested_get(data, "data", "jobBoardWithTeams", "jobPostings")
        if not isinstance(postings, list):
            return []
        return [posting for posting in postings if isinstance(posting, dict)]

    def _detect_board_url(self, url: str) -> str | None:
        try:
            html = self._fetch_html(url)
        except Exception:
            return None
        match = ASHBY_JOB_URL_PATTERN.search(html)
        if match is None:
            return None
        return f"https://jobs.ashbyhq.com/{match.group(1)}"

    def _assess_posting(self, url: str, title: str) -> RolePageAssessment:
        html = self._fetch_html(url)
        page = RenderedPageState(
            url=url,
            final_url=url,
            title=title,
            html=html,
            visible_text=None,
        )
        return assess_role_page(page, title_hints=(title,))


@dataclass(frozen=True)
class GreenhouseJobBoardScanner:
    board_token: str | None = None
    api_host: str = "boards-api.greenhouse.io"
    public_host: str = "job-boards.greenhouse.io"

    @classmethod
    def from_career_page(
        cls,
        company: Company,
        career_page: CompanyCareerPage,
    ) -> GreenhouseJobBoardScanner | None:
        _ = company
        direct_board = _direct_greenhouse_board(career_page.url)
        if direct_board is not None:
            return cls(**direct_board)
        detected_board = cls()._detect_board(career_page.url)
        if detected_board is not None:
            return cls(**detected_board)
        return None

    def supports(self, company: Company, career_page: CompanyCareerPage) -> bool:
        return self.from_career_page(company, career_page) is not None

    async def scan(
        self,
        company: Company,
        career_page: CompanyCareerPage,
        options: ScannerOptions,
    ) -> CareersPageScanResult:
        board = (
            {
                "board_token": self.board_token,
                "api_host": self.api_host,
                "public_host": self.public_host,
            }
            if self.board_token
            else _direct_greenhouse_board(career_page.url) or self._detect_board(career_page.url)
        )
        if board is None or not board.get("board_token"):
            raise RuntimeError(f"No Greenhouse board detected for {career_page.url}")

        jobs = self._fetch_jobs(str(board["board_token"]), str(board["api_host"]))
        candidates: list[ScoredLinkCandidate] = []
        links: list[DiscoveredJobLink] = []
        assessments: dict[str, dict[str, object]] = {}

        for job in jobs:
            posting_id = _optional_string(job.get("id")) or str(job.get("id") or "")
            title = _optional_string(job.get("title")) or ""
            url = _greenhouse_job_url(job, str(board["board_token"]), str(board["public_host"]))
            location = _greenhouse_location(job)
            description = _optional_string(job.get("content"))
            reasons = ["greenhouse job board API", f"job id: {posting_id}"]
            rejection_reason = _rejection_reason(
                title=title,
                description=description,
                location=location,
                url=url,
                options=options,
            )
            confidence = 0.0 if rejection_reason else 1.0
            candidates.append(
                _candidate(
                    url=url,
                    source_url=career_page.url,
                    title=title,
                    confidence=confidence,
                    reasons=[*reasons, *([rejection_reason] if rejection_reason else [])],
                )
            )
            if rejection_reason:
                continue
            links.append(
                DiscoveredJobLink(
                    url=url,
                    source_url=career_page.url,
                    text=title,
                    confidence=1.0,
                    discovery_method="heuristic",
                    reasons=reasons,
                )
            )
            assessments[url] = {
                "title": title,
                "location": location,
                "description": description,
                "posting_id": posting_id,
                "confidence": 1.0,
                "extraction_method": "ats_heuristic",
                "reasons": reasons,
            }

        result = CareersPageScanResult(
            source_url=career_page.url,
            final_url=career_page.url,
            title=f"Greenhouse: {board['board_token']}",
            candidates=candidates,
            links=links,
            candidates_scanned=len(candidates),
            confidence=ExtractionConfidence.HIGH if links else ExtractionConfidence.LOW,
        )
        if options.scan_run_id is not None and company.id is not None:
            _persist_scan_result(company, career_page, options.scan_run_id, result, assessments)
        return result

    def _fetch_html(self, url: str) -> str:
        request = urllib.request.Request(url, headers={"user-agent": "callumployed"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode()

    def _fetch_json(self, url: str) -> dict[str, object]:
        request = urllib.request.Request(url, headers={"user-agent": "callumployed"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode())
        return data if isinstance(data, dict) else {}

    def _fetch_jobs(self, board_token: str, api_host: str) -> list[dict[str, object]]:
        api_url = f"https://{api_host}/v1/boards/{board_token}/jobs?content=true"
        data = self._fetch_json(api_url)
        jobs = data.get("jobs")
        if isinstance(jobs, list):
            return [job for job in jobs if isinstance(job, dict)]
        return []

    def _detect_board(self, url: str) -> dict[str, str] | None:
        try:
            html = self._fetch_html(url)
        except Exception:
            return None
        api_match = GREENHOUSE_API_PATTERN.search(html)
        if api_match is not None:
            return {
                "board_token": api_match.group(1),
                "api_host": "api.greenhouse.io",
                "public_host": "boards.greenhouse.io",
            }
        board_match = GREENHOUSE_JOB_BOARD_PATTERN.search(html)
        if board_match is not None:
            return {
                "board_token": board_match.group(1),
                "api_host": "boards-api.greenhouse.io",
                "public_host": "job-boards.greenhouse.io",
            }
        return None


def scanner_for(company: Company, career_page: CompanyCareerPage) -> CompanyScanner | None:
    bytedance_scanner = ByteDanceApiScanner()
    if bytedance_scanner.supports(company, career_page):
        return bytedance_scanner
    ashby_scanner = AshbyJobBoardScanner.from_career_page(company, career_page)
    if ashby_scanner is not None:
        return ashby_scanner
    greenhouse_scanner = GreenhouseJobBoardScanner.from_career_page(company, career_page)
    if greenhouse_scanner is not None:
        return greenhouse_scanner
    return None


def _persist_scan_result(
    company: Company,
    career_page: CompanyCareerPage,
    scan_run_id: int,
    result: CareersPageScanResult,
    assessments: dict[str, dict[str, object]],
) -> None:
    if company.id is None:
        return
    with db.connect() as connection:
        scan_page = add_scan_page(
            connection,
            scan_run_id,
            result,
            company_career_page_id=career_page.id,
        )
        if scan_page.id is None:
            raise RuntimeError("created scan page did not include an id")
        stored_candidates = add_scan_candidates(
            connection,
            scan_page.id,
            result.candidates,
            result,
        )

    for candidate in stored_candidates:
        if not candidate.selected or candidate.id is None:
            continue
        assessment = assessments.get(candidate.url)
        if assessment is None:
            continue
        with db.connect() as connection:
            role = get_role_by_company_url(connection, company.id, candidate.url)
            if role is None:
                role = add_role(
                    connection,
                    Role(
                        company_id=company.id,
                        title=str(assessment["title"]),
                        role_url=candidate.url,
                        location=_optional_string(assessment["location"]),
                        description=_optional_string(assessment["description"]),
                        posting_id=_optional_string(assessment["posting_id"]),
                    ),
                )
            add_role_discovery_attempt(
                connection,
                RoleDiscoveryAttempt(
                    scan_run_id=scan_run_id,
                    scan_candidate_id=candidate.id,
                    company_id=company.id,
                    role_id=role.id,
                    url=candidate.url,
                    final_url=candidate.url,
                    title=role.title,
                    visible_text_excerpt=role.description,
                    assessment_is_role=True,
                    assessment_is_closed=False,
                    assessment_confidence=float(assessment["confidence"]),
                    assessment_location=role.location,
                    assessment_description=role.description,
                    assessment_posting_id=role.posting_id,
                    assessment_extraction_method=str(assessment["extraction_method"]),
                    assessment_reasons=list(assessment["reasons"]),
                    status=RoleDiscoveryStatus.SUCCEEDED,
                ),
            )


def _payload_from_url(url: str) -> dict[str, object]:
    from urllib.parse import parse_qs, urlparse

    query = parse_qs(urlparse(url).query)
    return {
        "recruitment_id_list": _split_query_list(query.get("recruitment_id_list", [""])[0]),
        "job_category_id_list": _split_query_list(query.get("job_category_id_list", [""])[0]),
        "subject_id_list": _split_query_list(query.get("subject_id_list", [""])[0]),
        "location_code_list": _split_query_list(query.get("location_code_list", [""])[0]),
        "keyword": query.get("keyword", [""])[0],
    }


def _split_query_list(value: str) -> list[str]:
    return [part for part in value.split(",") if part]


def _role_url(post: dict[str, object]) -> str:
    return f"https://joinbytedance.com/search/{post['id']}"


def _description_for(post: dict[str, object]) -> str | None:
    return "\n\n".join(
        part for part in (post.get("description"), post.get("requirement")) if isinstance(part, str)
    ) or None


def _location_for(post: dict[str, object]) -> str | None:
    parts: list[str] = []
    current = post.get("city_info")
    while isinstance(current, dict) and current:
        name = current.get("en_name") or current.get("i18n_name") or current.get("name")
        if isinstance(name, str):
            parts.append(name)
        current = current.get("parent")
    return ", ".join(parts) if parts else None


def _rejection_reason(
    *,
    title: str,
    description: str | None,
    location: str | None,
    url: str,
    options: ScannerOptions,
) -> str | None:
    if not options.include_graduate_degree_roles and is_graduate_degree_role(title, description):
        return "graduate-degree role filtered by app config"
    if not options.include_hardware_roles and is_hardware_only_role(title):
        return "hardware-only role filtered by app config"
    if options.require_software_keywords and not has_software_keyword(title, description):
        return "software keyword requirement filtered by app config"
    if not location_matches_filter(location, options.location_filter):
        return "location filtered by app config"
    if options.internship_mode and not has_intern_keyword(" ".join([title, url])):
        return "intern keyword requirement filtered by app config"
    return None


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _candidate(
    *,
    url: str,
    source_url: str,
    title: str | None,
    confidence: float,
    reasons: list[str],
) -> ScoredLinkCandidate:
    return ScoredLinkCandidate(
        url=url,
        source_url=source_url,
        text=title,
        confidence=confidence,
        reasons=reasons,
    )


def _extract_ashby_app_data(html: str) -> dict[str, object]:
    soup = BeautifulSoup(html, "lxml")
    decoder = json.JSONDecoder()
    marker = "window.__appData ="
    for script in soup.find_all("script"):
        text = script.string or script.get_text()
        marker_index = text.find(marker)
        if marker_index == -1:
            continue
        json_text = text[marker_index + len(marker) :].lstrip()
        data, _end = decoder.raw_decode(json_text)
        if isinstance(data, dict):
            return data
    return {}


def _ashby_postings(app_data: dict[str, object]) -> list[dict[str, object]]:
    posting = app_data.get("posting")
    if isinstance(posting, dict):
        return [posting]
    job_board = app_data.get("jobBoard")
    if not isinstance(job_board, dict):
        return []
    postings = job_board.get("jobPostings")
    if not isinstance(postings, list):
        return []
    return [posting for posting in postings if isinstance(posting, dict)]


def _ashby_posting_url(board_url: str, posting_id: str) -> str:
    parsed = urlparse(board_url)
    slug = _ashby_slug(parsed.path)
    return f"{parsed.scheme}://{parsed.netloc}/{slug}/{posting_id}"


def _direct_ashby_board_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc.lower() != "jobs.ashbyhq.com":
        return None
    slug = _ashby_slug(parsed.path)
    if slug is None:
        return None
    return f"{parsed.scheme}://{parsed.netloc}/{slug}"


def _ashby_slug(path: str) -> str | None:
    slug = path.strip("/").split("/", 1)[0]
    return slug or None


def _direct_greenhouse_board(url: str) -> dict[str, str] | None:
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    if hostname in {"api.greenhouse.io", "boards-api.greenhouse.io"}:
        path_parts = [part for part in parsed.path.split("/") if part]
        if len(path_parts) >= 4 and path_parts[:2] == ["v1", "boards"]:
            return {
                "board_token": path_parts[2],
                "api_host": hostname,
                "public_host": (
                    "boards.greenhouse.io"
                    if hostname == "api.greenhouse.io"
                    else "job-boards.greenhouse.io"
                ),
            }
    token = _greenhouse_token(parsed.path)
    if token is None:
        return None
    if hostname == "job-boards.greenhouse.io":
        return {
            "board_token": token,
            "api_host": "boards-api.greenhouse.io",
            "public_host": "job-boards.greenhouse.io",
        }
    if hostname == "boards.greenhouse.io":
        return {
            "board_token": token,
            "api_host": "api.greenhouse.io",
            "public_host": "boards.greenhouse.io",
        }
    return None


def _greenhouse_token(path: str) -> str | None:
    token = path.strip("/").split("/", 1)[0]
    if token in {"v1", "embed"}:
        return None
    return token or None


def _greenhouse_job_url(job: dict[str, object], board_token: str, public_host: str) -> str:
    absolute_url = _optional_string(job.get("absolute_url"))
    if absolute_url:
        return absolute_url
    job_id = str(job.get("id") or "")
    return f"https://{public_host}/{board_token}/jobs/{job_id}"


def _greenhouse_location(job: dict[str, object]) -> str | None:
    location = job.get("location")
    if isinstance(location, dict):
        name = location.get("name")
        if isinstance(name, str):
            return name
    location_name = job.get("location")
    return location_name if isinstance(location_name, str) else None


def _nested_get(data: dict[str, object], *keys: str) -> object:
    current: object = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current
