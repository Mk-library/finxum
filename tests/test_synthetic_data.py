import pytest

from app.risk import calculate_risk
from app.synthetic_data import SYNTHETIC_SCENARIOS


def test_exactly_25_scenarios():
    assert len(SYNTHETIC_SCENARIOS) == 25


def test_scenario_references_are_unique():
    references = [scenario.reference for scenario in SYNTHETIC_SCENARIOS]
    assert len(references) == len(set(references))


def test_scenario_references_use_synth_prefix():
    assert all(scenario.reference.startswith("SYNTH-") for scenario in SYNTHETIC_SCENARIOS)


def test_scenario_labels_are_descriptive():
    for scenario in SYNTHETIC_SCENARIOS:
        assert scenario.label
        assert len(scenario.label) > 10


def test_scenario_due_dates_are_not_before_issue_dates():
    for scenario in SYNTHETIC_SCENARIOS:
        assert scenario.due_date >= scenario.issue_date


def test_scenario_categories_cover_full_risk_range():
    categories = {scenario.expected_category for scenario in SYNTHETIC_SCENARIOS}
    assert categories == {"Low", "Medium", "High"}


@pytest.mark.parametrize(
    "scenario", SYNTHETIC_SCENARIOS, ids=[scenario.reference for scenario in SYNTHETIC_SCENARIOS]
)
def test_scenario_score_is_computed_by_calculate_risk(scenario):
    result = calculate_risk(
        scenario.amount,
        scenario.issue_date,
        scenario.due_date,
        scenario.prior_late_payments,
    )
    assert result.category == scenario.expected_category
    assert 0 <= result.score <= 100
    assert result.drivers
