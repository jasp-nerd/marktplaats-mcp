<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp: doorzoek Marktplaats en 2dehands vanuit elke AI-agent" width="760">
</p>

<p align="center">
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.md">English</a> | <b>Nederlands</b> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.fr.md">Français</a>
</p>

# marktplaats-mcp: de MCP-server voor Marktplaats & 2dehands

**marktplaats-mcp** is een MCP-server voor **Marktplaats.nl** (Nederland) en **2dehands.be** (België), de Nederlandse en Belgische tweedehands-advertentiesites (*tweedehands*, *petites annonces d'occasion*). Doorzoek advertenties, filter op categoriekenmerken, check verkopers, vergelijk prijzen en houd nieuwe advertenties in de gaten vanuit Claude, ChatGPT, Cursor, Codex, Gemini of elke andere MCP-client. Met je eigen login leest en verstuurt hij ook berichten, plaatst hij biedingen en beheert hij je favorieten en advertenties. Geen API-key.

<p align="center">
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/v/marktplaats-mcp.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg" alt="Python versions"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml/badge.svg" alt="Live API canary"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/dm/marktplaats-mcp.svg" alt="Downloads"></a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=marktplaats"><img src="https://img.shields.io/badge/MCP%20registry-listed-blue" alt="MCP registry"></a>
</p>

## 🚀 Aan de slag

**Zonder installatie: plak een URL.** De gehoste, alleen-lezen server draait op `https://marktplaats-mcp.jaspnerd.dev/mcp`. Voeg hem toe als custom connector in [claude.ai](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.nl.md#claudeai-web-and-mobile) (Settings → Connectors, werkt op het Free-plan en mobiel), [ChatGPT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.nl.md#chatgpt), [Mistral Le Chat](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.nl.md#mistral-le-chat), [Perplexity](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.nl.md#perplexity) of de [Gemini-app](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.nl.md#gemini-app).

**Claude Code: één commando.**

```bash
claude mcp add --scope user marktplaats -- uvx marktplaats-mcp
```

**Elke andere client.** Installeer [uv](https://docs.astral.sh/uv/getting-started/installation/) (`brew install uv`, of `winget install --id=astral-sh.uv -e` op Windows) en voeg de standaard MCP-config toe:

```json
{ "mcpServers": { "marktplaats": { "command": "uvx", "args": ["marktplaats-mcp"] } } }
```

Eén klik: [![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=) [![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) [![Add to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D) [![Add to Kiro](https://img.shields.io/badge/Kiro-Add-7B61FF?style=flat-square)](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D)

Stap-voor-stap instructies voor 40 clients (Cursor, VS Code, Codex, Gemini CLI, Cline, Windsurf, JetBrains, Zed, opencode, Goose, ...), met het configpad per OS en een link naar de officiële handleiding van elke client: **[docs/clients.nl.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.nl.md)**.

Vraag daarna: *"Zoek een racefiets onder de €500 binnen 25 km van 1011 AB, framemaat 57-61 cm, en zeg of de verkopers betrouwbaar lijken."*

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/trailer-crt.gif" alt="marktplaats-mcp trailer: an AI agent searches for a racefiets and vets the seller, rendered as a retro CRT terminal session" width="800">
</p>

## 👤 Je eigen account gebruiken (berichten, favorieten, biedingen, je advertenties)

Marktplaats heeft geen publieke API en het inloggen verloopt via sms-tweefactor, dus deze server vraagt nooit om je wachtwoord. Hij leent de sessie uit een browser waar je al bent ingelogd:

```bash
uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login
```

De sessie wordt opgeslagen in `~/.config/marktplaats-mcp/session.json`, alleen leesbaar voor jouw gebruiker. Herstart je MCP-client en de accounttools verschijnen.

```bash
marktplaats-mcp login --read-only     # never send, bid or change favorites
marktplaats-mcp login --paste         # paste a Cookie header from DevTools instead
marktplaats-mcp status                # is the stored session still valid?
marktplaats-mcp logout                # delete it
```

<details>
<summary><b>Als login zegt dat de cookies van je browser niet gelezen konden worden</b></summary>

- **macOS**: het systeem blokkeert terminalprogramma's die browserdata lezen en vraagt niets. Open eenmalig Systeeminstellingen → Privacy en beveiliging → **Volledige schijftoegang**, voeg je terminal-app toe (Terminal, iTerm, Warp of VS Code), sluit die helemaal af en open hem opnieuw. Voer daarna het login-commando opnieuw uit.
- **Windows**: Chrome en Edge vergrendelen hun cookiebestand terwijl ze draaien; de tool kopieert het eerst, dus dit werkt normaal gewoon. Zo niet: sluit de browser en probeer opnieuw, of gebruik `--paste`.
- **Linux**: Chromium-browsers bewaren de cookiesleutel in je sleutelhanger (GNOME Keyring of KWallet), die ontgrendeld moet zijn; Firefox heeft niets nodig. Snap- of Flatpak-browsers zetten hun profiel ergens anders neer; gebruik daar `--paste`.
- Overal: `marktplaats-mcp login --paste` heeft geen rechten nodig. Druk in je browser op marktplaats.nl op F12 → Network, klik op een willekeurig verzoek, kopieer de `Cookie`-header en plak die.
</details>

Of zet `MARKTPLAATS_COOKIE` / `TWEEDEHANDS_COOKIE` (de `Cookie`-header van het verzoek) in de configuratie van je client. Sessies gaan weken mee; loopt er een af, dan geven de tools aan dat je opnieuw moet inloggen.

Een bericht sturen, een verkoper benaderen en bieden geven eerst een voorbeeld en voeren pas iets uit als ze opnieuw worden aangeroepen met `confirm=true`. Een bod is bindend op Marktplaats; de tool weigert biedingen onder het minimum. Automatisch advertenties plaatsen is verboden volgens de voorwaarden van Marktplaats en bewust niet ingebouwd. Zie [Veiligheidsmodel](#-veiligheidsmodel).

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
Ja. Zie [docs/clients.nl.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.nl.md) voor stap-voor-stap instructies per client. Elke client die stdio-servers draait kan `uvx marktplaats-mcp` gebruiken; clients die remote servers ondersteunen kunnen de gehoste URL gebruiken.

### Is dit officieel of verbonden aan Marktplaats?
Nee. Het is een onafhankelijk open-sourceproject zonder banden met Marktplaats, 2dehands of Adevinta. Het gebruikt dezelfde publieke JSON-endpoints als de websites zelf; die API is ongedocumenteerd en kan veranderen, en daarom draait er elke dag een live canary.

### Waarom zie ik soms minder resultaten dan de limiet, of lijkt `total_count` hoog?
Betaalde promoties (DAGTOPPER, TOPADVERTENTIE) worden standaard weggefilterd; geef `include_sponsored=true` mee om ze te zien. `total_count` is het ruwe aantal van de marktplaats, van vóór dat filteren.

### Welke Python-versies worden ondersteund?
3.10 en hoger. CI test 3.11 tot en met 3.13 op Linux, macOS en Windows.

## 📚 Documentatie

- [Installeren in jouw client](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.nl.md): stap voor stap voor 40 clients
- [Configuratie](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/configuration.nl.md): omgevingsvariabelen voor de lokale en gehoste server
- [Hoe dit zich verhoudt tot andere servers](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/comparison.nl.md)
- [Changelog](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/CHANGELOG.md)

## 🗺️ Roadmap

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
