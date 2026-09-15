const fs = require("node:fs/promises");
const os = require("node:os");
const path = require("node:path");

const {initializeApp} = require("firebase-admin/app");
const {FieldValue, getFirestore} = require("firebase-admin/firestore");

const {
  atsSlug,
  canonicalRoleUrl,
  normalizeCompanyName,
  compactName,
  roleIdentity,
  stableId,
} = require("../lib/normalization.js");

const PROJECT_ID = "callumployed-central";
const RAMP_ID = "co_4a973f988e2541d014890979";
const RADIX_ID = "co_31aa52aeec419c8e07ece098";
const WAABI_ID = "co_6a8f48bb71101122f7fb13dc";
const COMPANY_REPAIRS = [
  {id: RAMP_ID, name: "Ramp", slug: "ashby:ramp", url: "https://jobs.ashbyhq.com/ramp"},
  {
    id: stableId("co", "ashby:cohere"),
    name: "Cohere",
    slug: "ashby:cohere",
    url: "https://jobs.ashbyhq.com/cohere",
  },
  {
    id: stableId("co", "ashby:mistral.ai"),
    name: "Mistral AI",
    slug: "ashby:mistral.ai",
    url: "https://jobs.ashbyhq.com/mistral.ai",
  },
  {
    id: stableId("co", "ashby:rivianvw.tech"),
    name: "Rivian and Volkswagen Group Technologies",
    slug: "ashby:rivianvw.tech",
    url: "https://jobs.ashbyhq.com/rivianvw.tech",
  },
  {
    id: stableId("co", "ashby:saronic"),
    name: "Saronic Technologies",
    slug: "ashby:saronic",
    url: "https://jobs.ashbyhq.com/saronic",
  },
  {
    id: stableId("co", "ashby:wealthsimple"),
    name: "Wealthsimple",
    slug: "ashby:wealthsimple",
    url: "https://jobs.ashbyhq.com/wealthsimple",
  },
  {
    id: stableId("co", "ashby:etched"),
    name: "Etched",
    slug: "ashby:etched",
    url: "https://jobs.ashbyhq.com/etched",
  },
  {
    id: stableId("co", "ashby:superhuman%20platform%20inc"),
    name: "Superhuman",
    slug: "ashby:superhuman%20platform%20inc",
    url: "https://jobs.ashbyhq.com/superhuman%20platform%20inc",
  },
  {
    id: stableId("co", "ashby:opengov"),
    name: "OpenGov",
    slug: "ashby:opengov",
    url: "https://jobs.ashbyhq.com/opengov",
  },
  {
    id: RADIX_ID,
    name: "Radix Trading",
    slug: "greenhouse:radixuniversity",
    url: "https://job-boards.greenhouse.io/radixuniversity",
  },
  {
    id: stableId("co", "greenhouse:aquaticcapitalmanagement"),
    name: "Aquatic Capital Management",
    slug: "greenhouse:aquaticcapitalmanagement",
    url: "https://job-boards.greenhouse.io/aquaticcapitalmanagement",
  },
  {
    id: stableId("co", "greenhouse:waterloocoop"),
    name: "PlayStation Waterloo Co-Op",
    slug: "greenhouse:waterloocoop",
    url: "https://job-boards.greenhouse.io/waterloocoop",
  },
  {
    id: stableId("co", "greenhouse:schonfeld"),
    name: "Schonfeld",
    slug: "greenhouse:schonfeld",
    url: "https://job-boards.greenhouse.io/schonfeld",
  },
  {
    id: WAABI_ID,
    name: "Waabi",
    slug: "lever:waabi",
    url: "https://jobs.lever.co/waabi",
  },
  {
    id: stableId("co", "lever:immuta"),
    name: "Immuta",
    slug: "lever:immuta",
    url: "https://jobs.lever.co/immuta",
  },
];
const OWNER_BY_SLUG = new Map(COMPANY_REPAIRS.map((company) => [company.slug, company]));

