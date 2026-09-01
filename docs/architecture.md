# Architecture

## Current — v0.1

FinXum follows a deliberately small, explainable pipeline:

`Streamlit UI → Python application/risk logic → SQLite`

The current risk logic validates the supplied inputs, derives the values needed by the rules, applies the versioned deterministic scoring rules, and returns explanatory drivers. Results and the applicable rules version are stored with the assessment.

### Components implemented

- **UI:** Streamlit.
- **Application logic:** Python risk calculation and validation.
- **Database:** SQLite for MVP assessment persistence and history.
- **Risk engine:** deterministic, versioned, interpretable rules/weighted scoring.
- **Testing:** pytest and Streamlit AppTest.
- **CI:** GitHub Actions on Python 3.11.

## Planned — v0.2+

Future boundaries will be introduced only when they provide real engineering value:

- **Feature extraction:** an explicit layer for derived invoice/business features.
- **API boundary:** programmatic access to the risk engine if needed.
- **Automation:** n8n webhook integration for qualifying risk events.
- **Invoice intelligence:** document/extraction capabilities only when implemented and tested.
- **Optional explanation layer:** an LLM may explain deterministic outputs, but it will not silently replace or determine the risk engine.

## Integrity

Risk decisions must be reproducible from stored inputs/features and the applicable rules/model version. Synthetic/demo data must remain clearly labelled. Planned components are not described as implemented until they are implemented and tested.

## Status

The v0.1 architecture is implemented and verified through automated tests plus manual smoke testing of the deployed Streamlit application. Planned components remain explicitly separated from the current implementation.
