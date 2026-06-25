import asyncio
from pathlib import Path

import pytest

from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    Role,
    RoleDiscoveryStatus,
    RoleStatus,
)
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    add_role,
    list_role_discovery_attempts,
    list_roles,
    list_scan_candidates,
    list_scan_pages,
    set_include_graduate_degree_roles,
    set_include_hardware_roles,
    set_require_software_keywords,
)
from callumployed.services import scan_workflow
from callumployed.webscraping.models import RenderedPageState


def _use_database(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "callumployed.sqlite3"))
    db.ensure_initialized()


def _page(url: str) -> RenderedPageState:
    return RenderedPageState(
        url=url,
        final_url=url,
        title="Example Careers",
        html="""
        <a href="/jobs/software-engineering-intern-12345">
          Software Engineering Intern
        </a>
        <a href="/roles/swe">Software Intern</a>
        <a href="/about">About</a>
        """,
    )


class EmptyStructuredModel:
    async def ainvoke(self, prompt: object) -> object:
        return {"decisions": []}


def test_render_page_node_passes_external_browser_port(monkeypatch: pytest.MonkeyPatch) -> None:
    rendered_ports: list[int | None] = []

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        rendered_ports.append(external_browser_port)
        return _page(url)

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    state = asyncio.run(
        scan_workflow.render_page_node(
            {"url": "https://example.com/careers", "external_browser_port": 9222}
        )
    )

    assert rendered_ports == [9222]
    assert state["page"].final_url == "https://example.com/careers"


def test_graph_calls_llm_for_ambiguous_candidates_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        return _page(url)

    model_calls = 0

    class FakeStructuredModel:
        async def ainvoke(self, prompt: object) -> object:
            nonlocal model_calls
            model_calls += 1
            return {"decisions": []}

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    result = asyncio.run(
        scan_workflow.scan_url(
            "https://example.com/careers",
            chat_model_factory=lambda _settings: FakeStructuredModel(),
        )
    )

    assert model_calls == 1
    assert "https://example.com/jobs/software-engineering-intern-12345" in {
        link.url for link in result.links
    }
    assert "https://example.com/roles/swe" not in {link.url for link in result.links}


def test_graph_calls_llm_only_with_ambiguous_candidates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prompts: list[str] = []

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        return _page(url)

    class FakeStructuredModel:
        async def ainvoke(self, prompt: object) -> object:
            assert isinstance(prompt, str)
            prompts.append(prompt)
            return {
                "decisions": [
                    {
                        "url": "https://example.com/roles/swe",
                        "is_job_posting": True,
                        "confidence": 0.9,
                        "title": "Software Intern",
                        "reasons": ["Specific role page."],
                    }
                ]
            }

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    result = asyncio.run(
        scan_workflow.scan_url(
            "https://example.com/careers",
            chat_model_factory=lambda _settings: FakeStructuredModel(),
        )
    )

    assert len(prompts) == 1
    assert "https://example.com/roles/swe" in prompts[0]
    assert "software-engineering-intern-12345" not in prompts[0]
    assert {link.discovery_method for link in result.links} == {"heuristic", "agent"}


