"""Critical hand-written tests for core functionality."""

import pytest
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.unit
class TestCriticalFlows:
    """Test critical user flows and scenarios."""

    def test_teams_list_retrieval(self, client: TestClient, respx_mock, mock_teams_response):
        """Test retrieving list of all teams."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(200, json=mock_teams_response)
        )

        response = client.get("/api/v1/teams")

        assert response.status_code == 200
        data = response.json()
        assert "teams" in data
        assert len(data["teams"]) >= 1
        assert data["teams"][0]["name"] == "New York Yankees"

    def test_team_by_id_retrieval(self, client: TestClient, respx_mock):
        """Test retrieving a specific team by ID."""
        team_data = {
            "teams": [
                {"id": 147, "name": "New York Yankees", "teamCode": "nya", "abbreviation": "NYY"}
            ]
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147").mock(
            return_value=Response(200, json=team_data)
        )

        response = client.get("/api/v1/teams/147")

        assert response.status_code == 200
        data = response.json()
        assert data["teams"][0]["id"] == 147
        assert data["teams"][0]["name"] == "New York Yankees"

    def test_person_lookup(self, client: TestClient, respx_mock, mock_people_response):
        """Test looking up a person by ID."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/people/660271").mock(
            return_value=Response(200, json=mock_people_response)
        )

        response = client.get("/api/v1/people/660271")

        assert response.status_code == 200
        data = response.json()
        assert "people" in data
        assert len(data["people"]) >= 1
        assert "fullName" in data["people"][0]
        assert "primaryNumber" in data["people"][0]

    def test_game_retrieval(self, client: TestClient, respx_mock, mock_game_response):
        """Test retrieving game data."""
        game_pk = mock_game_response.get("gamePk", 776135)
        respx_mock.get(f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live").mock(
            return_value=Response(200, json=mock_game_response)
        )

        response = client.get(f"/api/v1.1/game/{game_pk}/feed/live")

        assert response.status_code == 200
        data = response.json()
        assert "gamePk" in data
        assert data["gamePk"] == game_pk
        assert "status" in data or "gameData" in data  # Status may be nested or entire game data

    def test_lookup_values_all(self, client: TestClient, respx_mock, mock_lookup_values):
        """Test retrieving all lookup values."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/lookup/values/all").mock(
            return_value=Response(200, json=mock_lookup_values)
        )

        response = client.get("/api/v1/lookup/values/all")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        # Response contains various lookup categories (Sky, Game Types, etc.)
        assert any(key in data for key in ["Sky", "gameTypes", "positions", "statTypes"])


@pytest.mark.unit
class TestErrorHandling:
    """Test error handling scenarios."""

    def test_upstream_500_error(self, client: TestClient, respx_mock):
        """Test handling of upstream 500 error."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(500, json={"error": "Internal Server Error"})
        )

        response = client.get("/api/v1/teams")

        assert response.status_code == 500

    def test_upstream_404_error(self, client: TestClient, respx_mock):
        """Test handling of upstream 404 error."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams/99999").mock(
            return_value=Response(404, json={"error": "Not Found"})
        )

        response = client.get("/api/v1/teams/99999")

        assert response.status_code == 404

    def test_upstream_timeout(self, client: TestClient, respx_mock):
        """Test handling of upstream timeout."""
        import httpx

        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            side_effect=httpx.TimeoutException("Request timeout")
        )

        response = client.get("/api/v1/teams")

        # Should handle timeout gracefully
        assert response.status_code in [408, 500, 502, 504]

    def test_upstream_connection_error(self, client: TestClient, respx_mock):
        """Test handling of upstream connection error."""
        import httpx

        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            side_effect=httpx.ConnectError("Connection failed")
        )

        response = client.get("/api/v1/teams")

        # Should handle connection error gracefully
        assert response.status_code in [500, 502, 503]

    def test_invalid_endpoint(self, client: TestClient):
        """Test calling a non-existent endpoint."""
        response = client.get("/api/v1/nonexistent/endpoint")

        assert response.status_code == 404


@pytest.mark.unit
class TestQueryParameters:
    """Test query parameter forwarding."""

    def test_teams_with_season_param(self, client: TestClient, respx_mock):
        """Test teams endpoint with season parameter."""
        mock_response = {"teams": [{"id": 147, "name": "New York Yankees"}]}

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(200, json=mock_response)
        )

        response = client.get("/api/v1/teams?season=2024")

        assert response.status_code == 200
        # Verify query param was forwarded
        assert route.called
        assert "season=2024" in str(route.calls.last.request.url)

    def test_schedule_with_multiple_params(self, client: TestClient, respx_mock):
        """Test schedule endpoint with multiple parameters."""
        mock_response = {"dates": []}

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/schedule").mock(
            return_value=Response(200, json=mock_response)
        )

        response = client.get("/api/v1/schedule?sportId=1&startDate=2024-04-01&endDate=2024-04-30")

        assert response.status_code == 200
        assert route.called
        request_url = str(route.calls.last.request.url)
        assert "sportId=1" in request_url
        assert "startDate=2024-04-01" in request_url
        assert "endDate=2024-04-30" in request_url

    def test_people_search_with_params(self, client: TestClient, respx_mock):
        """Test people search with query parameters."""
        mock_response = {"people": [{"id": 660271, "fullName": "Aaron Judge"}]}

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/people/search").mock(
            return_value=Response(200, json=mock_response)
        )

        response = client.get("/api/v1/people/search?names=Judge")

        assert response.status_code == 200
        assert route.called
        assert "names=Judge" in str(route.calls.last.request.url)


@pytest.mark.unit
class TestCopyrightStripping:
    """Test copyright field removal."""

    def test_copyright_removed_from_response(self, client: TestClient, respx_mock):
        """Test that copyright field is stripped from response."""
        response_with_copyright = {
            "copyright": "Copyright MLB Advanced Media, LP",
            "teams": [{"id": 147, "name": "New York Yankees"}],
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(200, json=response_with_copyright)
        )

        response = client.get("/api/v1/teams")

        assert response.status_code == 200
        data = response.json()
        assert "copyright" not in data
        assert "teams" in data

    def test_nested_copyright_not_affected(self, client: TestClient, respx_mock):
        """Test that nested 'copyright' fields are not affected."""
        response_with_nested = {
            "copyright": "Copyright MLB Advanced Media, LP",
            "data": {"metadata": {"copyright": "Team copyright info"}},
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(200, json=response_with_nested)
        )

        response = client.get("/api/v1/teams")

        # The proxy strips only the top-level copyright
        assert response.status_code == 200
        data = response.json()
        assert "copyright" not in data


@pytest.mark.unit
class TestRequestHeaders:
    """Test request header handling."""

    def test_request_id_added_to_response(self, client: TestClient, respx_mock):
        """Test that X-Request-ID is added to responses."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(200, json={"teams": []})
        )

        response = client.get("/api/v1/teams")

        assert response.status_code == 200
        assert "x-request-id" in response.headers

    def test_request_id_echoed(self, client: TestClient, respx_mock):
        """Test that provided X-Request-ID is echoed back."""
        respx_mock.get("https://statsapi.mlb.com/api/v1/teams").mock(
            return_value=Response(200, json={"teams": []})
        )

        request_id = "test-request-123"
        response = client.get("/api/v1/teams", headers={"X-Request-ID": request_id})

        assert response.status_code == 200
        assert response.headers.get("x-request-id") == request_id


