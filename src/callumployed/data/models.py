from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class RoleStatus(StrEnum):
    DISCOVERED = "discovered"
    INTERESTED = "interested"
    DISINTERESTED = "disinterested"
    PREPARED = "prepared"
    APPLIED = "applied"
    OA = "OA"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    OFFER = "offer"
    CLOSED = "closed"
    ARCHIVED = "archived"


class ScanStatus(StrEnum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class EventSource(StrEnum):
    MANUAL = "manual"
    SCAN = "scan"


class RoleDiscoveryStatus(StrEnum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class AppModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Company(AppModel):
    id: int | None = None
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    notes: str | None = None
    prestige_tier: str | None = None


class CompanyCareerPage(AppModel):
    id: int | None = None
    company_id: int
    url: str
    label: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Role(AppModel):
    id: int | None = None
    company_id: int
    title: str
    role_url: str
    location: str | None = None
    role_status: RoleStatus = RoleStatus.DISCOVERED
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    notes: str | None = None
    description: str | None = None
    posting_id: str | None = None


class RoleListItem(AppModel):
    id: int
    company_id: int
    company_name: str
    title: str
    role_url: str
    location: str | None = None
    role_status: RoleStatus
    last_seen_at: datetime | None = None
    updated_at: datetime | None = None


class ScanRun(AppModel):
    id: int | None = None
    company_id: int
    started_at: datetime | None = None
    finished_at: datetime | None = None
    scan_status: ScanStatus = ScanStatus.RUNNING
    error: str | None = None
    created_at: datetime | None = None
    agent_trace: str | None = None


class ScanRunListItem(ScanRun):
    company_name: str


class ScanPage(AppModel):
    id: int | None = None
    scan_run_id: int
    company_career_page_id: int | None = None
    source_url: str
    final_url: str
    title: str | None = None
    candidates_scanned: int = 0
    confidence: str = "low"
    created_at: datetime | None = None


class ScanCandidate(AppModel):
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
    created_at: datetime | None = None


class RoleDiscoveryAttempt(AppModel):
    id: int | None = None
    scan_run_id: int
    scan_candidate_id: int
    company_id: int
    role_id: int | None = None
    url: str
    final_url: str | None = None
    title: str | None = None
    visible_text_excerpt: str | None = None
    assessment_is_role: bool | None = None
    assessment_is_closed: bool | None = None
    assessment_confidence: float | None = None
    assessment_location: str | None = None
    assessment_description: str | None = None
    assessment_posting_id: str | None = None
    assessment_extraction_method: str | None = None
    assessment_rejection_reason: str | None = None
    assessment_reasons: list[str] = Field(default_factory=list)
    status: RoleDiscoveryStatus = RoleDiscoveryStatus.SUCCEEDED
    error: str | None = None
    created_at: datetime | None = None


class Event(AppModel):
    id: int | None = None
    company_id: int
    role_id: int | None = None
    event_type: str
    old_status: RoleStatus | None = None
    new_status: RoleStatus | None = None
    source: EventSource
    summary: str = Field(min_length=1)
    created_at: datetime | None = None
