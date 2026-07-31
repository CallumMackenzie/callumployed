import {
  atsSlug,
  canonicalDomain,
  compactName,
  normalizeCompanyName,
} from "./normalization";

export interface CompanyCandidate {
  id: string;
  display_name: string;
  normalized_names?: string[];
  domains?: string[];
  ats_slugs?: string[];
  aliases?: string[];
}

export interface IncomingCompany {
  name: string;
  career_page_urls: string[];
  role_urls: string[];
}

export interface ScoreResult {
  confidence: number;
  matched_on: string[];
}

export function scoreCompany(candidate: CompanyCandidate, incoming: IncomingCompany): ScoreResult {
  let confidence = 0;
  const matchedOn = new Set<string>();
  const incomingName = normalizeCompanyName(incoming.name);
  const incomingCompactName = compactName(incoming.name);
  const urls = [...incoming.career_page_urls, ...incoming.role_urls];
  const incomingDomains = new Set(urls.map(canonicalDomain).filter((domain) => domain !== null));
  const incomingAtsSlugs = new Set(urls.map(atsSlug).filter((slug) => slug !== null));

  const candidateNames = new Set([
    normalizeCompanyName(candidate.display_name),
    ...(candidate.normalized_names ?? []).map(normalizeCompanyName),
    ...(candidate.aliases ?? []).map(normalizeCompanyName),
  ]);
  const candidateCompactNames = new Set([...candidateNames].map((name) => name.replace(/\s+/g, "")));
  const candidateDomains = new Set((candidate.domains ?? []).map((domain) => domain.toLowerCase()));
  const candidateAtsSlugs = new Set((candidate.ats_slugs ?? []).map((slug) => slug.toLowerCase()));

  if (hasIntersection(incomingDomains, candidateDomains)) {
    confidence += 100;
    matchedOn.add("domain");
  }
  if (hasIntersection(incomingAtsSlugs, candidateAtsSlugs)) {
    confidence += 90;
    matchedOn.add("ats_slug");
  }
  if (candidateNames.has(incomingName)) {
    confidence += 80;
    matchedOn.add("normalized_name");
  }
  if (candidateCompactNames.has(incomingCompactName)) {
    confidence += 50;
    matchedOn.add("compact_name");
  }

  return {
    confidence,
    matched_on: [...matchedOn],
  };
}

function hasIntersection(left: Set<string>, right: Set<string>): boolean {
  for (const value of left) {
    if (right.has(value)) {
      return true;
    }
  }
  return false;
}

