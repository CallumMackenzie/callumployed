import asyncio
from pathlib import Path
from typing import cast

import pytest

from callumployed.data import db
from callumployed.data.models import (
    Company,
    CompanyCareerPage,
    Role,
    RoleDiscoveryAttempt,
    RoleDiscoveryStatus,
    RoleStatus,
    ScanCandidate,
    ScanStatus,
)
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    add_role,
    add_role_discovery_attempt,
    add_scan_candidates,
    add_scan_page,
    create_scan_run,
    get_company,
    get_role,
    list_role_discovery_attempts,
    list_roles,
    list_scan_candidates,
    list_scan_pages,
    list_scan_runs,
    set_include_graduate_degree_roles,
    set_include_hardware_roles,
    set_internship_mode,
    set_location_filter,
    set_require_software_keywords,
)
from callumployed.services import scan_workflow
from callumployed.webscraping.errors import ClassificationError, NavigationError
from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    RenderedPageState,
    RolePageAssessment,
    ScoredLinkCandidate,
)
from callumployed.webscraping.profile_manager import BrowserProfileManager


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


def test_render_page_node_uses_browser_profile_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    rendered_ports: list[int | None] = []
    manager_calls: list[str] = []
    monkeypatch.setenv("CALLUMPLOYED_BROWSER_BACKEND", "local")

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        fallback_to_managed_browser: bool = True,
        **_render_options: object,
    ) -> RenderedPageState:
        assert fallback_to_managed_browser is False
        rendered_ports.append(external_browser_port)
        return _page(url)

    class FakeProfileManager:
        async def render(
            self,
            render: object,
            url: str,
            *,
            render_options: object | None = None,
        ) -> RenderedPageState:
            manager_calls.append(url)
            return await fake_render_careers_page(
                url,
                external_browser_port=9440,
                fallback_to_managed_browser=False,
            )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    state = asyncio.run(
        scan_workflow.render_page_node(
            {
                "url": "https://example.com/careers",
                "browser_profile_manager": cast(BrowserProfileManager, FakeProfileManager()),
            }
        )
    )

    assert manager_calls == ["https://example.com/careers"]
    assert rendered_ports == [9440]
    assert state["page"].final_url == "https://example.com/careers"


def test_render_page_node_falls_back_when_profile_manager_is_unconfigured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manager_calls: list[str] = []
    direct_render_calls: list[str] = []
    monkeypatch.setenv("CALLUMPLOYED_BROWSER_BACKEND", "local")

    async def fake_render_careers_page(
        url: str,
        **_render_options: object,
    ) -> RenderedPageState:
        direct_render_calls.append(url)
        return _page(url)

    class FakeProfileManager:
        async def render(
            self,
            render: object,
            url: str,
            *,
            render_options: object | None = None,
        ) -> RenderedPageState:
            _ = render, render_options
            manager_calls.append(url)
            raise ValueError("could not find Brave browser executable")

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    state = asyncio.run(
        scan_workflow.render_page_node(
            {
                "url": "https://example.com/careers",
                "browser_profile_manager": cast(BrowserProfileManager, FakeProfileManager()),
            }
        )
    )

    assert manager_calls == ["https://example.com/careers"]
    assert direct_render_calls == ["https://example.com/careers"]
    assert state["page"].final_url == "https://example.com/careers"


def test_render_page_node_falls_back_when_profile_browser_executable_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    direct_render_calls: list[str] = []
    monkeypatch.setenv("CALLUMPLOYED_BROWSER_BACKEND", "local")

    async def fake_render_careers_page(
        url: str,
        **_render_options: object,
    ) -> RenderedPageState:
        direct_render_calls.append(url)
        return _page(url)

    class FakeProfileManager:
        async def render(
            self,
            render: object,
            url: str,
            *,
            render_options: object | None = None,
        ) -> RenderedPageState:
            _ = render, url, render_options
            raise FileNotFoundError("Brave Browser")

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    state = asyncio.run(
        scan_workflow.render_page_node(
            {
                "url": "https://example.com/careers",
                "browser_profile_manager": cast(BrowserProfileManager, FakeProfileManager()),
            }
        )
    )

    assert direct_render_calls == ["https://example.com/careers"]
    assert state["page"].final_url == "https://example.com/careers"


