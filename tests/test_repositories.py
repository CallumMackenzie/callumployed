import pytest

from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    Role,
    RoleDiscoveryAttempt,
    RoleDiscoveryStatus,
    RoleStatus,
    ScanStatus,
)
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    add_cover_letter_example,
    add_role,
    add_role_discovery_attempt,
    add_scan_candidates,
    add_scan_page,
    clear_resume_feedback_history,
    clear_roles,
    count_resume_feedback_history,
    create_scan_run,
    deactivate_company,
    finish_scan_run,
    get_company,
    get_event,
    get_location_filter,
    get_master_resume,
    get_tracking_stats,
    increase_company_browser_wait,
    list_companies,
    list_company_career_pages,
    list_config_values,
    list_cover_letter_example_knowledge,
    list_cover_letter_examples,
    list_resume_feedback_knowledge,
    list_role_discovery_attempts,
    list_role_events,
    list_role_items,
    list_roles,
    list_scan_candidates,
    list_scan_pages,
    list_scan_runs,
    record_resume_feedback_history,
    record_role_review_later,
    set_include_graduate_degree_roles,
    set_include_hardware_roles,
    set_internship_mode,
    set_location_filter,
    set_primary_company_career_page_url,
    set_require_software_keywords,
    set_role_status,
    should_include_graduate_degree_roles,
    should_include_hardware_roles,
    should_require_software_keywords,
    should_use_internship_mode,
    update_role,
    upsert_master_resume,
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
        ),
    )

    assert company.id == 1
    assert company.browser_extra_wait_ms == 0
    assert company.is_active is True
    assert list_companies(connection) == [company]


def test_deactivate_company_hides_it_without_deleting_data() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(company_id=company.id, title="Backend Engineer", role_url="https://example.com"),
    )

    deactivated = deactivate_company(connection, company.id)

    assert deactivated.is_active is False
    assert list_companies(connection) == []
    assert list_companies(connection, include_inactive=True) == [deactivated]
    assert get_company(connection, company.id).is_active is False
    assert role.id is not None
    assert list_roles(connection) == [role]
    assert get_tracking_stats(connection)["companies_total"] == 0


def test_company_repository_increases_browser_wait_time() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(connection, Company(name="Acme"))
    if company.id is None:
        raise AssertionError("company id missing")

    updated_company = increase_company_browser_wait(connection, company.id)
    updated_company = increase_company_browser_wait(connection, company.id)

    assert updated_company.browser_extra_wait_ms == 2_000
    assert get_company(connection, company.id).browser_extra_wait_ms == 2_000


def test_resume_feedback_history_records_ranks_and_clears_decisions() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    company = add_company(connection, Company(name="Acme"))
    role = add_role(
        connection,
        Role(
            company_id=company.id or 1,
            title="Backend Intern",
            role_url="https://example.com/jobs/backend",
            description="Python distributed systems internship",
        ),
    )

    history_id = record_resume_feedback_history(
        connection,
        role=role,
        feedback_index=0,
        feedback={
            "label": "change_wording",
            "title": "change wording to align with posting: distributed systems",
            "detail": "rewrite the systems project bullet",
            "target_text": "Python systems",
            "replacement_text": "Python distributed systems",
        },
        response="ignored",
        comment="too generic for this resume",
    )

    assert history_id == 1
    assert count_resume_feedback_history(connection) == 1
    knowledge = list_resume_feedback_knowledge(
        connection,
        role=Role(
            company_id=company.id or 1,
            title="Distributed Systems Intern",
            role_url="https://example.com/jobs/distributed",
            description="Python backend distributed systems",
        ),
        resume_content="Python systems project",
    )

    assert knowledge[0]["response"] == "ignored"
    assert knowledge[0]["comment"] == "too generic for this resume"
    assert "preference_summary" in knowledge[0]
    assert "Python distributed systems internship" not in str(knowledge[0]["knowledge_text"])
    assert "Python distributed systems internship" not in str(knowledge[0]["preference_summary"])
    assert knowledge[0]["similarity"] > 0
    assert clear_resume_feedback_history(connection) == 1
    assert count_resume_feedback_history(connection) == 0


def test_config_repository_filters_graduate_degree_roles_by_default() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    assert should_include_graduate_degree_roles(connection) is False

    set_include_graduate_degree_roles(connection, True)
    assert should_include_graduate_degree_roles(connection) is True
    assert list_config_values(connection) == {"include_graduate_degree_roles": "true"}

    set_include_graduate_degree_roles(connection, False)
    assert should_include_graduate_degree_roles(connection) is False
    assert list_config_values(connection) == {"include_graduate_degree_roles": "false"}


