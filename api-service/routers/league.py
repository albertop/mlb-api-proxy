from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["League"])


@router.get("/api/v1/league")
async def get_league(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/league", x_api_key)


@router.get("/api/v1/league/{league_id}/allStarBallot")
async def get_league_all_star_ballot(
    league_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/league/{league_id}/allStarBallot", x_api_key)


@router.get("/api/v1/league/{league_id}/allStarFinalVote")
async def get_league_all_star_final_vote(
    league_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/league/{league_id}/allStarFinalVote", x_api_key)


@router.get("/api/v1/league/{league_id}/allStarWriteIns")
async def get_league_all_star_write_ins(
    league_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/league/{league_id}/allStarWriteIns", x_api_key)


@router.get("/api/v1/league/{league_id}")
async def get_league_by_id(
    league_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/league/{league_id}", x_api_key)


@router.get("/api/v1/leagues")
async def get_leagues(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/leagues", x_api_key)


@router.get("/api/v1/leagues/allStarBallot")
async def get_leagues_all_star_ballot_all(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/leagues/allStarBallot", x_api_key)


@router.get("/api/v1/leagues/{league_id}/allStarBallot")
async def get_leagues_all_star_ballot(
    league_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/leagues/{league_id}/allStarBallot", x_api_key)


@router.get("/api/v1/leagues/{league_id}/allStarFinalVote")
async def get_leagues_all_star_final_vote(
    league_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/leagues/{league_id}/allStarFinalVote", x_api_key)


@router.get("/api/v1/leagues/{league_id}/allStarWriteIns")
async def get_leagues_all_star_write_ins(
    league_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/leagues/{league_id}/allStarWriteIns", x_api_key)


@router.get("/api/v1/leagues/{league_id}")
async def get_leagues_by_id(
    league_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/leagues/{league_id}", x_api_key)
