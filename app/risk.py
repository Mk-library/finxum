"""Deterministic, explainable baseline risk engine."""

from dataclasses import dataclass
from datetime import date

from .config import RULES_VERSION


@dataclass(frozen=True)
class RiskResult:
    score: int
    category: str
    drivers: list[str]
    rules_version: str = RULES_VERSION


def calculate_risk(
    amount: float,
    issue_date: date,
    due_date: date,
    prior_late_payments: int,
) -> RiskResult:
    """Calculate a simple versioned demo score from supplied invoice inputs.

    This is a portfolio baseline, not a credit model and has no claimed
    predictive accuracy.
    """
    if amount <= 0:
        raise ValueError("Invoice amount must be greater than zero.")
    if due_date < issue_date:
        raise ValueError("Due date cannot be before issue date.")
    if prior_late_payments < 0:
        raise ValueError("Prior late payments cannot be negative.")

    score = 10
    drivers: list[str] = []

    term_days = (due_date - issue_date).days
    if term_days > 60:
        score += 25
        drivers.append("Long payment term (>60 days)")
    elif term_days > 30:
        score += 10
        drivers.append("Extended payment term (>30 days)")

    if amount >= 100_000:
        score += 25
        drivers.append("High invoice amount (≥100,000)")
    elif amount >= 25_000:
        score += 10
        drivers.append("Moderate invoice amount (≥25,000)")

    if prior_late_payments >= 3:
        score += 30
        drivers.append("Repeated prior late payments (≥3)")
    elif prior_late_payments >= 1:
        score += 15
        drivers.append("Prior late payment history")

    score = min(score, 100)
    if score >= 60:
        category = "High"
    elif score >= 30:
        category = "Medium"
    else:
        category = "Low"

    if not drivers:
        drivers.append("No elevated demo risk factors triggered")

    return RiskResult(score=score, category=category, drivers=drivers)
