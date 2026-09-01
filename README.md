# FinXum

**Financial risk analysis and invoice intelligence prototype built with Python.**

> Educational/demo prototype. Not financial advice and not a real credit decision system.

## Current status

FinXum contains the first implemented application slice: an interpretable, deterministic invoice-risk baseline, SQLite persistence, a Streamlit interface, and a pytest test suite. Runtime execution still needs to be verified in an environment with the project dependencies installed.

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

## Integrity rules

- No fabricated customers, transactions, revenue, accuracy, partnerships, or production claims.
- Synthetic data is labelled as synthetic.
- Every displayed result must come from code/data.
- An LLM, if added later, may explain deterministic results but will not decide the risk score.
- Secrets must never be committed.
- Planned work is never described as completed work.

## Verification & deployment

- Repository-level code and documentation have been reviewed.
- The test suite exists, but a successful runtime test run has **not** been claimed until it is actually executed.
- Vercel is not being used as the primary Streamlit host because FinXum is a Python/Streamlit application. Deployment should target a Streamlit-compatible host after runtime verification.

See `docs/project-log.md` for the development record.
