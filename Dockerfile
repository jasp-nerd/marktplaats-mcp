FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS build

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable

# Runtime image without uv: same Python build as the uv image, so the venv works as is.
FROM python:3.12-slim-bookworm

COPY --from=build /app/.venv /app/.venv
RUN useradd --no-create-home --uid 1000 mcp

# The hosted endpoint is read-only by design: account tools never register over HTTP.
# MALLOC_ARENA_MAX keeps glibc from growing a heap arena per thread.
ENV PATH=/app/.venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    MALLOC_ARENA_MAX=2 \
    MCP_TRANSPORT=http \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8000 \
    MCP_RPS=5 \
    MCP_MAX_CONNECTIONS=32 \
    MCP_ALLOWED_HOSTS=marktplaats-mcp.jaspnerd.dev \
    MCP_ALLOWED_ORIGINS=https://claude.ai,https://*.claude.ai,https://marktplaats-mcp.jaspnerd.dev

USER mcp
EXPOSE 8000
HEALTHCHECK --interval=60s --timeout=5s --start-period=20s \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status == 200 else 1)"
CMD ["marktplaats-mcp"]
