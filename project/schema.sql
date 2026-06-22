-- Drop tables if they exist to allow clean rebuilds during development
DROP TABLE IF EXISTS implemented_controls;
DROP TABLE IF EXISTS vulnerabilities;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS users;

-- 1. Users Table (Standard Authentication Structure)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

-- 2. Infrastructure/Application Assets Table
CREATE TABLE assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    asset_type TEXT NOT NULL, -- e.g., 'Database', 'Web Server', 'Cloud Storage'
    criticality TEXT CHECK(criticality IN ('Low', 'Medium', 'High', 'Critical')) DEFAULT 'Medium',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Vulnerabilities & Threat Management Table
CREATE TABLE vulnerabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    title TEXT NOT NULL,             -- e.g., 'SQL Injection vulnerability'
    cve_id TEXT DEFAULT 'N/A',       -- e.g., 'CVE-2026-1234'
    description TEXT NOT NULL,
    severity TEXT CHECK(severity IN ('Low', 'Medium', 'High', 'Critical')) DEFAULT 'Medium',
    risk_score REAL NOT NULL,        -- Numeric representation (e.g., 1.0 to 10.0)
    ai_analysis_summary TEXT,        -- General context returned by the LLM
    status TEXT CHECK(status IN ('Open', 'Mitigated', 'Risk Accepted')) DEFAULT 'Open',
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(asset_id) REFERENCES assets(id) ON DELETE CASCADE
);

-- 4. AI-Suggested Framework Controls Alignment Checklist Table
CREATE TABLE implemented_controls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vulnerability_id INTEGER NOT NULL,
    framework_standard TEXT NOT NULL, -- e.g., 'NIST SP 800-53' or 'ISO 27001'
    control_id TEXT NOT NULL,         -- e.g., 'AC-2', 'A.12.6.1'
    control_name TEXT NOT NULL,       -- e.g., 'Account Management'
    remediation_steps TEXT NOT NULL,  -- AI's actionable step-by-step description
    is_implemented INTEGER CHECK(is_implemented IN (0, 1)) DEFAULT 0, -- Boolean state
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(vulnerability_id) REFERENCES vulnerabilities(id) ON DELETE CASCADE
);

-- Optimization Performance Indices for Dashboards
CREATE INDEX idx_assets_user ON assets(user_id);
CREATE INDEX idx_vulnerabilities_asset ON vulnerabilities(asset_id);
CREATE INDEX idx_controls_vulnerability ON implemented_controls(vulnerability_id);