def test_browserbase_render_failure_falls_back_to_profile_manager(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manager_calls: list[str] = []

    async def fake_render_careers_page(
        url: str,
        **_render_options: object,
    ) -> RenderedPageState:
        raise NavigationError("browserbase failed")

    class FakeProfileManager:
        async def render(
            self,
            render: object,
            url: str,
            *,
            render_options: object | None = None,
        ) -> RenderedPageState:
            manager_calls.append(url)
            return _page(url)

    monkeypatch.setenv("CALLUMPLOYED_BROWSER_BACKEND", "browserbase")
    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    state = asyncio.run(
        scan_workflow.render_page_node(
            {
                "url": "https://example.com/careers",
                "browser_profile_manager": cast(BrowserProfileManager, FakeProfileManager()),
            }
        )
    )

    assert manager_calls == ["https://example.com/careers"]
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


def test_scan_url_surfaces_ai_classification_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        return _page(url)

    class FailingStructuredModel:
        async def ainvoke(self, prompt: object) -> object:
            _ = prompt
            raise RuntimeError("OpenAI quota exceeded")

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with pytest.raises(
        ClassificationError,
        match="AI classification failed: OpenAI quota exceeded",
    ):
        asyncio.run(
            scan_workflow.scan_url(
                "https://example.com/careers",
                chat_model_factory=lambda _settings: FailingStructuredModel(),
            )
        )


def test_scan_company_records_ai_classification_errors_on_scan_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        return _page(url)

    class FailingStructuredModel:
        async def ainvoke(self, prompt: object) -> object:
            _ = prompt
            raise RuntimeError("OpenAI API key is invalid")

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with pytest.raises(ClassificationError, match="AI classification failed: OpenAI API key"):
        asyncio.run(
            scan_workflow.scan_company(
                company,
                chat_model_factory=lambda _settings: FailingStructuredModel(),
            )
        )

    with db.connect() as connection:
        scan_runs = list_scan_runs(connection, company_id=company.id, limit=1)

    assert len(scan_runs) == 1
    assert scan_runs[0].scan_status is ScanStatus.FAILED
    assert scan_runs[0].error == "AI classification failed: OpenAI API key is invalid"


def test_scan_company_uses_bytedance_api_scanner(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    def fake_fetch_page(
        self: object,
        career_page: CompanyCareerPage,
        *,
        offset: int,
    ) -> dict[str, object]:
        _ = self, career_page
        assert offset == 0
        return {
            "data": {
                "count": 2,
                "job_post_list": [
                    {
                        "id": "7639884334834862341",
                        "code": "A123",
                        "title": "Software Engineer Project Intern - 2026 Start (BS/MS)",
                        "description": "Build distributed systems.",
                        "requirement": "Currently pursuing a Bachelor's or Master's degree.",
                        "city_info": {
                            "en_name": "San Jose",
                            "parent": {
                                "en_name": "California",
                                "parent": {"en_name": "United States of America"},
                            },
                        },
                    },
                    {
                        "id": "7639881929596586245",
                        "code": "A456",
                        "title": "Student Researcher - 2026 Start (PhD)",
                        "description": "Build AI systems.",
                        "requirement": "Currently pursuing a PhD.",
                        "city_info": {
                            "en_name": "San Jose",
                            "parent": {
                                "en_name": "California",
                                "parent": {"en_name": "United States of America"},
                            },
                        },
                    },
                ],
            }
        }

    monkeypatch.setattr(
        "callumployed.services.company_scanners.ByteDanceApiScanner._fetch_page",
        fake_fetch_page,
    )

    with db.connect() as connection:
        company = add_company(connection, Company(name="ByteDance"))
        assert company.id is not None
        add_company_career_page(
            connection,
            CompanyCareerPage(
                company_id=company.id,
                url="https://joinbytedance.com/search?recruitment_id_list=202%2C301",
            ),
        )
        set_location_filter(connection, "usa")

    scan = asyncio.run(scan_workflow.scan_company(company))

    assert scan is not None
    assert scan["results"][0].candidates_scanned == 2
    assert {link.url for link in scan["results"][0].links} == {
        "https://joinbytedance.com/search/7639884334834862341"
    }
    with db.connect() as connection:
        roles = list_roles(connection)
        attempts = list_role_discovery_attempts(connection)

    assert len(roles) == 1
    assert roles[0].title == "Software Engineer Project Intern - 2026 Start (BS/MS)"
    assert roles[0].location == "San Jose, California, United States of America"
    assert len(attempts) == 1
    assert attempts[0].role_id == roles[0].id
    assert attempts[0].assessment_extraction_method == "html_heuristic"


def test_scan_company_uses_ashby_embedded_job_board(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)
    posting_id = "91e0686e-272a-4780-b33d-d7860b94a7b4"
    posting_description = (
        "<p>Build physical AI software systems.</p><p>Current PhD or MSc studies.</p>"
    )

    def fake_fetch_html(self: object, url: str) -> str:
        _ = self
        if url == "https://www.appliedintuition.com/careers#jobs-list":
            return f"""
            <html>
              <script>
                self.__next_f.push([
                  "jobs",
                  {{"jobUrl":"https://jobs.ashbyhq.com/applied/{posting_id}"}}
                ]);
              </script>
            </html>
            """
        if url == "https://jobs.ashbyhq.com/applied":
            return f"""
            <html>
              <script>
                window.__appData = {{
                  "organization": {{"name": "Applied Intuition"}},
                  "posting": null,
                  "jobBoard": {{
                    "jobPostings": [
                      {{
                        "id": "{posting_id}",
                        "title": "Research Intern - 3D Vision and Generation, Self-Driving",
                        "locationName": "Sunnyvale",
                        "employmentType": "Intern"
                      }},
                      {{
                        "id": "ffd8635d-43d5-4298-a29c-67eaa45c5a4a",
                        "title": "Android Software Engineer - Applications",
                        "locationName": "Sunnyvale",
                        "employmentType": "FullTime"
                      }}
                    ]
                  }}
                }};
              </script>
            </html>
            """
        if url == f"https://jobs.ashbyhq.com/applied/{posting_id}":
            return f"""
            <html>
              <head>
                <title>Research Intern - 3D Vision and Generation, Self-Driving</title>
                <script type="application/ld+json">
                  {{
                    "@context": "https://schema.org/",
                    "@type": "JobPosting",
                    "title": "Research Intern - 3D Vision and Generation, Self-Driving",
                    "description": "{posting_description}",
                    "identifier": {{
                      "@type": "PropertyValue",
                      "name": "Applied Intuition",
                      "value": "{posting_id}"
                    }},
                    "jobLocation": {{
                      "@type": "Place",
                      "address": {{
                        "@type": "PostalAddress",
                        "addressLocality": "Sunnyvale",
                        "addressRegion": "California",
                        "addressCountry": "United States"
                      }}
                    }},
                    "employmentType": "INTERN"
                  }}
                </script>
              </head>
              <body>Research Intern - 3D Vision and Generation, Self-Driving</body>
            </html>
            """
        raise AssertionError(f"unexpected Ashby URL: {url}")

    monkeypatch.setattr(
        "callumployed.services.company_scanners.AshbyJobBoardScanner._fetch_html",
        fake_fetch_html,
    )

    with db.connect() as connection:
        company = add_company(connection, Company(name="Applied Intuition"))
        assert company.id is not None
        add_company_career_page(
            connection,
            CompanyCareerPage(
                company_id=company.id,
                url="https://www.appliedintuition.com/careers#jobs-list",
            ),
        )
        set_location_filter(connection, "usa")
        set_include_graduate_degree_roles(connection, True)

    scan = asyncio.run(scan_workflow.scan_company(company))

    assert scan is not None
    assert scan["results"][0].candidates_scanned == 2
    assert {link.url for link in scan["results"][0].links} == {
        f"https://jobs.ashbyhq.com/applied/{posting_id}"
    }
    with db.connect() as connection:
        roles = list_roles(connection)
        attempts = list_role_discovery_attempts(connection)

    assert len(roles) == 1
    assert roles[0].title == "Research Intern - 3D Vision and Generation, Self-Driving"
    assert roles[0].location == "Sunnyvale, CA, United States"
    assert roles[0].posting_id == posting_id
    assert len(attempts) == 1
    assert attempts[0].assessment_extraction_method == "jobposting_structured_data"


def test_scan_company_uses_ashby_graphql_when_app_data_has_no_board(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)
    posting_id = "bff67718-1dbf-4d66-bcef-8b68d93d716f"

    def fake_fetch_html(self: object, url: str) -> str:
        _ = self
        if url == "https://cursor.com/careers":
            return f'<a href="https://jobs.ashbyhq.com/cursor/{posting_id}">Role</a>'
        if url == "https://jobs.ashbyhq.com/cursor":
            return """
            <script>
              window.__appData = {
                "organization": null,
                "posting": null,
                "jobBoard": null
              };
            </script>
            """
        if url == f"https://jobs.ashbyhq.com/cursor/{posting_id}":
            return f"""
            <script type="application/ld+json">
              {{
                "@context": "https://schema.org/",
                "@type": "JobPosting",
                "title": "Software Engineer Intern",
                "description": "Build model infrastructure.",
                "identifier": {{"value": "{posting_id}"}},
                "jobLocation": {{
                  "@type": "Place",
                  "address": {{
                    "@type": "PostalAddress",
                    "addressLocality": "San Francisco",
                    "addressRegion": "California",
                    "addressCountry": "United States"
                  }}
                }}
              }}
            </script>
            """
        raise AssertionError(f"unexpected Ashby URL: {url}")

    def fake_fetch_json(
        self: object,
        url: str,
        payload: dict[str, object],
    ) -> dict[str, object]:
        _ = self
        assert url == "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"
        assert payload["variables"] == {"organizationHostedJobsPageName": "cursor"}
        return {
            "data": {
                "jobBoardWithTeams": {
                    "jobPostings": [
                        {
                            "id": posting_id,
                            "title": "Software Engineer Intern",
                            "employmentType": "Intern",
                            "locationName": "San Francisco",
                        }
                    ]
                }
            }
        }

    monkeypatch.setattr(
        "callumployed.services.company_scanners.AshbyJobBoardScanner._fetch_html",
        fake_fetch_html,
    )
    monkeypatch.setattr(
        "callumployed.services.company_scanners.AshbyJobBoardScanner._fetch_json",
        fake_fetch_json,
    )

    with db.connect() as connection:
        company = add_company(connection, Company(name="Cursor"))
        assert company.id is not None
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://cursor.com/careers"),
        )
        set_location_filter(connection, "usa")

    scan = asyncio.run(scan_workflow.scan_company(company))

    assert scan is not None
    assert {link.url for link in scan["results"][0].links} == {
        f"https://jobs.ashbyhq.com/cursor/{posting_id}"
    }
    with db.connect() as connection:
        roles = list_roles(connection)

    assert len(roles) == 1
    assert roles[0].title == "Software Engineer Intern"


def test_scan_company_uses_direct_greenhouse_job_board(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    def fake_fetch_json(self: object, url: str) -> dict[str, object]:
        _ = self
        assert url == (
            "https://boards-api.greenhouse.io/v1/boards/"
            "aquaticcapitalmanagement/jobs?content=true"
        )
        return {
            "jobs": [
                {
                    "id": 8489233002,
                    "title": "Software Engineer, Intern (Summer 2027)",
                    "absolute_url": (
                        "https://job-boards.greenhouse.io/"
                        "aquaticcapitalmanagement/jobs/8489233002"
                    ),
                    "location": {"name": "Chicago"},
                    "content": "<p>Build Python systems.</p>",
                },
                {
                    "id": 8489186002,
                    "title": "Quantitative Researcher, Intern (Summer 2027)",
                    "absolute_url": (
                        "https://job-boards.greenhouse.io/"
                        "aquaticcapitalmanagement/jobs/8489186002"
                    ),
                    "location": {"name": "London"},
                    "content": "<p>Research markets.</p>",
                },
                {
                    "id": 8489226002,
                    "title": "Software Engineer, Early Career",
                    "absolute_url": (
                        "https://job-boards.greenhouse.io/"
                        "aquaticcapitalmanagement/jobs/8489226002"
                    ),
                    "location": {"name": "Chicago"},
                    "content": "<p>Build Python systems.</p>",
                },
            ]
        }

    monkeypatch.setattr(
        "callumployed.services.company_scanners.GreenhouseJobBoardScanner._fetch_json",
        fake_fetch_json,
    )

    with db.connect() as connection:
        company = add_company(connection, Company(name="Aquatic Capital Management"))
        assert company.id is not None
        add_company_career_page(
            connection,
            CompanyCareerPage(
                company_id=company.id,
                url=(
                    "https://job-boards.greenhouse.io/"
                    "aquaticcapitalmanagement?field_4227559002%5B%5D=34246011002"
                ),
            ),
        )
        set_location_filter(connection, "usa")

    scan = asyncio.run(scan_workflow.scan_company(company))

    assert scan is not None
    assert scan["results"][0].candidates_scanned == 3
    assert {link.url for link in scan["results"][0].links} == {
        "https://job-boards.greenhouse.io/aquaticcapitalmanagement/jobs/8489233002"
    }
    with db.connect() as connection:
        roles = list_roles(connection)
        attempts = list_role_discovery_attempts(connection)

    assert len(roles) == 1
    assert roles[0].title == "Software Engineer, Intern (Summer 2027)"
    assert roles[0].posting_id == "8489233002"
    assert len(attempts) == 1
    assert attempts[0].assessment_extraction_method == "ats_heuristic"


def test_scan_company_detects_embedded_greenhouse_api(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    def fake_fetch_html(self: object, url: str) -> str:
        _ = self
        assert url == "https://careers.example.com/jobs"
        return """
        <script>
          fetch('https://api.greenhouse.io/v1/boards/robinhood/jobs')
        </script>
        """

    def fake_fetch_json(self: object, url: str) -> dict[str, object]:
        _ = self
        assert url == "https://api.greenhouse.io/v1/boards/robinhood/jobs?content=true"
        return {
            "jobs": [
                {
                    "id": 1001,
                    "title": "Software Engineer Intern, Backend",
                    "absolute_url": "https://boards.greenhouse.io/robinhood/jobs/1001",
                    "location": {"name": "Menlo Park, CA"},
                    "content": "<p>Build backend services.</p>",
                }
            ]
        }

    monkeypatch.setattr(
        "callumployed.services.company_scanners.GreenhouseJobBoardScanner._fetch_html",
        fake_fetch_html,
    )
    monkeypatch.setattr(
        "callumployed.services.company_scanners.GreenhouseJobBoardScanner._fetch_json",
        fake_fetch_json,
    )

    with db.connect() as connection:
        company = add_company(connection, Company(name="Robinhood"))
        assert company.id is not None
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://careers.example.com/jobs"),
        )
        set_location_filter(connection, "usa")

    scan = asyncio.run(scan_workflow.scan_company(company))

    assert scan is not None
    assert {link.url for link in scan["results"][0].links} == {
        "https://boards.greenhouse.io/robinhood/jobs/1001"
    }
    with db.connect() as connection:
        roles = list_roles(connection)

    assert len(roles) == 1
    assert roles[0].title == "Software Engineer Intern, Backend"


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


def test_scan_company_closes_disinterested_roles_missing_from_scan(
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
        seen_role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Seen disinterested",
                role_url="https://example.com/jobs/software-engineering-intern-12345",
                role_status=RoleStatus.DISINTERESTED,
            ),
        )
        missing_role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Missing disinterested",
                role_url="https://example.com/jobs/missing",
                role_status=RoleStatus.DISINTERESTED,
            ),
        )
        if seen_role.id is None or missing_role.id is None:
            raise AssertionError("role ids missing")

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    with db.connect() as connection:
        seen_role = get_role(connection, seen_role.id)
        missing_role = get_role(connection, missing_role.id)

    assert seen_role.role_status is RoleStatus.DISINTERESTED
    assert missing_role.role_status is RoleStatus.CLOSED


