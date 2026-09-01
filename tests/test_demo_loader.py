from app.database import initialize, list_assessments, save_assessment
from app.demo_loader import load_synthetic_assessments
from app.risk import calculate_risk
from app.synthetic_data import SYNTHETIC_SCENARIOS


def test_load_synthetic_assessments_inserts_all_25_into_empty_db(tmp_path):
    db_path = str(tmp_path / "finxum.db")
    initialize(db_path)

    result = load_synthetic_assessments(db_path)

    assert result.loaded == 25
    assert result.skipped == 0
    assert len(list_assessments(db_path)) == 25


def test_load_synthetic_assessments_is_idempotent(tmp_path):
    db_path = str(tmp_path / "finxum.db")
    initialize(db_path)

    load_synthetic_assessments(db_path)
    second_result = load_synthetic_assessments(db_path)

    assert second_result.loaded == 0
    assert second_result.skipped == 25
    assert len(list_assessments(db_path)) == 25


def test_load_synthetic_assessments_skips_only_existing_references(tmp_path):
    db_path = str(tmp_path / "finxum.db")
    initialize(db_path)

    first_scenario = SYNTHETIC_SCENARIOS[0]
    pre_existing = calculate_risk(
        first_scenario.amount,
        first_scenario.issue_date,
        first_scenario.due_date,
        first_scenario.prior_late_payments,
    )
    save_assessment(
        {
            "reference": first_scenario.reference,
            "amount": first_scenario.amount,
            "issue_date": first_scenario.issue_date.isoformat(),
            "due_date": first_scenario.due_date.isoformat(),
            "prior_late_payments": first_scenario.prior_late_payments,
            "score": pre_existing.score,
            "risk_category": pre_existing.category,
            "drivers": pre_existing.drivers,
            "rules_version": pre_existing.rules_version,
        },
        db_path,
    )

    result = load_synthetic_assessments(db_path)

    assert result.loaded == 24
    assert result.skipped == 1
    assert first_scenario.reference in result.skipped_references
    assert len(list_assessments(db_path)) == 25


def test_load_synthetic_assessments_does_not_duplicate_unrelated_references(tmp_path):
    db_path = str(tmp_path / "finxum.db")
    initialize(db_path)
    result = calculate_risk(1000, SYNTHETIC_SCENARIOS[0].issue_date, SYNTHETIC_SCENARIOS[0].due_date, 0)
    save_assessment(
        {
            "reference": "DEMO-001",
            "amount": 1000,
            "issue_date": SYNTHETIC_SCENARIOS[0].issue_date.isoformat(),
            "due_date": SYNTHETIC_SCENARIOS[0].due_date.isoformat(),
            "prior_late_payments": 0,
            "score": result.score,
            "risk_category": result.category,
            "drivers": result.drivers,
            "rules_version": result.rules_version,
        },
        db_path,
    )

    load_result = load_synthetic_assessments(db_path)

    assert load_result.loaded == 25
    assert load_result.skipped == 0
    assert len(list_assessments(db_path)) == 26


def test_load_synthetic_assessments_scores_match_calculate_risk(tmp_path):
    db_path = str(tmp_path / "finxum.db")
    initialize(db_path)

    load_synthetic_assessments(db_path)
    rows_by_reference = {row["reference"]: row for row in list_assessments(db_path)}

    for scenario in SYNTHETIC_SCENARIOS:
        expected = calculate_risk(
            scenario.amount, scenario.issue_date, scenario.due_date, scenario.prior_late_payments
        )
        stored = rows_by_reference[scenario.reference]
        assert stored["score"] == expected.score
        assert stored["risk_category"] == expected.category
