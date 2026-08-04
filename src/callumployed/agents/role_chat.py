import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, ValidationError

from callumployed.agents.posting_link_classifier import ChatModelFactory, build_chat_model
from callumployed.config import LlmSettings


class RoleChatModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class RoleChatMessage(RoleChatModel):
    role: Literal["user", "assistant"]
    content: str


class RoleChatResponse(RoleChatModel):
    answer: str


SYSTEM_PROMPT = """
You are a private job-application copilot for one saved role.

Answer questions using the supplied role, resume, cover letter, and employment
history context. Be direct, specific, and grounded in the provided material. If a
question asks for application strategy, compare the role requirements against the
resume and cover letter. If the answer is not supported by the supplied context,
say what is missing instead of guessing.

Do not claim edits have been made. Do not invent experience, job details, company
facts, dates, metrics, or credentials. Keep answers concise unless the user asks
for a draft or detailed comparison.
""".strip()


class RoleChatAgent:
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

    async def answer(
        self,
        *,
        role: dict[str, Any],
        resume_content: str | None = None,
        cover_letter_content: str | None = None,
        employment_history_context: list[dict[str, Any]] | None = None,
        messages: list[RoleChatMessage],
    ) -> RoleChatResponse:
        model = (
            self.chat_model_factory(self.settings)
            if self.chat_model_factory is not None
            else build_chat_model(self.settings)
        )
        result = await model.ainvoke(
            build_role_chat_prompt(
                role=role,
                resume_content=resume_content,
                cover_letter_content=cover_letter_content,
                employment_history_context=employment_history_context,
                messages=messages,
            )
        )
        return RoleChatResponse(answer=_message_content(result))


def build_role_chat_prompt(
    *,
    role: dict[str, Any],
    resume_content: str | None = None,
    cover_letter_content: str | None = None,
    employment_history_context: list[dict[str, Any]] | None = None,
    messages: list[RoleChatMessage],
) -> str:
    payload = {
        "role_context": {
            "id": role.get("id"),
            "company_id": role.get("company_id"),
            "company_name": role.get("company_name"),
            "title": role.get("title"),
            "url": role.get("role_url"),
            "location": role.get("location"),
            "description": role.get("description"),
            "status": role.get("role_status"),
        },
        "resume_context": {
            "format": "latex",
            "content": resume_content or "",
        },
        "cover_letter_context": {
            "format": "latex",
            "content": cover_letter_content or "",
        },
        "employment_history_context": [
            {
                "filename": item.get("filename"),
                "content": item.get("content"),
                "updated_at": item.get("updated_at"),
            }
            for item in employment_history_context or []
        ],
        "chat_history": [message.model_dump(mode="json") for message in messages],
    }
    return f"{SYSTEM_PROMPT}\n\nContext:\n{json.dumps(payload, indent=2, sort_keys=True)}"


async def generate_role_chat(
    *,
    role: dict[str, Any],
    resume_content: str | None = None,
    cover_letter_content: str | None = None,
    employment_history_context: list[dict[str, Any]] | None = None,
    messages: list[RoleChatMessage],
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> RoleChatResponse:
    return await RoleChatAgent(
        settings=settings,
        chat_model_factory=chat_model_factory,
    ).answer(
        role=role,
        resume_content=resume_content,
        cover_letter_content=cover_letter_content,
        employment_history_context=employment_history_context,
        messages=messages,
    )


def parse_role_chat_messages(value: object) -> list[RoleChatMessage]:
    if not isinstance(value, list):
        raise ValueError("Expected chat messages")
    messages: list[RoleChatMessage] = []
    for item in value[-12:]:
        try:
            messages.append(RoleChatMessage.model_validate(item))
        except ValidationError as error:
            raise ValueError("Expected valid chat messages") from error
    if not messages or messages[-1].role != "user" or not messages[-1].content.strip():
        raise ValueError("Expected a user message")
    return [
        message.model_copy(update={"content": message.content.strip()})
        for message in messages
        if message.content.strip()
    ]


def _message_content(result: object) -> str:
    if isinstance(result, str):
        return result.strip()
    content = getattr(result, "content", None)
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = [
            str(part.get("text") if isinstance(part, dict) else part)
            for part in content
            if part
        ]
        return "\n".join(part.strip() for part in parts if part.strip())
    return str(result).strip()
