"""Shared pytest fixtures for MLB API tests."""

import json
import os
import re
import sys
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
import respx
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response


def pytest_addoption(parser):
    parser.addoption(
        "--run-smoke",
        action="store_true",
        default=False,
        help="run smoke tests (skipped by default; meant for live-deployment checks)",
    )


def pytest_collection_modifyitems(config, items):
    """Skip tests marked `smoke` unless --run-smoke is passed."""
    if config.getoption("--run-smoke"):
        return
    skip_smoke = pytest.mark.skip(reason="smoke test; pass --run-smoke to enable")
    for item in items:
        if "smoke" in item.keywords:
            item.add_marker(skip_smoke)


# Set environment variables before importing app. Only real Settings fields are
# set here (see proxy.Settings); the cache is disabled so tests are deterministic.
os.environ.setdefault("MLB_BASE_URL", "https://statsapi.mlb.com")
os.environ.setdefault("PROXY_API_KEY", "test_proxy_key")
os.environ.setdefault("LOG_LEVEL", "ERROR")
os.environ.setdefault("ENABLE_CACHE", "false")

# Add api-service to path
api_service_path = Path(__file__).parent.parent / "api-service"
sys.path.insert(0, str(api_service_path))

from main import app  # noqa: E402

RESPONSE_EXAMPLES_DIR = Path(__file__).parent.parent / "docs" / "response-examples"
RESPONSE_EXAMPLES_INDEX = Path(__file__).parent.parent / "docs" / "response-examples-index.json"
_EXAMPLE_INDEX: dict[tuple[str, str], str] | None = None


def _normalize_example_path(path: str) -> str:
    normalized = path
    normalized = re.sub(r"^/api/v1/draft/\d+/latest$", "/api/v1/draft/{year}/latest", normalized)
    normalized = re.sub(
        r"^/api/v1/draft/prospects/\d+$", "/api/v1/draft/prospects/{year}", normalized
    )
    normalized = re.sub(r"^/api/v1/draft/\d+$", "/api/v1/draft/{year}", normalized)
    normalized = re.sub(r"^/api/v1/teams/\d+", "/api/v1/teams/{team_id}", normalized)
    normalized = re.sub(r"^/api/v1/people/\d+", "/api/v1/people/{person_id}", normalized)
    normalized = re.sub(r"/stats/game/\d+", "/stats/game/{game_pk}", normalized)
    normalized = re.sub(r"^/api/v1/game/\d+", "/api/v1/game/{game_pk}", normalized)
    normalized = re.sub(r"^/api/v1\.1/game/\d+", "/api/v1.1/game/{game_pk}", normalized)
    normalized = re.sub(r"^/api/v1/seasons/\d+", "/api/v1/seasons/{season_id}", normalized)
    normalized = re.sub(r"^/api/v1/venues/\d+", "/api/v1/venues/{venue_id}", normalized)
    normalized = re.sub(
        r"^/api/v1/standings/[^/]+$", "/api/v1/standings/{standings_type}", normalized
    )
    normalized = re.sub(r"^/api/v1/sports/\d+", "/api/v1/sports/{sport_id}", normalized)
    normalized = re.sub(r"^/api/v1/league/\d+", "/api/v1/league/{league_id}", normalized)
    normalized = re.sub(r"^/api/v1/leagues/\d+", "/api/v1/leagues/{league_id}", normalized)
    normalized = re.sub(
        r"^/api/v1/awards/[^/]+/recipients$", "/api/v1/awards/{award_id}/recipients", normalized
    )
    normalized = re.sub(r"^/api/v1/awards/[^/]+$", "/api/v1/awards/{award_id}", normalized)
    return normalized


def _load_example_index() -> dict[tuple[str, str], str]:
    global _EXAMPLE_INDEX
    if _EXAMPLE_INDEX is not None:
        return _EXAMPLE_INDEX
    if not RESPONSE_EXAMPLES_INDEX.exists():
        _EXAMPLE_INDEX = {}
        return _EXAMPLE_INDEX
    with RESPONSE_EXAMPLES_INDEX.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    index: dict[tuple[str, str], str] = {}
    for router in data.get("routers", []):
        for endpoint in router.get("endpoints", []):
            index[(endpoint.get("method"), endpoint.get("path"))] = endpoint.get("file")
    _EXAMPLE_INDEX = index
    return _EXAMPLE_INDEX


def load_response_example_by_endpoint(endpoint_path: str, method: str = "GET") -> dict[str, Any]:
    index = _load_example_index()
    normalized = _normalize_example_path(endpoint_path)
    file_rel = index.get((method, normalized))
    if not file_rel:
        return {}
    example_path = Path(__file__).parent.parent / "docs" / file_rel
    if not example_path.exists():
        return {}
    with example_path.open("r", encoding="utf-8") as handle:
        example = json.load(handle)
    return example.get("response", {})


