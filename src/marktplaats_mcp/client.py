"""Async HTTP client for the undocumented Marktplaats/2dehands JSON API.

Resilience model (proven in jasp-nerd/marktplaats-monitor): retry transient
statuses with bounded exponential backoff plus jitter, and honor Retry-After.
Outbound requests are additionally spaced by a minimum interval so an agent
firing many tool calls at once never bursts at the upstream WAF.
"""

from __future__ import annotations

import asyncio
import os
import random
import time
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from .sites import Site

# Browser-like headers; the API returns 200 with these and may block bare clients.
BASE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

RETRY_STATUSES = {429, 500, 502, 503, 504}

# Generic attribute value ids, identical in every category. Category-specific
# ids (car fuel, laptop RAM, ...) are discovered at runtime from the facets.
CONDITION_IDS = {
    "new": 30,
    "as_good_as_new": 31,
    "used": 32,
    "refurbished": 14050,
    "not_working": 13940,
}
DELIVERY_IDS = {"pickup": 33, "shipping": 34}
LANGUAGE_KEYS = {"nl": "nl-BE", "fr": "fr-BE", "all": "all-languages"}

SORT_BY = {
    "relevance": "OPTIMIZED",
    "date": "SORT_INDEX",
    "price": "PRICE",
    "location": "LOCATION",
}
SORT_ORDER = {"asc": "INCREASING", "desc": "DECREASING"}

# The API treats distanceMeters as "no filter" when very large.
NO_DISTANCE_FILTER = 1_000_000
MAX_LIMIT = 100

Range = tuple[int | None, int | None]


