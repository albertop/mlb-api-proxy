from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["HighLow"])


@router.get("/api/v1/highLow/types")
async def get_high_low_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/highLow/types", x_api_key)


@router.get("/api/v1/highLow/{high_low_type}")
async def get_high_low(
    high_low_type: str,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/highLow/{high_low_type}", x_api_key)
