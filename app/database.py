"""Small SQLite database for demo support tickets."""
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", "/app/data/tickets.db"))


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH, timeout=10)


def init_db():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_ticket(issue: str) -> int:
    with connect() as db:
        cursor = db.execute(
            "INSERT INTO tickets (issue) VALUES (?)", (issue,)
        )
        return int(cursor.lastrowid)


def list_tickets():
    with connect() as db:
        db.row_factory = sqlite3.Row
        rows = db.execute(
            "SELECT id, issue, status, created_at "
            "FROM tickets ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]