def test_scan_company_persists_page_and_candidates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        return _page(url)

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )
        add_role(
            connection,
            Role(
                company_id=company.id,
                title="Existing",
                role_url="https://example.com/jobs/software-engineering-intern-12345",
            ),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert scan["results"][0].links == []
    scan_run = scan["scan_run"]
    assert scan_run.id is not None
    with db.connect() as connection:
        pages = list_scan_pages(connection, scan_run.id)
        assert len(pages) == 1
        assert pages[0].source_url == "https://example.com/careers"
        if pages[0].id is None:
            raise AssertionError("scan page id missing")
        candidates = list_scan_candidates(connection, pages[0].id)

    by_url = {candidate.url: candidate for candidate in candidates}
    existing = by_url["https://example.com/jobs/software-engineering-intern-12345"]
    assert existing.confidence == 0.0
    assert existing.selected is False
    assert "already in database" in existing.reasons


def test_scan_company_visits_selected_discovered_links(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)
    rendered_urls: list[str] = []

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **render_options: object,
    ) -> RenderedPageState:
        rendered_urls.append(url)
        if url.endswith("/careers"):
            assert render_options == {}
        else:
            assert render_options == {
                "content_settle_min_wait_ms": scan_workflow.ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS,
                "content_settle_timeout_ms": scan_workflow.ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS,
                "content_settle_poll_ms": scan_workflow.ROLE_PAGE_CONTENT_SETTLE_POLL_MS,
                "lazy_scroll_step_delay_ms": scan_workflow.ROLE_PAGE_LAZY_SCROLL_STEP_DELAY_MS,
            }
        if url.endswith("/careers"):
            return _page(url)
        return RenderedPageState(
            url=url,
            final_url=f"{url}?tracked=true",
            title="Careers",
            html="""
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "Software Engineering Intern",
              "description": "Software Engineering Intern Vancouver Apply now",
              "identifier": {"value": "REQ-123"},
              "jobLocation": {
                "@type": "Place",
                "address": {
                  "@type": "PostalAddress",
                  "addressLocality": "Vancouver",
                  "addressRegion": "BC",
                  "addressCountry": "CA"
                }
              }
            }
            </script>
            <h1>Careers</h1>
            """,
            visible_text="Software Engineering Intern Vancouver Apply now",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    scan_run = scan["scan_run"]
    assert scan_run.id is not None
    with db.connect() as connection:
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)
        roles = list_roles(connection)

    assert rendered_urls == [
        "https://example.com/careers",
        "https://example.com/jobs/software-engineering-intern-12345",
    ]
    assert len(attempts) == 1
    assert scan["role_discovery_attempts"] == attempts
    assert attempts[0].status is RoleDiscoveryStatus.SUCCEEDED
    assert attempts[0].url == "https://example.com/jobs/software-engineering-intern-12345"
    assert attempts[0].final_url == (
        "https://example.com/jobs/software-engineering-intern-12345?tracked=true"
    )
    assert attempts[0].title == "Software Engineering Intern"
    assert attempts[0].visible_text_excerpt == (
        "Software Engineering Intern Vancouver Apply now"
    )
    assert attempts[0].assessment_is_role is True
    assert attempts[0].assessment_is_closed is False
    assert attempts[0].assessment_confidence == 0.95
    assert attempts[0].assessment_description == (
        "Software Engineering Intern Vancouver Apply now"
    )
    assert attempts[0].assessment_location == "Vancouver, BC, CA"
    assert attempts[0].assessment_posting_id == "REQ-123"
    assert attempts[0].assessment_extraction_method == "jobposting_structured_data"
    assert attempts[0].assessment_reasons == ["schema.org JobPosting structured data"]
    assert len(roles) == 1
    assert attempts[0].role_id == roles[0].id
    assert roles[0].title == "Software Engineering Intern"
    assert roles[0].role_url == "https://example.com/jobs/software-engineering-intern-12345"
    assert roles[0].location == "Vancouver, BC, CA"
    assert roles[0].description == "Software Engineering Intern Vancouver Apply now"
    assert roles[0].posting_id == "REQ-123"
    assert roles[0].role_status is RoleStatus.DISCOVERED


def test_scan_company_creates_discovered_role_for_closed_application_page(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url.endswith("/careers"):
            return _page(url)
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Careers",
            html="""
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "Software Engineering Intern",
              "description": "Software Engineering Intern. No longer accepting applications."
            }
            </script>
            <h1>Careers</h1>
            """,
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    with db.connect() as connection:
        roles = list_roles(connection)
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan["scan_run"].id)

    assert len(roles) == 1
    assert roles[0].role_status is RoleStatus.DISCOVERED
    assert attempts[0].role_id == roles[0].id
    assert attempts[0].assessment_is_closed is True


def test_scan_company_filters_graduate_degree_roles_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url.endswith("/careers"):
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Careers",
                html='<a href="/jobs/phd-research-intern-12345">PhD Research Intern</a>',
            )
        return RenderedPageState(
            url=url,
            final_url=url,
            title="PhD Research Intern",
            html="""
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "PhD Research Intern",
              "description": "PhD Research Intern. Must be pursuing a PhD or Master's degree."
            }
            </script>
            """,
            visible_text="PhD Research Intern. Must be pursuing a PhD or Master's degree.",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert scan["results"][0].links == []
    scan_run = scan["scan_run"]
    assert scan_run.id is not None
    with db.connect() as connection:
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)
        roles = list_roles(connection)

    assert roles == []
    assert attempts == []


def test_scan_company_can_include_graduate_degree_roles_when_configured(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url.endswith("/careers"):
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Careers",
                html='<a href="/jobs/phd-research-intern-12345">PhD Research Intern</a>',
            )
        return RenderedPageState(
            url=url,
            final_url=url,
            title="PhD Research Intern",
            html="""
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "PhD Research Intern",
              "description": "PhD Research Intern. Must be pursuing a PhD or Master's degree."
            }
            </script>
            """,
            visible_text="PhD Research Intern. Must be pursuing a PhD or Master's degree.",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        set_include_graduate_degree_roles(connection, True)
        set_require_software_keywords(connection, False)
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert {link.url for link in scan["results"][0].links} == {
        "https://example.com/jobs/phd-research-intern-12345"
    }
    scan_run = scan["scan_run"]
    assert scan_run.id is not None
    with db.connect() as connection:
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)
        roles = list_roles(connection)

    assert len(roles) == 1
    assert roles[0].title == "PhD Research Intern"
    assert len(attempts) == 1
    assert attempts[0].assessment_is_role is True
    assert attempts[0].assessment_rejection_reason is None


