from __future__ import annotations

import re
from collections.abc import Iterable

from bs4 import BeautifulSoup, Tag

CORE_SECTION_HEADINGS = (
    "who are we",
    "why this role",
    "about the role",
    "about this role",
    "about the team",
    "about citadel securities",
    "about the job",
    "about susquehanna",
    "job description",
    "job responsibilities",
    "what to expect",
    "what you'll do",
    "what you’ll do",
    "what you will do",
    "responsibilities",
    "requirements",
    "minimum qualifications",
    "minimum requirements",
    "preferred qualifications",
    "required qualifications",
    "bonus qualifications",
    "program requirements",
    "qualifications",
    "what you'll bring",
    "what you’ll bring",
    "what you will bring",
    "what's in it for you",
    "who you are",
    "who we are",
    "your role",
    "role overview",
    "you will",
    "you have",
    "we prefer",
    "nice to have",
    "assets",
    "your objectives",
    "your skills & talents",
)
STOP_SECTION_HEADINGS = (
    "benefits",
    "compensation",
    "equal opportunity",
    "reasonable accommodation",
    "accommodation",
    "privacy",
    "e-verify",
)
DESCRIPTION_SELECTORS = (
    "[data-testid*=description]",
    "[data-testid*=job][data-testid*=body]",
    "[data-qa*=description]",
    "[class*=job-description]",
    "[class*=jobDescription]",
    "[class*=description]",
    "[class*=posting]",
    "[class*=job-detail]",
    "[class*=jobDetail]",
    "[class*=details]",
    "main",
    "article",
)
NOISE_PATTERN = re.compile(
    r"\b(?:"
    r"ada@|all rights reserved|back-up childcare|benefits\s+for\s+this\s+role|"
    r"commuter benefits|"
    r"company paid|dental|e-verify|employee assistance program|employee discounts|"
    r"equal opportunity|family-building|fertility|flexible spending accounts|"
    r"health savings account|medical plans|pet insurance|privacy notice|"
    r"owner and data controller|reasonable accommodations?|recruiting agency|"
    r"screen reader|surrogacy|tesla ©|this website collects|types of data collected|"
    r"unexpected error|vision plans|voluntary benefits|website encountered an unexpected error"
    r")\b",
    re.I,
)
NAV_NOISE_PATTERN = re.compile(
    r"\b(?:"
    r"apply now|careers|connect|cookie|job alert|privacy\s*&\s*legal|"
    r"skip to main content|view all jobs"
    r")\b",
    re.I,
)
WHITESPACE_PATTERN = re.compile(r"[ \t\r\f\v]+")
HEADING_MARKER = "__CALLUMPLOYED_HEADING__ "
INLINE_SECTION_PATTERN = re.compile(
    r"\b("
    r"About Citadel Securities|About Susquehanna|Job Description|"
    r"What'?s in it for you|Your Objectives|Your Skills & Talents"
    r")\s*:?",
    re.I,
)
KNOWN_LINE_HEADING_PATTERN = re.compile(
    r"^(?:"
    r"who are we|why (?:this|the) (?:role|team|position)|"
    r"about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|"
    r"minimum (?:qualifications|requirements)|preferred qualifications|"
    r"required qualifications|bonus qualifications|program requirements|"
    r"qualifications|requirements|"
    r"responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|"
    r"what'?s in it for you|who (?:you|we) are|your role|role overview|"
    r"you will|you have|we prefer|nice to have|assets|your objectives|your skills & talents|"
    r"why join [a-z0-9 .&'-]{2,50}|"
    r"at [a-z0-9 .&'-]{2,50}, you will|"
    r"we(?:'|’)re looking for someone who has|"
    r"about (?:our|the) [a-z0-9 /&+().'-]{2,60} program|"
    r"as an? [a-z][a-z0-9 /&+().'-]{1,60}, you will|"
    r"you (?:may|might|would) be (?:a )?good fit if you (?:have|are)"
    r")[:?]?$",
    re.I,
)
COMPANY_ABOUT_HEADING_PATTERN = re.compile(
    r"^About (?:[A-Z][A-Za-z0-9&.'-]*)(?: [A-Z][A-Za-z0-9&.'-]*){0,4}:?$"
)
PERKS_HEADING_PATTERN = re.compile(
    r"^(?:full[- ]time )?employees at [a-z0-9 .&'-]{2,50} enjoy (?:these )?perks:?$",
    re.I,
)


def extract_job_description(
    soup: BeautifulSoup,
    *,
    structured_description: str | None = None,
    fallback_text: str | None = None,
) -> str | None:
    candidates = [
        _clean_description_text(structured_description),
        *(_candidate_texts_from_dom(soup)),
        _clean_description_text(fallback_text),
    ]
    return _best_description(candidate for candidate in candidates if candidate)


def clean_job_description(text: str | None) -> str | None:
    return _clean_description_text(text)


