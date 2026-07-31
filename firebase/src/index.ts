import express from "express";
import {initializeApp} from "firebase-admin/app";
import {getFirestore} from "firebase-admin/firestore";
import {onRequest} from "firebase-functions/v2/https";

import {centralPasskeySha256, hasValidPasskey, requirePasskey} from "./auth";
import {resolveCompany} from "./companies";
import {bulkUpsertRoles, listRoles} from "./roles";

initializeApp();

const app = express();
app.use(express.json({limit: "1mb"}));

app.post("/v1/companies/resolve", async (req, res) => {
  try {
    res.json(await resolveCompany(getFirestore(), req.body, hasValidPasskey(req)));
  } catch (error) {
    res.status(400).json({error: error instanceof Error ? error.message : "invalid request"});
  }
});

app.get("/v1/roles", requirePasskey, async (_req, res) => {
  res.json({roles: await listRoles(getFirestore())});
});

app.post("/v1/roles/bulk-upsert", requirePasskey, async (req, res) => {
  const roles = Array.isArray(req.body?.roles) ? req.body.roles : [];
  res.json({upserted: await bulkUpsertRoles(getFirestore(), roles)});
});

export const centralApi = onRequest(
  {
    secrets: [centralPasskeySha256],
    region: "us-central1",
  },
  app,
);
