from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Stats"])


@router.get("/api/v1/stats")
async def get_stats(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/stats", x_api_key)


@router.get("/api/v1/stats/grouped")
async def get_stats_grouped(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/stats/grouped", x_api_key)


@router.get("/api/v1/stats/leaders")
async def get_stats_leaders(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/stats/leaders", x_api_key)
