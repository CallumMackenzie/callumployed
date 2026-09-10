import type {Firestore} from "firebase-admin/firestore";

const MAX_RECORDS = 5000;
const COUNT_FIELDS = [
  "career_pages_total",
  "pages_scanned",
  "candidates_scanned",
  "potential_roles_discovered",
  "role_verification_attempts",
  "verified_open_roles",
  "roles_saved",
  "failed_role_visits",
] as const;

type MetricRecord = Record<string, unknown>;

export async function buildDashboardMetrics(db: Firestore, requestedDays: unknown): Promise<object> {
  const days = parseDays(requestedDays);
  const cutoff = days === null ? null : new Date(Date.now() - days * 86_400_000).toISOString();
  let query = db.collection("scan_metrics").orderBy("received_at", "desc");
  if (cutoff) query = query.where("received_at", ">=", cutoff);
  const snapshot = await query.limit(MAX_RECORDS).get();
  const records = snapshot.docs.map((document) => document.data() as MetricRecord).reverse();
  const latestClientRecords = latestByClient(records);
  const succeeded = records.filter((record) => record.scan_status === "succeeded").length;
  const durations = records.map((record) => numberValue(record.duration_ms)).sort((a, b) => a - b);
  const totals = Object.fromEntries(COUNT_FIELDS.map((field) => [
    field,
    records.reduce((sum, record) => sum + numberValue(record[field]), 0),
  ]));
  const agentAssistedScans = records.filter(isAgentAssistedScan).length;

  return {
    generated_at: new Date().toISOString(),
    range_days: days,
    record_count: records.length,
    truncated: records.length === MAX_RECORDS,
    summary: {
      total_scans: records.length,
      succeeded_scans: succeeded,
      failed_scans: records.length - succeeded,
      success_rate: records.length ? succeeded / records.length : 0,
      median_duration_ms: percentile(durations, 0.5),
      p95_duration_ms: percentile(durations, 0.95),
      agent_assisted_scans: agentAssistedScans,
      agent_trace_scans: records.filter((record) => record.agent_trace_present === true).length,
      ...totals,
    },
    timeseries: groupByDay(records),
    companies: groupCompanies(records),
    versions: groupCounts(records, "app_version"),
    failures: groupCounts(records.filter((record) => record.scan_status === "failed"), "error_type"),
    breakdowns: {
      role_status: aggregateBreakdown(latestClientRecords, "role_status_counts"),
      autoprep_outcome: aggregateBreakdown(latestClientRecords, "autoprep_outcome_counts"),
      page_confidence: aggregateBreakdown(records, "page_confidence_counts"),
      candidate_confidence: aggregateBreakdown(records, "candidate_confidence_counts"),
      candidate_selection: aggregateBreakdown(records, "candidate_selection_counts"),
      candidate_discovery_method: aggregateBreakdown(
        records, "candidate_discovery_method_counts",
      ),
      verification_status: aggregateBreakdown(records, "verification_status_counts"),
      verification_outcome: aggregateBreakdown(records, "verification_outcome_counts"),
      extraction_method: aggregateBreakdown(records, "extraction_method_counts"),
      rejection_reason: aggregateBreakdown(records, "rejection_reason_counts"),
    },
  };
}

export function isAgentAssistedScan(record: MetricRecord): boolean {
  if (record.agent_trace_present === true) return true;
  return breakdownCount(record.candidate_discovery_method_counts, "agent") > 0 ||
    breakdownCount(record.candidate_discovery_method_counts, "heuristic+agent") > 0 ||
    breakdownCount(record.extraction_method_counts, "llm") > 0;
}

function breakdownCount(value: unknown, category: string): number {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return 0;
  return numberValue((value as Record<string, unknown>)[category]);
}

function latestByClient(records: MetricRecord[]): MetricRecord[] {
  const latest = new Map<string, MetricRecord>();
  for (const record of records) {
    const clientId = String(record.client_id ?? "").trim();
    if (clientId) latest.set(clientId, record);
  }
  return [...latest.values()];
}

function parseDays(value: unknown): number | null {
  if (value === "all") return null;
  const parsed = Number(value ?? 30);
  return [7, 30, 90].includes(parsed) ? parsed : 30;
}

function numberValue(value: unknown): number {
  return typeof value === "number" && Number.isFinite(value) && value >= 0 ? value : 0;
}

function percentile(sorted: number[], fraction: number): number {
  if (!sorted.length) return 0;
  return sorted[Math.min(sorted.length - 1, Math.ceil(sorted.length * fraction) - 1)];
}

function groupByDay(records: MetricRecord[]): object[] {
  const groups = new Map<string, MetricRecord[]>();
  for (const record of records) {
    const timestamp = String(record.finished_at ?? record.received_at ?? "");
    const day = timestamp.slice(0, 10);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) continue;
    groups.set(day, [...(groups.get(day) ?? []), record]);
  }
  return [...groups.entries()].map(([date, items]) => ({
    date,
    scans: items.length,
    succeeded: items.filter((item) => item.scan_status === "succeeded").length,
    roles_discovered: items.reduce(
      (sum, item) => sum + numberValue(item.potential_roles_discovered), 0,
    ),
    roles_saved: items.reduce((sum, item) => sum + numberValue(item.roles_saved), 0),
  }));
}

function groupCompanies(records: MetricRecord[]): object[] {
  const groups = new Map<string, MetricRecord[]>();
  for (const record of records) {
    const company = String(record.company_name ?? "Unknown company").trim() || "Unknown company";
    groups.set(company, [...(groups.get(company) ?? []), record]);
  }
  return [...groups.entries()].map(([company_name, items]) => {
    const succeeded = items.filter((item) => item.scan_status === "succeeded").length;
    return {
      company_name,
      scans: items.length,
      success_rate: succeeded / items.length,
      average_duration_ms: Math.round(
        items.reduce((sum, item) => sum + numberValue(item.duration_ms), 0) / items.length,
      ),
      candidates_scanned: items.reduce(
        (sum, item) => sum + numberValue(item.candidates_scanned), 0,
      ),
      roles_discovered: items.reduce(
        (sum, item) => sum + numberValue(item.potential_roles_discovered), 0,
      ),
      roles_saved: items.reduce((sum, item) => sum + numberValue(item.roles_saved), 0),
      failed_role_visits: items.reduce(
        (sum, item) => sum + numberValue(item.failed_role_visits), 0,
      ),
    };
  }).sort((left, right) => right.scans - left.scans || left.company_name.localeCompare(right.company_name));
}

function groupCounts(records: MetricRecord[], field: string): object[] {
  const counts = new Map<string, number>();
  for (const record of records) {
    const label = String(record[field] ?? (field === "error_type" ? "unspecified" : "unknown"));
    counts.set(label, (counts.get(label) ?? 0) + 1);
  }
  return [...counts.entries()].map(([label, count]) => ({label, count}))
    .sort((left, right) => right.count - left.count || left.label.localeCompare(right.label));
}

function aggregateBreakdown(records: MetricRecord[], field: string): object[] {
  const counts = new Map<string, number>();
  for (const record of records) {
    const value = record[field];
    if (typeof value !== "object" || value === null || Array.isArray(value)) continue;
    for (const [label, count] of Object.entries(value)) {
      counts.set(label, (counts.get(label) ?? 0) + numberValue(count));
    }
  }
  return [...counts.entries()].map(([label, count]) => ({label, count}))
    .sort((left, right) => right.count - left.count || left.label.localeCompare(right.label));
}
