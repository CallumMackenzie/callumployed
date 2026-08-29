import asyncio
import json
from datetime import datetime
from pathlib import Path

import httpx
import pytest
from pydantic import BaseModel, ValidationError

from callumployed.agents.codex_chat_model import CodexStructuredChatModel
from callumployed.agents.cover_letter import (
    ApplicantProfile,
    CoverLetterAgent,
    build_cover_letter_prompt,
    find_named_hiring_contact,
)
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
from callumployed.agents.resume_feedback import (
    ResumeFeedbackAgent,
    ResumeFeedbackResponse,
    build_resume_feedback_prompt,
)
from callumployed.agents.resume_tweaker import build_resume_tweak_prompt
from callumployed.agents.role_chat import RoleChatMessage, build_role_chat_prompt
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


def test_resume_feedback_prompt_includes_verdict_rules_and_context() -> None:
    prompt = build_resume_feedback_prompt(
        role={
            "id": 1,
            "company_id": 2,
            "title": "Backend Intern",
            "role_url": "https://example.com/jobs/backend",
            "location": "Vancouver",
            "description": "Python distributed systems internship",
        },
        resume_content="Python systems projects in LaTeX",
    )

    assert '"ready_to_apply"' in prompt
    assert '"tweak"' in prompt
    assert "add skills matching the posting" in prompt
    assert "change wording to align with posting" in prompt
    assert "tweak_prompt" in prompt
    assert "Do not return exact LaTeX additions" in prompt
    assert "resume_context" in prompt
    assert "job_context" in prompt
    assert "Python distributed systems internship" in prompt
    assert "Python systems projects in LaTeX" in prompt


def test_resume_feedback_prompt_includes_other_experience_context() -> None:
    prompt = build_resume_feedback_prompt(
        role={
            "id": 1,
            "company_id": 2,
            "title": "Backend Intern",
            "role_url": "https://example.com/jobs/backend",
            "location": "Vancouver",
            "description": "Python distributed systems internship",
        },
        resume_content="Python systems projects in LaTeX",
        other_experience_context=[
            {
                "filename": "projects.md",
                "content": "Built an internal scheduler with Kubernetes and Redis.",
                "updated_at": "2026-07-29T12:00:00Z",
            }
        ],
    )

    assert "other_experience_context" in prompt
    assert "secondary evidence" in prompt
    assert "may or" in prompt
    assert "Never assume they are visible" in prompt
    assert "truthful tweak prompt" in prompt
    assert "ready_to_apply" in prompt
    assert "Built an internal scheduler with Kubernetes and Redis." in prompt


