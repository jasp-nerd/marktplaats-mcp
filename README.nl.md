<p align="center">
  <img src="assets/banner.svg" alt="marktplaats-mcp — doorzoek Marktplaats & 2dehands vanuit elke AI-agent" width="760">
</p>

[English](README.md) | **Nederlands** | [Français](README.fr.md)

# marktplaats-mcp

**Dé MCP-server voor Marktplaats & 2dehands** — doorzoek Nederlandse en Belgische tweedehands-advertenties rechtstreeks vanuit Claude, Cursor, Codex, opencode of elke andere MCP-compatibele AI-agent. Vind koopjes, check verkopers, blader door categorieën en monitor nieuwe advertenties, allemaal in gewone taal.

[![PyPI version](https://img.shields.io/pypi/v/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml)
[![Downloads](https://static.pepy.tech/badge/marktplaats-mcp/month)](https://pepy.tech/project/marktplaats-mcp)

> *"Zoek een tweedehands racefiets onder de €500 binnen 25 km van Amsterdam, alleen van geverifieerde verkopers."* — dat is nu één prompt.

## ✨ Functies

- 🔍 **Krachtig zoeken** — vrije tekst, categorieën, prijsbereik, conditie, afstand vanaf een postcode, recentheid, sortering
- 🇳🇱🇧🇪 **Twee marktplaatsen, één server** — marktplaats.nl (Nederland) en 2dehands.be (België) via een simpele `site`-parameter
- 📄 **Volledige advertentiedetails** — complete beschrijving, alle foto's, weergaven/favorieten en leeftijd van de advertentie
- 🛡️ **Verkopers checken** — geverifieerde bankrekening / identiteit / telefoon, reviewscore
- 🔔 **Nieuwe advertenties monitoren** — poll voor advertenties geplaatst na een tijdstip met een stateless cursor; perfect voor agent-automatiseringen
- 🧠 **Gebouwd voor LLM's** — token-efficiënte compacte output, betaalde promoties (Dagtoppers) standaard weggefilterd, gestructureerde resultaten
- 🔁 **Robuust** — automatische retries met exponential backoff, jitter en `Retry-After`
- 🔓 **Geen account, geen API-key** — werkt direct

## 🚀 Snelstart

De enige vereiste is [uv](https://docs.astral.sh/uv/) (`brew install uv` of `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code** — één commando:

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Vraag daarna gewoon: *"Zoek op Marktplaats een OLED-tv onder de €400 in de buurt van 3011 AB."*

## 📦 Installeren in jouw favoriete client

Alle configuraties draaien dezelfde stdio-server via `uvx marktplaats-mcp`. Zie de [Engelse README](README.md#-install-in-your-favorite-client) voor kant-en-klare snippets voor **Claude Desktop, OpenAI Codex, opencode, Cursor, VS Code/Copilot, Windsurf, Gemini CLI en JetBrains** — de configuratie is overal hetzelfde:

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
| `get_listing_details` | Volledige advertentie: complete beschrijving, alle foto's, weergaven/favorieten, leeftijd |
| `get_seller_profile` | Vertrouwenssignalen: geverifieerde bank/identiteit/telefoon, reviewscore en -aantal |
| `list_categories` | Blader door de categorieboom (namen + id's) voor filters |
| `check_new_listings` | Nieuwste-eerst-monitoring met een stateless cursor — alleen advertenties geplaatst na `since` |

Alle tools zijn read-only en zo geannoteerd, dus agents vragen niet steeds om bevestiging.

### Voorbeeldprompts

- *"Vind een tweedehands iPhone 15 onder de €600, zo goed als nieuw, gesorteerd op prijs."*
- *"Zoek op 2dehands een bakfiets binnen 20 km van postcode 2000 Antwerpen."*
- *"Is verkoper 12345 betrouwbaar? Check het profiel."*
- *"Check op nieuwe 'vintage lamp'-advertenties sinds mijn laatste check en vat de interessante samen."*

## ❓ FAQ

**Heb ik een Marktplaats-account of API-key nodig?**
Nee. De server gebruikt dezelfde publieke JSON-endpoints als de website zelf.

**Is dit een officieel Marktplaats-product?**
Nee — dit is een onafhankelijk open-sourceproject, niet gelieerd aan Marktplaats/Adevinta. De onderliggende API is ongedocumenteerd en kan veranderen.

**Waarom zie ik soms minder resultaten dan de limiet?**
Betaalde promoties (DAGTOPPER/TOPADVERTENTIE) worden standaard weggefilterd. Gebruik `include_sponsored=true` als je ze wél wilt zien.

## 🤝 Bijdragen

PRs welkom! Zie [CONTRIBUTING.md](.github/CONTRIBUTING.md). Gebouwd op de schouders van [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) en [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp).

## 📄 Licentie

[MIT](LICENSE) © 2026 jasp-nerd
