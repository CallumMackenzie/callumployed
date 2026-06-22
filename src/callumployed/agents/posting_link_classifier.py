import importlib
import inspect
import json
from collections.abc import Callable
from typing import Any, Protocol, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

from callumployed.data.models import Company, CompanyCareerPage, ScanCandidate, ScanPage


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


class AgentCallable(Protocol):
    def __call__(self, prompt: str) -> object: ...


AgentFactory = Callable[[], AgentCallable]


class StrandsAgentFactory(Protocol):
    def __call__(self, *, system_prompt: str) -> AgentCallable: ...


class StrandsModule(Protocol):
    Agent: StrandsAgentFactory

SYSTEM_PROMPT = """
You classify scraped links from one company's careers pages.

For each candidate, decide whether the URL is a specific job posting, not a generic
careers page, navigation link, closed role, legal page, search page, or marketing page.
Use the database context exactly as provided. The batch always belongs to one company.
Return only JSON matching this schema:
{"decisions":[{"candidate_id":1,"url":"https://...","is_job_posting":true,
"confidence":0.0,"title":null,"location":null,"reasons":["short reason"]}]}
""".strip()


def build_posting_link_classification_prompt(batch: PostingLinkClassificationBatch) -> str:
    payload = json.dumps(batch.to_agent_payload(), indent=2, sort_keys=True)
    return f"{SYSTEM_PROMPT}\n\nDatabase context:\n{payload}"


async def classify_posting_links(
    batch: PostingLinkClassificationBatch,
    *,
    agent_factory: AgentFactory | None = None,
) -> PostingLinkClassificationResponse:
    agent = agent_factory() if agent_factory is not None else _default_strands_agent()
    result = agent(build_posting_link_classification_prompt(batch))
    if inspect.isawaitable(result):
        result = await result
    return PostingLinkClassificationResponse.model_validate_json(_agent_result_text(result))


def _default_strands_agent() -> AgentCallable:
    try:
        strands = cast(StrandsModule, importlib.import_module("strands"))
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            'Strands is not installed. Install callumployed with the "agents" extra.'
        ) from exc
    return strands.Agent(system_prompt=SYSTEM_PROMPT)


def _agent_result_text(result: object) -> str:
    if isinstance(result, str):
        return result
    text = getattr(result, "text", None)
    if isinstance(text, str):
        return text
    message = getattr(result, "message", None)
    if isinstance(message, str):
        return message
    return str(result)
