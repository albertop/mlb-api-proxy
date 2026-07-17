import asyncio
import json
import logging
import secrets
from collections.abc import Awaitable, Callable
from typing import Any, NamedTuple
from urllib.parse import urlencode

import httpx
import xmltodict
from cachetools import TTLCache
from fastapi import HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from stats_translations import STAT_TRANSLATIONS

# Create lowercase-keyed version for case-insensitive lookups
_STAT_TRANSLATIONS_LOWER = {k.lower(): v for k, v in STAT_TRANSLATIONS.items()}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mlb_base_url: str = Field(
        default="https://statsapi.mlb.com",
        validation_alias="MLB_BASE_URL",
    )
    app_version: str = Field(default="1.2026.10", validation_alias="APP_VERSION")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    # Comma-separated list of allowed CORS origins for the browser front-end.
    # Empty = no cross-origin access (safe default). Never use "*" in production.
    cors_allow_origins: str = Field(default="", validation_alias="CORS_ALLOW_ORIGINS")
    # Expose interactive API docs (/docs, /redoc, /openapi.json). Disable in public prod.
    enable_docs: bool = Field(default=True, validation_alias="ENABLE_DOCS")
    proxy_api_key: str = Field(validation_alias="PROXY_API_KEY")
    upstream_bearer_token: str | None = Field(
        default=None,
        validation_alias="UPSTREAM_BEARER_TOKEN",
    )
    upstream_basic_auth: str | None = Field(
        default=None,
        validation_alias="UPSTREAM_BASIC_AUTH",
    )
    upstream_timeout_seconds: float = Field(
        default=30.0,
        validation_alias="UPSTREAM_TIMEOUT_SECONDS",
    )
    upstream_connect_timeout_seconds: float = Field(
        default=5.0,
        validation_alias="UPSTREAM_CONNECT_TIMEOUT_SECONDS",
    )
    # Connection pool limits for the shared httpx client (R1).
    upstream_max_connections: int = Field(
        default=100,
        validation_alias="UPSTREAM_MAX_CONNECTIONS",
    )
    upstream_max_keepalive_connections: int = Field(
        default=20,
        validation_alias="UPSTREAM_MAX_KEEPALIVE_CONNECTIONS",
    )
    # Retry policy for transient upstream failures (R2).
    upstream_max_retries: int = Field(
        default=2,
        validation_alias="UPSTREAM_MAX_RETRIES",
    )
    upstream_backoff_base_seconds: float = Field(
        default=0.5,
        validation_alias="UPSTREAM_BACKOFF_BASE_SECONDS",
    )
    upstream_backoff_max_seconds: float = Field(
        default=5.0,
        validation_alias="UPSTREAM_BACKOFF_MAX_SECONDS",
    )
    # In-process response cache (R3). In-process = per-worker; keep workers low.
    enable_cache: bool = Field(default=True, validation_alias="ENABLE_CACHE")
    cache_maxsize: int = Field(default=1000, validation_alias="CACHE_MAXSIZE")
    # TTL (seconds) for semi-dynamic data (schedule, standings, stats, rosters).
    cache_ttl_default: float = Field(default=300.0, validation_alias="CACHE_TTL_DEFAULT")
    # TTL (seconds) for reference/lookup data that rarely changes (teams, venues, types).
    cache_ttl_static: float = Field(default=21600.0, validation_alias="CACHE_TTL_STATIC")


class ProxyRequest(BaseModel):
    path: str
    params: list[tuple[str, str]]
    accept: str | None = None
    api_key: str | None = None


# pydantic-settings populates required fields (e.g. PROXY_API_KEY) from the
# environment/.env at runtime; mypy can't see that, hence the ignore.
settings = Settings()  # type: ignore[call-arg]

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("mlb-api-proxy")

# Suppress httpx INFO logs (like health check requests)
logging.getLogger("httpx").setLevel(logging.WARNING)

BASE_URL = settings.mlb_base_url.rstrip("/")
API_KEY = settings.proxy_api_key
UPSTREAM_BEARER_TOKEN = settings.upstream_bearer_token
UPSTREAM_BASIC_AUTH = settings.upstream_basic_auth
UPSTREAM_TIMEOUT_SECONDS = settings.upstream_timeout_seconds
UPSTREAM_CONNECT_TIMEOUT_SECONDS = settings.upstream_connect_timeout_seconds
UPSTREAM_MAX_CONNECTIONS = settings.upstream_max_connections
UPSTREAM_MAX_KEEPALIVE_CONNECTIONS = settings.upstream_max_keepalive_connections
UPSTREAM_MAX_RETRIES = settings.upstream_max_retries
UPSTREAM_BACKOFF_BASE_SECONDS = settings.upstream_backoff_base_seconds
UPSTREAM_BACKOFF_MAX_SECONDS = settings.upstream_backoff_max_seconds
CACHE_ENABLED = settings.enable_cache
CACHE_MAXSIZE = settings.cache_maxsize
CACHE_TTL_DEFAULT = settings.cache_ttl_default
CACHE_TTL_STATIC = settings.cache_ttl_static
# Parsed list of allowed CORS origins (empty when unset).
CORS_ALLOW_ORIGINS = [o.strip() for o in settings.cors_allow_origins.split(",") if o.strip()]