def test_scan_company_skips_previously_rejected_role_candidates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)
    rendered_urls: list[str] = []

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        rendered_urls.append(url)
        if url.endswith("/careers"):
            return _page(url)
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Careers",
            html="<h1>Careers</h1><p>Company profile.</p>",
            visible_text="Careers Company profile.",
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

    first_scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )
    assert first_scan is not None

    second_scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )
    assert second_scan is not None

    third_scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            retry_rejected_roles=True,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )
    assert third_scan is not None

    assert rendered_urls == [
        "https://example.com/careers",
        "https://example.com/jobs/software-engineering-intern-12345",
        "https://example.com/careers",
        "https://example.com/careers",
        "https://example.com/jobs/software-engineering-intern-12345",
    ]
    assert first_scan["role_discovery_attempts"][0].assessment_is_role is False
    assert second_scan["role_discovery_attempts"] == []
    assert third_scan["role_discovery_attempts"][0].assessment_is_role is False
    second_scan_run = second_scan["scan_run"]
    assert second_scan_run.id is not None
    with db.connect() as connection:
        pages = list_scan_pages(connection, second_scan_run.id)
        if pages[0].id is None:
            raise AssertionError("scan page id missing")
        candidates = list_scan_candidates(connection, pages[0].id)

    by_url = {candidate.url: candidate for candidate in candidates}
    rejected = by_url["https://example.com/jobs/software-engineering-intern-12345"]
    assert rejected.confidence == 0.0
    assert rejected.selected is False
    assert "already rejected as non-role" in rejected.reasons


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
    assert attempts[0].assessment_location == "Vancouver, BC, Canada"
    assert attempts[0].assessment_posting_id == "REQ-123"
    assert attempts[0].assessment_extraction_method == "jobposting_structured_data"
    assert attempts[0].assessment_reasons == ["schema.org JobPosting structured data"]
    assert len(roles) == 1
    assert attempts[0].role_id == roles[0].id
    assert roles[0].title == "Software Engineering Intern"
    assert roles[0].role_url == "https://example.com/jobs/software-engineering-intern-12345"
    assert roles[0].location == "Vancouver, BC, Canada"
    assert roles[0].description == "Software Engineering Intern Vancouver Apply now"
    assert roles[0].posting_id == "REQ-123"
    assert roles[0].role_status is RoleStatus.DISCOVERED


