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
- Repository code has been reviewed through GitHub file inspection.
- Runtime test execution has **not** been verified in this environment because no project execution environment is currently connected.
- Deployment has not been falsely marked complete. FinXum is a Streamlit/Python application, so the primary deployment target should be Streamlit-compatible rather than Vercel.

## AI assistance

AI tools may be used during development for code scaffolding, debugging, documentation and test assistance. Product decisions, validation, testing and final interpretation must remain attributable to the project owner and must reflect the actual implementation.

## Integrity rule

Do not backdate work or claim functionality, results, users, data, partnerships or validation that did not actually occur.
