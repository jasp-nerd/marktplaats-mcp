"""Tool-contract tests: the server is exercised through FastMCP's in-memory
client (real MCP round-trip), with HTTP mocked by respx using recorded payloads."""

from collections.abc import Callable

import httpx
import pytest
import respx
from fastmcp import Client
from fastmcp.exceptions import ToolError

from marktplaats_mcp.server import mcp
from marktplaats_mcp.sites import SITES

SEARCH_URL_NL = SITES["marktplaats"].search_url
SEARCH_URL_BE = SITES["2dehands"].search_url


async def call(tool: str, args: dict) -> dict:
    async with Client(mcp) as client:
        result = await client.call_tool(tool, args)
        assert result.data is not None
        return dict(result.data)


async def test_all_tools_are_registered_with_descriptions():
    async with Client(mcp) as client:
        tools = {tool.name: tool for tool in await client.list_tools()}
    expected = {
        "search_listings",
        "get_listing_details",
        "get_seller_profile",
        "list_categories",
        "check_new_listings",
    }
    assert expected == set(tools)
    for tool in tools.values():
        assert tool.description, f"{tool.name} must have a description"
        assert tool.annotations is not None
        assert tool.annotations.readOnlyHint is True
        assert tool.annotations.destructiveHint is False


@respx.mock
async def test_search_listings_contract(search_response):
    respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=search_response))
    data = await call("search_listings", {"query": "fiets", "limit": 5})
    assert data["site"] == "marktplaats"
    assert data["total_count"] == search_response["totalResultCount"]
    assert data["returned"] == len(data["listings"]) <= 5
    first = data["listings"][0]
    # ids are 'm...' for consumer ads, 'a...' for Admarkt pro ads
    assert first["id"][0] in "ma"
    assert first["id"][1:].isdigit()
    assert first["title"]
    assert first["price"]
    assert first["url"].startswith("https://www.marktplaats.nl/")
    # promos are filtered out by default
    assert all("is_sponsored" not in listing for listing in data["listings"])
    # offsets count returned (organic) listings, so the next page starts at 5
    assert data["next_offset"] == 5
    assert "offset=5" in data["note"]


@respx.mock
async def test_search_listings_include_sponsored(search_response):
    respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=search_response))
    data = await call(
        "search_listings",
        {"query": "fiets", "limit": 100, "include_sponsored": True},
    )
    assert any(listing.get("is_sponsored") for listing in data["listings"])


@respx.mock
async def test_search_listings_full_mode_carries_seller_and_images(search_response):
    respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=search_response))
    data = await call("search_listings", {"query": "fiets", "compact": False, "limit": 3})
    first = data["listings"][0]
    assert "seller" in first
    assert first["image_urls"][0].startswith("https://")


@respx.mock
async def test_search_listings_2dehands_site(search_response_be):
    route = respx.get(SEARCH_URL_BE).mock(return_value=httpx.Response(200, json=search_response_be))
    data = await call("search_listings", {"query": "fiets", "site": "2dehands"})
    assert route.called
    assert data["site"] == "2dehands"
    assert "2dehands.be" in data["listings"][0]["url"]


@respx.mock
async def test_search_listings_passes_filters_to_api(search_response):
    route = respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=search_response))
    await call(
        "search_listings",
        {
            "query": "racefiets",
            "category": "Fietsen en Brommers",
            "price_from": 100,
            "price_to": 750.50,
            "condition": "used",
            "postcode": "1011 AB",
            "distance_km": 25,
        },
    )
    params = str(route.calls[0].request.url)
    assert "l1CategoryId=445" in params
    assert "PriceCents%3A10000%3A75050" in params
    assert "attributesById%5B%5D=32" in params
    assert "distanceMeters=25000" in params


def _fake_listing(item_id: str, promoted: bool = False) -> dict:
    return {
        "itemId": item_id,
        "title": f"Listing {item_id}",
        "priceInfo": {"priceType": "FIXED", "priceCents": 1000},
        "vipUrl": f"/v/cat/sub/{item_id}-listing",
        "location": {"cityName": "Gent"},
        "date": "Vandaag",
        "priorityProduct": "DAGTOPPER" if promoted else "NONE",
    }


@respx.mock
async def test_search_stops_when_api_repeats_itself():
    page = {
        "listings": [_fake_listing("m1", promoted=True)],
        "totalResultCount": 300,
    }
    route = respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=page))
    data = await call("search_listings", {"query": "fiets", "limit": 5})
    assert data["returned"] == 0
    assert route.call_count == 2  # second page repeated the same ids → stop


