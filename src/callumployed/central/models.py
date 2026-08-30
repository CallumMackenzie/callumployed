from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CentralModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ResolveCompanyRequest(CentralModel):
    name: str
    career_page_urls: list[str] = Field(default_factory=list)
    role_urls: list[str] = Field(default_factory=list)
    prestige_tier: str | None = None
    tier_source_id: str | None = None


class ResolveCompanyResponse(CentralModel):
    action: Literal["matched", "created", "needs_review"] = "matched"
    global_company_id: str | None = None
    confidence: int = 0
    matched_on: list[str] = Field(default_factory=list)
    canonical_domain: str | None = None
    normalized_name: str | None = None
    default_tier: str | None = None
    career_page_urls: list[str] = Field(default_factory=list)
    candidates: list[dict[str, object]] = Field(default_factory=list)


class CentralCompany(CentralModel):
    global_company_id: str
    display_name: str
    normalized_names: list[str] = Field(default_factory=list)
    compact_names: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    ats_slugs: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    default_tier: str | None = None
    career_page_urls: list[str] = Field(default_factory=list)


class CentralCompaniesResponse(CentralModel):
    companies: list[CentralCompany] = Field(default_factory=list)


class CentralRole(CentralModel):
    global_role_id: str
    global_company_id: str
    company_name: str
    title: str
    role_url: str
    location: str | None = None
    description: str | None = None
    posting_id: str | None = None
    tier_classification: str | None = None
    status: Literal["open", "closed", "unknown"] = "unknown"


class CentralRolesResponse(CentralModel):
    roles: list[CentralRole] = Field(default_factory=list)


class BulkUpsertRole(CentralModel):
    global_company_id: str
    title: str
    role_url: str
    location: str | None = None
    description: str | None = None
    posting_id: str | None = None
    tier_classification: str | None = None


class BulkUpsertRolesRequest(CentralModel):
    roles: list[BulkUpsertRole]


class BulkUpsertRolesResponse(CentralModel):
    upserted: int


class ScanMetricsRequest(CentralModel):
    schema_version: Literal[3] = 3
    client_id: str = Field(min_length=1, max_length=128)
    scan_event_id: str = Field(min_length=1, max_length=128)
    global_company_id: str | None = Field(default=None, max_length=128)
    company_name: str = Field(min_length=1, max_length=256)
    scan_status: Literal["succeeded", "failed"]
    started_at: datetime
    finished_at: datetime
    duration_ms: int = Field(ge=0, le=86_400_000)
    career_pages_total: int = Field(ge=0, le=10_000)
    pages_scanned: int = Field(ge=0, le=10_000)
    candidates_scanned: int = Field(ge=0, le=1_000_000)
    potential_roles_discovered: int = Field(ge=0, le=1_000_000)
    role_verification_attempts: int = Field(ge=0, le=1_000_000)
    verified_open_roles: int = Field(ge=0, le=1_000_000)
    roles_saved: int = Field(ge=0, le=1_000_000)
    failed_role_visits: int = Field(ge=0, le=1_000_000)
    page_confidence_counts: dict[str, int] = Field(default_factory=dict)
    candidate_confidence_counts: dict[str, int] = Field(default_factory=dict)
    candidate_selection_counts: dict[str, int] = Field(default_factory=dict)
    candidate_discovery_method_counts: dict[str, int] = Field(default_factory=dict)
    verification_status_counts: dict[str, int] = Field(default_factory=dict)
    verification_outcome_counts: dict[str, int] = Field(default_factory=dict)
    extraction_method_counts: dict[str, int] = Field(default_factory=dict)
    rejection_reason_counts: dict[str, int] = Field(default_factory=dict)
    role_status_counts: dict[str, int] = Field(default_factory=dict)
    autoprep_outcome_counts: dict[str, int] = Field(default_factory=dict)
    agent_trace_present: bool = False
    error_type: str | None = Field(default=None, max_length=128)
    app_version: str = Field(min_length=1, max_length=64)


class ScanMetricsResponse(CentralModel):
    accepted: bool
    scan_metric_id: str
