export type ResolveCompanyAction = "matched" | "created" | "needs_review";
export type RoleStatus = "open" | "closed" | "unknown";

export interface ResolveCompanyRequest {
  name: string;
  career_page_urls?: string[];
  role_urls?: string[];
  prestige_tier?: string | null;
  tier_source_id?: string | null;
}

export interface ResolveCompanyResponse {
  action: ResolveCompanyAction;
  global_company_id: string | null;
  confidence: number;
  matched_on: string[];
  canonical_domain: string | null;
  normalized_name: string | null;
  default_tier: string | null;
  career_page_urls: string[];
  candidates: Array<Record<string, unknown>>;
}

export interface PublicResolveCompanyResponse {
  global_company_id: string | null;
  default_tier: string | null;
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
  career_page_urls: string[];
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

export interface ScanMetricsRequest {
  schema_version: 1 | 2 | 3;
  client_id: string;
  scan_event_id: string;
  global_company_id?: string | null;
  company_name: string;
  scan_status: "succeeded" | "failed";
  started_at: string;
  finished_at: string;
  duration_ms: number;
  career_pages_total: number;
  pages_scanned: number;
  candidates_scanned: number;
  potential_roles_discovered: number;
  role_verification_attempts: number;
  verified_open_roles: number;
  roles_saved: number;
  failed_role_visits: number;
  page_confidence_counts: Record<string, number>;
  candidate_confidence_counts: Record<string, number>;
  candidate_selection_counts: Record<string, number>;
  candidate_discovery_method_counts: Record<string, number>;
  verification_status_counts: Record<string, number>;
  verification_outcome_counts: Record<string, number>;
  extraction_method_counts: Record<string, number>;
  rejection_reason_counts: Record<string, number>;
  role_status_counts: Record<string, number>;
  autoprep_outcome_counts: Record<string, number>;
  agent_trace_present: boolean;
  error_type?: string | null;
  app_version: string;
}
