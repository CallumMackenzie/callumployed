import asyncio
from datetime import datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from callumployed.agents.posting_link_classifier import (
    PostingLinkClassificationBatch,
    PostingLinkClassificationDecision,
    PostingLinkClassificationItem,
    PostingLinkClassificationResponse,
    PostingLinkClassifierAgent,
    build_chat_model,
    build_posting_link_agent_classifier,
    build_posting_link_classification_prompt,
    classify_posting_links,
)
from callumployed.config import LlmSettings
from callumployed.data.models import Company, CompanyCareerPage, ScanCandidate, ScanPage
from callumployed.webscraping.models import (
    DiscoveredJobLink,
    RenderedPageState,
    ScoredLinkCandidate,
)


def _classification_item(company_id: int = 1) -> PostingLinkClassificationItem:
    return PostingLinkClassificationItem.from_database(
        career_page=CompanyCareerPage(
            id=20,
            company_id=company_id,
            url="https://example.com/careers",
            label="Main",
            created_at=datetime(2026, 1, 1),
            updated_at=datetime(2026, 1, 2),
        ),
        scan_page=ScanPage(
            id=30,
            scan_run_id=40,
            company_career_page_id=20,
            source_url="https://example.com/careers",
            final_url="https://example.com/careers/search",
            title="Example Careers",
            candidates_scanned=7,
            confidence="medium",
            created_at=datetime(2026, 1, 3),
        ),
        candidate=ScanCandidate(
            id=50,
            scan_page_id=30,
            url="https://example.com/jobs/backend",
            source_url="https://example.com/careers/search",
            text="Backend Engineer",
            tag="a",
            css_id="job-1",
            css_classes=("posting-link", "primary"),
            aria_label="Backend Engineer job posting",
            title="Backend Engineer",
            surrounding_text="Backend Engineer Vancouver Apply now",
            confidence=0.78,
            reasons=["job-like URL path", "job-like text: backend"],
            selected=True,
            discovery_method="heuristic",
            created_at=datetime(2026, 1, 4),
        ),
    )


def test_posting_link_classification_batch_payload_uses_database_context_without_timing() -> None:
    batch = PostingLinkClassificationBatch.from_database(
        company=Company(
            id=1,
            name="Acme",
            notes="Internships are interesting.",
            prestige_tier="A",
            created_at=datetime(2026, 1, 1),
            updated_at=datetime(2026, 1, 2),
            external_browser_port=9222,
        ),
        items=[_classification_item()],
    )

    payload = batch.to_agent_payload()
    item = payload["items"][0]

    assert payload["company"] == {
        "id": 1,
        "name": "Acme",
        "notes": "Internships are interesting.",
        "prestige_tier": "A",
    }
    assert item["career_page"] == {
        "id": 20,
        "company_id": 1,
        "url": "https://example.com/careers",
        "label": "Main",
    }
    assert item["scan_page"]["final_url"] == "https://example.com/careers/search"
    assert item["candidate"]["css_classes"] == ["posting-link", "primary"]
    assert item["candidate"]["reasons"] == ["job-like URL path", "job-like text: backend"]
    assert "created_at" not in str(payload)
    assert "updated_at" not in str(payload)
    assert "external_browser_port" not in str(payload)


def test_posting_link_classification_batch_rejects_cross_company_items() -> None:
    with pytest.raises(ValidationError, match="one company"):
        PostingLinkClassificationBatch.from_database(
            company=Company(id=1, name="Acme"),
            items=[_classification_item(company_id=2)],
        )


def test_build_posting_link_classification_prompt_batches_candidates_for_one_company() -> None:
    batch = PostingLinkClassificationBatch.from_database(
        company=Company(id=1, name="Acme"),
        items=[_classification_item()],
    )

    prompt = build_posting_link_classification_prompt(batch)

    assert "The batch always belongs to one company." in prompt
    assert '"company_id": 1' in prompt
    assert '"url": "https://example.com/jobs/backend"' in prompt
    assert "Return only JSON" in prompt


