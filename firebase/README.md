# Callumployed Central Store

TypeScript Firebase Functions API for the shared Callumployed company/role store.

## API

- `POST /v1/companies/resolve` resolves or creates a global company ID.
- `GET /v1/roles` returns central roles for local import.
- `POST /v1/roles/bulk-upsert` writes roles into the central store.
- `POST /v1/scan-metrics` writes an idempotent, privacy-safe scan aggregate to the
  `scan_metrics` collection. This endpoint does not require a passkey.
- `GET /dashboard` serves the private Central metrics dashboard. Sign in with the
  existing Central passkey; authentication uses an expiring secure session cookie.
- `GET /v1/dashboard/metrics?days=30` returns dashboard aggregates and requires a
  valid dashboard session.

All routes require:

`POST /v1/companies/resolve` can be called without a passkey. In that mode it returns
only:

```json
{"global_company_id": "co_..."}
```

Include the passkey to receive match confidence and candidate metadata:

```text
X-Callumployed-Passkey: <passkey>
```

`GET /v1/roles` and `POST /v1/roles/bulk-upsert` always require the passkey.

## Metrics dashboard

After deployment, open:

```text
https://us-central1-callumployed-central.cloudfunctions.net/centralApi/dashboard
```

The dashboard aggregates the `scan_metrics` collection into activity, reliability,
conversion, company-performance, app-version, confidence, discovery-method,
verification-outcome, extraction-method, and rejection-reason views. It never returns
raw client IDs. Dashboard sessions expire after 12 hours and are stored in `HttpOnly`,
`Secure`, `SameSite=Strict` cookies signed with the configured passkey hash.

## Secret

The function compares the bearer passkey to a SHA-256 hash stored in Secret Manager:

```bash
printf "%s" "your-passkey" | shasum -a 256
firebase functions:secrets:set CENTRAL_PASSKEY_SHA256
```

Paste only the hash into the secret prompt.

## Local Python Client

The Python client defaults to the deployed central store:
`https://us-central1-callumployed-central.cloudfunctions.net/centralApi`.

```bash
callumployed central resolve-companies
```

Add the passkey when you want to pull the private role feed:

```bash
callumployed central configure --prompt-passkey

callumployed central sync
```

When configured, the passkey is stored in the OS keyring. `CALLUMPLOYED_CENTRAL_API_URL`
can override the default API URL, and `CALLUMPLOYED_CENTRAL_PASSKEY` can override the
saved passkey for automation.

## Deploy

```bash
npm install
npm run build
firebase deploy --only functions
```
