import logging
import uuid
from time import monotonic
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from proxy import CORS_ALLOW_ORIGINS, create_http_client, logger, settings
from routers import (
    attendance,
    awards,
    broadcast,
    conference,
    division,
    draft,
    game_pace,
    games,
    high_low,
    job,
    league,
    milestones,
    misc,
    people,
    schedule,
    season,
    sports,
    standings,
    stats,
    teams,
    transactions,
    uniforms,
    venues,
)
from stats_translations import abbrev_description_spanish, metric_abbreviation


# Filter to suppress health/liveness probes from access logs
class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return "/health" not in message and "/live" not in message


# Apply filter to uvicorn access logger
logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create a single pooled httpx client for the app's lifetime (R1)."""
    app.state.http = create_http_client()
    logger.info("Started shared upstream HTTP client (pooled connections)")
    try:
        yield
    finally:
        await app.state.http.aclose()
        # Clear the reference so any post-shutdown code path falls back to a
        # fresh client instead of reusing a closed one.
        app.state.http = None
        logger.info("Closed shared upstream HTTP client")


app = FastAPI(
    title="MLB API Proxy",
    version=settings.app_version,
    lifespan=lifespan,
    # Interactive docs are toggleable; disable (ENABLE_DOCS=false) for public prod.
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    openapi_url="/openapi.json" if settings.enable_docs else None,
)

# CORS for the browser front-end. Origins are configured via CORS_ALLOW_ORIGINS
# (comma-separated); empty means no cross-origin access. Never "*" in production.
if CORS_ALLOW_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOW_ORIGINS,
        allow_methods=["GET"],
        allow_headers=["X-API-Key", "Accept", "Content-Type"],
    )
    logger.info("CORS enabled for origins: %s", CORS_ALLOW_ORIGINS)

app.include_router(teams.router)
app.include_router(people.router)
app.include_router(games.router)
app.include_router(schedule.router)
app.include_router(stats.router)
app.include_router(standings.router)
app.include_router(draft.router)
app.include_router(awards.router)
app.include_router(venues.router)
app.include_router(transactions.router)
app.include_router(sports.router)
app.include_router(league.router)
app.include_router(division.router)
app.include_router(conference.router)
app.include_router(season.router)
app.include_router(attendance.router)
app.include_router(broadcast.router)
app.include_router(uniforms.router)
app.include_router(milestones.router)
app.include_router(high_low.router)
app.include_router(game_pace.router)
app.include_router(job.router)
app.include_router(misc.router)


@app.get("/metric_abbreviation")
async def get_metric_abbreviation(metric: str) -> dict:
    """
    Get the standard baseball abbreviation for a metric name.

    Args:
        metric (str): The metric name to look up (camelCase format)

    Returns:
        dict: Contains the requested metric and its abbreviation

    Example:
        GET /metric_abbreviation?metric=battingAverage
        Returns: {"metric": "battingAverage", "abbreviation": "AVG"}
    """
    abbreviation = metric_abbreviation(metric)
    return {
        "metric": metric,
        "abbreviation": abbreviation,
    }


@app.get("/abbrev_description_spanish")
async def get_abbrev_description_spanish(abbreviation: str) -> dict:
    """
    Get the Spanish description for a baseball stat abbreviation.
    Search is case-insensitive.

    Args:
        abbreviation (str): The abbreviation to look up

    Returns:
        dict: Contains the requested abbreviation and its Spanish description

    Example:
        GET /abbrev_description_spanish?abbreviation=AVG
        Returns: {"abbreviation": "AVG", "description": "Promedio"}
    """
    description = abbrev_description_spanish(abbreviation)
    return {
        "abbreviation": abbreviation,
        "description": description,
    }


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


