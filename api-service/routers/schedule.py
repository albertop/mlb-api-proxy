from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Schedule"])


@router.get("/api/v1/schedule/games/tied")
async def get_schedule_games_tied(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/schedule/games/tied", x_api_key)


@router.get("/api/v1/schedule/postseason/series")
async def get_schedule_postseason_series(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/schedule/postseason/series", x_api_key)


@router.get("/api/v1/schedule/postseason/tuneIn")
async def get_schedule_postseason_tune_in(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/schedule/postseason/tuneIn", x_api_key)


@router.get("/api/v1/schedule/postseason")
async def get_schedule_postseason(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/schedule/postseason", x_api_key)


@router.get("/api/v1/schedule/{schedule_type}")
async def get_schedule_by_type(
    schedule_type: str,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/schedule/{schedule_type}", x_api_key)


@router.get("/api/v1/schedule")
async def get_schedule(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/schedule", x_api_key)
