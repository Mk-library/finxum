"""Deterministic, interpretable invoice-risk scoring primitives."""

from dataclasses import dataclass


@dataclass(frozen=True)
class InvoiceInput:
    """Minimal invoice/business inputs for the first deterministic baseline."""

    invoice_amount: float
    days_overdue: int
    customer_history_score: float


def validate_input(data: InvoiceInput) -> None:
    """Validate baseline inputs before scoring."""
    if data.invoice_amount <= 0:
        raise ValueError("invoice_amount must be greater than 0")
    if data.days_overdue < 0:
        raise ValueError("days_overdue cannot be negative")
    if not 0 <= data.customer_history_score <= 100:
        raise ValueError("customer_history_score must be between 0 and 100")


def risk_score(data: InvoiceInput) -> float:
    """Return a transparent 0-100 risk score using fixed rules.

    Higher values indicate higher modeled risk. This is a prototype baseline,
    not a financial or credit decision.
    """
    validate_input(data)
    overdue_component = min(data.days_overdue * 2.0, 60.0)
    history_component = (100.0 - data.customer_history_score) * 0.4
    return round(min(overdue_component + history_component, 100.0), 2)


def risk_band(score: float) -> str:
    """Map a score to a deterministic explanatory band."""
    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")
    if score < 30:
        return "low"
    if score < 60:
        return "medium"
    return "high"