# Upstream status codes worth retrying (transient server/gateway errors).
# 429 is intentionally excluded: it is passed through to the caller unchanged.
RETRYABLE_STATUS_CODES = frozenset({502, 503, 504})

# --- Response cache policy (R3) -----------------------------------------------
# Live, intra-game data must never be cached (it changes second-to-second).
_NEVER_CACHE_MARKERS = (
    "/feed/live",
    "/boxscore",
    "/linescore",
    "/playbyplay",
    "/diffpatch",
    "/winprobability",
    "/contextmetrics",
    "/withmetrics",
    "/changes",
    "/currentgamestats",
)
# Reference / lookup data that rarely changes -> long TTL.
_STATIC_MARKERS = (
    "/teams",
    "/venues",
    "/sports",
    "/divisions",
    "/leagues",
    "/conferences",
    "/awards",
    "/draft",
    "/jobs",
    "/uniforms",
    "/broadcasters",
    "/languages",
    "types",
    "status",
)


def cache_ttl_for_path(path: str) -> float | None:
    """Return the cache TTL (seconds) for an upstream path, or None to skip caching."""
    p = path.lower()
    if any(marker in p for marker in _NEVER_CACHE_MARKERS):
        return None
    if any(marker in p for marker in _STATIC_MARKERS):
        return CACHE_TTL_STATIC
    return CACHE_TTL_DEFAULT


# One bounded TTLCache per distinct TTL tier; created lazily. Each is memory-bounded
# by CACHE_MAXSIZE. Access happens only between awaits, so no locking is needed on
# the single-threaded event loop.
_caches: dict[float, TTLCache] = {}
# In-flight request coalescing (single-flight) to prevent cache stampedes.
_inflight: dict[str, asyncio.Future] = {}


def _cache_for_ttl(ttl: float) -> TTLCache:
    cache = _caches.get(ttl)
    if cache is None:
        cache = TTLCache(maxsize=CACHE_MAXSIZE, ttl=ttl)
        _caches[ttl] = cache
    return cache


def _cache_key(path: str, params: list[tuple[str, str]], accept: str | None) -> str:
    # urlencode percent-encodes keys/values so a literal "&"/"=" inside a value can't
    # collide with the pair separators (e.g. ?a=1&b=2 vs ?a=1%26b=2 stay distinct).
    query = urlencode(sorted(params))
    return f"{accept or ''}|{path}?{query}"


def clear_cache() -> None:
    """Drop all cached entries (used by tests and available for admin use)."""
    _caches.clear()
    _inflight.clear()


def _json_bytes(data: Any) -> bytes:
    """Serialize to JSON bytes the same way Starlette's JSONResponse does."""
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


class FetchResult(NamedTuple):
    """Immutable, fully-rendered upstream result.

    Storing the already-serialized ``content`` (instead of a dict) means a cache hit
    or a coalesced waiter just sends the bytes — no repeated JSON serialization of
    large payloads. ``is_json`` marks a successfully transformed JSON body (cacheable).
    """

    status_code: int
    content: bytes
    media_type: str
    is_json: bool


def create_http_client() -> httpx.AsyncClient:
    """Build an httpx client with a connection pool and granular timeouts (R1/R5).

    Used both for the long-lived shared client (created in the app lifespan) and,
    as a fallback, for per-request clients when no shared client is available
    (e.g. under TestClient without lifespan).
    """
    return httpx.AsyncClient(
        timeout=httpx.Timeout(
            UPSTREAM_TIMEOUT_SECONDS,
            connect=UPSTREAM_CONNECT_TIMEOUT_SECONDS,
        ),
        limits=httpx.Limits(
            max_connections=UPSTREAM_MAX_CONNECTIONS,
            max_keepalive_connections=UPSTREAM_MAX_KEEPALIVE_CONNECTIONS,
        ),
        follow_redirects=True,
    )


def require_api_key(x_api_key: str | None) -> None:
    if not API_KEY:
        logger.error("Proxy API key missing; set PROXY_API_KEY")
        raise HTTPException(
            status_code=500,
            detail="Server misconfigured: PROXY_API_KEY not set",
        )
    # Constant-time comparison to avoid leaking the key via timing.
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        logger.warning("Unauthorized request with invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API key")


