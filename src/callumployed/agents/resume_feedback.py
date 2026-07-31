import json
import re
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
- "ready_to_apply" when the resume already fits the job description well enough, or
  when every possible edit would be speculative, generic, unsupported, or marginal.
- "tweak" only when at least one concrete resume edit is clearly supported by the
  current resume or by explicitly supplied other-experience notes.

Use the resume context and job context directly. Evaluate:
- visible overlap with the role's required skills, domains, and seniority
- missing important keywords that are honestly supported by the resume
- other experience notes that may support optional additions not currently visible
- whether the strongest matching experience appears early enough
- whether the resume avoids adding unsupported claims
- whether changes are specific enough to improve this application
- prior recommendation history from the knowledge base, if provided

When the verdict is "tweak", return concise feedback items one by one. Each item must
be a concrete resume-edit operation, not generic application advice. Use one of these
operation styles:
- title: "add skills matching the posting: ..." when supported skills/projects are
  present in the resume or explicitly supplied notes but missing the posting's wording
- title: "change wording to align with posting: ..." when an existing bullet should
  be rewritten to use the posting's language
- title: "move emphasis earlier: ..." when relevant experience exists but is buried
- title: "remove or avoid unsupported claim: ..." when a tempting keyword is not
  supported by the resume context

Every add_skills or change_wording item must include either:
- target_text copied exactly from resume_context.content plus replacement_text, or
- latex_addition for a small standalone LaTeX line or bullet whose source is named in
  detail.
Do not return broad keyword advice such as "mention distributed systems" unless the
exact supported resume text to edit or the exact supported LaTeX addition is provided.
Do not invent experience.

For move_emphasis items, first verify the current resume ordering from
resume_context.content. Only suggest moving a role/project earlier when the exact
target role/project currently appears after less-relevant experience. If the
strongest matching role is already at the top of the relevant resume section,
do not suggest moving it earlier; suggest a wording or bullet-content edit
instead. Never use placeholders such as "[current ordering]" or replacement text
that only says to move a role.

Use other_experience_context only as secondary evidence. These notes may or may not
already be on the resume. Never assume they are visible in resume_context.content.
Suggest adding note-derived material only when the note is clearly relevant to the
job and supports an exact, truthful latex_addition. If the note-derived edit would be
nice-to-have, speculative, or less important than the current resume fit, keep the
verdict ready_to_apply and mention the note briefly in the overview at most.

Use the recommendation knowledge base as preference memory:
- accepted feedback means a similar recommendation was useful before
- ignored feedback means a similar recommendation was not useful
- user comments explain why a recommendation was accepted or ignored
- treat ignored feedback with comments as strong negative examples
- when accepted and ignored examples conflict, prefer specific user comments such as
  "not true", "unsupported", "already covered", "redundant", or "too generic"
- do not repeat a recommendation when the knowledge base says the user ignored
  that kind of edit as too generic, unsupported, irrelevant, or already covered
- avoid repeating ignored recommendation patterns unless the current job clearly
  changes the context

Return only JSON matching:
{"verdict":"tweak","overview":"...","feedback_items":[{"label":"add_skills","title":"...",
"detail":"...","target_text":null,"replacement_text":null,"latex_addition":"..."}]}
""".strip()


def build_resume_feedback_prompt(
    *,
    role: dict[str, Any],
    resume_content: str,
    knowledge_base: list[dict[str, Any]] | None = None,
    other_experience_context: list[dict[str, Any]] | None = None,
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
        "other_experience_context": [
            {
                "filename": item.get("filename"),
                "content": item.get("content"),
                "updated_at": item.get("updated_at"),
            }
            for item in other_experience_context or []
        ],
        "recommendation_knowledge_base": [
            {
                "response": item.get("response"),
                "comment": item.get("comment"),
                "role_title": item.get("role_title"),
                "feedback_title": item.get("feedback_title"),
                "feedback_detail": item.get("feedback_detail"),
                "preference_summary": item.get("preference_summary")
                or item.get("knowledge_text"),
                "similarity": item.get("similarity"),
            }
            for item in knowledge_base or []
        ],
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
        knowledge_base: list[dict[str, Any]] | None = None,
        other_experience_context: list[dict[str, Any]] | None = None,
    ) -> ResumeFeedbackResponse:
        model = (
            self.chat_model_factory(self.settings)
            if self.chat_model_factory is not None
            else build_chat_model(self.settings).with_structured_output(ResumeFeedbackResponse)
        )
        result = await model.ainvoke(
            build_resume_feedback_prompt(
                role=role,
                resume_content=resume_content,
                knowledge_base=knowledge_base,
                other_experience_context=other_experience_context,
            )
        )
        response = ResumeFeedbackResponse.model_validate(result)
        if response.verdict == "ready_to_apply":
            return response.model_copy(update={"feedback_items": []})
        feedback_items = [
            item
            for item in response.feedback_items
            if _is_actionable_feedback_item(item, resume_content)
        ]
        if not feedback_items:
            return response.model_copy(update={"verdict": "ready_to_apply", "feedback_items": []})
        return response.model_copy(
            update={
                "feedback_items": [
                    _normalize_feedback_title(item) for item in feedback_items
                ]
            }
        )


async def evaluate_resume_feedback(
    *,
    role: dict[str, Any],
    resume_content: str,
    knowledge_base: list[dict[str, Any]] | None = None,
    other_experience_context: list[dict[str, Any]] | None = None,
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> ResumeFeedbackResponse:
    return await ResumeFeedbackAgent(
        settings=settings,
        chat_model_factory=chat_model_factory,
    ).evaluate(
        role=role,
        resume_content=resume_content,
        knowledge_base=knowledge_base,
        other_experience_context=other_experience_context,
    )


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


def _is_actionable_feedback_item(item: ResumeFeedbackItem, resume_content: str) -> bool:
    target_text = (item.target_text or "").strip()
    replacement_text = (item.replacement_text or "").strip()
    latex_addition = (item.latex_addition or "").strip()
    if item.label in {"add_skills", "change_wording"}:
        if target_text:
            return bool(replacement_text) and _contains_normalized_text(
                resume_content, target_text
            )
        return bool(latex_addition)
    if item.label != "move_emphasis":
        return True
    if not target_text:
        return False
    if "[" in target_text or "]" in target_text:
        return False
    if re.search(r"\bmove\s+this\s+role\b|\bappear\s+before\b", replacement_text, re.I):
        return False
    return _contains_normalized_text(resume_content, target_text)


def _contains_normalized_text(haystack: str, needle: str) -> bool:
    normalized_haystack = " ".join(haystack.casefold().split())
    normalized_needle = " ".join(needle.casefold().split())
    return normalized_needle in normalized_haystack