def test_posting_link_classifier_agent_uses_settings_and_validates_response() -> None:
    batch = PostingLinkClassificationBatch.from_database(
        company=Company(id=1, name="Acme"),
        items=[_classification_item()],
    )

    calls: list[str] = []

    class FakeStructuredModel:
        async def ainvoke(self, prompt: object) -> PostingLinkClassificationResponse:
            assert isinstance(prompt, str)
            assert "Database context" in prompt
            calls.append(prompt)
            return PostingLinkClassificationResponse(
                decisions=[
                    PostingLinkClassificationDecision(
                        candidate_id=50,
                        url="https://example.com/jobs/backend",
                        is_job_posting=True,
                        confidence=0.94,
                        title="Backend Engineer",
                        location="Vancouver",
                        reasons=["Specific role URL with job title context."],
                    )
                ]
            )

    def fake_model_factory(settings: LlmSettings) -> FakeStructuredModel:
        assert settings.provider == "openai"
        assert settings.model == "gpt-4.1-mini"
        return FakeStructuredModel()

    agent = PostingLinkClassifierAgent(chat_model_factory=fake_model_factory)
    response = asyncio.run(agent.classify(batch))

    assert calls
    assert response.decisions[0].is_job_posting is True
    assert response.decisions[0].candidate_id == 50


def test_classify_posting_links_convenience_wrapper_uses_agent_system() -> None:
    batch = PostingLinkClassificationBatch.from_database(
        company=Company(id=1, name="Acme"),
        items=[_classification_item()],
    )

    class FakeStructuredModel:
        async def ainvoke(self, prompt: object) -> PostingLinkClassificationResponse:
            assert isinstance(prompt, str)
            assert "You classify scraped links" in prompt
            return PostingLinkClassificationResponse(decisions=[])

    response = asyncio.run(
        classify_posting_links(batch, chat_model_factory=lambda _settings: FakeStructuredModel())
    )

    assert response.decisions == []


def test_build_posting_link_agent_classifier_maps_agent_decisions_to_links() -> None:
    calls: list[str] = []

    class FakeStructuredModel:
        async def ainvoke(self, prompt: object) -> PostingLinkClassificationResponse:
            assert isinstance(prompt, str)
            calls.append(prompt)
            return PostingLinkClassificationResponse(
                decisions=[
                    PostingLinkClassificationDecision(
                        url="https://example.com/openings/software-intern",
                        is_job_posting=True,
                        confidence=0.91,
                        title="Software Intern",
                        reasons=["Specific role page."],
                    ),
                    PostingLinkClassificationDecision(
                        url="https://example.com/careers",
                        is_job_posting=False,
                        confidence=0.12,
                        reasons=["Generic careers page."],
                    ),
                ]
            )

    classifier = build_posting_link_agent_classifier(
        company=Company(id=1, name="Acme"),
        career_page=CompanyCareerPage(id=20, company_id=1, url="https://example.com/careers"),
        scan_run_id=30,
        chat_model_factory=lambda _settings: FakeStructuredModel(),
    )

    links: list[DiscoveredJobLink] = asyncio.run(
        classifier(
            [
                ScoredLinkCandidate(
                    url="https://example.com/openings/software-intern",
                    source_url="https://example.com/careers",
                    text="Software Intern",
                    confidence=0.25,
                    reasons=["job-like text: software, intern"],
                ),
                ScoredLinkCandidate(
                    url="https://example.com/careers",
                    source_url="https://example.com/careers",
                    text="Careers",
                    confidence=0.08,
                    reasons=["job-like text: career"],
                ),
            ],
            RenderedPageState(
                url="https://example.com/careers",
                final_url="https://example.com/careers",
                title="Acme Careers",
                html="",
            ),
        )
    )

    assert calls
    assert "Acme" in calls[0]
    assert len(links) == 1
    assert links[0].url == "https://example.com/openings/software-intern"
    assert links[0].confidence == 0.91
    assert links[0].discovery_method == "agent"


def test_llm_settings_reads_provider_and_model_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CALLUMPLOYED_LLM_PROVIDER", "openai")
    monkeypatch.setenv("CALLUMPLOYED_LLM_MODEL", "gpt-4.1-mini")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    settings = LlmSettings()

    assert settings.provider == "openai"
    assert settings.model == "gpt-4.1-mini"
    assert settings.openai_api_key is not None


def test_llm_settings_reads_provider_and_model_from_dotenv(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CALLUMPLOYED_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("CALLUMPLOYED_LLM_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text(
        "CALLUMPLOYED_LLM_PROVIDER=openai\n"
        "CALLUMPLOYED_LLM_MODEL=gpt-test-model\n"
        "OPENAI_API_KEY=test-key\n",
        encoding="utf-8",
    )

    settings = LlmSettings()

    assert settings.provider == "openai"
    assert settings.model == "gpt-test-model"
    assert settings.openai_api_key is not None


def test_build_chat_model_rejects_unsupported_provider() -> None:
    with pytest.raises(ValueError, match="unsupported LLM provider"):
        build_chat_model(LlmSettings(provider="bedrock"))
