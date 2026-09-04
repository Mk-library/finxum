"""Tests for the FastAPI risk-scoring boundary."""

from datetime import date

import pytest
from fastapi.testclient import TestClient

from app import api
from app.database import initialize, list_assessments
from app.risk import calculate_risk

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "finxum.db")
    initialize(db_path)
    monkeypatch.setattr(api, "DB_PATH", db_path)
    return db_path


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_assess_risk_matches_calculate_risk(isolated_db):
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


def test_assess_risk_persists_to_history(isolated_db):
    payload = {
        "reference": "API-001",
        "amount": 50000,
        "issue_date": "2026-01-01",
        "due_date": "2026-02-15",
        "prior_late_payments": 1,
    }
    response = client.post("/risk/assess", json=payload)
    assert response.status_code == 200
    body = response.json()

    rows = list_assessments(isolated_db)
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]
    assert rows[0]["reference"] == "API-001"
    assert rows[0]["score"] == body["score"]
    assert rows[0]["risk_category"] == body["category"]


def test_assess_risk_defaults_reference_when_blank(isolated_db):
    payload = {
        "amount": 1000,
        "issue_date": "2026-01-01",
        "due_date": "2026-01-15",
        "prior_late_payments": 0,
    }
    response = client.post("/risk/assess", json=payload)
    assert response.status_code == 200
    assert response.json()["reference"] == "UNSPECIFIED"
    assert list_assessments(isolated_db)[0]["reference"] == "UNSPECIFIED"


def test_assess_risk_rejects_zero_amount(isolated_db):
    payload = {
        "amount": 0,
        "issue_date": "2026-01-01",
        "due_date": "2026-02-01",
        "prior_late_payments": 0,
    }
    response = client.post("/risk/assess", json=payload)
    assert response.status_code == 422
    assert list_assessments(isolated_db) == []


def test_assess_risk_rejects_due_date_before_issue_date(isolated_db):
    payload = {
        "amount": 1000,
        "issue_date": "2026-02-01",
        "due_date": "2026-01-01",
        "prior_late_payments": 0,
    }
    response = client.post("/risk/assess", json=payload)
    assert response.status_code == 422
    assert list_assessments(isolated_db) == []
