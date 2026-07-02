-- Schema generated from apps/backend/src/core/models.py
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  avatar_url TEXT,
  time_zone TEXT DEFAULT 'UTC',
  language TEXT DEFAULT 'en',
  is_active INTEGER DEFAULT 1,
  is_verified INTEGER DEFAULT 0,
  theme TEXT DEFAULT 'light',
  created_at TEXT,
  updated_at TEXT,
  last_login TEXT,
  login_attempts INTEGER DEFAULT 0,
  locked_until TEXT
);

CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_is_active ON users(is_active);

CREATE TABLE IF NOT EXISTS teams (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  lead_id TEXT NOT NULL,
  created_at TEXT,
  updated_at TEXT,
  FOREIGN KEY(lead_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_team_lead_id ON teams(lead_id);

CREATE TABLE IF NOT EXISTS team_members (
  team_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  role TEXT,
  joined_at TEXT,
  PRIMARY KEY(team_id, user_id),
  FOREIGN KEY(team_id) REFERENCES teams(id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT,
  priority TEXT,
  created_by_id TEXT NOT NULL,
  assignee_id TEXT,
  team_id TEXT,
  due_date TEXT,
  created_at TEXT,
  updated_at TEXT,
  archived_at TEXT,
  is_archived INTEGER DEFAULT 0,
  labels TEXT,
  FOREIGN KEY(created_by_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY(assignee_id) REFERENCES users(id) ON DELETE SET NULL,
  FOREIGN KEY(team_id) REFERENCES teams(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_task_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_task_created_by ON tasks(created_by_id);
CREATE INDEX IF NOT EXISTS idx_task_assignee ON tasks(assignee_id);
CREATE INDEX IF NOT EXISTS idx_task_team ON tasks(team_id);
CREATE INDEX IF NOT EXISTS idx_task_created_at ON tasks(created_at);

CREATE TABLE IF NOT EXISTS task_history (
  id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL,
  changed_by_id TEXT NOT NULL,
  field_name TEXT NOT NULL,
  old_value TEXT,
  new_value TEXT,
  change_type TEXT NOT NULL,
  created_at TEXT,
  FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE,
  FOREIGN KEY(changed_by_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_task_history_task_id ON task_history(task_id);
CREATE INDEX IF NOT EXISTS idx_task_history_created_at ON task_history(created_at);

CREATE TABLE IF NOT EXISTS comments (
  id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL,
  author_id TEXT NOT NULL,
  content TEXT NOT NULL,
  mentions TEXT,
  attachments TEXT,
  created_at TEXT,
  updated_at TEXT,
  FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE,
  FOREIGN KEY(author_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_comment_task_id ON comments(task_id);
CREATE INDEX IF NOT EXISTS idx_comment_author_id ON comments(author_id);

CREATE TABLE IF NOT EXISTS notifications (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  notification_type TEXT NOT NULL,
  task_id TEXT,
  related_user_id TEXT,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  is_read INTEGER DEFAULT 0,
  created_at TEXT,
  read_at TEXT,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE SET NULL,
  FOREIGN KEY(related_user_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_notification_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notification_created_at ON notifications(created_at);

CREATE TABLE IF NOT EXISTS audit_logs (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  action TEXT NOT NULL,
  resource_type TEXT NOT NULL,
  resource_id TEXT,
  status TEXT NOT NULL,
  details TEXT,
  ip_address TEXT,
  user_agent TEXT,
  created_at TEXT,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_logs(created_at);
