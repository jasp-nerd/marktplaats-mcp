<p align="center">
  <img src="assets/banner.svg" alt="marktplaats-mcp — search Marktplaats & 2dehands from any AI agent" width="760">
</p>

**English** | [Nederlands](README.nl.md) | [Français](README.fr.md)

# marktplaats-mcp

**The MCP server for Marktplaats & 2dehands** — search Dutch and Belgian second-hand classifieds straight from Claude, Cursor, Codex, opencode or any other MCP-compatible AI agent. Find bargains, vet sellers, browse categories and monitor new listings, all through natural language.

[![PyPI version](https://img.shields.io/pypi/v/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml)
[![Downloads](https://static.pepy.tech/badge/marktplaats-mcp/month)](https://pepy.tech/project/marktplaats-mcp)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> *"Find me a used racefiets under €500 within 25 km of Amsterdam, from verified sellers only."* — that's now a single prompt.

## ✨ Features

- 🔍 **Powerful search** — free text, categories, price range, condition, distance from a postal code, recency, sorting
- 🇳🇱🇧🇪 **Two marketplaces, one server** — marktplaats.nl (Netherlands) and 2dehands.be (Belgium) via a simple `site` parameter
- 📄 **Full listing details** — complete description, all photos, view/favorite counts and listing age
- 🛡️ **Seller vetting** — verified bank account / identity / phone, review score
- 🔔 **New-listing monitoring** — poll for ads placed after a timestamp with a stateless cursor; perfect for agent automations
- 🧠 **Built for LLMs** — token-efficient compact output by default, paid promotions filtered out, structured results, honest pagination hints
- 🔁 **Resilient** — automatic retries with exponential backoff, jitter and `Retry-After` handling
- 🔓 **No account, no API key** — works out of the box

## 🚀 Quickstart

The only prerequisite is [uv](https://docs.astral.sh/uv/) (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code** — one command:

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Then just ask: *"Search Marktplaats for an OLED TV under €400 near 3011 AB."*

## 📦 Install in your favorite client

All configs run the same stdio server via `uvx marktplaats-mcp`.

<details>
<summary><b>Claude Desktop</b></summary>

Add to `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`), then fully restart Claude Desktop:

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

If Claude Desktop can't find `uvx`, use the absolute path (`which uvx`, e.g. `/Users/you/.local/bin/uvx`).
</details>

<details>
<summary><b>OpenAI Codex CLI</b></summary>

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.marktplaats]
command = "uvx"
args = ["marktplaats-mcp"]
```

Or: `codex mcp add marktplaats -- uvx marktplaats-mcp`
</details>

<details>
<summary><b>opencode</b></summary>

Add to `opencode.json`:

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

Add to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

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

Add to `.vscode/mcp.json` (note the `servers` key and explicit `type`):

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
<summary><b>Windsurf</b></summary>

Add to `~/.codeium/windsurf/mcp_config.json`:

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

Add to `~/.gemini/settings.json`:

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
<summary><b>JetBrains IDEs (AI Assistant / Junie)</b></summary>

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

## 🧰 Tools

| Tool | What it does |
|---|---|
| `search_listings` | Search with query, category, price range, condition, distance, recency, sorting and pagination |
| `get_listing_details` | Full ad: complete description, all images, view/favorite counts, listing age |
| `get_seller_profile` | Trust signals: verified bank/identity/phone, review score and count |
| `list_categories` | Browse the category tree (names + ids) used for filtering |
| `check_new_listings` | Newest-first monitoring with a stateless cursor — only ads placed after `since` |

All tools are read-only and annotated as such, so agents don't nag you with confirmation prompts.

### Example prompts

- *"Find a second-hand iPhone 15 under €600 in as-good-as-new condition, sorted by price."*
- *"Search 2dehands for a bakfiets within 20 km of postcode 2000 Antwerpen."*
- *"Is seller 12345 trustworthy? Check their profile."*
- *"Check for new 'vintage lamp' listings since my last check and summarize the interesting ones."*

## ❓ FAQ

**Does this need a Marktplaats account or API key?**
No. It uses the same public JSON endpoints the website itself uses. No login, no key.

**Is this an official Marktplaats product?**
No — this is an independent open-source project, not affiliated with Marktplaats/Adevinta. The underlying API is undocumented and may change. Be a good citizen: the server retries politely and doesn't hammer the API.

**Why do I sometimes see fewer results than the limit?**
Paid promotions (DAGTOPPER/TOPADVERTENTIE) are filtered out by default so agents see organic results. Pass `include_sponsored=true` if you want them.

**Which Python versions are supported?**
3.10+. The server is tested on 3.11–3.13 on Linux, macOS and Windows.

## 🗺️ Roadmap

- Persistent saved searches with price-drop detection
- Notifications (Discord/Telegram/ntfy via Apprise)
- Authenticated tools (your messages, favorites and bids)
- Docker image + Docker MCP Catalog

## 🤝 Contributing

PRs welcome! See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for dev setup (spoiler: `uv sync --all-groups`, `uv run pytest`).

Built on the shoulders of [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) and [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp) — see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## 📄 License

[MIT](LICENSE) © 2026 jasp-nerd

---

<sub>mcp-name: io.github.jasp-nerd/marktplaats-mcp</sub>
