"""Synthetic demo scenarios for FinXum.

Twenty-five clearly labelled synthetic invoice-risk scenarios. They exist to
give the Analytics page representative demo data and to exercise the risk
engine across its full Low/Medium/High output range.

Design note: the 25 scenarios are drawn from a systematic 3x3x3 grid over the
same three factors `calculate_risk()` scores on (payment term, invoice
amount, prior late payments), with two redundant combinations dropped to
reach exactly 25. See docs/methodology.md for the full design rationale.

Scores are never hardcoded here. `expected_category` records the outcome the
scenario is designed to demonstrate for documentation and test purposes, but
every score actually shown or stored by the application is computed by
`app.risk.calculate_risk()` at load time, from these inputs.

This is synthetic/demo data only. It does not represent real customers,
invoices, or payment behaviour.
"""

from dataclasses import dataclass
from datetime import date, timedelta

_BASE_DATE = date(2026, 1, 5)

# Term/amount/late-payment bands, chosen to sit clearly inside the bands
# `calculate_risk()` checks (see docs/methodology.md for the full table).
_SHORT_TERM_DAYS = 15
_MEDIUM_TERM_DAYS = 45
_LONG_TERM_DAYS = 90

_SMALL_AMOUNT = 5_000.0
_MODERATE_AMOUNT = 50_000.0
_HIGH_AMOUNT = 150_000.0

_NO_LATE_PAYMENTS = 0
_SOME_LATE_PAYMENTS = 2
_REPEATED_LATE_PAYMENTS = 4


@dataclass(frozen=True)
class SyntheticScenario:
    reference: str
    label: str
    amount: float
    issue_date: date
    term_days: int
    prior_late_payments: int
    expected_category: str

    @property
    def due_date(self) -> date:
        return self.issue_date + timedelta(days=self.term_days)


def _scenario(
    index: int,
    label: str,
    amount: float,
    term_days: int,
    prior_late_payments: int,
    expected_category: str,
) -> SyntheticScenario:
    return SyntheticScenario(
        reference=f"SYNTH-{index:03d}",
        label=label,
        amount=amount,
        issue_date=_BASE_DATE + timedelta(days=index * 3),
        term_days=term_days,
        prior_late_payments=prior_late_payments,
        expected_category=expected_category,
    )


SYNTHETIC_SCENARIOS: list[SyntheticScenario] = [
    _scenario(1, "Clean small invoice, short term, no late history", _SMALL_AMOUNT, _SHORT_TERM_DAYS, _NO_LATE_PAYMENTS, "Low"),
    _scenario(2, "Small invoice, short term, minor late-payment history", _SMALL_AMOUNT, _SHORT_TERM_DAYS, _SOME_LATE_PAYMENTS, "Low"),
    _scenario(3, "Small invoice, short term, repeated late payments", _SMALL_AMOUNT, _SHORT_TERM_DAYS, _REPEATED_LATE_PAYMENTS, "Medium"),
    _scenario(4, "Moderate invoice, short term, clean history", _MODERATE_AMOUNT, _SHORT_TERM_DAYS, _NO_LATE_PAYMENTS, "Low"),
    _scenario(5, "Moderate invoice, short term, some late payments", _MODERATE_AMOUNT, _SHORT_TERM_DAYS, _SOME_LATE_PAYMENTS, "Medium"),
    _scenario(6, "Moderate invoice, short term, repeated late payments", _MODERATE_AMOUNT, _SHORT_TERM_DAYS, _REPEATED_LATE_PAYMENTS, "Medium"),
    _scenario(7, "High-value invoice, short term, clean history", _HIGH_AMOUNT, _SHORT_TERM_DAYS, _NO_LATE_PAYMENTS, "Medium"),
    _scenario(8, "High-value invoice, short term, some late payments", _HIGH_AMOUNT, _SHORT_TERM_DAYS, _SOME_LATE_PAYMENTS, "Medium"),
    _scenario(9, "High-value invoice, short term, repeated late payments", _HIGH_AMOUNT, _SHORT_TERM_DAYS, _REPEATED_LATE_PAYMENTS, "High"),
    _scenario(10, "Small invoice, extended term, clean history", _SMALL_AMOUNT, _MEDIUM_TERM_DAYS, _NO_LATE_PAYMENTS, "Low"),
    _scenario(11, "Small invoice, extended term, some late payments", _SMALL_AMOUNT, _MEDIUM_TERM_DAYS, _SOME_LATE_PAYMENTS, "Medium"),
    _scenario(12, "Moderate invoice, extended term, clean history", _MODERATE_AMOUNT, _MEDIUM_TERM_DAYS, _NO_LATE_PAYMENTS, "Medium"),
    _scenario(13, "Moderate invoice, extended term, some late payments", _MODERATE_AMOUNT, _MEDIUM_TERM_DAYS, _SOME_LATE_PAYMENTS, "Medium"),
    _scenario(14, "Moderate invoice, extended term, repeated late payments", _MODERATE_AMOUNT, _MEDIUM_TERM_DAYS, _REPEATED_LATE_PAYMENTS, "High"),
    _scenario(15, "High-value invoice, extended term, clean history", _HIGH_AMOUNT, _MEDIUM_TERM_DAYS, _NO_LATE_PAYMENTS, "Medium"),
    _scenario(16, "High-value invoice, extended term, some late payments", _HIGH_AMOUNT, _MEDIUM_TERM_DAYS, _SOME_LATE_PAYMENTS, "High"),
    _scenario(17, "High-value invoice, extended term, repeated late payments", _HIGH_AMOUNT, _MEDIUM_TERM_DAYS, _REPEATED_LATE_PAYMENTS, "High"),
    _scenario(18, "Small invoice, long term, clean history", _SMALL_AMOUNT, _LONG_TERM_DAYS, _NO_LATE_PAYMENTS, "Medium"),
    _scenario(19, "Small invoice, long term, repeated late payments", _SMALL_AMOUNT, _LONG_TERM_DAYS, _REPEATED_LATE_PAYMENTS, "High"),
    _scenario(20, "Moderate invoice, long term, clean history", _MODERATE_AMOUNT, _LONG_TERM_DAYS, _NO_LATE_PAYMENTS, "Medium"),
    _scenario(21, "Moderate invoice, long term, some late payments", _MODERATE_AMOUNT, _LONG_TERM_DAYS, _SOME_LATE_PAYMENTS, "High"),
    _scenario(22, "Moderate invoice, long term, repeated late payments", _MODERATE_AMOUNT, _LONG_TERM_DAYS, _REPEATED_LATE_PAYMENTS, "High"),
    _scenario(23, "High-value invoice, long term, clean history", _HIGH_AMOUNT, _LONG_TERM_DAYS, _NO_LATE_PAYMENTS, "High"),
    _scenario(24, "High-value invoice, long term, some late payments", _HIGH_AMOUNT, _LONG_TERM_DAYS, _SOME_LATE_PAYMENTS, "High"),
    _scenario(25, "High-value invoice, long term, repeated late payments", _HIGH_AMOUNT, _LONG_TERM_DAYS, _REPEATED_LATE_PAYMENTS, "High"),
]
