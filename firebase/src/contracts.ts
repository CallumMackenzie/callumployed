export type ResolveCompanyAction = "matched" | "created" | "needs_review";
export type RoleStatus = "open" | "closed" | "unknown";

export interface ResolveCompanyRequest {
  name: string;
  career_page_urls?: string[];
  role_urls?: string[];
}

export interface ResolveCompanyResponse {
  action: ResolveCompanyAction;
  global_company_id: string | null;
  confidence: number;
  matched_on: string[];
  canonical_domain: string | null;
  normalized_name: string | null;
  candidates: Array<Record<string, unknown>>;
}

export interface PublicResolveCompanyResponse {
  global_company_id: string | null;
}

export interface CentralCompany {
  global_company_id: string;
  display_name: string;
  normalized_names: string[];
  compact_names: string[];
  domains: string[];
  ats_slugs: string[];
  aliases: string[];
  default_tier: string | null;
}

export interface CentralRole {
  global_role_id: string;
  global_company_id: string;
  company_name: string;
  title: string;
  role_url: string;
  location: string | null;
  description: string | null;
  posting_id: string | null;
  tier_classification: string | null;
  status: RoleStatus;
}

export interface BulkUpsertRole {
  global_company_id: string;
  title: string;
  role_url: string;
  location?: string | null;
  description?: string | null;
  posting_id?: string | null;
  tier_classification?: string | null;
}
