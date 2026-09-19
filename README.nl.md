<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp: doorzoek Marktplaats en 2dehands vanuit elke AI-agent" width="760">
</p>

<p align="center">
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.md">English</a> | <b>Nederlands</b> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.fr.md">Français</a>
</p>

# marktplaats-mcp: de MCP-server voor Marktplaats & 2dehands

**marktplaats-mcp** is een MCP-server voor **Marktplaats.nl** (Nederland) en **2dehands.be** (België), de Nederlandse en Belgische tweedehands-advertentiesites (*tweedehands*, *petites annonces d'occasion*). Claude, ChatGPT, Cursor, Codex, Gemini, VS Code Copilot, Cline, opencode en elke andere MCP-client kunnen er advertenties mee doorzoeken, filteren op categoriespecifieke kenmerken, verkopers checken, prijzen vergelijken, nieuwe advertenties monitoren en, met je eigen login, berichten lezen en versturen, bieden en favorieten en je eigen advertenties beheren. Geen API-key. Draait lokaal via stdio, of als gehost endpoint dat je in één stap in claude.ai plakt.

<p align="center">
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/v/marktplaats-mcp.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg" alt="Python versions"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml/badge.svg" alt="Live API canary"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/dm/marktplaats-mcp.svg" alt="Downloads"></a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=marktplaats"><img src="https://img.shields.io/badge/MCP%20registry-listed-blue" alt="MCP registry"></a>
</p>

## 🌐 Gebruik op claude.ai (zonder installatie)

Een gehoste versie van deze server draait op `https://marktplaats-mcp.jaspnerd.dev/mcp`, klaar voor [claude.ai](https://claude.ai) in je browser of de Claude-app op je telefoon. Custom connectors werken op elk Claude-abonnement, ook Free.

1. Open [claude.ai](https://claude.ai) → **Settings → Connectors → Add custom connector**.
2. Plak `https://marktplaats-mcp.jaspnerd.dev/mcp` als URL en klik op **Add**. Geen account of key nodig.
3. Vraag Claude: *"Zoek op Marktplaats een OLED-tv onder de €400 in de buurt van 3011 AB en check de verkoper."*

Het gehoste endpoint draait dezelfde code als het PyPI-pakket, heeft een rate-limit per client en biedt alleen de read-only tools. Wil je je eigen account gebruiken, installeer het dan lokaal, zie hieronder.

## 🚀 Snelstart (lokaal)

De enige vereiste is [uv](https://docs.astral.sh/uv/) (`brew install uv` of `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code**, één commando:

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Vraag daarna: *"Zoek een racefiets onder de €500 binnen 25 km van 1011 AB, framemaat 57-61 cm, en zeg of de verkopers betrouwbaar lijken."*

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/trailer-crt.gif" alt="marktplaats-mcp trailer: een AI-agent zoekt een racefiets en checkt de verkoper, weergegeven als een retro CRT-terminalsessie" width="800">
</p>

## 👤 Je eigen account gebruiken (berichten, favorieten, biedingen, je advertenties)

Marktplaats heeft geen publieke API en het inloggen verloopt via sms-tweefactor en reCAPTCHA, dus deze server vraagt nooit om je wachtwoord. In plaats daarvan leent hij de sessie uit een browser waar je al bent ingelogd, zoals `yt-dlp --cookies-from-browser` dat doet:

```bash
uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login
```

Dat zoekt naar een Marktplaats- of 2dehands-sessie in Chrome, Firefox, Safari, Edge, Brave, Arc en soortgelijke browsers (macOS vraagt één keer toegang tot de sleutelhanger; klik op Allow), controleert die bij de site en slaat hem op in `~/.config/marktplaats-mcp/session.json`, alleen leesbaar voor jouw gebruiker. Herstart je MCP-client en de accounttools verschijnen. Handige commando's:

```bash
marktplaats-mcp login --read-only     # never send, bid or change favorites
marktplaats-mcp login --paste         # paste a Cookie header from DevTools instead
marktplaats-mcp status                # is the stored session still valid?
marktplaats-mcp logout                # delete it
```

Of zet `MARKTPLAATS_COOKIE` / `TWEEDEHANDS_COOKIE` (de `Cookie`-header van het verzoek) in de configuratie van je client. Sessies gaan weken mee; loopt er een af, dan geven de tools aan dat je opnieuw moet inloggen.

**Wat er mis kan gaan, en wat niet.** Een bericht sturen, een verkoper benaderen en een bod plaatsen geven eerst een voorbeeld en voeren pas iets uit als ze opnieuw worden aangeroepen met `confirm=true`, zodat je agent je laat zien wat hij van plan is. Een bod is bindend op Marktplaats; de tool weigert biedingen onder het minimum van de advertentie en is gemarkeerd als destructief, zodat clients het vooraf vragen. Elke bevestigde schrijfactie wordt toegevoegd aan `~/.local/state/marktplaats-mcp/writes.jsonl`. Je sessie gaat alleen naar marktplaats.nl of 2dehands.be, en het gehoste endpoint registreert nooit accounttools. Het automatisch plaatsen van advertenties is verboden volgens de voorwaarden van Marktplaats en is bewust niet ingebouwd.

## 📦 Installeren in jouw favoriete client

Elke configuratie draait dezelfde stdio-server via `uvx marktplaats-mcp`.

<details>
<summary><b>Claude Desktop</b></summary>

Toevoegen aan `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`) en daarna Claude Desktop volledig herstarten:

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

Kan Claude Desktop `uvx` niet vinden, gebruik dan het absolute pad (`which uvx`, bijvoorbeeld `/Users/you/.local/bin/uvx`).
</details>

<details>
<summary><b>OpenAI Codex CLI</b></summary>

Toevoegen aan `~/.codex/config.toml`:

```toml
[mcp_servers.marktplaats]
command = "uvx"
args = ["marktplaats-mcp"]
```

Of: `codex mcp add marktplaats -- uvx marktplaats-mcp`
</details>

<details>
<summary><b>opencode</b></summary>

Toevoegen aan `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "marktplaats": {
      "type": "local",
      "command": ["uvx", "marktplaats-mcp"],
      "enabled": true
    }
  }
}
```
</details>

<details>
<summary><b>Cursor</b></summary>

Toevoegen aan `~/.cursor/mcp.json` (globaal) of `.cursor/mcp.json` (per project):

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
</details>

<details>
<summary><b>VS Code / GitHub Copilot</b></summary>

Toevoegen aan `.vscode/mcp.json` (let op de `servers`-sleutel en het expliciete `type`):

```json
{
  "servers": {
    "marktplaats": {
      "type": "stdio",
      "command": "uvx",
      "args": ["marktplaats-mcp"]
    }
  }
}
```
</details>

<details>
<summary><b>Cline</b></summary>

MCP Servers → Configure → toevoegen aan `cline_mcp_settings.json`:

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
</details>

<details>
<summary><b>Windsurf</b></summary>

Toevoegen aan `~/.codeium/windsurf/mcp_config.json`:

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
</details>

<details>
<summary><b>Gemini CLI</b></summary>

Toevoegen aan `~/.gemini/settings.json`:

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
</details>

<details>
<summary><b>JetBrains-IDE's (AI Assistant / Junie)</b></summary>

Settings → Tools → AI Assistant → Model Context Protocol (MCP) → Add:

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
</details>

<details>
<summary><b>Elke client die remote servers ondersteunt (ChatGPT, Gemini, andere)</b></summary>

Gebruik de Streamable HTTP-URL `https://marktplaats-mcp.jaspnerd.dev/mcp`, zonder authenticatie. Alleen read-only tools.
</details>

## 🧰 Tools

| Tool | Wat het doet | Account | Schrijft |
|---|---|:---:|:---:|
| `search_listings` | Zoeken met query, categorie, subcategorie, **categoriespecifieke kenmerken**, prijsbereik, conditie, levering (ophalen/verzenden), afstand vanaf een postcode, recentheid, negatieve zoekwoorden, sortering en paginering | | |
| `get_listing_details` | Volledige advertentie: beschrijving, kenmerken, status (actief/gesloten), exacte plaatsingstijd, aantal weergaven en favorieten, biedstatus en minimumbod, verzending, foto's, reactiesnelheid en accountleeftijd van de verkoper. Accepteert geplakte URL's | | |
| `get_seller_profile` | Vertrouwenssignalen: geverifieerde bankrekening, identiteit, telefoon, zakelijke verificatie, betaalmethode, reviewscore en -aantal, laagste bod dat de verkoper accepteert | | |
| `list_seller_listings` | Alles wat één verkoper aanbiedt: handelaren die zich voordoen als particulier en dubbele advertenties eruit pikken | | |
| `list_categories` | De categorieboom (namen en id's) die voor filteren wordt gebruikt, ook beschikbaar als MCP-resource | | |
| `list_category_filters` | Ontdek de filters van een categorie (merk, framehoogte, kilometerstand, brandstof, RAM, ...) met hun geldige waarden en aantallen | | |
| `check_new_listings` | Nieuwste-eerst-monitoring met een stateless cursor: geeft alleen advertenties die na `since` zijn geplaatst, en slaat er nooit een over | | |
| `analyze_prices` | Mediaan, kwartielen, min, max en gemiddelde vraagprijs voor een zoekopdracht, plus de goedkoopste treffers | | |
| `get_my_account` | Sessiecheck, ongelezen berichten en meldingen | ✅ | |
| `list_conversations`, `get_conversation` | Je inbox en volledige berichtenreeksen | ✅ | |
| `list_my_listings`, `list_favorites`, `list_my_bids`, `list_saved_searches` | Je eigen advertenties (weergaven, favorieten, hoogste bod, vervaldatum), favorieten, biedingen en opgeslagen zoekopdrachten | ✅ | |
| `send_message`, `contact_seller` | Reageren in een gesprek, of een verkoper een vraag stellen of een vrijblijvend bod doen. Eerst een voorbeeld, `confirm=true` om te versturen | ✅ | ✅ |
| `place_bid` | Bieden op een advertentie. Eerst een voorbeeld, weigert biedingen onder het minimum, gemarkeerd als destructief | ✅ | ✅ |
| `set_favorite`, `extend_my_listing` | Een advertentie bij favorieten zetten of eruit halen; een van je aflopende advertenties verlengen | ✅ | ✅ |

De read-only tools dragen de bijbehorende MCP-annotaties, dus clients slaan de bevestigingsprompts daarvoor over en vragen het wel bij de schrijftools. Elke tool geeft gestructureerde output met een echt schema. Twee prompts, `bargain_hunt` en `vet_listing`, leggen de gebruikelijke workflows vast.

### Wat je kunt vragen, en wat er gebeurt

| Jij zegt | De agent roept aan |
|---|---|
| *"Is €450 een eerlijke prijs voor een iPhone 15 128 GB in goede staat?"* | `analyze_prices` → mediaan, kwartielen en de drie goedkoopste advertenties |
| *"Zoek een tweedehands Golf, 2018-2022, minder dan 100.000 km, benzine, van een particulier"* | `list_category_filters("Auto's")` → `search_listings(attributes={"Bouwjaar": "2018-2022", "Kilometerstand": "-100000", "Brandstof": "Benzine", "Adverteerder": "Particulier"})` |
| *"Is deze verkoper te vertrouwen? Wat biedt hij nog meer aan?"* | `get_listing_details` → `get_seller_profile` → `list_seller_listings` |
| *"Laat het me weten als er nieuwe bakfiets-advertenties bij Antwerpen verschijnen"* | `check_new_listings(site="2dehands", postcode="2000", distance_km=25)` met de teruggegeven cursor bij elke volgende check |
| *"Vraag de verkoper of het nog beschikbaar is en bied €120"* | `contact_seller(..., offer_euros=120)` voorbeeld → jij bevestigt → verstuurd |
| *"Antwoord Piet dat ik het zaterdag kan ophalen"* | `list_conversations` → `send_message` voorbeeld → jij bevestigt → verstuurd |

## 🔒 Veiligheidsmodel

- **Standaard geen inloggegevens.** Zoeken, details opvragen, verkopers checken, filters, prijsstatistieken en monitoring werken zonder account.
- **Je sessie blijft van jou.** De lokale server leest de cookie uit je browser of uit een bestand dat alleen jij kunt lezen, stuurt hem alleen naar marktplaats.nl / 2dehands.be en logt hem nooit. Het gehoste endpoint weigert te starten als er accountgegevens zijn ingesteld.
- **Schrijfacties zijn expliciet.** Versturen en bieden tonen eerst een voorbeeld en vereisen `confirm=true`; biedingen onder het minimum worden geweigerd; `login --read-only` of `MARKTPLAATS_READ_ONLY=1` schakelt schrijfacties helemaal uit; elke bevestigde schrijfactie wordt lokaal gelogd.
- **Onbetrouwbare inhoud wordt gemarkeerd.** Advertentieteksten en berichten zijn geschreven door andere gebruikers; de server vertelt het model die als data te behandelen, nooit als instructies.
- **Netjes tegenover de marktplaats.** Verzoeken worden gespreid (`MARKTPLAATS_MIN_INTERVAL_MS`, standaard 200), opnieuw geprobeerd met backoff en `Retry-After`, en zoekpagina's worden een minuut gecached. Het gehoste endpoint heeft een rate-limit per client en in totaal.
- **Geen affiliate links, geen tracking.** Advertentie-URL's worden precies teruggegeven zoals de marktplaatsen ze publiceren.

## ⚖️ Hoe dit zich verhoudt tot andere servers

| | **marktplaats-mcp** (deze) | [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp) | [gjoris/marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) |
|---|:---:|:---:|:---:|
| Marktplaats.nl | ✅ | ✅ | ✅ |
| 2dehands.be (België), met taalfilter | ✅ | ❌ | ✅ |
| Subcategoriefilter dat echt wordt toegepast | ✅ | ❌ | ❌ |
| Filters op categoriekenmerken (merk, kilometerstand, RAM, ...) op label | ✅ | alleen id's | alleen id's |
| Prijsstatistieken, advertenties per verkoper, spellingsuggesties | ✅ | ❌ | ❌ |
| Advertentiedetails met status, exacte tijd, biedingen, reactiesnelheid verkoper | ✅ | deels | deels |
| Account: berichten, favorieten, biedingen, eigen advertenties | lezen + schrijven | ❌ | alleen lezen |
| Inloggen zonder wachtwoord (browsersessie importeren) | ✅ | n.v.t. | login via Playwright |
| Monitoring van nieuwe advertenties | ✅ | ❌ | opgeslagen zoekopdrachten op schijf |
| Betaalde promoties standaard weggefilterd | ✅ | ❌ | ❌ |
| Installatie | `uvx marktplaats-mcp` (PyPI) | `uvx git+https://…` (kapot op huidige `mcp`) | vanaf de broncode |
| Gehost endpoint, zonder installatie | ✅ | ❌ | ❌ |
| Officieel MCP-register | ✅ | ❌ | ❌ |
| Dagelijkse canary op de live API | ✅ | ❌ | ✅ |
| Laatste release | actueel | feb 2026 | mei 2026 |

Eer wie eer toekomt: de server van PonClick was er als eerste en de opmaak van advertenties daar heeft deze server beïnvloed, en gjoris was de eerste met het parsen van de ingebedde pagina en de live canary. Zie [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

## ❓ FAQ

### Bestaat er een MCP-server voor Marktplaats?
Ja, deze. Gratis, open source (MIT), geen API-key. Plak de gehoste URL in claude.ai of draai `uvx marktplaats-mcp`.

### Werkt het met 2dehands.be en België?
Ja. Elke tool accepteert `site="2dehands"`, en met `language="nl"` of `"fr"` beperk je Belgische resultaten tot één taal.

### Heb ik een Marktplaats-account of API-key nodig?
Nee. Alleen de accounttools hebben je eigen login nodig, en die gebruiken je bestaande browsersessie in plaats van een wachtwoord.

### Kan AI mijn Marktplaats-berichten lezen en beantwoorden, of biedingen plaatsen?
Ja, met de lokale server na `marktplaats-mcp login`. Versturen en bieden tonen een voorbeeld en gebeuren pas nadat jij bevestigt.

### Waar worden mijn inloggegevens bewaard?
In `~/.config/marktplaats-mcp/session.json` op je eigen machine, alleen leesbaar voor jouw gebruiker, of in de omgevingsvariabelen die je zelf instelt. Ze gaan alleen naar marktplaats.nl / 2dehands.be. Met `marktplaats-mcp logout` verwijder je ze.

### Kan ik het gebruiken zonder iets te installeren?
Ja: het gehoste endpoint `https://marktplaats-mcp.jaspnerd.dev/mcp` werkt in claude.ai, ook op het Free-abonnement en in de mobiele apps. Het biedt de read-only tools.

### Werkt het met ChatGPT, Cursor, Gemini, VS Code en Cline?
Ja. Elke client die stdio-servers draait kan `uvx marktplaats-mcp` gebruiken; clients die remote servers ondersteunen kunnen de gehoste URL gebruiken.

### Is dit officieel of verbonden aan Marktplaats?
Nee. Het is een onafhankelijk open-sourceproject zonder banden met Marktplaats, 2dehands of Adevinta. Het gebruikt dezelfde publieke JSON-endpoints als de websites zelf; die API is ongedocumenteerd en kan veranderen, en daarom draait er elke dag een live canary.

### Waarom zie ik soms minder resultaten dan de limiet, of lijkt `total_count` hoog?
Betaalde promoties (DAGTOPPER, TOPADVERTENTIE) worden standaard weggefilterd; geef `include_sponsored=true` mee om ze te zien. `total_count` is het ruwe aantal van de marktplaats, van vóór dat filteren.

### Welke Python-versies worden ondersteund?
3.10 en hoger. CI test 3.11 tot en met 3.13 op Linux, macOS en Windows.

## ⚙️ Configuratie

| Variabele | Waarvoor |
|---|---|
| `MARKTPLAATS_COOKIE`, `TWEEDEHANDS_COOKIE` | `Cookie`-header van de sessie per site (alternatief voor `marktplaats-mcp login`); de `*_FILE`-varianten lezen hem uit een bestand |
| `MARKTPLAATS_SESSION_FILE` | Waar `login` sessies opslaat (standaard `~/.config/marktplaats-mcp/session.json`) |
| `MARKTPLAATS_READ_ONLY` | `1` schakelt alle schrijftools uit |
| `MARKTPLAATS_AUDIT_LOG` | Pad van het auditlogboek voor schrijfacties, of `off` |
| `MARKTPLAATS_MIN_INTERVAL_MS` | Minimale tussentijd tussen verzoeken naar de marktplaats (standaard 200) |
| `MCP_TRANSPORT`, `MCP_HOST`, `MCP_PORT` | `http` serveert Streamable HTTP voor hosting (standaard stdio) |
| `MCP_RPS`, `MCP_GLOBAL_RPS`, `MCP_ALLOWED_HOSTS`, `MCP_ALLOWED_ORIGINS` | Rate-limits en Host/Origin-validatie in gehoste modus |

## 🗺️ Roadmap

- Ondersteuning voor FastMCP 4 / MCP-protocol 2026-07-28
- Zoeken over beide sites tegelijk (NL en BE in één aanroep)
- Opgeslagen zoekopdrachten aanmaken vanuit de agent
- Extensiebundel voor Claude Desktop (MCPB)

## 🤝 Bijdragen

PRs welkom. Zie [CONTRIBUTING.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/.github/CONTRIBUTING.md) voor de dev-setup: `uv sync --all-groups`, daarna `uv run pytest`. Met `uv run python scripts/e2e_smoke.py` draai je de live canary.

Dit project hergebruikt bewezen ideeën uit [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) en [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp). Details in [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

Heeft dit je een ritje naar Marktplaats bespaard, dan helpt een ster anderen om het te vinden.

## 📄 Licentie

[MIT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE) © 2026 jasp-nerd

---

<sub>mcp-name: io.github.jasp-nerd/marktplaats-mcp</sub>