def test_scan_company_filters_hardware_only_roles_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url.endswith("/careers"):
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Careers",
                html="""
                <a href="/jobs/hardware-intern-12345">Hardware Internships</a>
                <a href="/jobs/hardware-firmware-intern-12346">Hardware Firmware Internships</a>
                <a href="/jobs/hardware-developer-intern-12347">Hardware Developer Internships</a>
                """,
            )
        title = (
            "Hardware Developer Internships"
            if "developer" in url
            else "Hardware Firmware Internships"
        )
        return RenderedPageState(
            url=url,
            final_url=url,
            title=title,
            html=f"""
            <script type="application/ld+json">
            {{
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "{title}",
              "description": "{title}."
            }}
            </script>
            """,
            visible_text=f"{title}.",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert {link.text for link in scan["results"][0].links} == {
        "Hardware Firmware Internships",
        "Hardware Developer Internships",
    }
    scan_run = scan["scan_run"]
    assert scan_run.id is not None
    with db.connect() as connection:
        roles = list_roles(connection)

    assert len(roles) == 2
    assert {role.title for role in roles} == {
        "Hardware Firmware Internships",
        "Hardware Developer Internships",
    }


def test_scan_company_can_include_hardware_only_roles_when_configured(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url.endswith("/careers"):
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Careers",
                html='<a href="/jobs/hardware-intern-12345">Hardware Internships</a>',
            )
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Hardware Internships",
            html="""
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "Hardware Internships",
              "description": "Hardware internship."
            }
            </script>
            """,
            visible_text="Hardware internship.",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        set_include_hardware_roles(connection, True)
        set_require_software_keywords(connection, False)
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert {link.text for link in scan["results"][0].links} == {"Hardware Internships"}
    scan_run = scan["scan_run"]
    assert scan_run.id is not None
    with db.connect() as connection:
        roles = list_roles(connection)

    assert len(roles) == 1
    assert roles[0].title == "Hardware Internships"


def test_scan_company_requires_software_keywords_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url.endswith("/careers"):
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Careers",
                html="""
                <a href="/jobs/product-management-intern-12345">Product Management Internships</a>
                <a href="/jobs/ai-engineering-intern-12346">AI Engineering Internships</a>
                <a href="/jobs/backend-engineering-intern-12347">Backend Engineering Internships</a>
                <a href="/jobs/security-engineering-intern-12348">
                  Security Engineering Internships
                </a>
                """,
            )
        title_by_url = {
            "ai": "AI Engineering Internships",
            "backend": "Backend Engineering Internships",
            "security": "Security Engineering Internships",
        }
        title = next(value for key, value in title_by_url.items() if key in url)
        return RenderedPageState(
            url=url,
            final_url=url,
            title=title,
            html=f"""
            <script type="application/ld+json">
            {{
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "{title}",
              "description": "{title}."
            }}
            </script>
            """,
            visible_text=f"{title}.",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert {link.text for link in scan["results"][0].links} == {
        "AI Engineering Internships",
        "Backend Engineering Internships",
        "Security Engineering Internships",
    }
    with db.connect() as connection:
        roles = list_roles(connection)

    assert {role.title for role in roles} == {
        "AI Engineering Internships",
        "Backend Engineering Internships",
        "Security Engineering Internships",
    }


def test_scan_company_can_allow_non_software_keyword_roles_when_configured(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url.endswith("/careers"):
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Careers",
                html="""
                <a href="/jobs/product-management-intern-12345">
                  Product Management Internships
                </a>
                """,
            )
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Product Management Internships",
            html="""
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "Product Management Internships",
              "description": "Product management internship."
            }
            </script>
            """,
            visible_text="Product management internship.",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        set_require_software_keywords(connection, False)
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert {link.text for link in scan["results"][0].links} == {
        "Product Management Internships"
    }
    with db.connect() as connection:
        roles = list_roles(connection)

    assert len(roles) == 1
    assert roles[0].title == "Product Management Internships"


def test_scan_company_records_failed_discovered_link_visits(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url.endswith("/careers"):
            return _page(url)
        raise RuntimeError("posting page failed")

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    attempts = scan["role_discovery_attempts"]
    assert len(attempts) == 1
    assert attempts[0].status is RoleDiscoveryStatus.FAILED
    assert attempts[0].error == "posting page failed"
