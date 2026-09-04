Callumployed is a local-first job-search tracker and automation tool for managing companies, roles, scans, and application materials. It ships as a Python CLI, local web app, and MCP server so both humans and agents can work against the same SQLite-backed job-search data.

Most impactful features:

- Track companies, career pages, roles, statuses, notes, and application lifecycle counts from one local database.
- Scan company career pages and individual role links with Playwright-backed extraction, job-posting assessment, and configurable filters.
- Manage active/deactivated companies, company tiers, career links, explicit role additions, and lifecycle transitions from the web UI.
- Store a master resume, cover letter examples, render resources, and experience notes for role-specific prep.
- Generate resume feedback, tailored resumes, cover letters, and PDFs from saved materials and job postings.
- Sync shared company metadata on page load and publish privacy-safe scan metrics to the Firebase-backed Central store.
- Expose the same data and workflows through a Typer CLI and FastMCP tools for agent access.

Install: `curl -fsSL https://raw.githubusercontent.com/CallumMackenzie/callumployed/master/scripts/install.sh | bash`

Update an installed client with:

```bash
callumployed update
```

Start: `callumployed serve`

The web UI is served directly from the vanilla HTML, CSS, and JavaScript files in
`src/callumployed/web/static/`. It has no frontend build step or framework runtime.

## Details

### Stack

- Python 3.12+
- SQLite local database with concurrent frontend and CLI access
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

### Install Dependencies

The installer clones callumployed into `~/.local/share/callumployed/source`,
creates a Python 3.12 environment with `uv`, installs the CLI, installs Playwright's
Chromium browser, and creates a `~/.local/bin/callumployed` launcher.
The installed client uses the deployed central company-ID store by default; add the
central passkey later from web settings or with `callumployed central configure --prompt-passkey`
to enable the private role feed.

It prompts for:

- `OPENAI_API_KEY` - required for agent-backed classification and resume feedback.
- `BROWSERBASE_API_KEY` - optional. Leave blank to use local Playwright rendering.

On updates, the installer reuses `OPENAI_API_KEY` and `BROWSERBASE_API_KEY` from
the shell environment first, then from the existing `.env`, and only prompts for
missing values. It merges known settings into `.env` without deleting unrelated
local config.

Resume PDF rendering requires an external LaTeX compiler. The installer checks for
`tectonic`, `latexmk`, or `pdflatex`. On macOS with Homebrew, it can install the
recommended `tectonic` compiler for you; otherwise install one of those compilers
before rerunning the installer.

Advanced install options:

```bash
curl -fsSL https://raw.githubusercontent.com/CallumMackenzie/callumployed/master/scripts/install.sh | \
  CALLUMPLOYED_REPO_URL=https://github.com/your-fork/callumployed.git \
  CALLUMPLOYED_INSTALL_ROOT="$HOME/.local/share/callumployed" \
  CALLUMPLOYED_BIN_DIR="$HOME/.local/bin" \
  bash
```

### Manual install

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
- central: configure/status, resolve company IDs, pull roles, sync
- config: show and update scan filters
- scans: scan a URL, scan a company, list scan runs, show a scan run

## Central Store

Callumployed can optionally sync with a central Firebase-backed company and role store. Local
company and role IDs remain authoritative for each instance; central IDs are stored as
linking metadata so imported roles do not overwrite local status, notes, or application
history.

The default central API is the deployed Callumployed store:
`https://us-central1-callumployed-central.cloudfunctions.net/centralApi`.

Without a passkey, company resolution still works and stores only the returned central
company ID:

```bash
callumployed central resolve-companies
```

The web tracker runs company reconciliation and pulling during initial page load. If
Central is unavailable, startup continues with local company data. The manual company
sync control in settings can be used to retry and inspect the result.

Configure a passkey when you want to pull the private central role feed:

```bash
callumployed central configure --prompt-passkey
```

```bash
callumployed central sync
```

The TypeScript Firebase Functions app lives in `firebase/`. It owns Firestore access,
passkey auth, company matching, and the shared role feed. Python talks to it only over
the HTTP API. Set `CALLUMPLOYED_CENTRAL_API_URL` or run
`callumployed central configure --api-url ...` only when overriding the default store.

Every completed company scan also submits idempotent performance telemetry to the
public `POST /v1/scan-metrics` endpoint. These records are stored in Firestore's
`scan_metrics` collection and do not require the Central passkey. Metrics include a
pseudonymous client ID, company identity, scan timing/status, page and candidate
counts, confidence distributions, selection and discovery-method breakdowns,
role-verification outcomes, extraction methods, rejection categories, failed visits,
agent usage, and app version. They do not include role URLs, role text, raw errors,
filters, notes, application state, or application materials.
Central submission failures are logged but never fail the local scan.

The Central role models and pull/bulk-upsert endpoints are present, but automatic role
sharing after scans is not enabled yet.

### Optional LLM classifier

The scan flow uses LangGraph behind the CLI. Deterministic scoring handles obvious links;
LLM classification is always enabled for ambiguous link candidates.

Configure the provider through shell environment variables or a local `.env` file:

```bash
CALLUMPLOYED_LLM_PROVIDER=openai
CALLUMPLOYED_LLM_MODEL=gpt-5.6-terra
OPENAI_API_KEY=...
```

### Application generation

Résumé, cover-letter, and saved Prepped-role question generation use the built-in
OpenAI path only. The scan/classification provider setting remains separate and does
not change application generation. Hermes and OpenClaw are not application-generation
runtimes and are not required or invoked by Callumployed.

Applicant claims are grounded in saved/indexed application materials. Application
generation does not submit applications or change role status.

Examples:

```bash
callumployed stats
callumployed serve
callumployed startup enable
callumployed startup disable
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

On macOS, `callumployed startup enable` installs and starts a per-user LaunchAgent so
the tracker runs after login. Use `--host` and `--port` to override its bind address,
and run `callumployed startup disable` to unload and remove it. Other operating systems
currently report that startup management is unsupported without changing system state.

### Web tracker

The tracker groups roles by lifecycle status and exposes valid next actions on each
role card. Discovered roles can be marked interested, disinterested, or closed;
interested roles can move into application prep and applied states; and disinterested
roles can be restored to interested. Local status, notes, and application history are
never replaced by Central data.

The manage-companies view supports company creation/deactivation, tier and note
autosaving, and career-link management. A scanned company that has never yielded a
selected potential-role link displays `Discovered 0 potential roles`; never-scanned
companies are not given that label.

### Application materials

Application materials are stored in the local database alongside the tracker data.
The master resume is a single replaceable `.tex` document. Cover letter examples are
an append-only collection, so users can upload as many prior examples as they want for
future tailoring.
Uploading a replacement master resume through the web tracker also replaces the saved
`resume.tex` for every role currently in `interested`. Tailored resumes belonging to
roles in applied or later states are preserved.
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

Dedicated scanners bypass fragile rendered-page extraction where a supported job board
provides better structured data. Current adapters include ByteDance, Greenhouse, Ashby,
and Kula. Ashby detection can probe a company-derived public board slug when the source
careers page is blocked by Cloudflare or another anti-bot page.

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
page results, role-discovery attempts, and active scan-filter context. Successful and
failed scans then submit their aggregate metrics to Central through a failure-isolated
three-second client timeout.