def test_cover_letter_prompt_includes_resume_job_and_tool_results() -> None:
    prompt = build_cover_letter_prompt(
        applicant_profile=ApplicantProfile(
            first_name="Jake",
            last_name="Yeo",
            email="jake@example.com",
            institution="University of Victoria",
            degree="Bachelor of Software Engineering",
        ),
        role={
            "id": 1,
            "company_name": "Acme",
            "title": "Backend Intern",
            "role_url": "https://example.com/jobs/backend",
            "location": "Vancouver",
            "description": "Python distributed systems internship",
        },
        resume_content="Python systems resume",
        other_experience_context=[
            {
                "filename": "projects.md",
                "content": "Built a BLE sensor network for motion analysis.",
                "updated_at": "2026-07-29T12:00:00Z",
            }
        ],
        role_context=[
            {
                "label": "requirements",
                "content": "Python distributed systems internship",
            }
        ],
        tweaks="Make the tone warmer and emphasize ML infrastructure.",
        cover_letter_examples=[
            {
                "id": 7,
                "filename": "stripe.tex",
                "content": "Dear Stripe, I build backend systems.",
                "similarity": 0.8,
            }
        ],
        previous_cover_letter_latex=(
            "\\documentclass{letter}\\begin{document}Old draft\\end{document}"
        ),
    )

    assert "resume_context" in prompt
    assert "job_context" in prompt
    assert "other_experience_context" in prompt
    assert "projects / employment history" in prompt
    assert "may or may not already" in prompt
    assert "Built a BLE sensor network for motion analysis." in prompt
    assert "cover_letter_example_tool_results" in prompt
    assert '"description": "Python distributed systems internship"' in prompt
    assert "Python distributed systems internship" in prompt
    assert "Dear Stripe" in prompt
    assert "fits on one page" in prompt
    assert "325-400 words" in prompt
    assert "1in margins" in prompt
    assert "sender block, recipient/date block" in prompt
    assert "sender/contact header must contain only" in prompt
    assert "applicant_profile" in prompt
    assert "Jake Yeo" in prompt
    assert "jake@example.com" in prompt
    assert "University of Victoria" in prompt
    assert "Bachelor of Software Engineering" in prompt
    assert "Callum Mackenzie" not in prompt
    assert "callum@camackenzie.com" not in prompt
    assert "do not include the user's personal website, GitHub, LinkedIn" in prompt
    assert "Integrate the context deliberately" in prompt
    assert "tailor every body paragraph to the specific position" in prompt
    assert "sent unchanged to another company" in prompt
    assert "too generic" in prompt
    assert "must name the exact company and role" in prompt
    assert "specific responsibilities or requirements from the posting" in prompt
    assert "avoid generic filler" in prompt
    assert "exactly four cohesive body paragraphs" in prompt
    assert "how the role was found or a referral only when" in prompt
    assert "task or problem, the action taken, and the result delivered" in prompt
    assert "Never invent a number or metric" in prompt
    assert "soft skills through concrete evidence" in prompt
    assert "only when the posting asks for AI" in prompt
    assert "one evidence paragraph must discuss source-supported AI work" in prompt
    assert "Hermes or a relevant AI-enabled application by name" in prompt
    normalized_prompt = " ".join(prompt.split())
    assert "independently directed AI-enabled application" in normalized_prompt
    assert "merely listing coding assistants used in an unrelated job" in normalized_prompt
    assert "company values, mission, product, domain, or recent work" in prompt
    assert "thank the reader for their time" in prompt
    assert "invite an interview or conversation" in prompt
    assert "Use this exact LaTeX scaffold" in prompt
    assert "named hiring contact" in prompt
    assert "Dear Hiring Manager" in prompt
    assert prompt.count("Dear Hiring Team") == 1
    assert "\\documentclass[letterpaper,11pt]{article}" in prompt
    assert "\\pdfgentounicode" in prompt
    assert "plain ASCII apostrophes and quotes" in prompt
    assert "never use em dashes" in prompt
    assert "\\textemdash" in prompt
    assert "R\\&D" in prompt
    assert "50\\%" in prompt
    assert "regeneration_tweaks" in prompt
    assert "Make the tone warmer and emphasize ML infrastructure." in prompt
    assert "previous_cover_letter_context" in prompt
    assert "revise this prior draft according to regeneration_tweaks" in prompt
    assert "Old draft" in prompt


def test_cover_letter_prompt_requires_plain_language_project_introductions() -> None:
    prompt = build_cover_letter_prompt(
        applicant_profile=ApplicantProfile(first_name="Jake", last_name="Yeo"),
        role={
            "company_name": "Acme",
            "title": "Software Engineering Intern",
            "description": "Build user-facing software.",
        },
        resume_content="Built Nourish, a photo-first nutrition PWA.",
        other_experience_context=[
            {
                "filename": "nourish.md",
                "content": (
                    "Nourish is a photo-first nutrition app that lets users review "
                    "meal estimates before saving them to a diary."
                ),
            }
        ],
        cover_letter_examples=[],
        previous_cover_letter_latex=(
            "\\documentclass{article}\\begin{document}I built Nourish.\\end{document}"
        ),
        tweaks="Make the project example clearer.",
    )

    normalized_prompt = " ".join(prompt.split())
    assert "recruiter cannot be expected to recognize a project name" in normalized_prompt
    assert "first mention of every named project" in normalized_prompt
    assert "recognizable product category" in normalized_prompt
    assert "primary user or system purpose" in normalized_prompt
    assert "same sentence" in normalized_prompt
    assert "do not leave a project as an unexplained proper noun" in normalized_prompt
    assert "previous draft" in normalized_prompt


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        ("Hiring Manager: Jane Doe\nApply by Friday.", "Jane Doe"),
        ("Recruiter - Jordan Lee\nApplications are open.", "Jordan Lee"),
        ("Questions? Contact Priya Shah for details.", "Priya Shah"),
        ("Recruiter: Apply Now\nApplications are open.", None),
        ("Recruiter: Full Time Position\nApplications are open.", None),
        ("Recruiter: Senior Software Engineer\nApplications are open.", None),
        ("Recruiter: Chief Technology Officer\nApplications are open.", None),
        ("Contact: General Counsel\nApplications are open.", None),
        ("Hiring Manager: Legal Counsel\nApplications are open.", None),
        ("Recruiter: Marketing Manager\nApplications are open.", None),
        ("Contact: Technical Recruiter\nApplications are open.", None),
        ("Your recruiter can explain compensation.", None),
    ],
)
def test_find_named_hiring_contact_requires_an_explicit_person(
    description: str, expected: str | None
) -> None:
    assert find_named_hiring_contact(description) == expected


