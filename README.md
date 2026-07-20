<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp: search Marktplaats and 2dehands from any AI agent" width="760">
</p>

<p align="center">
  <b>English</b> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.nl.md">Nederlands</a> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.fr.md">Français</a>
</p>

# marktplaats-mcp

**marktplaats-mcp** is an MCP server that lets Claude, Cursor, Codex, opencode and every other MCP client search Marktplaats and 2dehands, the Dutch and Belgian second-hand classifieds. Find bargains, vet sellers, browse categories and monitor new listings in plain language.

<p align="center">
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/v/marktplaats-mcp.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg" alt="Python versions"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/dm/marktplaats-mcp.svg" alt="Downloads"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
</p>

## ✨ Features

- 🔍 **Powerful search**: free text, categories, price range, condition, distance from a postal code, recency, sorting
- 🇳🇱🇧🇪 **Two marketplaces, one server**: marktplaats.nl (Netherlands) and 2dehands.be (Belgium) via a `site` parameter
- 📄 **Full listing details**: complete description, all photos, view and favorite counts, listing age
- 🛡️ **Seller vetting**: verified bank account, identity and phone, review score
- 🔔 **New-listing monitoring**: poll for ads placed after a timestamp with a stateless cursor
- 🧠 **Built for LLMs**: compact token-efficient output, paid promotions filtered out, structured results, pagination hints
- 🔁 **Resilient**: retries with exponential backoff, jitter and `Retry-After` handling
- 🔓 **No account, no API key**

## 🚀 Quickstart

The only prerequisite is [uv](https://docs.astral.sh/uv/) (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code**, one command:

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Then ask: *"Search Marktplaats for an OLED TV under €400 near 3011 AB."*

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/trailer-crt.gif" alt="marktplaats-mcp trailer: an AI agent searches for a racefiets and vets the seller, rendered as a retro CRT terminal session" width="800">
</p>

## 📦 Install in your favorite client

Every config runs the same stdio server via `uvx marktplaats-mcp`.

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
| `get_listing_details` | Full ad: complete description, all images, view and favorite counts, listing age |
| `get_seller_profile` | Trust signals: verified bank, identity and phone, review score and count |
| `list_categories` | Browse the category tree (names + ids) used for filtering |
| `check_new_listings` | Newest-first monitoring with a stateless cursor: returns only ads placed after `since` |

All five tools are read-only and carry the matching MCP annotations, so clients skip the confirmation prompts.

### Example prompts

- *"Find a second-hand iPhone 15 under €600 in as-good-as-new condition, sorted by price."*
- *"Search 2dehands for a bakfiets within 20 km of postcode 2000 Antwerpen."*
- *"Is seller 12345 trustworthy? Check their profile."*
- *"Check for new 'vintage lamp' listings since my last check and summarize the interesting ones."*

## ❓ FAQ

**Does this need a Marktplaats account or API key?**
No. It uses the same public JSON endpoints the website itself uses.

**Is this an official Marktplaats product?**
No. This is an independent open source project with no ties to Marktplaats or Adevinta. The underlying API is undocumented and may change. The server backs off politely on rate limits; keep your own usage reasonable.

**Why do I sometimes see fewer results than the limit?**
Paid promotions (DAGTOPPER/TOPADVERTENTIE) are filtered out by default. Pass `include_sponsored=true` if you want them.

**Which Python versions are supported?**
3.10 and up. CI tests 3.11 through 3.13 on Linux, macOS and Windows.

## 🗺️ Roadmap

- Persistent saved searches with price-drop detection
- Notifications (Discord/Telegram/ntfy via Apprise)
- Authenticated tools (your messages, favorites and bids)
- Docker image + Docker MCP Catalog

## 🤝 Contributing

PRs welcome. See [CONTRIBUTING.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/.github/CONTRIBUTING.md) for the dev setup: `uv sync --all-groups`, then `uv run pytest`.

This project reuses proven ideas from [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) and [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp). Details in [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

## 📄 License

[MIT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE) © 2026 jasp-nerd

---

<sub>mcp-name: io.github.jasp-nerd/marktplaats-mcp</sub>
