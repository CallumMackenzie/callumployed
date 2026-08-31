import hashlib
import json
import math
import re
from pathlib import PurePath

import turso

from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    CoverLetterExample,
    Event,
    EventSource,
    ExperienceNote,
    MasterResume,
    Role,
    RoleDiscoveryAttempt,
    RoleDiscoveryStatus,
    RoleListItem,
    RoleStatus,
    ScanCandidate,
    ScanPage,
    ScanRun,
    ScanRunListItem,
    ScanStatus,
)
from callumployed.webscraping.models import CareersPageScanResult, ScoredLinkCandidate

INCLUDE_GRADUATE_DEGREE_ROLES_CONFIG_KEY = "include_graduate_degree_roles"
INCLUDE_HARDWARE_ROLES_CONFIG_KEY = "include_hardware_roles"
REQUIRE_SOFTWARE_KEYWORDS_CONFIG_KEY = "require_software_keywords"
INTERNSHIP_MODE_CONFIG_KEY = "internship_mode"
LOCATION_FILTER_CONFIG_KEY = "location_filter"
LOCATION_FILTER_VALUES = {"all", "canada", "usa", "north_america", "international"}
APPLICATION_STATUSES = (
    RoleStatus.APPLIED,
    RoleStatus.OA,
    RoleStatus.INTERVIEW,
    RoleStatus.REJECTED,
    RoleStatus.OFFER,
)
REVIEW_LATER_EVENT_TYPE = "review_later"
MASTER_RESUME_ID = 1
RESUME_FEEDBACK_HISTORY_LIMIT = 50
RESUME_FEEDBACK_SIMILARITY_THRESHOLD = 0.12
RESUME_FEEDBACK_RESPONSE_VALUES = {"accepted", "ignored"}
_VECTOR_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#.-]{2,}")
_VECTOR_STOP_WORDS = {
    "and",
    "are",
    "for",
    "from",
    "job",
    "resume",
    "role",
    "that",
    "the",
    "this",
    "with",
}


def _lastrowid(cursor: turso.Cursor) -> int:
    if cursor.lastrowid is None:
        raise RuntimeError("database did not return a row id")
    return cursor.lastrowid


def add_company(connection: turso.Connection, company: Company) -> Company:
    if _companies_has_legacy_careers_url(connection):
        cursor = connection.execute(
            """
            INSERT INTO companies (
                name,
                careers_url,
                notes,
                prestige_tier,
                is_active,
                browser_extra_wait_ms,
                central_company_id,
                canonical_domain,
                normalized_name,
                central_sync_status,
                central_sync_error,
                central_matched_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company.name,
                "",
                company.notes,
                company.prestige_tier,
                int(company.is_active),
                company.browser_extra_wait_ms,
                company.central_company_id,
                company.canonical_domain,
                company.normalized_name,
                company.central_sync_status,
                company.central_sync_error,
                company.central_matched_at.isoformat()
                if company.central_matched_at is not None
                else None,
            ),
        )
        connection.commit()
        return get_company(connection, _lastrowid(cursor))

    cursor = connection.execute(
        """
        INSERT INTO companies (
            name,
            notes,
            prestige_tier,
            is_active,
            browser_extra_wait_ms,
            central_company_id,
            canonical_domain,
            normalized_name,
            central_sync_status,
            central_sync_error,
            central_matched_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company.name,
            company.notes,
            company.prestige_tier,
            int(company.is_active),
            company.browser_extra_wait_ms,
            company.central_company_id,
            company.canonical_domain,
            company.normalized_name,
            company.central_sync_status,
            company.central_sync_error,
            company.central_matched_at.isoformat()
            if company.central_matched_at is not None
            else None,
        ),
    )
    connection.commit()
    return get_company(connection, _lastrowid(cursor))


def _companies_has_legacy_careers_url(connection: turso.Connection) -> bool:
    rows = connection.execute("PRAGMA table_info(companies)").fetchall()
    return any(row["name"] == "careers_url" for row in rows)


def set_config_value(connection: turso.Connection, key: str, value: str) -> None:
    connection.execute(
        """
        INSERT INTO app_config (key, value, updated_at)
        VALUES (?, ?, datetime('now'))
        ON CONFLICT(key) DO UPDATE SET
            value = excluded.value,
            updated_at = datetime('now')
        """,
        (key, value),
    )
    connection.commit()


def get_config_value(connection: turso.Connection, key: str) -> str | None:
    row = connection.execute(
        """
        SELECT value
        FROM app_config
        WHERE key = ?
        """,
        (key,),
    ).fetchone()
    if row is None:
        return None
    return str(row["value"])


def list_config_values(connection: turso.Connection) -> dict[str, str]:
    rows = connection.execute(
        """
        SELECT key, value
        FROM app_config
        ORDER BY key
        """
    ).fetchall()
    return {str(row["key"]): str(row["value"]) for row in rows}


def delete_config_value(connection: turso.Connection, key: str) -> None:
    connection.execute(
        """
        DELETE FROM app_config
        WHERE key = ?
        """,
        (key,),
    )
    connection.commit()


def record_resume_feedback_history(
    connection: turso.Connection,
    *,
    role: Role,
    feedback_index: int,
    feedback: dict[str, object],
    response: str,
    comment: str | None = None,
) -> int:
    if response not in RESUME_FEEDBACK_RESPONSE_VALUES:
        raise ValueError("feedback response must be accepted or ignored")
    title = _feedback_text(feedback.get("title")) or "untitled feedback"
    detail = _feedback_text(feedback.get("detail")) or ""
    label = _feedback_text(feedback.get("label"))
    cleaned_comment = comment.strip() if isinstance(comment, str) else None
    if cleaned_comment == "":
        cleaned_comment = None
    knowledge_text = _resume_feedback_knowledge_text(
        role=role,
        feedback_title=title,
        feedback_detail=detail,
        response=response,
        comment=cleaned_comment,
    )
    cursor = connection.execute(
        """
        INSERT INTO resume_feedback_history (
            role_id,
            company_id,
            role_title,
            role_url,
            role_description,
            feedback_index,
            feedback_label,
            feedback_title,
            feedback_detail,
            target_text,
            replacement_text,
            latex_addition,
            response,
            comment,
            knowledge_text,
            vector_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            role.id,
            role.company_id,
            role.title,
            role.role_url,
            role.description,
            feedback_index,
            label,
            title,
            detail,
            _feedback_text(feedback.get("target_text")),
            _feedback_text(feedback.get("replacement_text")),
            _feedback_text(feedback.get("latex_addition")),
            response,
            cleaned_comment,
            knowledge_text,
            json.dumps(_text_vector(knowledge_text), sort_keys=True),
        ),
    )
    connection.commit()
    return _lastrowid(cursor)


def list_resume_feedback_knowledge(
    connection: turso.Connection,
    *,
    role: Role | dict[str, object],
    resume_content: str,
    limit: int = 5,
) -> list[dict[str, object]]:
    role_title = _role_value(role, "title")
    role_description = _role_value(role, "description")
    role_location = _role_value(role, "location")
    query_vector = _text_vector(" ".join([role_title, role_description, role_location]))
    rows = connection.execute(
        """
        SELECT
            id,
            role_id,
            role_title,
            feedback_title,
            feedback_detail,
            response,
            comment,
            knowledge_text,
            created_at
        FROM resume_feedback_history
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (RESUME_FEEDBACK_HISTORY_LIMIT,),
    ).fetchall()
    matches: list[dict[str, object]] = []
    for row in rows:
        row_dict = dict(row)
        preference_summary = _resume_feedback_preference_summary(
            role_title=str(row_dict["role_title"] or ""),
            feedback_title=str(row_dict["feedback_title"] or ""),
            feedback_detail=str(row_dict["feedback_detail"] or ""),
            response=str(row_dict["response"] or ""),
            comment=row_dict["comment"] if isinstance(row_dict["comment"], str) else None,
        )
        similarity = _cosine_similarity(query_vector, _text_vector(preference_summary))
        if similarity < RESUME_FEEDBACK_SIMILARITY_THRESHOLD:
            continue
        matches.append(
            {
                "id": row_dict["id"],
                "role_id": row_dict["role_id"],
                "role_title": row_dict["role_title"],
                "feedback_title": row_dict["feedback_title"],
                "feedback_detail": row_dict["feedback_detail"],
                "response": row_dict["response"],
                "comment": row_dict["comment"],
                "knowledge_text": preference_summary,
                "preference_summary": preference_summary,
                "created_at": row_dict["created_at"],
                "similarity": similarity,
            }
        )
    matches.sort(
        key=lambda item: (_similarity_value(item), str(item["created_at"])),
        reverse=True,
    )
    return matches[:limit]


