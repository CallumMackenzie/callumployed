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