async function main() {
  const apply = process.argv.includes("--apply");
  initializeApp({projectId: PROJECT_ID});
  const db = getFirestore();
  const snapshot = await snapshotStore(db);
  const plan = buildPlan(snapshot);
  printPlan(plan, apply);
  if (!apply) {
    return;
  }

  const backupPath = await writeBackup(snapshot);
  console.log(`Backup written: ${backupPath}`);
  await applyPlan(db, snapshot);
  const repaired = await snapshotStore(db);
  const postPlan = buildPlan(repaired);
  if (
    postPlan.missingCompanies.length ||
    postPlan.incorrectLinks.length ||
    postPlan.atsIndexConflicts.length ||
    postPlan.roleConflicts.length ||
    postPlan.tierVotesToReset
  ) {
    throw new Error("post-repair audit failed");
  }
  console.log(`Repair complete: ${repaired.companies.length} companies, ${repaired.roles.length} roles`);
}

async function snapshotStore(db) {
  const collectionNames = [
    "companies",
    "companyDomains",
    "companyAtsSlugs",
    "companyNames",
    "roles",
  ];
  const snapshot = {};
  for (const collectionName of collectionNames) {
    const collection = await db.collection(collectionName).get();
    snapshot[collectionName] = collection.docs.map((doc) => ({id: doc.id, data: doc.data()}));
  }
  snapshot.tierVotes = [];
  for (const companyId of [RAMP_ID, RADIX_ID, WAABI_ID]) {
    const votes = await db.collection("companies").doc(companyId).collection("tierVotes").get();
    snapshot.tierVotes.push(...votes.docs.map((doc) => ({companyId, id: doc.id, data: doc.data()})));
  }
  return snapshot;
}

function buildPlan(snapshot) {
  const expectedById = new Map(COMPANY_REPAIRS.map((company) => [company.id, company]));
  const companyById = new Map(snapshot.companies.map((company) => [company.id, company.data]));
  const atsIndexOwners = new Map(
    snapshot.companyAtsSlugs.map((entry) => [entry.id, entry.data.global_company_id]),
  );
  const incorrectLinks = [];
  for (const stored of snapshot.companies) {
    const expected = expectedById.get(stored.id);
    for (const url of stored.data.career_page_urls || []) {
      const slug = atsSlug(url);
      const indexedOwner = slug ? atsIndexOwners.get(slug) : null;
      if (
        (expected && url !== expected.url) ||
        (slug && indexedOwner !== stored.id)
      ) {
        incorrectLinks.push({
          company: stored.data.display_name,
          url,
          slug,
          indexedOwner: indexedOwner || null,
        });
      }
    }
  }
  const atsIndexConflicts = [];
  for (const entry of snapshot.companyAtsSlugs) {
    const owner = companyById.get(entry.data.global_company_id);
    if (!owner || !(owner.ats_slugs || []).includes(entry.id)) {
      atsIndexConflicts.push({
        slug: entry.id,
        indexedOwner: entry.data.global_company_id || null,
      });
    }
  }
  for (const stored of snapshot.companies) {
    for (const slug of stored.data.ats_slugs || []) {
      if (atsIndexOwners.get(slug) !== stored.id) {
        atsIndexConflicts.push({
          slug,
          indexedOwner: atsIndexOwners.get(slug) || null,
          expectedOwner: stored.id,
        });
      }
    }
  }
  const roleConflicts = [];
  for (const stored of snapshot.roles) {
    const slug = atsSlug(stored.data.role_url || "");
    const expected = OWNER_BY_SLUG.get(slug);
    if (expected && expected.id !== stored.data.global_company_id) {
      roleConflicts.push({role: stored.id, from: stored.data.global_company_id, to: expected.id});
    }
    if (slug && !expected) {
      roleConflicts.push({role: stored.id, from: stored.data.global_company_id, to: null});
    }
  }
  return {
    companies: snapshot.companies.length,
    roles: snapshot.roles.length,
    missingCompanies: COMPANY_REPAIRS.filter(
      (company) => !snapshot.companies.some((stored) => stored.id === company.id),
    ).map((company) => company.name),
    incorrectLinks,
    atsIndexConflicts,
    roleConflicts,
    tierVotesToReset: snapshot.tierVotes.length,
  };
}

