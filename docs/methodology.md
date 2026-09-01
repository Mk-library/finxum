# Methodology & Design

This document explains how FinXum's risk score is computed, how the
synthetic demo dataset was designed, and how the Analytics page and demo
loader avoid creating duplicate data. It supplements `docs/architecture.md`
(component boundaries) and `docs/project-log.md` (implementation history).

## 1. Risk scoring methodology

All scores are produced by the single deterministic function
`app.risk.calculate_risk()`. No other code path assigns or overrides a
score — the Analytics page, the synthetic demo loader, and the New
Assessment form all call this same function. This document does not change
that function or its scoring logic.

### Inputs

- `amount` — invoice amount (must be > 0).
- `issue_date` / `due_date` — the payment term is derived as
  `due_date - issue_date` (must not be negative).
- `prior_late_payments` — count of prior late payments (must be ≥ 0).

Invalid inputs raise `ValueError` and are never scored.

### Rule table

The score starts at a base of **10** and adds points from three independent,
additive factors. The final score is capped at **100**.

| Factor | Band | Points |
| --- | --- | --- |
| Payment term | ≤ 30 days | +0 |
| Payment term | 31–60 days | +10 |
| Payment term | > 60 days | +25 |
| Invoice amount | < 25,000 | +0 |
| Invoice amount | 25,000–99,999 | +10 |
| Invoice amount | ≥ 100,000 | +25 |
| Prior late payments | 0 | +0 |
| Prior late payments | 1–2 | +15 |
| Prior late payments | ≥ 3 | +30 |

### Categories

- **Low:** score < 30
- **Medium:** 30 ≤ score < 60
- **High:** score ≥ 60

### Explainability

Every scored assessment carries a list of human-readable `drivers` naming
which bands were triggered, plus the `rules_version` that produced it, so a
result can always be traced back to the rule table above.

### What this is not

This is a deliberately simple, interpretable baseline for demonstration and
software-engineering purposes. It has no claimed predictive accuracy and is
not a real credit decision system.

## 2. Synthetic demo scenario design

The 25 scenarios in `app.synthetic_data.SYNTHETIC_SCENARIOS` exist to give
the Analytics page representative data to visualize, and to exercise
`calculate_risk()` across its full Low/Medium/High output range, without
using or fabricating any real customer, invoice, or payment data.

### Construction

The three factors `calculate_risk()` scores on (payment term, invoice
amount, prior late payments) each have three representative bands, which
gives a 3×3×3 = 27-cell factorial grid:

| Factor | Low band value | Medium band value | High band value |
| --- | --- | --- | --- |
| Payment term | 15 days | 45 days | 90 days |
| Invoice amount | 5,000 | 50,000 | 150,000 |
| Prior late payments | 0 | 2 | 4 |

Two redundant cells (`45-day / <25,000 / ≥3 late` and `90-day / <25,000 /
1–2 late`) were dropped to reach exactly **25** scenarios while keeping the
grid's coverage of the scoring rules intact. The resulting set spans 4 Low,
11 Medium, and 10 High outcomes.

### Labelling and traceability

- Every scenario has a fixed reference in the form `SYNTH-001`…`SYNTH-025`,
  and a plain-language `label` describing the combination it represents
  (e.g. "High-value invoice, long term, repeated late payments").
- Every scenario carries an `expected_category`, which documents the
  outcome the scenario is designed to demonstrate. This is a design/test
  aid only — it is never written to the database or shown to a user in
  place of an actual `calculate_risk()` result. `tests/test_synthetic_data.py`
  asserts that `calculate_risk()`, run on each scenario's actual inputs,
  produces that category.
- The synthetic reference prefix (`SYNTH-`) and the Analytics page caption
  make clear that this data is synthetic and does not represent real
  customers, invoices, or payment behaviour, consistent with the
  integrity rules in `README.md`.

## 3. Demo loader and duplicate prevention

The "Load 25 Synthetic Demo Assessments" button on the Analytics page calls
`app.demo_loader.load_synthetic_assessments()`, which:

1. Reads existing assessment references from the database.
2. For each of the 25 synthetic scenarios, skips it if its reference is
   already present, and otherwise scores it with `calculate_risk()` and
   persists it via the existing `save_assessment()` path.
3. Returns counts of newly loaded vs. skipped scenarios, which the UI
   surfaces back to the user.

Because each scenario has a fixed, stable reference, clicking the button
repeatedly — or loading the demo set, then creating more assessments, then
loading it again — never creates duplicate rows for the same scenario. This
uses the existing `risk_assessments` table and `reference` column; no new
table, index, or storage engine was introduced.

## 4. Analytics page

The Analytics page (`app/main.py`, backed by pure helpers in
`app/analytics.py`) renders three Plotly charts over whatever assessments
are currently stored (manually created and/or synthetic demo data):

- **Assessments by risk category** — bar chart of Low/Medium/High counts.
- **Score distribution** — histogram of all stored scores.
- **Invoice amount vs. demo risk score** — scatter plot, coloured by
  category.

The aggregation helpers (`category_counts`, `score_values`,
`amount_score_pairs`, `summary_stats`) only read already-persisted rows;
they perform no scoring themselves and are unit-tested independently of
Streamlit/Plotly rendering in `tests/test_analytics.py`.

## 5. Testing strategy

- `tests/test_risk.py` — unchanged; covers `calculate_risk()` boundaries and
  validation directly.
- `tests/test_synthetic_data.py` — validates the shape of the 25-scenario
  set (count, unique references, labels, valid dates) and cross-checks each
  scenario's `calculate_risk()` output against its declared
  `expected_category`.
- `tests/test_demo_loader.py` — covers first-load, idempotent re-load
  (duplicate prevention), partial-overlap skipping, and that persisted
  scores match `calculate_risk()` exactly.
- `tests/test_analytics.py` — unit tests for the pure aggregation helpers.
- `tests/test_streamlit_app.py` — end-to-end Streamlit `AppTest` coverage of
  the Analytics page, including clicking the demo-load button twice and
  confirming the History table still shows exactly 25 rows.
- `tests/test_database.py` — unchanged; persistence round-trip.
