# Third-party notices

This project combines ideas and data from the following MIT-licensed projects.
Thank you to their authors!

## marktplaats-py (jensjeflensje)

- https://github.com/jensjeflensje/marktplaats-py — MIT License
- `src/marktplaats_mcp/data/l1_categories.json` and `l2_categories.json` are
  vendored snapshots of its scraped category data (refreshed by our
  `update-categories` workflow using the same scraping approach).
- The condition codes, sort enums and price-type mapping follow its research.

## marktplaats-monitor (jasp-nerd)

- https://github.com/jasp-nerd/marktplaats-monitor — MIT License
- The retry/backoff/jitter + Retry-After resilience model, the paid-promotion
  filter (`priorityProduct` in DAGTOPPER/TOPADVERTENTIE) and its
  `docs/marktplaats-api.md` API reference informed `client.py` and `parsing.py`.

## marktplaats-2dehands-mcp (gjoris)

- https://github.com/gjoris/marktplaats-2dehands-mcp — MIT License
- The multi-site (marktplaats.nl / 2dehands.be) host resolution and the
  `window.__CONFIG__` listing-detail extraction pattern informed `sites.py`
  and `detail.py`.

## marktplaats-mcp (PonClick)

- https://github.com/PonClick/marktplaats-mcp — MIT License
- The token-efficient compact output mode was inspired by this project.