def test_rescan_role_refreshes_existing_role_fields(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Careers",
            html="""
            <html>
              <head>
                <script type="application/ld+json">
                {
                  "@context": "https://schema.org",
                  "@type": "JobPosting",
                  "title": "Software Engineering Intern, Platform",
                  "jobLocation": {
                    "@type": "Place",
                    "address": {
                      "@type": "PostalAddress",
                      "addressLocality": "Vancouver",
                      "addressRegion": "BC",
                      "addressCountry": "CA"
                    }
                  },
                  "description": "Build software systems for production services.",
                  "identifier": {
                    "@type": "PropertyValue",
                    "value": "REQ-123"
                  }
                }
                </script>
              </head>
              <body><h1>Careers</h1></body>
            </html>
            """,
            visible_text="Careers Apply now Job description",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Old Intern",
                role_url="https://example.com/jobs/software-engineering-intern-platform",
            ),
        )
        assert role.id is not None
        role_id = role.id

    result = asyncio.run(scan_workflow.rescan_role(role_id))

    assert result["assessment"].is_role is True
    assert result["role"].title == "Software Engineering Intern, Platform"
    assert result["role"].location == "Vancouver, BC, Canada"
    assert result["role"].description == "Build software systems for production services."
    assert result["role"].posting_id == "REQ-123"
    with db.connect() as connection:
        refreshed = get_role(connection, role_id)
    assert refreshed.title == "Software Engineering Intern, Platform"


def test_rescan_role_refreshes_fields_even_when_discovery_filters_would_reject(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Careers",
            html="""
            <html>
              <head>
                <script type="application/ld+json">
                {
                  "@context": "https://schema.org",
                  "@type": "JobPosting",
                  "title": "Software Engineering Intern",
                  "jobLocation": {
                    "@type": "Place",
                    "address": {
                      "@type": "PostalAddress",
                      "addressLocality": "Palo Alto",
                      "addressRegion": "CA",
                      "addressCountry": "US"
                    }
                  },
                  "description": "Build software. Currently pursuing a graduate degree."
                }
                </script>
              </head>
              <body><h1>Careers</h1></body>
            </html>
            """,
            visible_text="Careers Apply now Job description",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        set_include_graduate_degree_roles(connection, False)
        company = add_company(connection, Company(name="Tesla"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Old Intern",
                role_url="https://example.com/jobs/software-engineering-intern",
                location="Old Location",
                description="Old description",
            ),
        )
        assert role.id is not None
        role_id = role.id

    result = asyncio.run(scan_workflow.rescan_role(role_id))

    assert result["assessment"].is_role is True
    assert result["assessment"].rejection_reason is None
    assert result["role"].title == "Software Engineering Intern"
    assert result["role"].location == "Palo Alto, CA, United States"
    assert result["role"].description == "Build software. Currently pursuing a graduate degree."


def test_rescan_role_does_not_overwrite_when_job_redirects_to_listing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _use_database(monkeypatch, tmp_path)

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        return RenderedPageState(
            url=url,
            final_url="https://www.tesla.com/careers/search/?site=US",
            title="Tesla Careers",
            html="""
            <html>
              <body>
                <h1>Software Engineering Intern</h1>
                <section>
                  United States of America State - Select - Tesla Careers Skip
                  Software Engineering Intern Palo Alto, California
                </section>
              </body>
            </html>
            """,
            visible_text=(
                "Software Engineering Intern United States of America "
                "State - Select - Tesla Careers Skip Palo Alto, California"
            ),
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Tesla"))
        assert company.id is not None
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Software Engineering Intern",
                role_url="https://www.tesla.com/careers/search/job/software-engineering-intern-123",
                location="Palo Alto, CA",
                description="Old description",
            ),
        )
        assert role.id is not None
        role_id = role.id

    result = asyncio.run(scan_workflow.rescan_role(role_id))

    assert result["assessment"].is_role is False
    assert "generic careers listing" in result["assessment"].rejection_reason
    assert result["role"].location == "Palo Alto, CA"
    assert result["role"].description == "Old description"


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
            visible_text="PhD Research Intern. Must be pursuing a PhD.",
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
              "description": "PhD Research Intern. Must be pursuing a PhD."
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


