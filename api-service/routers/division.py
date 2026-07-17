from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Division"])


@router.get("/api/v1/divisions")
async def get_divisions(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/divisions", x_api_key)


@router.get("/api/v1/divisions/{division_id}")
async def get_division(
    division_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/divisions/{division_id}", x_api_key)