def count_resume_feedback_history(connection: turso.Connection) -> int:
    row = connection.execute("SELECT COUNT(*) AS count FROM resume_feedback_history").fetchone()
    return int(row["count"]) if row is not None else 0


def clear_resume_feedback_history(connection: turso.Connection) -> int:
    deleted_count = count_resume_feedback_history(connection)
    connection.execute("DELETE FROM resume_feedback_history")
    connection.commit()
    return deleted_count


def _resume_feedback_knowledge_text(
    *,
    role: Role,
    feedback_title: str,
    feedback_detail: str,
    response: str,
    comment: str | None,
) -> str:
    return _resume_feedback_preference_summary(
        role_title=role.title,
        feedback_title=feedback_title,
        feedback_detail=feedback_detail,
        response=response,
        comment=comment,
    )


def _resume_feedback_preference_summary(
    *,
    role_title: str,
    feedback_title: str,
    feedback_detail: str,
    response: str,
    comment: str | None,
) -> str:
    parts = [
        f"user {response} resume feedback",
        f"role title: {role_title}",
        f"feedback: {feedback_title}",
        f"detail: {feedback_detail}",
    ]
    if comment:
        parts.append(f"user comment: {comment}")
    return "\n".join(parts)


def _feedback_text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def _similarity_value(item: dict[str, object]) -> float:
    value = item.get("similarity")
    return value if isinstance(value, float) else 0.0


def _role_value(role: Role | dict[str, object], field: str) -> str:
    value = role.get(field) if isinstance(role, dict) else getattr(role, field)
    return value if isinstance(value, str) else ""


def _text_vector(text: str) -> dict[str, int]:
    vector: dict[str, int] = {}
    for token in _VECTOR_TOKEN_RE.findall(text.lower()):
        if token in _VECTOR_STOP_WORDS:
            continue
        vector[token] = vector.get(token, 0) + 1
    return vector


def _load_vector(value: object) -> dict[str, int]:
    if not isinstance(value, str):
        return {}
    try:
        raw_vector = json.loads(value)
    except json.JSONDecodeError:
        return {}
    if not isinstance(raw_vector, dict):
        return {}
    return {
        str(token): int(count)
        for token, count in raw_vector.items()
        if isinstance(count, int | float)
    }


