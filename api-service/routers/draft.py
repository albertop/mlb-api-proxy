from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Draft"])


@router.get("/api/v1/draft/{year}")
async def get_draft_by_year(
    year: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/draft/{year}", x_api_key)


@router.get("/api/v1/draft/{year}/latest")
async def get_draft_latest(
    year: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/draft/{year}/latest", x_api_key)


@router.get("/api/v1/draft/prospects/{year}")
async def get_draft_prospects_by_year(
    year: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/draft/prospects/{year}", x_api_key)
