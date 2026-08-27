# AGENTS.md

This is a local-first Python 3.12 CLI, MCP server, and web tracker for job-search
automation. SQLite is authoritative for user-owned state. The optional Firebase-backed
Central service shares company/role metadata and receives privacy-safe scan metrics.

## Project Constraints

- Keep the MVP small and boring.
- Prefer deterministic parsing and schemas before AI interpretation.
- Agents consume normalized inputs and return validated structured outputs.
- Never overwrite generated emails, files, artifacts, or status changes without history.
- Treat mailbox data as sensitive.
- Keep CLI, services, repositories, browser scanning, mailbox ingestion, LLM agents,
  MCP, web UI, config, application-material storage, and tests in separate boundaries.
- Route master resume and cover letter example behavior through repository helpers so
  CLI, MCP, and web surfaces stay consistent.
- Browser and mailbox tests should use fixtures by default.
- Keep optional remote failures isolated from local workflows. Central company sync and
  scan-metric publication must not prevent startup or fail a completed local scan.
- Do not touch real mailboxes or unrelated external/public systems without explicit
  approval. Product-defined Central calls are allowed only through the Central client.

## Current Boundaries

- `src/callumployed/cli.py`: Typer command surface
- `src/callumployed/mcp_server.py`: FastMCP server and tools
- `src/callumployed/web/`: local tracker UI, static assets, and JSON endpoints
- `src/callumployed/services/`: application workflows, including scanning and
  ATS-specific adapters
- `src/callumployed/data/`: models, migrations, and repository/database access
- `src/callumployed/webscraping/`: browser rendering and generic extraction
- `src/callumployed/agents/`: optional LangChain structured-output adapters
- `src/callumployed/central/`: Python Central contracts, reconciliation, client, and
  scan-metric construction
- `firebase/src/`: TypeScript Firebase Functions API for shared companies, roles, and
  scan metrics; edit source files, not generated `firebase/lib/` output
- `tests/`: unit and fixture-backed workflow tests

## Behavioral Invariants

- Local company and role IDs remain authoritative. Central IDs are linking metadata;
  remote data must not overwrite local role status, notes, or application history.
- Company reconciliation/pulling runs during initial web-page load and degrades cleanly
  to local data when Central is unavailable.
- `POST /v1/scan-metrics` is intentionally public and unauthenticated. Keep payloads
  aggregate and pseudonymous: never send role URLs, raw errors, scan filters, notes,
  application state, or application materials.
- Automatic role sharing after scans is not enabled yet. Do not conflate the existing
  role pull/bulk-upsert API with active upload behavior.
- Scanner-specific structured sources should be preferred over fragile rendered-page
  parsing when available. Existing adapters cover ByteDance, Greenhouse, Ashby, and
  Kula; preserve generic browser extraction as the fallback.
- A company may show `Discovered 0 potential roles` only after at least one scan and no
  selected potential-role link across its scans. Never-scanned companies must not show it.
- Replacing the web master resume updates each currently `interested` role's
  `resume.tex`. Preserve tailored resumes for roles in applied or later states.
- Role status changes must use the validated lifecycle and retain history. In particular,
  a `disinterested` role can be restored to `interested`.

## Verification

- Run `ruff check .` for linting and `mypy src` for type checking.
- Run `pytest` for the Python suite. Browser and integration tests are marker-separated;
  do not turn a fixture-backed test into a real network dependency.
- For Firebase changes, run `npm run build` from `firebase/` and include the generated
  `firebase/lib/` changes when the repository already tracks them.
- Keep changes scoped and preserve unrelated work in a dirty tree.