def test_applicant_profile_omits_unset_optional_sender_lines() -> None:
    profile = ApplicantProfile(first_name="Jake", institution="R&D University")

    assert profile.full_name == "Jake"
    assert profile.latex_sender_block == "Jake\\\\\nR\\&D University"
    assert "\\\\\n\\\\" not in profile.latex_sender_block


def test_applicant_profile_places_phone_below_email_in_sender_block() -> None:
    profile = ApplicantProfile(
        first_name="Callum",
        last_name="Mackenzie",
        email="callum@example.com",
        phone="+1 (250) 555-0123",
    )

    assert profile.latex_sender_block.endswith(
        "callum@example.com\\\\\n+1 (250) 555-0123"
    )


def test_resume_tweak_prompt_includes_existing_resume_and_tweaks() -> None:
    prompt = build_resume_tweak_prompt(
        role={
            "id": 1,
            "company_id": 2,
            "company_name": "Acme",
            "title": "Backend Intern",
            "role_url": "https://example.com/jobs/backend",
            "location": "Vancouver",
            "description": "Python distributed systems internship",
        },
        resume_content="\\documentclass{article}\\begin{document}Python systems\\end{document}",
        tweaks="Emphasize distributed systems without inventing metrics.",
        other_experience_context=[
            {
                "filename": "projects.md",
                "content": "Built a Kubernetes scheduler.",
                "updated_at": "2026-01-01T00:00:00",
            }
        ],
    )

    assert "regeneration_tweaks" in prompt
    assert "Emphasize distributed systems" in prompt
    assert "resume_context" in prompt
    assert "Built a Kubernetes scheduler" in prompt
    assert "full," in prompt
    assert "compilable replacement LaTeX document" in prompt
    assert "rewrite bullets and descriptions" in prompt
    assert "preserve every employer, role, project, education entry, date, and link" in prompt
    assert "strongest source-supported accomplishments" in prompt


def test_role_chat_prompt_includes_role_material_contexts() -> None:
    prompt = build_role_chat_prompt(
        role={
            "id": 1,
            "company_id": 2,
            "company_name": "Acme",
            "title": "Backend Intern",
            "role_url": "https://example.com/jobs/backend",
            "location": "Vancouver",
            "description": "Python distributed systems internship",
            "role_status": "interested",
        },
        resume_content="Python systems resume",
        cover_letter_content="Dear Acme, I build systems.",
        employment_history_context=[
            {
                "filename": "projects.md",
                "content": "Built a Kubernetes scheduler.",
                "updated_at": "2026-01-01T00:00:00",
            }
        ],
        messages=[
            RoleChatMessage(role="user", content="What should I emphasize?"),
        ],
    )

    assert "role_context" in prompt
    assert "resume_context" in prompt
    assert "cover_letter_context" in prompt
    assert "employment_history_context" in prompt
    assert "chat_history" in prompt
    assert "Backend Intern" in prompt
    assert "Python systems resume" in prompt
    assert "Dear Acme" in prompt
    assert "Built a Kubernetes scheduler" in prompt
    assert "What should I emphasize?" in prompt


