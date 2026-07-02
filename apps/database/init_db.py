"""Initialize and validate the application SQLite database.

Usage:
    python apps/database/init_db.py --validate    # Run schema validation in-memory
    python apps/database/init_db.py --init        # Create persistent DB at apps/database/app.db and seed
"""
import argparse
import os
import sqlite3
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "apps" / "database" / "sql" / "schema.sql"
DB_DIR = ROOT / "apps" / "database"
DB_PATH = DB_DIR / "app.db"


def run_sql_script(conn: sqlite3.Connection, sql: str):
    conn.executescript(sql)


def validate_schema():
    """Load schema into an in-memory SQLite DB to validate SQL"""
    sql = SCHEMA_PATH.read_text()
    conn = sqlite3.connect(":memory:")
    try:
        run_sql_script(conn, sql)
    finally:
        conn.close()
    print("VALIDATION: OK - schema executed in-memory")


def init_db(seed: bool = True, recreate: bool = False):
    """Create persistent DB file and seed sample data.

    If `recreate` is True, remove any existing DB before creating.
    """
    DB_DIR.mkdir(parents=True, exist_ok=True)
    if recreate and DB_PATH.exists():
        DB_PATH.unlink()
    sql = SCHEMA_PATH.read_text()
    conn = sqlite3.connect(str(DB_PATH))
    try:
        # Ensure foreign key enforcement is enabled on this connection
        conn.execute("PRAGMA foreign_keys = ON;")
        run_sql_script(conn, sql)
        if seed:
            cur = conn.cursor()
            # Insert sample user and team and a task
            user_id = str(uuid.uuid4())
            cur.execute(
                """
                INSERT OR IGNORE INTO users (id, email, display_name, password_hash, created_at)
                VALUES (?, ?, ?, ?, datetime('now'))
                """,
                (user_id, "alice@example.com", "Alice", "<hashed>")
            )
            team_id = str(uuid.uuid4())
            cur.execute(
                """
                INSERT OR IGNORE INTO teams (id, name, lead_id, created_at)
                VALUES (?, ?, ?, datetime('now'))
                """,
                (team_id, "Core Team", user_id)
            )
            cur.execute(
                """
                INSERT OR IGNORE INTO team_members (team_id, user_id, role, joined_at)
                VALUES (?, ?, ?, datetime('now'))
                """,
                (team_id, user_id, "user")
            )
            task_id = str(uuid.uuid4())
            cur.execute(
                """
                INSERT OR IGNORE INTO tasks (id, title, description, status, priority, created_by_id, team_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """,
                (task_id, "Welcome Task", "Initial seeded task", "todo", "medium", user_id, team_id),
            )
            conn.commit()
    finally:
        conn.close()
    print(f"INIT: Created DB at {DB_PATH}")


def verify_db():
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        print("TABLES:")
        for t in tables:
            print(" -", t)
        # Show sample counts
        cur.execute("SELECT COUNT(*) FROM users")
        users = cur.fetchone()[0]
        print(f"USERS: {users}")
        cur.execute("SELECT COUNT(*) FROM tasks")
        tasks = cur.fetchone()[0]
        print(f"TASKS: {tasks}")
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true", help="Run in-memory schema validation")
    parser.add_argument("--init", action="store_true", help="Initialize persistent DB and seed data")
    parser.add_argument("--recreate", action="store_true", help="Recreate persistent DB (delete then init) and seed data")
    args = parser.parse_args()

    if args.validate:
        validate_schema()
        return

    if args.init or args.recreate:
        init_db(seed=True, recreate=bool(args.recreate))
        verify_db()
        return

    parser.print_help()


if __name__ == "__main__":
    main()
