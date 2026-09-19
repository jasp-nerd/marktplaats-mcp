# Configuration

[← README](../README.md)

All settings are environment variables. The local server needs none of them; `marktplaats-mcp login` handles the account session.

| Variable | Purpose |
|---|---|
| `MARKTPLAATS_COOKIE`, `TWEEDEHANDS_COOKIE` | Session `Cookie` header per site (alternative to `marktplaats-mcp login`); `*_FILE` variants read it from a file |
| `MARKTPLAATS_SESSION_FILE` | Where `login` stores sessions (default `~/.config/marktplaats-mcp/session.json`) |
| `MARKTPLAATS_READ_ONLY` | `1` disables all write tools |
| `MARKTPLAATS_AUDIT_LOG` | Path of the write audit log, or `off` |
| `MARKTPLAATS_MIN_INTERVAL_MS` | Minimum spacing between upstream requests (default 200) |
| `MCP_TRANSPORT`, `MCP_HOST`, `MCP_PORT` | `http` serves Streamable HTTP for hosting (default stdio) |
| `MCP_RPS`, `MCP_GLOBAL_RPS`, `MCP_ALLOWED_HOSTS`, `MCP_ALLOWED_ORIGINS` | Hosted-mode rate limits and Host/Origin validation |
