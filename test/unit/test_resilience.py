"""Resilience tests for the shared HTTP client (R1) and upstream retries (R2)."""

import httpx
import pytest
import respx
from fastapi.testclient import TestClient

import proxy
from main import app

UPSTREAM = "https://statsapi.mlb.com/api/v1/teams"
HEADERS = {"X-API-Key": "test_proxy_key"}


@pytest.fixture(autouse=True)
def fast_backoff(monkeypatch):
    """Keep retry backoff near-zero so tests stay fast and deterministic."""
    monkeypatch.setattr(proxy, "UPSTREAM_BACKOFF_BASE_SECONDS", 0.0)
    monkeypatch.setattr(proxy, "UPSTREAM_BACKOFF_MAX_SECONDS", 0.0)
    monkeypatch.setattr(proxy, "UPSTREAM_MAX_RETRIES", 2)


# --- R1: shared pooled client -------------------------------------------------


def test_lifespan_creates_shared_client():
    """The app lifespan installs a single reusable httpx client on app.state."""
    with respx.mock:
        respx.get(UPSTREAM).mock(return_value=httpx.Response(200, json={"teams": []}))
        with TestClient(app) as client:
            shared = getattr(app.state, "http", None)
            assert isinstance(shared, httpx.AsyncClient)
            resp = client.get("/api/v1/teams", headers=HEADERS)
            assert resp.status_code == 200
            # The shared client is reused, not closed after each request.
            assert not shared.is_closed


# --- R2: retry policy ---------------------------------------------------------


def test_retryable_status_then_success():
    """A transient 503 is retried and the eventual 200 is returned."""
    with respx.mock:
        calls = {"n": 0}

        def handler(request):
            calls["n"] += 1
            if calls["n"] < 3:
                return httpx.Response(503, json={"err": "busy"})
            return httpx.Response(200, json={"teams": [], "ok": True})

        respx.get(UPSTREAM).mock(side_effect=handler)
        with TestClient(app) as client:
            resp = client.get("/api/v1/teams", headers=HEADERS)

        assert resp.status_code == 200
        assert calls["n"] == 3  # 1 initial + 2 retries


def test_connect_error_exhausts_retries_then_502():
    """A persistent connection error is retried, then surfaced as 502."""
    with respx.mock:
        calls = {"n": 0}

        def handler(request):
            calls["n"] += 1
            raise httpx.ConnectError("boom")

        respx.get(UPSTREAM).mock(side_effect=handler)
        with TestClient(app) as client:
            resp = client.get("/api/v1/teams", headers=HEADERS)

        assert resp.status_code == 502
        assert calls["n"] == 3  # 1 initial + 2 retries


def test_429_is_passed_through_without_retry():
    """429 is a client signal, not a transient error: pass it through unchanged."""
    with respx.mock:
        calls = {"n": 0}

        def handler(request):
            calls["n"] += 1
            return httpx.Response(429, json={"err": "rate"})

        respx.get(UPSTREAM).mock(side_effect=handler)
        with TestClient(app) as client:
            resp = client.get("/api/v1/teams", headers=HEADERS)

        assert resp.status_code == 429
        assert calls["n"] == 1  # not retried


def test_non_retryable_500_is_not_retried():
    """A plain 500 is not in the retryable set and is returned immediately."""
    with respx.mock:
        calls = {"n": 0}

        def handler(request):
            calls["n"] += 1
            return httpx.Response(500, json={"err": "oops"})

        respx.get(UPSTREAM).mock(side_effect=handler)
        with TestClient(app) as client:
            resp = client.get("/api/v1/teams", headers=HEADERS)

        assert resp.status_code == 500
        assert calls["n"] == 1  # not retried


# --- Liveness vs readiness ----------------------------------------------------


def test_live_endpoint_never_touches_upstream():
    """/live returns 200 without any upstream call (respx would error on a stray call)."""
    # No routes registered: any upstream request would raise.
    with respx.mock, TestClient(app) as client:
        resp = client.get("/live")
    assert resp.status_code == 200
    assert resp.json()["status"] == "alive"


# --- Non-JSON passthrough (no corruption) -------------------------------------


def test_non_json_body_is_forwarded_verbatim():
    """CSV/binary bodies pass through byte-for-byte, not re-encoded via text."""
    csv = b"col_a,col_b\n1,2\n"
    with respx.mock:
        respx.get(UPSTREAM).mock(
            return_value=httpx.Response(200, content=csv, headers={"content-type": "text/csv"})
        )
        with TestClient(app) as client:
            resp = client.get("/api/v1/teams", headers=HEADERS)

    assert resp.status_code == 200
    assert resp.content == csv  # exact bytes preserved
    assert resp.headers["content-type"].startswith("text/csv")
