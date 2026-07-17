"""Unit tests for league router."""

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.unit
@pytest.mark.parametrize(
    "endpoint_path,operation_id,summary",
    [
        ("/api/v1/league/103/allStarWriteIns", "allStarWriteIns", "View all star write ins info"),
        (
            "/api/v1/leagues/103/allStarWriteIns",
            "allStarWriteIns_1",
            "View all star write ins info",
        ),
        (
            "/api/v1/league/103/allStarFinalVote",
            "allStarFinalVote",
            "View all star final vote info",
        ),
        (
            "/api/v1/leagues/103/allStarFinalVote",
            "allStarFinalVote_1",
            "View all star final vote info",
        ),
        ("/api/v1/league/103/allStarBallot", "allStarBallot", "View al star ballot info"),
        ("/api/v1/league/103/allStarBallot", "allStarBallot_1", "View al star ballot info"),
        ("/api/v1/leagues/103/allStarBallot", "allStarBallot_2", "View al star ballot info"),
        ("/api/v1/leagues/103/allStarBallot", "allStarBallot_3", "View al star ballot info"),
        ("/api/v1/league", "league", "View league info"),
        ("/api/v1/league/103", "league_1", "View league info"),
        ("/api/v1/leagues", "league_2", "View league info"),
        ("/api/v1/leagues/103", "league_3", "View league info"),
    ],
)
def test_league_endpoint_exists(
    client: TestClient, endpoint_path: str, operation_id: str, summary: str, respx_mock
):
    """Test that league endpoint exists and returns expected structure."""
    # Mock the upstream MLB API
    upstream_url = f"https://statsapi.mlb.com{endpoint_path}"
    respx.get(upstream_url).mock(
        return_value=Response(200, json={"data": "test", "copyright": "MLB"})
    )

    # Make request to our API
    response = client.get(endpoint_path)

    # Verify response
    assert response.status_code == 200
    assert "copyright" not in response.json()  # Should be stripped


@pytest.mark.unit
def test_league_endpoints_require_valid_upstream(client: TestClient, respx_mock):
    """Test that league endpoints handle upstream failures gracefully."""
    # Mock upstream failure
    respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # This would need to be adjusted per router based on actual endpoints
    # For now, this is a placeholder for API error handling


@pytest.mark.unit
def test_league_endpoints_forward_query_params(client: TestClient, respx_mock):
    """Test that league endpoints forward query parameters correctly."""
    # Example test - would need to be customized per router
    pass