def sync_role_context_vectors(
    connection: turso.Connection,
    *,
    role: Role,
    company_name: str,
) -> bool:
    """Replace only one role's local retrieval projection when its source changes."""
    if role.id is None:
        raise ValueError("role context requires a persisted role id")
    chunks = _role_context_chunks(role, company_name=company_name)
    desired = [
        (label, content, hashlib.sha256(content.encode()).hexdigest()) for label, content in chunks
    ]
    existing_rows = connection.execute(
        """
        SELECT chunk_index, label, content_sha256
        FROM role_context_vectors
        WHERE role_id = ?
        ORDER BY chunk_index
        """,
        (role.id,),
    ).fetchall()
    existing = [(str(row["label"]), str(row["content_sha256"])) for row in existing_rows]
    if existing == [(label, digest) for label, _content, digest in desired]:
        return False
    connection.execute("DELETE FROM role_context_vectors WHERE role_id = ?", (role.id,))
    for chunk_index, (label, content, digest) in enumerate(desired):
        connection.execute(
            """
            INSERT INTO role_context_vectors (
                role_id, chunk_index, label, content, content_sha256, vector_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (
                role.id,
                chunk_index,
                label,
                content,
                digest,
                json.dumps(_text_vector(content), sort_keys=True),
            ),
        )
    connection.commit()
    return True


def retrieve_role_context(
    connection: turso.Connection,
    *,
    role_id: int,
    query: str,
    limit: int = 4,
) -> list[dict[str, object]]:
    """Retrieve local job context strictly scoped to one authoritative role ID."""
    if limit <= 0:
        return []
    query_vector = _text_vector(query)
    rows = connection.execute(
        """
        SELECT chunk_index, label, content, vector_json, updated_at
        FROM role_context_vectors
        WHERE role_id = ?
        ORDER BY chunk_index
        """,
        (role_id,),
    ).fetchall()
    ranked: list[dict[str, object]] = []
    for row in rows:
        item = dict(row)
        ranked.append(
            {
                "id": int(item["chunk_index"]),
                "filename": f"role-{role_id}-{item['label']}.txt",
                "label": item["label"],
                "content": item["content"],
                "similarity": _cosine_similarity(query_vector, _load_vector(item["vector_json"])),
                "updated_at": item["updated_at"],
            }
        )
    ranked.sort(key=_role_context_rank)
    return ranked[:limit]


def _role_context_rank(item: dict[str, object]) -> tuple[float, int]:
    similarity = item.get("similarity")
    chunk_index = item.get("id")
    return (
        -(similarity if isinstance(similarity, float) else 0.0),
        chunk_index if isinstance(chunk_index, int) else 0,
    )


def _role_context_chunks(role: Role, *, company_name: str) -> list[tuple[str, str]]:
    metadata = "\n".join(
        value
        for value in (
            "Role metadata",
            f"Company: {company_name}",
            f"Title: {role.title}",
            f"URL: {role.role_url}",
            f"Location: {role.location}" if role.location else "",
            f"Posting ID: {role.posting_id}" if role.posting_id else "",
            f"First seen: {role.first_seen_at}" if role.first_seen_at else "",
            f"Last seen: {role.last_seen_at}" if role.last_seen_at else "",
            f"Notes: {role.notes}" if role.notes else "",
        )
        if value
    )
    description = (role.description or "").strip()
    chunks: list[tuple[str, str]] = [("metadata", metadata)]
    if not description:
        return chunks
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", description) if part.strip()]
    current = ""
    part_index = 1
    for paragraph in paragraphs or [description]:
        while paragraph:
            capacity = 4_000 - len(current) - (2 if current else 0)
            if capacity <= 0:
                chunks.append((f"description-{part_index}", current))
                part_index += 1
                current = ""
                capacity = 4_000
            piece = paragraph[:capacity]
            paragraph = paragraph[capacity:].lstrip()
            current = f"{current}\n\n{piece}" if current else piece
            if len(current) >= 4_000:
                chunks.append((f"description-{part_index}", current))
                part_index += 1
                current = ""
    if current:
        chunks.append((f"description-{part_index}", current))
    return chunks


def _cosine_similarity(left: dict[str, int], right: dict[str, int]) -> float:
    if not left or not right:
        return 0.0
    dot = sum(count * right.get(token, 0) for token, count in left.items())
    if dot == 0:
        return 0.0
    left_norm = math.sqrt(sum(count * count for count in left.values()))
    right_norm = math.sqrt(sum(count * count for count in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def get_master_resume(connection: turso.Connection) -> MasterResume | None:
    row = connection.execute(
        """
        SELECT id, filename, content, content_sha256, created_at, updated_at
        FROM master_resumes
        WHERE id = ?
        """,
        (MASTER_RESUME_ID,),
    ).fetchone()
    if row is None:
        return None
    return MasterResume.model_validate(dict(row))


def upsert_master_resume(
    connection: turso.Connection,
    *,
    filename: str,
    content: str,
) -> MasterResume:
    cleaned_filename = PurePath(filename).name.strip()
    if not cleaned_filename.lower().endswith(".tex"):
        raise ValueError("master resume must be a .tex file")
    if not content.strip():
        raise ValueError("master resume content cannot be empty")

    content_sha256 = hashlib.sha256(content.encode()).hexdigest()
    connection.execute(
        """
        INSERT INTO master_resumes (
            id,
            filename,
            content,
            content_sha256
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            filename = excluded.filename,
            content = excluded.content,
            content_sha256 = excluded.content_sha256,
            updated_at = datetime('now')
        """,
        (MASTER_RESUME_ID, cleaned_filename, content, content_sha256),
    )
    connection.commit()
    resume = get_master_resume(connection)
    if resume is None:
        raise RuntimeError("stored master resume could not be loaded")
    return resume


def list_cover_letter_examples(connection: turso.Connection) -> list[CoverLetterExample]:
    rows = connection.execute(
        """
        SELECT id, filename, content, content_sha256, created_at, updated_at
        FROM cover_letter_examples
        ORDER BY updated_at DESC, id DESC
        """
    ).fetchall()
    return [CoverLetterExample.model_validate(dict(row)) for row in rows]


def get_cover_letter_example(
    connection: turso.Connection,
    example_id: int,
) -> CoverLetterExample | None:
    row = connection.execute(
        """
        SELECT id, filename, content, content_sha256, created_at, updated_at
        FROM cover_letter_examples
        WHERE id = ?
        """,
        (example_id,),
    ).fetchone()
    return CoverLetterExample.model_validate(dict(row)) if row is not None else None


def delete_cover_letter_example(connection: turso.Connection, example_id: int) -> bool:
    connection.execute(
        "DELETE FROM cover_letter_example_vectors WHERE cover_letter_example_id = ?",
        (example_id,),
    )
    cursor = connection.execute("DELETE FROM cover_letter_examples WHERE id = ?", (example_id,))
    connection.commit()
    return cursor.rowcount > 0


def add_cover_letter_example(
    connection: turso.Connection,
    *,
    filename: str,
    content: str,
) -> CoverLetterExample:
    cleaned_filename = PurePath(filename).name.strip()
    if not cleaned_filename:
        raise ValueError("cover letter example filename cannot be empty")
    if not content.strip():
        raise ValueError("cover letter example content cannot be empty")

    content_sha256 = hashlib.sha256(content.encode()).hexdigest()
    cursor = connection.execute(
        """
        INSERT INTO cover_letter_examples (
            filename,
            content,
            content_sha256
        )
        VALUES (?, ?, ?)
        """,
        (cleaned_filename, content, content_sha256),
    )
    connection.commit()
    row = connection.execute(
        """
        SELECT id, filename, content, content_sha256, created_at, updated_at
        FROM cover_letter_examples
        WHERE id = ?
        """,
        (_lastrowid(cursor),),
    ).fetchone()
    if row is None:
        raise RuntimeError("stored cover letter example could not be loaded")
    example = CoverLetterExample.model_validate(dict(row))
    _upsert_cover_letter_example_vector(connection, example)
    connection.commit()
    return example


def list_experience_notes(connection: turso.Connection) -> list[ExperienceNote]:
    rows = connection.execute(
        """
        SELECT id, filename, content, content_sha256, created_at, updated_at
        FROM experience_notes
        ORDER BY updated_at DESC, id DESC
        """
    ).fetchall()
    return [ExperienceNote.model_validate(dict(row)) for row in rows]


def get_experience_note(connection: turso.Connection, note_id: int) -> ExperienceNote | None:
    row = connection.execute(
        """
        SELECT id, filename, content, content_sha256, created_at, updated_at
        FROM experience_notes
        WHERE id = ?
        """,
        (note_id,),
    ).fetchone()
    return ExperienceNote.model_validate(dict(row)) if row is not None else None


def delete_experience_note(connection: turso.Connection, note_id: int) -> bool:
    cursor = connection.execute("DELETE FROM experience_notes WHERE id = ?", (note_id,))
    connection.commit()
    return cursor.rowcount > 0


def add_experience_note(
    connection: turso.Connection,
    *,
    filename: str,
    content: str,
) -> ExperienceNote:
    cleaned_filename = PurePath(filename).name.strip()
    if not cleaned_filename:
        raise ValueError("experience note filename cannot be empty")
    if not content.strip():
        raise ValueError("experience note content cannot be empty")

    content_sha256 = hashlib.sha256(content.encode()).hexdigest()
    cursor = connection.execute(
        """
        INSERT INTO experience_notes (
            filename,
            content,
            content_sha256
        )
        VALUES (?, ?, ?)
        """,
        (cleaned_filename, content, content_sha256),
    )
    connection.commit()
    row = connection.execute(
        """
        SELECT id, filename, content, content_sha256, created_at, updated_at
        FROM experience_notes
        WHERE id = ?
        """,
        (_lastrowid(cursor),),
    ).fetchone()
    if row is None:
        raise RuntimeError("stored experience note could not be loaded")
    return ExperienceNote.model_validate(dict(row))


def list_cover_letter_example_knowledge(
    connection: turso.Connection,
    *,
    query: str,
    limit: int = 5,
) -> list[dict[str, object]]:
    _backfill_cover_letter_example_vectors(connection)
    query_vector = _text_vector(query)
    rows = connection.execute(
        """
        SELECT
            cover_letter_examples.id,
            cover_letter_examples.filename,
            cover_letter_examples.content,
            cover_letter_example_vectors.knowledge_text,
            cover_letter_example_vectors.vector_json,
            cover_letter_example_vectors.updated_at
        FROM cover_letter_example_vectors
        JOIN cover_letter_examples
            ON cover_letter_examples.id = cover_letter_example_vectors.cover_letter_example_id
        ORDER BY cover_letter_example_vectors.updated_at DESC,
            cover_letter_examples.id DESC
        """
    ).fetchall()
    matches: list[dict[str, object]] = []
    for row in rows:
        row_dict = dict(row)
        similarity = _cosine_similarity(query_vector, _load_vector(row_dict["vector_json"]))
        matches.append(
            {
                "id": row_dict["id"],
                "filename": row_dict["filename"],
                "content": row_dict["content"],
                "knowledge_text": row_dict["knowledge_text"],
                "similarity": similarity,
            }
        )
    matches.sort(key=_similarity_value, reverse=True)
    return matches[:limit]


def _backfill_cover_letter_example_vectors(connection: turso.Connection) -> None:
    rows = connection.execute(
        """
        SELECT id, filename, content, content_sha256, created_at, updated_at
        FROM cover_letter_examples
        WHERE id NOT IN (
            SELECT cover_letter_example_id
            FROM cover_letter_example_vectors
        )
        """
    ).fetchall()
    for row in rows:
        _upsert_cover_letter_example_vector(
            connection,
            CoverLetterExample.model_validate(dict(row)),
        )
    if rows:
        connection.commit()


def _upsert_cover_letter_example_vector(
    connection: turso.Connection,
    example: CoverLetterExample,
) -> None:
    if example.id is None:
        return
    knowledge_text = "\n".join(
        [
            f"cover letter example: {example.filename}",
            example.content,
        ]
    )
    connection.execute(
        """
        INSERT INTO cover_letter_example_vectors (
            cover_letter_example_id,
            knowledge_text,
            vector_json,
            updated_at
        )
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(cover_letter_example_id) DO UPDATE SET
            knowledge_text = excluded.knowledge_text,
            vector_json = excluded.vector_json,
            updated_at = datetime('now')
        """,
        (
            example.id,
            knowledge_text,
            json.dumps(_text_vector(knowledge_text), sort_keys=True),
        ),
    )


def set_include_graduate_degree_roles(connection: turso.Connection, enabled: bool) -> None:
    set_config_value(
        connection,
        INCLUDE_GRADUATE_DEGREE_ROLES_CONFIG_KEY,
        "true" if enabled else "false",
    )


def should_include_graduate_degree_roles(connection: turso.Connection) -> bool:
    value = get_config_value(connection, INCLUDE_GRADUATE_DEGREE_ROLES_CONFIG_KEY)
    if value is None:
        return False
    return value.lower() in {"1", "true", "yes", "on"}


def set_include_hardware_roles(connection: turso.Connection, enabled: bool) -> None:
    set_config_value(
        connection,
        INCLUDE_HARDWARE_ROLES_CONFIG_KEY,
        "true" if enabled else "false",
    )


def should_include_hardware_roles(connection: turso.Connection) -> bool:
    value = get_config_value(connection, INCLUDE_HARDWARE_ROLES_CONFIG_KEY)
    if value is None:
        return False
    return value.lower() in {"1", "true", "yes", "on"}


def set_require_software_keywords(connection: turso.Connection, enabled: bool) -> None:
    set_config_value(
        connection,
        REQUIRE_SOFTWARE_KEYWORDS_CONFIG_KEY,
        "true" if enabled else "false",
    )


def should_require_software_keywords(connection: turso.Connection) -> bool:
    value = get_config_value(connection, REQUIRE_SOFTWARE_KEYWORDS_CONFIG_KEY)
    if value is None:
        return True
    return value.lower() in {"1", "true", "yes", "on"}


def set_internship_mode(connection: turso.Connection, enabled: bool) -> None:
    set_config_value(
        connection,
        INTERNSHIP_MODE_CONFIG_KEY,
        "true" if enabled else "false",
    )


def should_use_internship_mode(connection: turso.Connection) -> bool:
    value = get_config_value(connection, INTERNSHIP_MODE_CONFIG_KEY)
    if value is None:
        return True
    return value.lower() in {"1", "true", "yes", "on"}


def set_location_filter(connection: turso.Connection, value: str) -> None:
    cleaned_value = value.strip().lower().replace("-", "_")
    if cleaned_value not in LOCATION_FILTER_VALUES:
        expected_values = ", ".join(sorted(LOCATION_FILTER_VALUES))
        raise ValueError(f"location_filter must be one of: {expected_values}")
    set_config_value(connection, LOCATION_FILTER_CONFIG_KEY, cleaned_value)


def get_location_filter(connection: turso.Connection) -> str:
    value = get_config_value(connection, LOCATION_FILTER_CONFIG_KEY)
    if value is None:
        return "all"
    cleaned_value = value.strip().lower().replace("-", "_")
    if cleaned_value not in LOCATION_FILTER_VALUES:
        return "all"
    return cleaned_value


def get_company(connection: turso.Connection, company_id: int) -> Company:
    row = connection.execute(
        """
        SELECT
            id,
            name,
            created_at,
            updated_at,
            notes,
            prestige_tier,
            is_active,
            browser_extra_wait_ms,
            central_company_id,
            canonical_domain,
            normalized_name,
            central_sync_status,
            central_sync_error,
            central_matched_at
        FROM companies
        WHERE id = ?
        """,
        (company_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"company not found: {company_id}")
    return Company.model_validate(dict(row))


def list_companies(
    connection: turso.Connection,
    *,
    include_inactive: bool = False,
) -> list[Company]:
    where = "" if include_inactive else "WHERE is_active = 1"
    rows = connection.execute(
        f"""
        SELECT
            id,
            name,
            created_at,
            updated_at,
            notes,
            prestige_tier,
            is_active,
            browser_extra_wait_ms,
            central_company_id,
            canonical_domain,
            normalized_name,
            central_sync_status,
            central_sync_error,
            central_matched_at
        FROM companies
        {where}
        ORDER BY name
        """
    ).fetchall()
    return [Company.model_validate(dict(row)) for row in rows]


def list_companies_without_central_id(connection: turso.Connection) -> list[Company]:
    rows = connection.execute(
        """
        SELECT
            id,
            name,
            created_at,
            updated_at,
            notes,
            prestige_tier,
            is_active,
            browser_extra_wait_ms,
            central_company_id,
            canonical_domain,
            normalized_name,
            central_sync_status,
            central_sync_error,
            central_matched_at
        FROM companies
        WHERE central_company_id IS NULL
        ORDER BY name
        """
    ).fetchall()
    return [Company.model_validate(dict(row)) for row in rows]


def set_company_central_link(
    connection: turso.Connection,
    company_id: int,
    *,
    central_company_id: str,
    canonical_domain: str | None = None,
    normalized_name: str | None = None,
    prestige_tier: str | None = None,
) -> Company:
    connection.execute(
        """
        UPDATE companies
        SET
            central_company_id = ?,
            canonical_domain = COALESCE(?, canonical_domain),
            normalized_name = COALESCE(?, normalized_name),
            prestige_tier = COALESCE(?, prestige_tier),
            central_sync_status = 'linked',
            central_sync_error = NULL,
            central_matched_at = datetime('now'),
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (central_company_id, canonical_domain, normalized_name, prestige_tier, company_id),
    )
    connection.commit()
    return get_company(connection, company_id)


def set_company_central_sync_status(
    connection: turso.Connection,
    company_id: int,
    *,
    status: str,
    error: str | None = None,
) -> Company:
    if status not in {"pending", "linked", "needs_review", "failed"}:
        raise ValueError("central sync status must be pending, linked, needs_review, or failed")
    connection.execute(
        """
        UPDATE companies
        SET
            central_sync_status = ?,
            central_sync_error = ?,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (status, error, company_id),
    )
    connection.commit()
    return get_company(connection, company_id)


def update_company(
    connection: turso.Connection,
    company_id: int,
    *,
    notes: str | None = None,
    prestige_tier: str | None = None,
) -> Company:
    connection.execute(
        """
        UPDATE companies
        SET
            notes = ?,
            prestige_tier = ?,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (notes, prestige_tier, company_id),
    )
    connection.commit()
    return get_company(connection, company_id)


def deactivate_company(connection: turso.Connection, company_id: int) -> Company:
    get_company(connection, company_id)
    connection.execute(
        """
        UPDATE companies
        SET
            is_active = 0,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (company_id,),
    )
    connection.commit()
    return get_company(connection, company_id)


def increase_company_browser_wait(
    connection: turso.Connection,
    company_id: int,
    *,
    increment_ms: int = 1_000,
) -> Company:
    connection.execute(
        """
        UPDATE companies
        SET
            browser_extra_wait_ms = browser_extra_wait_ms + ?,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (increment_ms, company_id),
    )
    connection.commit()
    return get_company(connection, company_id)


def add_company_career_page(
    connection: turso.Connection,
    career_page: CompanyCareerPage,
) -> CompanyCareerPage:
    cursor = connection.execute(
        """
        INSERT INTO company_career_pages (company_id, url, label)
        VALUES (?, ?, ?)
        """,
        (
            career_page.company_id,
            career_page.url,
            career_page.label,
        ),
    )
    connection.commit()
    return get_company_career_page(connection, _lastrowid(cursor))


def delete_company_career_page(
    connection: turso.Connection,
    career_page_id: int,
) -> CompanyCareerPage:
    career_page = get_company_career_page(connection, career_page_id)
    connection.execute(
        """
        DELETE FROM company_career_pages
        WHERE id = ?
        """,
        (career_page_id,),
    )
    connection.commit()
    return career_page


def set_primary_company_career_page_url(
    connection: turso.Connection,
    company_id: int,
    url: str,
) -> CompanyCareerPage:
    career_pages = list_company_career_pages(connection, company_id)
    if not career_pages:
        return add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company_id, url=url, label="Main"),
        )

    primary_page = next(
        (page for page in career_pages if page.label and page.label.lower() == "main"),
        career_pages[0],
    )
    connection.execute(
        """
        UPDATE company_career_pages
        SET url = ?, updated_at = datetime('now')
        WHERE id = ?
        """,
        (url, primary_page.id),
    )
    connection.commit()
    if primary_page.id is None:
        raise RuntimeError("primary company career page did not include an id")
    return get_company_career_page(connection, primary_page.id)


