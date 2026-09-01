import pytest

from app.analytics import amount_score_pairs, category_counts, score_values, summary_stats

ROWS = [
    {"amount": 1000, "score": 10, "risk_category": "Low"},
    {"amount": 50000, "score": 45, "risk_category": "Medium"},
    {"amount": 150000, "score": 90, "risk_category": "High"},
    {"amount": 2000, "score": 20, "risk_category": "Low"},
]


def test_category_counts_with_data():
    assert category_counts(ROWS) == {"Low": 2, "Medium": 1, "High": 1}


def test_category_counts_empty():
    assert category_counts([]) == {"Low": 0, "Medium": 0, "High": 0}


def test_score_values_extracts_scores_in_order():
    assert score_values(ROWS) == [10, 45, 90, 20]


def test_score_values_empty():
    assert score_values([]) == []


def test_amount_score_pairs_includes_category():
    pairs = amount_score_pairs(ROWS)
    assert pairs[0] == (1000, 10, "Low")
    assert len(pairs) == 4


def test_summary_stats_empty():
    assert summary_stats([]) == {"count": 0, "average_score": 0.0, "min_score": 0, "max_score": 0}


def test_summary_stats_with_data():
    stats = summary_stats(ROWS)
    assert stats["count"] == 4
    assert stats["min_score"] == 10
    assert stats["max_score"] == 90
    assert stats["average_score"] == pytest.approx(41.25)
