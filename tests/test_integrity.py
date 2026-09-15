from callumployed.central.normalization import (
    ats_slug,
    canonical_company_domain,
    canonical_role_url,
    role_identity,
)
from callumployed.data import db
from callumployed.data.integrity import CENTRAL_LINK_REPAIR_KEY, repair_local_integrity
from callumployed.data.models import Company, CompanyCareerPage, Role, RoleStatus
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    add_role,
    list_company_career_pages,
    list_roles,
)
from callumployed.services.autoprep import ensure_autoprep_schema


def test_shared_ats_normalization_and_role_identity() -> None:
    assert ats_slug("https://jobs.ashbyhq.com/cohere") == "ashby:cohere"
    assert (
        ats_slug("https://job-boards.greenhouse.io/aquaticcapitalmanagement")
        == "greenhouse:aquaticcapitalmanagement"
    )
    assert canonical_company_domain("https://jobs.ashbyhq.com/cohere") is None
    assert canonical_company_domain("https://example.com/careers") == "example.com"
    assert role_identity("https://jobs.ashbyhq.com/cohere/job-123") == ("ashby:cohere:job:job-123")
    assert role_identity("https://jobs.ashbyhq.com/cohere") is None


def test_canonical_role_url_retains_gh_jid_and_sorts_parameters() -> None:
    first = canonical_role_url(
        "https://example.com/jobs/?z=2&utm_source=test&gh_jid=123&a=1#details"
    )
    second = canonical_role_url("https://example.com/jobs?a=1&gh_jid=123&z=2")
    assert first == second
    assert "gh_jid=123" in first
    assert "utm_source" not in first


def test_local_repair_invalidates_links_and_removes_only_central_pages() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(
        connection,
        Company(name="Cohere", central_company_id="co_ramp", central_sync_status="linked"),
    )
    assert company.id is not None
    add_company_career_page(
        connection,
        CompanyCareerPage(company_id=company.id, url="https://cohere.com/careers", label="Main"),
    )
    add_company_career_page(
        connection,
        CompanyCareerPage(
            company_id=company.id, url="https://jobs.ashbyhq.com/ramp", label="Central"
        ),
    )
    connection.execute("DELETE FROM migration_state WHERE key = ?", (CENTRAL_LINK_REPAIR_KEY,))

    repair_local_integrity(connection)
    repair_local_integrity(connection)

    repaired = connection.execute("SELECT * FROM companies WHERE id = ?", (company.id,)).fetchone()
    assert repaired["central_company_id"] is None
    assert repaired["central_sync_status"] == "pending"
    assert [page.url for page in list_company_career_pages(connection, company.id)] == [
        "https://cohere.com/careers"
    ]


def test_add_role_deduplicates_specific_postings_globally_but_not_board_roots() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    first_company = add_company(connection, Company(name="Cohere"))
    second_company = add_company(connection, Company(name="Ramp"))
    assert first_company.id is not None and second_company.id is not None

    first = add_role(
        connection,
        Role(
            company_id=first_company.id,
            title="Intern",
            role_url="https://jobs.ashbyhq.com/cohere/job-123?utm_source=test",
        ),
    )
    duplicate = add_role(
        connection,
        Role(
            company_id=second_company.id,
            title="Intern duplicate",
            role_url="https://jobs.ashbyhq.com/cohere/job-123",
        ),
    )
    first_root = add_role(
        connection,
        Role(
            company_id=first_company.id,
            title="General application",
            role_url="https://jobs.ashbyhq.com/cohere",
        ),
    )
    second_root = add_role(
        connection,
        Role(
            company_id=second_company.id,
            title="Another general application",
            role_url="https://jobs.ashbyhq.com/cohere",
        ),
    )

    assert duplicate.id == first.id
    assert first_root.id != second_root.id
    assert len(list_roles(connection)) == 3


def test_repair_merges_owned_data_into_application_stage_survivor() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    ensure_autoprep_schema(connection)
    wrong_company = add_company(connection, Company(name="Ramp"))
    right_company = add_company(connection, Company(name="Cohere"))
    assert wrong_company.id is not None and right_company.id is not None
    first = add_role(
        connection,
        Role(
            company_id=wrong_company.id,
            title="Intern",
            role_url="https://jobs.ashbyhq.com/cohere/job-123?utm_source=x",
            notes="wrong-company note",
        ),
    )
    assert first.id is not None
    connection.execute("DELETE FROM role_identities")
    cursor = connection.execute(
        """
        INSERT INTO roles (company_id, title, role_url, role_status, notes)
        VALUES (
            ?, 'Intern', 'https://jobs.ashbyhq.com/cohere/job-123',
            'applied', 'application note'
        )
        """,
        (right_company.id,),
    )
    second_id = int(cursor.lastrowid)
    connection.execute(
        """
        INSERT INTO events (company_id, role_id, event_type, source, summary)
        VALUES (?, ?, 'note', 'manual', 'history')
        """,
        (wrong_company.id, first.id),
    )
    connection.execute(
        "INSERT INTO application_answers (role_id, question, backend) VALUES (?, 'Why?', 'openai')",
        (first.id,),
    )
    connection.execute("INSERT INTO autoprep_jobs (role_id) VALUES (?)", (first.id,))
    connection.execute("INSERT INTO autoprep_jobs (role_id) VALUES (?)", (second_id,))
    connection.commit()

    repair_local_integrity(connection)

    roles = list_roles(connection)
    assert len(roles) == 1
    survivor = roles[0]
    assert survivor.id == second_id
    assert survivor.role_status is RoleStatus.APPLIED
    assert survivor.notes and "wrong-company note" in survivor.notes
    assert survivor.notes and "application note" in survivor.notes
    assert connection.execute("SELECT role_id FROM events").fetchone()["role_id"] == second_id
    assert (
        connection.execute("SELECT role_id FROM application_answers").fetchone()["role_id"]
        == second_id
    )
    assert (
        connection.execute("SELECT COUNT(*) AS count FROM autoprep_jobs").fetchone()["count"] == 1
    )
    assert (
        connection.execute("SELECT COUNT(*) AS count FROM autoprep_job_archives").fetchone()[
            "count"
        ]
        == 1
    )
