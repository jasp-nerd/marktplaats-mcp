# Install marktplaats-mcp in your client

[← README](../README.md) · Nederlands: [clients.nl.md](clients.nl.md) · Français: [clients.fr.md](clients.fr.md)

There are two ways to run this server. Pick the one your client supports; the table below shows the fastest route per client.

| | **Hosted URL** (nothing to install) | **Local** `uvx marktplaats-mcp` |
|---|---|---|
| Setup | Paste `https://marktplaats-mcp.jaspnerd.dev/mcp` | Install [uv](#prerequisite-for-local-installs-uv), then add one config line |
| Tools | Search, details, seller checks, filters, prices, monitoring | Everything, including your own messages, favorites, bids and ads after `marktplaats-mcp login` |
| Works in | Any client that accepts a remote (Streamable HTTP) MCP server | Any client that runs local (stdio) MCP servers |

| Client | Fastest way | Official guide |
|---|---|---|
| [Claude Code](#claude-code) | `claude mcp add --scope user marktplaats -- uvx marktplaats-mcp` | [MCP in Claude Code](https://code.claude.com/docs/en/mcp) |
| [claude.ai](#claudeai-web-and-mobile) | Settings → Connectors → Add custom connector → paste URL | [Custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) |
| [Claude Desktop](#claude-desktop) | Same as claude.ai, or edit `claude_desktop_config.json` for the account tools | [Local servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers) |
| [ChatGPT](#chatgpt) | Settings → Security → Developer mode → add the URL as an app | [Developer mode](https://developers.openai.com/api/docs/guides/developer-mode) |
| [Cursor](#cursor) | [![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=) | [MCP in Cursor](https://cursor.com/docs/mcp) |
| [VS Code / Copilot](#vs-code-and-github-copilot) | [Install in VS Code](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) or `code --add-mcp` | [MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers) |
| [Codex / ChatGPT desktop app](#openai-codex-and-the-chatgpt-desktop-app) | `codex mcp add marktplaats -- uvx marktplaats-mcp` | [MCP in Codex](https://developers.openai.com/codex/mcp) |
| [Gemini CLI](#gemini-cli) | `gemini mcp add -s user marktplaats uvx marktplaats-mcp` | [MCP servers](https://geminicli.com/docs/tools/mcp-server/) |
| [Gemini app](#gemini-app) | Settings → Connected apps → Custom apps → paste URL | [Connect custom apps](https://support.google.com/gemini/answer/17209137) |
| [Antigravity](#google-antigravity) | MCP Servers → View raw config | [MCP in Antigravity](https://antigravity.google/docs/mcp?tab=ide) |
| [Windsurf / Devin Desktop](#windsurf-devin-desktop) | `devin mcp add marktplaats -- uvx marktplaats-mcp` | [MCP in Cascade](https://docs.devin.ai/desktop/cascade/mcp) |
| [Mistral Le Chat](#mistral-le-chat) | Connectors → Add Connector → Custom MCP Connector → paste URL | [MCP connectors](https://docs.mistral.ai/le-chat/knowledge-integrations/connectors/mcp-connectors) |
| [Cline](#cline) | MCP Servers icon → Configure → Configure MCP Servers | [MCP overview](https://docs.cline.bot/mcp/mcp-overview) |
| [Roo Code](#roo-code) | MCP icon → Edit Global MCP | [Using MCP in Roo](https://docs.roocode.com/features/mcp/using-mcp-in-roo) |
| [JetBrains IDEs](#jetbrains-ides-ai-assistant-and-junie) | Settings → Tools → AI Assistant → MCP → Add | [Configure an MCP server](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html) |
| [Zed](#zed) | Settings → AI → MCP Servers → Add Local Server | [MCP in Zed](https://zed.dev/docs/ai/mcp) |
| [opencode](#opencode) | Add to `opencode.json` | [MCP servers](https://opencode.ai/docs/mcp-servers/) |
| [Goose](#goose) | `goose configure` → Add Extension → Command-line Extension | [Using extensions](https://goose-docs.ai/docs/getting-started/using-extensions/) |
| [LM Studio](#lm-studio) | [![Add to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D) | [MCP in LM Studio](https://lmstudio.ai/docs/app/mcp) |
| [Perplexity](#perplexity) | Account settings → Connectors → Custom connector → paste URL | [Custom connectors](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors) |
| [GitHub Copilot CLI](#github-copilot-cli) | `copilot mcp add marktplaats -- uvx marktplaats-mcp` | [Add MCP servers](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers) |
| [Kiro, Warp, Continue, Trae, Amp, Droid, Qwen Code, Kimi, Raycast, Open WebUI, LibreChat, Jan, ChatWise, Msty, Cherry Studio, 5ire, n8n, Docker, Copilot Studio](#more-clients) | One line each in the table below | |

Every local config below runs the same command, `uvx marktplaats-mcp`. Whichever client you use, the check is the same: ask *"Search Marktplaats for a racefiets under €500 near 1011 AB"* and the client should call `search_listings`.

<a name="prerequisite-for-local-installs-uv"></a>
<details>
<summary><b>Prerequisite for local installs: uv (one minute)</b></summary>

[uv](https://docs.astral.sh/uv/getting-started/installation/) provides `uvx`, which downloads `marktplaats-mcp` from PyPI on first run and keeps it cached. It also fetches Python if you have none.

| OS | Install |
|---|---|
| macOS | `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Windows | `winget install --id=astral-sh.uv -e` or `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

Open a **new** terminal afterwards and run `uvx marktplaats-mcp --help` once. The first run takes up to a minute while packages download; after that it starts instantly.

**If a client says it cannot find `uvx`**, GUI apps often do not see your shell's PATH. Replace `"uvx"` in the config with the full path: `~/.local/bin/uvx` on macOS/Linux (check with `which uvx`), `%USERPROFILE%\.local\bin\uvx.exe` on Windows (`where uvx`). Homebrew installs it at `/opt/homebrew/bin/uvx`.
</details>

<a name="claude-code"></a>
<details>
<summary><b>Claude Code</b> (CLI)</summary>

One command, available in every project:

```bash
claude mcp add --scope user marktplaats -- uvx marktplaats-mcp
```

Prefer the hosted, read-only endpoint? `claude mcp add --scope user --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`

- **Check:** `claude mcp list` shows `marktplaats: ✔ Connected`, or type `/mcp` inside a session. If the first check says "Failed to connect", wait a moment: `uvx` is still downloading the package.
- **Use:** just ask. Claude picks the tool itself and asks permission the first time it calls the server.
- **Own account:** run `marktplaats-mcp login` once; no config change needed. Or pass the cookie with `--env MARKTPLAATS_COOKIE=...` before the `--`.
- **Team project:** commit a `.mcp.json` with `{"mcpServers": {"marktplaats": {"type": "stdio", "command": "uvx", "args": ["marktplaats-mcp"]}}}` in the repo root.
- Docs: [MCP in Claude Code](https://code.claude.com/docs/en/mcp).
</details>

<a name="claudeai-web-and-mobile"></a>
<details>
<summary><b>claude.ai</b> (web and mobile, all plans including Free)</summary>

1. On [claude.ai](https://claude.ai) open **Settings → Connectors** and click **Add custom connector**.
2. Name it *Marktplaats*, paste `https://marktplaats-mcp.jaspnerd.dev/mcp`, leave authentication on "No sign-in", click **Add**.
3. In a chat, the connector appears under the **+** button (Connectors). Ask away.

Free accounts get one custom connector; Pro and Max are unlimited. On Team and Enterprise plans an owner adds it under **Organization settings → Connectors**, then members click **Connect**. Once added on the web it is available in the iOS and Android apps too. Read-only tools only; for your own account install locally in Claude Desktop or Claude Code.

Docs: [Get started with custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
</details>

<a name="claude-desktop"></a>
<details>
<summary><b>Claude Desktop</b> (macOS and Windows)</summary>

**Fastest, read-only:** Settings (`Ctrl/Cmd+,`) → **Connectors → Add → Add custom connector**, paste `https://marktplaats-mcp.jaspnerd.dev/mcp`. Same as claude.ai.

**Local, with your own account:** open the **Claude** menu in the menu bar → **Settings… → Developer → Edit Config**. That opens `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`). Add:

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

Quit Claude Desktop completely and start it again. Then click **+** in the chat box → **Connectors** to see the Marktplaats tools.

- **Own account:** run `marktplaats-mcp login` in a terminal, restart Claude Desktop.
- **"Could not attach" / server missing:** Claude Desktop usually cannot see `uvx` on your PATH. Use the absolute path (`which uvx`, e.g. `/Users/you/.local/bin/uvx` or `/opt/homebrew/bin/uvx`). Windows paths need double backslashes. Logs: `~/Library/Logs/Claude/mcp*.log` or `%APPDATA%\Claude\logs`.
- Docs: [Connect local servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers), [Local MCP servers on Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop).
</details>

<a name="chatgpt"></a>
<details>
<summary><b>ChatGPT</b> (web; Plus, Pro, Business, Enterprise and Edu)</summary>

ChatGPT connects to remote servers only, so use the hosted endpoint (read-only tools).

1. In ChatGPT open **Settings → Security and login** and turn on **Developer mode**.
2. Go to [chatgpt.com/plugins](https://chatgpt.com/plugins), click **+**, choose a name and description, paste `https://marktplaats-mcp.jaspnerd.dev/mcp` as the MCP server URL, set authentication to **No authentication** and click **Create**. ChatGPT lists the tools it discovered.
3. In a new chat click **+** → **Developer mode** and tick *Marktplaats*, then ask.

On Business, Enterprise and Edu workspaces an admin must first allow custom MCP connectors under **Workspace settings → Permissions**. The Free plan has no Developer mode.

Docs: [ChatGPT Developer mode](https://developers.openai.com/api/docs/guides/developer-mode), [Connect an MCP server to ChatGPT](https://developers.openai.com/plugins/deploy/connect-chatgpt).
</details>

<a name="mistral-le-chat"></a>
<details>
<summary><b>Mistral Le Chat</b> (now Vibe; web, all plans including Free)</summary>

1. Open **Connectors** in the sidebar → **+ Add Connector** → **Custom MCP Connector**.
2. Name it `marktplaats` (no spaces), paste `https://marktplaats-mcp.jaspnerd.dev/mcp` as the server URL. Authentication is detected automatically (none needed).
3. In a chat click **+** (or type `/`) → **Tools** and enable *marktplaats*.

Read-only tools. On Team and Enterprise workspaces an administrator adds the connector. Docs: [MCP connectors](https://docs.mistral.ai/le-chat/knowledge-integrations/connectors/mcp-connectors).
</details>

<a name="cursor"></a>
<details>
<summary><b>Cursor</b></summary>

[![Add marktplaats MCP server to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=)

Click the button and confirm in Cursor. Or add it by hand to `~/.cursor/mcp.json` (everywhere) or `.cursor/mcp.json` (this project):

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

Hosted, read-only alternative: `{"mcpServers": {"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}}}`, or [click here](https://cursor.com/install-mcp?name=marktplaats&config=eyJ1cmwiOiJodHRwczovL21hcmt0cGxhYXRzLW1jcC5qYXNwbmVyZC5kZXYvbWNwIn0=).

- **Check:** sidebar **Customize → MCPs** shows the server with a green dot and its tools; the tools list at the top of the chat panel lets you toggle them.
- **Use:** the Agent picks the tools itself and asks approval before each call unless you allowlist them under Settings → Agents → Approvals & Execution.
- If it fails to start, restart Cursor after installing uv, or use the absolute path to `uvx`. Logs: Output panel → **MCP Logs**.
- Docs: [MCP in Cursor](https://cursor.com/docs/mcp).
</details>

<a name="vs-code-and-github-copilot"></a>
<details>
<summary><b>VS Code</b> with GitHub Copilot (all Copilot plans including Free)</summary>

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_marktplaats-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_marktplaats-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D)

Or from a terminal:

```bash
code --add-mcp '{"name":"marktplaats","command":"uvx","args":["marktplaats-mcp"]}'
```

Or by hand: Command Palette → **MCP: Open User Configuration** (or create `.vscode/mcp.json` in a project; note the `servers` key and explicit `type`):

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

Hosted, read-only alternative: `"marktplaats": {"type": "http", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`.

- **Check:** Command Palette → **MCP: List Servers** shows it running (start it there if not). In the Chat view choose **Agent** mode and click the **Configure Tools** icon; the Marktplaats tools are listed.
- **Use:** ask in Agent mode; VS Code asks you to **Allow** the first calls. Trust the server when prompted.
- Docs: [Add and manage MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
</details>

<a name="openai-codex-and-the-chatgpt-desktop-app"></a>
<details>
<summary><b>OpenAI Codex</b> (CLI, IDE extension and the ChatGPT desktop app)</summary>

```bash
codex mcp add marktplaats -- uvx marktplaats-mcp
```

That writes to `~/.codex/config.toml`, which the Codex CLI, the Codex IDE extension and the ChatGPT desktop app all share:

```toml
[mcp_servers.marktplaats]
command = "uvx"
args = ["marktplaats-mcp"]
```

Hosted, read-only alternative: `codex mcp add marktplaats --url https://marktplaats-mcp.jaspnerd.dev/mcp`.

In the IDE extension or the desktop app you can also click the gear → **MCP servers → Add server**, choose **STDIO**, enter the command `uvx marktplaats-mcp`, save and **Restart**.

- **Check:** `codex mcp list`, or `/mcp` in the Codex composer.
- **Use:** ask; Codex prompts before tools that are not read-only. If the first start times out while `uvx` downloads, add `startup_timeout_sec = 60` under the server.
- Docs: [MCP in Codex](https://developers.openai.com/codex/mcp).
</details>

<a name="gemini-cli"></a>
<details>
<summary><b>Gemini CLI</b></summary>

```bash
gemini mcp add -s user marktplaats uvx marktplaats-mcp
```

Hosted, read-only alternative: `gemini mcp add -s user --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`.

Or add to `~/.gemini/settings.json` (or `.gemini/settings.json` in a project):

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

- **Check:** `gemini mcp list`, or `/mcp` inside the CLI shows CONNECTED and the tool list. Local servers only start in a trusted folder: run `gemini trust` first if needed.
- **Use:** ask; Gemini offers "Proceed once / Always allow this tool / Always allow this server".
- Docs: [MCP servers in Gemini CLI](https://geminicli.com/docs/tools/mcp-server/).
</details>

<a name="gemini-app"></a>
<details>
<summary><b>Gemini app</b> (gemini.google.com and mobile)</summary>

On [gemini.google.com](https://gemini.google.com) open **Settings → Connected apps**, then under **Custom apps** add `https://marktplaats-mcp.jaspnerd.dev/mcp`. Once connected it works in the mobile app as well; mention it with `@` in a prompt. Google currently limits custom apps to personal accounts, 18+, in the US, with Gemini Activity on. Read-only tools.

Docs: [Connect custom apps to Gemini](https://support.google.com/gemini/answer/17209137).
</details>

<a name="google-antigravity"></a>
<details>
<summary><b>Google Antigravity</b></summary>

In the agent panel click **… → MCP Servers → Manage MCP Servers → View raw config** and add to `~/.gemini/config/mcp_config.json` (or `.agents/mcp_config.json` in a project):

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

Hosted, read-only alternative: `"marktplaats": {"serverUrl": "https://marktplaats-mcp.jaspnerd.dev/mcp"}` (Antigravity uses `serverUrl`, not `url`).

Type `/mcp` to open the MCP manager and confirm the tools are listed; tools run in "Ask" mode by default. Docs: [MCP in Antigravity](https://antigravity.google/docs/mcp?tab=ide).
</details>

<a name="windsurf-devin-desktop"></a>
<details>
<summary><b>Windsurf</b> (now Devin Desktop)</summary>

Windsurf was renamed Devin Desktop. The default **Devin Local** agent is configured from a terminal:

```bash
devin mcp add marktplaats -- uvx marktplaats-mcp
```

That writes `~/.config/devin/mcp_config.json` (Windows: `%APPDATA%\devin\mcp_config.json`); use `.devin/mcp_config.json` for one project. Devin asks before every tool call unless you allow `mcp__marktplaats__*` in its permissions.

For the legacy **Cascade** agent: **Devin Settings → Cascade → MCP Servers** (or the MCPs icon in the Cascade panel) → **View raw config**, which is `~/.codeium/windsurf/mcp_config.json`:

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

Hosted, read-only alternative for Cascade: `"marktplaats": {"serverUrl": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`. Press the refresh button in the MCP panel afterwards; Cascade caps you at 100 tools in total across servers.

Docs: [MCP in Cascade](https://docs.devin.ai/desktop/cascade/mcp), [Devin CLI MCP configuration](https://docs.devin.ai/cli/extensibility/mcp/configuration).
</details>

<a name="cline"></a>
<details>
<summary><b>Cline</b> (VS Code, JetBrains, CLI)</summary>

Click the **MCP Servers** icon in Cline's top toolbar → **Configure** tab → **Configure MCP Servers**. That opens `cline_mcp_settings.json` (`~/.cline/data/settings/`); add:

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

Hosted, read-only alternative: **Remote Servers** tab → name *marktplaats*, URL `https://marktplaats-mcp.jaspnerd.dev/mcp`, transport **Streamable HTTP** → **Add Server**.

- **Check:** the server appears in the MCP panel with its tools listed; use the restart button there if it shows an error.
- **Use:** ask; approve each call, or add safe tools such as `search_listings` to `autoApprove`.
- Docs: [MCP overview](https://docs.cline.bot/mcp/mcp-overview).
</details>

<a name="roo-code"></a>
<details>
<summary><b>Roo Code</b></summary>

Click the **MCP** icon in the Roo Code pane → **Edit Global MCP** (or **Edit Project MCP** for `.roo/mcp.json`):

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

Hosted, read-only alternative: `"marktplaats": {"type": "streamable-http", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}` (the `type` is required for URLs). On Windows wrap local commands: `"command": "cmd", "args": ["/c", "uvx", "marktplaats-mcp"]`.

The server and its tools show up in the same MCP view; restart VS Code if they do not. Docs: [Using MCP in Roo Code](https://docs.roocode.com/features/mcp/using-mcp-in-roo).
</details>

<a name="jetbrains-ides-ai-assistant-and-junie"></a>
<details>
<summary><b>JetBrains IDEs</b> (AI Assistant and Junie)</summary>

**AI Assistant:** **Settings → Tools → AI Assistant → Model Context Protocol (MCP) → Add**, choose **STDIO** and paste:

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

Click **Apply**; the **Status** column turns to connected and the tools become available in the AI chat (the AI picks them, or type `/` to call one). For the hosted endpoint choose **HTTP** and paste `{"mcpServers": {"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}}}`. If the status stays red, replace `uvx` with its absolute path.

**Junie** has its own list: **Settings → Tools → Junie → MCP Settings → Add**, same JSON, stored in `~/.junie/mcp/mcp.json` (or `.junie/mcp/mcp.json` per project). The Junie CLI reads the same file.

Docs: [Configure an MCP server](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html), [Junie MCP settings](https://junie.jetbrains.com/docs/junie-plugin-mcp-settings.html).
</details>

<a name="zed"></a>
<details>
<summary><b>Zed</b></summary>

**Settings → AI → MCP Servers → Add Server → Add Local Server**, or put this in `settings.json`:

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

Hosted, read-only alternative: `"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`.

The dot next to the server in **Settings → AI → MCP Servers** turns green ("Server is active"). Tools are available in the Agent Panel and ask for confirmation by default. Docs: [MCP in Zed](https://zed.dev/docs/ai/mcp).
</details>

<a name="opencode"></a>
<details>
<summary><b>opencode</b></summary>

Add to `~/.config/opencode/opencode.json` (everywhere) or `opencode.json` in a project:

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

Hosted, read-only alternative: `"marktplaats": {"type": "remote", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp", "enabled": true}`.

Check with `opencode mcp list` (`opencode mcp debug marktplaats` if something is off), then just ask. Docs: [MCP servers in opencode](https://opencode.ai/docs/mcp-servers/).
</details>

<a name="goose"></a>
<details>
<summary><b>Goose</b> (CLI and desktop)</summary>

Run `goose configure` → **Add Extension** → **Command-line Extension**, name it *marktplaats*, command `uvx marktplaats-mcp`, accept the defaults. Or add to `~/.config/goose/config.yaml`:

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

Hosted, read-only alternative: `type: streamable_http` with `uri: https://marktplaats-mcp.jaspnerd.dev/mcp`. For the desktop app, open this link: `goose://extension?cmd=uvx&arg=marktplaats-mcp&id=marktplaats&name=Marktplaats&description=Search%20Marktplaats%20and%202dehands`.

Check with `goose info -v` (lists enabled extensions) or the **Extensions** sidebar in the desktop app. Docs: [Using extensions](https://goose-docs.ai/docs/getting-started/using-extensions/).
</details>

<a name="lm-studio"></a>
<details>
<summary><b>LM Studio</b> (local models)</summary>

[![Add MCP Server marktplaats to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D)

Or open the **Program** tab in the right sidebar → **Install → Edit mcp.json** (`~/.lmstudio/mcp.json`, Windows `%USERPROFILE%\.lmstudio\mcp.json`) and paste the same JSON as for Cursor:

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

Hosted, read-only alternative: `"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`. Pick a model that supports tool calling; LM Studio asks for confirmation on each tool call and you can "always allow" it. `uvx` must be on your PATH, so restart LM Studio after installing uv. Docs: [MCP in LM Studio](https://lmstudio.ai/docs/app/mcp).
</details>

<a name="perplexity"></a>
<details>
<summary><b>Perplexity</b> (web and desktop apps)</summary>

**Hosted:** **Account settings → Connectors → + Custom connector → Remote**. Name *Marktplaats*, URL `https://marktplaats-mcp.jaspnerd.dev/mcp`, authentication **None**, transport **Streamable HTTP**, tick the acknowledgement, **Add**, then click the connector card to enable it. Read-only tools.

**Local (macOS app from the Mac App Store):** same page, install the *PerplexityXPC* helper when asked, **Add Connector → Simple**, server name *Marktplaats*, command `uvx marktplaats-mcp`, **Save**. Wait for the status to say *Running*, then toggle it on under **Sources** in a chat. Tool calls ask for confirmation.

Docs: [Custom remote connectors](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors), [Local and remote MCPs](https://www.perplexity.ai/help-center/en/articles/11502712-local-and-remote-mcps-for-perplexity).
</details>

<a name="github-copilot-cli"></a>
<details>
<summary><b>GitHub Copilot CLI</b></summary>

```bash
copilot mcp add marktplaats -- uvx marktplaats-mcp
```

Hosted, read-only alternative: `copilot mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`. Inside a session, `/mcp add` opens the same form and the server is available immediately. The config lives in `~/.copilot/mcp-config.json`; a repo can ship `.github/mcp.json` with the VS Code-style `{"mcpServers": {"marktplaats": {"type": "stdio", "command": "uvx", "args": ["marktplaats-mcp"], "tools": ["*"]}}}`.

Check with `/mcp show marktplaats` or `copilot mcp list`. Docs: [Add MCP servers to Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers).
</details>

<a name="more-clients"></a>
<details>
<summary><b>More clients</b> (Kiro, Warp, Continue, Trae, Amp, Droid, Qwen Code, Kimi, Raycast, Open WebUI, LibreChat, Jan, ChatWise, Msty, Cherry Studio, 5ire, n8n, Docker, Copilot Studio, Ollama)</summary>

Local means `uvx marktplaats-mcp` over stdio; hosted means the read-only URL `https://marktplaats-mcp.jaspnerd.dev/mcp`. "Claude-style JSON" is the `{"mcpServers": {"marktplaats": {"command": "uvx", "args": ["marktplaats-mcp"]}}}` block from the Claude Desktop section.

| Client | Local install | Hosted URL | Docs |
|---|---|---|---|
| **Kiro** (IDE and CLI, ex-Amazon Q) | [Add to Kiro](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D), or Claude-style JSON in `~/.kiro/settings/mcp.json`; CLI: `kiro-cli mcp add --name marktplaats --command "uvx marktplaats-mcp" --scope global`. The MCP servers tab in the Kiro panel shows it connected | [Add to Kiro](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22url%22%3A%22https%3A%2F%2Fmarktplaats-mcp.jaspnerd.dev%2Fmcp%22%7D) | [MCP configuration](https://kiro.dev/docs/mcp/configuration/) |
| **Warp** | **Settings → Agents → MCP servers → + Add**, paste Claude-style JSON (or write it to `~/.warp/.mcp.json`). Warp also picks up servers from Claude Code and Codex configs when *Auto-spawn servers from third-party agents* is on | Same dialog with `{"mcpServers": {"marktplaats": {"url": "…/mcp"}}}` | [MCP in Warp](https://docs.warp.dev/agent-platform/capabilities/mcp/) |
| **Continue** | In `~/.continue/config.yaml` under `mcpServers:` add `- name: marktplaats`, `type: stdio`, `command: uvx`, `args: ["marktplaats-mcp"]`; or drop Claude-style JSON in `.continue/mcpServers/`. Tools appear in Agent mode only | `type: streamable-http`, `url: …/mcp` | [MCP deep dive](https://docs.continue.dev/customize/deep-dives/mcp) |
| **Trae** | Settings → **MCP → Add → Add Manually**, paste Claude-style JSON (or `.trae/mcp.json` per project). The built-in Agent gets all servers | `{"mcpServers": {"marktplaats": {"url": "…/mcp"}}}` | [Add MCP servers](https://docs.trae.ai/ide/add-mcp-servers) |
| **Amp** | `amp mcp add marktplaats -- uvx marktplaats-mcp`; check with `amp mcp doctor` | `amp mcp add marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` | [MCP in Amp](https://ampcode.com/docs/customize/mcp) |
| **Factory Droid** | `droid mcp add marktplaats "uvx marktplaats-mcp"`; check with `droid mcp list` or `/mcp` | `droid mcp add marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp --type http` | [MCP in Droid](https://docs.factory.ai/cli/configuration/mcp) |
| **Qwen Code** | `qwen mcp add --transport stdio marktplaats uvx marktplaats-mcp`; check with `/mcp` | `qwen mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` (config key is `httpUrl`) | [MCP in Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/) |
| **Kimi CLI** | `kimi mcp add --transport stdio marktplaats -- uvx marktplaats-mcp`; check with `kimi mcp test marktplaats` | `kimi mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` | [MCP in Kimi CLI](https://moonshotai.github.io/kimi-cli/en/customization/mcp.html) |
| **Raycast AI** (Pro) | Run the **Install MCP Server** command, transport **Standard Input/Output**, command `uvx`, arguments `marktplaats-mcp`; then type `@marktplaats` in AI Chat | Same command, transport **HTTP**, paste the URL (the only option on iOS) | [MCP in Raycast](https://manual.raycast.com/ai/model-context-protocol) |
| **Open WebUI** | Native MCP is HTTP only. For local, bridge it: `uvx mcpo --port 8000 -- uvx marktplaats-mcp`, then add `http://localhost:8000` as an OpenAPI tool server | Admin → **Settings → Integrations → External Tool Servers → Add**, type **MCP (Streamable HTTP)**, auth **None** | [MCP in Open WebUI](https://docs.openwebui.com/features/extensibility/mcp/) |
| **LibreChat** | In `librechat.yaml` under `mcpServers:` add `marktplaats:` with `type: stdio`, `command: uvx`, `args: ["marktplaats-mcp"]`, then restart | `type: streamable-http`, `url: …/mcp` | [MCP servers](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers) |
| **Jan** | **Settings → MCP Servers → + Add MCP Server**, transport **STDIO**, command `uvx`, args `marktplaats-mcp`; pick a model with the *tools* capability | Same dialog, transport **HTTP** | [MCP servers in Jan](https://www.jan.ai/docs/desktop/integrations/mcp-servers) |
| **ChatWise** | **Settings → Tools → +**, type **Command Line (stdio)**, command `uvx marktplaats-mcp`; or paste `{"mcpServers": {"marktplaats": {"command": "uvx marktplaats-mcp"}}}` via *Import JSON from Clipboard* | Type **Streamable HTTP** | [Tools](https://docs.chatwise.app/tools) |
| **Msty Studio** | **Toolbox → Add New Tool → STDIO / JSON**, paste `{"command": "uvx", "args": ["marktplaats-mcp"]}` | **Add New Tool → HTTP**, paste the URL | [Tools](https://docs.msty.ai/studio/toolbox/tools) |
| **Cherry Studio** | **Settings → MCP → Add**, type stdio, command `uvx`, args `marktplaats-mcp` (or import Claude-style JSON), then enable it on an agent | Same dialog, Streamable HTTP | [MCP](https://docs.cherryai.com.cn/advanced-basic/extensions/mcp.md) |
| **5ire** | Tools → add with `{"name": "marktplaats", "command": "uvx", "args": ["marktplaats-mcp"]}` | `{"name": "marktplaats", "url": "…/mcp"}` | [5ire docs](https://5ire.app/docs) |
| **n8n** | Not supported (remote only) | Add an **MCP Client Tool** node to an AI Agent, transport **HTTP Streamable**, endpoint `…/mcp`, authentication **None** | [MCP Client Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/) |
| **Docker MCP Toolkit** | Build the image from this repo's `Dockerfile` and add it to a profile with `docker mcp profile server add <profile> --server file://marktplaats.yaml` | `docker mcp profile server add <profile> --server https://registry.modelcontextprotocol.io/v0/servers/io.github.jasp-nerd/marktplaats-mcp` | [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/) |
| **Microsoft Copilot Studio** | Not supported (remote only) | Agent → **Tools → Add a tool → New tool → Model Context Protocol**, server URL `…/mcp`, authentication **None**. Consumer Copilot has no custom connectors | [Add an MCP server](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent) |
| **Ollama** | No MCP support in the app or CLI. Use `ollama launch claude` / `codex` / `opencode` with a local model and add the server in that client | Same | [ollama launch](https://docs.ollama.com/cli) |
</details>
