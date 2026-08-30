import json

from pydantic import BaseModel, ConfigDict

from callumployed.agents.posting_link_classifier import ChatModelFactory, build_chat_model
from callumployed.config import LlmSettings


class ApplicantProfileExtraction(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    institution: str = ""
    degree: str = ""


SYSTEM_PROMPT = """
Extract the applicant's profile from the supplied LaTeX resume.

Rules:
- use only information explicitly present in the resume
- return an empty string when a field is absent or ambiguous
- first_name and last_name are the applicant's name, not a reference or employer
- institution is the applicant's current or most recent school or university
- degree is the degree and program as written in the education section
- preserve meaningful phone formatting
- do not include LaTeX commands or escaping in extracted values

Return only JSON matching:
{"first_name":"","last_name":"","email":"","phone":"","institution":"","degree":""}
""".strip()


class ApplicantProfileExtractor:
    def __init__(
        self,
        *,
        settings: LlmSettings | None = None,
        chat_model_factory: ChatModelFactory | None = None,
    ) -> None:
        self.settings = settings or LlmSettings()
        self.chat_model_factory = chat_model_factory

    async def extract(self, *, resume_content: str) -> ApplicantProfileExtraction:
        model = (
            self.chat_model_factory(self.settings)
            if self.chat_model_factory is not None
            else build_chat_model(self.settings).with_structured_output(ApplicantProfileExtraction)
        )
        result = await model.ainvoke(build_applicant_profile_prompt(resume_content))
        return ApplicantProfileExtraction.model_validate(result)


def build_applicant_profile_prompt(resume_content: str) -> str:
    return "\n\n".join(
        (
            SYSTEM_PROMPT,
            json.dumps(
                {"resume_context": {"format": "latex", "content": resume_content}},
                ensure_ascii=True,
            ),
        )
    )


async def extract_applicant_profile(
    *,
    resume_content: str,
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> ApplicantProfileExtraction:
    return await ApplicantProfileExtractor(
        settings=settings,
        chat_model_factory=chat_model_factory,
    ).extract(resume_content=resume_content)