def test_config_repository_filters_hardware_roles_by_default() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    assert should_include_hardware_roles(connection) is False

    set_include_hardware_roles(connection, True)
    assert should_include_hardware_roles(connection) is True
    assert list_config_values(connection) == {"include_hardware_roles": "true"}

    set_include_hardware_roles(connection, False)
    assert should_include_hardware_roles(connection) is False
    assert list_config_values(connection) == {"include_hardware_roles": "false"}


def test_config_repository_requires_software_keywords_by_default() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    assert should_require_software_keywords(connection) is True

    set_require_software_keywords(connection, False)
    assert should_require_software_keywords(connection) is False
    assert list_config_values(connection) == {"require_software_keywords": "false"}

    set_require_software_keywords(connection, True)
    assert should_require_software_keywords(connection) is True
    assert list_config_values(connection) == {"require_software_keywords": "true"}


def test_config_repository_uses_internship_mode_by_default() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    assert should_use_internship_mode(connection) is True

    set_internship_mode(connection, False)
    assert should_use_internship_mode(connection) is False
    assert list_config_values(connection) == {"internship_mode": "false"}

    set_internship_mode(connection, True)
    assert should_use_internship_mode(connection) is True
    assert list_config_values(connection) == {"internship_mode": "true"}


def test_config_repository_uses_all_location_filter_by_default() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    assert get_location_filter(connection) == "all"

    set_location_filter(connection, "north-america")
    assert get_location_filter(connection) == "north_america"
    assert list_config_values(connection) == {"location_filter": "north_america"}

    with pytest.raises(ValueError, match="location_filter must be one of"):
        set_location_filter(connection, "mars")


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


def test_master_resume_repository_upserts_tex_resume() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    created = upsert_master_resume(
        connection,
        filename="/tmp/master.tex",
        content="\\documentclass{article}",
    )
    replaced = upsert_master_resume(
        connection,
        filename="updated.tex",
        content="\\documentclass{article}\n\\begin{document}Callum\\end{document}",
    )

    assert created.id == 1
    assert replaced.id == 1
    assert replaced.filename == "updated.tex"
    assert replaced.content.startswith("\\documentclass")
    assert replaced.content_sha256 != created.content_sha256
    assert get_master_resume(connection) == replaced


def test_master_resume_repository_rejects_non_tex_resume() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    with pytest.raises(ValueError, match=".tex"):
        upsert_master_resume(connection, filename="resume.pdf", content="not tex")


def test_cover_letter_example_repository_adds_multiple_examples() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    first = add_cover_letter_example(
        connection,
        filename="/tmp/apple-cover.tex",
        content="Dear Apple,",
    )
    second = add_cover_letter_example(
        connection,
        filename="stripe-cover.md",
        content="Dear Stripe,",
    )

    examples = list_cover_letter_examples(connection)

    assert first.id == 1
    assert second.id == 2
    assert [example.filename for example in examples] == [
        "stripe-cover.md",
        "apple-cover.tex",
    ]
    assert examples[0].content == "Dear Stripe,"
    assert examples[0].content_sha256 != examples[1].content_sha256


def test_cover_letter_example_repository_indexes_examples_for_similarity() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    add_cover_letter_example(
        connection,
        filename="backend.tex",
        content="I built Python distributed systems and backend APIs.",
    )
    add_cover_letter_example(
        connection,
        filename="hardware.tex",
        content="I designed embedded firmware and hardware validation tools.",
    )

    matches = list_cover_letter_example_knowledge(
        connection,
        query="backend Python APIs",
        limit=1,
    )

    assert matches[0]["filename"] == "backend.tex"
    assert matches[0]["similarity"] > 0


def test_cover_letter_example_repository_rejects_empty_content() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    with pytest.raises(ValueError, match="content"):
        add_cover_letter_example(connection, filename="empty.tex", content="  ")


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


