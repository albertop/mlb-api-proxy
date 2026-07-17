from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Sports"])


@router.get("/api/v1/sports")
async def get_sports(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/sports", x_api_key)


@router.get("/api/v1/sports/{sport_id}")
async def get_sport(
    sport_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/sports/{sport_id}", x_api_key)


@router.get("/api/v1/sports/{sport_id}/allSportBallot")
async def get_sport_all_sport_ballot(
    sport_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/sports/{sport_id}/allSportBallot", x_api_key)


@router.get("/api/v1/sports/{sport_id}/players")
async def get_sport_players(
    sport_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/sports/{sport_id}/players", x_api_key)