@app.exception_handler(HTTPException)
async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        "HTTP error %s on %s (request_id=%s): %s",
        exc.status_code,
        request.url.path,
        request_id,
        exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "request_id": request_id,
        },
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        "Validation error on %s (request_id=%s): %s",
        request.url.path,
        request_id,
        exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "Validation error",
            "details": exc.errors(),
            "request_id": request_id,
        },
    )


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception("Unhandled error on %s (request_id=%s)", request.url.path, request_id)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal server error",
            "request_id": request_id,
        },
    )


# Last upstream probe: (monotonic timestamp, healthy, error). Module-level and per-process, which
# means per-worker -- the same trade-off the response cache already makes (see ENABLE_CACHE). With
# two workers the upstream sees at most two probes per TTL instead of one, which is still two orders
# of magnitude better than one per request.
#
# No lock. Two concurrent calls on a cold cache may both probe; the cost is one extra upstream GET
# and the outcome is identical either way. A lock here would add a failure mode to save nothing.
_UPSTREAM_PROBE: tuple[float, bool, str | None] | None = None


async def _probe_upstream(request: Request) -> tuple[bool, str | None]:
    """Is the MLB API reachable? Reuses the last answer for `HEALTH_UPSTREAM_TTL` seconds.

    WHY THIS IS CACHED AT ALL. Every call used to reach the MLB API. The container healthcheck runs
    every 30 seconds on its own -- 2,880 upstream requests a day -- and any external uptime monitor
    adds its own on top, all of it to answer a question whose answer does not change from one second
    to the next. Under a rate limit, health checking would be competing with real traffic.

    The failure case is cached too, deliberately: during an outage every probe costs a 5-second
    timeout, so that is exactly when the reuse matters most. A recovery is still reported within one
    TTL, which is half a minute.
    """
    global _UPSTREAM_PROBE

    ttl = settings.health_upstream_ttl
    if ttl > 0 and _UPSTREAM_PROBE is not None:
        probed_at, healthy, error = _UPSTREAM_PROBE
        if monotonic() - probed_at < ttl:
            return healthy, error

    upstream_healthy = False
    upstream_error = None

    shared_client = getattr(request.app.state, "http", None)
    client = shared_client or create_http_client()
    try:
        response = await client.get(
            f"{settings.mlb_base_url}/api/v1/sports",
            timeout=5.0,
        )
        upstream_healthy = response.status_code == 200
        if not upstream_healthy:
            upstream_error = f"Upstream returned {response.status_code}"
    except Exception as exc:
        upstream_error = str(exc)
        logger.warning("Upstream health check failed: %s", upstream_error)
    finally:
        if shared_client is None:
            await client.aclose()

    _UPSTREAM_PROBE = (monotonic(), upstream_healthy, upstream_error)
    return upstream_healthy, upstream_error


@app.get("/health")
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for monitoring and load balancers.

    Verifies both the proxy service and upstream MLB API are accessible.
    Returns 200 only if both are healthy. The upstream answer is reused for a few seconds -- see
    `_probe_upstream` -- so that monitoring this endpoint does not turn into upstream traffic.

    NOT for the container healthcheck: use `/live` for that, or an MLB outage marks a perfectly
    healthy proxy as unhealthy.
    """
    upstream_healthy, upstream_error = await _probe_upstream(request)

    health_status = {
        "status": "healthy" if upstream_healthy else "degraded",
        "version": settings.app_version,
        "proxy": "ok",
        "upstream": "ok" if upstream_healthy else "unreachable",
    }

    if upstream_error:
        health_status["upstream_error"] = upstream_error

    status_code = 200 if upstream_healthy else 503
    return JSONResponse(status_code=status_code, content=health_status)


@app.get("/live")
async def liveness() -> JSONResponse:
    """Local liveness probe: is THIS process up and serving?

    Does NOT touch the upstream, so a MLB outage/rate-limit/DNS blip can't mark the
    container unhealthy while the proxy is fine (and still serving from cache). Used
    by the Docker/Compose healthcheck. Use /health for upstream readiness.
    """
    return JSONResponse(
        status_code=200,
        content={"status": "alive", "version": settings.app_version},
    )
