# FinXum

**Financial risk analysis and invoice intelligence prototype built with Python.**

> Educational/demo prototype. Not financial advice and not a real credit decision system.

## Current status

FinXum is being developed as a reproducible portfolio prototype for data-driven invoice risk assessment. The MVP starts with an interpretable, deterministic risk baseline rather than a black-box ML model.

## Planned MVP flow

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

## Integrity rules

- No fabricated customers, transactions, revenue, accuracy, partnerships, or production claims.
- Synthetic data is labelled as synthetic.
- Every displayed result must come from code/data.
- An LLM, if added later, may explain deterministic results but will not decide the risk score.
- Secrets must never be committed.

## Development

This repository is currently at the initial scaffold stage. Features will be added and tested incrementally.

See `docs/project-log.md` for the development record.
