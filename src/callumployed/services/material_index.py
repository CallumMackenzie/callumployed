from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

INDEX_VERSION = 1
MAX_SECTION_CHARS = 24_000
DEFAULT_RETRIEVAL_LIMIT = 5
DEFAULT_RETRIEVAL_CONTENT_CHARS = 16_000

_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9+#.\-/]{1,}", re.IGNORECASE)
_FILENAME_PATTERN = re.compile(r"[^a-z0-9]+")
_CONTROL_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

_STOP_WORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "built",
    "for",
    "from",
    "have",
    "into",
    "its",
    "that",
    "the",
    "their",
    "this",
    "used",
    "using",
    "was",
    "were",
    "with",
}

_TOOL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (name, re.compile(pattern, re.IGNORECASE))
    for name, pattern in (
        ("AWS", r"\b(?:aws|amazon web services)\b"),
        ("Azure", r"\bazure\b"),
        ("C++", r"(?<!\w)c\+\+(?!\w)"),
        ("C#", r"(?<!\w)c#(?!\w)"),
        ("Docker", r"\bdocker\b"),
        ("FastAPI", r"\bfastapi\b"),
        ("GCP", r"\b(?:gcp|google cloud)\b"),
        ("Git", r"\bgit(?:hub|lab)?\b"),
        ("Go", r"\b(?:go|golang)\b"),
        ("GraphQL", r"\bgraphql\b"),
        ("Java", r"\bjava\b"),
        ("JavaScript", r"\bjavascript\b"),
        ("Kafka", r"\bkafka\b"),
        ("Kubernetes", r"\b(?:kubernetes|k8s)\b"),
        ("LangChain", r"\blangchain\b"),
        ("Linux", r"\blinux\b"),
        ("MongoDB", r"\bmongodb\b"),
        ("MySQL", r"\bmysql\b"),
        ("Next.js", r"\bnext\.?js\b"),
        ("Node.js", r"\bnode\.?js\b"),
        ("OpenAI", r"\bopenai\b"),
        ("PostgreSQL", r"\b(?:postgresql|postgres)\b"),
        ("PyTorch", r"\bpytorch\b"),
        ("Python", r"\bpython\b"),
        ("React", r"\breact\b"),
        ("Redis", r"\bredis\b"),
        ("Rust", r"\brust\b"),
        ("SQL", r"\bsql\b"),
        ("Swift", r"\bswift\b"),
        ("TensorFlow", r"\btensorflow\b"),
        ("Terraform", r"\bterraform\b"),
        ("TypeScript", r"\btypescript\b"),
    )
)

_ATTRIBUTE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (name, re.compile(pattern, re.IGNORECASE))
    for name, pattern in (
        ("architecture", r"\b(?:architect|architecture|system design|distributed)\b"),
        ("automation", r"\b(?:automat|pipeline|workflow|orchestrat)\w*\b"),
        ("collaboration", r"\b(?:collaborat|cross-functional|stakeholder|partnered)\w*\b"),
        ("data", r"\b(?:data|analytics|etl|database|dataset)\b"),
        ("leadership", r"\b(?:lead|led|mentor|manage|owner|ownership)\w*\b"),
        ("machine learning", r"\b(?:machine learning|deep learning|model|training|inference)\b"),
        (
            "performance",
            r"(?:\bperformance\b|\blatency\b|\bthroughput\b|\boptim\w*\b|\d+(?:\.\d+)?\s*%)",
        ),
        ("product", r"\b(?:customer|product|user|ux|feature)\w*\b"),
        ("reliability", r"\b(?:reliab|availability|incident|monitor|observability|on-call)\w*\b"),
        ("security", r"\b(?:security|secure|auth|privacy|vulnerab)\w*\b"),
        ("testing", r"\b(?:test|quality|qa|verification|validation)\w*\b"),
    )
)

