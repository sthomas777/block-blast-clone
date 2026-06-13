FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Faster, reproducible installs.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy dependency files first so this layer is cached until they change.
# NOTE: pyproject.toml and uv.lock live at the repo root, so the build context
# must be the repo root (see build command below).
COPY pyproject.toml uv.lock ./

# Install only third-party deps (not the project itself — its source isn't
# copied yet), keeping this layer cache-friendly.
RUN uv sync --frozen --no-dev --no-install-project

# Copy application code (changes frequently — last layer).
COPY backend/ backend/

# Use the synced virtualenv directly; uvicorn adds the CWD (/app) to sys.path,
# so the `backend.src...` imports resolve.
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
