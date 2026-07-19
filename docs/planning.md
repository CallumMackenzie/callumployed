# Planning Notes

## Architecture Summary

The app should stay layered:

- CLI handles user input/output only.
- Services implement application use cases.
- Repositories own persistence for companies, roles, scan artifacts, and application
  materials.
- Browser scanning returns normalized deterministic scan results.
- Mailbox ingestion returns normalized message signals.
- LangGraph services orchestrate workflows; LangChain adapters emit validated structured outputs.
- MCP tools call the same services as the CLI.
- Config/secrets remain isolated from business logic.

## Current State

The project now has the core local tracker surfaces in place:

- Typer CLI commands for companies, roles, config, scanning, stats, and the local web UI.
- Repository tests and migration tests against temporary databases.
- A FastMCP server that calls the same service/repository layer as the CLI, including
  application-material tools.
- A static local web tracker served by `callumployed serve`.
- A compact application-materials UI for replacing the master `.tex` resume and adding
  multiple cover letter examples.
- CLI commands under `callumployed materials` for showing materials, setting the master
  resume, and adding one or more cover letter examples.
- Local database stores for the single master resume and many cover letter examples.
- LangGraph scan workflow orchestration for career pages and selected role pages.
- Deterministic role-page assessment with structured `JobPosting`, ATS/page-text
  heuristics, title ranking, and closed-role detection.
- Existing-role refresh through `callumployed roles rescan <role_id>`.

## Browser Strategy

Browser rendering should stay pluggable and conservative:

- `local` remains the default backend.
- `browserbase` is a try-first backend when configured with `BROWSERBASE_API_KEY`.
- Browserbase failures, missing keys, blocked HTTP statuses, and blocked page bodies
  should fall back locally instead of failing the scan.
- Scan workflows that have a `BrowserProfileManager` should be able to fall back from
  Browserbase/local Playwright to cloned Brave profiles for sites that require warmer
  browser state.
- Never upload a personal Brave profile to Browserbase; clone it locally only.

## Role Rescan

Role rescan is the update path for jobs already stored in the database:

- load an existing role by id
- revisit its stored `role_url`
- run role-page assessment with the current title as a hint
- refresh extracted fields when the page still looks like a role
- optionally mark a role closed with `--update-status`
- record a `role_rescanned` event

Known follow-up: Tesla location and posting-id extraction are still noisy. Title
recovery works, but metadata cleanup needs another pass.

## Application Materials

Application materials are local-first database records, not files copied into the repo:

- `master_resumes` stores one current master resume and requires a `.tex` filename.
- `cover_letter_examples` stores any number of prior examples and orders them newest
  first.
- CLI, MCP, and web UI surfaces should use the same repository helpers so validation
  and timestamps stay consistent.
- The web UI should remain compact because these controls share the tracker header
  area with search, filtering, and review actions.

Likely next step: wrap `tectonic` or `latexmk` behind a renderer service so stored
resume and cover letter content can produce exact PDFs without making the UI own
LaTeX execution details.

## Test Expectations

Before expanding behavior, keep coverage around:

- repository field updates and events
- CLI output for new commands
- material store validation across repository, CLI, MCP, and web endpoints
- browser backend fallback behavior
- role-page title ranking and blocked-page detection
- workflow routing between Browserbase, local Playwright, and managed Brave profiles
