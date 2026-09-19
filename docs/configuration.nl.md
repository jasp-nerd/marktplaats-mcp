# Configuratie

[← README](../README.nl.md)

Alle instellingen zijn omgevingsvariabelen. De lokale server heeft er geen nodig; `marktplaats-mcp login` regelt de accountsessie.

| Variabele | Waarvoor |
|---|---|
| `MARKTPLAATS_COOKIE`, `TWEEDEHANDS_COOKIE` | `Cookie`-header van de sessie per site (alternatief voor `marktplaats-mcp login`); de `*_FILE`-varianten lezen hem uit een bestand |
| `MARKTPLAATS_SESSION_FILE` | Waar `login` sessies opslaat (standaard `~/.config/marktplaats-mcp/session.json`) |
| `MARKTPLAATS_READ_ONLY` | `1` schakelt alle schrijftools uit |
| `MARKTPLAATS_AUDIT_LOG` | Pad van het auditlogboek voor schrijfacties, of `off` |
| `MARKTPLAATS_MIN_INTERVAL_MS` | Minimale tussentijd tussen verzoeken naar de marktplaats (standaard 200) |
| `MCP_TRANSPORT`, `MCP_HOST`, `MCP_PORT` | `http` serveert Streamable HTTP voor hosting (standaard stdio) |
| `MCP_RPS`, `MCP_GLOBAL_RPS`, `MCP_ALLOWED_HOSTS`, `MCP_ALLOWED_ORIGINS` | Rate-limits en Host/Origin-validatie in gehoste modus |