def _candidate_texts_from_dom(soup: BeautifulSoup) -> list[str]:
    candidates: list[str] = []
    seen: set[int] = set()
    for selector in DESCRIPTION_SELECTORS:
        for element in soup.select(selector):
            if not isinstance(element, Tag):
                continue
            element_id = id(element)
            if element_id in seen:
                continue
            seen.add(element_id)
            text = _text_from_element(element)
            cleaned = _clean_description_text(text)
            if cleaned:
                candidates.append(cleaned)
    return candidates


def _text_from_element(element: Tag) -> str:
    for removable in element.select("script, style, noscript, svg, nav, footer, header"):
        removable.decompose()
    blocks: list[str] = []
    heading_tags = {"h2", "h3", "h4", "h5", "h6"}
    content_tags = [*heading_tags, "p", "li", "div"]
    for child in element.find_all(content_tags, recursive=True):
        if child.name == "div" and child.find(content_tags):
            continue
        text = child.get_text(" ", strip=True)
        if text:
            if child.name in heading_tags:
                blocks.append(f"{HEADING_MARKER}{text}")
            else:
                blocks.append(text)
    if not blocks:
        return element.get_text("\n", strip=True)
    return "\n".join(blocks)


def _clean_description_text(text: str | None) -> str | None:
    if not text:
        return None
    soup = BeautifulSoup(text, "lxml")
    plain_text = _text_from_element(soup) if soup.find() else text
    plain_text = plain_text.replace("\xa0", " ")
    lines = [_normalize_line(line) for line in re.split(r"[\n•]+", plain_text)]
    lines = [line for line in lines if line]
    if _has_transient_error_shell(lines):
        return None
    lines = _split_inline_sections(lines)
    lines = _split_oversized_lines(lines)
    lines = _drop_leading_google_job_card_chrome(lines)
    lines = _trim_to_relevant_sections(lines)
    lines = _drop_noise_lines(lines)
    lines = _dedupe_lines(lines)
    lines = [_format_markdown_heading(line) for line in lines]
    if not lines:
        return None
    return "\n".join(lines)


def _normalize_line(line: str) -> str:
    is_heading = line.startswith(HEADING_MARKER)
    content = line[len(HEADING_MARKER) :] if is_heading else line
    normalized = WHITESPACE_PATTERN.sub(" ", content).strip(" -|•·")
    normalized = re.sub(
        r"^(?:single\s+position|multiple\s+locations?)\s+",
        "",
        normalized,
        flags=re.I,
    )
    if is_heading and normalized:
        return f"{HEADING_MARKER}{normalized}"
    return normalized


def _split_inline_sections(lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in lines:
        result.extend(_split_inline_section_line(line))
    return result


def _split_inline_section_line(line: str) -> list[str]:
    matches = list(INLINE_SECTION_PATTERN.finditer(line))
    if not matches:
        return _split_inline_dash_bullets(line)

    result: list[str] = []
    first_match = matches[0]
    prefix = line[: first_match.start()].strip()
    if prefix and _heading_key(f"{HEADING_MARKER}{first_match.group(1)}") != "job description":
        result.extend(_split_inline_dash_bullets(prefix))

    for index, match in enumerate(matches):
        heading = _normalize_inline_heading(match.group(1))
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(line)
        body = line[match.end() : next_start].strip(" :-")
        result.append(f"{HEADING_MARKER}{heading}")
        result.extend(_split_inline_dash_bullets(body))
    return [item for item in result if item]


def _split_inline_dash_bullets(line: str) -> list[str]:
    if " - " not in line:
        return [line] if line else []
    return [part.strip() for part in re.split(r"\s+-\s+", line) if part.strip()]


def _normalize_inline_heading(value: str) -> str:
    return WHITESPACE_PATTERN.sub(" ", value).strip(" :")


def _split_oversized_lines(lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in lines:
        if len(line) <= 500:
            result.append(line)
            continue
        result.extend(_sentence_chunks(line))
    return result


def _sentence_chunks(line: str) -> list[str]:
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z])", line)
        if sentence.strip()
    ]
    chunks: list[str] = []
    current: list[str] = []
    current_length = 0
    for sentence in sentences:
        if current and current_length + len(sentence) > 360:
            chunks.append(" ".join(current))
            current = []
            current_length = 0
        current.append(sentence)
        current_length += len(sentence) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks or [line]


def _trim_to_relevant_sections(lines: list[str]) -> list[str]:
    start_index = _description_start_index(lines)
    end_index = len(lines)
    for index in range(start_index + 1, len(lines)):
        if _is_stop_heading(lines[index]):
            end_index = index
            break
    return lines[start_index:end_index]


