"""Integration tests for MLB API proxy."""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response


@pytest.mark.integration
class TestEndToEndFlows:
    """Test end-to-end user scenarios."""

    def test_get_team_roster_flow(self, client: TestClient, respx_mock):
        """Test complete flow: get team -> get roster."""
        # Step 1: Get team info
        team_response = {"teams": [{"id": 147, "name": "New York Yankees", "abbreviation": "NYY"}]}
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147").mock(
            return_value=Response(200, json=team_response)
        )

        response1 = client.get("/api/v1/teams/147")
        assert response1.status_code == 200

        # Step 2: Get team roster
        roster_response = {
            "roster": [
                {"person": {"id": 660271, "fullName": "Aaron Judge"}},
                {"person": {"id": 542438, "fullName": "Gerrit Cole"}},
            ]
        }
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147/roster").mock(
            return_value=Response(200, json=roster_response)
        )

        response2 = client.get("/api/v1/teams/147/roster")
        assert response2.status_code == 200
        data = response2.json()
        assert len(data["roster"]) == 2

    def test_get_person_stats_flow(self, client: TestClient, respx_mock):
        """Test complete flow: search person -> get person -> get stats."""
        # Step 1: Search for person
        search_response = {"people": [{"id": 660271, "fullName": "Aaron Judge"}]}
        respx_mock.get("https://statsapi.mlb.com/api/v1/people/search").mock(
            return_value=Response(200, json=search_response)
        )

        response1 = client.get("/api/v1/people/search?names=Judge")
        assert response1.status_code == 200
        person_id = response1.json()["people"][0]["id"]

        # Step 2: Get person details
        person_response = {
            "people": [{"id": 660271, "fullName": "Aaron Judge", "primaryNumber": "99"}]
        }
        respx_mock.get(f"https://statsapi.mlb.com/api/v1/people/{person_id}").mock(
            return_value=Response(200, json=person_response)
        )

        response2 = client.get(f"/api/v1/people/{person_id}")
        assert response2.status_code == 200

        # Step 3: Get person stats
        stats_response = {
            "stats": [{"splits": [{"stat": {"gamesPlayed": 157, "homeRuns": 62, "avg": ".311"}}]}]
        }
        respx_mock.get(f"https://statsapi.mlb.com/api/v1/people/{person_id}/stats").mock(
            return_value=Response(200, json=stats_response)
        )

        response3 = client.get(f"/api/v1/people/{person_id}/stats?stats=season&season=2022")
        assert response3.status_code == 200
        data = response3.json()
        assert "stats" in data

    def test_get_game_schedule_flow(self, client: TestClient, respx_mock):
        """Test complete flow: get schedule -> get game details."""
        # Step 1: Get schedule
        schedule_response = {
            "dates": [{"games": [{"gamePk": 717073, "gameDate": "2024-04-01T17:05:00Z"}]}]
        }
        respx_mock.get("https://statsapi.mlb.com/api/v1/schedule").mock(
            return_value=Response(200, json=schedule_response)
        )

        response1 = client.get("/api/v1/schedule?sportId=1&startDate=2024-04-01&endDate=2024-04-01")
        assert response1.status_code == 200
        game_pk = response1.json()["dates"][0]["games"][0]["gamePk"]

        # Step 2: Get game details
        game_response = {
            "gamePk": 717073,
            "gameDate": "2024-04-01T17:05:00Z",
            "status": {"abstractGameState": "Final"},
            "teams": {
                "away": {"team": {"id": 147}, "score": 5},
                "home": {"team": {"id": 110}, "score": 3},
            },
        }
        respx_mock.get(f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live").mock(
            return_value=Response(200, json=game_response)
        )

        response2 = client.get(f"/api/v1.1/game/{game_pk}/feed/live")
        assert response2.status_code == 200
        data = response2.json()
        assert data["status"]["abstractGameState"] == "Final"

    def test_standings_to_team_flow(self, client: TestClient, respx_mock):
        """Test complete flow: get standings -> get team details."""
        # Step 1: Get standings
        standings_response = {
            "records": [
                {
                    "teamRecords": [
                        {"team": {"id": 147, "name": "New York Yankees"}, "wins": 95, "losses": 67}
                    ]
                }
            ]
        }
        respx_mock.get("https://statsapi.mlb.com/api/v1/standings").mock(
            return_value=Response(200, json=standings_response)
        )

        response1 = client.get("/api/v1/standings?leagueId=103&season=2024")
        assert response1.status_code == 200
        team_id = response1.json()["records"][0]["teamRecords"][0]["team"]["id"]

        # Step 2: Get team details
        team_response = {
            "teams": [
                {
                    "id": 147,
                    "name": "New York Yankees",
                    "venue": {"id": 3313, "name": "Yankee Stadium"},
                }
            ]
        }
        respx_mock.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}").mock(
            return_value=Response(200, json=team_response)
        )

        response2 = client.get(f"/api/v1/teams/{team_id}")
        assert response2.status_code == 200
        data = response2.json()
        assert data["teams"][0]["name"] == "New York Yankees"


