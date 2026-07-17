from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Miscellaneous"])


@router.get("/api/v1/baseballStats")
async def get_baseball_stats(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/baseballStats", x_api_key)


@router.get("/api/v1/broadcastAvailability")
async def get_broadcast_availability(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/broadcastAvailability", x_api_key)


@router.get("/api/v1/coachingVideoTypes")
async def get_coaching_video_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/coachingVideoTypes", x_api_key)


@router.get("/api/v1/eventStatus")
async def get_event_status(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/eventStatus", x_api_key)


@router.get("/api/v1/eventTypes")
async def get_event_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/eventTypes", x_api_key)


@router.get("/api/v1/fielderDetailTypes")
async def get_fielder_detail_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/fielderDetailTypes", x_api_key)


@router.get("/api/v1/freeGameTypes")
async def get_free_game_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/freeGameTypes", x_api_key)


@router.get("/api/v1/gameStatus")
async def get_game_status(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/gameStatus", x_api_key)


@router.get("/api/v1/gameTypes")
async def get_game_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/gameTypes", x_api_key)


@router.get("/api/v1/gamedayTypes")
async def get_gameday_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/gamedayTypes", x_api_key)


@router.get("/api/v1/groupByTypes")
async def get_group_by_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/groupByTypes", x_api_key)


@router.get("/api/v1/hitTrajectories")
async def get_hit_trajectories(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/hitTrajectories", x_api_key)


@router.get("/api/v1/jobTypes")
async def get_job_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/jobTypes", x_api_key)


@router.get("/api/v1/languages")
async def get_languages(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/languages", x_api_key)


@router.get("/api/v1/leagueLeaderTypes")
async def get_league_leader_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/leagueLeaderTypes", x_api_key)


@router.get("/api/v1/logicalEvents")
async def get_logical_events(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/logicalEvents", x_api_key)


@router.get("/api/v1/lookup/values/all")
async def get_lookup_values_all(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/lookup/values/all", x_api_key)


@router.get("/api/v1/mediaState")
async def get_media_state(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/mediaState", x_api_key)


@router.get("/api/v1/metrics")
async def get_metrics(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/metrics", x_api_key)


@router.get("/api/v1/moundVisitTypes")
async def get_mound_visit_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/moundVisitTypes", x_api_key)


@router.get("/api/v1/performerTypes")
async def get_performer_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/performerTypes", x_api_key)


@router.get("/api/v1/pitchCodes")
async def get_pitch_codes(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/pitchCodes", x_api_key)


@router.get("/api/v1/pitchTypes")
async def get_pitch_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/pitchTypes", x_api_key)


@router.get("/api/v1/platforms")
async def get_platforms(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/platforms", x_api_key)


@router.get("/api/v1/playerStatusCodes")
async def get_player_status_codes(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/playerStatusCodes", x_api_key)


@router.get("/api/v1/positions")
async def get_positions(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/positions", x_api_key)


@router.get("/api/v1/reviewReasons")
async def get_review_reasons(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/reviewReasons", x_api_key)


@router.get("/api/v1/roofTypes")
async def get_roof_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/roofTypes", x_api_key)


@router.get("/api/v1/rosterTypes")
async def get_roster_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/rosterTypes", x_api_key)


@router.get("/api/v1/ruleSettings")
async def get_rule_settings(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/ruleSettings", x_api_key)


@router.get("/api/v1/runnerDetailTypes")
async def get_runner_detail_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/runnerDetailTypes", x_api_key)


@router.get("/api/v1/scheduleEventTypes")
async def get_schedule_event_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/scheduleEventTypes", x_api_key)


@router.get("/api/v1/scheduleTypes")
async def get_schedule_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/scheduleTypes", x_api_key)


@router.get("/api/v1/situationCodes")
async def get_situation_codes(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/situationCodes", x_api_key)


@router.get("/api/v1/sky")
async def get_sky(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/sky", x_api_key)


@router.get("/api/v1/sortModifiers")
async def get_sort_modifiers(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/sortModifiers", x_api_key)


@router.get("/api/v1/standingsTypes")
async def get_standings_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/standingsTypes", x_api_key)


@router.get("/api/v1/statFields")
async def get_stat_fields(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/statFields", x_api_key)


@router.get("/api/v1/statGroups")
async def get_stat_groups(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/statGroups", x_api_key)


@router.get("/api/v1/statTypes")
async def get_stat_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/statTypes", x_api_key)


@router.get("/api/v1/statcastPositionTypes")
async def get_statcast_position_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/statcastPositionTypes", x_api_key)


@router.get("/api/v1/stats/search/config")
async def get_stats_search_config(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/stats/search/config", x_api_key)


@router.get("/api/v1/stats/search/groupByTypes")
async def get_stats_search_group_by_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/stats/search/groupByTypes", x_api_key)


@router.get("/api/v1/stats/search/params")
async def get_stats_search_params(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/stats/search/params", x_api_key)


@router.get("/api/v1/stats/search/stats")
async def get_stats_search_stats(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/stats/search/stats", x_api_key)


@router.get("/api/v1/trackingSoftwareVersions")
async def get_tracking_software_versions(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/trackingSoftwareVersions", x_api_key)


@router.get("/api/v1/trackingSystemOwners")
async def get_tracking_system_owners(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/trackingSystemOwners", x_api_key)


@router.get("/api/v1/trackingVendors")
async def get_tracking_vendors(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/trackingVendors", x_api_key)


@router.get("/api/v1/trackingVersions")
async def get_tracking_versions(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/trackingVersions", x_api_key)


@router.get("/api/v1/transactionTypes")
async def get_transaction_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/transactionTypes", x_api_key)


@router.get("/api/v1/videoResolutionTypes")
async def get_video_resolution_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/videoResolutionTypes", x_api_key)


@router.get("/api/v1/violationTypes")
async def get_violation_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/violationTypes", x_api_key)


@router.get("/api/v1/weatherTrajectoryConfidences")
async def get_weather_trajectory_confidences(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/weatherTrajectoryConfidences", x_api_key)


@router.get("/api/v1/windDirection")
async def get_wind_direction(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/windDirection", x_api_key)
