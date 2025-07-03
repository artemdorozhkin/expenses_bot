-- init migrations

CREATE TABLE IF NOT EXISTS schema_migrations (
    filename TEXT PRIMARY KEY,
    applied_at TEXT CURRENT_TIMESTAMP
);
