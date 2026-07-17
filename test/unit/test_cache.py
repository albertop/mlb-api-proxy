"""Tests for the in-process response cache and single-flight coalescing (R3)."""

import asyncio

import httpx
import pytest
import respx
from fastapi.testclient import TestClient

import proxy
from main import app

HEADERS = {"X-API-Key": "test_proxy_key"}


@pytest.fixture(autouse=True)
def enable_cache(monkeypatch):
    """Turn the cache on (tests default it off via conftest) and start from empty."""
    monkeypatch.setattr(proxy, "CACHE_ENABLED", True)
    proxy.clear_cache()
    yield
    proxy.clear_cache()


@pytest.fixture
def client():
    c = TestClient(app)
    c.headers = HEADERS
    return c


def _counting_route(url: str, response: httpx.Response) -> dict:
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return response

    respx.get(url).mock(side_effect=handler)
    return calls


# --- Cache hits / misses ------------------------------------------------------


def test_second_request_served_from_cache():
    """A cacheable endpoint hits the upstream once; the second call is a cache hit."""
    url = "https://statsapi.mlb.com/api/v1/teams"  # matches a "static" marker
    with respx.mock:
        calls = _counting_route(url, httpx.Response(200, json={"teams": [1, 2, 3]}))
        client = TestClient(app)
        r1 = client.get("/api/v1/teams", headers=HEADERS)
        r2 = client.get("/api/v1/teams", headers=HEADERS)

    assert r1.status_code == r2.status_code == 200
    assert r1.json() == r2.json() == {"teams": [1, 2, 3]}
    assert calls["n"] == 1, "second request should be served from cache"


def test_query_params_are_part_of_cache_key():
    """Different query strings are cached separately."""
    url = "https://statsapi.mlb.com/api/v1/teams"
    with respx.mock:
        calls = _counting_route(url, httpx.Response(200, json={"teams": []}))
        client = TestClient(app)
        client.get("/api/v1/teams?sportId=1", headers=HEADERS)
        client.get("/api/v1/teams?sportId=11", headers=HEADERS)  # different key -> miss
        client.get("/api/v1/teams?sportId=1", headers=HEADERS)  # same as first -> hit

    assert calls["n"] == 2


def test_live_endpoints_are_never_cached():
    """Intra-game data (boxscore) must always go to the upstream."""
    url = "https://statsapi.mlb.com/api/v1/game/12345/boxscore"
    with respx.mock:
        calls = _counting_route(url, httpx.Response(200, json={"teams": {}}))
        client = TestClient(app)
        client.get("/api/v1/game/12345/boxscore", headers=HEADERS)
        client.get("/api/v1/game/12345/boxscore", headers=HEADERS)

    assert calls["n"] == 2, "live endpoints must not be cached"


def test_error_responses_are_not_cached():
    """A non-200 response is not cached, so the next call retries the upstream."""
    url = "https://statsapi.mlb.com/api/v1/teams"
    with respx.mock:
        calls = _counting_route(url, httpx.Response(404, json={"message": "nope"}))
        client = TestClient(app)
        client.get("/api/v1/teams", headers=HEADERS)
        client.get("/api/v1/teams", headers=HEADERS)

    assert calls["n"] == 2


def test_cache_disabled_bypasses_cache(monkeypatch):
    """With ENABLE_CACHE off, every request reaches the upstream."""
    monkeypatch.setattr(proxy, "CACHE_ENABLED", False)
    url = "https://statsapi.mlb.com/api/v1/teams"
    with respx.mock:
        calls = _counting_route(url, httpx.Response(200, json={"teams": []}))
        client = TestClient(app)
        client.get("/api/v1/teams", headers=HEADERS)
        client.get("/api/v1/teams", headers=HEADERS)

    assert calls["n"] == 2


# --- Single-flight coalescing -------------------------------------------------


@pytest.mark.asyncio
async def test_coalesce_runs_factory_once_for_concurrent_callers():
    """Concurrent callers on the same key share a single factory execution."""
    calls = {"n": 0}
    gate = asyncio.Event()

    async def factory():
        calls["n"] += 1
        await gate.wait()  # hold the in-flight fetch open so others coalesce onto it
        return proxy.FetchResult(200, b'{"ok":true}', "application/json", True)

    waiters = [asyncio.create_task(proxy._coalesce("k", factory)) for _ in range(10)]
    await asyncio.sleep(0.01)  # let all tasks reach the in-flight await
    gate.set()
    results = await asyncio.gather(*waiters)

    assert calls["n"] == 1, "factory must run exactly once for coalesced callers"
    assert all(r.content == b'{"ok":true}' for r in results)


@pytest.mark.asyncio
async def test_coalesce_propagates_errors_and_clears_inflight():
    """If the factory fails, the error propagates and the key is freed for retry."""

    async def failing():
        raise httpx.ConnectError("boom")

    with pytest.raises(httpx.ConnectError):
        await proxy._coalesce("k2", failing)

    assert "k2" not in proxy._inflight  # freed, so a later call can retry
