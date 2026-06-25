from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WebscrapingModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class ExtractionConfidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RenderedPageState(WebscrapingModel):
    url: str
    final_url: str
    title: str | None = None
    html: str
    visible_text: str | None = None


class LinkCandidate(WebscrapingModel):
    url: str
    source_url: str
    text: str | None = None
    tag: Literal["a", "button"] = "a"
    css_id: str | None = None
    css_classes: tuple[str, ...] = ()
    aria_label: str | None = None
    title: str | None = None
    surrounding_text: str | None = None


class ScoredLinkCandidate(LinkCandidate):
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)


class DiscoveredJobLink(WebscrapingModel):
    url: str
    source_url: str
    text: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    discovery_method: Literal["heuristic", "agent", "heuristic+agent"]
    reasons: list[str] = Field(default_factory=list)


class RolePageAssessment(WebscrapingModel):
    is_role: bool
    is_closed: bool = False
    confidence: float = Field(ge=0.0, le=1.0)
    title: str | None = None
    location: str | None = None
    description: str | None = None
    posting_id: str | None = None
    extraction_method: Literal[
        "jobposting_structured_data",
        "ats_heuristic",
        "html_heuristic",
        "llm",
    ]
    rejection_reason: str | None = None
    reasons: list[str] = Field(default_factory=list)


class CareersPageScanResult(WebscrapingModel):
    source_url: str
    final_url: str
    title: str | None = None
    candidates: list[ScoredLinkCandidate] = Field(default_factory=list)
    links: list[DiscoveredJobLink] = Field(default_factory=list)
    candidates_scanned: int = 0
    confidence: ExtractionConfidence = ExtractionConfidence.LOW
    errors: list[str] = Field(default_factory=list)
