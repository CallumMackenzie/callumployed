# callumployed

Local-first Python CLI, MCP server, and web tracker for job-search automation.

The app tracks target companies, scans career pages, manages roles and application
lifecycles, stores reusable application materials, and gives agents structured access
to the same local data.

## Stack

- Python 3.12+
- SQLite/Turso-compatible local database
- Typer CLI
- FastMCP server for agent/tool access
- Playwright browser scanning
- Browserbase remote browser sessions with local fallback
- LangGraph scan workflow orchestration
- BeautifulSoup link extraction
- `extruct` structured-data extraction for `schema.org/JobPosting`
- `trafilatura` main-text extraction for rendered role pages
- pytest
- LangChain provider adapters for optional LLM classification

## Install dependencies

With standard Python tooling:

```bash
cd ~/Downloads/callumployed
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,agents,mcp]"
python -m playwright install chromium
```

With `uv`:

```bash
cd ~/Downloads/callumployed
uv sync --extra dev --extra agents --extra mcp
uv run playwright install chromium
```

If `python3.12` is not available, check your installed version:

```bash
python3 --version
```

Use `python3` instead if it is Python 3.12 or newer.

### External render dependencies

The web prep view can generate per-role resume PDFs from uploaded LaTeX. PDF
rendering requires one local TeX engine because Python dependencies do not bundle a
complete LaTeX renderer.

Recommended on macOS:

```bash
brew install tectonic
```

Callumployed checks for these compilers in order:

1. `tectonic`
2. `latexmk`
3. `pdflatex`

`tectonic` is the smallest recommended install path. `latexmk` or `pdflatex` also
work if they are already available from a TeX distribution such as MacTeX.

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

## Run the MCP server

Install the `mcp` optional dependency, then run the stdio MCP server:

```bash
source .venv/bin/activate
callumployed-mcp
```

The MCP server is implemented explicitly in `src/callumployed/mcp_server.py` with
`FastMCP`. It calls the same repository and service functions as the Typer CLI and
returns structured data instead of parsed CLI text.

Available MCP tools cover:

- companies: add, update career pages, list, show
- roles: add, list, show, update, set status
- materials: get/set the master resume, list/add cover letter examples
- stats: application and job counts by lifecycle status
- config: show and update scan filters
- scans: scan a URL, scan a company, list scan runs, show a scan run

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
callumployed stats
callumployed serve
callumployed materials show
callumployed materials set-master-resume path/to/master.tex
callumployed materials add-cover-letter-example path/to/example1.tex path/to/example2.md
callumployed scan url https://example.com/careers
callumployed scan company 1
callumployed scan all
callumployed roles rescan 49
```

`callumployed serve` starts a local web tracker at `http://127.0.0.1:8765`
with overall stats, status panes, search, compact application-material controls,
and collapsible job lists.

### Application materials

Application materials are stored in the local database alongside the tracker data.
The master resume is a single replaceable `.tex` document. Cover letter examples are
an append-only collection, so users can upload as many prior examples as they want for
future tailoring.
Resume render resources such as images, class files, and bibliography files are stored
locally next to the app data and copied into each per-role resume folder before PDF
generation.

CLI commands:

```bash
callumployed materials set-master-resume path/to/master.tex
callumployed materials add-cover-letter-example path/to/example1.tex path/to/example2.md
callumployed materials show
```

The web tracker exposes the same store through a compact application-materials bar:
one control replaces the master resume, one uploads shared render resources, and
another adds cover letter examples while showing recent uploaded filenames without
expanding the whole tracker view.

MCP tools expose the same data for agents:

- `get_master_resume`
- `set_master_resume`
- `list_cover_letter_examples`
- `add_cover_letter_example`

### Browser backend

Browser rendering defaults to local Playwright. To try Browserbase first, configure:

```bash
CALLUMPLOYED_BROWSER_BACKEND=browserbase
BROWSERBASE_API_KEY=...
```

When Browserbase is selected, rendering is opportunistic. If the API key is missing,
the Browserbase SDK is unavailable, the cloud session fails, or the rendered page is a
blocked body such as `Access Denied`, scanning falls back locally. Scan workflows that
receive a `BrowserProfileManager` can then fall back again to the managed Brave profile
pool, which is useful for sites that block clean cloud/local browser sessions.

Useful browser commands:

```bash
callumployed browser config
callumployed browser smoke https://example.com
callumployed browser profiles
```

`browser config` reports whether Browserbase is configured without printing the secret.

### Role rescans

Existing roles can be revisited without rediscovering them from a company career page:

```bash
callumployed roles rescan 49
callumployed roles rescan 49 --update-status
```

Rescans revisit the stored role URL, re-run role-page assessment, refresh extracted
fields such as title, location, description, posting ID, and `last_seen_at`, and record
a `role_rescanned` event. By default, status is preserved; `--update-status` marks a
role closed when the refreshed page looks closed or unavailable.

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
description excerpt, assessment fields, status, and error. For persisted company scans,
high-confidence role assessments create or reuse a `roles` row and link the discovery
attempt to that role.

## Test

After installing the `dev` dependencies:

```bash
source .venv/bin/activate
python -m pytest
ruff check .
mypy src tests
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
- Store a master resume and reusable cover letter examples
- List roles
- Manually set status
- Basic repository and CLI tests

## Full workflow breakdown

The current scan workflow starts from a career page and ends with persisted scan
artifacts plus role-discovery attempts for selected links.

### 1. Render the career page

`render_page_node` calls `render_careers_page()` and produces a `RenderedPageState`
with the requested URL, final URL, title, HTML, and visible text. Depending on config,
the renderer can use local Playwright or Browserbase. Browserbase failures fall back to
local rendering, and scan workflows with a managed profile pool can fall back to a
cloned Brave profile.

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
3. Create or reuse a `roles` row for high-confidence role pages.
4. Save a `role_discovery_attempts` row linked to the role when one was created or found.

If rendering or assessment fails, the attempt is saved with `failed` status and the
error text.

### 9. Assess the role page

`assess_role_page()` uses layered deterministic evidence:

1. `extruct` extracts JSON-LD, Microdata, and RDFa. A valid `JobPosting` is accepted as
   high-confidence role evidence.
2. Known ATS/job-board URL and page-text signals identify likely role pages without
   structured data.
3. Generic careers/search/listing signals reject pages that are not specific roles.
4. Title selection ranks structured titles, selected-link hints, DOM titles, browser
   titles, and URL slugs, so noisy titles such as generic careers-page text can be
   replaced with role-specific titles.
5. `trafilatura` extracts clean main text for descriptions and downstream use.
6. Closed-role phrases set `is_closed`.

The assessment improves the saved attempt title and text excerpt. For persisted company
scans, accepted role pages create or reuse a `roles` row when confidence is high enough
and a title is available.

### 10. Finish company scan

`scan_company()` scans each saved career page for the company. After all pages finish,
it marks the `scan_runs` row as succeeded and returns the scan run, career pages,
page results, role-discovery attempts, and browser-port context.