function printPlan(plan, apply) {
  console.log(apply ? "APPLYING central ATS ownership repair" : "DRY RUN central ATS ownership repair");
  console.log(JSON.stringify(plan, null, 2));
}

async function writeBackup(snapshot) {
  const directory = path.join(os.homedir(), "Downloads", "callumployed-central-backups");
  await fs.mkdir(directory, {recursive: true});
  const timestamp = new Date().toISOString().replaceAll(":", "-");
  const backupPath = path.join(directory, `ats-ownership-${timestamp}.json`);
  await fs.writeFile(backupPath, JSON.stringify(snapshot, jsonReplacer, 2), {flag: "wx"});
  return backupPath;
}

async function applyPlan(db, snapshot) {
  const batch = db.batch();
  const now = new Date().toISOString();
  const storedCompanies = new Map(snapshot.companies.map((company) => [company.id, company.data]));
  for (const company of COMPANY_REPAIRS) {
    const normalizedName = normalizeCompanyName(company.name);
    const stored = storedCompanies.get(company.id);
    batch.set(
      db.collection("companies").doc(company.id),
      {
        display_name: company.name,
        normalized_names: [normalizedName],
        compact_names: [compactName(company.name)],
        domains: [],
        career_page_urls: [company.url],
        ats_slugs: [company.slug],
        aliases: stored?.aliases || [],
        updated_at: now,
        created_at: stored?.created_at || now,
        default_tier: null,
      },
      {merge: true},
    );
    batch.set(
      db.collection("companyAtsSlugs").doc(company.slug),
      {global_company_id: company.id},
    );
    batch.set(
      db.collection("companyNames").doc(normalizedName),
      {global_company_ids: FieldValue.arrayUnion(company.id)},
      {merge: true},
    );
  }
  for (const id of ["jobs.ashbyhq.com", "job-boards.greenhouse.io", "boards.greenhouse.io"]) {
    batch.delete(db.collection("companyDomains").doc(id));
  }
  batch.delete(db.collection("companyAtsSlugs").doc("ashby:jobs"));
  for (const vote of snapshot.tierVotes) {
    batch.delete(db.collection("companies").doc(vote.companyId).collection("tierVotes").doc(vote.id));
  }
  for (const stored of snapshot.roles) {
    const slug = atsSlug(stored.data.role_url || "");
    const expected = OWNER_BY_SLUG.get(slug);
    if (slug && !expected) {
      throw new Error(`cannot repair role with unowned ATS board: ${stored.id} (${slug})`);
    }
    const companyId = expected?.id || stored.data.global_company_id;
    const companyName = expected?.name || stored.data.company_name;
    const canonicalUrl = canonicalRoleUrl(stored.data.role_url);
    const identity = roleIdentity(stored.data.role_url, stored.data.posting_id);
    const roleKey = identity ||
      `generic:${companyId}:${canonicalUrl}:${String(stored.data.title || "").trim().toLowerCase()}`;
    const roleId = stableId("role", roleKey);
    batch.set(
      db.collection("roles").doc(roleId),
      {
        ...stored.data,
        global_company_id: companyId,
        company_name: companyName,
        canonical_role_url: canonicalUrl,
        role_identity: identity,
        updated_at: now,
      },
      {merge: true},
    );
    if (roleId !== stored.id) batch.delete(db.collection("roles").doc(stored.id));
  }
  await batch.commit();
}

function jsonReplacer(_key, value) {
  return value && typeof value.toDate === "function" ? value.toDate().toISOString() : value;
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