def test_cover_letter_agent_queries_example_tool_and_passes_documents() -> None:
    calls: list[str] = []
    prompts: list[str] = []

    def search_tool(query: str, *, limit: int = 3) -> list[dict[str, object]]:
        calls.append(query)
        return [
            {
                "id": 7,
                "filename": "backend-cover.tex",
                "content": "Dear Backend Team, I write about distributed systems.",
                "similarity": 0.91,
            }
        ]

    class FakeCoverLetterModel:
        async def ainvoke(self, prompt: object) -> dict[str, object]:
            assert isinstance(prompt, str)
            prompts.append(prompt)
            return {
                "latex": (
                    "\\documentclass{letter}\\begin{document}"
                    "AI infrastructure \u2014 distributed systems --- backend tooling "
                    "\\textemdash{} platform work"
                    "\\end{document}"
                ),
                "summary": "drafted \u2014 no edits",
                "example_ids": [7],
            }

    response = asyncio.run(
        CoverLetterAgent(
            search_tool=search_tool,
            chat_model_factory=lambda _settings: FakeCoverLetterModel(),
        ).generate(
            role={
                "id": 1,
                "company_name": "Acme",
                "title": "Backend Intern",
                "location": "Vancouver",
                "description": "Python distributed systems internship",
            },
            resume_content="Python backend resume",
            other_experience_context=[
                {
                    "filename": "projects.md",
                    "content": "Built Kubernetes-backed internal scheduling tools.",
                    "updated_at": "2026-07-29T12:00:00Z",
                }
            ],
            tweaks="Cut one paragraph and make the intro more direct.",
            previous_cover_letter_latex=(
                "\\documentclass{letter}\\begin{document}Previous draft body\\end{document}"
            ),
        )
    )

    assert len(calls) == 2
    assert response.example_ids == [7]
    assert "\u2014" not in response.latex
    assert "---" not in response.latex
    assert "\\textemdash" not in response.latex
    assert "\u2014" not in response.summary
    assert "Dear Backend Team" in prompts[0]
    assert "cover_letter_example_tool_results" in prompts[0]
    assert "other_experience_context" in prompts[0]
    assert "Built Kubernetes-backed internal scheduling tools." in prompts[0]
    assert "primary writing-style reference" in prompts[0]
    assert "never use em dashes" in prompts[0]
    assert "fits on one page" in prompts[0]
    assert "Cut one paragraph and make the intro more direct." in prompts[0]
    assert "previous_cover_letter_context" in prompts[0]
    assert "Previous draft body" in prompts[0]


def test_cover_letter_agent_bounds_large_retrieved_context() -> None:
    queries: list[str] = []
    prompts: list[str] = []
    huge_context = "START " + ("context " * 80000) + " END"

    def search_tool(query: str, *, limit: int = 3) -> list[dict[str, object]]:
        queries.append(query)
        return [
            {
                "id": 7,
                "filename": "large-example.tex",
                "content": huge_context,
                "knowledge_text": huge_context,
                "similarity": 0.9,
            }
        ]

    class FakeCoverLetterModel:
        async def ainvoke(self, prompt: object) -> dict[str, object]:
            assert isinstance(prompt, str)
            prompts.append(prompt)
            return {
                "latex": "\\documentclass{letter}\\begin{document}Draft\\end{document}",
                "summary": "drafted",
                "example_ids": [7],
            }

    asyncio.run(
        CoverLetterAgent(
            search_tool=search_tool,
            chat_model_factory=lambda _settings: FakeCoverLetterModel(),
        ).generate(
            role={
                "id": 1,
                "company_name": "Acme",
                "title": "Backend Intern",
                "description": huge_context,
            },
            resume_content=huge_context,
            other_experience_context=[{"filename": "history.md", "content": huge_context}],
        )
    )

    assert max(map(len, queries)) <= 24000
    assert len(prompts[0]) <= 160000
    assert '"knowledge_text"' not in prompts[0]
    assert "START" in prompts[0]
    assert "END" in prompts[0]


def test_resume_feedback_prompt_includes_recommendation_history() -> None:
    prompt = build_resume_feedback_prompt(
        role={
            "id": 1,
            "company_id": 2,
            "title": "Backend Intern",
            "role_url": "https://example.com/jobs/backend",
            "location": "Vancouver",
            "description": "Python distributed systems internship",
        },
        resume_content="Python systems projects in LaTeX",
        knowledge_base=[
            {
                "response": "ignored",
                "comment": "do not suggest generic skills blocks",
                "role_title": "Backend Intern",
                "feedback_title": "add skills matching the posting: Kubernetes",
                "feedback_detail": "add Kubernetes where supported",
                "knowledge_text": "user ignored this because it was unsupported",
                "similarity": 0.82,
            }
        ],
    )

    assert "recommendation_knowledge_base" in prompt
    assert "ignored feedback means a similar recommendation was not useful" in prompt
    assert "strong negative examples" in prompt
    assert "prefer specific user comments" in prompt
    assert "do not suggest generic skills blocks" in prompt
    assert "user ignored this because it was unsupported" in prompt