def test_scan_company_filters_locations_by_config(
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
                <a href="/jobs/software-engineer-montreal">Software Engineer Canada</a>
                <a href="/jobs/software-engineer-palo-alto">Software Engineer USA</a>
                """,
            )
        is_canada = "montreal" in url
        title = "Software Engineer Canada" if is_canada else "Software Engineer USA"
        location_json = (
            '{"@type":"Place","address":{"addressLocality":"Montréal",'
            '"addressRegion":"QC","addressCountry":"Canada"}}'
            if is_canada
            else '{"@type":"Place","address":{"addressLocality":"Palo Alto",'
            '"addressRegion":"CA","addressCountry":"United States"}}'
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
              "description": "Build software systems.",
              "jobLocation": {location_json}
            }}
            </script>
            """,
            visible_text="Build software systems.",
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
        set_internship_mode(connection, False)
        set_location_filter(connection, "canada")

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert scan["location_filter"] == "canada"
    with db.connect() as connection:
        roles = list_roles(connection)
        attempts = list_role_discovery_attempts(connection)

    assert {role.title for role in roles} == {"Software Engineer Canada"}
    rejected_attempts = [
        attempt
        for attempt in attempts
        if attempt.assessment_rejection_reason == "location filtered by app config"
    ]
    assert len(rejected_attempts) == 1
    assert rejected_attempts[0].title == "Software Engineer USA"
    assert "location filter" in rejected_attempts[0].assessment_reasons


def test_location_filter_treats_calgary_as_canada() -> None:
    assert scan_workflow._location_matches_filter("Calgary, AB", "canada")
    assert scan_workflow._location_matches_filter("Calgary, AB", "north_america")
    assert not scan_workflow._location_matches_filter("Calgary, AB", "usa")
    assert not scan_workflow._location_matches_filter("Calgary, AB", "international")


def test_location_filter_treats_san_jose_as_usa() -> None:
    assert scan_workflow._location_matches_filter("San Jose", "usa")
    assert scan_workflow._location_matches_filter("Seattle", "usa")
    assert scan_workflow._location_matches_filter("Los Angeles", "usa")
    assert scan_workflow._location_matches_filter("San Jose", "north_america")
    assert not scan_workflow._location_matches_filter("San Jose", "canada")
    assert not scan_workflow._location_matches_filter("San Jose", "international")


def test_software_keyword_filter_allows_foundation_model_roles() -> None:
    assert scan_workflow._has_software_keyword(
        "Student Researcher (LLM - Seed) - 2027 Start (BS/MS)",
        None,
    )
    assert scan_workflow._has_software_keyword(
        "Student Researcher (Speech Foundation Model - Seed) - 2027 Start",
        None,
    )


def test_software_keyword_filter_rejects_obvious_non_software_titles() -> None:
    assert not scan_workflow._has_software_keyword(
        "Customer Experience Associate (New Grad)",
        "Help customers use our financial platform and products.",
    )
    assert not scan_workflow._has_software_keyword(
        "Accounting Intern (Fall 2026)",
        "Use automation tools to support accounting workflows.",
    )


def test_graduate_degree_filter_allows_bachelors_or_masters_roles() -> None:
    assert not scan_workflow._is_graduate_degree_role(
        "Student Researcher (LLM - Seed) - 2027 Start (BS/MS)",
        "Minimum Qualifications: Currently pursuing a Bachelor's or Master's degree.",
    )
    assert scan_workflow._is_graduate_degree_role(
        "Payment Partnership Project Intern (Global Payment) - 2026 Start (MBA)",
        None,
    )
    assert not scan_workflow._is_graduate_degree_role(
        "Research Intern - 3D Vision and Generation, Self-Driving",
        "Must be pursuing a PhD (or MSc) in machine learning.",
    )
    assert not scan_workflow._is_graduate_degree_role(
        "Software Engineer, Intern (Summer 2027)",
        "Active student pursuing a BS, MS, or PhD in computer science.",
    )
    assert scan_workflow._is_graduate_degree_role(
        "Student Researcher - 2026 Start (PhD)",
        "Must be pursuing a PhD.",
    )


def test_scan_company_requires_intern_keywords_when_internship_mode_enabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    source_url = "https://apply.careers.microsoft.com/careers"

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url == source_url:
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Microsoft Careers",
                html="""
                <a href="/careers/job/software-engineering-intern-1">
                  Software Engineering Intern
                </a>
                <a href="/careers/job/senior-data-center-technician-2">
                  Senior Data Center Technician - Evening
                </a>
                """,
            )
        title = (
            "Software Engineering Intern"
            if "software-engineering-intern" in url
            else "Senior Data Center Technician - Evening"
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
        company = add_company(connection, Company(name="Microsoft"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url=source_url),
        )

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert {link.text for link in scan["results"][0].links} == {
        "Software Engineering Intern"
    }
    with db.connect() as connection:
        roles = list_roles(connection)

    assert {role.title for role in roles} == {"Software Engineering Intern"}


def test_scan_company_can_disable_internship_mode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    source_url = "https://example.com/careers?filter_seniority=Intern"

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url == source_url:
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Careers",
                html='<a href="/jobs/software-engineer-12345">Software Engineer</a>',
            )
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Software Engineer",
            html="""
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "Software Engineer",
              "description": "Build software systems."
            }
            </script>
            """,
            visible_text="Build software systems.",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url=source_url),
        )
        set_internship_mode(connection, False)

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert {link.text for link in scan["results"][0].links} == {"Software Engineer"}
    assert scan["internship_mode"] is False
    with db.connect() as connection:
        roles = list_roles(connection)
        attempts = list_role_discovery_attempts(connection)

    assert {role.title for role in roles} == {"Software Engineer"}
    assert len(attempts) == 1
    assert attempts[0].assessment_rejection_reason is None


