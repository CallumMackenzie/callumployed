# AGENTS.md

This is a local-first Python CLI for job-search automation.

## Project Constraints

- Keep the MVP small and boring.
- Prefer deterministic parsing and schemas before AI interpretation.
- Agents consume normalized inputs and return validated structured outputs.
- Never overwrite generated emails, files, artifacts, or status changes without history.
- Treat mailbox data as sensitive.
- Keep CLI, services, repositories, browser scanning, mailbox ingestion, LLM agents,
  MCP, config, and tests in separate boundaries.
- Browser and mailbox tests should use fixtures by default.
- Do not touch real mailboxes, external services, or public systems without explicit approval.

## Planned Boundaries

- `cli`: Typer command surface
- `services`: application use cases
- `repositories`: database access
- `browser`: career-page rendering and extraction
- `mailbox`: mailbox ingestion and classification inputs
- `agents`: LangChain structured-output adapters
- `mcp`: MCP server and tools
- `config`: settings and secret lookup
