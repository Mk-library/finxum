"""Pure aggregation helpers for the FinXum Analytics page.

These functions only summarize rows already produced by
`app.risk.calculate_risk()` and persisted via `app.database`; they do not
compute or alter any risk score.
"""

from collections import Counter

_CATEGORIES = ("Low", "Medium", "High")


def category_counts(rows: list[dict]) -> dict[str, int]:
    counts = Counter(row["risk_category"] for row in rows)
    return {category: counts.get(category, 0) for category in _CATEGORIES}


def score_values(rows: list[dict]) -> list[int]:
    return [row["score"] for row in rows]


def amount_score_pairs(rows: list[dict]) -> list[tuple[float, int, str]]:
    return [(row["amount"], row["score"], row["risk_category"]) for row in rows]


def summary_stats(rows: list[dict]) -> dict:
    if not rows:
        return {"count": 0, "average_score": 0.0, "min_score": 0, "max_score": 0}

    scores = score_values(rows)
    return {
        "count": len(rows),
        "average_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores),
    }
