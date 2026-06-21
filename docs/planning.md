# Planning Notes

## Architecture Summary

The app should stay layered:

- CLI handles user input/output only.
- Services implement application use cases.
- Repositories own persistence.
- Browser scanning returns normalized deterministic scan results.
- Mailbox ingestion returns normalized message signals.
- Strands agents consume normalized records and emit validated structured outputs.
- MCP tools call the same services as the CLI.
- Config/secrets remain isolated from business logic.

## First Milestone

Smallest useful MVP:

- `addcompany`
- `listcompanies`
- `scan`
- `listroles`
- `setstatus`
- `events`

Schema subset:

- companies
- roles
- role_snapshots
- applications
- lifecycle_events
- scan_runs

Test requirements before expanding:

- unit tests for service transitions
- repository tests against temporary SQLite
- CLI tests for first commands
- browser extraction tests from saved HTML fixtures
