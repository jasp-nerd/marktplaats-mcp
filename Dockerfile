FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable \
    && useradd --create-home --uid 1000 mcp \
    && chown -R mcp:mcp /app

# The hosted endpoint is read-only by design: account tools never register over HTTP.
ENV MCP_TRANSPORT=http \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8000 \
    MCP_RPS=5 \
    MCP_ALLOWED_HOSTS=marktplaats-mcp.jaspnerd.dev \
    MCP_ALLOWED_ORIGINS=https://claude.ai,https://*.claude.ai,https://marktplaats-mcp.jaspnerd.dev

USER mcp
EXPOSE 8000
HEALTHCHECK --interval=60s --timeout=5s --start-period=20s \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status == 200 else 1)"
CMD ["uv", "run", "--no-sync", "marktplaats-mcp"]
