"""Smoke tests for MLB API deployment validation.

These tests are designed to run against a live deployment to verify
that the system is operational. They use real MLB API responses.
"""

import os

import pytest
from fastapi.testclient import TestClient

# Skip smoke tests by default - only run with --smoke flag
pytestmark = pytest.mark.smoke


# Determine if we're testing against live deployment
LIVE_BASE_URL = os.getenv("MLB_API_TEST_URL", None)


@pytest.fixture
def smoke_client():
    """Provide a client for smoke tests."""
    if LIVE_BASE_URL:
        # Use httpx directly for live deployment
        pytest.skip("Live deployment testing not yet implemented")
    else:
        # Use TestClient for local testing
        from main import app

        return TestClient(app)


@pytest.mark.smoke
class TestCriticalEndpoints:
    """Smoke tests for critical endpoints that must always work."""

    def test_teams_endpoint_available(self, client: TestClient):
        """Verify teams endpoint is available."""
        response = client.get("/api/v1/teams")
        assert response.status_code == 200

    def test_people_endpoint_available(self, client: TestClient):
        """Verify people endpoint is available."""
        # Use a well-known player ID
        response = client.get("/api/v1/people/660271")  # Aaron Judge
        assert response.status_code == 200

    def test_games_endpoint_available(self, client: TestClient):
        """Verify games endpoint is available."""
        response = client.get("/api/v1/schedule?sportId=1")
        assert response.status_code == 200

    def test_stats_endpoint_available(self, client: TestClient):
        """Verify stats endpoint is available."""
        response = client.get(
            "/api/v1/stats?stats=season&group=hitting&season=2024&sportId=1&playerPool=ALL"
        )
        assert response.status_code == 200

    def test_standings_endpoint_available(self, client: TestClient):
        """Verify standings endpoint is available."""
        response = client.get(
            "/api/v1/standings?leagueId=103,104&season=2024&standingsTypes=regularSeason"
        )
        assert response.status_code == 200


@pytest.mark.smoke
class TestSystemHealth:
    """Smoke tests for system health checks."""

    def test_api_responds(self, client: TestClient):
        """Verify the API responds to requests."""
        response = client.get("/api/v1/teams")
        assert response.status_code == 200

    def test_json_responses(self, client: TestClient):
        """Verify API returns JSON responses."""
        response = client.get("/api/v1/teams")
        response.json()
        assert response.status_code == 200

    def test_request_id_present(self, client: TestClient):
        """Verify X-Request-ID header is present."""
        response = client.get("/api/v1/teams")
        assert response.status_code == 200
        assert "x-request-id" in response.headers


@pytest.mark.smoke
class TestLookupEndpoints:
    """Smoke tests for lookup/reference endpoints."""

    def test_lookup_values_all(self, client: TestClient):
        """Verify all lookup values endpoint works."""
        response = client.get("/api/v1/lookup/values/all")
        assert response.status_code == 200

    def test_game_types_lookup(self, client: TestClient):
        """Verify game types lookup works."""
        response = client.get("/api/v1/gameTypes")
        assert response.status_code == 200

    def test_sports_lookup(self, client: TestClient):
        """Verify sports lookup works."""
        response = client.get("/api/v1/sports")
        assert response.status_code == 200


@pytest.mark.smoke
@pytest.mark.slow
class TestDataQuality:
    """Smoke tests for basic data quality (slow tests)."""

    def test_teams_returns_data(self, client: TestClient):
        """Verify teams endpoint returns actual team data."""
        response = client.get("/api/v1/teams")
        assert response.status_code == 200
        data = response.json()
        assert "teams" in data

    def test_schedule_returns_data(self, client: TestClient):
        """Verify schedule endpoint returns data for current season."""
        from datetime import datetime

        current_year = datetime.now().year
        response = client.get(
            f"/api/v1/schedule?sportId=1&startDate={current_year}-04-01&endDate={current_year}-04-07"
        )
        assert response.status_code == 200
        data = response.json()
        assert "dates" in data

    def test_standings_returns_data(self, client: TestClient):
        """Verify standings endpoint returns data."""
        from datetime import datetime

        current_year = datetime.now().year
        response = client.get(f"/api/v1/standings?leagueId=103&season={current_year}")
        assert response.status_code == 200
        data = response.json()
        assert "records" in data


@pytest.mark.smoke
class TestCopyrightHandling:
    """Smoke tests for copyright field handling."""

    def test_copyright_stripped(self, client: TestClient):
        """Verify copyright field is stripped from responses."""
        response = client.get("/api/v1/teams")
        assert response.status_code == 200
        data = response.json()
        assert "copyright" not in data


# Configuration for smoke tests
def pytest_configure(config):
    """Configure smoke test markers."""
    config.addinivalue_line("markers", "smoke: mark test as a smoke test for deployment validation")


def pytest_collection_modifyitems(config, items):
    """Skip smoke tests unless --smoke flag is provided."""
    if not config.getoption("--smoke", default=False):
        skip_smoke = pytest.mark.skip(reason="need --smoke option to run")
        for item in items:
            if "smoke" in item.keywords:
                item.add_marker(skip_smoke)
