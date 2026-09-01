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

## AI assistance

AI tools may be used during development for code scaffolding, debugging, documentation and test assistance. Product decisions, validation, testing and final interpretation must remain attributable to the project owner and must reflect the actual implementation.

## Integrity rule

Do not backdate work or claim functionality, results, users, data, partnerships or validation that did not actually occur.
