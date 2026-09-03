import json

from pydantic import BaseModel, ConfigDict, Field

from callumployed.agents.posting_link_classifier import ChatModelFactory, build_chat_model
from callumployed.config import LlmSettings
from callumployed.webscraping.models import RenderedPageState, RolePageAssessment

LLM_FALLBACK_REJECTION_REASON = "deterministic evidence is weak; LLM fallback recommended"
MAX_ROLE_PAGE_CONTEXT_CHARACTERS = 20_000


class RolePageAssessmentDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    is_role: bool
    is_closed: bool = False
    confidence: float = Field(ge=0.0, le=1.0)
    title: str | None = None
    location: str | None = None
    description: str | None = None
    posting_id: str | None = None
    rejection_reason: str | None = None
    reasons: list[str] = Field(default_factory=list)


SYSTEM_PROMPT = """
You assess whether a rendered web page is a specific job posting.

Use only the supplied page content and deterministic assessment. Decide whether the page
is one specific role rather than a careers index, search page, navigation page, marketing
page, or transient error. Report whether the role is closed and extract only details that
are explicitly supported by the page. Do not invent a title, location, description, or
posting ID. Return only JSON matching the requested schema.
""".strip()


def should_use_role_page_llm_fallback(assessment: RolePageAssessment) -> bool:
    return assessment.rejection_reason == LLM_FALLBACK_REJECTION_REASON


def build_role_page_assessment_prompt(
    page: RenderedPageState,
    deterministic_assessment: RolePageAssessment,
    *,
    title_hints: tuple[str | None, ...] = (),
) -> str:
    source_text = (page.visible_text or page.html)[:MAX_ROLE_PAGE_CONTEXT_CHARACTERS]
    payload = {
        "page": {
            "url": page.url,
            "final_url": page.final_url,
            "browser_title": page.title,
            "visible_text": source_text,
        },
        "title_hints": [hint for hint in title_hints if hint],
        "deterministic_assessment": deterministic_assessment.model_dump(mode="json"),
    }
    return f"{SYSTEM_PROMPT}\n\nRole-page context:\n{json.dumps(payload, indent=2, sort_keys=True)}"


async def assess_role_page_with_llm(
    page: RenderedPageState,
    deterministic_assessment: RolePageAssessment,
    *,
    title_hints: tuple[str | None, ...] = (),
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> RolePageAssessment:
    llm_settings = settings or LlmSettings()
    model = (
        chat_model_factory(llm_settings)
        if chat_model_factory is not None
        else build_chat_model(llm_settings).with_structured_output(RolePageAssessmentDecision)
    )
    result = await model.ainvoke(
        build_role_page_assessment_prompt(
            page,
            deterministic_assessment,
            title_hints=title_hints,
        )
    )
    decision = RolePageAssessmentDecision.model_validate(result)
    return RolePageAssessment(
        is_role=decision.is_role,
        is_closed=decision.is_closed,
        confidence=decision.confidence,
        title=decision.title,
        location=decision.location,
        description=decision.description,
        posting_id=decision.posting_id,
        extraction_method="llm",
        rejection_reason=decision.rejection_reason,
        reasons=["LLM fallback assessment", *decision.reasons],
    )