def test_role_discovery_attempt_repository_persists_page_data() -> None:
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
    scan_page = add_scan_page(
        connection,
        scan_run.id,
        CareersPageScanResult(
            source_url=career_page.url,
            final_url=career_page.url,
            candidates=[
                ScoredLinkCandidate(
                    url="https://example.com/jobs/backend",
                    source_url=career_page.url,
                    text="Backend Engineer",
                    confidence=0.78,
                )
            ],
            links=[
                DiscoveredJobLink(
                    url="https://example.com/jobs/backend",
                    source_url=career_page.url,
                    text="Backend Engineer",
                    confidence=0.78,
                    discovery_method="heuristic",
                )
            ],
        ),
        company_career_page_id=career_page.id,
    )
    assert scan_page.id is not None
    candidates = add_scan_candidates(
        connection,
        scan_page.id,
        [
            ScoredLinkCandidate(
                url="https://example.com/jobs/backend",
                source_url=career_page.url,
                text="Backend Engineer",
                confidence=0.78,
            )
        ],
        CareersPageScanResult(
            source_url=career_page.url,
            final_url=career_page.url,
            links=[
                DiscoveredJobLink(
                    url="https://example.com/jobs/backend",
                    source_url=career_page.url,
                    text="Backend Engineer",
                    confidence=0.78,
                    discovery_method="heuristic",
                )
            ],
        ),
    )
    assert candidates[0].id is not None

    attempt = add_role_discovery_attempt(
        connection,
        RoleDiscoveryAttempt(
            scan_run_id=scan_run.id,
            scan_candidate_id=candidates[0].id,
            company_id=company.id,
            url=candidates[0].url,
            final_url="https://example.com/jobs/backend",
            title="Backend Engineer",
            visible_text_excerpt="Backend Engineer Vancouver Apply now",
            assessment_is_role=True,
            assessment_is_closed=False,
            assessment_confidence=0.95,
            assessment_location="Vancouver, BC, CA",
            assessment_description="Backend Engineer Vancouver Apply now",
            assessment_posting_id="REQ-123",
            assessment_extraction_method="jobposting_structured_data",
            assessment_rejection_reason=None,
            assessment_reasons=["schema.org JobPosting structured data"],
            status=RoleDiscoveryStatus.SUCCEEDED,
        ),
    )

    attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)

    assert attempts == [attempt]
    assert attempts[0].title == "Backend Engineer"
    assert attempts[0].assessment_is_role is True
    assert attempts[0].assessment_is_closed is False
    assert attempts[0].assessment_confidence == 0.95
    assert attempts[0].assessment_location == "Vancouver, BC, CA"
    assert attempts[0].assessment_description == "Backend Engineer Vancouver Apply now"
    assert attempts[0].assessment_posting_id == "REQ-123"
    assert attempts[0].assessment_extraction_method == "jobposting_structured_data"
    assert attempts[0].assessment_reasons == ["schema.org JobPosting structured data"]
    assert attempts[0].status is RoleDiscoveryStatus.SUCCEEDED


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
            description="Build backend systems for the product team.",
            posting_id="REQ-1",
        ),
    )
    assert role.id is not None
    assert role.description == "Build backend systems for the product team."
    assert role.posting_id == "REQ-1"

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


def test_list_role_items_counts_review_later_events() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(company_id=company.id, title="Backend Engineer", role_url="https://example.com"),
    )
    assert role.id is not None

    record_role_review_later(connection, role.id)
    record_role_review_later(connection, role.id)

    roles = list_role_items(connection)

    assert len(roles) == 1
    assert roles[0].review_later_count == 2


def test_clear_roles_deletes_roles_and_role_linked_events() -> None:
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

    deleted_count = clear_roles(connection)

    assert deleted_count == 1
    assert list_roles(connection) == []
    assert list_role_events(connection, role.id) == []
    assert list_companies(connection) == [company]


def test_role_list_items_include_company_and_filter_by_query() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)
    company = add_company(connection, Company(name="Acme"))
    assert company.id is not None
    role = add_role(
        connection,
        Role(
            company_id=company.id,
            title="Backend Engineer",
            role_url="https://example.com/jobs/backend",
            location="Vancouver",
        ),
    )
    assert role.id is not None
    set_role_status(connection, role.id, RoleStatus.INTERESTED, summary="Worth tracking.")

    roles = list_role_items(connection, query="backend")
    link_roles = list_role_items(connection, link="example.com/jobs")
    status_roles = list_role_items(connection, query="interested")

    assert len(roles) == 1
    assert roles[0].company_name == "Acme"
    assert roles[0].title == "Backend Engineer"
    assert link_roles == roles
    assert status_roles == roles


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
        description="Build backend systems.",
        posting_id="REQ-42",
        clear_location=True,
        clear_notes=True,
        touch_last_seen=True,
    )

    assert updated_role.title == "Backend Engineer"
    assert updated_role.role_url == "https://example.com/jobs/backend"
    assert updated_role.location is None
    assert updated_role.notes is None
    assert updated_role.description == "Build backend systems."
    assert updated_role.posting_id == "REQ-42"


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
