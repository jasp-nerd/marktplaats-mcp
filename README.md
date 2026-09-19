<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp: search Marktplaats and 2dehands from any AI agent" width="760">
</p>

<p align="center">
  <b>English</b> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.nl.md">Nederlands</a> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.fr.md">Français</a>
</p>

# marktplaats-mcp: the Marktplaats & 2dehands MCP server

**marktplaats-mcp** is an MCP server for **Marktplaats.nl** (Netherlands) and **2dehands.be** (Belgium), the Dutch and Belgian second-hand classifieds (*tweedehands*, *petites annonces d'occasion*). It lets Claude, ChatGPT, Cursor, Codex, Gemini, VS Code Copilot, Cline, opencode and any other MCP client search listings, filter on category-specific attributes, vet sellers, compare prices, monitor new ads, and, with your own login, read and send messages, place bids and manage favorites and your own ads. No API key. Runs locally over stdio, or as a hosted endpoint you paste into claude.ai in one step.

<p align="center">
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/v/marktplaats-mcp.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg" alt="Python versions"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml/badge.svg" alt="Live API canary"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/dm/marktplaats-mcp.svg" alt="Downloads"></a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=marktplaats"><img src="https://img.shields.io/badge/MCP%20registry-listed-blue" alt="MCP registry"></a>
</p>

## 🌐 Use on claude.ai (no install)

A hosted copy of this server runs at `https://marktplaats-mcp.jaspnerd.dev/mcp`, ready for [claude.ai](https://claude.ai) in your browser or the Claude mobile app. Custom connectors work on every Claude plan, including Free.

1. Open [claude.ai](https://claude.ai) → **Settings → Connectors → Add custom connector**.
2. Paste `https://marktplaats-mcp.jaspnerd.dev/mcp` as the URL and click **Add**. No account or key needed.
3. Ask Claude: *"Search Marktplaats for an OLED TV under €400 near 3011 AB and check the seller."*

The hosted endpoint runs the same code as the PyPI package, is rate-limited per client and only offers the read-only tools. For your own account, install it locally below.

## 🚀 Quickstart (local)

The only prerequisite is [uv](https://docs.astral.sh/uv/) (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code**, one command:

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Then ask: *"Find a racefiets under €500 within 25 km of 1011 AB, frame 57-61 cm, and tell me if the sellers look legit."*

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/trailer-crt.gif" alt="marktplaats-mcp trailer: an AI agent searches for a racefiets and vets the seller, rendered as a retro CRT terminal session" width="800">
</p>

## 👤 Use your own account (messages, favorites, bids, your ads)

Marktplaats has no public API and its login uses SMS two-factor authentication and reCAPTCHA, so this server never asks for your password. Instead it borrows the session from a browser you are already logged into, the way `yt-dlp --cookies-from-browser` does:

```bash
uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login
```

That looks for a Marktplaats / 2dehands session in Chrome, Firefox, Safari, Edge, Brave, Arc and friends (macOS asks once for keychain access; click Allow), verifies it against the site, and stores it in `~/.config/marktplaats-mcp/session.json`, readable by your user only. Restart your MCP client and the account tools appear. Useful commands:

```bash
marktplaats-mcp login --read-only     # never send, bid or change favorites
marktplaats-mcp login --paste         # paste a Cookie header from DevTools instead
marktplaats-mcp status                # is the stored session still valid?
marktplaats-mcp logout                # delete it
```

Or set `MARKTPLAATS_COOKIE` / `TWEEDEHANDS_COOKIE` (the request `Cookie` header) in your client's config. Sessions last weeks; when one expires the tools tell you to log in again.

**What can go wrong, and what cannot.** Sending a message, contacting a seller and placing a bid return a preview first and only act when called again with `confirm=true`, so your agent shows you what it is about to do. A bid is binding on Marktplaats; the tool refuses bids below the listing's minimum and is marked destructive so clients ask before running it. Every confirmed write is appended to `~/.local/state/marktplaats-mcp/writes.jsonl`. Your session is only ever sent to marktplaats.nl or 2dehands.be, and the hosted endpoint never registers account tools. Automated ad placement is forbidden by Marktplaats' terms and is deliberately not implemented.

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
<summary><b>Cline</b></summary>

MCP Servers → Configure → add to `cline_mcp_settings.json`:

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

<details>
<summary><b>Any client that supports remote servers (ChatGPT, Gemini, others)</b></summary>

Use the Streamable HTTP URL `https://marktplaats-mcp.jaspnerd.dev/mcp`, no authentication. Read-only tools only.
</details>

## 🧰 Tools

| Tool | What it does | Account | Writes |
|---|---|:---:|:---:|
| `search_listings` | Search with query, category, subcategory, **category-specific attributes**, price range, condition, delivery (pickup/shipping), distance from a postcode, recency, negative keywords, sorting and pagination | | |
| `get_listing_details` | Full ad: description, attributes, status (active/closed), exact listing time, view and favorite counts, bidding state and minimum bid, shipping, images, seller response rate and account age. Accepts pasted URLs | | |
| `get_seller_profile` | Trust signals: verified bank account, identity, phone, business verification, payment method, review score and count, lowest bid the seller accepts | | |
| `list_seller_listings` | Everything one seller has on offer: spot dealers posing as private sellers and duplicate ads | | |
| `list_categories` | The category tree (names and ids) used for filtering, also available as an MCP resource | | |
| `list_category_filters` | Discover the filters for a category (brand, frame height, mileage, fuel, RAM, ...) with their valid values and counts | | |
| `check_new_listings` | Newest-first monitoring with a stateless cursor: returns only ads placed after `since`, never skips one | | |
| `analyze_prices` | Median, quartiles, min, max and mean asking prices for a search, plus the cheapest matches | | |
| `get_my_account` | Session check, unread messages and notifications | ✅ | |
| `list_conversations`, `get_conversation` | Your inbox and full message threads | ✅ | |
| `list_my_listings`, `list_favorites`, `list_my_bids`, `list_saved_searches` | Your ads (views, favorites, highest bid, expiry), favorites, bids and saved searches | ✅ | |
| `send_message`, `contact_seller` | Reply in a thread, or ask a seller a question or make a non-binding offer. Preview first, `confirm=true` to send | ✅ | ✅ |
| `place_bid` | Bid on a listing. Preview first, refuses bids below the minimum, marked destructive | ✅ | ✅ |
| `set_favorite`, `extend_my_listing` | Save/unsave a listing; renew one of your expiring ads | ✅ | ✅ |

Read-only tools carry the matching MCP annotations, so clients skip confirmation prompts for them and ask for the write tools. Every tool returns structured output with a real schema. Two prompts, `bargain_hunt` and `vet_listing`, encode the common workflows.

### What you can say, and what happens

| You say | The agent calls |
|---|---|
| *"Is €450 a fair price for an iPhone 15 128 GB in good condition?"* | `analyze_prices` → median, quartiles and the three cheapest ads |
| *"Find a used Golf, 2018-2022, under 100,000 km, petrol, from a private seller"* | `list_category_filters("Auto's")` → `search_listings(attributes={"Bouwjaar": "2018-2022", "Kilometerstand": "-100000", "Brandstof": "Benzine", "Adverteerder": "Particulier"})` |
| *"Is this seller trustworthy? What else are they selling?"* | `get_listing_details` → `get_seller_profile` → `list_seller_listings` |
| *"Tell me when new bakfiets ads appear near Antwerp"* | `check_new_listings(site="2dehands", postcode="2000", distance_km=25)` with the returned cursor on every poll |
| *"Ask the seller whether it's still available and offer €120"* | `contact_seller(..., offer_euros=120)` preview → you confirm → sent |
| *"Reply to Piet that I can pick it up Saturday"* | `list_conversations` → `send_message` preview → you confirm → sent |

## 🔒 Safety model

- **No credentials by default.** Searching, details, seller checks, filters, price statistics and monitoring need no account.
- **Your session stays yours.** The local server reads the cookie from your browser or a file only you can read, sends it only to marktplaats.nl / 2dehands.be, and never logs it. The hosted endpoint refuses to start with account credentials configured.
- **Writes are explicit.** Sending and bidding preview first and require `confirm=true`; bids below the minimum are refused; `login --read-only` or `MARKTPLAATS_READ_ONLY=1` disables writes entirely; every confirmed write is logged locally.
- **Untrusted content is labelled.** Listing text and messages are written by other users; the server tells the model to treat them as data, never as instructions.
- **Polite to the marketplace.** Requests are spaced (`MARKTPLAATS_MIN_INTERVAL_MS`, default 200), retried with backoff and `Retry-After`, and search pages are cached for a minute. The hosted endpoint is rate-limited per client and globally.
- **No affiliate links, no tracking.** Listing URLs are returned exactly as the marketplaces publish them.

## ⚖️ How this compares

| | **marktplaats-mcp** (this) | [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp) | [gjoris/marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) |
|---|:---:|:---:|:---:|
| Marktplaats.nl | ✅ | ✅ | ✅ |
| 2dehands.be (Belgium), with language filter | ✅ | ❌ | ✅ |
| Subcategory filter that actually applies | ✅ | ❌ | ❌ |
| Category attribute filters (brand, mileage, RAM, ...) by label | ✅ | ids only | ids only |
| Price statistics, seller listings, spelling suggestions | ✅ | ❌ | ❌ |
| Listing details with status, exact time, bids, seller response rate | ✅ | partial | partial |
| Account: messages, favorites, bids, own ads | read + write | ❌ | read-only |
| Login without password (browser session import) | ✅ | n/a | Playwright login |
| New-listing monitoring | ✅ | ❌ | saved searches on disk |
| Paid promotions filtered by default | ✅ | ❌ | ❌ |
| Install | `uvx marktplaats-mcp` (PyPI) | `uvx git+https://…` (broken on current `mcp`) | from source |
| Hosted endpoint, no install | ✅ | ❌ | ❌ |
| Official MCP registry | ✅ | ❌ | ❌ |
| Daily live-API canary | ✅ | ❌ | ✅ |
| Last release | current | Feb 2026 | May 2026 |

Credit where it is due: PonClick's server came first and its listing formatting informed this one, and gjoris pioneered the embedded-page parsing and the live canary. See [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

## ❓ FAQ

### Is there an MCP server for Marktplaats?
Yes, this one. Free, open source (MIT), no API key. Paste the hosted URL into claude.ai or run `uvx marktplaats-mcp`.

### Does it work with 2dehands.be and Belgium?
Yes. Every tool takes `site="2dehands"`, and `language="nl"` or `"fr"` narrows Belgian results to one language.

### Do I need a Marktplaats account or API key?
No. Only the account tools need your own login, and they use your existing browser session rather than a password.

### Can AI read and send my Marktplaats messages, or place bids?
Yes, with the local server after `marktplaats-mcp login`. Sending and bidding show a preview and only act after you confirm.

### Where are my login credentials stored?
In `~/.config/marktplaats-mcp/session.json` on your machine, readable by your user only, or in the environment variables you set yourself. They are only ever sent to marktplaats.nl / 2dehands.be. `marktplaats-mcp logout` removes them.

### Can I use it without installing anything?
Yes: the hosted endpoint `https://marktplaats-mcp.jaspnerd.dev/mcp` works in claude.ai, including the Free plan and mobile apps. It offers the read-only tools.

### Does it work with ChatGPT, Cursor, Gemini, VS Code and Cline?
Yes. Any client that runs stdio servers can use `uvx marktplaats-mcp`; clients that support remote servers can use the hosted URL.

### Is this official or affiliated with Marktplaats?
No. It is an independent open source project with no ties to Marktplaats, 2dehands or Adevinta. It uses the same public JSON endpoints the websites use; that API is undocumented and may change, which is why a live canary runs every day.

### Why do I sometimes see fewer results than the limit, or `total_count` looks high?
Paid promotions (DAGTOPPER, TOPADVERTENTIE) are filtered out by default; pass `include_sponsored=true` to see them. `total_count` is the marketplace's raw count before that filtering.

### Which Python versions are supported?
3.10 and up. CI tests 3.11 through 3.13 on Linux, macOS and Windows.

## ⚙️ Configuration

| Variable | Purpose |
|---|---|
| `MARKTPLAATS_COOKIE`, `TWEEDEHANDS_COOKIE` | Session `Cookie` header per site (alternative to `marktplaats-mcp login`); `*_FILE` variants read it from a file |
| `MARKTPLAATS_SESSION_FILE` | Where `login` stores sessions (default `~/.config/marktplaats-mcp/session.json`) |
| `MARKTPLAATS_READ_ONLY` | `1` disables all write tools |
| `MARKTPLAATS_AUDIT_LOG` | Path of the write audit log, or `off` |
| `MARKTPLAATS_MIN_INTERVAL_MS` | Minimum spacing between upstream requests (default 200) |
| `MCP_TRANSPORT`, `MCP_HOST`, `MCP_PORT` | `http` serves Streamable HTTP for hosting (default stdio) |
| `MCP_RPS`, `MCP_GLOBAL_RPS`, `MCP_ALLOWED_HOSTS`, `MCP_ALLOWED_ORIGINS` | Hosted-mode rate limits and Host/Origin validation |

## 🗺️ Roadmap

- FastMCP 4 / MCP 2026-07-28 protocol support
- Cross-site search (NL and BE in one call)
- Saved-search creation from the agent
- Claude Desktop extension bundle (MCPB)

## 🤝 Contributing

PRs welcome. See [CONTRIBUTING.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/.github/CONTRIBUTING.md) for the dev setup: `uv sync --all-groups`, then `uv run pytest`. `uv run python scripts/e2e_smoke.py` runs the live canary.

This project reuses proven ideas from [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) and [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp). Details in [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

If this saved you a trip to Marktplaats, a star helps other people find it.

## 📄 License

[MIT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE) © 2026 jasp-nerd

---

<sub>mcp-name: io.github.jasp-nerd/marktplaats-mcp</sub>
