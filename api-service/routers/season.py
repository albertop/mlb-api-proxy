from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Season"])


@router.get("/api/v1/seasons")
async def get_seasons(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/seasons", x_api_key)


@router.get("/api/v1/seasons/all")
async def get_seasons_all(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/seasons/all", x_api_key)


@router.get("/api/v1/seasons/{season_id}")
async def get_season(
    season_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/seasons/{season_id}", x_api_key)