def _description_start_index(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if not _is_core_heading(line):
            continue
        if _heading_key(line) == "job description":
            return index
        if all(_is_metadata_line(previous) for previous in lines[:index]):
            return index
        return 0
    return 0


def _is_core_heading(line: str) -> bool:
    if not _has_heading_structure(line):
        return False
    if COMPANY_ABOUT_HEADING_PATTERN.fullmatch(_strip_heading_structure(line).strip()):
        return True
    normalized = _heading_key(line)
    return bool(
        re.fullmatch(r"as an? .{2,60}, you will", normalized)
        or re.fullmatch(r"why join .{2,50}", normalized)
        or re.fullmatch(r"at .{2,50}, you will", normalized)
        or re.fullmatch(r"we(?:'|’)re looking for someone who has", normalized)
        or re.fullmatch(r"about (?:our|the) .{2,60} program", normalized)
        or re.fullmatch(
            r"you (?:may|might|would) be (?:a )?good fit if you (?:have|are)",
            normalized,
        )
        or any(
            normalized == heading or normalized.startswith(f"{heading}:")
            for heading in CORE_SECTION_HEADINGS
        )
    )


def _format_markdown_heading(line: str) -> str:
    if line.startswith(HEADING_MARKER) or _is_core_heading(line):
        return f"## {_strip_heading_structure(line).strip(': ')}"
    if _has_heading_structure(line):
        return _strip_heading_structure(line)
    return line


def _is_stop_heading(line: str) -> bool:
    if PERKS_HEADING_PATTERN.fullmatch(_strip_heading_structure(line).strip()):
        return True
    if not _has_heading_structure(line):
        return False
    normalized = _heading_key(line)
    if normalized == "apply":
        return True
    return any(
        normalized == heading or normalized.startswith(f"{heading}:")
        for heading in STOP_SECTION_HEADINGS
    )


def _heading_key(line: str) -> str:
    line = _strip_heading_structure(line)
    return re.sub(r"\s+", " ", line).strip(":? ").lower()


def _has_heading_structure(line: str) -> bool:
    return (
        line.startswith(HEADING_MARKER)
        or line.lstrip().startswith("##")
        or bool(KNOWN_LINE_HEADING_PATTERN.fullmatch(line.strip()))
        or bool(COMPANY_ABOUT_HEADING_PATTERN.fullmatch(line.strip()))
    )


def _strip_heading_structure(line: str) -> str:
    if line.startswith(HEADING_MARKER):
        return line[len(HEADING_MARKER) :]
    return re.sub(r"^#{1,6}\s*", "", line.strip())


def _is_metadata_line(line: str) -> bool:
    return bool(
        NAV_NOISE_PATTERN.search(line)
        or _is_google_job_card_chrome_line(line)
        or re.search(r"\b(?:req\.?\s*id|job\s*type|employment\s*type)\b", line, re.I)
        or re.fullmatch(r"[A-Za-z .'-]+,\s*[A-Za-z]{2,}(?:,\s*[A-Za-z .'-]+)?", line)
    )


def _drop_leading_google_job_card_chrome(lines: list[str]) -> list[str]:
    if not any(_is_google_job_card_chrome_line(line) for line in lines[:6]):
        return lines
    for index, line in enumerate(lines[:10]):
        if _is_google_job_body_start(line) or _is_core_heading(line):
            return lines[index:]
    return lines


def _is_google_job_card_chrome_line(line: str) -> bool:
    normalized = re.sub(r"\s+", " ", line).strip()
    return bool(
        re.fullmatch(r"(?:link\s+)?Copy link", normalized, re.I)
        or re.fullmatch(r"(?:email\s+)?Email a friend", normalized, re.I)
        or re.fullmatch(r"info_outline", normalized, re.I)
        or (
            normalized.startswith("corporate_fare ")
            and " place " in normalized
            and " bar_chart " in normalized
        )
    )


def _is_google_job_body_start(line: str) -> bool:
    body_start_pattern = (
        r"(?:This posting is for|Applications will be reviewed|"
        r"Participation in the internship)"
    )
    return bool(
        re.match(
            body_start_pattern,
            line,
            re.I,
        )
    )


def _drop_noise_lines(lines: list[str]) -> list[str]:
    kept: list[str] = []
    for line in lines:
        if len(line) < 2:
            continue
        if NOISE_PATTERN.search(line):
            break
        if NAV_NOISE_PATTERN.fullmatch(line):
            continue
        if _is_google_job_card_chrome_line(line):
            continue
        kept.append(line)
    return kept


def _has_transient_error_shell(lines: list[str]) -> bool:
    text = " ".join(lines)
    return bool(
        re.search(
            r"\b(?:an error has occurred|website encountered an unexpected error|"
            r"please try again later)\b",
            text,
            re.I,
        )
    )


def _dedupe_lines(lines: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for line in lines:
        key = _dedupe_key(line)
        if key in seen:
            continue
        seen.add(key)
        result.append(line)
    return result


def _dedupe_key(line: str) -> str:
    key = re.sub(r"[^a-z0-9]+", " ", line.lower())
    return re.sub(r"\s+", " ", key).strip()


def _best_description(candidates: Iterable[str]) -> str | None:
    best: str | None = None
    best_score = 0
    for candidate in candidates:
        score = _description_score(candidate)
        if score > best_score:
            best = candidate
            best_score = score
    return best


def _description_score(text: str) -> int:
    lines = text.splitlines()
    score = min(len(text), 4000)
    score += 500 * sum(1 for line in lines if _is_core_heading(line))
    score -= 400 * sum(1 for line in lines if _is_stop_heading(line))
    score -= 800 * len(NOISE_PATTERN.findall(text))
    return score
