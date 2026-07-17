"""Unit tests for games router."""

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.unit
@pytest.mark.parametrize(
    "endpoint_path,operation_id,summary",
    [
        ("/api/v1/game/776135/playByPlay", "playByPlay", "Get game play By Play"),
        ("/api/v1/game/776135/linescore", "linescore", "Get game linescore"),
        ("/api/v1/game/776135/content", "content", "Retrieve all content for a game."),
        ("/api/v1/game/776135/boxscore", "boxscore", "Get game boxscore."),
        ("/api/v1/game/776135/withMetrics", "getGameWithMetrics", "Get game info with metrics"),
        (
            "/api/v1/game/776135/winProbability",
            "getWinProbability",
            "Get the win probability for this game",
        ),
        (
            "/api/v1/game/776135/contextMetrics",
            "getGameContextMetrics",
            "Get the context metrics for this game based on its current state",
        ),
        ("/api/v1/game/changes", "currentGameStats_1", "View a game change log"),
        ("/api/v1.1/game/776135/feed/live", "liveGameV1", "Get live game status."),
        (
            "/api/v1.1/game/776135/feed/live/timestamps",
            "liveTimestampv11",
            "Retrieve all of the play timestamps for a game.",
        ),
        (
            "/api/v1.1/game/776135/feed/live/diffPatch",
            "liveGameDiffPatchV1",
            "Get live game status diffPatch.",
        ),
    ],
)
def test_games_endpoint_exists(
    client: TestClient, endpoint_path: str, operation_id: str, summary: str, respx_mock
):
    """Test that games endpoint exists and returns expected structure."""
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
def test_games_endpoints_require_valid_upstream(client: TestClient, respx_mock):
    """Test that games endpoints handle upstream failures gracefully."""
    # Mock upstream failure
    respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # This would need to be adjusted per router based on actual endpoints
    # For now, this is a placeholder for API error handling


@pytest.mark.unit
def test_games_endpoints_forward_query_params(client: TestClient, respx_mock):
    """Test that games endpoints forward query parameters correctly."""
    # Example test - would need to be customized per router
    pass
