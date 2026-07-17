# MLB Stats API Documentation

## Overview

**Title:** Stats API Documentation  
**Description:** Official API for Major League Baseball  
**Version:** 2.0.0  
**API Specification:** OpenAPI 3.0.1

---

## Base URLs

The API is available on multiple environments:

| Environment | URL |
|------------|-----|
| **Production** | `https://statsapi.mlb.com` |
| **Beta** | `https://beta-statsapi.mlb.com` |
| **QA** | `https://qa-statsapi.mlb.com` |
| **Local** | `http://localhost:8080` |

---

## Authentication

The API supports two authentication methods:

### Basic Authentication
```
Authorization: Basic <base64-encoded-credentials>
```

### Bearer Token (JWT)
```
Authorization: Bearer <jwt-token>
```

> **Note:** Not all endpoints require authentication. Endpoints requiring authentication are marked with 🔒 in this documentation.

---

## API Categories

The API is organized into the following categories:

- [**Teams**](#teams) - Team information, rosters, alumni, and statistics
- [**Person**](#players-person) - Player information and statistics
- [**Game**](#games) - Game data, schedules, and live game information
- [**Schedule**](#schedule) - Schedule information and types
- [**Stats**](#statistics) - Statistical data and metrics
- [**Standings**](#standings) - Team standings and rankings
- [**Analytics**](#analytics) - Advanced tracking data and metrics
- [**Draft**](#draft) - MLB Draft information
- [**Awards**](#awards) - Award information and recipients
- [**Venues**](#venues) - Stadium and venue information
- [**Weather**](#weather) - Weather data for venues and games
- [**Transactions**](#transactions) - Player transactions
- [**Sports**](#configuration-and-lookup-endpoints) - Sports-related endpoints
- [**League**](#configuration-and-lookup-endpoints) - League information
- [**Division**](#configuration-and-lookup-endpoints) - Division information
- [**Conference**](#configuration-and-lookup-endpoints) - Conference information
- [**Season**](#configuration-and-lookup-endpoints) - Season information
- [**Attendance**](#configuration-and-lookup-endpoints) - Attendance data
- [**Broadcast**](#configuration-and-lookup-endpoints) - Broadcast information
- [**Uniforms**](#uniforms) - Team uniform data
- [**Reviews**](#reviews) - Game review information
- [**Predictions**](#predictions) - Prediction data
- [**Milestones**](#milestones) - Player milestones
- [**Streaks**](#streaks) - Statistical streaks
- [**High/Low**](#configuration-and-lookup-endpoints) - High and low statistics
- [**Game Pace**](#configuration-and-lookup-endpoints) - Game pace statistics
- [**Homerun Derby**](#configuration-and-lookup-endpoints) - Home run derby data
- [**Bat Tracking**](#configuration-and-lookup-endpoints) - Bat tracking analytics
- [**Biomechanics**](#configuration-and-lookup-endpoints) - Biomechanical tracking data
- [**Skeletal**](#configuration-and-lookup-endpoints) - Skeletal tracking data
- [**Job**](#configuration-and-lookup-endpoints) - Job types and roles
- [**Misc**](#configuration-and-lookup-endpoints) - Miscellaneous configuration endpoints

---

## Common Query Parameters

Many endpoints support the following common parameters:

### Fields Parameter
```
fields=topLevelNode,childNode,attribute
```
Comma-delimited list of specific fields to be returned. This allows you to filter the response to only include the data you need.

**Example:**
```
GET /api/v1/teams?fields=teams,id,name,abbreviation
```

---

## Key Endpoints

### Teams

#### Get All Teams
```http
GET /api/v1/teams
```

**Query Parameters:**
- `sportId` (integer) - Unique Sport Identifier
- `season` (string) - Season of play
- `activeStatus` (string) - Active status (Y/N)
- `leagueIds` (array) - Unique League Identifier(s)
- `gameType` (GameType) - Type of Game
- `fields` (array) - Comma-delimited field list

**Response:** Returns a list of all MLB teams with their details.

---

#### Get Team Details
```http
GET /api/v1/teams/{teamId}
```

**Path Parameters:**
- `teamId` (integer, required) - Unique Team Identifier (e.g., 141, 147)

**Query Parameters:**
- `season` (string) - Season of play
- `sportId` (integer) - Unique Sport Identifier
- `fields` (array) - Comma-delimited field list

---

#### Get Team Roster
```http
GET /api/v1/teams/{teamId}/roster
```

**Path Parameters:**
- `teamId` (integer, required) - Unique Team Identifier

**Query Parameters:**
- `rosterType` (string) - Type of roster (e.g., active, 40Man, fullRoster)
- `season` (string) - Season of play
- `date` (string) - Date for roster (format: MM/DD/YYYY)

---

#### Get Team Alumni
```http
GET /api/v1/teams/{teamId}/alumni
```

**Path Parameters:**
- `teamId` (integer, required) - Unique Team Identifier

**Query Parameters:**
- `season` (string, required) - Season of play
- `group` (StatGroup) - Category of statistic to return
- `fields` (array) - Comma-delimited field list

---

#### Get Team Statistics
```http
GET /api/v1/teams/{teamId}/stats
```

**Path Parameters:**
- `teamId` (integer, required) - Unique Team Identifier

**Query Parameters:**
- `season` (string) - Season of play
- `stats` (array) - Type of statistics
- `group` (StatGroup) - Category of statistic

---

#### Get Team Leaders
```http
GET /api/v1/teams/{teamId}/leaders
```

**Path Parameters:**
- `teamId` (integer, required) - Unique Team Identifier

**Query Parameters:**
- `leaderCategories` (array, required) - Category of leaders
- `season` (string, required) - Season of play
- `leaderGameTypes` (array) - Game type for leaders
- `statGroup` (StatGroup) - Stat group
- `limit` (integer) - Number of results (default: 1)
- `fields` (array) - Comma-delimited field list

---

#### Get Team Coaches
```http
GET /api/v1/teams/{teamId}/coaches
```

**Path Parameters:**
- `teamId` (integer, required) - Unique Team Identifier

**Query Parameters:**
- `season` (string, required) - Season of play
- `date` (string) - Date for coaches (format: MM/DD/YYYY)

---

#### Get Team Affiliates
```http
GET /api/v1/teams/{teamId}/affiliates
```

**Path Parameters:**
- `teamId` (integer, required) - Unique Team Identifier

**Query Parameters:**
- `season` (string) - Season of play
- `sportId` (integer) - Unique Sport Identifier

---

### Players (Person)

#### Get Player Information
```http
GET /api/v1/people/{personId}
```

**Path Parameters:**
- `personId` (integer, required) - Unique Player Identifier

**Query Parameters:**
- `season` (string) - Season of play
- `hydrate` (array) - Hydration parameters for additional data
- `fields` (array) - Comma-delimited field list

---

#### Get Player Statistics
```http
GET /api/v1/people/{personId}/stats
```

**Path Parameters:**
- `personId` (integer, required) - Unique Player Identifier

**Query Parameters:**
- `stats` (array, required) - Type of statistics
- `group` (StatGroup) - Category of statistic
- `season` (string) - Season of play
- `gameType` (GameType) - Type of game

---

#### Get Player Game Stats
```http
GET /api/v1/people/{personId}/stats/game/{gamePk}
```

**Path Parameters:**
- `personId` (integer, required) - Unique Player Identifier
- `gamePk` (integer, required) - Unique Primary Key for a Game

**Query Parameters:**
- `fields` (array) - Comma-delimited field list

---

#### Search Players
```http
GET /api/v1/people/search
```

**Query Parameters:**
- `names` (string, required) - Player name(s)
- `sportId` (integer) - Sport Identifier
- `fields` (array) - Comma-delimited field list

---

### Games

#### Get Game Information
```http
GET /api/v1/game/{gamePk}
```

**Path Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game

**Query Parameters:**
- `timecode` (string) - Use this parameter to return game data with the state at a specific time
- `hydrate` (array) - Hydration parameters
- `fields` (array) - Comma-delimited field list

---

#### Get Game Live Feed
```http
GET /api/v1.1/game/{gamePk}/feed/live
```

**Path Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game

**Query Parameters:**
- `timecode` (string) - Timecode for specific game state
- `hydrate` (array) - Hydration parameters
- `fields` (array) - Comma-delimited field list

**Description:** Returns comprehensive live game data including plays, boxscore, and linescore.

---

#### Get Game Box Score
```http
GET /api/v1/game/{gamePk}/boxscore
```

**Path Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game

**Query Parameters:**
- `timecode` (string) - Timecode for specific game state
- `fields` (array) - Comma-delimited field list

---

#### Get Game Line Score
```http
GET /api/v1/game/{gamePk}/linescore
```

**Path Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game

**Query Parameters:**
- `timecode` (string) - Timecode for specific game state
- `fields` (array) - Comma-delimited field list

---

#### Get Game Content
```http
GET /api/v1/game/{gamePk}/content
```

**Path Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game

**Query Parameters:**
- `highlightLimit` (integer) - Number of highlights to return

---

### Schedule

#### Get Schedule
```http
GET /api/v1/schedule
```

**Query Parameters:**
- `sportId` (integer) - Unique Sport Identifier (default: 1 for MLB)
- `season` (string) - Season of play
- `date` (string) - Date for schedule (format: MM/DD/YYYY)
- `startDate` (string) - Start date for range
- `endDate` (string) - End date for range
- `gameType` (GameType) - Type of game
- `teamId` (integer) - Unique Team Identifier
- `leagueId` (integer) - Unique League Identifier
- `venueIds` (array) - Venue Identifier(s)
- `gamePks` (array) - Game Primary Key(s)
- `hydrate` (array) - Hydration parameters
- `fields` (array) - Comma-delimited field list

---

#### Get Postseason Schedule
```http
GET /api/v1/schedule/postseason
```

**Query Parameters:**
- `sportId` (integer) - Unique Sport Identifier
- `season` (string) - Season of play
- `gameTypes` (array) - Type(s) of game
- `seriesNumber` (integer) - Series number
- `teamId` (integer) - Unique Team Identifier

---

#### Get Postseason Series
```http
GET /api/v1/schedule/postseason/series
```

**Query Parameters:**
- `sportId` (integer) - Unique Sport Identifier
- `season` (string, required) - Season of play
- `fields` (array) - Comma-delimited field list

---

#### Get Tied Games
```http
GET /api/v1/schedule/games/tied
```

**Query Parameters:**
- `season` (string, required) - Season of play
- `gameTypes` (array) - Type(s) of game
- `fields` (array) - Comma-delimited field list

---

### Statistics

#### Get Statistics
```http
GET /api/v1/stats
```

**Query Parameters:**
- `stats` (array, required) - Type(s) of statistics
- `playerPool` (string) - Player pool filter
- `position` (string) - Position filter
- `teamId` (integer) - Team Identifier
- `leagueId` (integer) - League Identifier
- `limit` (integer) - Number of results to return
- `offset` (integer) - Offset for pagination
- `group` (StatGroup) - Stat group
- `gameType` (GameType) - Type of game
- `season` (string) - Season of play
- `sportIds` (array) - Sport Identifier(s)
- `sortStat` (string) - Stat to sort by
- `order` (string) - Sort order (asc/desc)
- `hydrate` (array) - Hydration parameters
- `fields` (array) - Comma-delimited field list

---

#### Get Stat Leaders
```http
GET /api/v1/stats/leaders
```

**Query Parameters:**
- `leaderCategories` (array, required) - Category of leaders
- `season` (string) - Season of play
- `leaderGameTypes` (array) - Game type(s) for leaders
- `sitCodes` (array) - Situation codes
- `position` (string) - Position filter
- `statGroup` (StatGroup) - Stat group
- `league` (integer) - League identifier
- `limit` (integer) - Number of results (default: 10)
- `fields` (array) - Comma-delimited field list

---

#### Get Stat Metrics
```http
GET /api/v1/stats/metrics
```

**Query Parameters:**
- `metrics` (array, required) - Metrics to retrieve
- `personIds` (array, required) - Person Identifier(s)
- `season` (string, required) - Season of play
- `fields` (array) - Comma-delimited field list

---

#### Get Statcast Metrics
```http
GET /api/v1/people/{personId}/stats/metrics
```

**Path Parameters:**
- `personId` (integer, required) - Unique Player Identifier

**Query Parameters:**
- `metrics` (array, required) - Metrics to retrieve
- `season` (string, required) - Season of play
- `fields` (array) - Comma-delimited field list

---

#### Get BEAST Stats
```http
GET /api/v1/beast/stats
```

**Query Parameters:**
- `metrics` (array, required) - Metrics to retrieve
- `fields` (array) - Comma-delimited field list
- Multiple filtering parameters for advanced queries

**Description:** Advanced statistical endpoint for detailed player metrics.

---

### Standings

#### Get Standings
```http
GET /api/v1/standings
```

**Query Parameters:**
- `leagueId` (array, required) - League Identifier(s)
- `season` (string, required) - Season of play
- `standingsTypes` (array) - Type(s) of standings
- `date` (string) - Date for standings (format: MM/DD/YYYY)
- `hydrate` (array) - Hydration parameters
- `fields` (array) - Comma-delimited field list

---

### Analytics

#### Get Play Tracking Data 🔒
```http
GET /api/v1/game/{gamePk}/{guid}/contextMetricsAverages
```

**Path Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game
- `guid` (string, required) - Unique identifier for a play within a game

**Query Parameters:**
- `fields` (array) - Comma-delimited field list

**Headers:**
- Recommended: `Accept-Encoding: gzip` (responses can be very large)

**Description:** Returns raw coordinate data and refined calculated metrics for a specific play.

---

#### Get Spray Chart
```http
GET /api/v1/spraycharts
```

**Query Parameters:**
- `personId` (integer, required) - Unique Player Identifier
- `season` (string, required) - Season of play
- `gameType` (GameType) - Type of game

---

#### Get Outs Above Average
```http
GET /api/v1/outsAboveAverage
```

**Query Parameters:**
- `personId` (integer, required) - Unique Player Identifier
- `season` (string, required) - Season of play
- `gameType` (GameType) - Type of game

---

#### Get Stolen Base Probability
```http
GET /api/v1/stolenBaseProbability
```

**Query Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game
- `playId` (string, required) - Play identifier

---

### Venues

#### Get All Venues
```http
GET /api/v1/venues
```

**Query Parameters:**
- `venueIds` (array) - Venue Identifier(s)
- `season` (string) - Season of play
- `fields` (array) - Comma-delimited field list

---

#### Get Venue Details
```http
GET /api/v1/venues/{venueId}
```

**Path Parameters:**
- `venueId` (integer, required) - Unique Venue Identifier

**Query Parameters:**
- `season` (string) - Season of play
- `hydrate` (array) - Hydration parameters
- `fields` (array) - Comma-delimited field list

---

### Weather

#### Get Venue Weather (Full) 🔒
```http
GET /api/v1/weather/venues/{venueId}/full
```

**Path Parameters:**
- `venueId` (integer, required) - Unique Venue Identifier

**Query Parameters:**
- `fields` (array) - Comma-delimited field list

---

#### Get Venue Weather (Basic) 🔒
```http
GET /api/v1/weather/venues/{venueId}/basic
```

**Path Parameters:**
- `venueId` (integer, required) - Unique Venue Identifier

**Query Parameters:**
- `fields` (array) - Comma-delimited field list

---

#### Get Weather Forecast 🔒
```http
GET /api/v1/weather/venues/{venueId}/forecasts/{targetTime}
```

**Path Parameters:**
- `venueId` (integer, required) - Unique Venue Identifier
- `targetTime` (string, required) - Target time for forecast

**Query Parameters:**
- `fields` (array) - Comma-delimited field list

---

### Draft

#### Get Draft
```http
GET /api/v1/draft/{year}
```

**Path Parameters:**
- `year` (string, required) - Year of draft

**Query Parameters:**
- `limit` (integer) - Number of results
- `fields` (array) - Comma-delimited field list
- `round` (string) - Specific round
- `name` (string) - Player name filter
- `school` (string) - School filter
- `state` (string) - State filter
- `country` (string) - Country filter
- `position` (string) - Position filter
- `teamId` (integer) - Team Identifier
- `playerId` (integer) - Player Identifier

---

#### Get Latest Draft Pick
```http
GET /api/v1/draft/latest
```

**Query Parameters:**
- `limit` (integer) - Number of results (default: 10)
- `fields` (array) - Comma-delimited field list

---

### Awards

#### Get Awards
```http
GET /api/v1/awards
```

**Query Parameters:**
- `sportId` (integer) - Sport Identifier
- `leagueId` (integer) - League Identifier
- `season` (string) - Season of play
- `hydrate` (array) - Hydration parameters
- `fields` (array) - Comma-delimited field list

---

#### Get Award Details
```http
GET /api/v1/awards/{awardId}
```

**Path Parameters:**
- `awardId` (string, required) - Award Identifier

**Query Parameters:**
- `fields` (array) - Comma-delimited field list

---

#### Get Award Recipients
```http
GET /api/v1/awards/{awardId}/recipients
```

**Path Parameters:**
- `awardId` (string, required) - Award Identifier

**Query Parameters:**
- `season` (string) - Season of play
- `hydrate` (array) - Hydration parameters
- `fields` (array) - Comma-delimited field list

---

### Transactions

#### Get Transactions
```http
GET /api/v1/transactions
```

**Query Parameters:**
- `teamId` (integer) - Team Identifier
- `playerId` (integer) - Player Identifier
- `date` (string) - Specific date (format: MM/DD/YYYY)
- `startDate` (string) - Start date for range
- `endDate` (string) - End date for range
- `sportId` (integer) - Sport Identifier

---

### Uniforms

#### Get Team Uniforms
```http
GET /api/v1/teams/{teamId}/uniforms
```

**Path Parameters:**
- `teamId` (integer, required) - Unique Team Identifier

**Query Parameters:**
- `season` (string) - Season of play
- `fields` (array) - Comma-delimited field list

---

#### Get Game Uniforms
```http
GET /api/v1/game/{gamePk}/uniforms
```

**Path Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game

**Query Parameters:**
- `fields` (array) - Comma-delimited field list

---

### Milestones

#### Get Milestones
```http
GET /api/v1/milestones
```

**Query Parameters:**
- `sportId` (integer) - Sport Identifier
- `season` (string) - Season of play
- `fields` (array) - Comma-delimited field list

---

### Streaks

#### Get Streaks
```http
GET /api/v1/streaks
```

**Query Parameters:**
- `sportId` (integer, required) - Sport Identifier
- `season` (string, required) - Season of play
- `streakType` (string, required) - Type of streak
- `gameType` (GameType) - Type of game
- `limit` (integer) - Number of results
- `fields` (array) - Comma-delimited field list

---

### Predictions

#### Get Game Predictions
```http
GET /api/v1/game/{gamePk}/predictions
```

**Path Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game

**Query Parameters:**
- `fields` (array) - Comma-delimited field list

---

### Reviews

#### Get Review Information
```http
GET /api/v1/reviews
```

**Query Parameters:**
- `gamePk` (integer, required) - Unique Primary Key for a Game
- `fields` (array) - Comma-delimited field list

---

## Configuration and Lookup Endpoints

The API provides numerous lookup endpoints for reference data:

### Sports
```http
GET /api/v1/sports
GET /api/v1/sports/{sportId}
```

### Leagues
```http
GET /api/v1/league
GET /api/v1/league/{leagueId}
```

### Divisions
```http
GET /api/v1/divisions
GET /api/v1/divisions/{divisionId}
```

### Seasons
```http
GET /api/v1/seasons
GET /api/v1/seasons/{seasonId}
GET /api/v1/seasons/all
```

### Game Types
```http
GET /api/v1/gameTypes
```

### Game Status
```http
GET /api/v1/gameStatus
```

### Stat Types
```http
GET /api/v1/statTypes
```

### Stat Groups
```http
GET /api/v1/statGroups
```

### Positions
```http
GET /api/v1/positions
```

### Roster Types
```http
GET /api/v1/rosterTypes
```

### Schedule Types
```http
GET /api/v1/scheduleEventTypes
GET /api/v1/scheduleTypes
```

### Standing Types
```http
GET /api/v1/standingsTypes
```

### Pitch Types
```http
GET /api/v1/pitchTypes
GET /api/v1/pitchCodes
```

### Job Types
```http
GET /api/v1/jobTypes
```

### Transaction Types
```http
GET /api/v1/transactionTypes
```

### Player Status Codes
```http
GET /api/v1/playerStatusCodes
```

### Wind Direction
```http
GET /api/v1/windDirection
```

### Review Reasons
```http
GET /api/v1/reviewReasons
```

### Platforms
```http
GET /api/v1/platforms
```

### Sky Conditions
```http
GET /api/v1/sky
```

### Situation Codes
```http
GET /api/v1/situationCodes
```

---

## Data Types and Enumerations

### StatGroup
Category of statistics. Available types can be retrieved from:
```http
GET /api/v1/statGroups
```

Common values include:
- `hitting`
- `pitching`
- `fielding`
- `catching`

### GameType
Type of game. Common values include:
- `R` - Regular Season
- `F` - Wild Card
- `D` - Division Series
- `L` - League Championship Series
- `W` - World Series
- `S` - Spring Training
- `E` - Exhibition
- `A` - All-Star Game

### Hydration Parameters
Many endpoints support hydration parameters to include additional related data in the response. Common hydration values include:
- `team`
- `person`
- `stats`
- `awards`
- `currentTeam`
- `league`
- `division`
- `sport`
- `venue`

---

## Response Format

All responses are in JSON format. Typical response structure:

```json
{
  "copyright": "Copyright information",
  "data": {
    // Response data here
  }
}
```

### Error Responses

Error responses will include appropriate HTTP status codes and error messages:

```json
{
  "message": "Error description",
  "timestamp": "2025-12-18T10:00:00Z"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

---

## Best Practices

### 1. Use Field Filtering
Always use the `fields` parameter to request only the data you need. This reduces payload size and improves performance.

**Example:**
```
GET /api/v1/teams?fields=teams,id,name,abbreviation
```

### 2. Enable Compression
For endpoints that return large datasets (especially analytics endpoints), include the compression header:
```
Accept-Encoding: gzip
```

### 3. Date Formatting
Dates should be formatted as `MM/DD/YYYY` for query parameters.

### 4. Rate Limiting
Be mindful of API rate limits. Implement appropriate caching and throttling in your applications.

### 5. Use Hydration Wisely
Hydration can significantly increase response size. Only hydrate relationships you actually need.

### 6. Timecodes for Historical Data
Use the `timecode` parameter on game endpoints to retrieve game state at specific points in time.

---

## Example Use Cases

### Get Today's Games
```http
GET /api/v1/schedule?sportId=1&date=12/18/2025
```

### Get Team Roster for Current Season
```http
GET /api/v1/teams/147/roster?rosterType=active
```

### Get Player Career Stats
```http
GET /api/v1/people/660271/stats?stats=career&group=hitting
```

### Get Live Game Feed
```http
GET /api/v1.1/game/717622/feed/live
```

### Get Current Standings
```http
GET /api/v1/standings?leagueId=103,104&season=2025
```

### Get Stat Leaders
```http
GET /api/v1/stats/leaders?leaderCategories=homeRuns&season=2025&limit=10
```

### Search for a Player
```http
GET /api/v1/people/search?names=Mike%20Trout
```

---

## Support and Resources

For additional information and support:

- **Production API:** https://statsapi.mlb.com
- **Beta API:** https://beta-statsapi.mlb.com
- **API Version:** 2.0.0
- **OpenAPI Specification:** Available in `mlb_api_spec.json`

---

## Notes

- 🔒 denotes endpoints requiring authentication
- All timestamps are in UTC unless otherwise specified
- The API supports both GET and POST methods for certain endpoints
- Some endpoints may have additional undocumented parameters
- Response schemas are defined in the OpenAPI specification file

---

*Documentation generated from OpenAPI 3.0.1 specification*  
*Last updated: December 18, 2025*
