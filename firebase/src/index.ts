import express from "express";
import {initializeApp} from "firebase-admin/app";
import {getFirestore} from "firebase-admin/firestore";
import {onRequest} from "firebase-functions/v2/https";

import {
  centralPasskeySha256,
  clearDashboardSessionCookie,
  createDashboardSession,
  dashboardSessionCookie,
  hasValidDashboardSession,
  hasValidPasskey,
  requireDashboardSession,
  requirePasskey,
  verifyPasskey,
} from "./auth";
import {listCompanies, resolveCompany} from "./companies";
import {dashboardLoginPage, dashboardPage} from "./dashboard";
import {buildDashboardMetrics} from "./dashboardMetrics";
import {bulkUpsertRoles, listRoles} from "./roles";
import {submitScanMetrics} from "./scanMetrics";

initializeApp();

const app = express();
app.use(express.json({limit: "1mb"}));
app.use(express.urlencoded({extended: false, limit: "16kb"}));

app.get("/dashboard", (req, res) => {
  setDashboardHeaders(res);
  res.type("html").send(
    hasValidDashboardSession(req) ? dashboardPage() : dashboardLoginPage(),
  );
});

app.post("/dashboard/login", (req, res) => {
  setDashboardHeaders(res);
  const passkey = typeof req.body?.passkey === "string" ? req.body.passkey : "";
  if (!verifyPasskey(passkey)) {
    res.status(401).type("html").send(dashboardLoginPage(true));
    return;
  }
  res.setHeader("Set-Cookie", dashboardSessionCookie(createDashboardSession()));
  res.redirect(303, "../dashboard");
});

app.post("/dashboard/logout", (_req, res) => {
  setDashboardHeaders(res);
  res.setHeader("Set-Cookie", clearDashboardSessionCookie());
  res.redirect(303, "../dashboard");
});

app.get("/v1/dashboard/metrics", requireDashboardSession, async (req, res) => {
  res.setHeader("Cache-Control", "private, no-store");
  try {
    res.json(await buildDashboardMetrics(getFirestore(), req.query.days));
  } catch (error) {
    console.error("Dashboard metrics query failed", error);
    res.status(500).json({error: "could not load dashboard metrics"});
  }
});

app.post("/v1/companies/resolve", async (req, res) => {
  try {
    res.json(await resolveCompany(getFirestore(), req.body, hasValidPasskey(req)));
  } catch (error) {
    res.status(400).json({error: error instanceof Error ? error.message : "invalid request"});
  }
});

app.get("/v1/companies", requirePasskey, async (_req, res) => {
  res.json({companies: await listCompanies(getFirestore())});
});

app.get("/v1/roles", requirePasskey, async (_req, res) => {
  res.json({roles: await listRoles(getFirestore())});
});

app.post("/v1/roles/bulk-upsert", requirePasskey, async (req, res) => {
  const roles = Array.isArray(req.body?.roles) ? req.body.roles : [];
  res.json({upserted: await bulkUpsertRoles(getFirestore(), roles)});
});

app.post("/v1/scan-metrics", async (req, res) => {
  try {
    const scanMetricId = await submitScanMetrics(getFirestore(), req.body ?? {});
    res.json({accepted: true, scan_metric_id: scanMetricId});
  } catch (error) {
    res.status(400).json({error: error instanceof Error ? error.message : "invalid request"});
  }
});

export const centralApi = onRequest(
  {
    secrets: [centralPasskeySha256],
    region: "us-central1",
  },
  app,
);

function setDashboardHeaders(res: express.Response): void {
  res.setHeader("Cache-Control", "private, no-store");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader(
    "Content-Security-Policy",
    "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; " +
      "connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
  );
}
