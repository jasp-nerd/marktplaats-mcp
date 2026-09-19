<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp: search Marktplaats and 2dehands from any AI agent" width="760">
</p>

<p align="center">
  <b>English</b> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.nl.md">Nederlands</a> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.fr.md">Français</a>
</p>

# marktplaats-mcp: the Marktplaats & 2dehands MCP server

**marktplaats-mcp** is an MCP server for **Marktplaats.nl** (Netherlands) and **2dehands.be** (Belgium), the Dutch and Belgian second-hand classifieds (*tweedehands*, *petites annonces d'occasion*). Search listings, filter on category attributes, vet sellers, compare prices and watch for new ads from Claude, ChatGPT, Cursor, Codex, Gemini or any other MCP client. With your own login it also reads and sends messages, places bids and manages your favorites and ads. No API key.

<p align="center">
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/v/marktplaats-mcp.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg" alt="Python versions"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml/badge.svg" alt="Live API canary"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/dm/marktplaats-mcp.svg" alt="Downloads"></a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=marktplaats"><img src="https://img.shields.io/badge/MCP%20registry-listed-blue" alt="MCP registry"></a>
</p>

## 🚀 Get started

**No install: paste a URL.** The hosted, read-only server runs at `https://marktplaats-mcp.jaspnerd.dev/mcp`. Add it as a custom connector in [claude.ai](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.md#claudeai-web-and-mobile) (Settings → Connectors, works on the Free plan and mobile), [ChatGPT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.md#chatgpt), [Mistral Le Chat](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.md#mistral-le-chat), [Perplexity](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.md#perplexity) or the [Gemini app](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.md#gemini-app).

**Claude Code: one command.**

```bash
claude mcp add --scope user marktplaats -- uvx marktplaats-mcp
```

**Any other client.** Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (`brew install uv`, or `winget install --id=astral-sh.uv -e` on Windows), then add the standard MCP config:

```json
{ "mcpServers": { "marktplaats": { "command": "uvx", "args": ["marktplaats-mcp"] } } }
```

One click: [![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=) [![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) [![Add to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D) [![Add to Kiro](https://img.shields.io/badge/Kiro-Add-7B61FF?style=flat-square)](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D)

Step-by-step instructions for 40 clients (Cursor, VS Code, Codex, Gemini CLI, Cline, Windsurf, JetBrains, Zed, opencode, Goose, ...), with the config path per OS and a link to each client's official guide: **[docs/clients.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.md)**.

Then ask: *"Find a racefiets under €500 within 25 km of 1011 AB, frame 57-61 cm, and tell me if the sellers look legit."*

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/trailer-crt.gif" alt="marktplaats-mcp trailer: an AI agent searches for a racefiets and vets the seller, rendered as a retro CRT terminal session" width="800">
</p>

## 👤 Use your own account (messages, favorites, bids, your ads)

Marktplaats has no public API and its login uses SMS two-factor authentication, so this server never asks for your password. It copies the session from a browser you are already logged into:

```bash
uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login
```

The session is stored in `~/.config/marktplaats-mcp/session.json`, readable by your user only. Restart your MCP client and the account tools appear.

```bash
marktplaats-mcp login --site 2dehands  # also import your 2dehands.be session
marktplaats-mcp login --read-only      # never send, bid or change favorites
marktplaats-mcp login --window         # open a browser window and log in there instead
marktplaats-mcp login --paste          # paste a Cookie header from DevTools instead
marktplaats-mcp status                 # is the stored session still valid?
marktplaats-mcp logout                 # delete it
```

<details>
<summary><b>If login says it could not read your browser's cookies</b></summary>

- **macOS**: the system blocks command-line tools from reading browser data and does not ask. Once, open System Settings → Privacy & Security → **Full Disk Access**, add the terminal app you use (Terminal, iTerm, Warp, or VS Code), then quit and reopen it. Then run the login command again.
- **Windows**: Chrome and Edge lock their cookie file while they run; the tool copies it first, so this normally just works. If it doesn't, close the browser and run the login again, or use `--paste`.
- **Linux**: Chromium browsers store the cookie key in your keyring (GNOME Keyring or KWallet), which must be unlocked; Firefox needs nothing. Snap or Flatpak browsers keep their profile elsewhere, so use `--paste` there.
- Everywhere: `marktplaats-mcp login --paste` never needs permissions. In your browser on marktplaats.nl press F12 → Network, click any request, copy the `Cookie` request header and paste it.
</details>

Or set `MARKTPLAATS_COOKIE` / `TWEEDEHANDS_COOKIE` (the request `Cookie` header) in your client's config. Sessions last weeks; when one expires the tools tell you to log in again.

Sending, contacting a seller and bidding return a preview first and only act when called again with `confirm=true`. Bids are binding on Marktplaats; the tool refuses bids below the minimum. Automated ad placement is forbidden by Marktplaats' terms and deliberately not implemented. See [Safety model](#-safety-model).

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
Yes. See [docs/clients.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.md) for step-by-step instructions per client. Any client that runs stdio servers can use `uvx marktplaats-mcp`; clients that support remote servers can use the hosted URL.

### Is this official or affiliated with Marktplaats?
No. It is an independent open source project with no ties to Marktplaats, 2dehands or Adevinta. It uses the same public JSON endpoints the websites use; that API is undocumented and may change, which is why a live canary runs every day.

### Why do I sometimes see fewer results than the limit, or `total_count` looks high?
Paid promotions (DAGTOPPER, TOPADVERTENTIE) are filtered out by default; pass `include_sponsored=true` to see them. `total_count` is the marketplace's raw count before that filtering.

### Which Python versions are supported?
3.10 and up. CI tests 3.11 through 3.13 on Linux, macOS and Windows.

## 📚 Docs

- [Install in your client](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.md): step-by-step for 40 clients
- [Configuration](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/configuration.md): environment variables for the local and hosted server
- [How this compares](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/comparison.md) to the other Marktplaats MCP servers
- [Changelog](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/CHANGELOG.md)

## 🗺️ Roadmap

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
