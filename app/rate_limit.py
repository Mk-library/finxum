"""In-process rate limiting for public write endpoints.

Fixed-window-ish limiter keyed by client IP, kept in memory. This is enough
to stop casual scripted abuse of a single-instance deployment; it resets on
process restart and does not coordinate across multiple instances. A
multi-instance production deployment needs a shared store (e.g. Redis)
instead.
"""

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: float) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.monotonic()
        hits = self._hits[key]
        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()
        if len(hits) >= self.max_requests:
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS,
                "Rate limit exceeded. Try again shortly.",
            )
        hits.append(now)


def client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"