def test_resume_feedback_response_requires_known_verdict() -> None:
    response = ResumeFeedbackResponse.model_validate(
        {"verdict": "ready_to_apply", "overview": "fits well", "feedback_items": []}
    )

    assert response.verdict == "ready_to_apply"

    with pytest.raises(ValidationError):
        ResumeFeedbackResponse.model_validate(
            {"verdict": "maybe", "overview": "unclear", "feedback_items": []}
        )

    with pytest.raises(ValidationError):
        ResumeFeedbackResponse.model_validate(
            {
                "verdict": "tweak",
                "overview": "needs work",
                "feedback_items": [
                    {
                        "label": "generic",
                        "title": "be better",
                        "detail": "improve the resume",
                    }
                ],
            }
        )


def test_resume_feedback_agent_normalizes_operation_titles() -> None:
    class FakeResumeFeedbackModel:
        async def ainvoke(self, _input: object) -> dict[str, object]:
            return {
                "verdict": "tweak",
                "overview": "needs tailoring",
                "feedback_items": [
                    {
                        "label": "add_skills",
                        "title": "Add specific tech keywords from job posting",
                        "detail": "mention supported skills from the posting",
                        "tweak_prompt": (
                            "Revise the resume to emphasize existing Python backend "
                            "systems work for this posting."
                        ),
                    },
                    {
                        "label": "change_wording",
                        "title": "Change wording to align with posting: distributed systems",
                        "detail": "rewrite one bullet around distributed systems",
                        "tweak_prompt": (
                            "Tune the existing Python systems bullet toward distributed systems."
                        ),
                    },
                ],
            }

    response = asyncio.run(
        ResumeFeedbackAgent(
            chat_model_factory=lambda _settings: FakeResumeFeedbackModel()
        ).evaluate(
            role={"id": 1, "title": "Backend Intern"},
            resume_content="Python systems",
        )
    )

    assert response.feedback_items[0].title == (
        "add skills matching the posting: Add specific tech keywords from job posting"
    )
    assert response.feedback_items[1].title == (
        "change wording to align with posting: distributed systems"
    )
    assert response.feedback_items[1].tweak_prompt == (
        "Tune the existing Python systems bullet toward distributed systems."
    )


def test_resume_feedback_agent_surfaces_feedback_without_tweak_prompt() -> None:
    class FakeResumeFeedbackModel:
        async def ainvoke(self, _input: object) -> dict[str, object]:
            return {
                "verdict": "tweak",
                "overview": "needs tailoring",
                "feedback_items": [
                    {
                        "label": "add_skills",
                        "title": "add skills matching the posting: distributed systems",
                        "detail": (
                            "distributed systems appears important but is not backed by "
                            "the current resume."
                        ),
                        "tweak_prompt": None,
                    },
                    {
                        "label": "change_wording",
                        "title": "change wording to align with posting: Linux C++",
                        "detail": (
                            "Linux C++ may be relevant if there is supporting project context."
                        ),
                        "tweak_prompt": "",
                    },
                ],
            }

    response = asyncio.run(
        ResumeFeedbackAgent(
            chat_model_factory=lambda _settings: FakeResumeFeedbackModel()
        ).evaluate(
            role={"id": 1, "title": "Backend Intern"},
            resume_content="Python systems",
        )
    )

    assert response.verdict == "tweak"
    assert len(response.feedback_items) == 2
    assert response.feedback_items[0].tweak_prompt is None
    assert response.feedback_items[1].tweak_prompt is None


def test_resume_feedback_agent_keeps_nonactionable_move_emphasis_feedback() -> None:
    class FakeResumeFeedbackModel:
        async def ainvoke(self, _input: object) -> dict[str, object]:
            return {
                "verdict": "tweak",
                "overview": "needs tailoring",
                "feedback_items": [
                    {
                        "label": "move_emphasis",
                        "title": "move ai platform development experience earlier",
                        "detail": (
                            "position the Amazon AI platform work at the top of the "
                            "experience section."
                        ),
                        "tweak_prompt": None,
                    }
                ],
            }

    response = asyncio.run(
        ResumeFeedbackAgent(
            chat_model_factory=lambda _settings: FakeResumeFeedbackModel()
        ).evaluate(
            role={"id": 1, "title": "Backend Intern"},
            resume_content=(
                "\\section{Experience}\n"
                "\\textbf{Amazon} -- Software Development Engineer Intern\n"
                "\\textbf{General Dynamics} -- Embedded Software Engineer Co-op\n"
            ),
        )
    )

    assert response.verdict == "tweak"
    assert len(response.feedback_items) == 1
    assert response.feedback_items[0].tweak_prompt is None


