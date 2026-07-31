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
