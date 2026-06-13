FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Faster, reproducible installs.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy dependency files first so this layer is cached until they change.
COPY pyproject.toml uv.lock README.md ./

# Install only third-party deps (not the project itself — its source isn't
# copied yet), keeping this layer cache-friendly.
RUN uv sync --frozen --no-dev --no-install-project

# Copy application code (changes frequently — last layer).
COPY src/ src/

# Use the synced virtualenv directly; uvicorn adds the CWD (/app) to sys.path,
# so the `src...` imports resolve.
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
