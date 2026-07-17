from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Broadcast"])


@router.get("/api/v1/broadcast")
async def get_broadcast(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/broadcast", x_api_key)


@router.get("/api/v1/broadcasters")
async def get_broadcasters(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/broadcasters", x_api_key)
