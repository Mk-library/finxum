"""SQLite persistence for FinXum assessments."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def connect(db_path: str = "finxum.db") -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize(db_path: str = "finxum.db") -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS risk_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference TEXT NOT NULL,
                amount REAL NOT NULL,
                issue_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                prior_late_payments INTEGER NOT NULL,
                score INTEGER NOT NULL,
                risk_category TEXT NOT NULL,
                drivers TEXT NOT NULL,
                rules_version TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_assessment(data: dict, db_path: str = "finxum.db") -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    with connect(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO risk_assessments
            (reference, amount, issue_date, due_date, prior_late_payments,
             score, risk_category, drivers, rules_version, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["reference"], data["amount"], data["issue_date"],
                data["due_date"], data["prior_late_payments"], data["score"],
                data["risk_category"], json.dumps(data["drivers"]),
                data["rules_version"], created_at,
            ),
        )
        return int(cursor.lastrowid)


def list_assessments(db_path: str = "finxum.db") -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM risk_assessments ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]