def test_scan_company_allows_intern_source_role_when_listing_text_is_intern(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    source_url = "https://example.com/careers?filter_seniority=Intern"

    async def fake_render_careers_page(
        url: str,
        *,
        external_browser_port: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        if url == source_url:
            return RenderedPageState(
                url=url,
                final_url=url,
                title="Careers",
                html="""
                <a href="/jobs/software-engineering-intern-12345">
                  Software Engineering Intern
                </a>
                """,
            )
        return RenderedPageState(
            url=url,
            final_url=url,
            title="Software Engineer",
            html="""
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "JobPosting",
              "title": "Software Engineer",
              "description": "Software engineering internship."
            }
            </script>
            """,
            visible_text="Software engineering internship.",
        )

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url=source_url),
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
        attempts = list_role_discovery_attempts(connection)

    assert {role.title for role in roles} == {"Software Engineer"}
    assert len(attempts) == 1
    assert attempts[0].title == "Software Engineer"
    assert attempts[0].assessment_rejection_reason is None
    assert "intern keyword evidence: selected link text" in attempts[0].assessment_reasons


def test_intern_keyword_evidence_uses_role_url_not_source_url() -> None:
    assessment = RolePageAssessment(
        is_role=True,
        confidence=0.95,
        title="Software Engineer",
        extraction_method="jobposting_structured_data",
    )
    candidate = ScanCandidate(
        id=1,
        scan_page_id=1,
        url="https://example.com/jobs/software-engineering-intern-12345",
        source_url="https://example.com/careers?filter_seniority=Intern",
        text="Software Engineer",
        confidence=0.9,
        selected=True,
    )
    page = RenderedPageState(
        url=candidate.url,
        final_url=candidate.url,
        title="Software Engineer",
        html="",
    )

    assert (
        scan_workflow._intern_keyword_evidence_source(assessment, candidate, page)
        == "role URL"
    )

    candidate_without_role_evidence = candidate.model_copy(
        update={"url": "https://example.com/jobs/software-engineer-12345"}
    )
    page_without_role_evidence = page.model_copy(
        update={
            "url": candidate_without_role_evidence.url,
            "final_url": candidate_without_role_evidence.url,
        }
    )

    assert (
        scan_workflow._intern_keyword_evidence_source(
            assessment,
            candidate_without_role_evidence,
            page_without_role_evidence,
        )
        is None
    )


def test_refilter_collected_roles_creates_role_from_selected_link_intern_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        career_page = add_company_career_page(
            connection,
            CompanyCareerPage(
                company_id=company.id,
                url="https://example.com/careers?filter=intern",
            ),
        )
        scan_run = create_scan_run(connection, company.id)
        if scan_run.id is None:
            raise AssertionError("scan run id missing")
        scan_page = add_scan_page(
            connection,
            scan_run.id,
            CareersPageScanResult(
                source_url=career_page.url,
                final_url=career_page.url,
                candidates=[
                    ScoredLinkCandidate(
                        url="https://example.com/jobs/software-engineer",
                        source_url=career_page.url,
                        text="Software Engineering Intern",
                        confidence=0.9,
                    )
                ],
                links=[
                    DiscoveredJobLink(
                        url="https://example.com/jobs/software-engineer",
                        source_url=career_page.url,
                        text="Software Engineering Intern",
                        confidence=0.9,
                        discovery_method="heuristic",
                    )
                ],
                candidates_scanned=1,
                confidence=ExtractionConfidence.HIGH,
            ),
            company_career_page_id=career_page.id,
        )
        if scan_page.id is None:
            raise AssertionError("scan page id missing")
        candidates = add_scan_candidates(
            connection,
            scan_page.id,
            [
                ScoredLinkCandidate(
                    url="https://example.com/jobs/software-engineer",
                    source_url=career_page.url,
                    text="Software Engineering Intern",
                    confidence=0.9,
                )
            ],
            CareersPageScanResult(
                source_url=career_page.url,
                final_url=career_page.url,
                links=[
                    DiscoveredJobLink(
                        url="https://example.com/jobs/software-engineer",
                        source_url=career_page.url,
                        text="Software Engineering Intern",
                        confidence=0.9,
                        discovery_method="heuristic",
                    )
                ],
            ),
        )
        add_role_discovery_attempt(
            connection,
            RoleDiscoveryAttempt(
                scan_run_id=scan_run.id,
                scan_candidate_id=candidates[0].id or 0,
                company_id=company.id,
                url="https://example.com/jobs/software-engineer",
                final_url="https://example.com/jobs/software-engineer",
                title="Software Engineer",
                assessment_is_role=False,
                assessment_confidence=0.95,
                assessment_description="Software engineering internship.",
                assessment_extraction_method="jobposting_structured_data",
                assessment_rejection_reason=(
                    "intern keyword requirement filtered by app config"
                ),
                assessment_reasons=[
                    "schema.org JobPosting structured data",
                    "intern keyword requirement",
                ],
            ),
        )

    dry_run = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id)

    assert dry_run["dry_run"] is True
    assert dry_run["changed_attempts"] == 1
    assert dry_run["attempts"][0]["action"] == "create_role"
    with db.connect() as connection:
        assert list_roles(connection) == []

    applied = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id, apply=True)

    assert applied["roles_created"] == 1
    with db.connect() as connection:
        roles = list_roles(connection)
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)

    assert len(roles) == 1
    assert roles[0].title == "Software Engineer"
    assert attempts[0].assessment_is_role is True
    assert attempts[0].role_id == roles[0].id
    assert attempts[0].assessment_rejection_reason is None
    assert "intern keyword evidence: selected link text" in attempts[0].assessment_reasons