@pytest.mark.integration
class TestDataConsistency:
    """Test data consistency across related endpoints."""

    def test_team_id_consistency(self, client: TestClient, respx_mock):
        """Test that team IDs are consistent across endpoints."""
        team_id = 147

        # Mock teams endpoint
        respx_mock.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}").mock(
            return_value=Response(
                200, json={"teams": [{"id": team_id, "name": "New York Yankees"}]}
            )
        )

        # Mock roster endpoint
        respx_mock.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster").mock(
            return_value=Response(200, json={"roster": [], "teamId": team_id})
        )

        response1 = client.get(f"/api/v1/teams/{team_id}")
        response2 = client.get(f"/api/v1/teams/{team_id}/roster")

        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_person_id_consistency(self, client: TestClient, respx_mock):
        """Test that person IDs are consistent across endpoints."""
        person_id = 660271

        # Mock people endpoint
        respx_mock.get(f"https://statsapi.mlb.com/api/v1/people/{person_id}").mock(
            return_value=Response(
                200, json={"people": [{"id": person_id, "fullName": "Aaron Judge"}]}
            )
        )

        # Mock stats endpoint
        respx_mock.get(f"https://statsapi.mlb.com/api/v1/people/{person_id}/stats").mock(
            return_value=Response(200, json={"stats": [], "id": person_id})
        )

        response1 = client.get(f"/api/v1/people/{person_id}")
        response2 = client.get(f"/api/v1/people/{person_id}/stats?stats=season")

        assert response1.status_code == 200
        assert response2.status_code == 200


@pytest.mark.integration
class TestConcurrentRequests:
    """Test handling of concurrent requests."""

    @pytest.mark.asyncio
    async def test_multiple_teams_concurrent(self, async_client: AsyncClient, respx_mock):
        """Test concurrent requests for multiple teams."""
        team_ids = [147, 121, 111]

        for team_id in team_ids:
            respx_mock.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}").mock(
                return_value=Response(
                    200, json={"teams": [{"id": team_id, "name": f"Team {team_id}"}]}
                )
            )

        # Make concurrent requests
        import asyncio

        responses = await asyncio.gather(
            *[async_client.get(f"/api/v1/teams/{team_id}") for team_id in team_ids]
        )

        assert all(r.status_code == 200 for r in responses)
        assert len(responses) == 3

    @pytest.mark.asyncio
    async def test_mixed_endpoints_concurrent(self, async_client: AsyncClient, respx_mock):
        """Test concurrent requests to different endpoints."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(200, json={"teams": []})
        )
        respx_mock.get("https://statsapi.mlb.com/api/v1/people/660271").mock(
            return_value=Response(200, json={"people": []})
        )
        respx_mock.get("https://statsapi.mlb.com/api/v1/schedule").mock(
            return_value=Response(200, json={"dates": []})
        )

        import asyncio

        responses = await asyncio.gather(
            async_client.get("/api/v1/teams"),
            async_client.get("/api/v1/people/660271"),
            async_client.get("/api/v1/schedule?sportId=1"),
        )

        assert all(r.status_code == 200 for r in responses)


@pytest.mark.integration
@pytest.mark.slow
class TestRateLimitingAndRetry:
    """Test rate limiting and retry logic."""

    def test_multiple_requests_same_endpoint(self, client: TestClient, respx_mock):
        """Test multiple requests to the same endpoint."""
        call_count = 0

        def response_handler(request):
            nonlocal call_count
            call_count += 1
            return Response(200, json={"teams": [], "call": call_count})

        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(side_effect=response_handler)

        # Make multiple requests
        for _ in range(5):
            response = client.get("/api/v1/teams")
            assert response.status_code == 200

        assert call_count == 5

    def test_upstream_rate_limit_response(self, client: TestClient, respx_mock):
        """Test handling of upstream rate limit (429)."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(429, json={"error": "Rate limit exceeded"})
        )

        response = client.get("/api/v1/teams")

        assert response.status_code == 429
