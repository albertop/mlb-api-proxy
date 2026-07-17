from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Awards"])


@router.get("/api/v1/awards")
async def get_awards(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/awards", x_api_key)


@router.get("/api/v1/awards/{award_id}")
async def get_award(
    award_id: str,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/awards/{award_id}", x_api_key)


@router.get("/api/v1/awards/{award_id}/recipients")
async def get_award_recipients(
    award_id: str,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/awards/{award_id}/recipients", x_api_key)
