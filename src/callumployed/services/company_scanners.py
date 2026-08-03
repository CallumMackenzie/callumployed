from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from typing import Protocol

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
    ScoredLinkCandidate,
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
            self._persist_result(company, career_page, options.scan_run_id, result, assessments)
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

    def _persist_result(
        self,
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
                        assessment_confidence=1.0,
                        assessment_location=role.location,
                        assessment_description=role.description,
                        assessment_posting_id=role.posting_id,
                        assessment_extraction_method="html_heuristic",
                        assessment_reasons=list(assessment["reasons"]),
                        status=RoleDiscoveryStatus.SUCCEEDED,
                    ),
                )


def scanner_for(company: Company, career_page: CompanyCareerPage) -> CompanyScanner | None:
    for scanner in (ByteDanceApiScanner(),):
        if scanner.supports(company, career_page):
            return scanner
    return None


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
