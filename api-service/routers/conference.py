from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Conference"])


@router.get("/api/v1/conferences")
async def get_conferences(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/conferences", x_api_key)


@router.get("/api/v1/conferences/{conference_id}")
async def get_conference(
    conference_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/conferences/{conference_id}", x_api_key)
