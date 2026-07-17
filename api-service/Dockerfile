# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# Builder stage: install dependencies into an isolated virtualenv
# ---------------------------------------------------------------------------
FROM python:3.13-slim AS builder

WORKDIR /tmp

# Install dependencies first (cached unless requirements.txt changes)
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------------
# Final stage: minimal runtime image
# ---------------------------------------------------------------------------
FROM python:3.13-slim

ARG APP_VERSION=1.2026.12

LABEL maintainer="MLB API Team" \
      version="${APP_VERSION}" \
      description="MLB Stats API Proxy Service"

WORKDIR /app

# Create a non-root user to run the app
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1000 -m -s /usr/sbin/nologin appuser

# Copy the virtualenv and app code already owned by appuser (no extra chown layer).
COPY --chown=appuser:appuser --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appuser api-service/ .

# Runtime environment
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LOG_LEVEL=INFO \
    WORKERS=2 \
    MLB_BASE_URL=https://statsapi.mlb.com \
    APP_VERSION=${APP_VERSION} \
    UPSTREAM_TIMEOUT_SECONDS=30.0

USER appuser

EXPOSE 8000

# Liveness probe: checks THIS process only (/live), not the MLB upstream, so an
# upstream outage can't mark the container unhealthy. Use /health for readiness.
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/live', timeout=5)" || exit 1

# `exec` so uvicorn becomes PID 1 and receives SIGTERM for graceful shutdown
# (the app's lifespan closes the shared HTTP client on shutdown).
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers ${WORKERS}"]