class ApiError(Exception):
    """The Marktplaats API returned an unusable response."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class NotFoundError(ApiError):
    """The requested resource does not exist (HTTP 404)."""


class PageCache:
    """Small TTL cache for raw JSON responses.

    Pagination walks aligned pages from offset 0 (see server._collect_listings),
    so consecutive tool calls in one session re-read the same page. Serving it
    from memory keeps us polite towards the upstream API.
    """

    def __init__(self, ttl: float = 60.0, max_entries: int = 64) -> None:
        self.ttl = ttl
        self.max_entries = max_entries
        self._entries: OrderedDict[Any, tuple[float, dict[str, Any]]] = OrderedDict()

    def get(self, key: Any) -> dict[str, Any] | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if expires_at < time.monotonic():
            del self._entries[key]
            return None
        self._entries.move_to_end(key)
        return value

    def put(self, key: Any, value: dict[str, Any]) -> None:
        if self.ttl <= 0:
            return
        self._entries[key] = (time.monotonic() + self.ttl, value)
        self._entries.move_to_end(key)
        while len(self._entries) > self.max_entries:
            self._entries.popitem(last=False)

    def clear(self) -> None:
        self._entries.clear()


class MarktplaatsClient:
    def __init__(
        self,
        timeout: float = 15.0,
        max_retries: int = 3,
        backoff_base: float = 1.0,
        backoff_cap: float = 30.0,
        cache_ttl: float = 60.0,
        min_interval: float | None = None,
    ) -> None:
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.backoff_cap = backoff_cap
        self.cache = PageCache(ttl=cache_ttl)
        self.min_interval = (
            min_interval
            if min_interval is not None
            else int(os.environ.get("MARKTPLAATS_MIN_INTERVAL_MS", "200")) / 1000
        )
        self._gate = asyncio.Lock()
        self._next_slot = 0.0
        self._http = httpx.AsyncClient(timeout=timeout, follow_redirects=True)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def _wait_for_slot(self) -> None:
        async with self._gate:
            now = time.monotonic()
            if now < self._next_slot:
                await asyncio.sleep(self._next_slot - now)
            self._next_slot = max(now, self._next_slot) + self.min_interval

    async def _request(
        self,
        method: str,
        url: str,
        site: Site,
        params: list[tuple[str, str]] | None = None,
        headers: dict[str, str] | None = None,
        json_body: Any | None = None,
    ) -> httpx.Response:
        all_headers = {**BASE_HEADERS, "Referer": f"{site.base_url}/", **(headers or {})}
        query = httpx.QueryParams(tuple(params)) if params is not None else None
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            await self._wait_for_slot()
            try:
                response = await self._http.request(
                    method, url, params=query, headers=all_headers, json=json_body
                )
            except httpx.HTTPError as exc:
                last_error = exc
            else:
                status = response.status_code
                if status < 400:
                    return response
                if status == 404:
                    raise NotFoundError(f"HTTP 404 for {url}", status)
                if status not in RETRY_STATUSES:
                    raise ApiError(f"HTTP {status} for {url}", status)
                last_error = ApiError(f"HTTP {status} for {url}", status)
                retry_after = _parse_retry_after(response.headers.get("Retry-After"))
                if retry_after is not None and attempt < self.max_retries:
                    await asyncio.sleep(min(retry_after, self.backoff_cap))
                    continue
            if attempt < self.max_retries:
                delay = min(self.backoff_cap, self.backoff_base * 2**attempt)
                await asyncio.sleep(delay + random.uniform(0, self.backoff_base))
        final_status = last_error.status if isinstance(last_error, ApiError) else None
        raise ApiError(
            f"Request failed after {self.max_retries + 1} attempts: {last_error}", final_status
        )

    async def search(self, site: Site, params: list[tuple[str, str]]) -> dict[str, Any]:
        key = (site.key, tuple(params))
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        response = await self._request("GET", site.search_url, site, params=params)
        data = _decode_json(response)
        self.cache.put(key, data)
        return data

    async def seller_profile(self, site: Site, seller_id: int) -> dict[str, Any]:
        response = await self._request("GET", site.seller_url(seller_id), site)
        return _decode_json(response)

    async def listing(self, site: Site, item_id: str) -> dict[str, Any]:
        """Full listing payload from the app endpoint (typed attributes, status,
        exact timestamps, seller response rate, bidding state)."""
        response = await self._request(
            "POST",
            site.vip_url(item_id),
            site,
            headers={"ecg-locale": site.locale, "Content-Type": "application/json"},
        )
        return _decode_json(response)

    async def listing_page(self, site: Site, item_id: str) -> str:
        response = await self._request(
            "GET",
            site.listing_url(item_id),
            site,
            headers={"Accept": "text/html,application/xhtml+xml"},
        )
        return response.text


def _decode_json(response: httpx.Response) -> dict[str, Any]:
    try:
        data = response.json()
    except ValueError as exc:
        raise ApiError(f"Invalid JSON from {response.url}") from exc
    if not isinstance(data, dict):
        raise ApiError(f"Unexpected JSON shape from {response.url}")
    return data


def _parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        return None


def build_search_params(
    query: str = "",
    l1_category_id: int | None = None,
    l2_category_ids: list[int] | None = None,
    postcode: str | None = None,
    distance_km: float | None = None,
    price_from_cents: int | None = None,
    price_to_cents: int | None = None,
    condition: str | None = None,
    delivery: str | None = None,
    language: str | None = None,
    attribute_ids: list[int] | None = None,
    attribute_ranges: dict[str, Range] | None = None,
    seller_ids: list[int] | None = None,
    offered_since: datetime | None = None,
    sort_by: str = "relevance",
    sort_order: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> list[tuple[str, str]]:
    """Translate friendly arguments into the raw lrp/api/search query string.

    Note that the API only honours the plural ``l2CategoryIds`` form for
    subcategories (the singular ``l2CategoryId`` is silently ignored) and that
    it aligns ``offset`` down to a multiple of ``limit``.
    """
    if sort_by not in SORT_BY:
        raise ValueError(f"Invalid sort_by {sort_by!r}. Valid: {', '.join(SORT_BY)}.")
    if sort_order not in SORT_ORDER:
        raise ValueError(f"Invalid sort_order {sort_order!r}. Valid: {', '.join(SORT_ORDER)}.")
    if condition is not None and condition not in CONDITION_IDS:
        raise ValueError(f"Invalid condition {condition!r}. Valid: {', '.join(CONDITION_IDS)}.")
    if delivery is not None and delivery not in DELIVERY_IDS:
        raise ValueError(f"Invalid delivery {delivery!r}. Valid: {', '.join(DELIVERY_IDS)}.")
    if language is not None and language not in LANGUAGE_KEYS:
        raise ValueError(f"Invalid language {language!r}. Valid: {', '.join(LANGUAGE_KEYS)}.")
    if not query and l1_category_id is None and not l2_category_ids and not seller_ids:
        raise ValueError("Provide a query and/or a category.")

    limit = max(1, min(limit, MAX_LIMIT))
    params: list[tuple[str, str]] = [
        ("query", query),
        ("limit", str(limit)),
        ("offset", str(max(0, offset))),
        ("searchInTitleAndDescription", "true"),
        ("viewOptions", "list-view"),
        ("sortBy", SORT_BY[sort_by]),
        ("sortOrder", SORT_ORDER[sort_order]),
    ]
    if postcode:
        params.append(("postcode", postcode.strip().upper()))
        meters = NO_DISTANCE_FILTER if distance_km is None else int(distance_km * 1000)
        params.append(("distanceMeters", str(meters)))
    if l1_category_id is not None:
        params.append(("l1CategoryId", str(l1_category_id)))
    for l2_id in l2_category_ids or []:
        params.append(("l2CategoryIds[]", str(l2_id)))
    for seller_id in seller_ids or []:
        params.append(("sellerIds[]", str(seller_id)))
    ranges: dict[str, Range] = {}
    if price_from_cents is not None or price_to_cents is not None:
        ranges["PriceCents"] = (price_from_cents, price_to_cents)
    ranges.update(attribute_ranges or {})
    for key, (lower, upper) in ranges.items():
        lower_s = "" if lower is None else str(lower)
        upper_s = "" if upper is None else str(upper)
        params.append(("attributeRanges[]", f"{key}:{lower_s}:{upper_s}"))
    ids: list[int] = []
    if condition is not None:
        ids.append(CONDITION_IDS[condition])
    if delivery is not None:
        ids.append(DELIVERY_IDS[delivery])
    ids.extend(attribute_ids or [])
    for attribute_id in ids:
        params.append(("attributesById[]", str(attribute_id)))
    if language is not None:
        params.append(("attributesByKey[]", f"Language:{LANGUAGE_KEYS[language]}"))
    if offered_since is not None:
        millis = int(offered_since.timestamp() * 1000)
        params.append(("attributesByKey[]", f"offeredSince:{millis}"))
    return params


def since_days_ago(days: float) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)
