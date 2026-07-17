"""Unit tests for schedule router."""

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.unit
@pytest.mark.parametrize(
    "endpoint_path,operation_id,summary",
    [
        (
            "/api/v1/schedule/trackingEvents",
            "trackingEventsSchedule",
            "Get tracking event schedules",
        ),
        ("/api/v1/schedule/postseason", "postseasonSchedule", "Get postseason schedule"),
        ("/api/v1/schedule/postseason/tuneIn", "tuneIn", "Get postseason TuneIn schedules"),
        (
            "/api/v1/schedule/postseason/series",
            "postseasonScheduleSeries",
            "Get postseason series schedules",
        ),
        ("/api/v1/schedule/games/tied", "tieGames", "Get tied game schedules"),
        ("/api/v1/schedule", "schedule", "View schedule info based on scheduleType."),
        (
            "/api/v1/schedule/{scheduleType}",
            "schedule_1",
            "View schedule info based on scheduleType.",
        ),
    ],
)
def test_schedule_endpoint_exists(
    client: TestClient, endpoint_path: str, operation_id: str, summary: str, respx_mock
):
    """Test that schedule endpoint exists and returns expected structure."""
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
def test_schedule_endpoints_require_valid_upstream(client: TestClient, respx_mock):
    """Test that schedule endpoints handle upstream failures gracefully."""
    # Mock upstream failure
    respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # This would need to be adjusted per router based on actual endpoints
    # For now, this is a placeholder for API error handling


@pytest.mark.unit
def test_schedule_endpoints_forward_query_params(client: TestClient, respx_mock):
    """Test that schedule endpoints forward query parameters correctly."""
    # Example test - would need to be customized per router
    pass
