"""HTTP resilience and query-building tests (respx-mocked, no network)."""

from datetime import datetime, timezone

import httpx
import pytest
import respx

from marktplaats_mcp.client import (
    ApiError,
    MarktplaatsClient,
    build_search_params,
)
from marktplaats_mcp.sites import SITES

NL = SITES["marktplaats"]
SEARCH_URL = NL.search_url


def fast_client() -> MarktplaatsClient:
    return MarktplaatsClient(max_retries=2, backoff_base=0.001, backoff_cap=0.002)


@respx.mock
async def test_retries_on_429_then_succeeds():
    route = respx.get(SEARCH_URL).mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "0"}),
            httpx.Response(200, json={"listings": []}),
        ]
    )
    client = fast_client()
    try:
        data = await client.search(NL, [("query", "fiets")])
    finally:
        await client.aclose()
    assert data == {"listings": []}
    assert route.call_count == 2


@respx.mock
async def test_gives_up_after_max_retries_on_500():
    respx.get(SEARCH_URL).mock(return_value=httpx.Response(500))
    client = fast_client()
    try:
        with pytest.raises(ApiError, match="HTTP 500"):
            await client.search(NL, [("query", "fiets")])
    finally:
        await client.aclose()


@respx.mock
async def test_non_retryable_status_fails_immediately():
    route = respx.get(SEARCH_URL).mock(return_value=httpx.Response(404))
    client = fast_client()
    try:
        with pytest.raises(ApiError, match="HTTP 404"):
            await client.search(NL, [("query", "fiets")])
    finally:
        await client.aclose()
    assert route.call_count == 1


@respx.mock
async def test_malformed_json_raises_api_error():
    respx.get(SEARCH_URL).mock(return_value=httpx.Response(200, text="<html>not json</html>"))
    client = fast_client()
    try:
        with pytest.raises(ApiError, match="Invalid JSON"):
            await client.search(NL, [("query", "fiets")])
    finally:
        await client.aclose()


@respx.mock
async def test_network_error_is_retried():
    route = respx.get(SEARCH_URL).mock(
        side_effect=[
            httpx.ConnectError("boom"),
            httpx.Response(200, json={"listings": []}),
        ]
    )
    client = fast_client()
    try:
        data = await client.search(NL, [("query", "fiets")])
    finally:
        await client.aclose()
    assert data == {"listings": []}
    assert route.call_count == 2


@respx.mock
async def test_browser_headers_and_referer_are_sent():
    route = respx.get(SEARCH_URL).mock(return_value=httpx.Response(200, json={}))
    client = fast_client()
    try:
        await client.search(NL, [("query", "fiets")])
    finally:
        await client.aclose()
    request = route.calls[0].request
    assert "Mozilla/5.0" in request.headers["User-Agent"]
    assert request.headers["Referer"] == "https://www.marktplaats.nl/"
    assert request.headers["Accept-Language"].startswith("nl-NL")


class TestBuildSearchParams:
    def test_price_range_in_cents(self):
        params = build_search_params(query="fiets", price_from_cents=1000, price_to_cents=25000)
        assert ("attributeRanges[]", "PriceCents:1000:25000") in params

    def test_open_ended_price_range(self):
        params = build_search_params(query="fiets", price_to_cents=5000)
        assert ("attributeRanges[]", "PriceCents::5000") in params

    def test_condition_maps_to_numeric_code(self):
        params = build_search_params(query="fiets", condition="used")
        assert ("attributesById[]", "32") in params

    def test_offered_since_is_unix_millis(self):
        moment = datetime(2026, 7, 15, 12, 0, 0, tzinfo=timezone.utc)
        params = build_search_params(query="fiets", offered_since=moment)
        assert ("attributesByKey[]", f"offeredSince:{int(moment.timestamp() * 1000)}") in params

    def test_postcode_without_distance_uses_no_filter_sentinel(self):
        params = build_search_params(query="fiets", postcode="1011 ab")
        assert ("postcode", "1011 AB") in params
        assert ("distanceMeters", "1000000") in params

    def test_distance_km_converted_to_meters(self):
        params = build_search_params(query="fiets", postcode="1011 AB", distance_km=25)
        assert ("distanceMeters", "25000") in params

    def test_sort_date_desc_maps_to_sort_index(self):
        params = build_search_params(query="fiets", sort_by="date", sort_order="desc")
        assert ("sortBy", "SORT_INDEX") in params
        assert ("sortOrder", "DECREASING") in params

    def test_limit_is_clamped_to_api_maximum(self):
        params = build_search_params(query="fiets", limit=500)
        assert ("limit", "100") in params

    def test_requires_query_or_category(self):
        with pytest.raises(ValueError, match="query and/or a category"):
            build_search_params(query="")

    def test_category_only_is_allowed(self):
        params = build_search_params(query="", l1_category_id=445)
        assert ("l1CategoryId", "445") in params

    def test_invalid_condition_rejected(self):
        with pytest.raises(ValueError, match="Invalid condition"):
            build_search_params(query="fiets", condition="broken")