_ACTION_PATTERN = re.compile(
    r"\b(?:built|created|designed|developed|implemented|improved|launched|led|"
    r"maintained|managed|migrated|optimized|reduced|shipped|trained)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class MaterialSection:
    source_id: int | None
    source_filename: str
    ordinal: int
    title: str
    content: str
    tools: tuple[str, ...]
    attributes: tuple[str, ...]
    summary: str
    keywords: tuple[str, ...]


def default_material_index_root() -> Path:
    configured = os.environ.get("CALLUMPLOYED_MATERIAL_INDEX_ROOT", "").strip()
    if configured:
        return Path(configured).expanduser()
    project_root = Path(__file__).resolve().parents[3]
    if (project_root / "pyproject.toml").exists():
        return project_root / "application-material-index"
    return Path.home() / ".local" / "share" / "callumployed" / "application-material-index"


def split_experience_note(note: Mapping[str, object]) -> list[MaterialSection]:
    filename = str(note.get("filename") or "experience-note.md")
    raw_content = str(note.get("content") or "")
    if _looks_like_binary_document(raw_content):
        return []
    content = _normalize_source_text(raw_content)
    raw_source_id = note.get("id")
    source_id = raw_source_id if isinstance(raw_source_id, int) else None
    titled_chunks = _split_markdown_sections(content, fallback_title=Path(filename).stem)
    sections: list[MaterialSection] = []
    ordinal = 0
    for title, section_content in titled_chunks:
        for part_number, bounded_content in enumerate(_chunk_content(section_content), start=1):
            ordinal += 1
            part_title = title
            if len(section_content) > MAX_SECTION_CHARS:
                part_title = f"{title} (part {part_number})"
            tools = tuple(sorted(_extract_tools(f"{part_title}\n{bounded_content}")))
            attributes = tuple(sorted(_extract_attributes(f"{part_title}\n{bounded_content}")))
            summary = _summarize_section(part_title, bounded_content, tools, attributes)
            keywords = tuple(
                sorted(
                    _tokens(" ".join([part_title, summary, " ".join(tools), " ".join(attributes)]))
                )
            )
            sections.append(
                MaterialSection(
                    source_id=source_id,
                    source_filename=filename,
                    ordinal=ordinal,
                    title=part_title,
                    content=bounded_content.strip(),
                    tools=tools,
                    attributes=attributes,
                    summary=summary,
                    keywords=keywords,
                )
            )
    return sections


def build_material_index(
    notes: Iterable[Mapping[str, object]],
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    source_notes = list(notes)
    destination = root or default_material_index_root()
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}-", dir=destination.parent))
    backup = destination.with_name(f".{destination.name}-previous")
    generated_at = datetime.now(UTC).isoformat()
    try:
        sections_root = temporary / "sections"
        sections_root.mkdir(parents=True)
        records: list[dict[str, Any]] = []
        skipped_sources: list[dict[str, str]] = []
        used_names: set[str] = set()
        for note in source_notes:
            note_sections = split_experience_note(note)
            if not note_sections:
                skipped_sources.append(
                    {
                        "filename": str(note.get("filename") or "experience-note"),
                        "reason": (
                            "The stored content appears to be an unextracted binary document."
                        ),
                    }
                )
            for section in note_sections:
                filename = _unique_section_filename(section, used_names)
                relative_path = Path("sections") / filename
                (temporary / relative_path).write_text(
                    _render_section_document(section), encoding="utf-8"
                )
                records.append(
                    {
                        "title": section.title,
                        "path": relative_path.as_posix(),
                        "source_id": section.source_id,
                        "source_filename": section.source_filename,
                        "summary": section.summary,
                        "tools": list(section.tools),
                        "attributes": list(section.attributes),
                        "keywords": list(section.keywords),
                        "content_chars": len(section.content),
                    }
                )
        manifest = {
            "version": INDEX_VERSION,
            "generated_at": generated_at,
            "source_fingerprint": _source_fingerprint(source_notes),
            "source_count": len(source_notes),
            "indexed_source_count": len(source_notes) - len(skipped_sources),
            "skipped_source_count": len(skipped_sources),
            "skipped_sources": skipped_sources,
            "document_count": len(records),
            "documents": records,
        }
        (temporary / "index.md").write_text(
            _render_index_document(
                records,
                generated_at=generated_at,
                skipped_sources=skipped_sources,
            ),
            encoding="utf-8",
        )
        (temporary / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if backup.exists():
            shutil.rmtree(backup)
        if destination.exists():
            destination.rename(backup)
        temporary.rename(destination)
        if backup.exists():
            shutil.rmtree(backup)
    except Exception:
        if destination.exists() and backup.exists():
            shutil.rmtree(destination)
            backup.rename(destination)
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return get_material_index_status(source_notes, root=destination)


def get_material_index_status(
    notes: Iterable[Mapping[str, object]],
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    source_notes = list(notes)
    destination = root or default_material_index_root()
    manifest = _load_manifest(destination)
    if manifest is None:
        status = "missing"
    elif manifest.get("source_fingerprint") != _source_fingerprint(source_notes):
        status = "stale"
    else:
        status = "ready"
    return {
        "status": status,
        "needs_index": status != "ready",
        "warning": _index_warning(status, bool(source_notes)),
        "generated_at": manifest.get("generated_at") if manifest else None,
        "document_count": int(manifest.get("document_count") or 0) if manifest else 0,
        "source_count": len(source_notes),
        "indexed_source_count": (
            int(manifest.get("indexed_source_count") or 0) if manifest else 0
        ),
        "skipped_source_count": (
            int(manifest.get("skipped_source_count") or 0) if manifest else 0
        ),
        "folder": str(destination),
        "index_path": str(destination / "index.md"),
    }


def retrieve_indexed_materials(
    notes: Iterable[Mapping[str, object]],
    *,
    query: str,
    root: Path | None = None,
    limit: int = DEFAULT_RETRIEVAL_LIMIT,
    total_content_limit: int = DEFAULT_RETRIEVAL_CONTENT_CHARS,
) -> list[dict[str, object]]:
    source_notes = list(notes)
    destination = root or default_material_index_root()
    status = get_material_index_status(source_notes, root=destination)
    if status["status"] != "ready" or limit <= 0 or total_content_limit <= 0:
        return []
    manifest = _load_manifest(destination)
    if manifest is None:
        return []
    query_tokens = _tokens(query)
    ranked: list[tuple[float, int, Mapping[str, object]]] = []
    documents = manifest.get("documents")
    if not isinstance(documents, list):
        return []
    for position, raw_document in enumerate(documents):
        if not isinstance(raw_document, dict):
            continue
        document = raw_document
        title_tokens = _tokens(str(document.get("title") or ""))
        tool_tokens = _tokens(" ".join(str(item) for item in document.get("tools") or []))
        attribute_tokens = _tokens(" ".join(str(item) for item in document.get("attributes") or []))
        keyword_tokens = {
            str(item).lower() for item in document.get("keywords") or [] if str(item).strip()
        }
        score = (
            5 * len(query_tokens & title_tokens)
            + 4 * len(query_tokens & tool_tokens)
            + 2 * len(query_tokens & attribute_tokens)
            + len(query_tokens & keyword_tokens)
        )
        if score > 0:
            ranked.append((float(score), position, document))
    ranked.sort(key=lambda item: (-item[0], item[1]))

    selected: list[dict[str, object]] = []
    remaining = total_content_limit
    per_document_limit = max(500, total_content_limit // max(1, limit))
    for rank_score, _, indexed_document in ranked[:limit]:
        relative_path = str(indexed_document.get("path") or "")
        page_path = destination / relative_path
        try:
            content = page_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if remaining <= 0:
            break
        content = _bounded_relevant_page(
            content,
            query_tokens=query_tokens,
            limit=min(per_document_limit, remaining),
        )
        remaining -= len(content)
        selected.append(
            {
                "filename": relative_path,
                "title": indexed_document.get("title"),
                "content": content,
                "summary": indexed_document.get("summary"),
                "tools": indexed_document.get("tools") or [],
                "attributes": indexed_document.get("attributes") or [],
                "relevance_score": rank_score,
                "updated_at": status.get("generated_at"),
            }
        )
    return selected


def _bounded_relevant_page(content: str, *, query_tokens: set[str], limit: int) -> str:
    if len(content) <= limit:
        return content
    if limit <= 0:
        return ""
    source_marker = "## Source details"
    marker_index = content.find(source_marker)
    header_end = marker_index + len(source_marker) if marker_index >= 0 else min(900, len(content))
    header = content[:header_end].strip()
    body = content[header_end:].strip()
    header_limit = min(len(header), max(200, limit // 3))
    rendered = header[:header_limit].rstrip()
    remaining = limit - len(rendered) - 2
    if remaining <= 0:
        return rendered[:limit]

    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
    ranked = sorted(
        enumerate(paragraphs),
        key=lambda item: (
            -(
                5 * len(query_tokens & _tokens(item[1]))
                + 2 * bool(re.search(r"\d", item[1]))
                + bool(_ACTION_PATTERN.search(item[1]))
            ),
            item[0],
        ),
    )
    chosen: list[tuple[int, str]] = []
    for index, paragraph in ranked:
        if remaining <= 0:
            break
        excerpt = paragraph[: min(remaining, 1_200)]
        chosen.append((index, excerpt))
        remaining -= len(excerpt) + 2
    chosen.sort(key=lambda item: item[0])
    if chosen:
        rendered += "\n\n" + "\n\n".join(paragraph for _, paragraph in chosen)
    return rendered[:limit]


def _looks_like_binary_document(content: str) -> bool:
    leading = content.lstrip()[:16]
    if leading.startswith(("%PDF-", "PK\x03\x04")):
        return True
    sample = content[:20_000]
    if not sample:
        return False
    suspicious = sum(
        character == "\ufffd" or (ord(character) < 32 and character not in "\n\r\t\f")
        for character in sample
    )
    return suspicious / len(sample) > 0.02


def _normalize_source_text(content: str) -> str:
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    normalized = _CONTROL_PATTERN.sub("", normalized)
    return normalized.strip()


def _split_markdown_sections(content: str, *, fallback_title: str) -> list[tuple[str, str]]:
    if not content:
        return [(fallback_title or "Experience note", "")]
    sections: list[tuple[str, str]] = []
    current_title = fallback_title or "Experience note"
    current_lines: list[str] = []
    found_heading = False
    for line in content.splitlines():
        match = _HEADING_PATTERN.match(line)
        if match:
            if found_heading or any(item.strip() for item in current_lines):
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = _clean_title(match.group(2))
            current_lines = []
            found_heading = True
        else:
            current_lines.append(line)
    if found_heading or any(item.strip() for item in current_lines):
        sections.append((current_title, "\n".join(current_lines).strip()))
    if not found_heading and len(content) > MAX_SECTION_CHARS:
        return [
            (f"{fallback_title} part {i}", chunk)
            for i, chunk in enumerate(_chunk_content(content), 1)
        ]
    return sections or [(fallback_title or "Experience note", content)]


def _chunk_content(content: str) -> list[str]:
    if len(content) <= MAX_SECTION_CHARS:
        return [content]
    chunks: list[str] = []
    remaining = content
    while len(remaining) > MAX_SECTION_CHARS:
        boundary = remaining.rfind("\n\n", 0, MAX_SECTION_CHARS)
        if boundary < MAX_SECTION_CHARS // 2:
            boundary = remaining.rfind("\n", 0, MAX_SECTION_CHARS)
        if boundary < MAX_SECTION_CHARS // 2:
            boundary = MAX_SECTION_CHARS
        chunks.append(remaining[:boundary].strip())
        remaining = remaining[boundary:].strip()
    if remaining:
        chunks.append(remaining)
    return chunks or [""]


def _extract_tools(content: str) -> set[str]:
    return {name for name, pattern in _TOOL_PATTERNS if pattern.search(content)}


def _extract_attributes(content: str) -> set[str]:
    return {name for name, pattern in _ATTRIBUTE_PATTERNS if pattern.search(content)}


def _summarize_section(
    title: str,
    content: str,
    tools: tuple[str, ...],
    attributes: tuple[str, ...],
) -> str:
    candidates = [part.strip(" -\t") for part in re.split(r"\n+|(?<=[.!?])\s+", content)]
    candidates = [part for part in candidates if len(part) >= 20]
    ranked = sorted(
        enumerate(candidates),
        key=lambda item: (
            -(
                3 * bool(re.search(r"\d", item[1]))
                + 2 * bool(_ACTION_PATTERN.search(item[1]))
                + len(_extract_tools(item[1]))
            ),
            item[0],
        ),
    )
    evidence = [_clean_excerpt(text) for _, text in ranked[:2]]
    details: list[str] = []
    if tools:
        details.append(f"Tools: {', '.join(tools)}.")
    if attributes:
        details.append(f"Useful attributes: {', '.join(attributes)}.")
    if evidence:
        details.append("Evidence: " + " ".join(evidence))
    if not details:
        details.append(f"Section covering {title}.")
    return " ".join(details)


def _clean_excerpt(value: str, limit: int = 280) -> str:
    excerpt = re.sub(r"\s+", " ", value).strip()
    if len(excerpt) > limit:
        excerpt = excerpt[: limit - 1].rstrip() + "…"
    if excerpt and excerpt[-1] not in ".!?":
        excerpt += "."
    return excerpt


def _tokens(value: str) -> set[str]:
    return {
        token.lower().strip("./-")
        for token in _TOKEN_PATTERN.findall(value)
        if token.lower().strip("./-") not in _STOP_WORDS and len(token.lower().strip("./-")) >= 2
    }


def _source_fingerprint(notes: Iterable[Mapping[str, object]]) -> str:
    digest = hashlib.sha256()
    normalized: list[tuple[str, str, str]] = []
    for note in notes:
        content = str(note.get("content") or "")
        normalized.append(
            (
                str(note.get("id") or ""),
                str(note.get("filename") or ""),
                hashlib.sha256(content.encode()).hexdigest(),
            )
        )
    for item in sorted(normalized):
        digest.update(json.dumps(item, ensure_ascii=False).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def _unique_section_filename(section: MaterialSection, used_names: set[str]) -> str:
    source_slug = _slug(Path(section.source_filename).stem) or "note"
    title_slug = _slug(section.title) or "section"
    base = f"{source_slug}-{section.ordinal:03d}-{title_slug}"
    candidate = f"{base}.md"
    suffix = 2
    while candidate in used_names:
        candidate = f"{base}-{suffix}.md"
        suffix += 1
    used_names.add(candidate)
    return candidate


def _slug(value: str) -> str:
    return _FILENAME_PATTERN.sub("-", value.lower()).strip("-")[:72]


def _clean_title(value: str) -> str:
    title = re.sub(r"\s+#+\s*$", "", value).strip()
    return re.sub(r"\s+", " ", title) or "Untitled section"


def _render_section_document(section: MaterialSection) -> str:
    metadata = [
        f"# {section.title}",
        "",
        f"- Source: `{section.source_filename}`",
        f"- Source section: {section.ordinal}",
    ]
    if section.tools:
        metadata.append(f"- Tools: {', '.join(section.tools)}")
    if section.attributes:
        metadata.append(f"- Useful attributes: {', '.join(section.attributes)}")
    metadata.extend(["", "## Index summary", "", section.summary, "", "## Source details", ""])
    if section.content:
        metadata.append(section.content)
    return "\n".join(metadata).rstrip() + "\n"


def _render_index_document(
    records: list[dict[str, Any]],
    *,
    generated_at: str,
    skipped_sources: list[dict[str, str]],
) -> str:
    lines = [
        "# Application material index",
        "",
        f"Generated: {generated_at}",
        "",
        (
            "This index summarizes project and employment-history pages for targeted "
            "resume and cover-letter retrieval."
        ),
        "",
    ]
    if not records:
        lines.append("No project or employment-history sections were available.")
    for record in records:
        lines.extend(
            [
                f"## {record['title']}",
                "",
                f"- Page: [{record['path']}]({record['path']})",
                f"- Source: `{record['source_filename']}`",
                f"- Summary: {record['summary']}",
                f"- Tools: {', '.join(record['tools']) or 'Not explicitly identified'}",
                (
                    "- Useful attributes: "
                    f"{', '.join(record['attributes']) or 'Not explicitly identified'}"
                ),
                "",
            ]
        )
    if skipped_sources:
        lines.extend(["## Skipped source uploads", ""])
        for source in skipped_sources:
            lines.append(f"- `{source['filename']}` — {source['reason']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _load_manifest(root: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or payload.get("version") != INDEX_VERSION:
        return None
    return payload


def _index_warning(status: str, has_notes: bool) -> str:
    if not has_notes:
        return "Upload project or employment-history notes before indexing."
    if status == "stale":
        return (
            "Application materials changed. Index them again before generating tailored documents."
        )
    if status == "missing":
        return "Index application materials before generating tailored documents."
    return ""
