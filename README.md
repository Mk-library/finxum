# FinXum

**Financial risk analysis and invoice intelligence prototype built with Python.**

> Educational/demo prototype. Not financial advice and not a real credit decision system.

## Current status

FinXum contains the first implemented application slice: an interpretable, deterministic invoice-risk baseline, SQLite persistence, a Streamlit interface, and a pytest test suite. The repository CI pipeline currently passes on the main branch.

## MVP flow

`Input → Validation → Features → Versioned Risk Rules → Explanation → SQLite → History → n8n`

## Scope

- Dynamic invoice/business assessment inputs
- Transparent financial features and deterministic risk scoring
- Versioned rules and traceable results
- SQLite persistence
- Synthetic/demo data, clearly labelled
- Streamlit interface for the MVP
- Tests and documentation
- n8n webhook automation after the core application is stable

## Architecture

The canonical application lives under `app/` and is packaged/tested from that layout. The first implementation consists of:

- `app/risk.py` — deterministic scoring and explanatory drivers
- `app/database.py` — SQLite persistence and history queries
- `app/main.py` — Streamlit UI
- `app/config.py` — application/rules configuration
- `tests/test_risk.py` — baseline unit tests
- `tests/test_database.py` — persistence round-trip test
- `tests/test_streamlit_app.py` — Streamlit startup test

## Integrity rules

- No fabricated customers, transactions, revenue, accuracy, partnerships, or production claims.
- Synthetic data is labelled as synthetic.
- Every displayed result must come from code/data.
- An LLM, if added later, may explain deterministic results but will not decide the risk score.
- Secrets must never be committed.
- Planned work is never described as completed work.

## Verification & deployment

- The repository test suite passes in GitHub Actions on Python 3.11.
- The Streamlit app has an automated startup test covering the UI entry module.
- `requirements.txt` pins the Streamlit runtime version used by the deployment target.
- Vercel is not being used as the primary Streamlit host because FinXum is a Python/Streamlit application.
- Live Streamlit Cloud behavior still requires external runtime confirmation; repository CI cannot prove that the deployed Cloud instance is serving the latest commit.

See `docs/project-log.md` for the development record.