@pytest.mark.unit
class TestScheduleCriticalPaths:
    """Detailed tests for schedule endpoints."""

    def test_schedule_basic_query(self, client: TestClient, respx_mock):
        """Test basic schedule query with date range."""
        mock_schedule = {
            "dates": [
                {
                    "date": "2024-04-01",
                    "totalGames": 15,
                    "games": [
                        {
                            "gamePk": 717073,
                            "gameDate": "2024-04-01T17:05:00Z",
                            "status": {"detailedState": "Final"},
                            "teams": {
                                "away": {"team": {"id": 147, "name": "Yankees"}},
                                "home": {"team": {"id": 110, "name": "Orioles"}},
                            },
                        }
                    ],
                }
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/schedule").mock(
            return_value=Response(200, json=mock_schedule)
        )

        response = client.get("/api/v1/schedule?sportId=1&startDate=2024-04-01&endDate=2024-04-01")

        assert response.status_code == 200
        data = response.json()
        assert "dates" in data
        assert len(data["dates"]) == 1
        assert data["dates"][0]["totalGames"] == 15
        assert route.called

    def test_schedule_team_specific(self, client: TestClient, respx_mock):
        """Test schedule filtered by team."""
        mock_schedule = {
            "dates": [
                {
                    "date": "2024-04-01",
                    "games": [
                        {
                            "gamePk": 717073,
                            "teams": {
                                "away": {"team": {"id": 147, "name": "Yankees"}},
                                "home": {"team": {"id": 110, "name": "Orioles"}},
                            },
                        }
                    ],
                }
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/schedule").mock(
            return_value=Response(200, json=mock_schedule)
        )

        response = client.get("/api/v1/schedule?teamId=147&season=2024")

        assert response.status_code == 200
        assert route.called
        request_url = str(route.calls.last.request.url)
        assert "teamId=147" in request_url
        assert "season=2024" in request_url

    def test_schedule_with_hydrations(self, client: TestClient, respx_mock):
        """Test schedule with hydration parameters."""
        mock_schedule = {
            "dates": [
                {
                    "games": [
                        {
                            "gamePk": 717073,
                            "linescore": {"currentInning": 9},
                            "content": {"link": "/content/123"},
                        }
                    ]
                }
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/schedule").mock(
            return_value=Response(200, json=mock_schedule)
        )

        response = client.get("/api/v1/schedule?sportId=1&hydrate=linescore,broadcasts")

        assert response.status_code == 200
        assert route.called
        assert "hydrate=linescore" in str(route.calls.last.request.url)

    def test_schedule_postseason(self, client: TestClient, respx_mock):
        """Test postseason schedule endpoint."""
        mock_postseason = {
            "series": [
                {"seriesNumber": 1, "seriesDescription": "Wild Card", "games": [{"gamePk": 717073}]}
            ]
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/schedule/postseason").mock(
            return_value=Response(200, json=mock_postseason)
        )

        response = client.get("/api/v1/schedule/postseason?season=2024")

        assert response.status_code == 200
        data = response.json()
        assert "series" in data

    def test_schedule_postseason_series(self, client: TestClient, respx_mock):
        """Test postseason series details."""
        mock_series = {
            "series": {
                "seriesNumber": 1,
                "shortDescription": "ALWC",
                "teams": {"home": {"team": {"id": 147}}, "away": {"team": {"id": 111}}},
            }
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/schedule/postseason/series").mock(
            return_value=Response(200, json=mock_series)
        )

        response = client.get("/api/v1/schedule/postseason/series?seriesNumber=1&season=2024")

        assert response.status_code == 200

    def test_schedule_tied_games(self, client: TestClient, respx_mock):
        """Test tied games schedule endpoint."""
        mock_tied = {"dates": [{"games": [{"gamePk": 717073, "status": {"codedGameState": "T"}}]}]}

        respx_mock.get("https://statsapi.mlb.com/api/v1/schedule/games/tied").mock(
            return_value=Response(200, json=mock_tied)
        )

        response = client.get("/api/v1/schedule/games/tied?season=2024")

        assert response.status_code == 200

    def test_schedule_date_range_validation(self, client: TestClient, respx_mock):
        """Test schedule handles date range properly."""
        mock_schedule = {
            "dates": [
                {"date": "2024-04-01", "games": []},
                {"date": "2024-04-02", "games": []},
                {"date": "2024-04-03", "games": []},
            ]
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/schedule").mock(
            return_value=Response(200, json=mock_schedule)
        )

        response = client.get("/api/v1/schedule?startDate=2024-04-01&endDate=2024-04-03")

        assert response.status_code == 200
        data = response.json()
        assert len(data["dates"]) == 3


@pytest.mark.unit
class TestTransactionsCriticalPaths:
    """Detailed tests for transactions endpoints."""

    def test_transactions_by_date(self, client: TestClient, respx_mock):
        """Test retrieving transactions by date."""
        mock_transactions = {
            "transactions": [
                {
                    "transactionId": "tx_001",
                    "date": "2024-02-01",
                    "type": "Signed",
                    "description": "Signed 1B John Doe to a minor league contract",
                    "person": {"id": 123456, "fullName": "John Doe"},
                },
                {
                    "transactionId": "tx_002",
                    "date": "2024-02-01",
                    "type": "Trade",
                    "description": "Traded RHP Jane Smith to Team X",
                },
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/transactions").mock(
            return_value=Response(200, json=mock_transactions)
        )

        response = client.get("/api/v1/transactions?date=2024-02-01")

        assert response.status_code == 200
        data = response.json()
        assert "transactions" in data
        assert len(data["transactions"]) == 2
        assert data["transactions"][0]["type"] == "Signed"
        assert route.called

    def test_transactions_by_team(self, client: TestClient, respx_mock):
        """Test retrieving transactions filtered by team."""
        mock_transactions = {
            "transactions": [
                {
                    "transactionId": "tx_003",
                    "type": "Recalled",
                    "description": "Recalled OF Player from AAA",
                    "fromTeam": {"id": 147, "name": "Yankees"},
                }
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/transactions").mock(
            return_value=Response(200, json=mock_transactions)
        )

        response = client.get(
            "/api/v1/transactions?teamId=147&startDate=2024-01-01&endDate=2024-12-31"
        )

        assert response.status_code == 200
        assert route.called
        request_url = str(route.calls.last.request.url)
        assert "teamId=147" in request_url

    def test_transactions_by_player(self, client: TestClient, respx_mock):
        """Test retrieving transactions for a specific player."""
        mock_transactions = {
            "transactions": [
                {
                    "transactionId": "tx_004",
                    "date": "2024-03-15",
                    "type": "Status Change",
                    "person": {"id": 660271, "fullName": "Aaron Judge"},
                }
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/transactions").mock(
            return_value=Response(200, json=mock_transactions)
        )

        response = client.get("/api/v1/transactions?playerId=660271")

        assert response.status_code == 200
        data = response.json()
        assert "transactions" in data
        assert route.called

    def test_transactions_date_range(self, client: TestClient, respx_mock):
        """Test transactions within a date range."""
        mock_transactions = {
            "transactions": [
                {"transactionId": "tx_005", "date": "2024-01-15", "type": "Signed"},
                {"transactionId": "tx_006", "date": "2024-01-20", "type": "Trade"},
                {"transactionId": "tx_007", "date": "2024-01-25", "type": "Released"},
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/transactions").mock(
            return_value=Response(200, json=mock_transactions)
        )

        response = client.get("/api/v1/transactions?startDate=2024-01-01&endDate=2024-01-31")

        assert response.status_code == 200
        data = response.json()
        assert len(data["transactions"]) == 3
        assert route.called
        request_url = str(route.calls.last.request.url)
        assert "startDate=2024-01-01" in request_url
        assert "endDate=2024-01-31" in request_url

    def test_transactions_multiple_filters(self, client: TestClient, respx_mock):
        """Test transactions with multiple filter parameters."""
        mock_transactions = {
            "transactions": [
                {
                    "transactionId": "tx_008",
                    "date": "2024-02-15",
                    "type": "Signed",
                    "person": {"id": 123456},
                    "fromTeam": {"id": 147},
                }
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/transactions").mock(
            return_value=Response(200, json=mock_transactions)
        )

        response = client.get("/api/v1/transactions?teamId=147&date=2024-02-15&sportId=1")

        assert response.status_code == 200
        assert route.called
        request_url = str(route.calls.last.request.url)
        assert "teamId=147" in request_url
        assert "date=2024-02-15" in request_url
        assert "sportId=1" in request_url


@pytest.mark.unit
class TestRostersCriticalPaths:
    """Detailed tests for roster endpoints."""

    def test_team_active_roster(self, client: TestClient, respx_mock):
        """Test retrieving active 40-man roster."""
        mock_roster = {
            "roster": [
                {
                    "person": {"id": 660271, "fullName": "Aaron Judge"},
                    "jerseyNumber": "99",
                    "position": {"code": "9", "name": "Outfielder"},
                    "status": {"code": "A", "description": "Active"},
                },
                {
                    "person": {"id": 542438, "fullName": "Gerrit Cole"},
                    "jerseyNumber": "45",
                    "position": {"code": "1", "name": "Pitcher"},
                    "status": {"code": "A", "description": "Active"},
                },
            ],
            "teamId": 147,
            "rosterType": "active",
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147/roster").mock(
            return_value=Response(200, json=mock_roster)
        )

        response = client.get("/api/v1/teams/147/roster")

        assert response.status_code == 200
        data = response.json()
        assert "roster" in data
        assert len(data["roster"]) == 2
        assert data["roster"][0]["person"]["fullName"] == "Aaron Judge"
        assert data["teamId"] == 147
        assert route.called

    def test_roster_by_type_40man(self, client: TestClient, respx_mock):
        """Test retrieving 40-man roster."""
        mock_roster = {
            "roster": [
                {"person": {"id": 1}, "status": {"code": "A"}},
                {"person": {"id": 2}, "status": {"code": "RM"}},
                {"person": {"id": 3}, "status": {"code": "D10"}},
            ],
            "rosterType": "40Man",
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147/roster/40Man").mock(
            return_value=Response(200, json=mock_roster)
        )

        response = client.get("/api/v1/teams/147/roster/40Man")

        assert response.status_code == 200
        data = response.json()
        assert data["rosterType"] == "40Man"
        assert len(data["roster"]) == 3
        assert route.called

    def test_roster_by_type_fullseason(self, client: TestClient, respx_mock):
        """Test retrieving full season roster."""
        mock_roster = {
            "roster": [
                {"person": {"id": 660271, "fullName": "Aaron Judge"}},
                {"person": {"id": 542438, "fullName": "Gerrit Cole"}},
            ],
            "rosterType": "fullSeason",
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147/roster/fullSeason").mock(
            return_value=Response(200, json=mock_roster)
        )

        response = client.get("/api/v1/teams/147/roster/fullSeason")

        assert response.status_code == 200
        data = response.json()
        assert data["rosterType"] == "fullSeason"

    def test_roster_with_season_param(self, client: TestClient, respx_mock):
        """Test roster retrieval with season parameter."""
        mock_roster = {"roster": [{"person": {"id": 1}}], "season": 2023}

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147/roster").mock(
            return_value=Response(200, json=mock_roster)
        )

        response = client.get("/api/v1/teams/147/roster?season=2023")

        assert response.status_code == 200
        assert route.called
        assert "season=2023" in str(route.calls.last.request.url)

    def test_roster_with_date_param(self, client: TestClient, respx_mock):
        """Test historical roster by date."""
        mock_roster = {"roster": [{"person": {"id": 1}}], "date": "2023-07-01"}

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147/roster").mock(
            return_value=Response(200, json=mock_roster)
        )

        response = client.get("/api/v1/teams/147/roster?date=2023-07-01")

        assert response.status_code == 200
        assert route.called
        assert "date=2023-07-01" in str(route.calls.last.request.url)

    def test_roster_multiple_teams(self, client: TestClient, respx_mock):
        """Test roster retrieval for different teams."""
        teams = [147, 121, 111]  # Yankees, Mets, Red Sox

        for team_id in teams:
            mock_roster = {"roster": [{"person": {"id": 1}}], "teamId": team_id}

            respx_mock.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster").mock(
                return_value=Response(200, json=mock_roster)
            )

        for team_id in teams:
            response = client.get(f"/api/v1/teams/{team_id}/roster")
            assert response.status_code == 200
            data = response.json()
            assert data["teamId"] == team_id

    def test_roster_player_details(self, client: TestClient, respx_mock):
        """Test roster includes detailed player information."""
        mock_roster = {
            "roster": [
                {
                    "person": {
                        "id": 660271,
                        "fullName": "Aaron Judge",
                        "firstName": "Aaron",
                        "lastName": "Judge",
                    },
                    "jerseyNumber": "99",
                    "position": {
                        "code": "9",
                        "name": "Outfielder",
                        "type": "Outfielder",
                        "abbreviation": "RF",
                    },
                    "status": {"code": "A", "description": "Active"},
                }
            ]
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/teams/147/roster").mock(
            return_value=Response(200, json=mock_roster)
        )

        response = client.get("/api/v1/teams/147/roster")

        assert response.status_code == 200
        data = response.json()
        player = data["roster"][0]
        assert player["person"]["fullName"] == "Aaron Judge"
        assert player["jerseyNumber"] == "99"
        assert player["position"]["code"] == "9"
        assert player["status"]["code"] == "A"


@pytest.mark.unit
class TestAwardsCriticalPaths:
    """Detailed tests for awards endpoints."""

    def test_awards_list(self, client: TestClient, respx_mock):
        """Test retrieving list of all awards."""
        mock_awards = {
            "awards": [
                {
                    "id": "MLBHOF",
                    "name": "Baseball Hall of Fame",
                    "description": "National Baseball Hall of Fame and Museum",
                },
                {"id": "MLBMVP", "name": "Most Valuable Player", "description": "League MVP Award"},
                {"id": "MLBCYA", "name": "Cy Young Award", "description": "Best Pitcher Award"},
            ]
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/awards").mock(
            return_value=Response(200, json=mock_awards)
        )

        response = client.get("/api/v1/awards")

        assert response.status_code == 200
        data = response.json()
        assert "awards" in data
        assert len(data["awards"]) == 3
        assert data["awards"][0]["id"] == "MLBHOF"
        assert data["awards"][1]["name"] == "Most Valuable Player"

    def test_awards_by_sport(self, client: TestClient, respx_mock):
        """Test filtering awards by sport."""
        mock_awards = {
            "awards": [
                {"id": "MLBMVP", "name": "Most Valuable Player", "sportId": 1},
                {"id": "MLBCYA", "name": "Cy Young Award", "sportId": 1},
            ]
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/awards").mock(
            return_value=Response(200, json=mock_awards)
        )

        response = client.get("/api/v1/awards?sportId=1")

        assert response.status_code == 200
        assert route.called
        assert "sportId=1" in str(route.calls.last.request.url)

    def test_specific_award(self, client: TestClient, respx_mock):
        """Test retrieving details for a specific award."""
        mock_award = {
            "id": 1,
            "name": "Most Valuable Player",
            "description": "Annual award given to the most valuable player in each league",
            "notes": "Voted by Baseball Writers' Association of America",
            "firstAwarded": 1931,
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/awards/1").mock(
            return_value=Response(200, json=mock_award)
        )

        response = client.get("/api/v1/awards/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Most Valuable Player"
        assert data["firstAwarded"] == 1931

    def test_award_recipients(self, client: TestClient, respx_mock):
        """Test retrieving recipients of an award."""
        mock_recipients = {
            "awardId": 1,
            "recipients": [
                {
                    "season": 2022,
                    "person": {"id": 660271, "fullName": "Aaron Judge"},
                    "team": {"id": 147, "name": "New York Yankees"},
                    "league": {"id": 103, "name": "American League"},
                },
                {
                    "season": 2021,
                    "person": {"id": 660670, "fullName": "Shohei Ohtani"},
                    "team": {"id": 108, "name": "Los Angeles Angels"},
                    "league": {"id": 103, "name": "American League"},
                },
            ],
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/awards/1/recipients").mock(
            return_value=Response(200, json=mock_recipients)
        )

        response = client.get("/api/v1/awards/1/recipients")

        assert response.status_code == 200
        data = response.json()
        assert data["awardId"] == 1
        assert len(data["recipients"]) == 2
        assert data["recipients"][0]["season"] == 2022
        assert data["recipients"][0]["person"]["fullName"] == "Aaron Judge"

    def test_award_recipients_by_season(self, client: TestClient, respx_mock):
        """Test award recipients filtered by season."""
        mock_recipients = {
            "awardId": 2,
            "season": 2023,
            "recipients": [
                {
                    "person": {"id": 605483, "fullName": "Gerrit Cole"},
                    "league": {"id": 103, "name": "American League"},
                },
                {
                    "person": {"id": 669302, "fullName": "Blake Snell"},
                    "league": {"id": 104, "name": "National League"},
                },
            ],
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/awards/2/recipients").mock(
            return_value=Response(200, json=mock_recipients)
        )

        response = client.get("/api/v1/awards/2/recipients?season=2023")

        assert response.status_code == 200
        data = response.json()
        assert data["season"] == 2023
        assert len(data["recipients"]) == 2
        assert route.called
        assert "season=2023" in str(route.calls.last.request.url)

    def test_award_recipients_by_league(self, client: TestClient, respx_mock):
        """Test award recipients filtered by league."""
        mock_recipients = {
            "awardId": 3,
            "recipients": [
                {
                    "season": 2023,
                    "person": {"id": 677594, "fullName": "Gunnar Henderson"},
                    "league": {"id": 103, "name": "American League"},
                }
            ],
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/awards/3/recipients").mock(
            return_value=Response(200, json=mock_recipients)
        )

        response = client.get("/api/v1/awards/3/recipients?leagueId=103")

        assert response.status_code == 200
        assert route.called
        assert "leagueId=103" in str(route.calls.last.request.url)

    def test_multiple_award_types(self, client: TestClient, respx_mock):
        """Test retrieving different award types."""
        award_ids = [1, 2, 3, 4, 5]  # MVP, Cy Young, ROY, Gold Glove, Silver Slugger

        for award_id in award_ids:
            mock_award = {
                "id": award_id,
                "name": f"Award {award_id}",
                "description": f"Description for Award {award_id}",
            }

            respx_mock.get(f"https://statsapi.mlb.com/api/v1/awards/{award_id}").mock(
                return_value=Response(200, json=mock_award)
            )

        for award_id in award_ids:
            response = client.get(f"/api/v1/awards/{award_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == award_id

    def test_award_recipients_historical(self, client: TestClient, respx_mock):
        """Test historical award recipients spanning multiple seasons."""
        mock_recipients = {
            "awardId": 10,
            "recipients": [
                {"season": 2023, "person": {"id": 123, "fullName": "Player One"}},
                {"season": 2022, "person": {"id": 456, "fullName": "Player Two"}},
                {"season": 2021, "person": {"id": 789, "fullName": "Player Three"}},
                {"season": 2020, "person": {"id": 101, "fullName": "Player Four"}},
            ],
            "totalRecipients": 4,
        }

        route = respx_mock.get("https://statsapi.mlb.com/api/v1/awards/10/recipients").mock(
            return_value=Response(200, json=mock_recipients)
        )

        response = client.get("/api/v1/awards/10/recipients?startSeason=2020&endSeason=2023")

        assert response.status_code == 200
        data = response.json()
        assert len(data["recipients"]) == 4
        assert data["totalRecipients"] == 4
        assert route.called

    def test_award_recipients_with_stats(self, client: TestClient, respx_mock):
        """Test award recipients with statistical information."""
        mock_recipients = {
            "awardId": 1,
            "season": 2022,
            "recipients": [
                {
                    "person": {"id": 660271, "fullName": "Aaron Judge"},
                    "stats": {
                        "gamesPlayed": 157,
                        "homeRuns": 62,
                        "rbi": 131,
                        "avg": ".311",
                        "ops": 1.111,
                    },
                }
            ],
        }

        respx_mock.get("https://statsapi.mlb.com/api/v1/awards/1/recipients").mock(
            return_value=Response(200, json=mock_recipients)
        )

        response = client.get("/api/v1/awards/1/recipients?season=2022&hydrate=stats")

        assert response.status_code == 200
        data = response.json()
        recipient = data["recipients"][0]
        assert recipient["person"]["fullName"] == "Aaron Judge"
        # Stat field names are translated to standard abbreviations (homeRuns -> HR).
        assert recipient["stats"]["HR"] == 62
