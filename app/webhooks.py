"""Inbound webhook endpoint for authorized n8n workflows.

An n8n workflow POSTs invoice/business data here to have FinXum score it
with the same deterministic engine used by the Streamlit UI and the
/risk/assess API, and persist the result into the shared risk_assessments
history table.

Authentication
--------------
Every request must carry:

    Authorization: Bearer <token>

where <token> matches the FINXUM_N8N_WEBHOOK_SECRET environment variable
(set it via a local .env / deployment secret store; never commit it). If
the variable is unset, the endpoint refuses all requests (fails closed)
rather than accepting unauthenticated calls. Configure this as the value
of an "Authorization" header on the n8n HTTP Request node that calls this
endpoint (e.g. via a Header Auth credential).

Payload contract
----------------
POST /webhooks/n8n/risk-event

{
  "reference": "INV-12345",       # required, non-empty invoice/business id
  "amount": 42000.0,              # required, > 0
  "issue_date": "2026-01-01",     # required, ISO 8601 date
  "due_date": "2026-02-15",       # required, ISO 8601 date, not before issue_date
  "prior_late_payments": 0        # required, >= 0
}

The schema is strict: unrecognized fields are rejected (422) rather than
silently ignored, so a misconfigured n8n node fails fast instead of
dropping data unnoticed.
"""

import hmac
import os
from datetime import date

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from .config import DB_PATH
from .risk_service import RiskAssessmentResult, score_and_persist

WEBHOOK_SECRET_ENV_VAR = "FINXUM_N8N_WEBHOOK_SECRET"

router = APIRouter(prefix="/webhooks/n8n", tags=["n8n"])


def verify_n8n_token(authorization: str | None = Header(default=None)) -> None:
    """FastAPI dependency enforcing bearer-token auth for n8n webhook calls."""
    secret = os.environ.get(WEBHOOK_SECRET_ENV_VAR)
    if not secret:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            f"n8n webhook is not configured ({WEBHOOK_SECRET_ENV_VAR} is unset).",
        )
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token.")

    token = authorization.removeprefix("Bearer ").strip()
    if not token or not hmac.compare_digest(token, secret):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid webhook token.")


class N8nRiskEventPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference: str = Field(..., min_length=1, description="Invoice / business reference.")
    amount: float = Field(..., gt=0, description="Invoice amount, must be greater than zero.")
    issue_date: date
    due_date: date
    prior_late_payments: int = Field(..., ge=0)


@router.post(
    "/risk-event",
    response_model=RiskAssessmentResult,
    dependencies=[Depends(verify_n8n_token)],
)
def receive_risk_event(payload: N8nRiskEventPayload) -> RiskAssessmentResult:
    try:
        return score_and_persist(
            payload.reference,
            payload.amount,
            payload.issue_date,
            payload.due_date,
            payload.prior_late_payments,
            DB_PATH,
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, str(exc)) from exc
