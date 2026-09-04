"""Tests for the n8n webhook endpoint (app/webhooks.py)."""

import pytest
from fastapi.testclient import TestClient

from app import webhooks
from app.api import app
from app.database import initialize, list_assessments
from app.webhooks import WEBHOOK_SECRET_ENV_VAR

client = TestClient(app)

VALID_PAYLOAD = {
    "reference": "N8N-001",
    "amount": 50000,
    "issue_date": "2026-01-01",
    "due_date": "2026-02-15",
    "prior_late_payments": 1,
}


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "finxum.db")
    initialize(db_path)
    monkeypatch.setattr(webhooks, "DB_PATH", db_path)
    return db_path


@pytest.fixture
def configured_secret(monkeypatch):
    secret = "test-secret-token"
    monkeypatch.setenv(WEBHOOK_SECRET_ENV_VAR, secret)
    return secret


def test_rejects_when_secret_not_configured(monkeypatch):
    monkeypatch.delenv(WEBHOOK_SECRET_ENV_VAR, raising=False)
    response = client.post(
        "/webhooks/n8n/risk-event",
        json=VALID_PAYLOAD,
        headers={"Authorization": "Bearer whatever"},
    )
    assert response.status_code == 503


def test_rejects_missing_token(configured_secret):
    response = client.post("/webhooks/n8n/risk-event", json=VALID_PAYLOAD)
    assert response.status_code == 401


def test_rejects_wrong_token(configured_secret):
    response = client.post(
        "/webhooks/n8n/risk-event",
        json=VALID_PAYLOAD,
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401


def test_accepts_correct_token_and_persists(configured_secret, isolated_db):
    response = client.post(
        "/webhooks/n8n/risk-event",
        json=VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {configured_secret}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["reference"] == "N8N-001"

    rows = list_assessments(isolated_db)
    assert len(rows) == 1
    assert rows[0]["reference"] == "N8N-001"
    assert rows[0]["id"] == body["id"]


def test_rejects_missing_reference(configured_secret, isolated_db):
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "reference"}
    response = client.post(
        "/webhooks/n8n/risk-event",
        json=payload,
        headers={"Authorization": f"Bearer {configured_secret}"},
    )
    assert response.status_code == 422
    assert list_assessments(isolated_db) == []


def test_rejects_unexpected_field(configured_secret, isolated_db):
    payload = {**VALID_PAYLOAD, "extra_field": "not allowed"}
    response = client.post(
        "/webhooks/n8n/risk-event",
        json=payload,
        headers={"Authorization": f"Bearer {configured_secret}"},
    )
    assert response.status_code == 422
    assert list_assessments(isolated_db) == []


def test_rejects_invalid_business_rule(configured_secret, isolated_db):
    payload = {**VALID_PAYLOAD, "due_date": "2025-01-01"}
    response = client.post(
        "/webhooks/n8n/risk-event",
        json=payload,
        headers={"Authorization": f"Bearer {configured_secret}"},
    )
    assert response.status_code == 422
    assert list_assessments(isolated_db) == []
