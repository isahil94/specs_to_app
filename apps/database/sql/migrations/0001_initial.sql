-- Non-destructive starter migration: create migration history table
CREATE TABLE IF NOT EXISTS migration_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  migration_id TEXT NOT NULL UNIQUE,
  applied_at TEXT DEFAULT (datetime('now')),
  description TEXT
);
