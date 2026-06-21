PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    notes TEXT,
    prestige_tier TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_companies_name ON companies (name);

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
