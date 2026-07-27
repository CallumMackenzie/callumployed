from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

LOCATION_LABEL_PATTERN = re.compile(
    r"^\s*(?:job\s*)?(?:location|locations|office|offices|work\s*location)\s*:?\s*",
    re.I,
)
LOCATION_SENTENCE_PATTERN = re.compile(
    r"\b(?:"
    r"locations?|offices?|work\s+location|based\s+(?:in|out\s+of)|"
    r"this\s+role\s+is\s+based\s+in"
    r")\s*:?\s*([^\n.]{2,140})",
    re.I,
)
REMOTE_PATTERN = re.compile(r"\bremote(?:ly)?\b", re.I)
HYBRID_PATTERN = re.compile(r"\bhybrid\b", re.I)
IN_OFFICE_PATTERN = re.compile(r"\bin[- ]?office\b", re.I)
MULTIPLE_PATTERN = re.compile(r"\b(?:multiple|various)\s+locations\b", re.I)
SEPARATOR_PATTERN = re.compile(r"\s*(?:;|\||/|\bor\b|\band\b)\s*", re.I)
TRAILING_NOISE_PATTERN = re.compile(
    r"\s+(?:"
    r"apply|compensation|department|employment\s+type|job\s+description|job\s+type|"
    r"qualifications|req\.?\s*id|requirements|responsibilities|team|"
    r"what\s+to\s+expect|what\s+you(?:'|’)ll\s+do"
    r")\b.*$",
    re.I,
)
SEARCH_FILTER_NOISE_PATTERN = re.compile(
    r"\b(?:state\s*[-:]\s*select|help\s+us\s+improve\s+our\s+website|"
    r"privacy\s*&\s*legal|skip\s+navigation|street\s+view\s+puzzles|"
    r"departments\s+open\s+roles\s+programs|who\s+we\s+are\s+trade\s+with\s+us|"
    r"diversity\s*&\s+inclusion\s+contact|north\s+america\s+new\s+york\s+city)\b",
    re.I,
)
LOCATION_CONTEXT_PATTERNS = (
    re.compile(
        r"\blocation\s+(.{2,140}?)(?=\s+(?:department|team|apply|share\b|$))",
        re.I,
    ),
    re.compile(
        r"\babout\s+this\s+role\s+[\ue000-\uf8ff]?\s*(.{2,140}?)(?=\s*[\ue000-\uf8ff]|\s+job\s+id\b|\s+#\s*view\b)",
        re.I,
    ),
)
GOOGLE_JOB_CARD_LOCATION_PATTERN = re.compile(
    r"\bplace\s+([\s\S]{2,260}?)(?=\s+bar_chart\b|\s+info_outline\b|\s+This\s+posting\b)",
    re.I,
)
COUNTRY_ALIASES = {
    "br": "Brazil",
    "brazil": "Brazil",
    "ca": "Canada",
    "canada": "Canada",
    "united states": "United States",
    "united states of america": "United States",
    "usa": "United States",
    "us": "United States",
    "u.s.": "United States",
    "u.s.a.": "United States",
}
REGION_ALIASES = {
    "bc": "BC",
    "british columbia": "BC",
    "on": "ON",
    "ontario": "ON",
    "qc": "QC",
    "quebec": "QC",
    "ca": "CA",
    "california": "CA",
    "ny": "NY",
    "wa": "WA",
    "washington": "WA",
}
CANADIAN_REGION_CODES = {
    "AB",
    "BC",
    "MB",
    "NB",
    "NL",
    "NS",
    "NT",
    "NU",
    "ON",
    "PE",
    "QC",
    "SK",
    "YT",
}
NON_LOCATION_PLACES = {
    "apply",
    "hybrid",
    "job",
    "location",
    "locations",
    "office",
    "offices",
    "remote",
    "role",
}


def parse_job_location(
    location_text: str | None,
    *,
    context_text: str | None = None,
) -> str | None:
    google_location = _google_job_card_location(location_text) or _google_job_card_location(
        context_text
    )
    if google_location:
        return google_location

    direct_location = _normalize_location_text(location_text)
    if direct_location:
        return direct_location
    if not context_text:
        return None

    candidate = _location_phrase_from_context(context_text)
    normalized_candidate = _normalize_location_text(candidate)
    if normalized_candidate:
        return normalized_candidate

    geograpy_location = _location_from_geograpy(context_text)
    if geograpy_location:
        return geograpy_location

    if REMOTE_PATTERN.search(context_text):
        return "Remote"
    return None


