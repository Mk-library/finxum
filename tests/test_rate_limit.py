"""Tests for the in-process rate limiter (app/rate_limit.py)."""

import pytest
from fastapi import HTTPException

from app.rate_limit import RateLimiter


def test_allows_up_to_the_limit():
    limiter = RateLimiter(max_requests=3, window_seconds=60)
    for _ in range(3):
        limiter.check("client-a")


def test_rejects_once_limit_exceeded():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    limiter.check("client-a")
    limiter.check("client-a")

    with pytest.raises(HTTPException) as exc_info:
        limiter.check("client-a")
    assert exc_info.value.status_code == 429


def test_limits_are_independent_per_key():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    limiter.check("client-a")
    limiter.check("client-b")  # different key, own budget


def test_old_hits_expire_out_of_the_window():
    limiter = RateLimiter(max_requests=1, window_seconds=0.05)
    limiter.check("client-a")
    with pytest.raises(HTTPException):
        limiter.check("client-a")

    import time

    time.sleep(0.1)
    limiter.check("client-a")  # window has passed, budget refreshed
