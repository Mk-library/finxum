from datetime import date

import pytest

from app.risk import calculate_risk


def test_low_risk_baseline():
    result = calculate_risk(1000, date(2026, 9, 1), date(2026, 9, 15), 0)
    assert result.score == 10
    assert result.category == "Low"
    assert result.rules_version == "rules-v0.1"


def test_high_risk_factors_are_applied():
    result = calculate_risk(150000, date(2026, 9, 1), date(2026, 11, 15), 3)
    assert result.score == 90
    assert result.category == "High"
    assert len(result.drivers) == 3


def test_boundary_values_do_not_trigger_next_band():
    result = calculate_risk(25000, date(2026, 9, 1), date(2026, 10, 1), 0)
    assert result.score == 20
    assert result.category == "Low"

    result = calculate_risk(100000, date(2026, 9, 1), date(2026, 11, 1), 0)
    assert result.score == 45
    assert result.category == "Medium"


def test_amount_zero_is_rejected():
    with pytest.raises(ValueError, match="Invoice amount"):
        calculate_risk(0, date(2026, 9, 1), date(2026, 9, 15), 0)


def test_invalid_dates_are_rejected():
    with pytest.raises(ValueError, match="Due date"):
        calculate_risk(1000, date(2026, 9, 10), date(2026, 9, 1), 0)


def test_negative_late_payments_are_rejected():
    with pytest.raises(ValueError, match="late payments"):
        calculate_risk(1000, date(2026, 9, 1), date(2026, 9, 15), -1)
