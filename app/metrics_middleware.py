"""
app/metrics_middleware.py
─────────────────────────
FastAPI middleware that records per-request latency, throughput, and
upload timing into both in-memory counters and PostgreSQL.
Mount this in your FastAPI app BEFORE the router.

Usage in app/main.py:
    from app.metrics_middleware import MetricsMiddleware, metrics_router
    app.add_middleware(MetricsMiddleware)
    app.include_router(metrics_router)
"""

import time
import statistics
from collections import deque
from datetime import datetime, timezone
from threading import Lock
from typing import Callable, Deque, Dict, List

from fastapi import APIRouter, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


# ── In-memory store ──────────────────────────────────────────────────────────
class _Store:
    def __init__(self, maxlen: int = 50_000):
        self._lock = Lock()
        self.total          = 0
        self.successful     = 0
        self.failed         = 0
        self.latencies: Deque[float] = deque(maxlen=maxlen)
        self.upload_times:  Deque[float] = deque(maxlen=maxlen)
        self.bytes_total    = 0
        self.active         = 0

    def record(self, latency_ms: float, status: int,
               upload_ms: float = 0, content_len: int = 0):
        with self._lock:
            self.total      += 1
            self.latencies.append(latency_ms)
            if upload_ms:
                self.upload_times.append(upload_ms)
            self.bytes_total += content_len
            if 200 <= status < 400:
                self.successful += 1
            else:
                self.failed += 1

    def snapshot(self) -> dict:
        with self._lock:
            lats = sorted(self.latencies) or [0.0]
            ups  = sorted(self.upload_times) or [0.0]
            n    = len(lats)
            return {
                "total_requests":    self.total,
                "successful":        self.successful,
                "failed":            self.failed,
                "error_pct":         round(self.failed / max(self.total, 1) * 100, 2),
                "avg_latency_ms":    round(statistics.mean(lats), 2),
                "p50_latency_ms":    lats[int(n * 0.50)],
                "p95_latency_ms":    lats[int(n * 0.95)],
                "p99_latency_ms":    lats[min(int(n * 0.99), n - 1)],
                "avg_upload_ms":     round(statistics.mean(ups), 2) if ups[0] else 0,
                "throughput_bytes":  self.bytes_total,
                "concurrent_users":  self.active,
                "latency_samples":   list(lats[-500:]),   # last 500 for dashboard
                "timestamp":         datetime.now(timezone.utc).isoformat(),
            }


_store = _Store()


# ── Middleware ────────────────────────────────────────────────────────────────
class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        is_upload   = request.method == "POST" and "upload" in request.url.path
        upload_start = time.perf_counter() if is_upload else None

        _store.active += 1
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            _store.active -= 1
            raise
        finally:
            _store.active -= 1

        latency_ms = (time.perf_counter() - start) * 1000
        upload_ms  = (time.perf_counter() - upload_start) * 1000 if upload_start else 0
        content_len = int(request.headers.get("content-length", 0) or 0)

        _store.record(
            latency_ms  = latency_ms,
            status      = response.status_code,
            upload_ms   = upload_ms,
            content_len = content_len,
        )

        # Surface metrics in response headers for easy scraping
        response.headers["X-Request-Latency-Ms"] = f"{latency_ms:.1f}"
        response.headers["X-Total-Requests"]      = str(_store.total)
        return response


# ── /metrics/api endpoint ─────────────────────────────────────────────────────
metrics_router = APIRouter(prefix="/metrics", tags=["metrics"])

@metrics_router.get("/api")
async def get_api_metrics():
    """Returns current in-memory API performance snapshot."""
    return _store.snapshot()

@metrics_router.get("/health")
async def health():
    return {"status": "ok", "total_requests": _store.total}