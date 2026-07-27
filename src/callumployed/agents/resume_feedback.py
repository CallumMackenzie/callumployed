import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from callumployed.agents.posting_link_classifier import ChatModelFactory, build_chat_model
from callumployed.config import LlmSettings


class ResumeFeedbackModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class ResumeFeedbackItem(ResumeFeedbackModel):
    label: Literal[
        "add_skills",
        "change_wording",
        "move_emphasis",
        "remove_or_avoid",
        "setup",
        "refresh_context",
    ]
    title: str
    detail: str
    target_text: str | None = None
    replacement_text: str | None = None
    latex_addition: str | None = None


class ResumeFeedbackResponse(ResumeFeedbackModel):
    verdict: Literal["tweak", "ready_to_apply"]
    overview: str
    feedback_items: list[ResumeFeedbackItem] = Field(default_factory=list)


TITLE_PREFIX_BY_LABEL = {
    "add_skills": "add skills matching the posting",
    "change_wording": "change wording to align with posting",
    "move_emphasis": "move emphasis earlier",
    "remove_or_avoid": "remove or avoid unsupported claim",
    "setup": "setup",
    "refresh_context": "refresh job context",
}


SYSTEM_PROMPT = """
You are evaluating whether a LaTeX resume is ready for a specific job application.

Reply with exactly one verdict:
- "ready_to_apply" when the resume already fits the job description well enough.
- "tweak" when the resume should be tailored before applying.

Use the resume context and job context directly. Evaluate:
- visible overlap with the role's required skills, domains, and seniority
- missing important keywords that are honestly supported by the resume
- whether the strongest matching experience appears early enough
- whether the resume avoids adding unsupported claims
- whether changes are specific enough to improve this application

When the verdict is "tweak", return concise feedback items one by one. Each item must
be a concrete resume-edit operation, not generic application advice. Use one of these
operation styles:
- title: "add skills matching the posting: ..." when supported skills/projects are
  present or implied in the resume but missing the posting's wording
- title: "change wording to align with posting: ..." when an existing bullet should
  be rewritten to use the posting's language
- title: "move emphasis earlier: ..." when relevant experience exists but is buried
- title: "remove or avoid unsupported claim: ..." when a tempting keyword is not
  supported by the resume context

Prefer target_text + replacement_text when an exact resume phrase should be replaced.
Use latex_addition only when a small standalone LaTeX line or bullet should be
inserted. Do not invent experience.

Return only JSON matching:
{"verdict":"tweak","overview":"...","feedback_items":[{"label":"add_skills","title":"...",
"detail":"...","target_text":null,"replacement_text":null,"latex_addition":"..."}]}
""".strip()


def build_resume_feedback_prompt(
    *,
    role: dict[str, Any],
    resume_content: str,
) -> str:
    payload = {
        "job_context": {
            "id": role.get("id"),
            "company_id": role.get("company_id"),
            "title": role.get("title"),
            "url": role.get("role_url"),
            "location": role.get("location"),
            "description": role.get("description"),
        },
        "resume_context": {
            "format": "latex",
            "content": resume_content,
        },
    }
    return f"{SYSTEM_PROMPT}\n\nContext:\n{json.dumps(payload, indent=2, sort_keys=True)}"


class ResumeFeedbackAgent:
    settings: LlmSettings
    chat_model_factory: ChatModelFactory | None

    def __init__(
        self,
        *,
        settings: LlmSettings | None = None,
        chat_model_factory: ChatModelFactory | None = None,
    ) -> None:
        self.settings = settings or LlmSettings()
        self.chat_model_factory = chat_model_factory

    async def evaluate(
        self,
        *,
        role: dict[str, Any],
        resume_content: str,
    ) -> ResumeFeedbackResponse:
        model = (
            self.chat_model_factory(self.settings)
            if self.chat_model_factory is not None
            else build_chat_model(self.settings).with_structured_output(ResumeFeedbackResponse)
        )
        result = await model.ainvoke(
            build_resume_feedback_prompt(role=role, resume_content=resume_content)
        )
        response = ResumeFeedbackResponse.model_validate(result)
        if response.verdict == "ready_to_apply":
            return response.model_copy(update={"feedback_items": []})
        if not response.feedback_items:
            return response.model_copy(update={"verdict": "ready_to_apply"})
        return response.model_copy(
            update={
                "feedback_items": [
                    _normalize_feedback_title(item) for item in response.feedback_items
                ]
            }
        )


async def evaluate_resume_feedback(
    *,
    role: dict[str, Any],
    resume_content: str,
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> ResumeFeedbackResponse:
    return await ResumeFeedbackAgent(
        settings=settings,
        chat_model_factory=chat_model_factory,
    ).evaluate(role=role, resume_content=resume_content)


def _normalize_feedback_title(item: ResumeFeedbackItem) -> ResumeFeedbackItem:
    prefix = TITLE_PREFIX_BY_LABEL[item.label]
    normalized_title = item.title.strip()
    if normalized_title.lower().startswith(prefix):
        suffix = normalized_title[len(prefix) :].strip(" :")
        title = f"{prefix}: {suffix}" if suffix else prefix
        return item.model_copy(update={"title": title})
    if ":" in normalized_title:
        normalized_title = normalized_title.split(":", 1)[1].strip()
    return item.model_copy(update={"title": f"{prefix}: {normalized_title}"})