def fake_search_api(total: int, organic_from: int) -> Callable[[httpx.Request], httpx.Response]:
    """Simulate lrp/api/search: every raw row before ``organic_from`` is a paid
    promotion, and, like the real API, the offset is aligned down to a multiple
    of the requested limit."""

    def responder(request: httpx.Request) -> httpx.Response:
        params = request.url.params
        size = int(params["limit"])
        start = (int(params["offset"]) // size) * size
        rows = [
            _fake_listing(f"m{i}", promoted=i < organic_from)
            for i in range(start, min(start + size, total))
        ]
        return httpx.Response(200, json={"totalResultCount": total, "listings": rows})

    return responder


@respx.mock
async def test_small_limit_survives_promo_padded_pages():
    """Regression: date-sorted page 1 is often 100% DAGTOPPER. A poll with a small
    limit used to fetch three tiny pages of promos and return nothing."""
    route = respx.get(SEARCH_URL_NL).mock(side_effect=fake_search_api(500, organic_from=39))
    data = await call("check_new_listings", {"query": "racefiets", "limit": 3})
    assert data["new_count"] == 3
    assert [listing["id"] for listing in data["listings"]] == ["m39", "m40", "m41"]
    assert data["note"]  # more new listings exist beyond the limit
    assert route.call_count == 1


@respx.mock
async def test_search_fills_up_from_next_pages_when_page_one_is_all_promos():
    route = respx.get(SEARCH_URL_NL).mock(side_effect=fake_search_api(250, organic_from=120))
    data = await call("search_listings", {"query": "fiets", "limit": 3})
    assert route.call_count == 2
    assert [listing["id"] for listing in data["listings"]] == ["m120", "m121", "m122"]


@respx.mock
async def test_pagination_with_next_offset_yields_no_duplicates():
    route = respx.get(SEARCH_URL_NL).mock(side_effect=fake_search_api(160, organic_from=110))
    seen: list[str] = []
    offset = 0
    for _ in range(10):
        data = await call("search_listings", {"query": "fiets", "limit": 20, "offset": offset})
        seen += [listing["id"] for listing in data["listings"]]
        if data.get("next_offset") is None:
            assert "note" not in data
            break
        assert data["next_offset"] == offset + data["returned"]
        offset = data["next_offset"]
    assert seen == [f"m{i}" for i in range(110, 160)]
    # pages are cached between calls, so walking 50 listings hits the API twice
    assert route.call_count == 2


@respx.mock
async def test_page_cache_expires(monkeypatch):
    route = respx.get(SEARCH_URL_NL).mock(side_effect=fake_search_api(30, organic_from=0))
    await call("search_listings", {"query": "fiets", "limit": 5})
    await call("search_listings", {"query": "fiets", "limit": 5, "offset": 5})
    assert route.call_count == 1
    from marktplaats_mcp.server import get_client

    get_client().cache.ttl = 0
    get_client().cache.clear()
    await call("search_listings", {"query": "fiets", "limit": 5})
    await call("search_listings", {"query": "fiets", "limit": 5, "offset": 5})
    assert route.call_count == 3
    get_client().cache.ttl = 60


async def test_search_listings_requires_query_or_category():
    with pytest.raises(ToolError, match="query and/or a category"):
        await call("search_listings", {"query": ""})


@respx.mock
async def test_search_listings_surfaces_api_failure_as_tool_error():
    respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(403))
    with pytest.raises(ToolError, match="HTTP 403"):
        await call("search_listings", {"query": "fiets"})


@respx.mock
async def test_get_listing_details_contract(listing_page_html):
    respx.get(url__regex=r"https://link\.marktplaats\.nl/.*").mock(
        return_value=httpx.Response(200, text=listing_page_html)
    )
    data = await call("get_listing_details", {"listing_id": "m2420210707"})
    assert data["id"] == "m2420210707"
    assert data["title"]
    assert data["price"]
    assert data["view_count"] >= 0
    assert data["since"]
    assert data["description"]  # extracted from the description div fallback
    assert data["seller"]["id"]


@respx.mock
async def test_get_listing_details_prefixes_bare_numeric_id(listing_page_html):
    route = respx.get(url__regex=r"https://link\.marktplaats\.nl/.*").mock(
        return_value=httpx.Response(200, text=listing_page_html)
    )
    await call("get_listing_details", {"listing_id": "2420210707"})
    assert str(route.calls[0].request.url).endswith("/m2420210707")


@respx.mock
async def test_get_listing_details_not_found():
    respx.get(url__regex=r"https://link\.marktplaats\.nl/.*").mock(
        return_value=httpx.Response(200, text="<html><body>no config here</body></html>")
    )
    with pytest.raises(ToolError, match="not found"):
        await call("get_listing_details", {"listing_id": "m1"})


@respx.mock
async def test_get_seller_profile_contract(seller_response):
    respx.get(url__regex=r"https://www\.marktplaats\.nl/v/api/seller-profile/\d+").mock(
        return_value=httpx.Response(200, json=seller_response)
    )
    data = await call("get_seller_profile", {"seller_id": 12345})
    assert data["seller_id"] == 12345
    assert data["phone_number_verified"] is True
    assert data["bank_account_verified"] is False


async def test_list_categories_l1():
    data = await call("list_categories", {})
    assert data["level"] == "L1"
    names = {category["name"] for category in data["categories"]}
    assert "Fietsen en Brommers" in names
    assert all(isinstance(category["id"], int) for category in data["categories"])


async def test_list_categories_l2_by_parent_name():
    data = await call("list_categories", {"parent": "fietsen en brommers"})
    assert data["level"] == "L2"
    assert data["categories"]
    assert all(c["parent"] == "Fietsen en Brommers" for c in data["categories"])


async def test_list_categories_unknown_parent():
    with pytest.raises(ToolError, match="Unknown category"):
        await call("list_categories", {"parent": "does-not-exist"})


@respx.mock
async def test_check_new_listings_contract(search_response):
    route = respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=search_response))
    data = await call(
        "check_new_listings",
        {"query": "fiets", "since": "2026-07-14T00:00:00Z"},
    )
    params = str(route.calls[0].request.url)
    assert "sortBy=SORT_INDEX" in params
    assert "sortOrder=DECREASING" in params
    assert "offeredSince%3A1783987200000" in params  # 2026-07-14T00:00:00Z in unix millis
    assert data["since"] == "2026-07-14T00:00:00+00:00"
    assert data["cursor"] > data["since"]  # ISO strings compare chronologically here
    assert data["new_count"] == len(data["listings"])
    # promos never appear in monitoring results
    assert all("is_sponsored" not in listing for listing in data["listings"])


async def test_check_new_listings_rejects_bad_timestamp():
    with pytest.raises(ToolError, match="ISO 8601"):
        await call("check_new_listings", {"query": "fiets", "since": "yesterday"})
