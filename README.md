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
- LangGraph scan workflow orchestration
- pytest
- LangChain provider adapters for optional LLM classification
- MCP server exposing the CLI command surface

## Install dependencies

With standard Python tooling:

```bash
cd ~/Downloads/callumployed
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,agents]"
python -m playwright install chromium
```

With `uv`:

```bash
cd ~/Downloads/callumployed
uv sync --extra dev --extra agents
uv run playwright install chromium
```

If `python3.12` is not available, check your installed version:

```bash
python3 --version
```

Use `python3` instead if it is Python 3.12 or newer.

## Run the CLI

After installing dependencies:

```bash
source .venv/bin/activate
callumployed --help
```

Or run it without relying on the installed console script:

```bash
PYTHONPATH=src python -m callumployed.cli --help
```

### Optional LLM classifier

The scan flow uses LangGraph behind the CLI. Deterministic scoring handles obvious links;
LLM classification is always enabled for ambiguous link candidates.

Configure the provider through shell environment variables or a local `.env` file:

```bash
CALLUMPLOYED_LLM_PROVIDER=openai
CALLUMPLOYED_LLM_MODEL=gpt-4.1-mini
OPENAI_API_KEY=...
```

Examples:

```bash
callumployed scan url https://example.com/careers
callumployed scan company 1
callumployed scan all
```

The first graph handles career-page scan orchestration only. It does not use
LangGraph checkpointing yet.

## Test

After installing the `dev` dependencies:

```bash
source .venv/bin/activate
python -m pytest
```

Quick import check without installing dependencies:

```bash
PYTHONPATH=src python3 -c "import callumployed; print(callumployed.__version__)"
```

## First milestone

Keep the MVP small:

- Add/list companies
- Scan saved/static career pages through deterministic extraction
- Store discovered roles and lifecycle events
- List roles
- Manually set status
- Basic repository and CLI tests
