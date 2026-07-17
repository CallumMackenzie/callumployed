from __future__ import annotations

import re
from collections.abc import Iterable

from bs4 import BeautifulSoup, Tag

CORE_SECTION_HEADINGS = (
    "about the role",
    "about this role",
    "about the team",
    "about the job",
    "what to expect",
    "what you'll do",
    "what you’ll do",
    "what you will do",
    "responsibilities",
    "requirements",
    "minimum qualifications",
    "preferred qualifications",
    "qualifications",
    "what you'll bring",
    "what you’ll bring",
    "what you will bring",
    "who you are",
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
    r"ada@|all rights reserved|back-up childcare|commuter benefits|"
    r"company paid|dental|e-verify|employee assistance program|employee discounts|"
    r"equal opportunity|family-building|fertility|flexible spending accounts|"
    r"health savings account|medical plans|pet insurance|privacy notice|"
    r"reasonable accommodations?|screen reader|surrogacy|tesla ©|"
    r"vision plans|voluntary benefits"
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
    for child in element.find_all(["h2", "h3", "h4", "p", "li", "div"], recursive=True):
        if child.name == "div" and child.find(["h2", "h3", "h4", "p", "li"]):
            continue
        text = child.get_text(" ", strip=True)
        if text:
            blocks.append(text)
    if not blocks:
        return element.get_text("\n", strip=True)
    return "\n".join(blocks)


def _clean_description_text(text: str | None) -> str | None:
    if not text:
        return None
    soup = BeautifulSoup(text, "lxml")
    plain_text = soup.get_text("\n", strip=True) if soup.find() else text
    plain_text = _insert_section_breaks(plain_text.replace("\xa0", " "))
    lines = [_normalize_line(line) for line in re.split(r"[\n•]+", plain_text)]
    lines = [line for line in lines if line]
    lines = _split_oversized_lines(lines)
    lines = _trim_to_relevant_sections(lines)
    lines = _drop_noise_lines(lines)
    lines = _dedupe_lines(lines)
    lines = [_format_markdown_heading(line) for line in lines]
    if not lines:
        return None
    return "\n".join(lines)


def _normalize_line(line: str) -> str:
    normalized = WHITESPACE_PATTERN.sub(" ", line).strip(" -|•·")
    return normalized


def _insert_section_breaks(text: str) -> str:
    headings = [*CORE_SECTION_HEADINGS, *STOP_SECTION_HEADINGS, "benefits as a"]
    result = text
    for heading in sorted(headings, key=len, reverse=True):
        result = re.sub(
            rf"(?<!^)(?<!\n)\b({re.escape(heading)})\b",
            r"\n\1",
            result,
            flags=re.I,
        )
        result = re.sub(
            rf"\b({re.escape(heading)})\s+(?=[A-Z])",
            r"\1\n",
            result,
            flags=re.I,
        )
    return result


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
        if all(_is_metadata_line(previous) for previous in lines[:index]):
            return index
        return 0
    return 0


def _is_core_heading(line: str) -> bool:
    normalized = _heading_key(line)
    return any(
        normalized == heading or normalized.startswith(f"{heading}:")
        for heading in CORE_SECTION_HEADINGS
    )


def _format_markdown_heading(line: str) -> str:
    if _is_core_heading(line):
        return f"## {line.strip(': ')}"
    return line


def _is_stop_heading(line: str) -> bool:
    normalized = _heading_key(line)
    if normalized == "apply":
        return True
    return any(
        normalized == heading or normalized.startswith(f"{heading}:")
        for heading in STOP_SECTION_HEADINGS
    )


def _heading_key(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip(": ").lower()


def _is_metadata_line(line: str) -> bool:
    return bool(
        NAV_NOISE_PATTERN.search(line)
        or re.search(r"\b(?:req\.?\s*id|job\s*type|employment\s*type)\b", line, re.I)
        or re.fullmatch(r"[A-Za-z .'-]+,\s*[A-Za-z]{2,}(?:,\s*[A-Za-z .'-]+)?", line)
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
        kept.append(line)
    return kept


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
    lower = text.lower()
    score = min(len(text), 4000)
    score += 500 * sum(1 for heading in CORE_SECTION_HEADINGS if heading in lower)
    score -= 400 * sum(1 for heading in STOP_SECTION_HEADINGS if heading in lower)
    score -= 800 * len(NOISE_PATTERN.findall(text))
    return score
