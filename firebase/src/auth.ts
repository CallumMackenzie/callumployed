import crypto from "node:crypto";

import type {Request, Response, NextFunction} from "express";
import {defineSecret} from "firebase-functions/params";

export const centralPasskeySha256 = defineSecret("CENTRAL_PASSKEY_SHA256");
export const DASHBOARD_SESSION_COOKIE = "callumployed_dashboard_session";
const DASHBOARD_SESSION_SECONDS = 12 * 60 * 60;

export function requirePasskey(req: Request, res: Response, next: NextFunction): void {
  if (!hasValidPasskey(req)) {
    res.status(401).json({error: "unauthorized"});
    return;
  }
  next();
}

export function hasValidPasskey(req: Request): boolean {
  const authHeader = req.header("authorization") ?? "";
  const customHeaderPasskey = req.header("x-callumployed-passkey")?.trim() ?? "";
  const bearerPasskey = authHeader.startsWith("Bearer ")
    ? authHeader.slice("Bearer ".length).trim()
    : "";
  const providedPasskey = customHeaderPasskey || bearerPasskey;
  return verifyPasskey(providedPasskey);
}

export function verifyPasskey(providedPasskey: string): boolean {
  const expectedHash = centralPasskeySha256.value();
  if (!expectedHash || !providedPasskey.trim()) return false;
  const providedHash = crypto.createHash("sha256").update(providedPasskey).digest("hex");
  return timingSafeEqual(providedHash, expectedHash);
}

export function createDashboardSession(now = Date.now()): string {
  const payload = Buffer.from(JSON.stringify({exp: now + DASHBOARD_SESSION_SECONDS * 1000}))
    .toString("base64url");
  return `${payload}.${signDashboardSession(payload)}`;
}

export function hasValidDashboardSession(req: Request, now = Date.now()): boolean {
  const secret = centralPasskeySha256.value();
  if (!secret) return false;
  const token = parseCookies(req.header("cookie") ?? "")[DASHBOARD_SESSION_COOKIE];
  if (!token) return false;
  const [payload, signature, extra] = token.split(".");
  if (!payload || !signature || extra || !timingSafeEqual(signature, signDashboardSession(payload))) {
    return false;
  }
  try {
    const parsed = JSON.parse(Buffer.from(payload, "base64url").toString("utf8")) as {exp?: unknown};
    return typeof parsed.exp === "number" && parsed.exp > now;
  } catch {
    return false;
  }
}

export function requireDashboardSession(
  req: Request,
  res: Response,
  next: NextFunction,
): void {
  if (!hasValidDashboardSession(req)) {
    res.status(401).json({error: "unauthorized"});
    return;
  }
  next();
}

export function dashboardSessionCookie(token: string): string {
  return [
    `${DASHBOARD_SESSION_COOKIE}=${token}`,
    "Path=/",
    `Max-Age=${DASHBOARD_SESSION_SECONDS}`,
    "HttpOnly",
    "Secure",
    "SameSite=Strict",
  ].join("; ");
}

export function clearDashboardSessionCookie(): string {
  return `${DASHBOARD_SESSION_COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Strict`;
}

function signDashboardSession(payload: string): string {
  const secret = centralPasskeySha256.value();
  return crypto.createHmac("sha256", secret).update(payload).digest("base64url");
}

function parseCookies(header: string): Record<string, string> {
  return Object.fromEntries(header.split(";").flatMap((part) => {
    const separator = part.indexOf("=");
    if (separator < 0) return [];
    const key = part.slice(0, separator).trim();
    const value = part.slice(separator + 1).trim();
    return key ? [[key, value]] : [];
  }));
}

function timingSafeEqual(left: string, right: string): boolean {
  const leftBuffer = Buffer.from(left);
  const rightBuffer = Buffer.from(right);
  return leftBuffer.length === rightBuffer.length && crypto.timingSafeEqual(leftBuffer, rightBuffer);
}
