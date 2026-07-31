import type {Firestore} from "firebase-admin/firestore";

import type {BulkUpsertRole, CentralRole} from "./contracts";
import {canonicalRoleUrl, stableId} from "./normalization";

export async function listRoles(db: Firestore): Promise<CentralRole[]> {
  const snapshot = await db.collection("roles").orderBy("updated_at", "desc").limit(5000).get();
  return snapshot.docs.map((doc) => {
    const data = doc.data();
    return {
      global_role_id: doc.id,
      global_company_id: stringValue(data.global_company_id, ""),
      company_name: stringValue(data.company_name, ""),
      title: stringValue(data.title, ""),
      role_url: stringValue(data.role_url, ""),
      location: nullableString(data.location),
      description: nullableString(data.description),
      posting_id: nullableString(data.posting_id),
      tier_classification: nullableString(data.tier_classification),
      status: data.status === "open" || data.status === "closed" ? data.status : "unknown",
    };
  });
}

export async function bulkUpsertRoles(db: Firestore, roles: BulkUpsertRole[]): Promise<number> {
  const batch = db.batch();
  let upserted = 0;
  for (const role of roles) {
    if (!role.global_company_id || !role.title || !role.role_url) {
      continue;
    }
    const canonicalUrl = canonicalRoleUrl(role.role_url);
    const roleId = stableId("role", `${role.global_company_id}:${canonicalUrl}`);
    const company = await db.collection("companies").doc(role.global_company_id).get();
    const companyName = stringValue(company.get("display_name"), role.global_company_id);
    batch.set(
      db.collection("roles").doc(roleId),
      {
        global_company_id: role.global_company_id,
        company_name: companyName,
        title: role.title,
        role_url: role.role_url,
        canonical_role_url: canonicalUrl,
        location: role.location ?? null,
        description: role.description ?? null,
        posting_id: role.posting_id ?? null,
        tier_classification: role.tier_classification ?? null,
        status: "unknown",
        updated_at: new Date().toISOString(),
      },
      {merge: true},
    );
    upserted += 1;
  }
  await batch.commit();
  return upserted;
}

function stringValue(value: unknown, fallback: string): string {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function nullableString(value: unknown): string | null {
  return typeof value === "string" && value.trim() ? value : null;
}

