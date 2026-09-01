"""Streamlit MVP for FinXum."""

from datetime import date, timedelta
from pathlib import Path
import sys

import plotly.express as px
import streamlit as st

# Make this module safe to launch directly with Streamlit from app/main.py.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from app.analytics import amount_score_pairs, category_counts, score_values, summary_stats
from app.config import DB_PATH, DISCLAIMER, RULES_VERSION
from app.database import initialize, list_assessments, save_assessment
from app.demo_loader import load_synthetic_assessments
from app.risk import calculate_risk

_CATEGORY_COLORS = {"Low": "#2ca02c", "Medium": "#ff7f0e", "High": "#d62728"}

st.set_page_config(page_title="FinXum", page_icon="📊", layout="wide")
initialize(DB_PATH)

st.title("FinXum")
st.caption("Financial risk analysis and invoice intelligence prototype")
st.warning(DISCLAIMER)

page = st.sidebar.radio("Navigate", ["New Assessment", "History", "Analytics", "Methodology"])

if page == "New Assessment":
    st.header("New Assessment")
    with st.form("assessment"):
        reference = st.text_input("Invoice / business reference", value="DEMO-001")
        amount = st.number_input("Invoice amount", min_value=0.01, value=10000.0, step=1000.0)
        issue_date = st.date_input("Issue date", value=date.today())
        due_date = st.date_input("Due date", value=date.today() + timedelta(days=30))
        prior_late_payments = st.number_input("Prior late payments", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Assess risk")

    if submitted:
        try:
            result = calculate_risk(amount, issue_date, due_date, prior_late_payments)
            assessment = {
                "reference": reference.strip() or "UNSPECIFIED",
                "amount": amount,
                "issue_date": issue_date.isoformat(),
                "due_date": due_date.isoformat(),
                "prior_late_payments": prior_late_payments,
                "score": result.score,
                "risk_category": result.category,
                "drivers": result.drivers,
                "rules_version": result.rules_version,
            }
            assessment_id = save_assessment(assessment, DB_PATH)
            st.success(f"Assessment #{assessment_id} saved.")
            st.metric("Demo risk score", result.score)
            st.subheader(f"Risk category: {result.category}")
            st.write("**Principal drivers**")
            for driver in result.drivers:
                st.write(f"- {driver}")
            st.caption(f"Rules version: {RULES_VERSION}")
        except ValueError as exc:
            st.error(str(exc))

elif page == "History":
    st.header("Assessment History")
    rows = list_assessments(DB_PATH)
    if not rows:
        st.info("No assessments yet. Create one from New Assessment.")
    else:
        st.dataframe(
            [
                {
                    "ID": row["id"],
                    "Reference": row["reference"],
                    "Amount": row["amount"],
                    "Score": row["score"],
                    "Category": row["risk_category"],
                    "Rules": row["rules_version"],
                    "Created": row["created_at"],
                }
                for row in rows
            ],
            use_container_width=True,
        )

elif page == "Analytics":
    st.header("Analytics")
    st.caption(
        "Portfolio-level view of stored assessments. All scores shown here were "
        "computed by calculate_risk() when each assessment was created or loaded."
    )

    if st.button("Load 25 Synthetic Demo Assessments"):
        load_result = load_synthetic_assessments(DB_PATH)
        if load_result.loaded:
            st.success(f"Loaded {load_result.loaded} new synthetic demo assessment(s).")
        if load_result.skipped:
            st.info(
                f"Skipped {load_result.skipped} synthetic demo assessment(s) already "
                "present (duplicate prevention)."
            )

    rows = list_assessments(DB_PATH)
    if not rows:
        st.info(
            "No assessments yet. Create one from New Assessment, or click "
            "'Load 25 Synthetic Demo Assessments' above."
        )
    else:
        stats = summary_stats(rows)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Assessments", stats["count"])
        col2.metric("Average score", f"{stats['average_score']:.1f}")
        col3.metric("Min score", stats["min_score"])
        col4.metric("Max score", stats["max_score"])

        counts = category_counts(rows)
        category_fig = px.bar(
            x=list(counts.keys()),
            y=list(counts.values()),
            labels={"x": "Risk category", "y": "Assessments"},
            title="Assessments by risk category",
            color=list(counts.keys()),
            color_discrete_map=_CATEGORY_COLORS,
        )
        st.plotly_chart(category_fig, use_container_width=True)

        score_fig = px.histogram(
            x=score_values(rows),
            nbins=10,
            labels={"x": "Demo risk score"},
            title="Score distribution",
        )
        st.plotly_chart(score_fig, use_container_width=True)

        pairs = amount_score_pairs(rows)
        scatter_fig = px.scatter(
            x=[pair[0] for pair in pairs],
            y=[pair[1] for pair in pairs],
            color=[pair[2] for pair in pairs],
            labels={"x": "Invoice amount", "y": "Demo risk score", "color": "Risk category"},
            title="Invoice amount vs. demo risk score",
            color_discrete_map=_CATEGORY_COLORS,
        )
        st.plotly_chart(scatter_fig, use_container_width=True)

    st.caption(
        "All synthetic demo data is clearly labelled with 'SYNTH-' references "
        "and represents no real customers, invoices, or payment behaviour."
    )

elif page == "Methodology":
    st.header("Methodology")
    st.write(
        "FinXum currently uses a deliberately simple deterministic baseline. "
        "The score starts at 10 and adds documented points for extended payment terms, "
        "invoice amount bands, and prior late-payment history. The final score is capped at 100."
    )
    st.write("**Categories:** Low < 30, Medium 30–59, High ≥ 60.")
    st.write(f"**Rules version:** {RULES_VERSION}")
    st.write(
        "This baseline is for demonstration and software-engineering purposes. "
        "It has no claimed predictive accuracy and must not be used as a real credit decision."
    )
    st.write(
        "See `docs/methodology.md` for the full scoring rationale, the synthetic "
        "demo scenario design, and the duplicate-prevention approach used by the "
        "Analytics page's demo loader."
    )
