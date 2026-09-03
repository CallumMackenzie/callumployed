const assert = require("node:assert/strict");
const test = require("node:test");

const {companyTier} = require("../lib/companies.js");

test("companyTier accepts every supported tier from 0 through 7", () => {
  for (let tier = 0; tier <= 7; tier += 1) {
    assert.equal(companyTier(String(tier)), String(tier));
  }
});

test("companyTier accepts an unset tier", () => {
  assert.equal(companyTier(null), null);
  assert.equal(companyTier(undefined), null);
  assert.equal(companyTier(""), null);
});

test("companyTier rejects values outside the API contract", () => {
  assert.throws(() => companyTier("8"), /0 to 7/);
  assert.throws(() => companyTier("-1"), /0 to 7/);
  assert.throws(() => companyTier("A"), /0 to 7/);
  assert.throws(() => companyTier(7), /string from 0 to 7/);
});
