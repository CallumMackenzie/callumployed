# Callumployed Central Store

TypeScript Firebase Functions API for the shared Callumployed company/role store.

## API

- `POST /v1/companies/resolve` resolves or creates a global company ID.
- `GET /v1/roles` returns central roles for local import.
- `POST /v1/roles/bulk-upsert` writes roles into the central store.

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

## Secret

The function compares the bearer passkey to a SHA-256 hash stored in Secret Manager:

```bash
printf "%s" "your-passkey" | shasum -a 256
firebase functions:secrets:set CENTRAL_PASSKEY_SHA256
```

Paste only the hash into the secret prompt.

## Local Python Client

Configure a Callumployed instance after deploy:

```bash
callumployed central configure \
  --api-url https://us-central1-<project-id>.cloudfunctions.net/centralApi

callumployed central resolve-companies
```

Add the passkey when you want to pull the private role feed:

```bash
callumployed central configure \
  --api-url https://us-central1-<project-id>.cloudfunctions.net/centralApi \
  --prompt-passkey

callumployed central sync
```

When configured, the passkey is stored in the OS keyring. `CALLUMPLOYED_CENTRAL_API_URL` and
`CALLUMPLOYED_CENTRAL_PASSKEY` can override saved config for automation.

## Deploy

```bash
npm install
npm run build
firebase deploy --only functions
```
