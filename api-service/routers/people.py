from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Person"])


@router.get("/api/v1/people/changes")
async def get_people_changes(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/people/changes", x_api_key)


@router.get("/api/v1/people/freeAgents")
async def get_free_agents(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/people/freeAgents", x_api_key)


@router.get("/api/v1/people/search")
async def search_people(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/people/search", x_api_key)


@router.get("/api/v1/people/{person_id}")
async def get_person(
    person_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/people/{person_id}", x_api_key)


@router.get("/api/v1/people/{person_id}/awards")
async def get_person_awards(
    person_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/people/{person_id}/awards", x_api_key)


@router.get("/api/v1/people/{person_id}/stats")
async def get_person_stats(
    person_id: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/people/{person_id}/stats", x_api_key)


@router.get("/api/v1/people/{person_id}/stats/game/{game_pk}")
async def get_person_stats_game(
    person_id: int,
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/people/{person_id}/stats/game/{game_pk}", x_api_key)
