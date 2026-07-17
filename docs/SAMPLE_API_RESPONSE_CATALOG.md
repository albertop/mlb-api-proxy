# API Response Examples Catalog

This document provides a complete index of collected API response examples for the MLB API proxy.

**Generated**: 2026-02-07T14:32:45
**Base URL**: http://localhost:8000
**Total Routers**: 33
**Total Endpoints**: 189

## Quick Navigation

### Routers

- [analytics](#analytics) - 8 endpoints
- [attendance](#attendance) - 4 endpoints
- [awards](#awards) - 3 endpoints
- [bat_tracking](#bat-tracking) - 2 endpoints
- [biomechanics](#biomechanics) - 5 endpoints
- [broadcast](#broadcast) - 3 endpoints
- [conference](#conference) - 2 endpoints
- [division](#division) - 4 endpoints
- [draft](#draft) - 3 endpoints
- [games](#games) - 13 endpoints
- [game_pace](#game-pace) - 2 endpoints
- [high_low](#high-low) - 2 endpoints
- [home_run_derby](#home-run-derby) - 2 endpoints
- [job](#job) - 2 endpoints
- [league](#league) - 3 endpoints
- [milestones](#milestones) - 4 endpoints
- [misc](#misc) - 54 endpoints
- [people](#people) - 9 endpoints
- [predictions](#predictions) - 2 endpoints
- [reviews](#reviews) - 7 endpoints
- [schedule](#schedule) - 7 endpoints
- [season](#season) - 3 endpoints
- [skeletal](#skeletal) - 2 endpoints
- [sports](#sports) - 3 endpoints
- [standings](#standings) - 4 endpoints
- [stats](#stats) - 8 endpoints
- [streaks](#streaks) - 2 endpoints
- [teams](#teams) - 15 endpoints
- [transactions](#transactions) - 5 endpoints
- [uniforms](#uniforms) - 4 endpoints
- [venues](#venues) - 4 endpoints
- [weather](#weather) - 2 endpoints

---

## Analytics

**Endpoints**: 8
**Details**: See [full documentation](response-examples/analytics/README.md)

| Method | Endpoint | Response File |
|--------|----------|---|
| `GET` | `/api/v1/analytics/game` | [get_analytics_game.json](response-examples/analytics/get_analytics_game.json) |
| `GET` | `/api/v1/analytics/guids` | [get_analytics_guids.json](response-examples/analytics/get_analytics_guids.json) |
| `GET` | `/api/v1/game/{game_pk}/{guid}/analytics` | [get_game_game_pk_guid_analytics.json](response-examples/analytics/get_game_game_pk_guid_analytics.json) |
| `GET` | `/api/v1/game/{game_pk}/{guid}/contextMetrics` | [get_game_game_pk_guid_contextmetrics.json](response-examples/analytics/get_game_game_pk_guid_contextmetrics.json) |
| `GET` | `/api/v1/game/{game_pk}/{guid}/contextMetricsAverages` | [get_game_game_pk_guid_contextmetricsaverages.json](response-examples/analytics/get_game_game_pk_guid_contextmetricsaverages.json) |
| `GET` | `/api/v1/game/{game_pk}/{guid}/homeRunBallparks` | [get_game_game_pk_guid_homerunballparks.json](response-examples/analytics/get_game_game_pk_guid_homerunballparks.json) |
| `GET` | `/api/v1/game/lastPitch` | [get_game_lastpitch.json](response-examples/analytics/get_game_lastpitch.json) |
| `GET` | `/api/v1/game/{game_pk}/guids` | [get_game_game_pk_guids.json](response-examples/analytics/get_game_game_pk_guids.json) |

## Awards

**Endpoints**: 3
**Details**: See [full documentation](response-examples/awards/README.md)

| Method | Endpoint | Response File |
|--------|----------|---|
| `GET` | `/api/v1/awards` | [get_awards.json](response-examples/awards/get_awards.json) |
| `GET` | `/api/v1/awards/{award_id}` | [get_awards_award_id.json](response-examples/awards/get_awards_award_id.json) |
| `GET` | `/api/v1/awards/{award_id}/recipients` | [get_awards_award_id_recipients.json](response-examples/awards/get_awards_award_id_recipients.json) |

## Games

**Endpoints**: 13
**Details**: See [full documentation](response-examples/games/README.md)

| Method | Endpoint | Response File |
|--------|----------|---|
| `GET` | `/api/v1.1/game/{game_pk}/feed/live` | [get_game_game_pk_feed_live.json](response-examples/games/get_game_game_pk_feed_live.json) |
| `GET` | `/api/v1/game/{game_pk}/boxscore` | [get_game_game_pk_boxscore.json](response-examples/games/get_game_game_pk_boxscore.json) |
| `GET` | `/api/v1/game/{game_pk}/feed/live` | [get_game_game_pk_feed_live.json](response-examples/games/get_game_game_pk_feed_live.json) |
| `GET` | `/api/v1/game/{game_pk}/linescore` | [get_game_game_pk_linescore.json](response-examples/games/get_game_game_pk_linescore.json) |
| `GET` | `/api/v1/game/{game_pk}/timecode` | [get_game_game_pk_timecode.json](response-examples/games/get_game_game_pk_timecode.json) |
| `GET` | `/api/v1/games` | [get_games.json](response-examples/games/get_games.json) |
| `GET` | `/api/v1/games/updates` | [get_games_updates.json](response-examples/games/get_games_updates.json) |
| `POST` | `/api/v1/game/{game_pk}/events` | [post_game_game_pk_events.json](response-examples/games/post_game_game_pk_events.json) |

## People

**Endpoints**: 9
**Details**: See [full documentation](response-examples/people/README.md)

| Method | Endpoint | Response File |
|--------|----------|---|
| `GET` | `/api/v1/people` | [get_people.json](response-examples/people/get_people.json) |
| `GET` | `/api/v1/people/{person_id}` | [get_people_person_id.json](response-examples/people/get_people_person_id.json) |
| `GET` | `/api/v1/people/{person_id}/stat/data` | [get_people_person_id_stat_data.json](response-examples/people/get_people_person_id_stat_data.json) |
| `GET` | `/api/v1/people/search` | [get_people_search.json](response-examples/people/get_people_search.json) |

## Schedule

**Endpoints**: 7
**Details**: See [full documentation](response-examples/schedule/README.md)

| Method | Endpoint | Response File |
|--------|----------|---|
| `GET` | `/api/v1/schedule` | [get_schedule.json](response-examples/schedule/get_schedule.json) |
| `GET` | `/api/v1/schedule/games` | [get_schedule_games.json](response-examples/schedule/get_schedule_games.json) |

## Teams

**Endpoints**: 15
**Details**: See [full documentation](response-examples/teams/README.md)

| Method | Endpoint | Response File |
|--------|----------|---|
| `GET` | `/api/v1/teams` | [get_teams.json](response-examples/teams/get_teams.json) |
| `GET` | `/api/v1/teams/{team_id}` | [get_teams_team_id.json](response-examples/teams/get_teams_team_id.json) |
| `GET` | `/api/v1/teams/{team_id}/roster` | [get_teams_team_id_roster.json](response-examples/teams/get_teams_team_id_roster.json) |
| `GET` | `/api/v1/teams/{team_id}/stats` | [get_teams_team_id_stats.json](response-examples/teams/get_teams_team_id_stats.json) |

---

## How to Use This Catalog

### 1. **Find an Endpoint**
   - Use the Quick Navigation section to find the router (domain)
   - Click the router name to jump to that section

### 2. **View Response Files**
   - Click the response file link to view the actual JSON response
   - Each file contains metadata about the request and response

### 3. **Understand Response Structure**
   - Each JSON file includes:
     - `endpoint` - The API path
     - `method` - HTTP method used
     - `status_code` - HTTP response code
     - `response` - The actual response body
     - `url` - Full URL that was called
     - `timestamp` - When the response was collected

### 4. **Use for Development**
   - Reference for API client development
   - Schema validation for request/response parsing
   - Understanding response structure before coding
   - Integration testing examples

## Machine-Readable Index

For programmatic access to this data, see:
- **File**: `response-examples-index.json`
- **Format**: JSON with complete endpoint metadata
- **Use**: API client libraries, code generation, validation

## Notes

- All responses were collected from the MLB API proxy
- Sample parameters used from conftest.py test fixtures
- Time-sensitive data (dates, seasons) from collection time
- Some endpoints may return different data based on current date/season
- Error responses show validation and error handling patterns
