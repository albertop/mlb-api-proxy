from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Job"])


@router.get("/api/v1/jobs")
async def get_jobs(request: Request, x_api_key: str | None = Header(None)) -> Response:
    return await forward_get(request, "/api/v1/jobs", x_api_key)


@router.get("/api/v1/jobs/datacasters")
async def get_jobs_datacasters(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/jobs/datacasters", x_api_key)


@router.get("/api/v1/jobs/officialScorers")
async def get_jobs_official_scorers(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/jobs/officialScorers", x_api_key)


@router.get("/api/v1/jobs/umpires")
async def get_jobs_umpires(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/jobs/umpires", x_api_key)
