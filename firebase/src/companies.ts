import {FieldValue, type Firestore} from "firebase-admin/firestore";

import type {
  CentralCompany,
  CompanyTier,
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
  const submittedTier = companyTier(request.prestige_tier);
  const tierSourceId = sourceId(request.tier_source_id);
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
    const defaultTier = await recordCompanyTier(
      db,
      best.candidate.id,
      submittedTier,
      tierSourceId,
    );
    const returnedCareerPageUrls = await mergeCompanyCareerPageUrls(
      db,
      best.candidate.id,
      careerPageUrls,
    );
    const response: ResolveCompanyResponse = {
      action: "matched",
      global_company_id: best.candidate.id,
      confidence: best.score.confidence,
      matched_on: best.score.matched_on,
      canonical_domain: domains[0] ?? null,
      normalized_name: normalizedName,
      default_tier: defaultTier,
      career_page_urls: returnedCareerPageUrls,
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
      default_tier: null,
      career_page_urls: [],
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
        career_page_urls: careerPageUrls,
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
  const defaultTier = await recordCompanyTier(db, globalCompanyId, submittedTier, tierSourceId);
  const returnedCareerPageUrls = await mergeCompanyCareerPageUrls(
    db,
    globalCompanyId,
    careerPageUrls,
  );

  const response: ResolveCompanyResponse = {
    action: "created",
    global_company_id: globalCompanyId,
    confidence: 0,
    matched_on: [],
    canonical_domain: domains[0] ?? null,
    normalized_name: normalizedName,
    default_tier: defaultTier,
    career_page_urls: returnedCareerPageUrls,
    candidates: [],
  };
  return includeMetadata ? response : redactResolveResponse(response);
}

export async function listCompanies(db: Firestore): Promise<CentralCompany[]> {
  const snapshot = await db.collection("companies").orderBy("updated_at", "desc").limit(10000).get();
  return snapshot.docs.map((doc) => {
    const data = doc.data();
    return {
      global_company_id: doc.id,
      display_name: stringValue(data.display_name, doc.id),
      normalized_names: stringArray(data.normalized_names),
      compact_names: stringArray(data.compact_names),
      domains: stringArray(data.domains),
      ats_slugs: stringArray(data.ats_slugs),
      aliases: stringArray(data.aliases),
      default_tier: storedCompanyTier(data.default_tier),
      career_page_urls: stringArray(data.career_page_urls),
    };
  });
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
  return {
    global_company_id: response.global_company_id,
    default_tier: response.default_tier,
  };
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

export function companyTier(value: unknown): CompanyTier | null {
  if (value === null || value === undefined || value === "") {
    return null;
  }
  if (typeof value !== "string") {
    throw new Error("prestige_tier must be a string from 0 to 7");
  }
  const cleaned = value.trim();
  if (!/^[0-7]$/.test(cleaned)) {
    throw new Error("prestige_tier must be from 0 to 7");
  }
  return cleaned as CompanyTier;
}

function storedCompanyTier(value: unknown): CompanyTier | null {
  try {
    return companyTier(value);
  } catch {
    return null;
  }
}

function sourceId(value: unknown): string | null {
  if (typeof value !== "string") {
    return null;
  }
  const cleaned = value.trim().replace(/[^A-Za-z0-9_-]/g, "").slice(0, 80);
  return cleaned || null;
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

async function recordCompanyTier(
  db: Firestore,
  globalCompanyId: string,
  tier: CompanyTier | null,
  tierSourceId: string | null,
): Promise<CompanyTier | null> {
  if (tier === null || tierSourceId === null) {
    const company = await db.collection("companies").doc(globalCompanyId).get();
    return storedCompanyTier(company.get("default_tier"));
  }

  const companyRef = db.collection("companies").doc(globalCompanyId);
  const voteRef = companyRef.collection("tierVotes").doc(tierSourceId);
  return db.runTransaction(async (transaction) => {
    const votes = await transaction.get(companyRef.collection("tierVotes"));
    const tierBySource = new Map<string, CompanyTier>();
    for (const doc of votes.docs) {
      const savedTier = storedCompanyTier(doc.get("tier"));
      if (savedTier !== null) {
        tierBySource.set(doc.id, savedTier);
      }
    }
    tierBySource.set(tierSourceId, tier);
    const tiers = [...tierBySource.values()]
      .map((value) => Number(value))
      .sort((left, right) => left - right);
    const defaultTier = medianTier(tiers);
    transaction.set(
      voteRef,
      {
        tier,
        updated_at: new Date().toISOString(),
      },
      {merge: true},
    );
    transaction.set(
      companyRef,
      {
        default_tier: defaultTier,
        updated_at: new Date().toISOString(),
      },
      {merge: true},
    );
    return defaultTier;
  });
}

function medianTier(tiers: number[]): CompanyTier | null {
  if (tiers.length === 0) {
    return null;
  }
  const middle = Math.floor(tiers.length / 2);
  if (tiers.length % 2 === 1) {
    return String(tiers[middle]) as CompanyTier;
  }
  return String(Math.round((tiers[middle - 1] + tiers[middle]) / 2)) as CompanyTier;
}

async function mergeCompanyCareerPageUrls(
  db: Firestore,
  globalCompanyId: string,
  careerPageUrls: string[],
): Promise<string[]> {
  const companyRef = db.collection("companies").doc(globalCompanyId);
  const uniqueUrls = unique(careerPageUrls);
  if (uniqueUrls.length > 0) {
    await companyRef.set(
      {
        career_page_urls: FieldValue.arrayUnion(...uniqueUrls),
        updated_at: new Date().toISOString(),
      },
      {merge: true},
    );
  }
  const company = await companyRef.get();
  return stringArray(company.get("career_page_urls"));
}
