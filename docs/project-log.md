# Project Log

## 2026-09-02 — Repository initialization and first implementation slice

- Created the public `finxum` repository.
- Added the project README and initial MVP architecture decision.
- Implemented the first application slice under `app/`:
  - deterministic, versioned risk scoring;
  - SQLite persistence and assessment history;
  - Streamlit MVP interface;
  - baseline pytest coverage for core risk behaviour.
- Removed an accidental duplicate implementation under `src/finxum/` so `app/` remains the canonical package layout.
- Repository code was reviewed through GitHub file inspection.
- Runtime test execution had not been verified in the initial development environment at the time of this entry.
- Deployment was not marked complete before external runtime verification.

## 2026-09-02 — v0.1 verification and deployment

- GitHub Actions CI passed on the `main` branch after the risk-boundary test correction.
- The Streamlit application was deployed at `https://finxum.streamlit.app`.
- Manual smoke testing verified:
  - normal assessment creation and scoring;
  - invalid invoice amount handling;
  - invalid due-date handling;
  - high-risk assessment scoring and drivers;
  - assessment history retrieval/persistence;
  - methodology navigation and displayed rules version.
- The v0.1 implementation is considered functionally verified and is now frozen for evidence packaging.
- No claims of real customers, revenue, predictive accuracy, partnerships, production credit decisions, or real-world validation are made.

## 2026-09-02 — Deployment-path cleanup

- Removed the obsolete Vercel `finxum` project because Vercel was attempting to interpret the Streamlit application as a Python serverless function.
- Streamlit Community Cloud remains the sole intended deployment target for the v0.1 application.
- The GitHub repository remains the canonical source of code.
- No application functionality was changed by this cleanup.

## 2026-09-02 — Analytics page, synthetic demo dataset, and demo loader

- Added `app/synthetic_data.py`: 25 clearly labelled synthetic invoice-risk
  scenarios (`SYNTH-001`…`SYNTH-025`) built from a systematic grid over the
  `calculate_risk()` scoring factors. Design rationale documented in
  `docs/methodology.md`.
- Added `app/demo_loader.py`: a duplicate-safe loader that scores each
  scenario through the existing, unmodified `app.risk.calculate_risk()` and
  persists it via the existing `save_assessment()` path. Re-running the
  loader skips any scenario already present by reference.
- Added `app/analytics.py`: pure aggregation helpers (category counts, score
  distribution, amount/score pairs, summary stats) over stored assessments.
- Added an Analytics page to the Streamlit UI (`app/main.py`) with a
  "Load 25 Synthetic Demo Assessments" button and three Plotly charts
  (category breakdown, score distribution, amount vs. score).
- Added `docs/methodology.md` covering the scoring rule table, the synthetic
  scenario design, and the duplicate-prevention approach.
- Added `plotly==5.24.1` as a pinned dependency in `requirements.txt` and
  `pyproject.toml`. No other new dependencies or infrastructure were
  introduced; SQLite remains the only persistence layer.
- `app/risk.py` (the scoring logic) was not modified.
- Added `tests/test_synthetic_data.py`, `tests/test_demo_loader.py`,
  `tests/test_analytics.py`, and extended `tests/test_streamlit_app.py`.
  Full local `pytest` run (`python -m pytest -q`, Python 3.13.5 in a
  project-local virtualenv): **66 passed**, 0 failed.
- This work has been implemented and locally test-verified only. It has not
  been pushed to `origin/main`, deployed, or manually smoke-tested on the
  live Streamlit application at the time of this entry.

## 2026-09-05 — FastAPI boundary, SQLite integration, and n8n webhook

- Added `app/api.py`: a FastAPI boundary exposing `GET /health` and
  `POST /risk/assess`, calling the existing, unmodified
  `app.risk.calculate_risk()`.
- Connected `POST /risk/assess` to the existing SQLite persistence path:
  every scored assessment is saved via `save_assessment()` into the same
  `risk_assessments` table used by the Streamlit UI, so API-submitted
  assessments appear in the same History/Analytics views.
- Added `app/webhooks.py`: a dedicated, schema-strict endpoint,
  `POST /webhooks/n8n/risk-event`, for n8n workflows to submit invoice
  data for scoring. Secured with bearer-token authentication checked via
  `hmac.compare_digest` against a `FINXUM_N8N_WEBHOOK_SECRET` environment
  variable; the endpoint fails closed (503) if that variable is unset
  rather than accepting unauthenticated requests. The payload schema
  forbids unrecognized fields (`extra="forbid"`).
- Added `app/risk_service.py`: the score-then-persist path shared by
  `/risk/assess` and the webhook, avoiding duplicated logic.
- Added `tests/test_api.py` and `tests/test_webhooks.py`. Full local
  `pytest` run (`python -m pytest -q`, Python 3.13.5 in a project-local
  virtualenv): **79 passed**, 0 failed.
- Manually verified the running server (`uvicorn app.api:app`) against
  `FINXUM_N8N_WEBHOOK_SECRET=my-secret-token`:
  - `GET /health` returned the expected status/version payload;
  - a correctly authenticated webhook request was accepted (200) and
    persisted into `finxum.db`, visible via `list_assessments()`;
  - a request with no `Authorization` header was rejected (401);
  - a request with the wrong token was rejected (401);
  - a request sent while `FINXUM_N8N_WEBHOOK_SECRET` was unset was
    rejected (503) rather than falling back to unauthenticated access;
  - a request containing an unrecognized extra field was rejected (422);
  - a request with `due_date` before `issue_date` was rejected (422);
  - a request with a malformed date string was rejected (422);
  - all of the above rejected requests were confirmed to persist nothing
    into `finxum.db`.
- Updated `README.md` to reflect the n8n integration as implemented,
  worded precisely: it is inbound-only (n8n submits data to FinXum), so
  the previously-planned *outbound* "notify on qualifying risk events"
  direction is now listed separately under Planned rather than marked
  done.
- This work has been implemented, automated-test-verified, and manually
  smoke-tested locally only. The FastAPI service is not yet part of the
  deployed Streamlit Cloud app, and this work had not yet been pushed to
  `origin/main` at the time of this entry.

## AI assistance

AI tools may be used during development for code scaffolding, debugging, documentation and test assistance. Product decisions, validation, testing and final interpretation must remain attributable to the project owner and must reflect the actual implementation.

## Integrity rule

Do not backdate work or claim functionality, results, users, data, partnerships or validation that did not actually occur.
