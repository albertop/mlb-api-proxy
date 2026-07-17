from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Uniforms"])


@router.get("/api/v1/uniforms/game")
async def get_uniforms_game(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/uniforms/game", x_api_key)


@router.get("/api/v1/uniforms/team")
async def get_uniforms_team(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/uniforms/team", x_api_key)