def _google_job_card_location(text: str | None) -> str | None:
    if not text:
        return None
    match = GOOGLE_JOB_CARD_LOCATION_PATTERN.search(text)
    if not match:
        return None
    raw_location = _clean_location_text(match.group(1))
    if not raw_location:
        return None

    has_more_locations = bool(re.search(r"\+\d+\s+more\b", raw_location, re.I))
    segments = [
        segment.strip(" -|:;,")
        for segment in SEPARATOR_PATTERN.split(raw_location)
        if segment.strip(" -|:;,") and not re.fullmatch(r"\+\d+\s+more", segment.strip(), re.I)
    ]
    normalized_segments = [
        _normalize_location_fragment(segment)
        for segment in segments
        if _looks_like_location_fragment(segment)
    ]
    if has_more_locations:
        normalized_segments.append("Multiple locations")
    return _join_location_parts(normalized_segments)


def _normalize_location_text(text: str | None) -> str | None:
    cleaned = _clean_location_text(text)
    if not cleaned:
        return None

    modes = _work_modes(cleaned)
    if MULTIPLE_PATTERN.search(cleaned):
        return _join_location_parts([*modes, "Multiple locations"])

    places = _extract_geograpy_places(cleaned)
    if places:
        return _join_location_parts([*modes, *_normalize_place_segments(cleaned, places)])

    if modes and _looks_remote_only(cleaned):
        return _join_location_parts(modes)

    location_fragment = _strip_work_modes(cleaned)
    if _looks_like_location_fragment(location_fragment):
        normalized_fragment = _normalize_location_fragment(location_fragment)
        return _join_location_parts([*modes, normalized_fragment])
    return _join_location_parts(modes)


def _clean_location_text(text: str | None) -> str | None:
    if not text:
        return None
    cleaned = re.sub(r"\s+", " ", text).strip(" -|:;,")
    structured_country_match = re.search(
        r"['\"]name['\"]\s*:\s*['\"]([^'\"]+)['\"]",
        cleaned,
        re.I,
    )
    if structured_country_match:
        cleaned = structured_country_match.group(1)
    cleaned = LOCATION_LABEL_PATTERN.sub("", cleaned)
    cleaned = TRAILING_NOISE_PATTERN.sub("", cleaned)
    cleaned = cleaned.strip(" -|:;,")
    if SEARCH_FILTER_NOISE_PATTERN.search(cleaned):
        return None
    return cleaned or None


def _location_phrase_from_context(text: str) -> str | None:
    for pattern in LOCATION_CONTEXT_PATTERNS:
        match = pattern.search(text)
        if match:
            candidate = _clean_location_text(match.group(1))
            if candidate:
                return candidate

    match = LOCATION_SENTENCE_PATTERN.search(text)
    if not match:
        return None
    candidate = match.group(1)
    candidate = re.split(
        r"\b(?:employment\s+type|job\s+description|responsibilities|requirements|apply)\b",
        candidate,
        maxsplit=1,
        flags=re.I,
    )[0]
    return _clean_location_text(candidate)


def _work_modes(text: str) -> list[str]:
    modes: list[str] = []
    if REMOTE_PATTERN.search(text):
        modes.append("Remote")
    if HYBRID_PATTERN.search(text):
        modes.append("Hybrid")
    if IN_OFFICE_PATTERN.search(text):
        modes.append("In-office")
    return modes


def _looks_remote_only(text: str) -> bool:
    without_modes = _strip_work_modes(text)
    without_modes = re.sub(r"[-,;|/()\s]+", "", without_modes)
    return not without_modes


def _strip_work_modes(text: str) -> str:
    without_modes = REMOTE_PATTERN.sub("", text)
    without_modes = HYBRID_PATTERN.sub("", without_modes)
    without_modes = IN_OFFICE_PATTERN.sub("", without_modes)
    return without_modes.strip(" -|:;,")


def _looks_like_location_fragment(text: str) -> bool:
    if len(text) > 100:
        return False
    if re.search(r"\b(?:job|responsibilities|requirements|qualifications|salary)\b", text, re.I):
        return False
    return bool(re.search(r"[A-Za-z]", text))


def _normalize_location_fragment(text: str) -> str:
    segments = [segment for segment in SEPARATOR_PATTERN.split(text) if segment.strip(" -|:;,")]
    if len(segments) > 1:
        return _join_location_parts(_normalize_place_name(segment) for segment in segments) or ""
    parts = _comma_parts(text)
    if len(parts) <= 1:
        return _normalize_place_name(text)
    return ", ".join(
        _normalize_place_part(part, index=index, total=len(parts), raw_parts=parts)
        for index, part in enumerate(parts)
    )


def _normalize_place_segments(text: str, places: list[str]) -> list[str]:
    segments = [
        _normalize_place_segment(segment, places)
        for segment in SEPARATOR_PATTERN.split(text)
        if _clean_location_text(segment)
    ]
    segments = [segment for segment in segments if segment]
    if segments:
        return segments
    return [_normalize_place_name(place) for place in places]