def get_company_career_page(
    connection: turso.Connection,
    career_page_id: int,
) -> CompanyCareerPage:
    row = connection.execute(
        """
        SELECT id, company_id, url, label, created_at, updated_at
        FROM company_career_pages
        WHERE id = ?
        """,
        (career_page_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"company career page not found: {career_page_id}")
    return _career_page_from_row(row)


def list_company_career_pages(
    connection: turso.Connection,
    company_id: int,
) -> list[CompanyCareerPage]:
    rows = connection.execute(
        """
        SELECT id, company_id, url, label, created_at, updated_at
        FROM company_career_pages
        WHERE company_id = ?
        ORDER BY id
        """,
        (company_id,),
    ).fetchall()
    return [_career_page_from_row(row) for row in rows]


def list_company_career_pages_by_company(
    connection: turso.Connection,
) -> dict[int, list[CompanyCareerPage]]:
    rows = connection.execute(
        """
        SELECT id, company_id, url, label, created_at, updated_at
        FROM company_career_pages
        ORDER BY company_id, id
        """
    ).fetchall()
    pages_by_company: dict[int, list[CompanyCareerPage]] = {}
    for row in rows:
        page = _career_page_from_row(row)
        pages_by_company.setdefault(page.company_id, []).append(page)
    return pages_by_company


def _career_page_from_row(row: turso.Row) -> CompanyCareerPage:
    return CompanyCareerPage.model_validate(dict(row))


def add_role(connection: turso.Connection, role: Role) -> Role:
    cursor = connection.execute(
        """
        INSERT INTO roles (
            company_id,
            title,
            role_url,
            location,
            role_status,
            notes,
            description,
            posting_id,
            central_role_id,
            central_source,
            central_synced_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            role.company_id,
            role.title,
            role.role_url,
            role.location,
            role.role_status.value,
            role.notes,
            role.description,
            role.posting_id,
            role.central_role_id,
            role.central_source,
            role.central_synced_at.isoformat() if role.central_synced_at is not None else None,
        ),
    )
    connection.commit()
    return get_role(connection, _lastrowid(cursor))


def get_role(connection: turso.Connection, role_id: int) -> Role:
    row = connection.execute(
        """
        SELECT
            id,
            company_id,
            title,
            role_url,
            location,
            role_status,
            first_seen_at,
            last_seen_at,
            created_at,
            updated_at,
            notes,
            description,
            posting_id,
            central_role_id,
            central_source,
            central_synced_at
        FROM roles
        WHERE id = ?
        """,
        (role_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"role not found: {role_id}")
    return Role.model_validate(dict(row))


def get_role_by_company_url(
    connection: turso.Connection,
    company_id: int,
    role_url: str,
) -> Role | None:
    row = connection.execute(
        """
        SELECT
            id,
            company_id,
            title,
            role_url,
            location,
            role_status,
            first_seen_at,
            last_seen_at,
            created_at,
            updated_at,
            notes,
            description,
            posting_id,
            central_role_id,
            central_source,
            central_synced_at
        FROM roles
        WHERE company_id = ?
            AND role_url = ?
        """,
        (company_id, role_url),
    ).fetchone()
    if row is None:
        return None
    return Role.model_validate(dict(row))


def get_role_by_central_id(connection: turso.Connection, central_role_id: str) -> Role | None:
    row = connection.execute(
        """
        SELECT
            id,
            company_id,
            title,
            role_url,
            location,
            role_status,
            first_seen_at,
            last_seen_at,
            created_at,
            updated_at,
            notes,
            description,
            posting_id,
            central_role_id,
            central_source,
            central_synced_at
        FROM roles
        WHERE central_role_id = ?
        """,
        (central_role_id,),
    ).fetchone()
    if row is None:
        return None
    return Role.model_validate(dict(row))


def upsert_central_role(
    connection: turso.Connection,
    role: Role,
) -> tuple[Role, bool]:
    if role.central_role_id is None:
        raise ValueError("central role must include central_role_id")

    existing_by_central_id = get_role_by_central_id(connection, role.central_role_id)
    if existing_by_central_id is not None:
        updated = update_central_role_fields(
            connection,
            existing_by_central_id.id or 0,
            title=role.title,
            role_url=role.role_url,
            location=role.location,
            description=role.description,
            posting_id=role.posting_id,
            central_role_id=role.central_role_id,
            central_source=role.central_source,
        )
        return updated, False

    existing_by_url = get_role_by_company_url(connection, role.company_id, role.role_url)
    if existing_by_url is not None:
        updated = update_central_role_fields(
            connection,
            existing_by_url.id or 0,
            title=role.title,
            role_url=role.role_url,
            location=role.location,
            description=role.description,
            posting_id=role.posting_id,
            central_role_id=role.central_role_id,
            central_source=role.central_source,
        )
        return updated, False

    created = add_role(connection, role)
    connection.execute(
        """
        UPDATE roles
        SET central_synced_at = datetime('now')
        WHERE id = ?
        """,
        (created.id,),
    )
    connection.commit()
    return get_role(connection, created.id or 0), True


def clear_roles(connection: turso.Connection) -> int:
    row = connection.execute("SELECT COUNT(*) AS count FROM roles").fetchone()
    role_count = int(row["count"]) if row is not None else 0
    connection.execute("DELETE FROM events WHERE role_id IS NOT NULL")
    connection.execute("UPDATE role_discovery_attempts SET role_id = NULL")
    connection.execute("DELETE FROM roles")
    connection.commit()
    return role_count


def update_central_role_fields(
    connection: turso.Connection,
    role_id: int,
    *,
    title: str,
    role_url: str,
    location: str | None,
    description: str | None,
    posting_id: str | None,
    central_role_id: str,
    central_source: str = "central",
) -> Role:
    connection.execute(
        """
        UPDATE roles
        SET
            title = ?,
            role_url = ?,
            location = ?,
            description = ?,
            posting_id = ?,
            central_role_id = ?,
            central_source = ?,
            central_synced_at = datetime('now'),
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (
            title,
            role_url,
            location,
            description,
            posting_id,
            central_role_id,
            central_source,
            role_id,
        ),
    )
    connection.commit()
    return get_role(connection, role_id)


def update_role(
    connection: turso.Connection,
    role_id: int,
    *,
    title: str | None = None,
    role_url: str | None = None,
    location: str | None = None,
    notes: str | None = None,
    description: str | None = None,
    posting_id: str | None = None,
    clear_location: bool = False,
    clear_notes: bool = False,
    touch_last_seen: bool = False,
) -> Role:
    assignments = []
    values: list[object] = []
    if title is not None:
        assignments.append("title = ?")
        values.append(title)
    if role_url is not None:
        assignments.append("role_url = ?")
        values.append(role_url)
    if clear_location:
        assignments.append("location = NULL")
    elif location is not None:
        assignments.append("location = ?")
        values.append(location)
    if clear_notes:
        assignments.append("notes = NULL")
    elif notes is not None:
        assignments.append("notes = ?")
        values.append(notes)
    if description is not None:
        assignments.append("description = ?")
        values.append(description)
    if posting_id is not None:
        assignments.append("posting_id = ?")
        values.append(posting_id)
    if touch_last_seen:
        assignments.append("last_seen_at = datetime('now')")

    if not assignments:
        return get_role(connection, role_id)

    assignments.append("updated_at = datetime('now')")
    values.append(role_id)
    connection.execute(
        f"""
        UPDATE roles
        SET {", ".join(assignments)}
        WHERE id = ?
        """,
        values,
    )
    connection.commit()
    return get_role(connection, role_id)


def list_roles(
    connection: turso.Connection,
    *,
    company_id: int | None = None,
    role_status: RoleStatus | None = None,
) -> list[Role]:
    clauses = []
    values: list[object] = []
    if company_id is not None:
        clauses.append("company_id = ?")
        values.append(company_id)
    if role_status is not None:
        clauses.append("role_status = ?")
        values.append(role_status.value)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = connection.execute(
        f"""
        SELECT
            id,
            company_id,
            title,
            role_url,
            location,
            role_status,
            first_seen_at,
            last_seen_at,
            created_at,
            updated_at,
            notes,
            description,
            posting_id,
            central_role_id,
            central_source,
            central_synced_at
        FROM roles
        {where}
        ORDER BY updated_at DESC, id DESC
        """,
        values,
    ).fetchall()
    return [Role.model_validate(dict(row)) for row in rows]


def list_role_items(
    connection: turso.Connection,
    *,
    company_id: int | None = None,
    company: str | None = None,
    role_status: RoleStatus | None = None,
    title: str | None = None,
    link: str | None = None,
    location: str | None = None,
    query: str | None = None,
) -> list[RoleListItem]:
    clauses = []
    values: list[object] = []
    if company_id is not None:
        clauses.append("roles.company_id = ?")
        values.append(company_id)
    if role_status is not None:
        clauses.append("roles.role_status = ?")
        values.append(role_status.value)
    if company:
        clauses.append("LOWER(companies.name) LIKE ?")
        values.append(f"%{company.lower()}%")
    if title:
        clauses.append("LOWER(roles.title) LIKE ?")
        values.append(f"%{title.lower()}%")
    if link:
        clauses.append("LOWER(roles.role_url) LIKE ?")
        values.append(f"%{link.lower()}%")
    if location:
        clauses.append("LOWER(roles.location) LIKE ?")
        values.append(f"%{location.lower()}%")
    if query:
        clauses.append(
            """
            (
                LOWER(roles.title) LIKE ?
                OR LOWER(companies.name) LIKE ?
                OR LOWER(roles.role_url) LIKE ?
                OR LOWER(roles.location) LIKE ?
                OR LOWER(roles.role_status) LIKE ?
            )
            """
        )
        query_like = f"%{query.lower()}%"
        values.extend([query_like, query_like, query_like, query_like, query_like])

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = connection.execute(
        f"""
        SELECT
            roles.id,
            roles.company_id,
            companies.name AS company_name,
            roles.title,
            roles.role_url,
            roles.location,
            roles.role_status,
            roles.first_seen_at,
            roles.last_seen_at,
            roles.created_at,
            roles.updated_at,
            roles.notes,
            roles.description,
            roles.posting_id,
            roles.central_role_id,
            roles.central_source,
            roles.central_synced_at,
            COUNT(review_later_events.id) AS review_later_count
        FROM roles
        JOIN companies ON companies.id = roles.company_id
        LEFT JOIN events AS review_later_events
            ON review_later_events.role_id = roles.id
            AND review_later_events.event_type = ?
        {where}
        GROUP BY
            roles.id,
            roles.company_id,
            companies.name,
            roles.title,
            roles.role_url,
            roles.location,
            roles.role_status,
            roles.first_seen_at,
            roles.last_seen_at,
            roles.created_at,
            roles.updated_at,
            roles.notes,
            roles.description,
            roles.posting_id,
            roles.central_role_id,
            roles.central_source,
            roles.central_synced_at
        ORDER BY roles.updated_at DESC, roles.id DESC
        """,
        [REVIEW_LATER_EVENT_TYPE, *values],
    ).fetchall()
    return [RoleListItem.model_validate(dict(row)) for row in rows]


def get_tracking_stats(connection: turso.Connection) -> dict[str, object]:
    company_row = connection.execute(
        "SELECT COUNT(*) AS count FROM companies WHERE is_active = 1"
    ).fetchone()
    company_count = int(company_row["count"]) if company_row is not None else 0

    role_rows = connection.execute(
        """
        SELECT role_status, COUNT(*) AS count
        FROM roles
        GROUP BY role_status
        """
    ).fetchall()
    jobs_by_status = {status.value: 0 for status in RoleStatus}
    for row in role_rows:
        jobs_by_status[str(row["role_status"])] = int(row["count"])

    application_status_values = {status.value for status in APPLICATION_STATUSES}
    applications_by_status = {
        status: count
        for status, count in jobs_by_status.items()
        if status in application_status_values
    }

    return {
        "companies_total": company_count,
        "jobs_total": sum(jobs_by_status.values()),
        "applications_total": sum(applications_by_status.values()),
        "jobs_by_status": jobs_by_status,
        "applications_by_status": applications_by_status,
    }


def set_role_status(
    connection: turso.Connection,
    role_id: int,
    new_status: RoleStatus,
    *,
    summary: str,
    source: EventSource = EventSource.MANUAL,
) -> Role:
    old_role = get_role(connection, role_id)
    connection.execute(
        """
        UPDATE roles
        SET role_status = ?, updated_at = datetime('now')
        WHERE id = ?
        """,
        (new_status.value, role_id),
    )
    add_event(
        connection,
        Event(
            company_id=old_role.company_id,
            role_id=role_id,
            event_type="status_changed",
            old_status=old_role.role_status,
            new_status=new_status,
            source=source,
            summary=summary,
        ),
    )
    connection.commit()
    return get_role(connection, role_id)


def set_role_status_if_changed(
    connection: turso.Connection,
    role_id: int,
    new_status: RoleStatus,
    *,
    summary: str,
    source: EventSource = EventSource.MANUAL,
) -> Role:
    """Atomically change a role status once, even under repeated requests."""
    try:
        connection.execute("BEGIN IMMEDIATE")
        old_role = get_role(connection, role_id)
        if old_role.role_status == new_status:
            connection.commit()
            return old_role
        connection.execute(
            """
            UPDATE roles
            SET role_status = ?, updated_at = datetime('now')
            WHERE id = ?
            """,
            (new_status.value, role_id),
        )
        add_event(
            connection,
            Event(
                company_id=old_role.company_id,
                role_id=role_id,
                event_type="status_changed",
                old_status=old_role.role_status,
                new_status=new_status,
                source=source,
                summary=summary,
            ),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    return get_role(connection, role_id)


def record_role_review_later(
    connection: turso.Connection,
    role_id: int,
    *,
    summary: str = "Review postponed from tracker.",
) -> Role:
    role = get_role(connection, role_id)
    add_event(
        connection,
        Event(
            company_id=role.company_id,
            role_id=role_id,
            event_type=REVIEW_LATER_EVENT_TYPE,
            source=EventSource.MANUAL,
            summary=summary,
        ),
    )
    connection.commit()
    return role


def create_scan_run(connection: turso.Connection, company_id: int) -> ScanRun:
    cursor = connection.execute(
        """
        INSERT INTO scan_runs (company_id)
        VALUES (?)
        """,
        (company_id,),
    )
    connection.commit()
    return get_scan_run(connection, _lastrowid(cursor))


def finish_scan_run(
    connection: turso.Connection,
    scan_run_id: int,
    scan_status: ScanStatus,
    *,
    error: str | None = None,
    agent_trace: str | None = None,
) -> ScanRun:
    connection.execute(
        """
        UPDATE scan_runs
        SET
            scan_status = ?,
            finished_at = datetime('now'),
            error = ?,
            agent_trace = ?
        WHERE id = ?
        """,
        (scan_status.value, error, agent_trace, scan_run_id),
    )
    connection.commit()
    return get_scan_run(connection, scan_run_id)


def get_scan_run(connection: turso.Connection, scan_run_id: int) -> ScanRun:
    row = connection.execute(
        """
        SELECT
            id,
            company_id,
            started_at,
            finished_at,
            scan_status,
            error,
            created_at,
            agent_trace
        FROM scan_runs
        WHERE id = ?
        """,
        (scan_run_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"scan run not found: {scan_run_id}")
    return ScanRun.model_validate(dict(row))


def list_scan_runs(
    connection: turso.Connection,
    *,
    company_id: int | None = None,
    limit: int = 10,
) -> list[ScanRunListItem]:
    clauses = []
    values: list[object] = []
    if company_id is not None:
        clauses.append("scan_runs.company_id = ?")
        values.append(company_id)
    values.append(limit)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = connection.execute(
        f"""
        SELECT
            scan_runs.id,
            scan_runs.company_id,
            companies.name AS company_name,
            scan_runs.started_at,
            scan_runs.finished_at,
            scan_runs.scan_status,
            scan_runs.error,
            scan_runs.created_at,
            scan_runs.agent_trace
        FROM scan_runs
        JOIN companies ON companies.id = scan_runs.company_id
        {where}
        ORDER BY scan_runs.started_at DESC, scan_runs.id DESC
        LIMIT ?
        """,
        values,
    ).fetchall()
    return [ScanRunListItem.model_validate(dict(row)) for row in rows]


def get_latest_scan_role_presence(
    connection: turso.Connection,
    company_ids: set[int],
) -> dict[int, tuple[int, set[int], set[str]]]:
    if not company_ids:
        return {}
    placeholders = ", ".join("?" for _ in company_ids)
    latest_rows = connection.execute(
        f"""
        WITH ranked_scan_runs AS (
            SELECT
                id,
                company_id,
                ROW_NUMBER() OVER (
                    PARTITION BY company_id
                    ORDER BY started_at DESC, id DESC
                ) AS position
            FROM scan_runs
            WHERE company_id IN ({placeholders})
        )
        SELECT id, company_id
        FROM ranked_scan_runs
        WHERE position = 1
        """,
        sorted(company_ids),
    ).fetchall()
    scan_id_to_company = {int(row["id"]): int(row["company_id"]) for row in latest_rows}
    presence: dict[int, tuple[int, set[int], set[str]]] = {
        company_id: (scan_id, set(), set())
        for scan_id, company_id in scan_id_to_company.items()
    }
    if not scan_id_to_company:
        return presence

    scan_placeholders = ", ".join("?" for _ in scan_id_to_company)
    scan_ids = sorted(scan_id_to_company)
    attempt_rows = connection.execute(
        f"""
        SELECT scan_run_id, role_id
        FROM role_discovery_attempts
        WHERE scan_run_id IN ({scan_placeholders})
          AND role_id IS NOT NULL
        """,
        scan_ids,
    ).fetchall()
    for row in attempt_rows:
        company_id = scan_id_to_company[int(row["scan_run_id"])]
        presence[company_id][1].add(int(row["role_id"]))

    candidate_rows = connection.execute(
        f"""
        SELECT scan_pages.scan_run_id, scan_candidates.url
        FROM scan_pages
        JOIN scan_candidates ON scan_candidates.scan_page_id = scan_pages.id
        WHERE scan_pages.scan_run_id IN ({scan_placeholders})
        """,
        scan_ids,
    ).fetchall()
    for row in candidate_rows:
        company_id = scan_id_to_company[int(row["scan_run_id"])]
        presence[company_id][2].add(str(row["url"]))
    return presence


def get_company_scan_discovery_counts(
    connection: turso.Connection,
) -> dict[int, tuple[int, int]]:
    rows = connection.execute(
        """
        SELECT
            scan_runs.company_id,
            COUNT(DISTINCT scan_runs.id) AS scan_count,
            COUNT(DISTINCT CASE WHEN scan_candidates.selected = 1 THEN scan_candidates.id END)
                AS discovered_role_count
        FROM scan_runs
        LEFT JOIN scan_pages ON scan_pages.scan_run_id = scan_runs.id
        LEFT JOIN scan_candidates ON scan_candidates.scan_page_id = scan_pages.id
        GROUP BY scan_runs.company_id
        """
    ).fetchall()
    return {
        int(row["company_id"]): (int(row["scan_count"]), int(row["discovered_role_count"]))
        for row in rows
    }


def add_scan_page(
    connection: turso.Connection,
    scan_run_id: int,
    result: CareersPageScanResult,
    *,
    company_career_page_id: int | None = None,
) -> ScanPage:
    cursor = connection.execute(
        """
        INSERT INTO scan_pages (
            scan_run_id,
            company_career_page_id,
            source_url,
            final_url,
            title,
            candidates_scanned,
            confidence
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            scan_run_id,
            company_career_page_id,
            result.source_url,
            result.final_url,
            result.title,
            result.candidates_scanned,
            result.confidence.value,
        ),
    )
    connection.commit()
    return get_scan_page(connection, _lastrowid(cursor))


def get_scan_page(connection: turso.Connection, scan_page_id: int) -> ScanPage:
    row = connection.execute(
        """
        SELECT
            id,
            scan_run_id,
            company_career_page_id,
            source_url,
            final_url,
            title,
            candidates_scanned,
            confidence,
            created_at
        FROM scan_pages
        WHERE id = ?
        """,
        (scan_page_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"scan page not found: {scan_page_id}")
    return ScanPage.model_validate(dict(row))


def list_scan_pages(connection: turso.Connection, scan_run_id: int) -> list[ScanPage]:
    rows = connection.execute(
        """
        SELECT
            id,
            scan_run_id,
            company_career_page_id,
            source_url,
            final_url,
            title,
            candidates_scanned,
            confidence,
            created_at
        FROM scan_pages
        WHERE scan_run_id = ?
        ORDER BY id
        """,
        (scan_run_id,),
    ).fetchall()
    return [ScanPage.model_validate(dict(row)) for row in rows]


def add_scan_candidates(
    connection: turso.Connection,
    scan_page_id: int,
    candidates: list[ScoredLinkCandidate],
    result: CareersPageScanResult,
) -> list[ScanCandidate]:
    selected_links = {link.url: link for link in result.links}
    created_candidates = []
    for candidate in candidates:
        selected_link = selected_links.get(candidate.url)
        cursor = connection.execute(
            """
            INSERT INTO scan_candidates (
                scan_page_id,
                url,
                source_url,
                text,
                tag,
                css_id,
                css_classes_json,
                aria_label,
                title,
                surrounding_text,
                confidence,
                reasons_json,
                selected,
                discovery_method
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                scan_page_id,
                candidate.url,
                candidate.source_url,
                candidate.text,
                candidate.tag,
                candidate.css_id,
                json.dumps(list(candidate.css_classes)),
                candidate.aria_label,
                candidate.title,
                candidate.surrounding_text,
                candidate.confidence,
                json.dumps(candidate.reasons),
                1 if selected_link is not None else 0,
                selected_link.discovery_method if selected_link is not None else None,
            ),
        )
        created_candidates.append(get_scan_candidate(connection, _lastrowid(cursor)))
    connection.commit()
    return created_candidates


def get_scan_candidate(connection: turso.Connection, scan_candidate_id: int) -> ScanCandidate:
    row = connection.execute(
        """
        SELECT
            id,
            scan_page_id,
            url,
            source_url,
            text,
            tag,
            css_id,
            css_classes_json,
            aria_label,
            title,
            surrounding_text,
            confidence,
            reasons_json,
            selected,
            discovery_method,
            created_at
        FROM scan_candidates
        WHERE id = ?
        """,
        (scan_candidate_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"scan candidate not found: {scan_candidate_id}")
    return _scan_candidate_from_row(row)


def list_scan_candidates(connection: turso.Connection, scan_page_id: int) -> list[ScanCandidate]:
    rows = connection.execute(
        """
        SELECT
            id,
            scan_page_id,
            url,
            source_url,
            text,
            tag,
            css_id,
            css_classes_json,
            aria_label,
            title,
            surrounding_text,
            confidence,
            reasons_json,
            selected,
            discovery_method,
            created_at
        FROM scan_candidates
        WHERE scan_page_id = ?
        ORDER BY confidence DESC, id
        """,
        (scan_page_id,),
    ).fetchall()
    return [_scan_candidate_from_row(row) for row in rows]


def _scan_candidate_from_row(row: turso.Row) -> ScanCandidate:
    candidate = dict(row)
    candidate["css_classes"] = tuple(json.loads(candidate.pop("css_classes_json")))
    candidate["reasons"] = json.loads(candidate.pop("reasons_json"))
    candidate["selected"] = bool(candidate["selected"])
    return ScanCandidate.model_validate(candidate)


def add_role_discovery_attempt(
    connection: turso.Connection,
    attempt: RoleDiscoveryAttempt,
) -> RoleDiscoveryAttempt:
    cursor = connection.execute(
        """
        INSERT INTO role_discovery_attempts (
            scan_run_id,
            scan_candidate_id,
            company_id,
            role_id,
            url,
            final_url,
            title,
            visible_text_excerpt,
            assessment_is_role,
            assessment_is_closed,
            assessment_confidence,
            assessment_location,
            assessment_description,
            assessment_posting_id,
            assessment_extraction_method,
            assessment_rejection_reason,
            assessment_reasons_json,
            status,
            error
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            attempt.scan_run_id,
            attempt.scan_candidate_id,
            attempt.company_id,
            attempt.role_id,
            attempt.url,
            attempt.final_url,
            attempt.title,
            attempt.visible_text_excerpt,
            _optional_bool_to_int(attempt.assessment_is_role),
            _optional_bool_to_int(attempt.assessment_is_closed),
            attempt.assessment_confidence,
            attempt.assessment_location,
            attempt.assessment_description,
            attempt.assessment_posting_id,
            attempt.assessment_extraction_method,
            attempt.assessment_rejection_reason,
            json.dumps(attempt.assessment_reasons),
            attempt.status.value,
            attempt.error,
        ),
    )
    connection.commit()
    return get_role_discovery_attempt(connection, _lastrowid(cursor))


def get_role_discovery_attempt(
    connection: turso.Connection,
    attempt_id: int,
) -> RoleDiscoveryAttempt:
    row = connection.execute(
        """
        SELECT
            id,
            scan_run_id,
            scan_candidate_id,
            company_id,
            role_id,
            url,
            final_url,
            title,
            visible_text_excerpt,
            assessment_is_role,
            assessment_is_closed,
            assessment_confidence,
            assessment_location,
            assessment_description,
            assessment_posting_id,
            assessment_extraction_method,
            assessment_rejection_reason,
            assessment_reasons_json,
            status,
            error,
            created_at
        FROM role_discovery_attempts
        WHERE id = ?
        """,
        (attempt_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"role discovery attempt not found: {attempt_id}")
    return _role_discovery_attempt_from_row(row)


def list_role_discovery_attempts(
    connection: turso.Connection,
    *,
    scan_run_id: int | None = None,
    scan_candidate_id: int | None = None,
) -> list[RoleDiscoveryAttempt]:
    clauses = []
    values: list[object] = []
    if scan_run_id is not None:
        clauses.append("scan_run_id = ?")
        values.append(scan_run_id)
    if scan_candidate_id is not None:
        clauses.append("scan_candidate_id = ?")
        values.append(scan_candidate_id)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = connection.execute(
        f"""
        SELECT
            id,
            scan_run_id,
            scan_candidate_id,
            company_id,
            role_id,
            url,
            final_url,
            title,
            visible_text_excerpt,
            assessment_is_role,
            assessment_is_closed,
            assessment_confidence,
            assessment_location,
            assessment_description,
            assessment_posting_id,
            assessment_extraction_method,
            assessment_rejection_reason,
            assessment_reasons_json,
            status,
            error,
            created_at
        FROM role_discovery_attempts
        {where}
        ORDER BY id
        """,
        values,
    ).fetchall()
    return [_role_discovery_attempt_from_row(row) for row in rows]


def update_role_discovery_attempt_assessment(
    connection: turso.Connection,
    attempt_id: int,
    *,
    role_id: int | None,
    assessment_is_role: bool,
    assessment_confidence: float | None,
    assessment_location: str | None,
    assessment_description: str | None,
    assessment_rejection_reason: str | None,
    assessment_reasons: list[str],
) -> RoleDiscoveryAttempt:
    connection.execute(
        """
        UPDATE role_discovery_attempts
        SET
            role_id = ?,
            assessment_is_role = ?,
            assessment_confidence = ?,
            assessment_location = ?,
            assessment_description = ?,
            assessment_rejection_reason = ?,
            assessment_reasons_json = ?
        WHERE id = ?
        """,
        (
            role_id,
            _optional_bool_to_int(assessment_is_role),
            assessment_confidence,
            assessment_location,
            assessment_description,
            assessment_rejection_reason,
            json.dumps(assessment_reasons),
            attempt_id,
        ),
    )
    connection.commit()
    return get_role_discovery_attempt(connection, attempt_id)


def list_rejected_role_urls(connection: turso.Connection, company_id: int) -> set[str]:
    rows = connection.execute(
        """
        SELECT url, final_url
        FROM role_discovery_attempts
        WHERE company_id = ?
            AND status = ?
            AND assessment_is_role = 0
            AND (
                assessment_rejection_reason IS NULL
                OR assessment_rejection_reason NOT LIKE '%filtered by app config%'
            )
        """,
        (company_id, RoleDiscoveryStatus.SUCCEEDED.value),
    ).fetchall()
    urls: set[str] = set()
    for row in rows:
        if row["url"]:
            urls.add(row["url"])
        if row["final_url"]:
            urls.add(row["final_url"])
    return urls


def _role_discovery_attempt_from_row(row: turso.Row) -> RoleDiscoveryAttempt:
    attempt = dict(row)
    attempt["assessment_is_role"] = _optional_int_to_bool(attempt["assessment_is_role"])
    attempt["assessment_is_closed"] = _optional_int_to_bool(attempt["assessment_is_closed"])
    attempt["assessment_reasons"] = json.loads(attempt.pop("assessment_reasons_json"))
    return RoleDiscoveryAttempt.model_validate(attempt)


def _optional_bool_to_int(value: bool | None) -> int | None:
    if value is None:
        return None
    return 1 if value else 0


def _optional_int_to_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def add_event(connection: turso.Connection, event: Event) -> Event:
    cursor = connection.execute(
        """
        INSERT INTO events (
            company_id,
            role_id,
            event_type,
            old_status,
            new_status,
            source,
            summary
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event.company_id,
            event.role_id,
            event.event_type,
            event.old_status.value if event.old_status is not None else None,
            event.new_status.value if event.new_status is not None else None,
            event.source.value,
            event.summary,
        ),
    )
    connection.commit()
    return get_event(connection, _lastrowid(cursor))


def get_event(connection: turso.Connection, event_id: int) -> Event:
    row = connection.execute(
        """
        SELECT
            id,
            company_id,
            role_id,
            event_type,
            old_status,
            new_status,
            source,
            summary,
            created_at
        FROM events
        WHERE id = ?
        """,
        (event_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"event not found: {event_id}")
    return Event.model_validate(dict(row))


def list_role_events(connection: turso.Connection, role_id: int, *, limit: int = 5) -> list[Event]:
    rows = connection.execute(
        """
        SELECT
            id,
            company_id,
            role_id,
            event_type,
            old_status,
            new_status,
            source,
            summary,
            created_at
        FROM events
        WHERE role_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (role_id, limit),
    ).fetchall()
    return [Event.model_validate(dict(row)) for row in rows]
