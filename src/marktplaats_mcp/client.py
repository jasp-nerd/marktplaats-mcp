"""Async HTTP client for the undocumented Marktplaats/2dehands JSON API.

Resilience model (proven in jasp-nerd/marktplaats-monitor): retry transient
statuses with bounded exponential backoff plus jitter, and honor Retry-After.
"""

from __future__ import annotations

import asyncio
import random
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

# Condition filter codes for attributesById[].
CONDITION_IDS = {
    "new": 30,
    "as_good_as_new": 31,
    "used": 32,
    "refurbished": 14050,
    "not_working": 13940,
}

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


class ApiError(Exception):
    """The Marktplaats API returned an unusable response."""


class MarktplaatsClient:
    def __init__(
        self,
        timeout: float = 15.0,
        max_retries: int = 3,
        backoff_base: float = 1.0,
        backoff_cap: float = 30.0,
    ) -> None:
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.backoff_cap = backoff_cap
        self._http = httpx.AsyncClient(timeout=timeout, follow_redirects=True)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def _get(
        self,
        url: str,
        site: Site,
        params: list[tuple[str, str]] | None = None,
        accept: str | None = None,
    ) -> httpx.Response:
        headers = {**BASE_HEADERS, "Referer": f"{site.base_url}/"}
        if accept:
            headers["Accept"] = accept
        query = httpx.QueryParams(tuple(params)) if params is not None else None
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._http.get(url, params=query, headers=headers)
            except httpx.HTTPError as exc:
                last_error = exc
            else:
                if response.status_code < 400:
                    return response
                if response.status_code not in RETRY_STATUSES:
                    raise ApiError(f"HTTP {response.status_code} for {url}")
                last_error = ApiError(f"HTTP {response.status_code} for {url}")
                retry_after = _parse_retry_after(response.headers.get("Retry-After"))
                if retry_after is not None and attempt < self.max_retries:
                    await asyncio.sleep(min(retry_after, self.backoff_cap))
                    continue
            if attempt < self.max_retries:
                delay = min(self.backoff_cap, self.backoff_base * 2**attempt)
                await asyncio.sleep(delay + random.uniform(0, self.backoff_base))
        raise ApiError(f"Request failed after {self.max_retries + 1} attempts: {last_error}")

    async def search(self, site: Site, params: list[tuple[str, str]]) -> dict[str, Any]:
        response = await self._get(site.search_url, site, params=params)
        return _decode_json(response)

    async def seller_profile(self, site: Site, seller_id: int) -> dict[str, Any]:
        response = await self._get(site.seller_url(seller_id), site)
        return _decode_json(response)

    async def listing_page(self, site: Site, item_id: str) -> str:
        response = await self._get(
            site.listing_url(item_id),
            site,
            accept="text/html,application/xhtml+xml",
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
    l2_category_id: int | None = None,
    postcode: str | None = None,
    distance_km: float | None = None,
    price_from_cents: int | None = None,
    price_to_cents: int | None = None,
    condition: str | None = None,
    offered_since: datetime | None = None,
    sort_by: str = "relevance",
    sort_order: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> list[tuple[str, str]]:
    """Translate friendly arguments into the raw lrp/api/search query string."""
    if sort_by not in SORT_BY:
        raise ValueError(f"Invalid sort_by {sort_by!r}. Valid: {', '.join(SORT_BY)}.")
    if sort_order not in SORT_ORDER:
        raise ValueError(f"Invalid sort_order {sort_order!r}. Valid: {', '.join(SORT_ORDER)}.")
    if condition is not None and condition not in CONDITION_IDS:
        raise ValueError(f"Invalid condition {condition!r}. Valid: {', '.join(CONDITION_IDS)}.")
    if not query and l1_category_id is None and l2_category_id is None:
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
    if l2_category_id is not None:
        params.append(("l2CategoryId", str(l2_category_id)))
    if price_from_cents is not None or price_to_cents is not None:
        lower = "" if price_from_cents is None else str(price_from_cents)
        upper = "" if price_to_cents is None else str(price_to_cents)
        params.append(("attributeRanges[]", f"PriceCents:{lower}:{upper}"))
    if condition is not None:
        params.append(("attributesById[]", str(CONDITION_IDS[condition])))
    if offered_since is not None:
        millis = int(offered_since.timestamp() * 1000)
        params.append(("attributesByKey[]", f"offeredSince:{millis}"))
    return params


def since_days_ago(days: float) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)
