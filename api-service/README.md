# MLB API Proxy

A FastAPI proxy in front of the MLB Stats API (`https://statsapi.mlb.com`). It mirrors
**~150 GET endpoints** across 25 routers and adds resilience, normalization, and Spanish
stat translations on top of the upstream.

## What it adds over the raw upstream

- **Auth** — requires an `X-API-Key` header matching `PROXY_API_KEY` (constant-time compare).
- **Resilience** — a shared pooled `httpx` client, granular connect/read timeouts, and
  automatic retries with exponential backoff for transient upstream failures (502/503/504,
  timeouts, connection errors). `429` is passed through unchanged.
- **Response cache** — in-process TTL cache with per-endpoint TTLs (reference data 6h,
  semi-dynamic 5min, live game data not cached) and single-flight request coalescing to
  prevent cache stampedes. Cached responses are stored pre-serialized (bytes).
- **XML → JSON** — auto-detects XML (by Content-Type or a leading `<`) and converts it.
- **Stat translations** — renames MLB stat fields to standard abbreviations
  (`homeRuns` → `HR`) and offers Spanish descriptions. See `stats_translations.py`.
- **Null normalization** — converts MLB's missing-data sentinels (`-1`, `.---`, …) to `null`.
- **Observability** — per-request `x-request-id`, centralized error handlers.
- Non-JSON/XML upstream bodies (CSV, binary) are forwarded **verbatim**, unaltered.

## Endpoints

- `GET /api/v1/...` — the proxied MLB endpoints (teams, people, games, schedule, stats,
  standings, draft, awards, venues, …). Full catalog: `docs/API_RESPONSE_CATALOG.md`.
- `GET /metric_abbreviation?metric=battingAverage` → `{"abbreviation": "AVG"}`
- `GET /abbrev_description_spanish?abbreviation=AVG` → `{"description": "Promedio"}`
- `GET /health` — **readiness**: verifies the upstream is reachable (503 if not).
- `GET /live` — **liveness**: this process is up (never touches the upstream). Used by the
  container healthcheck.
- Interactive docs at `/docs` and `/redoc` (toggle with `ENABLE_DOCS`).

## Configuration (env / `.env`)

| Variable | Default | Purpose |
|---|---|---|
| `PROXY_API_KEY` | *(required)* | API key callers must send as `X-API-Key`. |
| `MLB_BASE_URL` | `https://statsapi.mlb.com` | Upstream base URL. |
| `LOG_LEVEL` | `INFO` | Logging level. |
| `CORS_ALLOW_ORIGINS` | `""` | Comma-separated allowed origins (empty = none). |
| `ENABLE_DOCS` | `true` | Expose `/docs`, `/redoc`, `/openapi.json`. |
| `ENABLE_CACHE` | `true` | Toggle the response cache. |
| `CACHE_MAXSIZE` / `CACHE_TTL_DEFAULT` / `CACHE_TTL_STATIC` | `1000` / `300` / `21600` | Cache sizing & TTLs (seconds). |
| `UPSTREAM_TIMEOUT_SECONDS` / `UPSTREAM_CONNECT_TIMEOUT_SECONDS` | `30` / `5` | Upstream timeouts. |
| `UPSTREAM_MAX_RETRIES` / `UPSTREAM_BACKOFF_BASE_SECONDS` | `2` / `0.5` | Retry policy. |
| `UPSTREAM_MAX_CONNECTIONS` / `UPSTREAM_MAX_KEEPALIVE_CONNECTIONS` | `100` / `20` | Pool limits. |

> The response cache is **per-worker**. Keep `WORKERS` low (1–2) for a good hit rate.

## Run locally

```bash
pip install -r requirements.txt
PROXY_API_KEY=dev-key uvicorn main:app --reload --port 8000
```

## Docker

See the repository root: `Dockerfile`, `docker-compose.yml`, `docker-compose.env.example`,
and `PORTAINER_DEPLOYMENT.md`.
