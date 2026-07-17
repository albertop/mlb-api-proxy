from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Milestones"])


@router.get("/api/v1/achievementStatuses")
async def get_achievement_statuses(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/achievementStatuses", x_api_key)


@router.get("/api/v1/milestoneDurations")
async def get_milestone_durations(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/milestoneDurations", x_api_key)


@router.get("/api/v1/milestoneLookups")
async def get_milestone_lookups(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/milestoneLookups", x_api_key)


@router.get("/api/v1/milestoneStatistics")
async def get_milestone_statistics(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/milestoneStatistics", x_api_key)


@router.get("/api/v1/milestoneTypes")
async def get_milestone_types(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/milestoneTypes", x_api_key)


@router.get("/api/v1/milestones")
async def get_milestones(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/milestones", x_api_key)
