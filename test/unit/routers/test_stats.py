"""Unit tests for stats router."""

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.unit
@pytest.mark.parametrize(
    "endpoint_path,operation_id,summary",
    [
        ("/api/v1/stats", "stats_2", "View stats"),
        ("/api/v1/stats/leaders", "leaders_2", "Get leaders for a statistic"),
        ("/api/v1/stats/grouped", "groupedStats", "View grouped stats"),
    ],
)
def test_stats_endpoint_exists(
    client: TestClient,
    endpoint_path: str,
    operation_id: str,
    summary: str,
    respx_mock,
    response_example_loader,
):
    """Test that stats endpoint exists and returns expected structure."""
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
def test_stats_endpoints_require_valid_upstream(client: TestClient, respx_mock):
    """Test that stats endpoints handle upstream failures gracefully."""
    # Mock upstream failure
    respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # This would need to be adjusted per router based on actual endpoints
    # For now, this is a placeholder for API error handling


@pytest.mark.unit
def test_stats_endpoints_forward_query_params(client: TestClient, respx_mock):
    """Test that stats endpoints forward query parameters correctly."""
    # Example test - would need to be customized per router
    pass
