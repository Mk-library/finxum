"""Application configuration."""

import os

APP_VERSION = "0.1.0"
RULES_VERSION = "rules-v0.1"

# A plain filesystem path (e.g. "finxum.db") stores to a local SQLite file —
# fine for dev/tests, but not durable on hosts with an ephemeral filesystem
# (e.g. Streamlit Community Cloud resets local disk on redeploy/restart).
# Setting DATABASE_URL to a SQLAlchemy URL (e.g.
# "postgresql+psycopg://user:pass@host/db") switches to that database
# instead, with no other code changes required.
DB_PATH = os.environ.get("DATABASE_URL", "finxum.db")

DISCLAIMER = (
    "Educational/demo prototype. Not financial advice and not a real credit decision system."
)