def test_posting_link_classification_batch_payload_uses_database_context_without_timing() -> None:
    batch = PostingLinkClassificationBatch.from_database(
        company=Company(
            id=1,
            name="Acme",
            notes="Internships are interesting.",
            prestige_tier="A",
            created_at=datetime(2026, 1, 1),
            updated_at=datetime(2026, 1, 2),
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
        assert settings.model == "gpt-5.6-terra"
        return FakeStructuredModel()

    agent = PostingLinkClassifierAgent(
        settings=LlmSettings(provider="openai", model="gpt-5.6-terra"),
        chat_model_factory=fake_model_factory,
    )
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


def test_build_chat_model_supports_codex_without_changing_openai_configuration() -> None:
    model = build_chat_model(
        LlmSettings(provider="codex", codex_model="gpt-5.3-codex")
    )

    assert model.__class__.__name__ == "CodexStructuredChatModel"
    assert model.model == "gpt-5.3-codex"


def test_codex_subscription_provider_posts_structured_request_without_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_path = tmp_path / "auth.json"
    auth_path.write_text(
        json.dumps(
            {
                "auth_mode": "chatgpt",
                "tokens": {
                    "access_token": "access-token",
                    "refresh_token": "refresh-token",
                    "account_id": "account-123",
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("CALLUMPLOYED_CHATGPT_AUTH_PATH", str(auth_path))
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        body = (
            'data: {"type":"response.output_text.delta","delta":"{\\"accepted\\":"}\n\n'
            'data: {"type":"response.output_text.delta","delta":"true}"}\n\n'
            'data: {"type":"response.completed","response":{"id":"response-1"}}\n\n'
        )
        return httpx.Response(200, text=body)

    class Result(BaseModel):
        accepted: bool

    model = CodexStructuredChatModel(
        output_model=Result,
        model="gpt-5.6-terra",
        transport=httpx.MockTransport(handler),
    )
    result = asyncio.run(model.ainvoke("Return an accepted result"))

    assert result == Result(accepted=True)
    assert len(requests) == 1
    request = requests[0]
    assert request.url == "https://chatgpt.com/backend-api/codex/responses"
    assert request.headers["authorization"] == "Bearer access-token"
    assert request.headers["chatgpt-account-id"] == "account-123"
    payload = json.loads(request.content)
    assert payload["model"] == "gpt-5.6-terra"
    assert payload["stream"] is True
    assert payload["text"]["format"]["type"] == "json_schema"


def test_codex_subscription_provider_refreshes_expired_access_token(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_path = tmp_path / "auth.json"
    auth_path.write_text(
        json.dumps(
            {
                "auth_mode": "chatgpt",
                "tokens": {
                    "access_token": "expired-access-token",
                    "refresh_token": "refresh-token",
                    "account_id": "account-123",
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("CALLUMPLOYED_CHATGPT_AUTH_PATH", str(auth_path))
    response_attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal response_attempts
        if request.url == "https://auth.openai.com/oauth/token":
            assert json.loads(request.content) == {
                "client_id": "app_EMoamEEZ73f0CkXaXp7hrann",
                "grant_type": "refresh_token",
                "refresh_token": "refresh-token",
            }
            return httpx.Response(
                200,
                json={
                    "access_token": "fresh-access-token",
                    "refresh_token": "fresh-refresh-token",
                },
            )
        response_attempts += 1
        if response_attempts == 1:
            return httpx.Response(401, json={"error": {"message": "expired"}})
        assert request.headers["authorization"] == "Bearer fresh-access-token"
        return httpx.Response(
            200,
            text=(
                'data: {"type":"response.output_text.delta","delta":"{\\"accepted\\":true}"}\n\n'
                'data: {"type":"response.completed","response":{"id":"response-1"}}\n\n'
            ),
        )

    class Result(BaseModel):
        accepted: bool

    model = CodexStructuredChatModel(
        output_model=Result,
        transport=httpx.MockTransport(handler),
    )
    result = asyncio.run(model.ainvoke("Return an accepted result"))

    assert result.accepted is True
    stored = json.loads(auth_path.read_text(encoding="utf-8"))
    assert stored["tokens"]["access_token"] == "fresh-access-token"
    assert stored["tokens"]["refresh_token"] == "fresh-refresh-token"
    assert stored["last_refresh"].endswith("Z")


def test_codex_subscription_provider_uses_newer_shared_auth_instead_of_stale_refresh(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_path = tmp_path / "auth.json"
    stale_auth = {
        "auth_mode": "chatgpt",
        "tokens": {
            "access_token": "stale-access-token",
            "refresh_token": "stale-refresh-token",
            "account_id": "account-123",
        },
    }
    fresh_auth = {
        "auth_mode": "chatgpt",
        "tokens": {
            "access_token": "external-fresh-access-token",
            "refresh_token": "external-fresh-refresh-token",
            "account_id": "account-123",
        },
    }
    auth_path.write_text(json.dumps(stale_auth), encoding="utf-8")
    monkeypatch.setenv("CALLUMPLOYED_CHATGPT_AUTH_PATH", str(auth_path))
    refresh_attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal refresh_attempts
        if request.url == "https://auth.openai.com/oauth/token":
            refresh_attempts += 1
            return httpx.Response(500)
        if request.headers["authorization"] == "Bearer stale-access-token":
            auth_path.write_text(json.dumps(fresh_auth), encoding="utf-8")
            return httpx.Response(401)
        assert request.headers["authorization"] == "Bearer external-fresh-access-token"
        return httpx.Response(
            200,
            text=(
                'data: {"type":"response.output_text.delta","delta":"{\\"accepted\\":true}"}\n\n'
                'data: {"type":"response.completed","response":{"id":"response-1"}}\n\n'
            ),
        )

    class Result(BaseModel):
        accepted: bool

    model = CodexStructuredChatModel(
        output_model=Result,
        transport=httpx.MockTransport(handler),
    )
    result = asyncio.run(model.ainvoke("Return an accepted result"))

    assert result.accepted is True
    assert refresh_attempts == 0
    assert json.loads(auth_path.read_text(encoding="utf-8")) == fresh_auth


def test_codex_subscription_provider_serializes_concurrent_refreshes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_path = tmp_path / "auth.json"
    auth_path.write_text(
        json.dumps(
            {
                "auth_mode": "chatgpt",
                "tokens": {
                    "access_token": "expired-access-token",
                    "refresh_token": "shared-refresh-token",
                    "account_id": "account-123",
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("CALLUMPLOYED_CHATGPT_AUTH_PATH", str(auth_path))
    stale_attempts = 0
    refresh_attempts = 0
    both_stale_requests_started = asyncio.Event()

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal stale_attempts, refresh_attempts
        if request.url == "https://auth.openai.com/oauth/token":
            refresh_attempts += 1
            return httpx.Response(
                200,
                json={
                    "access_token": "fresh-access-token",
                    "refresh_token": "rotated-refresh-token",
                },
            )
        if request.headers["authorization"] == "Bearer expired-access-token":
            stale_attempts += 1
            if stale_attempts == 2:
                both_stale_requests_started.set()
            await both_stale_requests_started.wait()
            return httpx.Response(401)
        assert request.headers["authorization"] == "Bearer fresh-access-token"
        return httpx.Response(
            200,
            text=(
                'data: {"type":"response.output_text.delta","delta":"{\\"accepted\\":true}"}\n\n'
                'data: {"type":"response.completed","response":{"id":"response-1"}}\n\n'
            ),
        )

    class Result(BaseModel):
        accepted: bool

    transport = httpx.MockTransport(handler)

    async def invoke_twice() -> list[Result]:
        models = [
            CodexStructuredChatModel(output_model=Result, transport=transport),
            CodexStructuredChatModel(output_model=Result, transport=transport),
        ]
        return await asyncio.gather(*(model.ainvoke("Return accepted") for model in models))

    results = asyncio.run(invoke_twice())

    assert results == [Result(accepted=True), Result(accepted=True)]
    assert stale_attempts == 2
    assert refresh_attempts == 1


def test_build_chat_model_rejects_unsupported_provider() -> None:
    with pytest.raises(ValueError, match="unsupported LLM provider"):
        build_chat_model(LlmSettings(provider="bedrock"))
