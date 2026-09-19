# Changelog

All notable changes to marktplaats-mcp. The format follows [Keep a Changelog](https://keepachangelog.com/).

## [0.2.0] - 2026-09-19

### Added
- **Account mode** (local server only): `marktplaats-mcp login` opens a browser window where you log in as usual (no password handled by the server, two-factor included) and captures the session; `--import` copies it from a browser you are logged into, `--paste` takes a Cookie header; plus `status`, `logout` and `--read-only`. Verified against a live account. Tools: `get_my_account`, `list_conversations`, `get_conversation` (with `mark_read`), `list_my_listings`, `list_favorites`, `list_my_bids`, `list_saved_searches`, `send_message`, `contact_seller`, `set_favorite`, `place_bid`, `extend_my_listing`. Sending and bidding preview first and need `confirm=true`; bids below the minimum are refused; confirmed writes are appended to a local audit log.
- `list_category_filters`: discover category-specific filters (brand, frame height, mileage, fuel, RAM, ...) with valid values and counts, and an `attributes` parameter on `search_listings`, `check_new_listings` and `analyze_prices` that accepts those labels, including ranges like `"2018-2022"`.
- `list_seller_listings`: everything one seller has on offer.
- `analyze_prices`: median, quartiles, min, max, mean asking prices and the cheapest matches.
- New search filters: `delivery` (pickup/shipping), `language` (2dehands: Dutch or French ads), `exclude` (negative keywords).
- Listing details now come from the app's JSON listing endpoint: typed attributes, car attributes, status (active/closed), exact listing time, postcode, bidding state and minimum bid, shipping, image count, seller type, account age, response rate and review summary. `get_listing_details` accepts pasted URLs and a `max_images` parameter.
- `search_listings` skips ads without an asking price when sorting or filtering on price (`include_unpriced=true` keeps them); `analyze_prices` takes `price_from`/`price_to` and trims outliers; `list_category_filters` caps values per filter (`max_options`); listing details report `delivery` (pickup/shipping/both) from the ad itself.
- Listings carry `price_euros`, an ISO `listed` date, `reserved` and `is_business` flags; search results surface the site's spelling suggestion; seller profiles add business verification, payment method and the lowest accepted bid (with explicit nulls).
- Real output schemas on every tool, MCP resources for the category tree, prompts `bargain_hunt` and `vet_listing`, server icons and website metadata.
- Hosted mode: landing page, `llms.txt`, privacy policy, icons, `/health`; per-client and global rate limits; Host/Origin validation; non-root container with a health check.
- Daily live-API canary workflow that opens an issue when the marketplace changes.

### Fixed
- The subcategory filter never applied: the API ignores `l2CategoryId` and only honours `l2CategoryIds[]`. Every subcategory search previously returned the whole parent category.
- Small-limit searches and polls sorted by date returned nothing because the first pages are padded with paid promotions; pages are now fetched at full size and paginated on returned listings, so `offset`/`next_offset` no longer skip or repeat ads.
- `check_new_listings` no longer skips ads when the result is truncated: the cursor advances only to the oldest ad returned.
- `get_listing_details` returned no attributes and image URLs with an unresolved size placeholder.
- Condition ids differ per category (a used car is not a used bike); they are now resolved from the category's own filters.
- Actionable errors for missing listings, rate limiting and stale sessions instead of raw HTTP messages.

### Changed
- Built on FastMCP 4 / MCP SDK 2: speaks both the 2025-11-25 and the sessionless 2026-07-28 protocol eras. Requires pydantic 2.12 or newer.
- Outbound requests are spaced by `MARKTPLAATS_MIN_INTERVAL_MS` (default 200 ms) and search pages are cached for 60 s.
- `total_count` remains the marketplace's raw count; `returned`, `next_offset` and `note` describe the filtered page.

## [0.1.1] - 2026-07-15

- Remote Streamable HTTP mode and the hosted endpoint.

## [0.1.0] - 2026-07-15

- First release: search, listing details, seller profiles, categories and new-listing monitoring for marktplaats.nl and 2dehands.be.