def build_upstream_headers(accept: str | None) -> dict:
    headers = {}
    if accept:
        logger.debug("Forwarding Accept header: %s", accept)
        headers["Accept"] = accept
    if UPSTREAM_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {UPSTREAM_BEARER_TOKEN}"
    elif UPSTREAM_BASIC_AUTH:
        headers["Authorization"] = f"Basic {UPSTREAM_BASIC_AUTH}"
    return headers


def should_parse_xml(content_type: str, body: str) -> bool:
    if "xml" in content_type.lower():
        logger.debug("XML detected via Content-Type: %s", content_type)
        return True
    if body.lstrip().startswith("<"):
        # Body looks like XML/HTML but the upstream didn't say so; log the real
        # Content-Type to aid debugging false positives (e.g. an HTML error page).
        logger.debug("XML inferred from leading '<'; upstream Content-Type=%r", content_type)
        return True
    return False


def strip_copyright(payload: Any) -> Any:
    """Recursively remove any ``copyright`` key from the payload (MLB nests it)."""
    if isinstance(payload, dict):
        return {key: strip_copyright(value) for key, value in payload.items() if key != "copyright"}
    if isinstance(payload, list):
        return [strip_copyright(item) for item in payload]
    return payload


def normalize_null_values(data: Any) -> Any:
    """Convert null-like string values to actual null.

    Handles values like: ".---", "-.---", "-.--", "-", "-1" which represent missing data.
    """
    NULL_LIKE_VALUES = {".---", "-.---", "-.--", "-", "-1", ""}

    if isinstance(data, dict):
        return {key: normalize_null_values(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [normalize_null_values(item) for item in data]
    elif isinstance(data, str) and data in NULL_LIKE_VALUES:
        return None
    return data


def translate_stat_fields(data: Any) -> Any:
    """Translate stat field names using STAT_TRANSLATIONS mapping.

    Recursively processes dicts and lists to rename stat fields.
    Only translates keys that exist in STAT_TRANSLATIONS.
    Case-insensitive lookup: matches keys regardless of case.
    """
    if isinstance(data, dict):
        translated = {}
        for key, value in data.items():
            # Case-insensitive lookup in the stat translations
            new_key = _STAT_TRANSLATIONS_LOWER.get(key.lower(), key)
            # Recursively translate the value
            translated[new_key] = translate_stat_fields(value)
        return translated
    elif isinstance(data, list):
        return [translate_stat_fields(item) for item in data]
    else:
        return data


def _backoff_delay(attempt: int) -> float:
    """Exponential backoff delay (seconds) for a given zero-based attempt index."""
    delay = UPSTREAM_BACKOFF_BASE_SECONDS * (2**attempt)
    return min(delay, UPSTREAM_BACKOFF_MAX_SECONDS)


async def get_with_retries(
    client: httpx.AsyncClient,
    url: str,
    *,
    params: list[tuple[str, str]],
    headers: dict,
) -> httpx.Response:
    """GET the upstream, retrying transient failures with exponential backoff (R2).

    Retries on connection/timeout errors and on ``RETRYABLE_STATUS_CODES``. GET is
    idempotent, so retries are safe. Non-retryable responses (including 4xx and 429)
    are returned as-is. Raises ``httpx.HTTPError`` if every attempt fails to connect.
    """
    last_exc: httpx.HTTPError | None = None
    total_attempts = UPSTREAM_MAX_RETRIES + 1

    for attempt in range(total_attempts):
        try:
            # httpx accepts list[tuple[str, str]] for params at runtime; mypy's
            # narrower signature flags it, so the type is annotated for the call.
            response = await client.get(url, params=params, headers=headers)  # type: ignore[arg-type]
        except httpx.HTTPError as exc:
            last_exc = exc
            if attempt + 1 >= total_attempts:
                raise
            delay = _backoff_delay(attempt)
            logger.warning(
                "Upstream transport error (attempt %d/%d): %s; retrying in %.2fs",
                attempt + 1,
                total_attempts,
                exc,
                delay,
            )
            await asyncio.sleep(delay)
            continue

        if response.status_code in RETRYABLE_STATUS_CODES and attempt + 1 < total_attempts:
            delay = _backoff_delay(attempt)
            logger.warning(
                "Upstream returned %d (attempt %d/%d); retrying in %.2fs",
                response.status_code,
                attempt + 1,
                total_attempts,
                delay,
            )
            await asyncio.sleep(delay)
            continue

        return response

    # Loop only exits via return or raise; this satisfies type-checkers.
    raise last_exc if last_exc else RuntimeError("get_with_retries exhausted without result")


async def _fetch_upstream(
    request: Request,
    url: str,
    params: list[tuple[str, str]],
    headers: dict,
    upstream_path: str,
) -> FetchResult:
    """Perform the upstream GET (with retries) and transform the body into a FetchResult."""
    # Reuse the shared pooled client when available (R1); fall back to a
    # per-request client when the app lifespan hasn't run (e.g. under TestClient).
    shared_client: httpx.AsyncClient | None = getattr(request.app.state, "http", None)
    client = shared_client or create_http_client()
    try:
        upstream = await get_with_retries(client, url, params=params, headers=headers)
    finally:
        if shared_client is None:
            await client.aclose()

    content_type = upstream.headers.get("content-type", "")
    text = upstream.text
    logger.info("Upstream status %s for %s", upstream.status_code, upstream_path)
    if upstream.status_code >= 400:
        logger.warning("Upstream error status %s for %s", upstream.status_code, upstream_path)

    if should_parse_xml(content_type, text):
        try:
            parsed = xmltodict.parse(text)
        except Exception as exc:
            logger.error("Failed to parse XML: %s", exc)
            raise HTTPException(status_code=502, detail=f"Failed to parse XML: {exc}") from exc
        body = translate_stat_fields(normalize_null_values(strip_copyright(parsed)))
        return FetchResult(upstream.status_code, _json_bytes(body), "application/json", True)

    if "json" in content_type.lower():
        try:
            payload = upstream.json()
        except ValueError:
            logger.warning("Invalid JSON from upstream; returning raw body")
            # Passthrough: forward the original bytes untouched (don't re-encode).
            return FetchResult(upstream.status_code, upstream.content, content_type or "text/plain", False)
        body = translate_stat_fields(normalize_null_values(strip_copyright(payload)))
        return FetchResult(upstream.status_code, _json_bytes(body), "application/json", True)

    # Non-JSON / non-XML (CSV, binary, other charsets): forward raw bytes verbatim so
    # the proxy never corrupts content it doesn't transform.
    logger.debug("Returning upstream raw content")
    return FetchResult(upstream.status_code, upstream.content, content_type or "text/plain", False)


def _build_response(result: FetchResult) -> Response:
    """Send the pre-rendered bytes directly — no per-request (re)serialization."""
    return Response(
        status_code=result.status_code,
        content=result.content,
        media_type=result.media_type,
    )


async def _coalesce(
    key: str,
    factory: Callable[[], Awaitable[FetchResult]],
) -> FetchResult:
    """Single-flight: run ``factory`` once per key, sharing the result with waiters (R3)."""
    existing = _inflight.get(key)
    if existing is not None:
        logger.debug("Coalescing onto in-flight upstream fetch: %s", key)
        return await existing

    loop = asyncio.get_running_loop()
    future: asyncio.Future = loop.create_future()
    _inflight[key] = future
    try:
        result = await factory()
    except BaseException as exc:
        future.set_exception(exc)
        future.exception()  # mark retrieved to avoid "never retrieved" warnings
        raise
    else:
        future.set_result(result)
        return result
    finally:
        _inflight.pop(key, None)


async def forward_get(
    request: Request,
    upstream_path: str,
    x_api_key: str | None,
) -> Response:
    logger.info("Proxying GET %s", upstream_path)
    proxy_request = ProxyRequest(
        path=upstream_path,
        params=list(request.query_params.multi_items()),
        accept=request.headers.get("accept"),
        api_key=x_api_key,
    )
    require_api_key(proxy_request.api_key)

    url = f"{BASE_URL}{upstream_path}"
    params = proxy_request.params
    headers = build_upstream_headers(proxy_request.accept)

    if params:
        logger.debug("Query params: %s", params)

    ttl = cache_ttl_for_path(upstream_path) if CACHE_ENABLED else None

    async def fetch() -> FetchResult:
        return await _fetch_upstream(request, url, params, headers, upstream_path)

    try:
        if ttl is None:
            return _build_response(await fetch())

        cache = _cache_for_ttl(ttl)
        cache_key = _cache_key(upstream_path, params, proxy_request.accept)
        cached = cache.get(cache_key)
        if cached is not None:
            logger.debug("Cache hit for %s", upstream_path)
            return _build_response(cached)

        result = await _coalesce(cache_key, fetch)
        # Only cache successful, transformed-JSON responses.
        if result.status_code == 200 and result.is_json:
            cache[cache_key] = result
        return _build_response(result)
    except httpx.HTTPError as exc:
        logger.error("Upstream request failed: %s", exc)
        raise HTTPException(status_code=502, detail="Upstream request failed") from exc
