<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp: doorzoek Marktplaats en 2dehands vanuit elke AI-agent" width="760">
</p>

<p align="center">
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.md">English</a> | <b>Nederlands</b> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.fr.md">Français</a>
</p>

# marktplaats-mcp

**marktplaats-mcp** is een MCP-server waarmee Claude, Cursor, Codex, opencode en elke andere MCP-client Marktplaats en 2dehands kunnen doorzoeken. Vind koopjes, check verkopers, blader door categorieën en monitor nieuwe advertenties in gewone taal.

<p align="center">
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/v/marktplaats-mcp.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg" alt="Python versions"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/dm/marktplaats-mcp.svg" alt="Downloads"></a>
</p>

## ✨ Functies

- 🔍 **Krachtig zoeken**: vrije tekst, categorieën, prijsbereik, conditie, afstand vanaf een postcode, recentheid, sortering
- 🇳🇱🇧🇪 **Twee marktplaatsen, één server**: marktplaats.nl (Nederland) en 2dehands.be (België) via een `site`-parameter
- 📄 **Volledige advertentiedetails**: complete beschrijving, alle foto's, weergaven en favorieten, leeftijd van de advertentie
- 🛡️ **Verkopers checken**: geverifieerde bankrekening, identiteit en telefoon, reviewscore
- 🔔 **Nieuwe advertenties monitoren**: poll voor advertenties geplaatst na een tijdstip met een stateless cursor
- 🧠 **Gebouwd voor LLM's**: compacte token-efficiënte output, betaalde promoties (Dagtoppers) weggefilterd, gestructureerde resultaten
- 🔁 **Robuust**: retries met exponential backoff, jitter en `Retry-After`
- 🔓 **Geen account, geen API-key**

## 🚀 Snelstart

De enige vereiste is [uv](https://docs.astral.sh/uv/) (`brew install uv` of `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code**, één commando:

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Vraag daarna: *"Zoek op Marktplaats een OLED-tv onder de €400 in de buurt van 3011 AB."*

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/trailer-playful.gif" alt="marktplaats-mcp trailer: koopjes zonder scrollen — vraag het gewoon aan je AI" width="800">
</p>

## 🌐 Gebruik op claude.ai (zonder installatie)

De terminal kun je helemaal overslaan. Een gehoste versie van deze server draait op `https://marktplaats-mcp.jaspnerd.dev/mcp`, klaar om te koppelen aan [claude.ai](https://claude.ai) in je browser of de Claude-app op je telefoon. Custom connectors werken op elk Claude-abonnement, ook Free.

1. Open [claude.ai](https://claude.ai) en ga naar **Settings → Connectors**.
2. Klik op **Add custom connector**.
3. Plak `https://marktplaats-mcp.jaspnerd.dev/mcp` als URL en klik op **Add**. Geen account of key nodig.
4. Vraag Claude: *"Zoek op Marktplaats een OLED-tv onder de €400 in de buurt van 3011 AB."*

Het gehoste endpoint draait dezelfde code als het PyPI-pakket, met een rate-limit per client. Wil je liever dat verzoeken vanaf je eigen machine komen? Installeer dan lokaal, zie hieronder.

## 📦 Installeren in jouw favoriete client

Elke configuratie draait dezelfde stdio-server via `uvx marktplaats-mcp`. In de [Engelse README](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.md#-install-in-your-favorite-client) staan kant-en-klare snippets voor **Claude Desktop, OpenAI Codex, opencode, Cursor, VS Code/Copilot, Windsurf, Gemini CLI en JetBrains**. De configuratie is overal hetzelfde:

```json
{
  "mcpServers": {
    "marktplaats": {
      "command": "uvx",
      "args": ["marktplaats-mcp"]
    }
  }
}
```

## 🧰 Tools

| Tool | Wat het doet |
|---|---|
| `search_listings` | Zoeken met query, categorie, prijsbereik, conditie, afstand, recentheid, sortering en paginering |
| `get_listing_details` | Volledige advertentie: complete beschrijving, alle foto's, weergaven en favorieten, leeftijd |
| `get_seller_profile` | Vertrouwenssignalen: geverifieerde bank, identiteit en telefoon, reviewscore en -aantal |
| `list_categories` | Blader door de categorieboom (namen + id's) voor filters |
| `check_new_listings` | Nieuwste-eerst-monitoring met een stateless cursor: alleen advertenties geplaatst na `since` |

Alle vijf tools zijn read-only en dragen de bijbehorende MCP-annotaties, dus clients slaan de bevestigingsprompts over.

### Voorbeeldprompts

- *"Vind een tweedehands iPhone 15 onder de €600, zo goed als nieuw, gesorteerd op prijs."*
- *"Zoek op 2dehands een bakfiets binnen 20 km van postcode 2000 Antwerpen."*
- *"Is verkoper 12345 betrouwbaar? Check het profiel."*
- *"Check op nieuwe 'vintage lamp'-advertenties sinds mijn laatste check en vat de interessante samen."*

## ❓ FAQ

**Heb ik een Marktplaats-account of API-key nodig?**
Nee. De server gebruikt dezelfde publieke JSON-endpoints als de website zelf.

**Is dit een officieel Marktplaats-product?**
Nee. Dit is een onafhankelijk open-sourceproject zonder banden met Marktplaats of Adevinta. De onderliggende API is ongedocumenteerd en kan veranderen.

**Waarom zie ik soms minder resultaten dan de limiet?**
Betaalde promoties (DAGTOPPER/TOPADVERTENTIE) worden standaard weggefilterd. Gebruik `include_sponsored=true` als je ze wél wilt zien.

## 🤝 Bijdragen

PRs welkom. Zie [CONTRIBUTING.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/.github/CONTRIBUTING.md). Dit project hergebruikt bewezen ideeën uit [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) en [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp).

## 📄 Licentie

[MIT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE) © 2026 jasp-nerd
