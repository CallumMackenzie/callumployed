from callumployed.data import db
from callumployed.data.models import Company, CompanyCareerPage, Role, RoleStatus, ScanStatus
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    add_role,
    add_scan_candidates,
    add_scan_page,
    clear_default_external_browser_port,
    create_scan_run,
    finish_scan_run,
    get_default_external_browser_port,
    get_event,
    list_companies,
    list_company_career_pages,
    list_config_values,
    list_role_events,
    list_role_items,
    list_roles,
    list_scan_candidates,
    list_scan_pages,
    list_scan_runs,
    set_company_external_browser_port,
    set_default_external_browser_port,
    set_primary_company_career_page_url,
    set_role_status,
    update_role,
)
from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    ScoredLinkCandidate,
)


def test_company_repository_adds_and_lists_companies() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(
        connection,
        Company(
            name="Acme",
            prestige_tier="A",
            external_browser_port=9222,
        ),
    )

    assert company.id == 1
    assert company.external_browser_port == 9222
    assert list_companies(connection) == [company]


def test_company_repository_sets_external_browser_port() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None

    updated_company = set_company_external_browser_port(connection, company.id, 9222)

    assert updated_company.external_browser_port == 9222


def test_config_repository_sets_lists_and_clears_default_external_browser_port() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    set_default_external_browser_port(connection, 9222)

    assert get_default_external_browser_port(connection) == 9222
    assert list_config_values(connection) == {"external_browser_port": "9222"}

    clear_default_external_browser_port(connection)

    assert get_default_external_browser_port(connection) is None
    assert list_config_values(connection) == {}


def test_company_repository_tracks_multiple_career_pages() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    add_company_career_page(
        connection,
        CompanyCareerPage(
            company_id=company.id,
            url="https://example.com/main",
            label="Main",
        ),
    )
    add_company_career_page(
        connection,
        CompanyCareerPage(
            company_id=company.id,
            url="https://example.com/internships",
            label="Internships",
        ),
    )
    add_company_career_page(
        connection,
        CompanyCareerPage(
            company_id=company.id,
            url="https://example.com/students",
            label="Students",
        ),
    )

    career_pages = list_company_career_pages(connection, company.id)

    assert [page.url for page in career_pages] == [
        "https://example.com/main",
        "https://example.com/internships",
        "https://example.com/students",
    ]


def test_company_repository_updates_primary_career_page() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    add_company_career_page(
        connection,
        CompanyCareerPage(
            company_id=company.id,
            url="https://example.com/main",
            label="Main",
        ),
    )
    add_company_career_page(
        connection,
        CompanyCareerPage(
            company_id=company.id,
            url="https://example.com/internships",
            label="Internships",
        ),
    )

    updated_page = set_primary_company_career_page_url(
        connection,
        company.id,
        "https://example.com/jobs",
    )
    career_pages = list_company_career_pages(connection, company.id)

    assert updated_page.url == "https://example.com/jobs"
    assert [page.url for page in career_pages] == [
        "https://example.com/jobs",
        "https://example.com/internships",
    ]


def test_scan_repository_persists_pages_and_candidates() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    career_page = add_company_career_page(
        connection,
        CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
    )
    assert career_page.id is not None
    scan_run = create_scan_run(connection, company.id)
    assert scan_run.id is not None
    result = CareersPageScanResult(
        source_url="https://example.com/careers",
        final_url="https://example.com/careers",
        candidates=[
            ScoredLinkCandidate(
                url="https://example.com/jobs/backend",
                source_url="https://example.com/careers",
                text="Backend Engineer",
                confidence=0.78,
                reasons=["job-like URL path"],
            ),
            ScoredLinkCandidate(
                url="https://example.com/about",
                source_url="https://example.com/careers",
                text="About",
                confidence=0.0,
                reasons=[],
            ),
        ],
        links=[
            DiscoveredJobLink(
                url="https://example.com/jobs/backend",
                source_url="https://example.com/careers",
                text="Backend Engineer",
                confidence=0.78,
                discovery_method="heuristic",
                reasons=["job-like URL path"],
            )
        ],
        candidates_scanned=2,
        confidence=ExtractionConfidence.MEDIUM,
    )

    scan_page = add_scan_page(
        connection,
        scan_run.id,
        result,
        company_career_page_id=career_page.id,
    )
    assert scan_page.id is not None
    add_scan_candidates(connection, scan_page.id, result.candidates, result)
    finished_run = finish_scan_run(connection, scan_run.id, ScanStatus.SUCCEEDED)
    scan_runs = list_scan_runs(connection)
    scan_pages = list_scan_pages(connection, scan_run.id)
    scan_candidates = list_scan_candidates(connection, scan_page.id)

    assert finished_run.scan_status is ScanStatus.SUCCEEDED
    assert scan_runs[0].company_name == "Acme"
    assert scan_pages == [scan_page]
    assert [candidate.url for candidate in scan_candidates] == [
        "https://example.com/jobs/backend",
        "https://example.com/about",
    ]
    assert scan_candidates[0].selected is True
    assert scan_candidates[1].selected is False


