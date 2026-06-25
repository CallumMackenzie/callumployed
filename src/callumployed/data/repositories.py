import json

import turso

from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    Event,
    EventSource,
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

EXTERNAL_BROWSER_PORT_CONFIG_KEY = "external_browser_port"
INCLUDE_GRADUATE_DEGREE_ROLES_CONFIG_KEY = "include_graduate_degree_roles"
INCLUDE_HARDWARE_ROLES_CONFIG_KEY = "include_hardware_roles"
REQUIRE_SOFTWARE_KEYWORDS_CONFIG_KEY = "require_software_keywords"


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
                external_browser_port
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                company.name,
                "",
                company.notes,
                company.prestige_tier,
                company.external_browser_port,
            ),
        )
        connection.commit()
        return get_company(connection, _lastrowid(cursor))

    cursor = connection.execute(
        """
        INSERT INTO companies (name, notes, prestige_tier, external_browser_port)
        VALUES (?, ?, ?, ?)
        """,
        (
            company.name,
            company.notes,
            company.prestige_tier,
            company.external_browser_port,
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


def set_default_external_browser_port(
    connection: turso.Connection,
    external_browser_port: int,
) -> None:
    set_config_value(
        connection,
        EXTERNAL_BROWSER_PORT_CONFIG_KEY,
        str(external_browser_port),
    )


def get_default_external_browser_port(connection: turso.Connection) -> int | None:
    value = get_config_value(connection, EXTERNAL_BROWSER_PORT_CONFIG_KEY)
    if value is None:
        return None
    return int(value)


def clear_default_external_browser_port(connection: turso.Connection) -> None:
    delete_config_value(connection, EXTERNAL_BROWSER_PORT_CONFIG_KEY)


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
            external_browser_port
        FROM companies
        WHERE id = ?
        """,
        (company_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"company not found: {company_id}")
    return Company.model_validate(dict(row))


def list_companies(connection: turso.Connection) -> list[Company]:
    rows = connection.execute(
        """
        SELECT
            id,
            name,
            created_at,
            updated_at,
            notes,
            prestige_tier,
            external_browser_port
        FROM companies
        ORDER BY name
        """
    ).fetchall()
    return [Company.model_validate(dict(row)) for row in rows]


def set_company_external_browser_port(
    connection: turso.Connection,
    company_id: int,
    external_browser_port: int | None,
) -> Company:
    connection.execute(
        """
        UPDATE companies
        SET external_browser_port = ?, updated_at = datetime('now')
        WHERE id = ?
        """,
        (external_browser_port, company_id),
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
            posting_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            posting_id
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
            posting_id
        FROM roles
        WHERE company_id = ?
            AND role_url = ?
        """,
        (company_id, role_url),
    ).fetchone()
    if row is None:
        return None
    return Role.model_validate(dict(row))


def clear_roles(connection: turso.Connection) -> int:
    row = connection.execute("SELECT COUNT(*) AS count FROM roles").fetchone()
    role_count = int(row["count"]) if row is not None else 0
    connection.execute("DELETE FROM events WHERE role_id IS NOT NULL")
    connection.execute("UPDATE role_discovery_attempts SET role_id = NULL")
    connection.execute("DELETE FROM roles")
    connection.commit()
    return role_count


def update_role(
    connection: turso.Connection,
    role_id: int,
    *,
    title: str | None = None,
    role_url: str | None = None,
    location: str | None = None,
    notes: str | None = None,
    clear_location: bool = False,
    clear_notes: bool = False,
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

    if not assignments:
        return get_role(connection, role_id)

    assignments.append("updated_at = datetime('now')")
    values.append(role_id)
    connection.execute(
        f"""
        UPDATE roles
        SET {', '.join(assignments)}
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
            posting_id
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
            roles.last_seen_at,
            roles.updated_at
        FROM roles
        JOIN companies ON companies.id = roles.company_id
        {where}
        ORDER BY roles.updated_at DESC, roles.id DESC
        """,
        values,
    ).fetchall()
    return [RoleListItem.model_validate(dict(row)) for row in rows]


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
