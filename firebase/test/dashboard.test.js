const assert = require("node:assert/strict");
const test = require("node:test");

const {compareCompanyRows, dashboardPage} = require("../lib/dashboard.js");
const {isAgentAssistedScan} = require("../lib/dashboardMetrics.js");

test("agent-assisted scans include every supported agent signal", () => {
  assert.equal(isAgentAssistedScan({agent_trace_present: true}), true);
  assert.equal(isAgentAssistedScan({candidate_discovery_method_counts: {agent: 1}}), true);
  assert.equal(
    isAgentAssistedScan({candidate_discovery_method_counts: {"heuristic+agent": 2}}),
    true,
  );
  assert.equal(isAgentAssistedScan({extraction_method_counts: {llm: 1}}), true);
  assert.equal(
    isAgentAssistedScan({
      agent_trace_present: false,
      candidate_discovery_method_counts: {heuristic: 4},
      extraction_method_counts: {deterministic: 3},
    }),
    false,
  );
});

test("company rows sort names and numbers in both directions", () => {
  const rows = [
    {company_name: "Zulu", scans: 2},
    {company_name: "alpha", scans: 10},
    {company_name: "Beta", scans: 4},
  ];
  assert.deepEqual(
    [...rows].sort((a, b) => compareCompanyRows(a, b, "company_name", "asc"))
      .map((row) => row.company_name),
    ["alpha", "Beta", "Zulu"],
  );
  assert.deepEqual(
    [...rows].sort((a, b) => compareCompanyRows(a, b, "company_name", "desc"))
      .map((row) => row.company_name),
    ["Zulu", "Beta", "alpha"],
  );
  assert.deepEqual(
    [...rows].sort((a, b) => compareCompanyRows(a, b, "scans", "asc"))
      .map((row) => row.scans),
    [2, 4, 10],
  );
  assert.deepEqual(
    [...rows].sort((a, b) => compareCompanyRows(a, b, "scans", "desc"))
      .map((row) => row.scans),
    [10, 4, 2],
  );
});

test("company table uses one shared sort state and clears inactive headers", () => {
  const page = dashboardPage();
  assert.match(page, /const companySort = \{key:'scans', direction:'desc'\}/);
  assert.match(page, /header\.setAttribute\('aria-sort',active\?/);
  assert.match(page, /companySort\.key=key/);
  assert.equal((page.match(/data-company-sort="/g) ?? []).length, 8);
  assert.equal((page.match(/aria-sort="descending"/g) ?? []).length, 1);
  const script = page.match(/<script>([\s\S]*?)<\/script>/)?.[1];
  assert.ok(script);
  assert.doesNotThrow(() => new Function(script));
});
