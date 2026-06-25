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
- BeautifulSoup link extraction
- `extruct` structured-data extraction for `schema.org/JobPosting`
- `trafilatura` main-text extraction for rendered role pages
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

The scan graph handles career-page scan orchestration only. It does not use
LangGraph checkpointing yet. Link discovery is layered:

1. Deterministic link extraction and scoring select obvious job-posting links.
2. Ambiguous link candidates go through the optional LLM posting-link classifier.
3. Selected links are rendered and assessed as role pages.
4. Role-page assessment prefers structured `schema.org/JobPosting` data, then ATS
   and HTML/text heuristics.

### Role-page assessment

Selected discovered links are rendered and passed through `assess_role_page()`.
The assessment returns:

- whether the page is a role
- whether the role looks closed
- confidence
- title
- location
- description
- posting id
- extraction method
- rejection reason
- evidence reasons

Current persistence stores the rendered role attempt with final URL, assessed title,
description excerpt, status, and error. The full assessment payload is not yet stored.

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

## Full workflow breakdown

The current scan workflow starts from a career page and ends with persisted scan
artifacts plus role-discovery attempts for selected links.

### 1. Render the career page

`render_page_node` calls Playwright through `render_careers_page()` and produces a
`RenderedPageState` with the requested URL, final URL, title, HTML, and visible text.

### 2. Extract link candidates

`extract_candidates_node` calls `extract_link_candidates()`.

Extraction parses the rendered HTML with BeautifulSoup and emits `LinkCandidate`
objects from anchors and button-like link elements. Each candidate can include:

- normalized URL
- source URL
- link text
- tag
- element id/classes
- aria label
- title attribute
- surrounding text

### 3. Prepare and score candidates

`score_candidates_node` dedupes candidates by URL with `prepare_candidates()`, keeping
the candidate with the richest extraction metadata.

Then `score_candidates()` produces `ScoredLinkCandidate` objects. Scoring uses:

- known ATS/job-board domains
- job-like URL paths
- numeric job IDs
- job-like text
- generic careers navigation penalties
- rejected/nav text penalties
- closed-role signals
- existing posting URLs already in the database

### 4. Select obvious links

`select_heuristic_links()` turns high-confidence scored candidates into
`DiscoveredJobLink` objects. The current threshold is `0.35`.

### 5. Classify ambiguous links

If any candidate has `0.0 < confidence < 0.35`, `should_classify()` routes the graph
to `classify_ambiguous_node`.

That node builds the LangChain/LangGraph posting-link classifier and asks it to decide
which ambiguous URLs are specific job postings. The LLM only sees the ambiguous
candidates, not the already-obvious ones.

### 6. Merge discovered links

`build_result_node` merges heuristic and agent links with `merge_discovered_links()`.
If both paths select the same URL, confidence is maxed, reasons are combined, and the
method becomes `heuristic+agent`.

The node returns a `CareersPageScanResult` containing:

- source/final URL
- page title
- all scored candidates
- selected discovered links
- candidate count
- overall extraction confidence
- errors

### 7. Persist scan page and candidates

For company scans with a scan run, `persist_scan_node` saves:

- one `scan_pages` row for the rendered career page
- one `scan_candidates` row for every scored candidate

Each saved candidate is marked `selected = true` if its URL appears in the discovered
links. The saved candidate also receives the discovery method when selected.

Ad hoc `scan url` runs return the in-memory result and skip persistence because they
do not have a scan run id.

### 8. Visit selected links

`visit_discovered_links_node` only visits persisted selected candidates. For each one:

1. Render the selected candidate URL.
2. Run `assess_role_page()` on the rendered page.
3. Save a `role_discovery_attempts` row.

If rendering or assessment fails, the attempt is saved with `failed` status and the
error text.

### 9. Assess the role page

`assess_role_page()` uses layered deterministic evidence:

1. `extruct` extracts JSON-LD, Microdata, and RDFa. A valid `JobPosting` is accepted as
   high-confidence role evidence.
2. Known ATS/job-board URL and page-text signals identify likely role pages without
   structured data.
3. Generic careers/search/listing signals reject pages that are not specific roles.
4. `trafilatura` extracts clean main text for descriptions and downstream use.
5. Closed-role phrases set `is_closed`.

The assessment currently improves the saved attempt title and text excerpt. It does
not yet create or update a `roles` row automatically.

### 10. Finish company scan

`scan_company()` scans each saved career page for the company. After all pages finish,
it marks the `scan_runs` row as succeeded and returns the scan run, career pages,
page results, role-discovery attempts, and browser-port context.
