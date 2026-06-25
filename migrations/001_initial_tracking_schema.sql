PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    notes TEXT,
    prestige_tier TEXT,
    external_browser_port INTEGER
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_companies_name ON companies (name);

CREATE TABLE IF NOT EXISTS app_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS company_career_pages (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    label TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_company_career_pages_company_url
    ON company_career_pages (company_id, url);

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    role_url TEXT NOT NULL,
    location TEXT,
    role_status TEXT NOT NULL DEFAULT 'discovered' CHECK (
        role_status IN (
            'discovered',
            'interested',
            'disinterested',
            'prepared',
            'applied',
            'OA',
            'interview',
            'rejected',
            'offer',
            'closed',
            'archived'
        )
    ),
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    notes TEXT,
    description TEXT,
    posting_id TEXT,
    FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_roles_company_url ON roles (company_id, role_url);
CREATE INDEX IF NOT EXISTS idx_roles_company_status ON roles (company_id, role_status);
CREATE INDEX IF NOT EXISTS idx_roles_last_seen_at ON roles (last_seen_at);

CREATE TABLE IF NOT EXISTS scan_runs (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    started_at TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT,
    scan_status TEXT NOT NULL DEFAULT 'running' CHECK (
        scan_status IN ('running', 'succeeded', 'failed')
    ),
    error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    agent_trace TEXT,
    FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_scan_runs_company_started_at
    ON scan_runs (company_id, started_at);
CREATE INDEX IF NOT EXISTS idx_scan_runs_status ON scan_runs (scan_status);

CREATE TABLE IF NOT EXISTS scan_pages (
    id INTEGER PRIMARY KEY,
    scan_run_id INTEGER NOT NULL,
    company_career_page_id INTEGER,
    source_url TEXT NOT NULL,
    final_url TEXT NOT NULL,
    title TEXT,
    candidates_scanned INTEGER NOT NULL DEFAULT 0,
    confidence TEXT NOT NULL DEFAULT 'low' CHECK (confidence IN ('low', 'medium', 'high')),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (scan_run_id) REFERENCES scan_runs (id) ON DELETE CASCADE,
    FOREIGN KEY (company_career_page_id) REFERENCES company_career_pages (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_scan_pages_scan_run_id ON scan_pages (scan_run_id);

CREATE TABLE IF NOT EXISTS scan_candidates (
    id INTEGER PRIMARY KEY,
    scan_page_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    source_url TEXT NOT NULL,
    text TEXT,
    tag TEXT NOT NULL,
    css_id TEXT,
    css_classes_json TEXT NOT NULL DEFAULT '[]',
    aria_label TEXT,
    title TEXT,
    surrounding_text TEXT,
    confidence REAL NOT NULL,
    reasons_json TEXT NOT NULL DEFAULT '[]',
    selected INTEGER NOT NULL DEFAULT 0 CHECK (selected IN (0, 1)),
    discovery_method TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (scan_page_id) REFERENCES scan_pages (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_scan_candidates_scan_page_id
    ON scan_candidates (scan_page_id);
CREATE INDEX IF NOT EXISTS idx_scan_candidates_selected ON scan_candidates (selected);

CREATE TABLE IF NOT EXISTS role_discovery_attempts (
    id INTEGER PRIMARY KEY,
    scan_run_id INTEGER NOT NULL,
    scan_candidate_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    role_id INTEGER,
    url TEXT NOT NULL,
    final_url TEXT,
    title TEXT,
    visible_text_excerpt TEXT,
    assessment_is_role INTEGER CHECK (assessment_is_role IN (0, 1)),
    assessment_is_closed INTEGER CHECK (assessment_is_closed IN (0, 1)),
    assessment_confidence REAL,
    assessment_location TEXT,
    assessment_description TEXT,
    assessment_posting_id TEXT,
    assessment_extraction_method TEXT,
    assessment_rejection_reason TEXT,
    assessment_reasons_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'succeeded' CHECK (status IN ('succeeded', 'failed')),
    error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (scan_run_id) REFERENCES scan_runs (id) ON DELETE CASCADE,
    FOREIGN KEY (scan_candidate_id) REFERENCES scan_candidates (id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_role_discovery_attempts_scan_run_id
    ON role_discovery_attempts (scan_run_id);
CREATE INDEX IF NOT EXISTS idx_role_discovery_attempts_scan_candidate_id
    ON role_discovery_attempts (scan_candidate_id);
CREATE INDEX IF NOT EXISTS idx_role_discovery_attempts_company_id
    ON role_discovery_attempts (company_id);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    role_id INTEGER,
    event_type TEXT NOT NULL,
    old_status TEXT,
    new_status TEXT,
    source TEXT NOT NULL CHECK (source IN ('manual', 'scan')),
    summary TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_events_company_created_at ON events (company_id, created_at);
CREATE INDEX IF NOT EXISTS idx_events_role_created_at ON events (role_id, created_at);
CREATE INDEX IF NOT EXISTS idx_events_source ON events (source);
