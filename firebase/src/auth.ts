import crypto from "node:crypto";

import type {Request, Response, NextFunction} from "express";
import {defineSecret} from "firebase-functions/params";

export const centralPasskeySha256 = defineSecret("CENTRAL_PASSKEY_SHA256");

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
  const expectedHash = centralPasskeySha256.value();
  if (!expectedHash || !providedPasskey) {
    return false;
  }

  const providedHash = crypto.createHash("sha256").update(providedPasskey).digest("hex");
  if (!timingSafeEqual(providedHash, expectedHash)) {
    return false;
  }
  return true;
}

function timingSafeEqual(left: string, right: string): boolean {
  const leftBuffer = Buffer.from(left);
  const rightBuffer = Buffer.from(right);
  return leftBuffer.length === rightBuffer.length && crypto.timingSafeEqual(leftBuffer, rightBuffer);
}
