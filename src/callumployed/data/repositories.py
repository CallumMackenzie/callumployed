import turso

from callumployed.data.models import Company, Event, EventSource, Role, RoleListItem, RoleStatus


def _lastrowid(cursor: turso.Cursor) -> int:
    if cursor.lastrowid is None:
        raise RuntimeError("database did not return a row id")
    return cursor.lastrowid


def add_company(connection: turso.Connection, company: Company) -> Company:
    cursor = connection.execute(
        """
        INSERT INTO companies (name, careers_url, notes, prestige_tier)
        VALUES (?, ?, ?, ?)
        """,
        (company.name, company.careers_url, company.notes, company.prestige_tier),
    )
    connection.commit()
    return get_company(connection, _lastrowid(cursor))


def get_company(connection: turso.Connection, company_id: int) -> Company:
    row = connection.execute(
        """
        SELECT id, name, careers_url, created_at, updated_at, notes, prestige_tier
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
        SELECT id, name, careers_url, created_at, updated_at, notes, prestige_tier
        FROM companies
        ORDER BY name
        """
    ).fetchall()
    return [Company.model_validate(dict(row)) for row in rows]


def add_role(connection: turso.Connection, role: Role) -> Role:
    cursor = connection.execute(
        """
        INSERT INTO roles (company_id, title, role_url, location, role_status, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            role.company_id,
            role.title,
            role.role_url,
            role.location,
            role.role_status.value,
            role.notes,
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
            notes
        FROM roles
        WHERE id = ?
        """,
        (role_id,),
    ).fetchone()
    if row is None:
        raise LookupError(f"role not found: {role_id}")
    return Role.model_validate(dict(row))


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
            notes
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
    role_status: RoleStatus | None = None,
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
    if location:
        clauses.append("LOWER(roles.location) LIKE ?")
        values.append(f"%{location.lower()}%")
    if query:
        clauses.append(
            """
            (
                LOWER(roles.title) LIKE ?
                OR LOWER(companies.name) LIKE ?
                OR LOWER(roles.location) LIKE ?
            )
            """
        )
        query_like = f"%{query.lower()}%"
        values.extend([query_like, query_like, query_like])

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
