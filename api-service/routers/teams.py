from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Teams"])


@router.get("/api/v1/teams")
async def get_teams(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/teams", x_api_key)


@router.get("/api/v1/teams/affiliates")
async def get_teams_affiliates(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/teams/affiliates", x_api_key)


@router.get("/api/v1/teams/history")
async def get_teams_history(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/teams/history", x_api_key)


@router.get("/api/v1/teams/stats")
async def get_teams_stats(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/teams/stats", x_api_key)


@router.get("/api/v1/teams/stats/leaders")
async def get_teams_stats_leaders(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/teams/stats/leaders", x_api_key)


@router.get("/api/v1/teams/{team_id}")
async def get_team(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}", x_api_key)


@router.get("/api/v1/teams/{team_id}/affiliates")
async def get_team_affiliates(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/affiliates", x_api_key)


@router.get("/api/v1/teams/{team_id}/alumni")
async def get_team_alumni(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/alumni", x_api_key)


@router.get("/api/v1/teams/{team_id}/coaches")
async def get_team_coaches(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/coaches", x_api_key)


@router.get("/api/v1/teams/{team_id}/history")
async def get_team_history(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/history", x_api_key)


@router.get("/api/v1/teams/{team_id}/leaders")
async def get_team_leaders(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/leaders", x_api_key)


@router.get("/api/v1/teams/{team_id}/personnel")
async def get_team_personnel(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/personnel", x_api_key)


@router.get("/api/v1/teams/{team_id}/roster")
async def get_team_roster(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/roster", x_api_key)


@router.get("/api/v1/teams/{team_id}/roster/{roster_type}")
async def get_team_roster_by_type(
    team_id: int,
    roster_type: str,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/roster/{roster_type}", x_api_key)


@router.get("/api/v1/teams/{team_id}/stats")
async def get_team_stats(
    team_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/teams/{team_id}/stats", x_api_key)
