from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Venues"])


@router.get("/api/v1/venues")
async def get_venues(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/venues", x_api_key)


@router.get("/api/v1/venues/{venue_id}")
async def get_venue(
    venue_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/venues/{venue_id}", x_api_key)
