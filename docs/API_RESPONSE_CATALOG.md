# API Response Examples Catalog

This document provides a complete index of collected API response examples for the MLB API proxy.

**Generated**: 2026-02-15 16:33:05
**Base URL**: http://10.0.0.39:3002
**Total Routers**: 23
**Total Endpoints**: 146

## Quick Navigation

### Routers

- [attendance](#attendance) - 1 endpoints
- [awards](#awards) - 3 endpoints
- [broadcast](#broadcast) - 2 endpoints
- [conference](#conference) - 2 endpoints
- [division](#division) - 2 endpoints
- [draft](#draft) - 3 endpoints
- [games](#games) - 11 endpoints
- [game_pace](#game_pace) - 1 endpoints
- [high_low](#high_low) - 2 endpoints
- [job](#job) - 4 endpoints
- [league](#league) - 11 endpoints
- [milestones](#milestones) - 6 endpoints
- [misc](#misc) - 54 endpoints
- [people](#people) - 7 endpoints
- [schedule](#schedule) - 5 endpoints
- [season](#season) - 3 endpoints
- [sports](#sports) - 4 endpoints
- [standings](#standings) - 2 endpoints
- [stats](#stats) - 3 endpoints
- [teams](#teams) - 15 endpoints
- [transactions](#transactions) - 1 endpoints
- [uniforms](#uniforms) - 2 endpoints
- [venues](#venues) - 2 endpoints

---

## Attendance

**Endpoints**: 1
**Details**: See [full documentation](response-examples/attendance/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/attendance` | [`GET_attendance.json`](response-examples/attendance/GET_attendance.json) |

## Awards

**Endpoints**: 3
**Details**: See [full documentation](response-examples/awards/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/awards` | [`GET_awards.json`](response-examples/awards/GET_awards.json) |
| `GET` | `/api/v1/awards/{award_id}` | [`GET_awards_award_id.json`](response-examples/awards/GET_awards_award_id.json) |
| `GET` | `/api/v1/awards/{award_id}/recipients` | [`GET_awards_award_id_recipients.json`](response-examples/awards/GET_awards_award_id_recipients.json) |

## Broadcast

**Endpoints**: 2
**Details**: See [full documentation](response-examples/broadcast/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/broadcast` | [`GET_broadcast.json`](response-examples/broadcast/GET_broadcast.json) |
| `GET` | `/api/v1/broadcasters` | [`GET_broadcasters.json`](response-examples/broadcast/GET_broadcasters.json) |

## Conference

**Endpoints**: 2
**Details**: See [full documentation](response-examples/conference/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/conferences` | [`GET_conferences.json`](response-examples/conference/GET_conferences.json) |
| `GET` | `/api/v1/conferences/{conference_id}` | [`GET_conferences_conference_id.json`](response-examples/conference/GET_conferences_conference_id.json) |

## Division

**Endpoints**: 2
**Details**: See [full documentation](response-examples/division/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/divisions` | [`GET_divisions.json`](response-examples/division/GET_divisions.json) |
| `GET` | `/api/v1/divisions/{division_id}` | [`GET_divisions_division_id.json`](response-examples/division/GET_divisions_division_id.json) |

## Draft

**Endpoints**: 3
**Details**: See [full documentation](response-examples/draft/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/draft/{year}` | [`GET_draft_year.json`](response-examples/draft/GET_draft_year.json) |
| `GET` | `/api/v1/draft/{year}/latest` | [`GET_draft_year_latest.json`](response-examples/draft/GET_draft_year_latest.json) |
| `GET` | `/api/v1/draft/prospects/{year}` | [`GET_draft_prospects_year.json`](response-examples/draft/GET_draft_prospects_year.json) |

## Games

**Endpoints**: 11
**Details**: See [full documentation](response-examples/games/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1.1/game/{game_pk}/feed/live` | [`GET_game_game_pk_feed_live.json`](response-examples/games/GET_game_game_pk_feed_live.json) |
| `GET` | `/api/v1.1/game/{game_pk}/feed/live/diffPatch` | [`GET_game_game_pk_feed_live_diffpatch.json`](response-examples/games/GET_game_game_pk_feed_live_diffpatch.json) |
| `GET` | `/api/v1.1/game/{game_pk}/feed/live/timestamps` | [`GET_game_game_pk_feed_live_timestamps.json`](response-examples/games/GET_game_game_pk_feed_live_timestamps.json) |
| `GET` | `/api/v1/game/{game_pk}/contextMetrics` | [`GET_game_game_pk_contextmetrics.json`](response-examples/games/GET_game_game_pk_contextmetrics.json) |
| `GET` | `/api/v1/game/{game_pk}/winProbability` | [`GET_game_game_pk_winprobability.json`](response-examples/games/GET_game_game_pk_winprobability.json) |
| `GET` | `/api/v1/game/{game_pk}/withMetrics` | [`GET_game_game_pk_withmetrics.json`](response-examples/games/GET_game_game_pk_withmetrics.json) |
| `GET` | `/api/v1/game/{game_pk}/boxscore` | [`GET_game_game_pk_boxscore.json`](response-examples/games/GET_game_game_pk_boxscore.json) |
| `GET` | `/api/v1/game/{game_pk}/content` | [`GET_game_game_pk_content.json`](response-examples/games/GET_game_game_pk_content.json) |
| `GET` | `/api/v1/game/{game_pk}/linescore` | [`GET_game_game_pk_linescore.json`](response-examples/games/GET_game_game_pk_linescore.json) |
| `GET` | `/api/v1/game/{game_pk}/playByPlay` | [`GET_game_game_pk_playbyplay.json`](response-examples/games/GET_game_game_pk_playbyplay.json) |
| `GET` | `/api/v1/game/changes` | [`GET_game_changes.json`](response-examples/games/GET_game_changes.json) |

## Game Pace

**Endpoints**: 1
**Details**: See [full documentation](response-examples/game_pace/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/gamePace` | [`GET_gamepace.json`](response-examples/game_pace/GET_gamepace.json) |

## High Low

**Endpoints**: 2
**Details**: See [full documentation](response-examples/high_low/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/highLow/types` | [`GET_highlow_types.json`](response-examples/high_low/GET_highlow_types.json) |
| `GET` | `/api/v1/highLow/{high_low_type}` | [`GET_highlow_high_low_type.json`](response-examples/high_low/GET_highlow_high_low_type.json) |

## Job

**Endpoints**: 4
**Details**: See [full documentation](response-examples/job/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/jobs` | [`GET_jobs.json`](response-examples/job/GET_jobs.json) |
| `GET` | `/api/v1/jobs/datacasters` | [`GET_jobs_datacasters.json`](response-examples/job/GET_jobs_datacasters.json) |
| `GET` | `/api/v1/jobs/officialScorers` | [`GET_jobs_officialscorers.json`](response-examples/job/GET_jobs_officialscorers.json) |
| `GET` | `/api/v1/jobs/umpires` | [`GET_jobs_umpires.json`](response-examples/job/GET_jobs_umpires.json) |

## League

**Endpoints**: 11
**Details**: See [full documentation](response-examples/league/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/league` | [`GET_league.json`](response-examples/league/GET_league.json) |
| `GET` | `/api/v1/league/{league_id}/allStarBallot` | [`GET_league_league_id_allstarballot.json`](response-examples/league/GET_league_league_id_allstarballot.json) |
| `GET` | `/api/v1/league/{league_id}/allStarFinalVote` | [`GET_league_league_id_allstarfinalvote.json`](response-examples/league/GET_league_league_id_allstarfinalvote.json) |
| `GET` | `/api/v1/league/{league_id}/allStarWriteIns` | [`GET_league_league_id_allstarwriteins.json`](response-examples/league/GET_league_league_id_allstarwriteins.json) |
| `GET` | `/api/v1/league/{league_id}` | [`GET_league_league_id.json`](response-examples/league/GET_league_league_id.json) |
| `GET` | `/api/v1/leagues` | [`GET_leagues.json`](response-examples/league/GET_leagues.json) |
| `GET` | `/api/v1/leagues/allStarBallot` | [`GET_leagues_allstarballot.json`](response-examples/league/GET_leagues_allstarballot.json) |
| `GET` | `/api/v1/leagues/{league_id}/allStarBallot` | [`GET_leagues_league_id_allstarballot.json`](response-examples/league/GET_leagues_league_id_allstarballot.json) |
| `GET` | `/api/v1/leagues/{league_id}/allStarFinalVote` | [`GET_leagues_league_id_allstarfinalvote.json`](response-examples/league/GET_leagues_league_id_allstarfinalvote.json) |
| `GET` | `/api/v1/leagues/{league_id}/allStarWriteIns` | [`GET_leagues_league_id_allstarwriteins.json`](response-examples/league/GET_leagues_league_id_allstarwriteins.json) |
| `GET` | `/api/v1/leagues/{league_id}` | [`GET_leagues_league_id.json`](response-examples/league/GET_leagues_league_id.json) |

## Milestones

**Endpoints**: 6
**Details**: See [full documentation](response-examples/milestones/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/achievementStatuses` | [`GET_achievementstatuses.json`](response-examples/milestones/GET_achievementstatuses.json) |
| `GET` | `/api/v1/milestoneDurations` | [`GET_milestonedurations.json`](response-examples/milestones/GET_milestonedurations.json) |
| `GET` | `/api/v1/milestoneLookups` | [`GET_milestonelookups.json`](response-examples/milestones/GET_milestonelookups.json) |
| `GET` | `/api/v1/milestoneStatistics` | [`GET_milestonestatistics.json`](response-examples/milestones/GET_milestonestatistics.json) |
| `GET` | `/api/v1/milestoneTypes` | [`GET_milestonetypes.json`](response-examples/milestones/GET_milestonetypes.json) |
| `GET` | `/api/v1/milestones` | [`GET_milestones.json`](response-examples/milestones/GET_milestones.json) |

## Misc

**Endpoints**: 54
**Details**: See [full documentation](response-examples/misc/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/baseballStats` | [`GET_baseballstats.json`](response-examples/misc/GET_baseballstats.json) |
| `GET` | `/api/v1/broadcastAvailability` | [`GET_broadcastavailability.json`](response-examples/misc/GET_broadcastavailability.json) |
| `GET` | `/api/v1/coachingVideoTypes` | [`GET_coachingvideotypes.json`](response-examples/misc/GET_coachingvideotypes.json) |
| `GET` | `/api/v1/eventStatus` | [`GET_eventstatus.json`](response-examples/misc/GET_eventstatus.json) |
| `GET` | `/api/v1/eventTypes` | [`GET_eventtypes.json`](response-examples/misc/GET_eventtypes.json) |
| `GET` | `/api/v1/fielderDetailTypes` | [`GET_fielderdetailtypes.json`](response-examples/misc/GET_fielderdetailtypes.json) |
| `GET` | `/api/v1/freeGameTypes` | [`GET_freegametypes.json`](response-examples/misc/GET_freegametypes.json) |
| `GET` | `/api/v1/gameStatus` | [`GET_gamestatus.json`](response-examples/misc/GET_gamestatus.json) |
| `GET` | `/api/v1/gameTypes` | [`GET_gametypes.json`](response-examples/misc/GET_gametypes.json) |
| `GET` | `/api/v1/gamedayTypes` | [`GET_gamedaytypes.json`](response-examples/misc/GET_gamedaytypes.json) |
| `GET` | `/api/v1/groupByTypes` | [`GET_groupbytypes.json`](response-examples/misc/GET_groupbytypes.json) |
| `GET` | `/api/v1/hitTrajectories` | [`GET_hittrajectories.json`](response-examples/misc/GET_hittrajectories.json) |
| `GET` | `/api/v1/jobTypes` | [`GET_jobtypes.json`](response-examples/misc/GET_jobtypes.json) |
| `GET` | `/api/v1/languages` | [`GET_languages.json`](response-examples/misc/GET_languages.json) |
| `GET` | `/api/v1/leagueLeaderTypes` | [`GET_leagueleadertypes.json`](response-examples/misc/GET_leagueleadertypes.json) |
| `GET` | `/api/v1/logicalEvents` | [`GET_logicalevents.json`](response-examples/misc/GET_logicalevents.json) |
| `GET` | `/api/v1/lookup/values/all` | [`GET_lookup_values_all.json`](response-examples/misc/GET_lookup_values_all.json) |
| `GET` | `/api/v1/mediaState` | [`GET_mediastate.json`](response-examples/misc/GET_mediastate.json) |
| `GET` | `/api/v1/metrics` | [`GET_metrics.json`](response-examples/misc/GET_metrics.json) |
| `GET` | `/api/v1/moundVisitTypes` | [`GET_moundvisittypes.json`](response-examples/misc/GET_moundvisittypes.json) |
| `GET` | `/api/v1/performerTypes` | [`GET_performertypes.json`](response-examples/misc/GET_performertypes.json) |
| `GET` | `/api/v1/pitchCodes` | [`GET_pitchcodes.json`](response-examples/misc/GET_pitchcodes.json) |
| `GET` | `/api/v1/pitchTypes` | [`GET_pitchtypes.json`](response-examples/misc/GET_pitchtypes.json) |
| `GET` | `/api/v1/platforms` | [`GET_platforms.json`](response-examples/misc/GET_platforms.json) |
| `GET` | `/api/v1/playerStatusCodes` | [`GET_playerstatuscodes.json`](response-examples/misc/GET_playerstatuscodes.json) |
| `GET` | `/api/v1/positions` | [`GET_positions.json`](response-examples/misc/GET_positions.json) |
| `GET` | `/api/v1/reviewReasons` | [`GET_reviewreasons.json`](response-examples/misc/GET_reviewreasons.json) |
| `GET` | `/api/v1/roofTypes` | [`GET_rooftypes.json`](response-examples/misc/GET_rooftypes.json) |
| `GET` | `/api/v1/rosterTypes` | [`GET_rostertypes.json`](response-examples/misc/GET_rostertypes.json) |
| `GET` | `/api/v1/ruleSettings` | [`GET_rulesettings.json`](response-examples/misc/GET_rulesettings.json) |
| `GET` | `/api/v1/runnerDetailTypes` | [`GET_runnerdetailtypes.json`](response-examples/misc/GET_runnerdetailtypes.json) |
| `GET` | `/api/v1/scheduleEventTypes` | [`GET_scheduleeventtypes.json`](response-examples/misc/GET_scheduleeventtypes.json) |
| `GET` | `/api/v1/scheduleTypes` | [`GET_scheduletypes.json`](response-examples/misc/GET_scheduletypes.json) |
| `GET` | `/api/v1/situationCodes` | [`GET_situationcodes.json`](response-examples/misc/GET_situationcodes.json) |
| `GET` | `/api/v1/sky` | [`GET_sky.json`](response-examples/misc/GET_sky.json) |
| `GET` | `/api/v1/sortModifiers` | [`GET_sortmodifiers.json`](response-examples/misc/GET_sortmodifiers.json) |
| `GET` | `/api/v1/standingsTypes` | [`GET_standingstypes.json`](response-examples/misc/GET_standingstypes.json) |
| `GET` | `/api/v1/statFields` | [`GET_statfields.json`](response-examples/misc/GET_statfields.json) |
| `GET` | `/api/v1/statGroups` | [`GET_statgroups.json`](response-examples/misc/GET_statgroups.json) |
| `GET` | `/api/v1/statTypes` | [`GET_stattypes.json`](response-examples/misc/GET_stattypes.json) |
| `GET` | `/api/v1/statcastPositionTypes` | [`GET_statcastpositiontypes.json`](response-examples/misc/GET_statcastpositiontypes.json) |
| `GET` | `/api/v1/stats/search/config` | [`GET_stats_search_config.json`](response-examples/misc/GET_stats_search_config.json) |
| `GET` | `/api/v1/stats/search/groupByTypes` | [`GET_stats_search_groupbytypes.json`](response-examples/misc/GET_stats_search_groupbytypes.json) |
| `GET` | `/api/v1/stats/search/params` | [`GET_stats_search_params.json`](response-examples/misc/GET_stats_search_params.json) |
| `GET` | `/api/v1/stats/search/stats` | [`GET_stats_search_stats.json`](response-examples/misc/GET_stats_search_stats.json) |
| `GET` | `/api/v1/trackingSoftwareVersions` | [`GET_trackingsoftwareversions.json`](response-examples/misc/GET_trackingsoftwareversions.json) |
| `GET` | `/api/v1/trackingSystemOwners` | [`GET_trackingsystemowners.json`](response-examples/misc/GET_trackingsystemowners.json) |
| `GET` | `/api/v1/trackingVendors` | [`GET_trackingvendors.json`](response-examples/misc/GET_trackingvendors.json) |
| `GET` | `/api/v1/trackingVersions` | [`GET_trackingversions.json`](response-examples/misc/GET_trackingversions.json) |
| `GET` | `/api/v1/transactionTypes` | [`GET_transactiontypes.json`](response-examples/misc/GET_transactiontypes.json) |
| `GET` | `/api/v1/videoResolutionTypes` | [`GET_videoresolutiontypes.json`](response-examples/misc/GET_videoresolutiontypes.json) |
| `GET` | `/api/v1/violationTypes` | [`GET_violationtypes.json`](response-examples/misc/GET_violationtypes.json) |
| `GET` | `/api/v1/weatherTrajectoryConfidences` | [`GET_weathertrajectoryconfidences.json`](response-examples/misc/GET_weathertrajectoryconfidences.json) |
| `GET` | `/api/v1/windDirection` | [`GET_winddirection.json`](response-examples/misc/GET_winddirection.json) |

## People

**Endpoints**: 7
**Details**: See [full documentation](response-examples/people/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/people/changes` | [`GET_people_changes.json`](response-examples/people/GET_people_changes.json) |
| `GET` | `/api/v1/people/freeAgents` | [`GET_people_freeagents.json`](response-examples/people/GET_people_freeagents.json) |
| `GET` | `/api/v1/people/search` | [`GET_people_search.json`](response-examples/people/GET_people_search.json) |
| `GET` | `/api/v1/people/608070` | [`GET_people_608070.json`](response-examples/people/GET_people_608070.json) |
| `GET` | `/api/v1/people/608070/awards` | [`GET_people_608070_awards.json`](response-examples/people/GET_people_608070_awards.json) |
| `GET` | `/api/v1/people/608070/stats` | [`GET_people_608070_stats.json`](response-examples/people/GET_people_608070_stats.json) |
| `GET` | `/api/v1/people/608070/stats/game/{game_pk}` | [`GET_people_608070_stats_game_game_pk.json`](response-examples/people/GET_people_608070_stats_game_game_pk.json) |

## Schedule

**Endpoints**: 5
**Details**: See [full documentation](response-examples/schedule/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/schedule/games/tied` | [`GET_schedule_games_tied.json`](response-examples/schedule/GET_schedule_games_tied.json) |
| `GET` | `/api/v1/schedule/postseason/series` | [`GET_schedule_postseason_series.json`](response-examples/schedule/GET_schedule_postseason_series.json) |
| `GET` | `/api/v1/schedule/postseason/tuneIn` | [`GET_schedule_postseason_tunein.json`](response-examples/schedule/GET_schedule_postseason_tunein.json) |
| `GET` | `/api/v1/schedule/postseason` | [`GET_schedule_postseason.json`](response-examples/schedule/GET_schedule_postseason.json) |
| `GET` | `/api/v1/schedule` | [`GET_schedule.json`](response-examples/schedule/GET_schedule.json) |

## Season

**Endpoints**: 3
**Details**: See [full documentation](response-examples/season/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/seasons` | [`GET_seasons.json`](response-examples/season/GET_seasons.json) |
| `GET` | `/api/v1/seasons/all` | [`GET_seasons_all.json`](response-examples/season/GET_seasons_all.json) |
| `GET` | `/api/v1/seasons/{season_id}` | [`GET_seasons_season_id.json`](response-examples/season/GET_seasons_season_id.json) |

## Sports

**Endpoints**: 4
**Details**: See [full documentation](response-examples/sports/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/sports` | [`GET_sports.json`](response-examples/sports/GET_sports.json) |
| `GET` | `/api/v1/sports/{sport_id}` | [`GET_sports_sport_id.json`](response-examples/sports/GET_sports_sport_id.json) |
| `GET` | `/api/v1/sports/{sport_id}/allSportBallot` | [`GET_sports_sport_id_allsportballot.json`](response-examples/sports/GET_sports_sport_id_allsportballot.json) |
| `GET` | `/api/v1/sports/{sport_id}/players` | [`GET_sports_sport_id_players.json`](response-examples/sports/GET_sports_sport_id_players.json) |

## Standings

**Endpoints**: 2
**Details**: See [full documentation](response-examples/standings/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/standings` | [`GET_standings.json`](response-examples/standings/GET_standings.json) |
| `GET` | `/api/v1/standings/{standings_type}` | [`GET_standings_standings_type.json`](response-examples/standings/GET_standings_standings_type.json) |

## Stats

**Endpoints**: 3
**Details**: See [full documentation](response-examples/stats/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/stats` | [`GET_stats.json`](response-examples/stats/GET_stats.json) |
| `GET` | `/api/v1/stats/grouped` | [`GET_stats_grouped.json`](response-examples/stats/GET_stats_grouped.json) |
| `GET` | `/api/v1/stats/leaders` | [`GET_stats_leaders.json`](response-examples/stats/GET_stats_leaders.json) |

## Teams

**Endpoints**: 15
**Details**: See [full documentation](response-examples/teams/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/teams` | [`GET_teams.json`](response-examples/teams/GET_teams.json) |
| `GET` | `/api/v1/teams/affiliates` | [`GET_teams_affiliates.json`](response-examples/teams/GET_teams_affiliates.json) |
| `GET` | `/api/v1/teams/history` | [`GET_teams_history.json`](response-examples/teams/GET_teams_history.json) |
| `GET` | `/api/v1/teams/stats` | [`GET_teams_stats.json`](response-examples/teams/GET_teams_stats.json) |
| `GET` | `/api/v1/teams/stats/leaders` | [`GET_teams_stats_leaders.json`](response-examples/teams/GET_teams_stats_leaders.json) |
| `GET` | `/api/v1/teams/{team_id}` | [`GET_teams_team_id.json`](response-examples/teams/GET_teams_team_id.json) |
| `GET` | `/api/v1/teams/{team_id}/affiliates` | [`GET_teams_team_id_affiliates.json`](response-examples/teams/GET_teams_team_id_affiliates.json) |
| `GET` | `/api/v1/teams/{team_id}/alumni` | [`GET_teams_team_id_alumni.json`](response-examples/teams/GET_teams_team_id_alumni.json) |
| `GET` | `/api/v1/teams/{team_id}/coaches` | [`GET_teams_team_id_coaches.json`](response-examples/teams/GET_teams_team_id_coaches.json) |
| `GET` | `/api/v1/teams/{team_id}/history` | [`GET_teams_team_id_history.json`](response-examples/teams/GET_teams_team_id_history.json) |
| `GET` | `/api/v1/teams/{team_id}/leaders` | [`GET_teams_team_id_leaders.json`](response-examples/teams/GET_teams_team_id_leaders.json) |
| `GET` | `/api/v1/teams/{team_id}/personnel` | [`GET_teams_team_id_personnel.json`](response-examples/teams/GET_teams_team_id_personnel.json) |
| `GET` | `/api/v1/teams/{team_id}/roster` | [`GET_teams_team_id_roster.json`](response-examples/teams/GET_teams_team_id_roster.json) |
| `GET` | `/api/v1/teams/{team_id}/roster/{roster_type}` | [`GET_teams_team_id_roster_roster_type.json`](response-examples/teams/GET_teams_team_id_roster_roster_type.json) |
| `GET` | `/api/v1/teams/{team_id}/stats` | [`GET_teams_team_id_stats.json`](response-examples/teams/GET_teams_team_id_stats.json) |

## Transactions

**Endpoints**: 1
**Details**: See [full documentation](response-examples/transactions/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/transactions` | [`GET_transactions.json`](response-examples/transactions/GET_transactions.json) |

## Uniforms

**Endpoints**: 2
**Details**: See [full documentation](response-examples/uniforms/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/uniforms/game` | [`GET_uniforms_game.json`](response-examples/uniforms/GET_uniforms_game.json) |
| `GET` | `/api/v1/uniforms/team` | [`GET_uniforms_team.json`](response-examples/uniforms/GET_uniforms_team.json) |

## Venues

**Endpoints**: 2
**Details**: See [full documentation](response-examples/venues/README.md)

| Method | Endpoint | Response File |
|--------|----------|---------------|
| `GET` | `/api/v1/venues` | [`GET_venues.json`](response-examples/venues/GET_venues.json) |
| `GET` | `/api/v1/venues/{venue_id}` | [`GET_venues_venue_id.json`](response-examples/venues/GET_venues_venue_id.json) |


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

