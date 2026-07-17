from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Standings"])


@router.get("/api/v1/standings")
async def get_standings(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/standings", x_api_key)


@router.get("/api/v1/standings/{standings_type}")
async def get_standings_by_type(
    standings_type: str,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/standings/{standings_type}", x_api_key)
