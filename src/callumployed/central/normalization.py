from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_TRACKING_PARAMETERS = {
    "ref",
    "source",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
}
_SHARED_ATS_HOSTS = {
    "boards.greenhouse.io",
    "job-boards.greenhouse.io",
    "jobs.ashbyhq.com",
    "jobs.lever.co",
}


def canonical_company_domain(raw_url: str) -> str | None:
    host = _hostname(raw_url)
    return None if not host or host in _SHARED_ATS_HOSTS else host


def ats_slug(raw_url: str) -> str | None:
    parsed = urlsplit(raw_url)
    host = (parsed.hostname or "").lower().removeprefix("www.")
    segments = [segment.lower() for segment in parsed.path.split("/") if segment]
    if host in {"boards.greenhouse.io", "job-boards.greenhouse.io"} and segments:
        return f"greenhouse:{segments[0]}"
    if host == "jobs.ashbyhq.com" and segments:
        return f"ashby:{segments[0]}"
    if host.endswith(".ashbyhq.com") and host != "jobs.ashbyhq.com":
        return f"ashby:{host.split('.')[0]}"
    if host == "jobs.lever.co" and segments:
        return f"lever:{segments[0]}"
    if host.endswith(".workdayjobs.com"):
        return f"workday:{host.split('.')[0]}"
    return None


def canonical_role_url(raw_url: str) -> str:
    parsed = urlsplit(raw_url)
    retained = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() not in _TRACKING_PARAMETERS
    ]
    retained.sort(key=lambda item: (item[0].lower(), item[0], item[1]))
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, urlencode(retained), ""))


def role_identity(raw_url: str, posting_id: str | None = None) -> str | None:
    parsed = urlsplit(raw_url)
    host = (parsed.hostname or "").lower().removeprefix("www.")
    segments = [segment for segment in parsed.path.split("/") if segment]
    board = ats_slug(raw_url)

    if host in {"boards.greenhouse.io", "job-boards.greenhouse.io"}:
        lowered = [segment.lower() for segment in segments]
        jobs_index = lowered.index("jobs") if "jobs" in lowered else -1
        url_posting_id = segments[jobs_index + 1] if jobs_index + 1 < len(segments) else None
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        greenhouse_id = url_posting_id or query.get("gh_jid") or posting_id
        return f"{board}:job:{greenhouse_id}" if board and greenhouse_id else None

    if host == "jobs.ashbyhq.com" or host.endswith(".ashbyhq.com"):
        posting_segment = (
            segments[1]
            if host == "jobs.ashbyhq.com" and len(segments) > 1
            else segments[0]
            if host != "jobs.ashbyhq.com" and segments
            else None
        )
        ashby_id = posting_segment or posting_id
        return f"{board}:job:{ashby_id.lower()}" if board and ashby_id else None

    if host == "jobs.lever.co":
        lever_id = segments[1] if len(segments) > 1 else posting_id
        return f"{board}:job:{lever_id.lower()}" if board and lever_id else None

    if posting_id and host:
        return f"posting:{host}:{posting_id.lower()}"

    normalized_path = parsed.path.rstrip("/").lower()
    if not normalized_path or normalized_path in {"/career", "/careers", "/job", "/jobs"}:
        return None
    return f"url:{canonical_role_url(raw_url)}"


def _hostname(raw_url: str) -> str | None:
    try:
        return (urlsplit(raw_url).hostname or "").lower().removeprefix("www.") or None
    except ValueError:
        return None
