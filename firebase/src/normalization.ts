import crypto from "node:crypto";

const COMPANY_SUFFIXES = /\b(inc|incorporated|llc|ltd|limited|corp|corporation|co|company)\b/g;

export function normalizeCompanyName(name: string): string {
  return name
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(COMPANY_SUFFIXES, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .replace(/\s+/g, " ");
}

export function compactName(name: string): string {
  return normalizeCompanyName(name).replace(/\s+/g, "");
}

export function canonicalDomain(rawUrl: string): string | null {
  try {
    const parsed = new URL(rawUrl);
    return parsed.hostname.toLowerCase().replace(/^www\./, "");
  } catch {
    return null;
  }
}

export function atsSlug(rawUrl: string): string | null {
  try {
    const parsed = new URL(rawUrl);
    const host = parsed.hostname.toLowerCase().replace(/^www\./, "");
    const segments = parsed.pathname.split("/").filter(Boolean);
    if (host === "boards.greenhouse.io" && segments[0]) {
      return `greenhouse:${segments[0].toLowerCase()}`;
    }
    if (host === "jobs.lever.co" && segments[0]) {
      return `lever:${segments[0].toLowerCase()}`;
    }
    if (host.endsWith(".ashbyhq.com")) {
      return `ashby:${host.split(".")[0]}`;
    }
    if (host.endsWith(".workdayjobs.com")) {
      return `workday:${host.split(".")[0]}`;
    }
    return null;
  } catch {
    return null;
  }
}

export function canonicalRoleUrl(rawUrl: string): string {
  const parsed = new URL(rawUrl);
  const ignoredParams = new Set([
    "gh_jid",
    "ref",
    "source",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
  ]);
  for (const param of [...parsed.searchParams.keys()]) {
    if (ignoredParams.has(param.toLowerCase())) {
      parsed.searchParams.delete(param);
    }
  }
  parsed.hash = "";
  parsed.pathname = parsed.pathname.replace(/\/+$/, "") || "/";
  return parsed.toString();
}

export function stableId(prefix: string, value: string): string {
  const hash = crypto.createHash("sha256").update(value).digest("hex").slice(0, 24);
  return `${prefix}_${hash}`;
}

