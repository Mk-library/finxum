# FinXum

**Financial risk analysis prototype built with Python.**

> Educational/demo prototype. Not financial advice and not a real credit decision system.

## Current status — v0.1

FinXum v0.1 implements an interpretable, deterministic invoice-risk baseline with input validation, SQLite persistence, a Streamlit interface, automated tests, and GitHub Actions CI.

The deployed Streamlit application has also been manually smoke-tested for normal assessment, invalid input handling, high-risk assessment, history retrieval, and methodology navigation.

## Live demo

https://finxum.streamlit.app

## MVP flow

`Input → Validation → Risk Rules → Explanation → SQLite → History`

## Scope — implemented in v0.1

- Dynamic invoice/business assessment inputs
- Transparent deterministic risk scoring
- Versioned rules and traceable results
- SQLite persistence
- 25 clearly labelled synthetic demo scenarios, scored via `calculate_risk()`
- One-click "Load 25 Synthetic Demo Assessments" loader with duplicate prevention
- Analytics page with Plotly charts (category breakdown, score distribution, amount vs. score)
- Streamlit interface
- FastAPI boundary for programmatic risk scoring (`POST /risk/assess`), persisting results to the same SQLite history table
- Authenticated n8n webhook integration (`POST /webhooks/n8n/risk-event`) so an n8n workflow can submit invoice data for scoring; secured with bearer-token authentication (fails closed if unconfigured) and a strict, schema-validated payload
- Automated tests and GitHub Actions CI
- Methodology and development documentation

## Planned — not implemented in v0.1

- Feature-extraction layer with explicit boundaries
- Outbound automation that proactively notifies n8n (or another system) when a stored assessment qualifies as high-risk — the current n8n integration is inbound-only (n8n submits data to FinXum)
- More advanced invoice intelligence capabilities
- Optional LLM explanation layer that does not determine the risk score

## Architecture

The canonical application lives under `app/` and is packaged/tested from that layout.

### Current v0.1

`Streamlit UI → Python application/risk logic → SQLite`
`FastAPI (/risk/assess, /webhooks/n8n/risk-event) → Python application/risk logic → SQLite`

The risk logic currently performs validation, derives the required inputs/features, applies versioned deterministic rules, and returns explanatory drivers. The Streamlit UI and the FastAPI boundary call the same `calculate_risk()` and persist to the same `risk_assessments` table, so a demo assessment, an API call, and an n8n webhook submission all show up in the same history.

### Planned v0.2+

The architecture may separate validation, feature extraction, risk scoring, persistence, and external automation when those boundaries provide real engineering value.

## Repository structure

- `app/risk.py` — deterministic scoring, validation, and explanatory drivers
- `app/database.py` — SQLite persistence and history queries
- `app/main.py` — Streamlit UI, including the Analytics page
- `app/analytics.py` — pure aggregation helpers for the Analytics page
- `app/synthetic_data.py` — the 25 labelled synthetic demo scenarios
- `app/demo_loader.py` — duplicate-safe loader that scores and persists the synthetic scenarios
- `app/config.py` — application and rules configuration
- `app/api.py` — FastAPI boundary (`/health`, `POST /risk/assess`); mounts the n8n webhook router
- `app/webhooks.py` — authenticated n8n webhook endpoint (`POST /webhooks/n8n/risk-event`)
- `app/risk_service.py` — shared scoring + persistence path used by both `app/api.py` and `app/webhooks.py`
- `tests/test_risk.py` — risk-engine unit tests
- `tests/test_database.py` — persistence round-trip test
- `tests/test_synthetic_data.py` — synthetic scenario shape and scoring cross-checks
- `tests/test_demo_loader.py` — demo loader and duplicate-prevention tests
- `tests/test_analytics.py` — analytics aggregation helper tests
- `tests/test_streamlit_app.py` — Streamlit startup and Analytics/demo-loader tests
- `tests/test_api.py` — FastAPI risk-scoring endpoint tests, including history persistence
- `tests/test_webhooks.py` — n8n webhook authentication and payload-validation tests
- `docs/architecture.md` — current and planned architecture
- `docs/methodology.md` — scoring methodology, synthetic scenario design, and duplicate-prevention design
- `docs/project-log.md` — implementation and verification record
- `docs/verification.md` — v0.1 automated and manual verification record

## Integrity rules

- No fabricated customers, transactions, revenue, accuracy, partnerships, or production claims.
- Synthetic data is labelled as synthetic.
- Every displayed result must come from code/data.
- An LLM, if added later, may explain deterministic results but will not decide the risk score.
- Secrets must never be committed.
- Planned work is never described as completed work.

## Verification & deployment

- GitHub Actions CI runs the test suite on Python 3.11 for pushes and pull requests to `main`.
- The Streamlit app has an automated startup test covering the UI entry module.
- The deployment runtime pins Streamlit to `1.62.0`.
- The live Streamlit application has been manually smoke-tested after deployment.
- Vercel is not used as the primary host because FinXum is a Python/Streamlit application.
- The FastAPI service (`app/api.py`) is run locally via `uvicorn app.api:app`; it is not yet part of the deployed Streamlit Cloud app.
- The n8n webhook (`app/webhooks.py`) requires a `FINXUM_N8N_WEBHOOK_SECRET` environment variable wherever the API runs. The endpoint refuses all requests if this is unset — it never falls back to an unauthenticated mode.

See `docs/methodology.md` for the full scoring, synthetic-data, and duplicate-prevention design, and `docs/project-log.md` / `docs/verification.md` for the development and verification records.
