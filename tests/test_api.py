"""Tests for the FastAPI risk-scoring boundary."""

from datetime import date

from fastapi.testclient import TestClient

from app.api import app
from app.risk import calculate_risk

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_assess_risk_matches_calculate_risk():
    payload = {
        "amount": 50000,
        "issue_date": "2026-01-01",
        "due_date": "2026-02-15",
        "prior_late_payments": 1,
    }
    response = client.post("/risk/assess", json=payload)
    assert response.status_code == 200

    expected = calculate_risk(50000, date(2026, 1, 1), date(2026, 2, 15), 1)
    body = response.json()
    assert body["score"] == expected.score
    assert body["category"] == expected.category
    assert body["drivers"] == expected.drivers
    assert body["rules_version"] == expected.rules_version


def test_assess_risk_rejects_zero_amount():
    payload = {
        "amount": 0,
        "issue_date": "2026-01-01",
        "due_date": "2026-02-01",
        "prior_late_payments": 0,
    }
    response = client.post("/risk/assess", json=payload)
    assert response.status_code == 422


def test_assess_risk_rejects_due_date_before_issue_date():
    payload = {
        "amount": 1000,
        "issue_date": "2026-02-01",
        "due_date": "2026-01-01",
        "prior_late_payments": 0,
    }
    response = client.post("/risk/assess", json=payload)
    assert response.status_code == 422
