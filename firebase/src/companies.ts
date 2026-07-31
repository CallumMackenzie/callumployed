import {FieldValue, type Firestore} from "firebase-admin/firestore";

import type {
  PublicResolveCompanyResponse,
  ResolveCompanyRequest,
  ResolveCompanyResponse,
} from "./contracts";
import {
  atsSlug,
  canonicalDomain,
  compactName,
  normalizeCompanyName,
  stableId,
} from "./normalization";
import {scoreCompany, type CompanyCandidate} from "./scoring";

const AUTO_MATCH_THRESHOLD = 90;
const REVIEW_THRESHOLD = 70;

export async function resolveCompany(
  db: Firestore,
  request: ResolveCompanyRequest,
  includeMetadata: boolean,
): Promise<ResolveCompanyResponse | PublicResolveCompanyResponse> {
  const name = requiredString(request.name, "name");
  const careerPageUrls = stringArray(request.career_page_urls);
  const roleUrls = stringArray(request.role_urls);
  const urls = [...careerPageUrls, ...roleUrls];
  const normalizedName = normalizeCompanyName(name);
  const domains = unique(urls.map(canonicalDomain).filter((domain) => domain !== null));
  const atsSlugs = unique(urls.map(atsSlug).filter((slug) => slug !== null));
  const candidateIds = await candidateCompanyIds(db, normalizedName, domains, atsSlugs);
  const candidates = await loadCandidates(db, candidateIds);
  const scored = candidates
    .map((candidate) => ({
      candidate,
      score: scoreCompany(candidate, {name, career_page_urls: careerPageUrls, role_urls: roleUrls}),
    }))
    .sort((left, right) => right.score.confidence - left.score.confidence);

  const best = scored[0];
  if (best && best.score.confidence >= AUTO_MATCH_THRESHOLD) {
    const response: ResolveCompanyResponse = {
      action: "matched",
      global_company_id: best.candidate.id,
      confidence: best.score.confidence,
      matched_on: best.score.matched_on,
      canonical_domain: domains[0] ?? null,
      normalized_name: normalizedName,
      candidates: scored.slice(0, 5).map(toCandidateResponse),
    };
    return includeMetadata ? response : redactResolveResponse(response);
  }
  if (includeMetadata && best && best.score.confidence >= REVIEW_THRESHOLD) {
    return {
      action: "needs_review",
      global_company_id: null,
      confidence: best.score.confidence,
      matched_on: best.score.matched_on,
      canonical_domain: domains[0] ?? null,
      normalized_name: normalizedName,
      candidates: scored.slice(0, 5).map(toCandidateResponse),
    };
  }

  const globalCompanyId = stableId("co", domains[0] ?? normalizedName);
  await db.runTransaction(async (transaction) => {
    const companyRef = db.collection("companies").doc(globalCompanyId);
    const company = await transaction.get(companyRef);
    if (!company.exists) {
      transaction.set(companyRef, {
        display_name: name,
        normalized_names: [normalizedName],
        compact_names: [compactName(name)],
        domains,
        ats_slugs: atsSlugs,
        aliases: [],
        default_tier: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      });
    }
    for (const domain of domains) {
      transaction.set(db.collection("companyDomains").doc(domain), {global_company_id: globalCompanyId});
    }
    for (const slug of atsSlugs) {
      transaction.set(db.collection("companyAtsSlugs").doc(slug), {global_company_id: globalCompanyId});
    }
    transaction.set(
      db.collection("companyNames").doc(normalizedName),
      {global_company_ids: FieldValue.arrayUnion(globalCompanyId)},
      {merge: true},
    );
  });

  const response: ResolveCompanyResponse = {
    action: "created",
    global_company_id: globalCompanyId,
    confidence: 0,
    matched_on: [],
    canonical_domain: domains[0] ?? null,
    normalized_name: normalizedName,
    candidates: [],
  };
  return includeMetadata ? response : redactResolveResponse(response);
}

async function candidateCompanyIds(
  db: Firestore,
  normalizedName: string,
  domains: string[],
  atsSlugs: string[],
): Promise<string[]> {
  const ids = new Set<string>();
  for (const domain of domains) {
    const doc = await db.collection("companyDomains").doc(domain).get();
    const id = doc.get("global_company_id");
    if (typeof id === "string") {
      ids.add(id);
    }
  }
  for (const slug of atsSlugs) {
    const doc = await db.collection("companyAtsSlugs").doc(slug).get();
    const id = doc.get("global_company_id");
    if (typeof id === "string") {
      ids.add(id);
    }
  }
  const nameDoc = await db.collection("companyNames").doc(normalizedName).get();
  const nameIds = nameDoc.get("global_company_ids");
  if (Array.isArray(nameIds)) {
    for (const id of nameIds) {
      if (typeof id === "string") {
        ids.add(id);
      }
    }
  }
  return [...ids];
}

async function loadCandidates(db: Firestore, ids: string[]): Promise<CompanyCandidate[]> {
  const candidates: CompanyCandidate[] = [];
  for (const id of ids) {
    const doc = await db.collection("companies").doc(id).get();
    if (!doc.exists) {
      continue;
    }
    const data = doc.data() ?? {};
    candidates.push({
      id,
      display_name: stringValue(data.display_name, id),
      normalized_names: stringArray(data.normalized_names),
      domains: stringArray(data.domains),
      ats_slugs: stringArray(data.ats_slugs),
      aliases: stringArray(data.aliases),
    });
  }
  return candidates;
}

function toCandidateResponse(scored: {
  candidate: CompanyCandidate;
  score: {confidence: number; matched_on: string[]};
}): Record<string, unknown> {
  return {
    global_company_id: scored.candidate.id,
    display_name: scored.candidate.display_name,
    confidence: scored.score.confidence,
    matched_on: scored.score.matched_on,
  };
}

function redactResolveResponse(
  response: ResolveCompanyResponse,
): PublicResolveCompanyResponse {
  return {global_company_id: response.global_company_id};
}

function requiredString(value: unknown, field: string): string {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`${field} is required`);
  }
  return value.trim();
}

function stringValue(value: unknown, fallback: string): string {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function stringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }
  return value.filter((item): item is string => typeof item === "string" && item.trim() !== "");
}

function unique(values: string[]): string[] {
  return [...new Set(values)];
}
