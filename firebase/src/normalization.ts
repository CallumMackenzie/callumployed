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
    const host = parsed.hostname.toLowerCase().replace(/^www\./, "");
    return isSharedAtsHost(host) ? null : host;
  } catch {
    return null;
  }
}

export function atsSlug(rawUrl: string): string | null {
  try {
    const parsed = new URL(rawUrl);
    const host = parsed.hostname.toLowerCase().replace(/^www\./, "");
    const segments = parsed.pathname.split("/").filter(Boolean);
    if ((host === "boards.greenhouse.io" || host === "job-boards.greenhouse.io") && segments[0]) {
      return `greenhouse:${segments[0].toLowerCase()}`;
    }
    if (host === "jobs.lever.co" && segments[0]) {
      return `lever:${segments[0].toLowerCase()}`;
    }
    if (host === "jobs.ashbyhq.com" && segments[0]) {
      return `ashby:${segments[0].toLowerCase()}`;
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
  parsed.searchParams.sort();
  return parsed.toString();
}

export function roleIdentity(rawUrl: string, postingId?: string | null): string | null {
  const parsed = new URL(rawUrl);
  const host = parsed.hostname.toLowerCase().replace(/^www\./, "");
  const segments = parsed.pathname.split("/").filter(Boolean);
  const board = atsSlug(rawUrl);

  if (host === "boards.greenhouse.io" || host === "job-boards.greenhouse.io") {
    const jobsIndex = segments.findIndex((segment) => segment.toLowerCase() === "jobs");
    const urlPostingId = jobsIndex >= 0 ? segments[jobsIndex + 1] : null;
    const greenhouseId = urlPostingId || parsed.searchParams.get("gh_jid") || postingId;
    return board && greenhouseId ? `${board}:job:${greenhouseId}` : null;
  }

  if (host === "jobs.ashbyhq.com" || host.endsWith(".ashbyhq.com")) {
    const postingSegment = host === "jobs.ashbyhq.com" ? segments[1] : segments[0];
    const ashbyId = postingSegment || postingId;
    return board && ashbyId ? `${board}:job:${ashbyId.toLowerCase()}` : null;
  }

  if (host === "jobs.lever.co") {
    const leverId = segments[1] || postingId;
    return board && leverId ? `${board}:job:${leverId.toLowerCase()}` : null;
  }

  if (postingId) {
    return `posting:${host}:${postingId.toLowerCase()}`;
  }

  const canonical = canonicalRoleUrl(rawUrl);
  return isGenericCareerPath(parsed.pathname) ? null : `url:${canonical}`;
}

export function isSharedAtsHost(host: string): boolean {
  return host === "boards.greenhouse.io" ||
    host === "job-boards.greenhouse.io" ||
    host === "jobs.ashbyhq.com" ||
    host === "jobs.lever.co";
}

function isGenericCareerPath(pathname: string): boolean {
  const normalized = pathname.replace(/\/+$/, "").toLowerCase();
  return normalized === "" || normalized === "/" ||
    /\/(careers?|jobs?|opportunities)$/.test(normalized);
}

export function stableId(prefix: string, value: string): string {
  const hash = crypto.createHash("sha256").update(value).digest("hex").slice(0, 24);
  return `${prefix}_${hash}`;
}
