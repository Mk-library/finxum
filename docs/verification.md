# v0.1 Verification Record

## Automated verification

- GitHub Actions CI runs on pushes and pull requests to `main`.
- CI uses Python 3.11 and installs the project with the test extra.
- The pytest suite covers baseline scoring, high-risk scoring, scoring boundaries, invalid amount, invalid dates, negative late payments, SQLite persistence, and Streamlit startup.
- The boundary-test hardening commit was verified successfully by GitHub Actions run #24, including the full `Run tests` step.
- The latest CI run is a documentation-only follow-up and does not change application code or tests.

## Manual deployed smoke tests

The deployed Streamlit application was manually exercised through the following cases:

| Test | Expected behaviour | Observed result |
| --- | --- | --- |
| Normal assessment | Valid assessment is saved and scored | Passed; low-risk result displayed and persisted |
| Zero invoice amount | Invalid input is rejected | Passed; validation error displayed |
| Due date before issue date | Invalid date order is rejected | Passed; validation error displayed and no new assessment saved |
| High-risk assessment | Multiple elevated factors produce a high score with drivers | Passed; high-risk result and three drivers displayed |
| History | Saved assessments can be retrieved | Passed; records displayed in History |
| Methodology | Rules, categories, version and disclaimer are visible | Passed |

## Integrity boundary

These tests verify application behaviour. They do not establish predictive accuracy, creditworthiness, financial performance, real customers, production credit decisions, revenue, partnerships, or real-world model validation.

## v0.1 status

The application functionality is verified. The current changes are verification/documentation hardening only; no new product capability has been added. New product capabilities belong in a separately scoped v0.2 rather than being added opportunistically to the v0.1 verification record.
