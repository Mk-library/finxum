from datetime import date, timedelta

import pytest

from app.risk import calculate_risk

BASE_DATE = date(2026, 9, 1)


def test_low_risk_baseline():
    result = calculate_risk(1000, BASE_DATE, date(2026, 9, 15), 0)
    assert result.score == 10
    assert result.category == "Low"
    assert result.rules_version == "rules-v0.1"


def test_high_risk_factors_are_applied():
    result = calculate_risk(150000, BASE_DATE, date(2026, 11, 15), 3)
    assert result.score == 90
    assert result.category == "High"
    assert len(result.drivers) == 3


@pytest.mark.parametrize(
    ("amount", "term_days", "late_payments", "expected_score"),
    [
        (1000, 30, 0, 10),
        (1000, 31, 0, 20),
        (1000, 60, 0, 20),
        (1000, 61, 0, 35),
        (24999, 30, 0, 10),
        (25000, 30, 0, 20),
        (99999, 30, 0, 20),
        (100000, 30, 0, 35),
        (1000, 30, 1, 25),
        (1000, 30, 2, 25),
        (1000, 30, 3, 40),
        (1000, 31, 1, 35),
        (100000, 31, 1, 60),
    ],
)
def test_scoring_boundaries(amount, term_days, late_payments, expected_score):
    result = calculate_risk(
        amount,
        BASE_DATE,
        BASE_DATE + timedelta(days=term_days),
        late_payments,
    )
    assert result.score == expected_score


def test_high_category_starts_at_60():
    result = calculate_risk(100000, BASE_DATE, BASE_DATE + timedelta(days=31), 1)
    assert result.score == 60
    assert result.category == "High"


def test_amount_zero_is_rejected():
    with pytest.raises(ValueError, match="Invoice amount"):
        calculate_risk(0, BASE_DATE, date(2026, 9, 15), 0)


def test_invalid_dates_are_rejected():
    with pytest.raises(ValueError, match="Due date"):
        calculate_risk(1000, date(2026, 9, 10), date(2026, 9, 1), 0)


def test_negative_late_payments_are_rejected():
    with pytest.raises(ValueError, match="late payments"):
        calculate_risk(1000, BASE_DATE, date(2026, 9, 15), -1)