def test_refilter_collected_roles_does_not_use_source_url_as_intern_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        career_page = add_company_career_page(
            connection,
            CompanyCareerPage(
                company_id=company.id,
                url="https://example.com/careers?filter=intern",
            ),
        )
        scan_run = create_scan_run(connection, company.id)
        if scan_run.id is None:
            raise AssertionError("scan run id missing")
        scan_page = add_scan_page(
            connection,
            scan_run.id,
            CareersPageScanResult(
                source_url=career_page.url,
                final_url=career_page.url,
                candidates_scanned=1,
                confidence=ExtractionConfidence.HIGH,
            ),
            company_career_page_id=career_page.id,
        )
        if scan_page.id is None:
            raise AssertionError("scan page id missing")
        candidates = add_scan_candidates(
            connection,
            scan_page.id,
            [
                ScoredLinkCandidate(
                    url="https://example.com/jobs/software-engineer",
                    source_url=career_page.url,
                    text="Software Engineer",
                    confidence=0.9,
                )
            ],
            CareersPageScanResult(source_url=career_page.url, final_url=career_page.url),
        )
        add_role_discovery_attempt(
            connection,
            RoleDiscoveryAttempt(
                scan_run_id=scan_run.id,
                scan_candidate_id=candidates[0].id or 0,
                company_id=company.id,
                url="https://example.com/jobs/software-engineer",
                final_url="https://example.com/jobs/software-engineer",
                title="Software Engineer",
                assessment_is_role=False,
                assessment_confidence=0.95,
                assessment_description="Software engineering role.",
                assessment_extraction_method="jobposting_structured_data",
                assessment_rejection_reason=(
                    "intern keyword requirement filtered by app config"
                ),
                assessment_reasons=[
                    "schema.org JobPosting structured data",
                    "intern keyword requirement",
                ],
            ),
        )

    applied = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id, apply=True)

    assert applied["changed_attempts"] == 0
    with db.connect() as connection:
        assert list_roles(connection) == []
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)
    assert attempts[0].assessment_is_role is False


def test_refilter_collected_roles_treats_early_talent_source_as_intern_intent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Cloudflare"))
        if company.id is None:
            raise AssertionError("company id missing")
        career_page = add_company_career_page(
            connection,
            CompanyCareerPage(
                company_id=company.id,
                url="https://www.cloudflare.com/careers/jobs/?department=Early+Talent",
            ),
        )
        scan_run = create_scan_run(connection, company.id)
        if scan_run.id is None:
            raise AssertionError("scan run id missing")
        scan_page = add_scan_page(
            connection,
            scan_run.id,
            CareersPageScanResult(
                source_url=career_page.url,
                final_url=career_page.url,
                candidates_scanned=1,
                confidence=ExtractionConfidence.HIGH,
            ),
            company_career_page_id=career_page.id,
        )
        if scan_page.id is None:
            raise AssertionError("scan page id missing")
        candidates = add_scan_candidates(
            connection,
            scan_page.id,
            [
                ScoredLinkCandidate(
                    url=(
                        "https://www.cloudflare.com/careers/jobs/"
                        "distributed-systems-engineer/"
                    ),
                    source_url=career_page.url,
                    text="Distributed Systems Engineer",
                    confidence=0.9,
                )
            ],
            CareersPageScanResult(source_url=career_page.url, final_url=career_page.url),
        )
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Distributed Systems Engineer",
                role_url=(
                    "https://www.cloudflare.com/careers/jobs/"
                    "distributed-systems-engineer/"
                ),
            ),
        )
        if role.id is None:
            raise AssertionError("role id missing")
        add_role_discovery_attempt(
            connection,
            RoleDiscoveryAttempt(
                scan_run_id=scan_run.id,
                scan_candidate_id=candidates[0].id or 0,
                company_id=company.id,
                role_id=role.id,
                url=role.role_url,
                final_url=role.role_url,
                title=role.title,
                assessment_is_role=True,
                assessment_confidence=0.95,
                assessment_description="Build distributed systems.",
                assessment_extraction_method="jobposting_structured_data",
                assessment_reasons=["schema.org JobPosting structured data"],
            ),
        )

    dry_run = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id)

    assert dry_run["changed_attempts"] == 1
    assert dry_run["attempts"][0]["action"] == "archive_role"
    assert dry_run["attempts"][0]["reason"] == (
        "intern keyword requirement filtered by app config"
    )

    applied = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id, apply=True)

    assert applied["roles_archived"] == 1
    with db.connect() as connection:
        archived = get_role(connection, role.id)
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)

    assert archived.role_status is RoleStatus.ARCHIVED
    assert attempts[0].assessment_is_role is False
    assert attempts[0].assessment_rejection_reason == (
        "intern keyword requirement filtered by app config"
    )


def test_refilter_collected_roles_refreshes_stored_location_and_description(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Microsoft"))
        if company.id is None:
            raise AssertionError("company id missing")
        career_page = add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )
        scan_run = create_scan_run(connection, company.id)
        if scan_run.id is None:
            raise AssertionError("scan run id missing")
        scan_page = add_scan_page(
            connection,
            scan_run.id,
            CareersPageScanResult(
                source_url=career_page.url,
                final_url=career_page.url,
                candidates_scanned=1,
                confidence=ExtractionConfidence.HIGH,
            ),
            company_career_page_id=career_page.id,
        )
        if scan_page.id is None:
            raise AssertionError("scan page id missing")
        candidates = add_scan_candidates(
            connection,
            scan_page.id,
            [
                ScoredLinkCandidate(
                    url="https://example.com/jobs/software-engineering-intern",
                    source_url=career_page.url,
                    text="Software Engineering INTERN",
                    confidence=0.9,
                )
            ],
            CareersPageScanResult(source_url=career_page.url, final_url=career_page.url),
        )
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Software Engineering INTERN",
                role_url="https://example.com/jobs/software-engineering-intern",
                location="{'@type': 'Country', 'name': 'BR'}",
                description="Single Position Come build software.",
            ),
        )
        if role.id is None:
            raise AssertionError("role id missing")
        add_role_discovery_attempt(
            connection,
            RoleDiscoveryAttempt(
                scan_run_id=scan_run.id,
                scan_candidate_id=candidates[0].id or 0,
                company_id=company.id,
                role_id=role.id,
                url=role.role_url,
                final_url=role.role_url,
                title=role.title,
                assessment_is_role=True,
                assessment_confidence=0.95,
                assessment_location="{'@type': 'Country', 'name': 'BR'}",
                assessment_description="Single Position Come build software.",
                assessment_extraction_method="jobposting_structured_data",
                assessment_reasons=["schema.org JobPosting structured data"],
            ),
        )

    dry_run = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id)

    assert dry_run["changed_attempts"] == 1
    assert dry_run["attempts"][0]["action"] == "refresh_fields"

    applied = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id, apply=True)

    assert applied["changed_attempts"] == 1
    with db.connect() as connection:
        refreshed_role = get_role(connection, role.id)
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)
    assert refreshed_role.location == "Brazil"
    assert refreshed_role.description == "Come build software."
    assert attempts[0].assessment_location == "Brazil"
    assert attempts[0].assessment_description == "Come build software."


