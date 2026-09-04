"""FastAPI boundary exposing the deterministic risk engine programmatically.

This mirrors the scoring path used by the Streamlit UI (app/main.py): validate
input, call calculate_risk(), persist the result, and return it. Every
assessment scored through this API is saved into the same SQLite history
table used by the Streamlit app.
"""

from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import APP_VERSION, DB_PATH, DISCLAIMER, RULES_VERSION
from .database import initialize, save_assessment
from .risk import calculate_risk

app = FastAPI(
    title="FinXum Risk API",
    version=APP_VERSION,
    description=f"{DISCLAIMER} Scores are deterministic and rule-based, not ML-driven.",
)

initialize(DB_PATH)


class RiskAssessmentRequest(BaseModel):
    reference: str | None = Field(None, description="Invoice / business reference.")
    amount: float = Field(..., gt=0, description="Invoice amount, must be greater than zero.")
    issue_date: date
    due_date: date
    prior_late_payments: int = Field(..., ge=0)


class RiskAssessmentResponse(BaseModel):
    id: int
    reference: str
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

    reference = (request.reference or "").strip() or "UNSPECIFIED"
    assessment_id = save_assessment(
        {
            "reference": reference,
            "amount": request.amount,
            "issue_date": request.issue_date.isoformat(),
            "due_date": request.due_date.isoformat(),
            "prior_late_payments": request.prior_late_payments,
            "score": result.score,
            "risk_category": result.category,
            "drivers": result.drivers,
            "rules_version": result.rules_version,
        },
        DB_PATH,
    )

    return RiskAssessmentResponse(
        id=assessment_id,
        reference=reference,
        score=result.score,
        category=result.category,
        drivers=result.drivers,
        rules_version=result.rules_version,
    )
