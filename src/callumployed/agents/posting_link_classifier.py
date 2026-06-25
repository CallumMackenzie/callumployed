import json
from collections.abc import Callable, Coroutine
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field, model_validator

from callumployed.config import LlmSettings
from callumployed.data.models import Company, CompanyCareerPage, ScanCandidate, ScanPage
from callumployed.webscraping.models import (
    DiscoveredJobLink,
    RenderedPageState,
    ScoredLinkCandidate,
)


class AgentModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class PostingLinkCompanyContext(AgentModel):
    id: int | None = None
    name: str
    notes: str | None = None
    prestige_tier: str | None = None


class PostingLinkCareerPageContext(AgentModel):
    id: int | None = None
    company_id: int
    url: str
    label: str | None = None


class PostingLinkScanPageContext(AgentModel):
    id: int | None = None
    scan_run_id: int
    company_career_page_id: int | None = None
    source_url: str
    final_url: str
    title: str | None = None
    candidates_scanned: int = 0
    confidence: str = "low"


class PostingLinkCandidateContext(AgentModel):
    id: int | None = None
    scan_page_id: int
    url: str
    source_url: str
    text: str | None = None
    tag: str = "a"
    css_id: str | None = None
    css_classes: tuple[str, ...] = ()
    aria_label: str | None = None
    title: str | None = None
    surrounding_text: str | None = None
    confidence: float
    reasons: list[str] = Field(default_factory=list)
    selected: bool = False
    discovery_method: str | None = None


class PostingLinkClassificationItem(AgentModel):
    career_page: PostingLinkCareerPageContext
    scan_page: PostingLinkScanPageContext
    candidate: PostingLinkCandidateContext

    @classmethod
    def from_database(
        cls,
        *,
        career_page: CompanyCareerPage,
        scan_page: ScanPage,
        candidate: ScanCandidate,
    ) -> "PostingLinkClassificationItem":
        return cls(
            career_page=PostingLinkCareerPageContext(
                id=career_page.id,
                company_id=career_page.company_id,
                url=career_page.url,
                label=career_page.label,
            ),
            scan_page=PostingLinkScanPageContext(
                id=scan_page.id,
                scan_run_id=scan_page.scan_run_id,
                company_career_page_id=scan_page.company_career_page_id,
                source_url=scan_page.source_url,
                final_url=scan_page.final_url,
                title=scan_page.title,
                candidates_scanned=scan_page.candidates_scanned,
                confidence=scan_page.confidence,
            ),
            candidate=PostingLinkCandidateContext(
                id=candidate.id,
                scan_page_id=candidate.scan_page_id,
                url=candidate.url,
                source_url=candidate.source_url,
                text=candidate.text,
                tag=candidate.tag,
                css_id=candidate.css_id,
                css_classes=candidate.css_classes,
                aria_label=candidate.aria_label,
                title=candidate.title,
                surrounding_text=candidate.surrounding_text,
                confidence=candidate.confidence,
                reasons=candidate.reasons,
                selected=candidate.selected,
                discovery_method=candidate.discovery_method,
            ),
        )


class PostingLinkClassificationBatch(AgentModel):
    company: PostingLinkCompanyContext
    items: list[PostingLinkClassificationItem] = Field(min_length=1)

    @classmethod
    def from_database(
        cls,
        *,
        company: Company,
        items: list[PostingLinkClassificationItem],
    ) -> "PostingLinkClassificationBatch":
        return cls(
            company=PostingLinkCompanyContext(
                id=company.id,
                name=company.name,
                notes=company.notes,
                prestige_tier=company.prestige_tier,
            ),
            items=items,
        )

    @model_validator(mode="after")
    def validate_single_company_batch(self) -> "PostingLinkClassificationBatch":
        if self.company.id is None:
            return self
        mismatched = [
            item.career_page.company_id
            for item in self.items
            if item.career_page.company_id != self.company.id
        ]
        if mismatched:
            raise ValueError("posting link classification batches must stay within one company")
        return self

    def to_agent_payload(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)


class PostingLinkClassificationDecision(AgentModel):
    candidate_id: int | None = None
    url: str
    is_job_posting: bool
    confidence: float = Field(ge=0.0, le=1.0)
    title: str | None = None
    location: str | None = None
    reasons: list[str] = Field(default_factory=list)


class PostingLinkClassificationResponse(AgentModel):
    decisions: list[PostingLinkClassificationDecision]


class StructuredChatModel(Protocol):
    async def ainvoke(self, input: object) -> object: ...


ChatModelFactory = Callable[[LlmSettings], StructuredChatModel]


