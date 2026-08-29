import json
from typing import Any

from pydantic import BaseModel, ConfigDict

from callumployed.agents.posting_link_classifier import ChatModelFactory, build_chat_model
from callumployed.config import LlmSettings


class ResumeTweakModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class ResumeTweakDraft(ResumeTweakModel):
    latex: str
    summary: str


SYSTEM_PROMPT = """
You revise a LaTeX resume for a specific job application.

Use the provided existing resume LaTeX as the source document and return a full,
compilable replacement LaTeX document. Apply regeneration_tweaks directly, but
only when the edit is supported by the existing resume or explicitly supplied
other-experience notes. Keep the resume truthful and concise.

Rules:
- preserve the current LaTeX structure, packages, commands, and formatting unless
  a requested tweak requires a narrow content edit
- actively rewrite bullets and descriptions so the resume is clearer, smoother,
  stronger, and specifically tailored to the job; do not merely copy the source
- preserve every employer, role, project, education entry, date, and link, but do
  not preserve source sentences verbatim when better truthful wording is possible
- select the strongest source-supported accomplishments for each entry; bullets may
  be reordered, split, tightened, or consolidated within the same experience, but
  never awkwardly combine unrelated projects, employers, or accomplishments
- use readable spacing and typography to fill one page effectively; if the page is
  sparse, add useful source-supported specificity rather than filler or repetition
- do not invent employers, projects, metrics, skills, dates, schools, awards, or
  responsibilities
- use job_context to choose wording and emphasis, but do not copy unsupported
  requirements into the resume
- use other_experience_context only when the notes clearly support an addition
- make substantive wording improvements when they strengthen relevance or clarity
- keep the output as LaTeX only in the latex field, not Markdown
- return the full document, not a diff or excerpt

Return only JSON matching:
{"latex":"...","summary":"short note describing what changed"}
""".strip()


class ResumeTweakAgent:
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

    async def generate(
        self,
        *,
        role: dict[str, Any],
        resume_content: str,
        tweaks: str,
        other_experience_context: list[dict[str, Any]] | None = None,
    ) -> ResumeTweakDraft:
        model = (
            self.chat_model_factory(self.settings)
            if self.chat_model_factory is not None
            else build_chat_model(self.settings).with_structured_output(ResumeTweakDraft)
        )
        result = await model.ainvoke(
            build_resume_tweak_prompt(
                role=role,
                resume_content=resume_content,
                tweaks=tweaks,
                other_experience_context=other_experience_context,
            )
        )
        return ResumeTweakDraft.model_validate(result)


def build_resume_tweak_prompt(
    *,
    role: dict[str, Any],
    resume_content: str,
    tweaks: str,
    other_experience_context: list[dict[str, Any]] | None = None,
) -> str:
    payload = {
        "job_context": {
            "id": role.get("id"),
            "company_id": role.get("company_id"),
            "company_name": role.get("company_name"),
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
        "regeneration_tweaks": tweaks,
    }
    return f"{SYSTEM_PROMPT}\n\nContext:\n{json.dumps(payload, indent=2, sort_keys=True)}"


async def generate_resume_tweak(
    *,
    role: dict[str, Any],
    resume_content: str,
    tweaks: str,
    other_experience_context: list[dict[str, Any]] | None = None,
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> ResumeTweakDraft:
    return await ResumeTweakAgent(
        settings=settings,
        chat_model_factory=chat_model_factory,
    ).generate(
        role=role,
        resume_content=resume_content,
        tweaks=tweaks,
        other_experience_context=other_experience_context,
    )
