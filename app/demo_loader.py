"""Loader for the synthetic demo assessment set.

Every score persisted here is produced by `app.risk.calculate_risk()` — this
module never assigns or overrides a score. Loading is duplicate-safe: each
synthetic scenario has a fixed reference, and a scenario already present in
the database (by reference) is skipped rather than re-inserted, so the
"Load 25 Synthetic Demo Assessments" action can be clicked repeatedly without
creating duplicate rows.
"""

from dataclasses import dataclass

from .database import list_assessments, save_assessment
from .risk import calculate_risk
from .synthetic_data import SYNTHETIC_SCENARIOS


@dataclass(frozen=True)
class DemoLoadResult:
    loaded: int
    skipped: int
    loaded_references: list[str]
    skipped_references: list[str]


def load_synthetic_assessments(db_path: str = "finxum.db") -> DemoLoadResult:
    existing_references = {row["reference"] for row in list_assessments(db_path)}

    loaded_references: list[str] = []
    skipped_references: list[str] = []

    for scenario in SYNTHETIC_SCENARIOS:
        if scenario.reference in existing_references:
            skipped_references.append(scenario.reference)
            continue

        result = calculate_risk(
            scenario.amount,
            scenario.issue_date,
            scenario.due_date,
            scenario.prior_late_payments,
        )
        save_assessment(
            {
                "reference": scenario.reference,
                "amount": scenario.amount,
                "issue_date": scenario.issue_date.isoformat(),
                "due_date": scenario.due_date.isoformat(),
                "prior_late_payments": scenario.prior_late_payments,
                "score": result.score,
                "risk_category": result.category,
                "drivers": result.drivers,
                "rules_version": result.rules_version,
            },
            db_path,
        )
        loaded_references.append(scenario.reference)

    return DemoLoadResult(
        loaded=len(loaded_references),
        skipped=len(skipped_references),
        loaded_references=loaded_references,
        skipped_references=skipped_references,
    )
