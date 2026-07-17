from fastapi import APIRouter, Header, Request
from fastapi.responses import Response

from proxy import forward_get

router = APIRouter(tags=["Game"])


@router.get("/api/v1.1/game/{game_pk}/feed/live")
async def get_game_feed_live(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1.1/game/{game_pk}/feed/live", x_api_key)


@router.get("/api/v1.1/game/{game_pk}/feed/live/diffPatch")
async def get_game_feed_live_diff_patch(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1.1/game/{game_pk}/feed/live/diffPatch", x_api_key)


@router.get("/api/v1.1/game/{game_pk}/feed/live/timestamps")
async def get_game_feed_live_timestamps(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1.1/game/{game_pk}/feed/live/timestamps", x_api_key)


@router.get("/api/v1/game/{game_pk}/contextMetrics")
async def get_game_context_metrics(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/game/{game_pk}/contextMetrics", x_api_key)


@router.get("/api/v1/game/{game_pk}/winProbability")
async def get_game_win_probability(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/game/{game_pk}/winProbability", x_api_key)


@router.get("/api/v1/game/{game_pk}/withMetrics")
async def get_game_with_metrics(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/game/{game_pk}/withMetrics", x_api_key)


@router.get("/api/v1/game/{game_pk}/boxscore")
async def get_game_boxscore(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/game/{game_pk}/boxscore", x_api_key)


@router.get("/api/v1/game/{game_pk}/content")
async def get_game_content(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/game/{game_pk}/content", x_api_key)


@router.get("/api/v1/game/{game_pk}/linescore")
async def get_game_linescore(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/game/{game_pk}/linescore", x_api_key)


@router.get("/api/v1/game/{game_pk}/playByPlay")
async def get_game_play_by_play(
    game_pk: int,
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, f"/api/v1/game/{game_pk}/playByPlay", x_api_key)


@router.get("/api/v1/game/changes")
async def get_game_changes(
    request: Request,
    x_api_key: str | None = Header(None),
) -> Response:
    return await forward_get(request, "/api/v1/game/changes", x_api_key)
