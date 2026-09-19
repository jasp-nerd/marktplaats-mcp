# Configuration

[← README](../README.fr.md)

Tous les réglages sont des variables d'environnement. Le serveur local n'en a besoin d'aucune ; `marktplaats-mcp login` gère la session du compte.

| Variable | Rôle |
|---|---|
| `MARKTPLAATS_COOKIE`, `TWEEDEHANDS_COOKIE` | En-tête `Cookie` de session par site (alternative à `marktplaats-mcp login`) ; les variantes `*_FILE` le lisent depuis un fichier |
| `MARKTPLAATS_SESSION_FILE` | Emplacement où `login` stocke les sessions (par défaut `~/.config/marktplaats-mcp/session.json`) |
| `MARKTPLAATS_READ_ONLY` | `1` désactive tous les outils d'écriture |
| `MARKTPLAATS_AUDIT_LOG` | Chemin du journal d'audit des écritures, ou `off` |
| `MARKTPLAATS_MIN_INTERVAL_MS` | Espacement minimal entre les requêtes sortantes (200 par défaut) |
| `MCP_TRANSPORT`, `MCP_HOST`, `MCP_PORT` | `http` sert le transport Streamable HTTP pour l'hébergement (stdio par défaut) |
| `MCP_RPS`, `MCP_GLOBAL_RPS`, `MCP_ALLOWED_HOSTS`, `MCP_ALLOWED_ORIGINS` | Limites de débit et validation Host/Origin en mode hébergé |