def test_company_repository_adds_company_with_legacy_careers_url_column() -> None:
    connection = db.connect(":memory:")
    connection.executescript(
        """
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            careers_url TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            notes TEXT,
            prestige_tier TEXT
        );
        """
    )
    db.run_migrations(connection)

    company = add_company(connection, Company(name="Acme"))

    legacy_row = connection.execute(
        "SELECT careers_url FROM companies WHERE id = ?",
        (company.id,),
    ).fetchone()
    assert company.name == "Acme"
    assert legacy_row["careers_url"] == ""


def test_migrations_backfill_legacy_company_career_pages() -> None:
    connection = db.connect(":memory:")
    connection.executescript(
        """
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            careers_url TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            notes TEXT,
            prestige_tier TEXT
        );

        INSERT INTO companies (id, name, careers_url)
        VALUES (1, 'Apple', 'https://jobs.apple.com/search');
        """
    )

    db.run_migrations(connection)

    career_pages = list_company_career_pages(connection, 1)
    assert len(career_pages) == 1
    assert career_pages[0].url == "https://jobs.apple.com/search"


def test_role_repository_adds_filters_and_records_status_events() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(
            company_id=company.id,
            title="Software Engineer",
            role_url="https://example.com/jobs/1",
            location="Vancouver",
        ),
    )
    assert role.id is not None

    filtered_roles = list_roles(
        connection,
        company_id=company.id,
        role_status=RoleStatus.DISCOVERED,
    )

    assert filtered_roles == [role]

    updated_role = set_role_status(
        connection,
        role.id,
        RoleStatus.INTERESTED,
        summary="Looks worth applying to.",
    )
    event = get_event(connection, 1)

    assert updated_role.role_status is RoleStatus.INTERESTED
    assert event.old_status is RoleStatus.DISCOVERED
    assert event.new_status is RoleStatus.INTERESTED


def test_role_list_items_include_company_and_filter_by_query() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    add_role(
        connection,
        Role(
            company_id=company.id,
            title="Backend Engineer",
            role_url="https://example.com/jobs/backend",
            location="Vancouver",
        ),
    )

    roles = list_role_items(connection, query="backend")

    assert len(roles) == 1
    assert roles[0].company_name == "Acme"
    assert roles[0].title == "Backend Engineer"


def test_update_role_changes_and_clears_fields() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(
            company_id=company.id,
            title="Software Engineer",
            role_url="https://example.com/jobs/1",
            location="Remote",
            notes="Initial notes.",
        ),
    )
    assert role.id is not None

    updated_role = update_role(
        connection,
        role.id,
        title="Backend Engineer",
        role_url="https://example.com/jobs/backend",
        clear_location=True,
        clear_notes=True,
    )

    assert updated_role.title == "Backend Engineer"
    assert updated_role.role_url == "https://example.com/jobs/backend"
    assert updated_role.location is None
    assert updated_role.notes is None


def test_list_role_events_returns_recent_role_events() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(company_id=company.id, title="Backend Engineer", role_url="https://example.com"),
    )
    assert role.id is not None

    set_role_status(connection, role.id, RoleStatus.INTERESTED, summary="Worth tracking.")

    events = list_role_events(connection, role.id)

    assert len(events) == 1
    assert events[0].summary == "Worth tracking."
