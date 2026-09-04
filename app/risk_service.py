"""Shared scoring + persistence path used by both the direct risk API and
the n8n webhook (app/api.py and app/webhooks.py). Kept separate from both so
neither module has to import the other.
"""

from datetime import date

from pydantic import BaseModel

from .database import save_assessment
from .risk import calculate_risk


class RiskAssessmentResult(BaseModel):
    id: int
    reference: str
    score: int
    category: str
    drivers: list[str]
    rules_version: str


def score_and_persist(
    reference: str | None,
    amount: float,
    issue_date: date,
    due_date: date,
    prior_late_payments: int,
    db_path: str,
) -> RiskAssessmentResult:
    """Score an invoice and persist it into the risk_assessments history table.

    Raises ValueError (propagated from calculate_risk()) for invalid input;
    callers are expected to translate that into an HTTP error response.
    """
    result = calculate_risk(amount, issue_date, due_date, prior_late_payments)

    resolved_reference = (reference or "").strip() or "UNSPECIFIED"
    assessment_id = save_assessment(
        {
            "reference": resolved_reference,
            "amount": amount,
            "issue_date": issue_date.isoformat(),
            "due_date": due_date.isoformat(),
            "prior_late_payments": prior_late_payments,
            "score": result.score,
            "risk_category": result.category,
            "drivers": result.drivers,
            "rules_version": result.rules_version,
        },
        db_path,
    )

    return RiskAssessmentResult(
        id=assessment_id,
        reference=resolved_reference,
        score=result.score,
        category=result.category,
        drivers=result.drivers,
        rules_version=result.rules_version,
    )
