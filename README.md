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
- Automated tests and GitHub Actions CI
- Methodology and development documentation

## Planned — not implemented in v0.1

- Feature-extraction layer with explicit boundaries
- API boundary for programmatic access
- n8n webhook automation for qualifying risk events
- More advanced invoice intelligence capabilities
- Optional LLM explanation layer that does not determine the risk score

## Architecture

The canonical application lives under `app/` and is packaged/tested from that layout.

### Current v0.1

`Streamlit UI → Python application/risk logic → SQLite`

The risk logic currently performs validation, derives the required inputs/features, applies versioned deterministic rules, and returns explanatory drivers.

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
- `tests/test_risk.py` — risk-engine unit tests
- `tests/test_database.py` — persistence round-trip test
- `tests/test_synthetic_data.py` — synthetic scenario shape and scoring cross-checks
- `tests/test_demo_loader.py` — demo loader and duplicate-prevention tests
- `tests/test_analytics.py` — analytics aggregation helper tests
- `tests/test_streamlit_app.py` — Streamlit startup and Analytics/demo-loader tests
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

See `docs/methodology.md` for the full scoring, synthetic-data, and duplicate-prevention design, and `docs/project-log.md` / `docs/verification.md` for the development and verification records.