def _normalize_place_segment(segment: str, places: list[str]) -> str | None:
    cleaned = _clean_location_text(segment)
    if not cleaned:
        return None
    cleaned = _strip_work_modes(cleaned)
    if not cleaned:
        return None
    lower = cleaned.lower()
    if lower in NON_LOCATION_PLACES:
        return None
    if REMOTE_PATTERN.fullmatch(cleaned) or HYBRID_PATTERN.fullmatch(cleaned):
        return None
    if not any(place.lower() in lower for place in places):
        raw_parts = _comma_parts(cleaned)
        parts = [
            _normalize_place_part(part, index=index, total=len(raw_parts), raw_parts=raw_parts)
            for index, part in enumerate(raw_parts)
        ]
        parts = [part for part in parts if part.lower() not in NON_LOCATION_PLACES]
        return ", ".join(parts) or None

    raw_parts = _comma_parts(cleaned)
    parts = [
        _normalize_place_part(part, index=index, total=len(raw_parts), raw_parts=raw_parts)
        for index, part in enumerate(raw_parts)
    ]
    parts = [part for part in parts if part.lower() not in NON_LOCATION_PLACES]
    return ", ".join(parts) or None


def _comma_parts(segment: str) -> list[str]:
    return [part.strip(" -|:;,") for part in segment.split(",") if part.strip(" -|:;,")]


def _normalize_place_name(place: str) -> str:
    compact = re.sub(r"\s+", " ", place).strip(" -|:;,")
    lowered = compact.lower()
    if lowered in REGION_ALIASES:
        return REGION_ALIASES[lowered]
    if lowered in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[lowered]
    return compact


def _normalize_place_part(part: str, *, index: int, total: int, raw_parts: list[str]) -> str:
    compact = re.sub(r"\s+", " ", part).strip(" -|:;,")
    lowered = compact.lower()
    if lowered == "ca" and index == total - 1:
        previous_regions = {
            REGION_ALIASES.get(previous.lower(), previous.upper())
            for previous in raw_parts[:index]
        }
        if previous_regions & CANADIAN_REGION_CODES:
            return "Canada"
    return _normalize_place_name(compact)


def _location_from_geograpy(text: str) -> str | None:
    places = _extract_geograpy_places(text)
    modes = _work_modes(text)
    if not places:
        return _join_location_parts(modes)
    return _join_location_parts([*modes, *(_normalize_place_name(place) for place in places[:4])])


def _extract_geograpy_places(text: str | None) -> list[str]:
    cleaned = _clean_location_text(text)
    if not cleaned:
        return []
    context = _geograpy_context(cleaned)
    if context is None:
        return []
    raw_places = [
        *getattr(context, "cities", []),
        *getattr(context, "regions", []),
        *getattr(context, "places", []),
        *(
            country
            for country in getattr(context, "countries", [])
            if _country_is_explicit(cleaned, str(country))
        ),
    ]
    return _dedupe(
        _normalize_place_name(place)
        for place in raw_places
        if _is_useful_place_name(str(place)) and _place_is_explicit(cleaned, str(place))
    )


def _is_useful_place_name(place: str) -> bool:
    cleaned = _normalize_place_name(place)
    if not cleaned or cleaned.lower() in NON_LOCATION_PLACES:
        return False
    return bool(re.search(r"[A-Za-z]", cleaned))


def _place_is_explicit(text: str, place: str) -> bool:
    normalized = _normalize_place_name(place)
    variants = {place, normalized}
    variants.update(alias for alias, value in COUNTRY_ALIASES.items() if value == normalized)
    variants.update(alias for alias, value in REGION_ALIASES.items() if value == normalized)
    if normalized == "Canada":
        variants.discard("ca")
    text_lower = text.lower()
    return any(re.search(rf"\b{re.escape(variant.lower())}\b", text_lower) for variant in variants)


def _country_is_explicit(text: str, country: str) -> bool:
    normalized = _normalize_place_name(country)
    variants = {country, normalized}
    variants.update(alias for alias, value in COUNTRY_ALIASES.items() if value == normalized)
    if normalized == "Canada":
        variants.discard("ca")
    text_lower = text.lower()
    return any(re.search(rf"\b{re.escape(variant.lower())}\b", text_lower) for variant in variants)


@lru_cache(maxsize=256)
def _geograpy_context(text: str) -> Any | None:
    try:
        from geograpy import get_place_context
    except Exception:
        return None
    try:
        return get_place_context(text=text)
    except Exception:
        return None


def _join_location_parts(parts: Any) -> str | None:
    cleaned_parts = _dedupe(
        str(part).strip()
        for part in parts
        if part is not None and str(part).strip()
    )
    return "; ".join(cleaned_parts) or None


def _dedupe(parts: Any) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for part in parts:
        key = part.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(part)
    return result
