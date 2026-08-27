import type {Firestore} from "firebase-admin/firestore";

import type {ScanMetricsRequest} from "./contracts";
import {stableId} from "./normalization";

const COUNT_FIELDS = [
  "duration_ms",
  "career_pages_total",
  "pages_scanned",
  "candidates_scanned",
  "potential_roles_discovered",
  "role_verification_attempts",
  "verified_open_roles",
  "roles_saved",
  "failed_role_visits",
] as const;

export async function submitScanMetrics(
  db: Firestore,
  input: Partial<ScanMetricsRequest>,
): Promise<string> {
  const metrics = validateScanMetrics(input);
  const scanMetricId = stableId("scan_metric", `${metrics.client_id}:${metrics.scan_event_id}`);
  await db.collection("scan_metrics").doc(scanMetricId).set(
    {
      ...metrics,
      received_at: new Date().toISOString(),
    },
    {merge: true},
  );
  return scanMetricId;
}

function validateScanMetrics(input: Partial<ScanMetricsRequest>): ScanMetricsRequest {
  const clientId = requiredString(input.client_id, "client_id", 128);
  const scanEventId = requiredString(input.scan_event_id, "scan_event_id", 128);
  const companyName = requiredString(input.company_name, "company_name", 256);
  const appVersion = requiredString(input.app_version, "app_version", 64);
  if (input.schema_version !== 1) throw new Error("schema_version must be 1");
  if (input.scan_status !== "succeeded" && input.scan_status !== "failed") {
    throw new Error("scan_status must be succeeded or failed");
  }
  const startedAt = requiredDate(input.started_at, "started_at");
  const finishedAt = requiredDate(input.finished_at, "finished_at");
  const counts = Object.fromEntries(
    COUNT_FIELDS.map((field) => [
      field,
      nonNegativeInteger(input[field], field, field === "duration_ms" ? 86_400_000 : 1_000_000),
    ]),
  ) as Record<(typeof COUNT_FIELDS)[number], number>;

  return {
    schema_version: 1,
    client_id: clientId,
    scan_event_id: scanEventId,
    global_company_id: optionalString(input.global_company_id, 128),
    company_name: companyName,
    scan_status: input.scan_status,
    started_at: startedAt,
    finished_at: finishedAt,
    duration_ms: counts.duration_ms,
    career_pages_total: counts.career_pages_total,
    pages_scanned: counts.pages_scanned,
    candidates_scanned: counts.candidates_scanned,
    potential_roles_discovered: counts.potential_roles_discovered,
    role_verification_attempts: counts.role_verification_attempts,
    verified_open_roles: counts.verified_open_roles,
    roles_saved: counts.roles_saved,
    failed_role_visits: counts.failed_role_visits,
    error_type: optionalString(input.error_type, 128),
    app_version: appVersion,
  };
}

function requiredString(value: unknown, field: string, maxLength: number): string {
  if (typeof value !== "string" || !value.trim() || value.length > maxLength) {
    throw new Error(`${field} must be a non-empty string up to ${maxLength} characters`);
  }
  return value.trim();
}

function optionalString(value: unknown, maxLength: number): string | null {
  if (value === null || value === undefined || value === "") return null;
  if (typeof value !== "string" || value.length > maxLength) {
    throw new Error(`optional string must be up to ${maxLength} characters`);
  }
  return value.trim() || null;
}

function requiredDate(value: unknown, field: string): string {
  if (typeof value !== "string" || Number.isNaN(Date.parse(value))) {
    throw new Error(`${field} must be an ISO timestamp`);
  }
  return value;
}

function nonNegativeInteger(value: unknown, field: string, maximum: number): number {
  if (typeof value !== "number" || !Number.isInteger(value) || value < 0 || value > maximum) {
    throw new Error(`${field} must be a non-negative integer`);
  }
  return value;
}
