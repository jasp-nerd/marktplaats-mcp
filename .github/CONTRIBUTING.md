# Contributing to marktplaats-mcp

Thanks for wanting to help! This project aims to stay small, well-tested and
easy to hack on.

## Dev setup

```bash
git clone https://github.com/jasp-nerd/marktplaats-mcp
cd marktplaats-mcp
uv sync --all-groups        # installs runtime + dev dependencies
uv run pre-commit install   # ruff + gitleaks on every commit
```

Requires [uv](https://docs.astral.sh/uv/) and Python 3.10+.

## Running the server locally

```bash
uv run marktplaats-mcp                       # stdio server
claude mcp add mp-dev -- uv run marktplaats-mcp   # try it from Claude Code
```

## Tests, lint, types

```bash
uv run pytest              # full suite (no network needed — recorded fixtures)
uv run pytest --cov        # with coverage
uv run ruff check .        # lint
uv run ruff format .       # format
uv run mypy                # strict type checking
```

All four must be green before a PR can merge (CI enforces this).

### Writing meaningful tests

- Tool behavior is tested through FastMCP's **in-memory client** (`Client(mcp)`),
  so the real MCP round-trip is exercised.
- HTTP is mocked with **respx**; parsers are tested against **recorded real API
  responses** in `tests/fixtures/`. If Marktplaats changes its payload, refresh
  a fixture rather than hand-editing it.
- Cover error paths (429/500, malformed JSON, empty results), not just happy paths.

## Project layout

| Module | Responsibility |
|---|---|
| `client.py` | HTTP + retries + query building for the undocumented API |
| `sites.py` | marktplaats.nl / 2dehands.be host resolution |
| `parsing.py` | raw listing → model, price formatting, promo filtering |
| `detail.py` | `window.__CONFIG__` extraction from listing pages |
| `categories.py` | vendored category data + lookup |
| `server.py` | FastMCP tools (thin layer over the above) |

## Pull requests

1. Fork, create a feature branch (`feat/...`, `fix/...`).
2. Keep PRs small and focused; add or update tests for behavior changes.
3. Make sure `uv run pytest && uv run ruff check . && uv run mypy` pass.
4. Describe *why* in the PR body; link an issue if one exists.

Be polite to the Marktplaats API: no scraping loops in tests, keep live calls
out of the test suite (CI has no network access to Marktplaats).

## Reporting bugs / requesting features

Use the [issue templates](https://github.com/jasp-nerd/marktplaats-mcp/issues/new/choose).
Security issues: see [SECURITY.md](SECURITY.md) — please don't open public issues for those.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
