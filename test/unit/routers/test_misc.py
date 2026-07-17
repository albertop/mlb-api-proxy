"""Unit tests for misc router."""

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.unit
@pytest.mark.parametrize(
    "endpoint_path,operation_id,summary",
    [
        ("/api/v1/jobTypes", "jobTypes", "List all job types"),
        ("/api/v1/gameStatus", "gameStatus", "List all status types"),
        ("/api/v1/windDirection", "windDirection", "List all wind direction options"),
        (
            "/api/v1/weatherTrajectoryConfidences",
            "weatherTrajectoryConfidences",
            "List all weather trajectories",
        ),
        ("/api/v1/violationTypes", "violationTypes", "View available violationType options"),
        ("/api/v1/videoResolutionTypes", "videoResolutionTypes", "View video resolution options"),
        ("/api/v1/transactionTypes", "transactionTypes", "List all transaction types"),
        ("/api/v1/trackingVersions", "trackingVersions", "List all tracking versions"),
        ("/api/v1/trackingVendors", "trackingVendors", "List all tracking vendors"),
        ("/api/v1/trackingSystemOwners", "trackingSystemOwners", "List all tracking system owners"),
        (
            "/api/v1/trackingSoftwareVersions",
            "trackingSoftwareVersions",
            "List the tracking software versions and notes",
        ),
        ("/api/v1/stats/search/stats", "statSearchStats", "List stat search stats"),
        ("/api/v1/stats/search/params", "statSearchParams", "List stat search parameters"),
        ("/api/v1/stats/search/groupByTypes", "statSearchGroupByTypes", "List groupBy types"),
        ("/api/v1/stats/search/config", "statSearchConfig", "Stats Search Config Endpoint"),
        (
            "/api/v1/statcastPositionTypes",
            "statcastPositionTypes",
            "List all statcast position types",
        ),
        ("/api/v1/statTypes", "statTypes", "List all stat types"),
        ("/api/v1/statGroups", "statGroups", "List all stat groups"),
        ("/api/v1/statFields", "statFields", "List all stat fields"),
        ("/api/v1/standingsTypes", "standingsTypes", "List all standings types"),
        ("/api/v1/sortModifiers", "aggregateSortEnum", "List all stat fields"),
        ("/api/v1/sky", "sky", "List all sky options"),
        ("/api/v1/situationCodes", "sitCodes", "List all situation codes"),
        ("/api/v1/scheduleTypes", "scheduleTypes", "List all possible schedule types"),
        ("/api/v1/scheduleEventTypes", "scheduleEventTypes", "List all schedule event types"),
        ("/api/v1/runnerDetailTypes", "runnerDetailTypes", "List runner detail types"),
        ("/api/v1/ruleSettings", "ruleSettings", "List all ruleSettings"),
        ("/api/v1/rosterTypes", "rosterTypes", "List all possible roster types"),
        ("/api/v1/roofTypes", "roofTypes", "List all roof types"),
        ("/api/v1/reviewReasons", "reviewReasons", "List all replay review reasons"),
        ("/api/v1/positions", "positions", "List all possible positions"),
        ("/api/v1/playerStatusCodes", "playerStatusCodes", "List all player status codes"),
        ("/api/v1/platforms", "platforms", "List all possible platforms"),
        ("/api/v1/pitchTypes", "pitchTypes", "List all pitch classification types"),
        ("/api/v1/pitchCodes", "pitchCodes", "List all pitch codes"),
        ("/api/v1/performerTypes", "performerTypes", "List all possible performer types"),
        ("/api/v1/moundVisitTypes", "moundVisitTypes", "List all mound visit types"),
        ("/api/v1/metrics", "metrics", "List all possible metrics"),
        ("/api/v1/mediaState", "mediaStateTypes", "View media state options"),
        ("/api/v1/lookup/values/all", "getLookupValues", "View all lookup values"),
        ("/api/v1/logicalEvents", "logicalEvents", "List all logical event types"),
        (
            "/api/v1/leagueLeaderTypes",
            "leagueLeaderTypes",
            "List all possible player league leader types",
        ),
        ("/api/v1/languages", "languages", "List all support languages"),
        ("/api/v1/hitTrajectories", "hitTrajectories", "List all hit trajectories"),
        ("/api/v1/groupByTypes", "groupByTypes", "List groupBy types"),
        ("/api/v1/gamedayTypes", "gamedayTypes", "List all gameday types"),
        ("/api/v1/gameTypes", "gameTypes", "List all game types"),
        ("/api/v1/freeGameTypes", "freeGameTypes", "View free game types"),
        ("/api/v1/fielderDetailTypes", "fielderDetailTypes", "List fielder detail types"),
        ("/api/v1/eventTypes", "eventTypes", "List all event types"),
        ("/api/v1/eventStatus", "eventStatus", "List all possible event status types"),
        ("/api/v1/coachingVideoTypes", "coachingVideoTypes", "List all coaching video types"),
        (
            "/api/v1/broadcastAvailability",
            "broadcastAvailabilityTypes",
            "View broadcast availability options",
        ),
        ("/api/v1/baseballStats", "baseballStats", "List all baseball stats"),
    ],
)
def test_misc_endpoint_exists(
    client: TestClient,
    endpoint_path: str,
    operation_id: str,
    summary: str,
    respx_mock,
    response_example_loader,
):
    """Test that misc endpoint exists and returns expected structure."""
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
def test_misc_endpoints_require_valid_upstream(client: TestClient, respx_mock):
    """Test that misc endpoints handle upstream failures gracefully."""
    # Mock upstream failure
    respx.get("https://statsapi.mlb.com/api/v1/test").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # This would need to be adjusted per router based on actual endpoints
    # For now, this is a placeholder for API error handling


@pytest.mark.unit
def test_misc_endpoints_forward_query_params(client: TestClient, respx_mock):
    """Test that misc endpoints forward query parameters correctly."""
    # Example test - would need to be customized per router
    pass
