const assert = require("node:assert/strict");
const test = require("node:test");

const {
  atsSlug,
  canonicalDomain,
  canonicalRoleUrl,
  roleIdentity,
} = require("../lib/normalization.js");
const {scoreCompany} = require("../lib/scoring.js");

test("shared ATS company identity includes the board slug", () => {
  assert.equal(atsSlug("https://jobs.ashbyhq.com/cohere"), "ashby:cohere");
  assert.equal(atsSlug("https://jobs.ashbyhq.com/rivianvw.tech/"), "ashby:rivianvw.tech");
  assert.equal(
    atsSlug("https://job-boards.greenhouse.io/aquaticcapitalmanagement"),
    "greenhouse:aquaticcapitalmanagement",
  );
  assert.equal(
    atsSlug("https://boards.greenhouse.io/radixuniversity/jobs/123"),
    "greenhouse:radixuniversity",
  );
});

test("shared ATS hosts are not company domains", () => {
  assert.equal(canonicalDomain("https://jobs.ashbyhq.com/cohere"), null);
  assert.equal(canonicalDomain("https://job-boards.greenhouse.io/aquatic"), null);
  assert.equal(canonicalDomain("https://example.com/careers"), "example.com");
});

test("role canonicalization retains posting identifiers and sorts query parameters", () => {
  const first = canonicalRoleUrl(
    "https://example.com/job/?z=2&utm_source=test&gh_jid=123&a=1#details",
  );
  const second = canonicalRoleUrl("https://example.com/job?a=1&gh_jid=123&z=2");
  assert.equal(first, second);
  assert.match(first, /gh_jid=123/);
  assert.doesNotMatch(first, /utm_source/);
});

test("specific ATS postings have global identities while board roots remain generic", () => {
  assert.equal(
    roleIdentity("https://job-boards.greenhouse.io/cohere/jobs/456?utm_source=x"),
    "greenhouse:cohere:job:456",
  );
  assert.equal(
    roleIdentity("https://jobs.ashbyhq.com/cohere/ABC-123"),
    "ashby:cohere:job:abc-123",
  );
  assert.equal(roleIdentity("https://jobs.ashbyhq.com/cohere"), null);
});

test("a shared hostname alone cannot match another ATS board owner", () => {
  const score = scoreCompany(
    {
      id: "co_ramp",
      display_name: "Ramp",
      domains: ["jobs.ashbyhq.com"],
      ats_slugs: ["ashby:ramp"],
    },
    {
      name: "Cohere",
      career_page_urls: ["https://jobs.ashbyhq.com/cohere"],
      role_urls: [],
    },
  );
  assert.equal(score.confidence, 0);
  assert.deepEqual(score.matched_on, []);
});