def test_refilter_collected_roles_recovers_location_from_stored_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)

    bad_location = (
        "S STREET VIEW PUZZLES DEPARTMENTS OPEN ROLES PROGRAMS; "
        "EVENTS INTERNSHIPS INTERVIEWING Join Jane Street Open roles"
    )
    stored_context = (
        "Accept All Reject All Software Engineer Internship, May-August "
        "LOCATION New York DEPARTMENT Technology TEAM Software Engineering Apply"
    )

    with db.connect() as connection:
        company = add_company(connection, Company(name="Jane Street"))
        if company.id is None:
            raise AssertionError("company id missing")
        career_page = add_company_career_page(
            connection,
            CompanyCareerPage(
                company_id=company.id,
                url="https://www.janestreet.com/join-jane-street/open-roles/?type=internship",
            ),
        )
        scan_run = create_scan_run(connection, company.id)
        if scan_run.id is None:
            raise AssertionError("scan run id missing")
        scan_page = add_scan_page(
            connection,
            scan_run.id,
            CareersPageScanResult(
                source_url=career_page.url,
                final_url=career_page.url,
                candidates_scanned=1,
                confidence=ExtractionConfidence.HIGH,
            ),
            company_career_page_id=career_page.id,
        )
        if scan_page.id is None:
            raise AssertionError("scan page id missing")
        candidates = add_scan_candidates(
            connection,
            scan_page.id,
            [
                ScoredLinkCandidate(
                    url="https://www.janestreet.com/join-jane-street/position/8599644002/",
                    source_url=career_page.url,
                    text="Software Engineer Internship",
                    confidence=0.9,
                )
            ],
            CareersPageScanResult(source_url=career_page.url, final_url=career_page.url),
        )
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Software Engineer Internship",
                role_url=(
                    "https://www.janestreet.com/join-jane-street/"
                    "position/8599644002/"
                ),
                location=bad_location,
            ),
        )
        if role.id is None:
            raise AssertionError("role id missing")
        add_role_discovery_attempt(
            connection,
            RoleDiscoveryAttempt(
                scan_run_id=scan_run.id,
                scan_candidate_id=candidates[0].id or 0,
                company_id=company.id,
                role_id=role.id,
                url=role.role_url,
                final_url=role.role_url,
                title=role.title,
                assessment_is_role=True,
                assessment_confidence=0.95,
                assessment_location=bad_location,
                assessment_description="Build software.",
                assessment_extraction_method="html_heuristic",
                assessment_reasons=["job-like page title"],
                visible_text_excerpt=stored_context,
            ),
        )

    dry_run = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id)

    assert dry_run["changed_attempts"] == 1
    assert dry_run["attempts"][0]["action"] == "refresh_fields"

    applied = scan_workflow.refilter_collected_roles(scan_run_id=scan_run.id, apply=True)

    assert applied["changed_attempts"] == 1
    with db.connect() as connection:
        refreshed_role = get_role(connection, role.id)
        attempts = list_role_discovery_attempts(connection, scan_run_id=scan_run.id)
    assert refreshed_role.location == "New York"
    assert attempts[0].assessment_location == "New York"


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


def test_scan_company_touches_rediscovered_existing_roles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)
    existing_url = "https://example.com/jobs/software-engineering-intern-12345"
    old_seen_at = "2026-01-01 00:00:00"

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
        role = add_role(
            connection,
            Role(
                company_id=company.id,
                title="Software Engineering Intern",
                role_url=existing_url,
            ),
        )
        if role.id is None:
            raise AssertionError("role id missing")
        connection.execute(
            """
            UPDATE roles
            SET last_seen_at = ?, updated_at = ?
            WHERE id = ?
            """,
            (old_seen_at, old_seen_at, role.id),
        )
        connection.commit()

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert any(
        candidate.url == existing_url and "already in database" in candidate.reasons
        for candidate in scan["results"][0].candidates
    )
    with db.connect() as connection:
        updated_role = get_role(connection, role.id)
        assert updated_role.last_seen_at is not None
        assert updated_role.updated_at is not None
        assert updated_role.last_seen_at.isoformat() != "2026-01-01T00:00:00"
        assert updated_role.updated_at.isoformat() != "2026-01-01T00:00:00"



def test_scan_company_increases_company_wait_and_retries_timeout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)
    render_timeouts: list[int | None] = []

    async def fake_render_careers_page(
        url: str,
        *,
        timeout_ms: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        render_timeouts.append(timeout_ms)
        if len(render_timeouts) == 1:
            raise NavigationError(f"Timed out while navigating to {url}")
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

    scan = asyncio.run(
        scan_workflow.scan_company(
            company,
            chat_model_factory=lambda _settings: EmptyStructuredModel(),
        )
    )

    assert scan is not None
    assert render_timeouts[:2] == [
        None,
        scan_workflow.browser.DEFAULT_TIMEOUT_MS
        + scan_workflow.COMPANY_TIMEOUT_RETRY_INCREMENT_MS,
    ]
    assert scan["company"].browser_extra_wait_ms == 1_000
    with db.connect() as connection:
        assert get_company(connection, company.id).browser_extra_wait_ms == 1_000


def test_scan_company_caps_timeout_wait_increases_per_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_database(monkeypatch, tmp_path)
    render_timeouts: list[int | None] = []

    async def fake_render_careers_page(
        url: str,
        *,
        timeout_ms: int | None = None,
        **_render_options: object,
    ) -> RenderedPageState:
        render_timeouts.append(timeout_ms)
        raise NavigationError(f"Timed out while navigating to {url}")

    monkeypatch.setattr(scan_workflow, "render_careers_page", fake_render_careers_page)

    with db.connect() as connection:
        company = add_company(connection, Company(name="Acme"))
        if company.id is None:
            raise AssertionError("company id missing")
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url="https://example.com/careers"),
        )

    with pytest.raises(NavigationError, match="Timed out while navigating"):
        asyncio.run(
            scan_workflow.scan_company(
                company,
                chat_model_factory=lambda _settings: EmptyStructuredModel(),
            )
        )

    assert render_timeouts == [
        None,
        scan_workflow.browser.DEFAULT_TIMEOUT_MS + 1_000,
        scan_workflow.browser.DEFAULT_TIMEOUT_MS + 2_000,
        scan_workflow.browser.DEFAULT_TIMEOUT_MS + 3_000,
    ]
    with db.connect() as connection:
        assert get_company(connection, company.id).browser_extra_wait_ms == 3_000
