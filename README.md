# callumployed

Local-first Python CLI for job-search automation.

The app will track target companies, scan career pages, manage roles and application
lifecycles, prepare tailored application materials, and update application statuses
from mailbox signals.

## Planned stack

- Python 3.12+
- SQLite/Turso-compatible local database
- Typer CLI
- Playwright browser scanning
- pytest
- Strands agents for AI-heavy tasks
- MCP server exposing the CLI command surface

## Bootstrap

With standard Python tooling:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m playwright install chromium
python -m pytest
```

With `uv`:

```bash
uv sync --extra dev
uv run playwright install chromium
uv run pytest
```

## First milestone

Keep the MVP small:

- Add/list companies
- Scan saved/static career pages through deterministic extraction
- Store discovered roles and lifecycle events
- List roles
- Manually set status
- Basic repository and CLI tests
