# marktplaats-mcp installeren in jouw client

[← README](../README.nl.md) · English: [clients.md](clients.md) · Français: [clients.fr.md](clients.fr.md)

Je kunt deze server op twee manieren draaien. Kies de manier die jouw client ondersteunt; de tabel hieronder laat per client de snelste route zien.

| | **Gehoste URL** (niets te installeren) | **Lokaal** `uvx marktplaats-mcp` |
|---|---|---|
| Setup | Plak `https://marktplaats-mcp.jaspnerd.dev/mcp` | Installeer [uv](#prerequisite-for-local-installs-uv) en voeg één configregel toe |
| Tools | Zoeken, details, verkopers checken, filters, prijzen, monitoring | Alles, inclusief je eigen berichten, favorieten, biedingen en advertenties na `marktplaats-mcp login` |
| Werkt in | Elke client die een remote (Streamable HTTP) MCP-server accepteert | Elke client die lokale (stdio) MCP-servers draait |

| Client | Snelste manier | Officiële handleiding |
|---|---|---|
| [Claude Code](#claude-code) | `claude mcp add --scope user marktplaats -- uvx marktplaats-mcp` | [MCP in Claude Code](https://code.claude.com/docs/en/mcp) |
| [claude.ai](#claudeai-web-and-mobile) | Settings → Connectors → Add custom connector → URL plakken | [Custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) |
| [Claude Desktop](#claude-desktop) | Zoals claude.ai, of bewerk `claude_desktop_config.json` voor de accounttools | [Lokale servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers) |
| [ChatGPT](#chatgpt) | Settings → Security → Developer mode → voeg de URL toe als app | [Developer mode](https://developers.openai.com/api/docs/guides/developer-mode) |
| [Cursor](#cursor) | [![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=) | [MCP in Cursor](https://cursor.com/docs/mcp) |
| [VS Code / Copilot](#vs-code-and-github-copilot) | [Installeren in VS Code](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) of `code --add-mcp` | [MCP-servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers) |
| [Codex / ChatGPT-desktopapp](#openai-codex-and-the-chatgpt-desktop-app) | `codex mcp add marktplaats -- uvx marktplaats-mcp` | [MCP in Codex](https://developers.openai.com/codex/mcp) |
| [Gemini CLI](#gemini-cli) | `gemini mcp add -s user marktplaats uvx marktplaats-mcp` | [MCP-servers](https://geminicli.com/docs/tools/mcp-server/) |
| [Gemini-app](#gemini-app) | Settings → Connected apps → Custom apps → URL plakken | [Custom apps koppelen](https://support.google.com/gemini/answer/17209137) |
| [Antigravity](#google-antigravity) | MCP Servers → View raw config | [MCP in Antigravity](https://antigravity.google/docs/mcp?tab=ide) |
| [Windsurf / Devin Desktop](#windsurf-devin-desktop) | `devin mcp add marktplaats -- uvx marktplaats-mcp` | [MCP in Cascade](https://docs.devin.ai/desktop/cascade/mcp) |
| [Mistral Le Chat](#mistral-le-chat) | Connectors → Add Connector → Custom MCP Connector → URL plakken | [MCP-connectors](https://docs.mistral.ai/le-chat/knowledge-integrations/connectors/mcp-connectors) |
| [Cline](#cline) | MCP Servers-icoon → Configure → Configure MCP Servers | [MCP-overzicht](https://docs.cline.bot/mcp/mcp-overview) |
| [Roo Code](#roo-code) | MCP-icoon → Edit Global MCP | [MCP gebruiken in Roo](https://docs.roocode.com/features/mcp/using-mcp-in-roo) |
| [JetBrains-IDE's](#jetbrains-ides-ai-assistant-and-junie) | Settings → Tools → AI Assistant → MCP → Add | [Een MCP-server configureren](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html) |
| [Zed](#zed) | Settings → AI → MCP Servers → Add Local Server | [MCP in Zed](https://zed.dev/docs/ai/mcp) |
| [opencode](#opencode) | Toevoegen aan `opencode.json` | [MCP-servers](https://opencode.ai/docs/mcp-servers/) |
| [Goose](#goose) | `goose configure` → Add Extension → Command-line Extension | [Extensies gebruiken](https://goose-docs.ai/docs/getting-started/using-extensions/) |
| [LM Studio](#lm-studio) | [![Add to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D) | [MCP in LM Studio](https://lmstudio.ai/docs/app/mcp) |
| [Perplexity](#perplexity) | Account settings → Connectors → Custom connector → URL plakken | [Custom connectors](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors) |
| [GitHub Copilot CLI](#github-copilot-cli) | `copilot mcp add marktplaats -- uvx marktplaats-mcp` | [MCP-servers toevoegen](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers) |
| [Kiro, Warp, Continue, Trae, Amp, Droid, Qwen Code, Kimi, Raycast, Open WebUI, LibreChat, Jan, ChatWise, Msty, Cherry Studio, 5ire, n8n, Docker, Copilot Studio](#more-clients) | Eén regel per client in de tabel hieronder | |

Elke lokale configuratie hieronder draait hetzelfde commando, `uvx marktplaats-mcp`. Welke client je ook gebruikt, de check is hetzelfde: vraag *"Zoek op Marktplaats een racefiets onder €500 in de buurt van 1011 AB"* en de client hoort `search_listings` aan te roepen.

<a name="prerequisite-for-local-installs-uv"></a>
<details>
<summary><b>Vereiste voor lokale installatie: uv (één minuut)</b></summary>

[uv](https://docs.astral.sh/uv/getting-started/installation/) levert `uvx`, dat `marktplaats-mcp` bij de eerste keer van PyPI downloadt en daarna gecachet houdt. Het haalt ook Python op als je die niet hebt.

| OS | Installeren |
|---|---|
| macOS | `brew install uv` of `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Windows | `winget install --id=astral-sh.uv -e` of `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

Open daarna een **nieuwe** terminal en draai één keer `uvx marktplaats-mcp --help`. De eerste keer duurt tot een minuut omdat de pakketten worden gedownload; daarna start het direct.

**Zegt een client dat hij `uvx` niet kan vinden**, dan komt dat meestal doordat GUI-apps de PATH van je shell niet zien. Vervang `"uvx"` in de config door het volledige pad: `~/.local/bin/uvx` op macOS/Linux (check met `which uvx`), `%USERPROFILE%\.local\bin\uvx.exe` op Windows (`where uvx`). Homebrew zet hem op `/opt/homebrew/bin/uvx`.
</details>

<a name="claude-code"></a>
<details>
<summary><b>Claude Code</b> (CLI)</summary>

Eén commando, beschikbaar in elk project:

```bash
claude mcp add --scope user marktplaats -- uvx marktplaats-mcp
```

Liever het gehoste, read-only endpoint? `claude mcp add --scope user --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`

- **Check:** `claude mcp list` toont `marktplaats: ✔ Connected`, of typ `/mcp` in een sessie. Zegt de eerste check "Failed to connect", wacht dan even: `uvx` is het pakket nog aan het downloaden.
- **Gebruik:** gewoon vragen. Claude kiest zelf de tool en vraagt toestemming de eerste keer dat hij de server aanroept.
- **Eigen account:** draai één keer `marktplaats-mcp login`; geen configwijziging nodig. Of geef de cookie mee met `--env MARKTPLAATS_COOKIE=...` vóór de `--`.
- **Teamproject:** commit een `.mcp.json` met `{"mcpServers": {"marktplaats": {"type": "stdio", "command": "uvx", "args": ["marktplaats-mcp"]}}}` in de root van de repo.
- Docs: [MCP in Claude Code](https://code.claude.com/docs/en/mcp).
</details>

<a name="claudeai-web-and-mobile"></a>
<details>
<summary><b>claude.ai</b> (web en mobiel, alle abonnementen inclusief Free)</summary>

1. Open op [claude.ai](https://claude.ai) **Settings → Connectors** en klik op **Add custom connector**.
2. Noem hem *Marktplaats*, plak `https://marktplaats-mcp.jaspnerd.dev/mcp`, laat de authenticatie op "No sign-in" staan en klik op **Add**.
3. In een chat verschijnt de connector onder de **+**-knop (Connectors). Vraag maar raak.

Free-accounts krijgen één custom connector; Pro en Max zijn onbeperkt. Op Team- en Enterprise-abonnementen voegt een owner hem toe onder **Organization settings → Connectors**, waarna leden op **Connect** klikken. Eenmaal toegevoegd op het web is hij ook beschikbaar in de iOS- en Android-apps. Alleen read-only tools; voor je eigen account installeer je lokaal in Claude Desktop of Claude Code.

Docs: [Aan de slag met custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
</details>

<a name="claude-desktop"></a>
<details>
<summary><b>Claude Desktop</b> (macOS en Windows)</summary>

**Snelst, read-only:** Settings (`Ctrl/Cmd+,`) → **Connectors → Add → Add custom connector**, plak `https://marktplaats-mcp.jaspnerd.dev/mcp`. Zoals bij claude.ai.

**Lokaal, met je eigen account:** open het **Claude**-menu in de menubalk → **Settings… → Developer → Edit Config**. Dat opent `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`). Voeg toe:

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

Sluit Claude Desktop helemaal af en start hem opnieuw. Klik daarna op **+** in het chatvak → **Connectors** om de Marktplaats-tools te zien.

- **Eigen account:** draai `marktplaats-mcp login` in een terminal en herstart Claude Desktop.
- **"Could not attach" / server ontbreekt:** Claude Desktop ziet `uvx` meestal niet op je PATH. Gebruik het absolute pad (`which uvx`, bijvoorbeeld `/Users/you/.local/bin/uvx` of `/opt/homebrew/bin/uvx`). Windows-paden hebben dubbele backslashes nodig. Logs: `~/Library/Logs/Claude/mcp*.log` of `%APPDATA%\Claude\logs`.
- Docs: [Lokale servers koppelen](https://modelcontextprotocol.io/docs/develop/connect-local-servers), [Lokale MCP-servers in Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop).
</details>

<a name="chatgpt"></a>
<details>
<summary><b>ChatGPT</b> (web; Plus, Pro, Business, Enterprise en Edu)</summary>

ChatGPT maakt alleen verbinding met remote servers, dus gebruik het gehoste endpoint (read-only tools).

1. Open in ChatGPT **Settings → Security and login** en zet **Developer mode** aan.
2. Ga naar [chatgpt.com/plugins](https://chatgpt.com/plugins), klik op **+**, kies een naam en beschrijving, plak `https://marktplaats-mcp.jaspnerd.dev/mcp` als MCP-server-URL, zet authenticatie op **No authentication** en klik op **Create**. ChatGPT toont de tools die het heeft gevonden.
3. Klik in een nieuwe chat op **+** → **Developer mode**, vink *Marktplaats* aan en stel je vraag.

In Business-, Enterprise- en Edu-workspaces moet een admin custom MCP-connectors eerst toestaan onder **Workspace settings → Permissions**. Het Free-abonnement heeft geen Developer mode.

Docs: [ChatGPT Developer mode](https://developers.openai.com/api/docs/guides/developer-mode), [Een MCP-server koppelen aan ChatGPT](https://developers.openai.com/plugins/deploy/connect-chatgpt).
</details>

<a name="mistral-le-chat"></a>
<details>
<summary><b>Mistral Le Chat</b> (nu Vibe; web, alle abonnementen inclusief Free)</summary>

1. Open **Connectors** in de zijbalk → **+ Add Connector** → **Custom MCP Connector**.
2. Noem hem `marktplaats` (zonder spaties) en plak `https://marktplaats-mcp.jaspnerd.dev/mcp` als server-URL. Authenticatie wordt automatisch gedetecteerd (niet nodig).
3. Klik in een chat op **+** (of typ `/`) → **Tools** en zet *marktplaats* aan.

Alleen read-only tools. In Team- en Enterprise-workspaces voegt een beheerder de connector toe. Docs: [MCP-connectors](https://docs.mistral.ai/le-chat/knowledge-integrations/connectors/mcp-connectors).
</details>

<a name="cursor"></a>
<details>
<summary><b>Cursor</b></summary>

[![Add marktplaats MCP server to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=)

Klik op de knop en bevestig in Cursor. Of voeg hem handmatig toe aan `~/.cursor/mcp.json` (overal) of `.cursor/mcp.json` (alleen dit project):

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

Gehost, alleen-lezen alternatief: `{"mcpServers": {"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}}}`, of [klik hier](https://cursor.com/install-mcp?name=marktplaats&config=eyJ1cmwiOiJodHRwczovL21hcmt0cGxhYXRzLW1jcC5qYXNwbmVyZC5kZXYvbWNwIn0=).

- **Check:** zijbalk **Customize → MCPs** toont de server met een groene stip en zijn tools; in de toollijst bovenaan het chatpaneel kun je ze aan- en uitzetten.
- **Gebruik:** de Agent kiest zelf de tools en vraagt vóór elke aanroep om goedkeuring, tenzij je ze op de allowlist zet onder Settings → Agents → Approvals & Execution.
- Start hij niet, herstart Cursor dan na het installeren van uv, of gebruik het absolute pad naar `uvx`. Logs: Output-paneel → **MCP Logs**.
- Docs: [MCP in Cursor](https://cursor.com/docs/mcp).
</details>

<a name="vs-code-and-github-copilot"></a>
<details>
<summary><b>VS Code</b> met GitHub Copilot (alle Copilot-abonnementen inclusief Free)</summary>

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_marktplaats-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_marktplaats-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D)

Of vanuit een terminal:

```bash
code --add-mcp '{"name":"marktplaats","command":"uvx","args":["marktplaats-mcp"]}'
```

Of handmatig: Command Palette → **MCP: Open User Configuration** (of maak `.vscode/mcp.json` aan in een project; let op de `servers`-sleutel en het expliciete `type`):

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

Gehost, alleen-lezen alternatief: `"marktplaats": {"type": "http", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`.

- **Check:** Command Palette → **MCP: List Servers** toont hem als running (start hem daar als dat niet zo is). Kies in de Chat-view de **Agent**-modus en klik op het **Configure Tools**-icoon; de Marktplaats-tools staan in de lijst.
- **Gebruik:** vraag het in Agent-modus; VS Code vraagt je de eerste aanroepen toe te staan met **Allow**. Vertrouw de server als daarom wordt gevraagd.
- Docs: [MCP-servers toevoegen en beheren in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
</details>

<a name="openai-codex-and-the-chatgpt-desktop-app"></a>
<details>
<summary><b>OpenAI Codex</b> (CLI, IDE-extensie en de ChatGPT-desktopapp)</summary>

```bash
codex mcp add marktplaats -- uvx marktplaats-mcp
```

Dat schrijft naar `~/.codex/config.toml`, dat de Codex CLI, de Codex IDE-extensie en de ChatGPT-desktopapp allemaal delen:

```toml
[mcp_servers.marktplaats]
command = "uvx"
args = ["marktplaats-mcp"]
```

Gehost, alleen-lezen alternatief: `codex mcp add marktplaats --url https://marktplaats-mcp.jaspnerd.dev/mcp`.

In de IDE-extensie of de desktopapp kun je ook op het tandwiel klikken → **MCP servers → Add server**, **STDIO** kiezen, het commando `uvx marktplaats-mcp` invullen, opslaan en op **Restart** klikken.

- **Check:** `codex mcp list`, of `/mcp` in de Codex-composer.
- **Gebruik:** vraag; Codex vraagt om bevestiging bij tools die niet read-only zijn. Loopt de eerste start vast op een time-out terwijl `uvx` downloadt, voeg dan `startup_timeout_sec = 60` toe onder de server.
- Docs: [MCP in Codex](https://developers.openai.com/codex/mcp).
</details>

<a name="gemini-cli"></a>
<details>
<summary><b>Gemini CLI</b></summary>

```bash
gemini mcp add -s user marktplaats uvx marktplaats-mcp
```

Gehost, alleen-lezen alternatief: `gemini mcp add -s user --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`.

Of voeg toe aan `~/.gemini/settings.json` (of `.gemini/settings.json` in een project):

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

- **Check:** `gemini mcp list`, of `/mcp` in de CLI toont CONNECTED en de toollijst. Lokale servers starten alleen in een vertrouwde map: draai zo nodig eerst `gemini trust`.
- **Gebruik:** vraag; Gemini biedt "Proceed once / Always allow this tool / Always allow this server" aan.
- Docs: [MCP-servers in Gemini CLI](https://geminicli.com/docs/tools/mcp-server/).
</details>

<a name="gemini-app"></a>
<details>
<summary><b>Gemini-app</b> (gemini.google.com en mobiel)</summary>

Open op [gemini.google.com](https://gemini.google.com) **Settings → Connected apps** en voeg onder **Custom apps** `https://marktplaats-mcp.jaspnerd.dev/mcp` toe. Eenmaal gekoppeld werkt het ook in de mobiele app; noem hem met `@` in een prompt. Google beperkt custom apps momenteel tot persoonlijke accounts, 18+, in de VS, met Gemini Activity aan. Alleen read-only tools.

Docs: [Custom apps koppelen aan Gemini](https://support.google.com/gemini/answer/17209137).
</details>

<a name="google-antigravity"></a>
<details>
<summary><b>Google Antigravity</b></summary>

Klik in het agentpaneel op **… → MCP Servers → Manage MCP Servers → View raw config** en voeg toe aan `~/.gemini/config/mcp_config.json` (of `.agents/mcp_config.json` in een project):

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

Gehost, alleen-lezen alternatief: `"marktplaats": {"serverUrl": "https://marktplaats-mcp.jaspnerd.dev/mcp"}` (Antigravity gebruikt `serverUrl`, niet `url`).

Typ `/mcp` om de MCP-manager te openen en te controleren of de tools in de lijst staan; tools draaien standaard in de "Ask"-modus. Docs: [MCP in Antigravity](https://antigravity.google/docs/mcp?tab=ide).
</details>

<a name="windsurf-devin-desktop"></a>
<details>
<summary><b>Windsurf</b> (nu Devin Desktop)</summary>

Windsurf heet nu Devin Desktop. De standaardagent **Devin Local** configureer je vanuit een terminal:

```bash
devin mcp add marktplaats -- uvx marktplaats-mcp
```

Dat schrijft `~/.config/devin/mcp_config.json` (Windows: `%APPDATA%\devin\mcp_config.json`); gebruik `.devin/mcp_config.json` voor één project. Devin vraagt vóór elke toolaanroep om toestemming, tenzij je `mcp__marktplaats__*` toestaat in zijn permissions.

Voor de oudere **Cascade**-agent: **Devin Settings → Cascade → MCP Servers** (of het MCPs-icoon in het Cascade-paneel) → **View raw config**, dat is `~/.codeium/windsurf/mcp_config.json`:

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

Gehost, alleen-lezen alternatief voor Cascade: `"marktplaats": {"serverUrl": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`. Druk daarna op de verversknop in het MCP-paneel; Cascade staat in totaal maximaal 100 tools toe over alle servers samen.

Docs: [MCP in Cascade](https://docs.devin.ai/desktop/cascade/mcp), [MCP-configuratie van de Devin CLI](https://docs.devin.ai/cli/extensibility/mcp/configuration).
</details>

<a name="cline"></a>
<details>
<summary><b>Cline</b> (VS Code, JetBrains, CLI)</summary>

Klik op het **MCP Servers**-icoon in de bovenste werkbalk van Cline → tabblad **Configure** → **Configure MCP Servers**. Dat opent `cline_mcp_settings.json` (`~/.cline/data/settings/`); voeg toe:

```json
{
  "mcpServers": {
    "marktplaats": {
      "command": "uvx",
      "args": ["marktplaats-mcp"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Gehost, alleen-lezen alternatief: tabblad **Remote Servers** → naam *marktplaats*, URL `https://marktplaats-mcp.jaspnerd.dev/mcp`, transport **Streamable HTTP** → **Add Server**.

- **Check:** de server verschijnt in het MCP-paneel met zijn tools; gebruik daar de herstartknop als hij een fout toont.
- **Gebruik:** vraag; keur elke aanroep goed, of zet veilige tools zoals `search_listings` in `autoApprove`.
- Docs: [MCP-overzicht](https://docs.cline.bot/mcp/mcp-overview).
</details>

<a name="roo-code"></a>
<details>
<summary><b>Roo Code</b></summary>

Klik op het **MCP**-icoon in het Roo Code-paneel → **Edit Global MCP** (of **Edit Project MCP** voor `.roo/mcp.json`):

```json
{
  "mcpServers": {
    "marktplaats": {
      "command": "uvx",
      "args": ["marktplaats-mcp"],
      "alwaysAllow": ["search_listings", "get_listing_details", "analyze_prices"]
    }
  }
}
```

Gehost, alleen-lezen alternatief: `"marktplaats": {"type": "streamable-http", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}` (het `type` is verplicht bij URL's). Op Windows wikkel je lokale commando's in: `"command": "cmd", "args": ["/c", "uvx", "marktplaats-mcp"]`.

De server en zijn tools verschijnen in dezelfde MCP-view; herstart VS Code als dat niet gebeurt. Docs: [MCP gebruiken in Roo Code](https://docs.roocode.com/features/mcp/using-mcp-in-roo).
</details>

<a name="jetbrains-ides-ai-assistant-and-junie"></a>
<details>
<summary><b>JetBrains-IDE's</b> (AI Assistant en Junie)</summary>

**AI Assistant:** **Settings → Tools → AI Assistant → Model Context Protocol (MCP) → Add**, kies **STDIO** en plak:

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

Klik op **Apply**; de kolom **Status** springt op connected en de tools zijn beschikbaar in de AI-chat (de AI kiest ze zelf, of typ `/` om er een aan te roepen). Voor het gehoste endpoint kies je **HTTP** en plak je `{"mcpServers": {"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}}}`. Blijft de status rood, vervang `uvx` dan door het absolute pad.

**Junie** heeft een eigen lijst: **Settings → Tools → Junie → MCP Settings → Add**, dezelfde JSON, opgeslagen in `~/.junie/mcp/mcp.json` (of `.junie/mcp/mcp.json` per project). De Junie CLI leest hetzelfde bestand.

Docs: [Een MCP-server configureren](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html), [Junie MCP-instellingen](https://junie.jetbrains.com/docs/junie-plugin-mcp-settings.html).
</details>

<a name="zed"></a>
<details>
<summary><b>Zed</b></summary>

**Settings → AI → MCP Servers → Add Server → Add Local Server**, of zet dit in `settings.json`:

```json
{
  "context_servers": {
    "marktplaats": {
      "command": "uvx",
      "args": ["marktplaats-mcp"]
    }
  }
}
```

Gehost, alleen-lezen alternatief: `"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`.

De stip naast de server in **Settings → AI → MCP Servers** wordt groen ("Server is active"). De tools zijn beschikbaar in het Agent Panel en vragen standaard om bevestiging. Docs: [MCP in Zed](https://zed.dev/docs/ai/mcp).
</details>

<a name="opencode"></a>
<details>
<summary><b>opencode</b></summary>

Voeg toe aan `~/.config/opencode/opencode.json` (overal) of `opencode.json` in een project:

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

Gehost, alleen-lezen alternatief: `"marktplaats": {"type": "remote", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp", "enabled": true}`.

Check met `opencode mcp list` (`opencode mcp debug marktplaats` als er iets mis is) en vraag daarna gewoon. Docs: [MCP-servers in opencode](https://opencode.ai/docs/mcp-servers/).
</details>

<a name="goose"></a>
<details>
<summary><b>Goose</b> (CLI en desktop)</summary>

Draai `goose configure` → **Add Extension** → **Command-line Extension**, noem hem *marktplaats*, commando `uvx marktplaats-mcp`, accepteer de standaardwaarden. Of voeg toe aan `~/.config/goose/config.yaml`:

```yaml
extensions:
  marktplaats:
    name: Marktplaats
    type: stdio
    cmd: uvx
    args: [marktplaats-mcp]
    enabled: true
    timeout: 300
```

Gehost, alleen-lezen alternatief: `type: streamable_http` met `uri: https://marktplaats-mcp.jaspnerd.dev/mcp`. Voor de desktopapp open je deze link: `goose://extension?cmd=uvx&arg=marktplaats-mcp&id=marktplaats&name=Marktplaats&description=Search%20Marktplaats%20and%202dehands`.

Check met `goose info -v` (toont de ingeschakelde extensies) of de zijbalk **Extensions** in de desktopapp. Docs: [Extensies gebruiken](https://goose-docs.ai/docs/getting-started/using-extensions/).
</details>

<a name="lm-studio"></a>
<details>
<summary><b>LM Studio</b> (lokale modellen)</summary>

[![Add MCP Server marktplaats to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D)

Of open het tabblad **Program** in de rechterzijbalk → **Install → Edit mcp.json** (`~/.lmstudio/mcp.json`, Windows `%USERPROFILE%\.lmstudio\mcp.json`) en plak dezelfde JSON als bij Cursor:

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

Gehost, alleen-lezen alternatief: `"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`. Kies een model dat tool calling ondersteunt; LM Studio vraagt bij elke toolaanroep om bevestiging en je kunt hem "always allow" geven. `uvx` moet op je PATH staan, dus herstart LM Studio na het installeren van uv. Docs: [MCP in LM Studio](https://lmstudio.ai/docs/app/mcp).
</details>

<a name="perplexity"></a>
<details>
<summary><b>Perplexity</b> (web en desktopapps)</summary>

**Gehost:** **Account settings → Connectors → + Custom connector → Remote**. Naam *Marktplaats*, URL `https://marktplaats-mcp.jaspnerd.dev/mcp`, authenticatie **None**, transport **Streamable HTTP**, vink de bevestiging aan, **Add**, en klik daarna op de connectorkaart om hem in te schakelen. Alleen read-only tools.

**Lokaal (macOS-app uit de Mac App Store):** dezelfde pagina, installeer de *PerplexityXPC*-helper als daarom wordt gevraagd, **Add Connector → Simple**, servernaam *Marktplaats*, commando `uvx marktplaats-mcp`, **Save**. Wacht tot de status *Running* zegt en zet hem daarna aan onder **Sources** in een chat. Toolaanroepen vragen om bevestiging.

Docs: [Custom remote connectors](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors), [Lokale en remote MCP's](https://www.perplexity.ai/help-center/en/articles/11502712-local-and-remote-mcps-for-perplexity).
</details>

<a name="github-copilot-cli"></a>
<details>
<summary><b>GitHub Copilot CLI</b></summary>

```bash
copilot mcp add marktplaats -- uvx marktplaats-mcp
```

Gehost, alleen-lezen alternatief: `copilot mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`. In een sessie opent `/mcp add` hetzelfde formulier en is de server direct beschikbaar. De config staat in `~/.copilot/mcp-config.json`; een repo kan een `.github/mcp.json` meeleveren met de VS Code-achtige `{"mcpServers": {"marktplaats": {"type": "stdio", "command": "uvx", "args": ["marktplaats-mcp"], "tools": ["*"]}}}`.

Check met `/mcp show marktplaats` of `copilot mcp list`. Docs: [MCP-servers toevoegen aan Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers).
</details>

<a name="more-clients"></a>
<details>
<summary><b>Meer clients</b> (Kiro, Warp, Continue, Trae, Amp, Droid, Qwen Code, Kimi, Raycast, Open WebUI, LibreChat, Jan, ChatWise, Msty, Cherry Studio, 5ire, n8n, Docker, Copilot Studio, Ollama)</summary>

Lokaal betekent `uvx marktplaats-mcp` via stdio; gehost betekent de read-only URL `https://marktplaats-mcp.jaspnerd.dev/mcp`. "Claude-stijl JSON" is het blok `{"mcpServers": {"marktplaats": {"command": "uvx", "args": ["marktplaats-mcp"]}}}` uit de Claude Desktop-sectie.

| Client | Lokale installatie | Gehoste URL | Docs |
|---|---|---|---|
| **Kiro** (IDE en CLI, ex-Amazon Q) | [Toevoegen aan Kiro](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D), of Claude-stijl JSON in `~/.kiro/settings/mcp.json`; CLI: `kiro-cli mcp add --name marktplaats --command "uvx marktplaats-mcp" --scope global`. Het tabblad MCP servers in het Kiro-paneel toont hem als connected | [Toevoegen aan Kiro](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22url%22%3A%22https%3A%2F%2Fmarktplaats-mcp.jaspnerd.dev%2Fmcp%22%7D) | [MCP-configuratie](https://kiro.dev/docs/mcp/configuration/) |
| **Warp** | **Settings → Agents → MCP servers → + Add**, plak Claude-stijl JSON (of schrijf het naar `~/.warp/.mcp.json`). Warp pikt ook servers op uit de configs van Claude Code en Codex als *Auto-spawn servers from third-party agents* aanstaat | Hetzelfde dialoogvenster met `{"mcpServers": {"marktplaats": {"url": "…/mcp"}}}` | [MCP in Warp](https://docs.warp.dev/agent-platform/capabilities/mcp/) |
| **Continue** | Voeg in `~/.continue/config.yaml` onder `mcpServers:` toe: `- name: marktplaats`, `type: stdio`, `command: uvx`, `args: ["marktplaats-mcp"]`; of zet Claude-stijl JSON in `.continue/mcpServers/`. Tools verschijnen alleen in Agent-modus | `type: streamable-http`, `url: …/mcp` | [MCP deep dive](https://docs.continue.dev/customize/deep-dives/mcp) |
| **Trae** | Settings → **MCP → Add → Add Manually**, plak Claude-stijl JSON (of `.trae/mcp.json` per project). De ingebouwde Agent krijgt alle servers | `{"mcpServers": {"marktplaats": {"url": "…/mcp"}}}` | [MCP-servers toevoegen](https://docs.trae.ai/ide/add-mcp-servers) |
| **Amp** | `amp mcp add marktplaats -- uvx marktplaats-mcp`; check met `amp mcp doctor` | `amp mcp add marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` | [MCP in Amp](https://ampcode.com/docs/customize/mcp) |
| **Factory Droid** | `droid mcp add marktplaats "uvx marktplaats-mcp"`; check met `droid mcp list` of `/mcp` | `droid mcp add marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp --type http` | [MCP in Droid](https://docs.factory.ai/cli/configuration/mcp) |
| **Qwen Code** | `qwen mcp add --transport stdio marktplaats uvx marktplaats-mcp`; check met `/mcp` | `qwen mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` (de configsleutel is `httpUrl`) | [MCP in Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/) |
| **Kimi CLI** | `kimi mcp add --transport stdio marktplaats -- uvx marktplaats-mcp`; check met `kimi mcp test marktplaats` | `kimi mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` | [MCP in Kimi CLI](https://moonshotai.github.io/kimi-cli/en/customization/mcp.html) |
| **Raycast AI** (Pro) | Draai het commando **Install MCP Server**, transport **Standard Input/Output**, commando `uvx`, argumenten `marktplaats-mcp`; typ daarna `@marktplaats` in AI Chat | Hetzelfde commando, transport **HTTP**, plak de URL (de enige optie op iOS) | [MCP in Raycast](https://manual.raycast.com/ai/model-context-protocol) |
| **Open WebUI** | Native MCP is alleen HTTP. Voor lokaal maak je een brug: `uvx mcpo --port 8000 -- uvx marktplaats-mcp`, en voeg daarna `http://localhost:8000` toe als OpenAPI-toolserver | Admin → **Settings → Integrations → External Tool Servers → Add**, type **MCP (Streamable HTTP)**, auth **None** | [MCP in Open WebUI](https://docs.openwebui.com/features/extensibility/mcp/) |
| **LibreChat** | Voeg in `librechat.yaml` onder `mcpServers:` `marktplaats:` toe met `type: stdio`, `command: uvx`, `args: ["marktplaats-mcp"]` en herstart daarna | `type: streamable-http`, `url: …/mcp` | [MCP-servers](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers) |
| **Jan** | **Settings → MCP Servers → + Add MCP Server**, transport **STDIO**, commando `uvx`, args `marktplaats-mcp`; kies een model met de *tools*-capability | Hetzelfde dialoogvenster, transport **HTTP** | [MCP-servers in Jan](https://www.jan.ai/docs/desktop/integrations/mcp-servers) |
| **ChatWise** | **Settings → Tools → +**, type **Command Line (stdio)**, commando `uvx marktplaats-mcp`; of plak `{"mcpServers": {"marktplaats": {"command": "uvx marktplaats-mcp"}}}` via *Import JSON from Clipboard* | Type **Streamable HTTP** | [Tools](https://docs.chatwise.app/tools) |
| **Msty Studio** | **Toolbox → Add New Tool → STDIO / JSON**, plak `{"command": "uvx", "args": ["marktplaats-mcp"]}` | **Add New Tool → HTTP**, plak de URL | [Tools](https://docs.msty.ai/studio/toolbox/tools) |
| **Cherry Studio** | **Settings → MCP → Add**, type stdio, commando `uvx`, args `marktplaats-mcp` (of importeer Claude-stijl JSON), en zet hem daarna aan op een agent | Hetzelfde dialoogvenster, Streamable HTTP | [MCP](https://docs.cherryai.com.cn/advanced-basic/extensions/mcp.md) |
| **5ire** | Tools → toevoegen met `{"name": "marktplaats", "command": "uvx", "args": ["marktplaats-mcp"]}` | `{"name": "marktplaats", "url": "…/mcp"}` | [5ire-docs](https://5ire.app/docs) |
| **n8n** | Niet ondersteund (alleen remote) | Voeg een **MCP Client Tool**-node toe aan een AI Agent, transport **HTTP Streamable**, endpoint `…/mcp`, authenticatie **None** | [MCP Client Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/) |
| **Docker MCP Toolkit** | Bouw de image vanuit de `Dockerfile` in deze repo en voeg hem toe aan een profiel met `docker mcp profile server add <profile> --server file://marktplaats.yaml` | `docker mcp profile server add <profile> --server https://registry.modelcontextprotocol.io/v0/servers/io.github.jasp-nerd/marktplaats-mcp` | [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/) |
| **Microsoft Copilot Studio** | Niet ondersteund (alleen remote) | Agent → **Tools → Add a tool → New tool → Model Context Protocol**, server-URL `…/mcp`, authenticatie **None**. De consumentenversie van Copilot heeft geen custom connectors | [Een MCP-server toevoegen](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent) |
| **Ollama** | Geen MCP-ondersteuning in de app of CLI. Gebruik `ollama launch claude` / `codex` / `opencode` met een lokaal model en voeg de server toe in die client | Hetzelfde | [ollama launch](https://docs.ollama.com/cli) |
</details>
