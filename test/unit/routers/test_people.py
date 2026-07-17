"""Unit tests for people router."""

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.unit
@pytest.mark.parametrize(
    "endpoint_path,operation_id,summary",
    [
        ("/api/v1/people/123/stats", "stats_3", "View a players stats"),
        ("/api/v1/people/123/stats/game/776135", "playerGameStats", "View a player's game stats"),
        ("/api/v1/people/123/awards", "award", "View a player's awards"),
        ("/api/v1/people/123", "person", "View a player"),
        ("/api/v1/people/search", "search", "Search for a player by name"),
        ("/api/v1/people/freeAgents", "freeAgents", "Get free agents"),
        ("/api/v1/people/changes", "currentGameStats", "View a player's change log"),
    ],
)
def test_people_endpoint_exists(
    client: TestClient,
    endpoint_path: str,
    operation_id: str,
    summary: str,
    respx_mock,
    response_example_loader,
):
    """Test that people endpoint exists and returns expected structure."""
    # Mock the upstream MLB API
    upstream_url = f"https://statsapi.mlb.com{endpoint_path}"
    example_payload = response_example_loader(endpoint_path)
    respx.get(upstream_url).mock(
        return_value=Response(200, json=example_payload or {"data": "test", "copyright": "MLB"})
    )

    # Make request to our API
    response = client.get(endpoint_path)

    # Verify response
    assert response.status_code == 200
    assert "copyright" not in response.json()  # Should be stripped


@pytest.mark.unit
def test_people_endpoints_require_valid_upstream(client: TestClient, respx_mock):
    """Test that people endpoints handle upstream failures gracefully."""
    # Mock upstream failure
    respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # This would need to be adjusted per router based on actual endpoints
    # For now, this is a placeholder for API error handling


@pytest.mark.unit
def test_people_endpoints_forward_query_params(client: TestClient, respx_mock):
    """Test that people endpoints forward query parameters correctly."""
    # Example test - would need to be customized per router
    pass
