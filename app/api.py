"""FastAPI boundary exposing the deterministic risk engine programmatically.

This mirrors the scoring path used by the Streamlit UI (app/main.py): validate
input, call calculate_risk(), persist the result, and return it. Every
assessment scored through this API is saved into the same SQLite history
table used by the Streamlit app.

Also mounts the n8n webhook router (app/webhooks.py) under /webhooks/n8n,
which uses the same scoring/persistence path but with its own strict
payload schema and bearer-token authentication for automated callers.
"""

from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import APP_VERSION, DB_PATH, DISCLAIMER, RULES_VERSION
from .database import initialize
from .risk_service import RiskAssessmentResult, score_and_persist
from .webhooks import router as n8n_webhook_router

app = FastAPI(
    title="FinXum Risk API",
    version=APP_VERSION,
    description=f"{DISCLAIMER} Scores are deterministic and rule-based, not ML-driven.",
)

initialize(DB_PATH)
app.include_router(n8n_webhook_router)


class RiskAssessmentRequest(BaseModel):
    reference: str | None = Field(None, description="Invoice / business reference.")
    amount: float = Field(..., gt=0, description="Invoice amount, must be greater than zero.")
    issue_date: date
    due_date: date
    prior_late_payments: int = Field(..., ge=0)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app_version": APP_VERSION, "rules_version": RULES_VERSION}


@app.post("/risk/assess", response_model=RiskAssessmentResult)
def assess_risk(request: RiskAssessmentRequest) -> RiskAssessmentResult:
    try:
        return score_and_persist(
            request.reference,
            request.amount,
            request.issue_date,
            request.due_date,
            request.prior_late_payments,
            DB_PATH,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
