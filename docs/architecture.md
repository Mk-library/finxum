# Architecture

## MVP architecture

FinXum follows a simple, explainable pipeline:

`Streamlit UI → application/risk services → SQLite`

The application will later expose an API boundary where it adds value and integrate with n8n through a webhook for risk events.

## Planned components

- **UI:** Streamlit for a fast, reliable portfolio MVP.
- **Application logic:** Python services with clear boundaries between validation, feature calculation, risk scoring and persistence.
- **Data processing:** pandas and NumPy where justified.
- **Database:** SQLite for local MVP persistence without external infrastructure.
- **Risk engine:** deterministic, versioned, interpretable rules/weighted scoring.
- **Automation:** n8n webhook triggered by qualifying risk events.
- **Testing:** pytest.

## Integrity

Risk decisions must be reproducible from stored inputs/features and the applicable rules/model version. An optional LLM explanation layer, if implemented, will receive deterministic outputs and will not silently replace the risk engine.

## Status

Architecture is documented before implementation. Components will be marked complete only after they are implemented and tested.
