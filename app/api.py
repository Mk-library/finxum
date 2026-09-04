"""FastAPI boundary exposing the deterministic risk engine programmatically.

This mirrors the scoring path used by the Streamlit UI (app/main.py): validate
input, call calculate_risk(), and return the result. It does not persist
assessments; SQLite history remains a Streamlit-only concern for now.
"""

from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import APP_VERSION, DISCLAIMER, RULES_VERSION
from .risk import calculate_risk

app = FastAPI(
    title="FinXum Risk API",
    version=APP_VERSION,
    description=f"{DISCLAIMER} Scores are deterministic and rule-based, not ML-driven.",
)


class RiskAssessmentRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Invoice amount, must be greater than zero.")
    issue_date: date
    due_date: date
    prior_late_payments: int = Field(..., ge=0)


class RiskAssessmentResponse(BaseModel):
    score: int
    category: str
    drivers: list[str]
    rules_version: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app_version": APP_VERSION, "rules_version": RULES_VERSION}


@app.post("/risk/assess", response_model=RiskAssessmentResponse)
def assess_risk(request: RiskAssessmentRequest) -> RiskAssessmentResponse:
    try:
        result = calculate_risk(
            request.amount,
            request.issue_date,
            request.due_date,
            request.prior_late_payments,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return RiskAssessmentResponse(
        score=result.score,
        category=result.category,
        drivers=result.drivers,
        rules_version=result.rules_version,
    )