@pytest.fixture
def client() -> TestClient:
    """Provide a test client for the FastAPI app."""
    client = TestClient(app)
    # Add default API key header for all requests
    client.headers = {"X-API-Key": "test_proxy_key"}
    return client


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient]:
    """Provide an async test client for the FastAPI app."""
    from httpx import ASGITransport

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Add default API key header for all requests
        ac.headers["X-API-Key"] = "test_proxy_key"
        yield ac


@pytest.fixture
def mock_upstream_response() -> dict[str, Any]:
    """Provide a mock upstream API response."""
    return {
        "copyright": "Copyright MLB Advanced Media, LP",
        "data": {"id": 123, "name": "Test Data", "description": "This is test data"},
    }


@pytest.fixture
def mock_upstream_response_stripped() -> dict[str, Any]:
    """Provide a mock upstream API response with copyright stripped."""
    return {"data": {"id": 123, "name": "Test Data", "description": "This is test data"}}


@pytest.fixture
def mock_teams_response() -> dict[str, Any]:
    """Provide a mock teams response."""
    example = load_response_example_by_endpoint("/api/v1/teams")
    return example or {
        "teams": [
            {
                "id": 147,
                "name": "New York Yankees",
                "teamCode": "nya",
                "abbreviation": "NYY",
                "teamName": "Yankees",
                "locationName": "The Bronx",
            }
        ]
    }


@pytest.fixture
def mock_people_response() -> dict[str, Any]:
    """Provide a mock people response."""
    example = load_response_example_by_endpoint("/api/v1/people/search")
    return example or {"people": [{"id": 660271, "fullName": "Aaron Judge", "primaryNumber": "99"}]}


@pytest.fixture
def mock_game_response() -> dict[str, Any]:
    """Provide a mock game response."""
    example = load_response_example_by_endpoint("/api/v1.1/game/776135/feed/live")
    return example or {
        "gamePk": 776135,
        "status": {"abstractGameState": "Final"},
        "teams": {
            "away": {"team": {"id": 147, "name": "New York Yankees"}, "score": 5},
            "home": {"team": {"id": 110, "name": "Baltimore Orioles"}, "score": 3},
        },
    }


@pytest.fixture
def mock_lookup_values() -> dict[str, Any]:
    """Provide mock lookup values response."""
    example = load_response_example_by_endpoint("/api/v1/lookup/values/all")
    return example or {
        "gameTypes": [{"id": "R", "description": "Regular Season"}],
        "positions": [{"code": "1", "name": "Pitcher", "type": "Pitcher", "abbreviation": "P"}],
        "statTypes": [{"name": "hitting", "displayName": "Hitting"}],
    }


@pytest.fixture
def response_example_loader():
    """Load response examples by endpoint path for tests."""

    def _load(endpoint_path: str, method: str = "GET") -> dict[str, Any]:
        return load_response_example_by_endpoint(endpoint_path, method)

    return _load


@pytest.fixture
def respx_mock():
    """Provide respx mock context manager."""
    with respx.mock:
        yield respx


@pytest.fixture
def mock_mlb_api_success(respx_mock, mock_upstream_response):
    """Mock successful MLB API response."""
    route = respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(200, json=mock_upstream_response)
    )
    return route


@pytest.fixture
def mock_mlb_api_error(respx_mock):
    """Mock MLB API error response."""
    route = respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )
    return route


@pytest.fixture
def mock_mlb_api_not_found(respx_mock):
    """Mock MLB API 404 response."""
    route = respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(404, json={"error": "Not Found"})
    )
    return route


@pytest.fixture
def sample_team_ids() -> list[int]:
    """Provide sample team IDs for testing."""
    return [147, 121, 111, 110, 108]  # Yankees, Mets, Red Sox, Orioles, Angels


@pytest.fixture
def sample_person_ids() -> list[int]:
    """Provide sample person IDs for testing."""
    return [660271, 545361, 542438, 665487]  # Aaron Judge, Mike Trout, Gerrit Cole, Juan Soto


@pytest.fixture
def sample_game_pks() -> list[int]:
    """Provide sample game PKs for testing."""
    return [717073, 717074, 717075, 717076, 717077]


@pytest.fixture
def sample_seasons() -> list[int]:
    """Provide sample seasons for testing."""
    return [2024, 2023, 2022, 2021, 2020]


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "contract: Contract tests")
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
