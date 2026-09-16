"""Persistence for FinXum assessments.

Uses SQLAlchemy Core so the same code path works against either:

- a local SQLite file (`db_path` is a plain filesystem path, e.g.
  "finxum.db") — the historical behaviour, still used by default and by
  the test suite; or
- a persistent database (`db_path` is a full SQLAlchemy URL, e.g.
  "postgresql+psycopg://user:pass@host/db") — required for any deployment
  whose local filesystem is not durable across restarts/redeploys (this
  includes Streamlit Community Cloud). See app/config.py (DATABASE_URL).

Callers keep passing a `db_path` string exactly as before; only its
contents (path vs. URL) determine which backend is used.
"""

import json
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from sqlalchemy import Column, Float, Integer, MetaData, String, Table, Text, create_engine, insert, select
from sqlalchemy.engine import Engine

_metadata = MetaData()

risk_assessments = Table(
    "risk_assessments",
    _metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("issue_date", String, nullable=False),
    Column("due_date", String, nullable=False),
    Column("prior_late_payments", Integer, nullable=False),
    Column("score", Integer, nullable=False),
    Column("risk_category", String, nullable=False),
    Column("drivers", Text, nullable=False),
    Column("rules_version", String, nullable=False),
    Column("created_at", String, nullable=False),
)


def _resolve_url(db_path: str) -> str:
    if "://" in db_path:
        return db_path
    # Resolve to an absolute path (relative to cwd at call time, same as the
    # historical sqlite3.connect(db_path) behaviour) before it becomes an
    # engine-cache key below — otherwise two different relative "finxum.db"
    # paths resolved from different working directories (e.g. isolated
    # per-test tmp dirs) would collide on the same cache key and share one
    # cached engine/connection pointing at only the first one's real file.
    resolved_path = Path(db_path).resolve()
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{resolved_path}"


@lru_cache(maxsize=64)
def _get_engine(url: str) -> Engine:
    return create_engine(url, future=True)


def initialize(db_path: str = "finxum.db") -> None:
    engine = _get_engine(_resolve_url(db_path))
    _metadata.create_all(engine)


def save_assessment(data: dict, db_path: str = "finxum.db") -> int:
    engine = _get_engine(_resolve_url(db_path))
    created_at = datetime.now(timezone.utc).isoformat()
    with engine.begin() as conn:
        result = conn.execute(
            insert(risk_assessments).values(
                reference=data["reference"],
                amount=data["amount"],
                issue_date=data["issue_date"],
                due_date=data["due_date"],
                prior_late_payments=data["prior_late_payments"],
                score=data["score"],
                risk_category=data["risk_category"],
                drivers=json.dumps(data["drivers"]),
                rules_version=data["rules_version"],
                created_at=created_at,
            )
        )
        return int(result.inserted_primary_key[0])


def list_assessments(db_path: str = "finxum.db") -> list[dict]:
    engine = _get_engine(_resolve_url(db_path))
    with engine.connect() as conn:
        rows = conn.execute(
            select(risk_assessments).order_by(risk_assessments.c.id.desc())
        ).mappings().all()
    return [dict(row) for row in rows]
