from datetime import date

from app.database import initialize, list_assessments, save_assessment
from app.risk import calculate_risk


def test_assessment_persists_and_round_trips(tmp_path):
    db_path = tmp_path / "finxum.db"
    initialize(str(db_path))

    result = calculate_risk(1000, date(2026, 9, 1), date(2026, 9, 15), 0)
    assessment = {
        "reference": "TEST-001",
        "amount": 1000,
        "issue_date": "2026-09-01",
        "due_date": "2026-09-15",
        "prior_late_payments": 0,
        "score": result.score,
        "risk_category": result.category,
        "drivers": result.drivers,
        "rules_version": result.rules_version,
    }

    assessment_id = save_assessment(assessment, str(db_path))
    rows = list_assessments(str(db_path))

    assert assessment_id == 1
    assert len(rows) == 1
    assert rows[0]["reference"] == "TEST-001"
    assert rows[0]["score"] == 10
    assert rows[0]["risk_category"] == "Low"