SYSTEM_PROMPT = """
You classify scraped links from one company's careers pages.

For each candidate, decide whether the URL is a specific job posting, not a generic
careers page, navigation link, closed role, legal page, search page, or marketing page.
Use the database context exactly as provided. The batch always belongs to one company.
Return only JSON matching this schema:
{"decisions":[{"candidate_id":1,"url":"https://...","is_job_posting":true,
"confidence":0.0,"title":null,"location":null,"reasons":["short reason"]}]}
""".strip()


class PostingLinkClassifierAgent:
    """Self-contained LangChain model wrapper for posting/link classification."""

    settings: LlmSettings
    system_prompt: str
    chat_model_factory: ChatModelFactory | None

    def __init__(
        self,
        *,
        settings: LlmSettings | None = None,
        system_prompt: str = SYSTEM_PROMPT,
        chat_model_factory: ChatModelFactory | None = None,
    ) -> None:
        self.settings = settings or LlmSettings()
        self.system_prompt = system_prompt
        self.chat_model_factory = chat_model_factory

    def build_prompt(self, batch: PostingLinkClassificationBatch) -> str:
        payload = json.dumps(batch.to_agent_payload(), indent=2, sort_keys=True)
        return f"{self.system_prompt}\n\nDatabase context:\n{payload}"

    async def classify(
        self,
        batch: PostingLinkClassificationBatch,
    ) -> PostingLinkClassificationResponse:
        model = (
            self.chat_model_factory(self.settings)
            if self.chat_model_factory is not None
            else build_chat_model(self.settings).with_structured_output(
                PostingLinkClassificationResponse
            )
        )
        result = await model.ainvoke(self.build_prompt(batch))
        return PostingLinkClassificationResponse.model_validate(result)


def build_posting_link_classification_prompt(batch: PostingLinkClassificationBatch) -> str:
    return PostingLinkClassifierAgent().build_prompt(batch)


async def classify_posting_links(
    batch: PostingLinkClassificationBatch,
    *,
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> PostingLinkClassificationResponse:
    return await PostingLinkClassifierAgent(
        settings=settings,
        chat_model_factory=chat_model_factory,
    ).classify(batch)


def build_posting_link_agent_classifier(
    *,
    company: Company,
    career_page: CompanyCareerPage,
    scan_run_id: int,
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> Callable[
    [list[ScoredLinkCandidate], RenderedPageState],
    Coroutine[Any, Any, list[DiscoveredJobLink]],
]:
    async def classify_scored_links(
        candidates: list[ScoredLinkCandidate],
        page: RenderedPageState,
    ) -> list[DiscoveredJobLink]:
        if not candidates:
            return []

        batch = PostingLinkClassificationBatch.from_database(
            company=company,
            items=[
                PostingLinkClassificationItem(
                    career_page=PostingLinkCareerPageContext(
                        id=career_page.id,
                        company_id=career_page.company_id,
                        url=career_page.url,
                        label=career_page.label,
                    ),
                    scan_page=PostingLinkScanPageContext(
                        scan_run_id=scan_run_id,
                        company_career_page_id=career_page.id,
                        source_url=page.url,
                        final_url=page.final_url,
                        title=page.title,
                        candidates_scanned=len(candidates),
                    ),
                    candidate=PostingLinkCandidateContext(
                        scan_page_id=0,
                        url=candidate.url,
                        source_url=candidate.source_url,
                        text=candidate.text,
                        tag=candidate.tag,
                        css_id=candidate.css_id,
                        css_classes=candidate.css_classes,
                        aria_label=candidate.aria_label,
                        title=candidate.title,
                        surrounding_text=candidate.surrounding_text,
                        confidence=candidate.confidence,
                        reasons=candidate.reasons,
                    ),
                )
                for candidate in candidates
            ],
        )
        response = await classify_posting_links(
            batch,
            settings=settings,
            chat_model_factory=chat_model_factory,
        )
        candidates_by_url = {candidate.url: candidate for candidate in candidates}
        links: list[DiscoveredJobLink] = []
        for decision in response.decisions:
            if not decision.is_job_posting:
                continue
            candidate = candidates_by_url.get(decision.url)
            if candidate is None:
                continue
            links.append(
                DiscoveredJobLink(
                    url=candidate.url,
                    source_url=candidate.source_url,
                    text=decision.title or candidate.text,
                    confidence=decision.confidence,
                    discovery_method="agent",
                    reasons=decision.reasons,
                )
            )
        return links

    return classify_scored_links


def build_chat_model(settings: LlmSettings) -> Any:
    provider = settings.provider.lower()
    if provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                'OpenAI support is not installed. Install callumployed with the "agents" extra.'
            ) from exc
        if settings.openai_api_key is None:
            return ChatOpenAI(model=settings.model)
        return ChatOpenAI(model=settings.model, api_key=settings.openai_api_key)
    raise ValueError(f"unsupported LLM provider: {settings.provider}")
