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
VIP_URL_NL = r"https://app\.marktplaats\.nl/app/vip/v4/item/.*"
PAGE_URL_NL = r"https://link\.marktplaats\.nl/.*"

READ_ONLY_TOOLS = {
    "search_listings",
    "get_listing_details",
    "get_seller_profile",
    "list_seller_listings",
    "list_categories",
    "list_category_filters",
    "check_new_listings",
    "analyze_prices",
}


async def call(tool: str, args: dict) -> dict:
    async with Client(mcp) as client:
        result = await client.call_tool(tool, args)
        assert result.structured_content is not None
        return dict(result.structured_content)


async def test_all_tools_are_registered_with_descriptions():
    async with Client(mcp) as client:
        tools = {tool.name: tool for tool in await client.list_tools()}
        prompts = {prompt.name for prompt in await client.list_prompts()}
    assert set(tools) == READ_ONLY_TOOLS
    for tool in tools.values():
        assert tool.description, f"{tool.name} must have a description"
        assert tool.annotations is not None
        assert tool.annotations.read_only_hint is True
        assert tool.annotations.destructive_hint is False
    assert {"bargain_hunt", "vet_listing"} <= prompts
    for tool in tools.values():
        schema = tool.output_schema or {}
        assert schema.get("properties"), f"{tool.name} has no real output schema"


async def test_category_resources():
    async with Client(mcp) as client:
        resources = {str(r.uri) for r in await client.list_resources()}
        templates = {t.uri_template for t in await client.list_resource_templates()}
        assert "marktplaats://categories" in resources
        assert "marktplaats://categories/{parent}" in templates
        top = await client.read_resource("marktplaats://categories")
        sub = await client.read_resource("marktplaats://categories/445")
    assert "Fietsen en Brommers" in top[0].text
    assert "Racefietsen" in sub[0].text


# --- search_listings ---------------------------------------------------------


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
    assert first["listed"].count("-") == 2  # ISO date, not "Vandaag"
    # promos are filtered out by default
    assert all("is_sponsored" not in listing for listing in data["listings"])
    # next_offset is a position in the raw result list, so it lands past the
    # five returned ads plus any promotions that were skipped in between
    assert data["next_offset"] >= 5
    assert f"offset={data['next_offset']}" in data["note"]


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
    assert "attributes" in first


@respx.mock
async def test_search_listings_2dehands_site(search_response_be):
    route = respx.get(SEARCH_URL_BE).mock(return_value=httpx.Response(200, json=search_response_be))
    data = await call("search_listings", {"query": "fiets", "site": "2dehands", "language": "nl"})
    assert route.called
    assert data["site"] == "2dehands"
    assert "2dehands.be" in data["listings"][0]["url"]
    assert "Language%3Anl-BE" in str(route.calls[0].request.url)


async def test_language_is_2dehands_only():
    with pytest.raises(ToolError, match="2dehands"):
        await call("search_listings", {"query": "fiets", "language": "fr"})


async def test_distance_requires_postcode():
    with pytest.raises(ToolError, match="postcode"):
        await call("search_listings", {"query": "fiets", "distance_km": 10})


@respx.mock
async def test_search_listings_passes_filters_to_api(search_response):
    route = respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=search_response))
    await call(
        "search_listings",
        {
            "query": "racefiets",
            "category": "Fietsen en Brommers",
            "subcategory": "Fietsen | Racefietsen",
            "price_from": 100,
            "price_to": 750.50,
            "condition": "used",
            "delivery": "shipping",
            "postcode": "1011 AB",
            "distance_km": 25,
        },
    )
    params = str(route.calls[-1].request.url)
    assert "l1CategoryId=445" in params
    assert "l2CategoryIds%5B%5D=464" in params
    assert "PriceCents%3A10000%3A75050" in params
    assert "attributesById%5B%5D=32" in params
    assert "attributesById%5B%5D=34" in params
    assert "distanceMeters=25000" in params


@respx.mock
async def test_subcategory_alone_resolves_its_parent(search_response):
    route = respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=search_response))
    await call("search_listings", {"query": "", "subcategory": "racefietsen"})
    params = str(route.calls[-1].request.url)
    assert "l1CategoryId=445" in params
    assert "l2CategoryIds%5B%5D=464" in params


@respx.mock
async def test_attributes_are_resolved_through_live_facets(facets_bikes, search_response):
    def responder(request: httpx.Request) -> httpx.Response:
        if request.url.params["limit"] == "1":
            return httpx.Response(200, json=facets_bikes)  # the facet probe
        return httpx.Response(200, json=search_response)

    route = respx.get(SEARCH_URL_NL).mock(side_effect=responder)
    await call(
        "search_listings",
        {
            "query": "",
            "subcategory": "Fietsen | Racefietsen",
            "attributes": {"Merk": "Batavus", "Framehoogte": ["57 tot 61 cm"]},
        },
    )
    assert route.call_count == 2
    params = str(route.calls[-1].request.url)
    assert "attributesById%5B%5D=3408" in params
    # a second search in the same category reuses the cached facets
    await call(
        "search_listings",
        {"query": "", "subcategory": "racefietsen", "attributes": {"merk": "batavus"}},
    )
    assert route.call_count == 3


@respx.mock
async def test_condition_uses_the_category_specific_id(facets_cars, search_response):
    def responder(request: httpx.Request) -> httpx.Response:
        if request.url.params["limit"] == "1":
            return httpx.Response(200, json=facets_cars)
        return httpx.Response(200, json=search_response)

    route = respx.get(SEARCH_URL_NL).mock(side_effect=responder)
    await call("search_listings", {"query": "golf", "category": "Auto's", "condition": "used"})
    params = str(route.calls[-1].request.url)
    assert "attributesById%5B%5D=14049" in params  # used cars, not the generic 32


@respx.mock
async def test_unknown_attribute_is_a_tool_error(facets_bikes):
    respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=facets_bikes))
    with pytest.raises(ToolError, match="Unknown filter 'kleur'"):
        await call(
            "search_listings",
            {"query": "", "subcategory": "racefietsen", "attributes": {"kleur": "rood"}},
        )


def _fake_listing(item_id: str, promoted: bool = False, title: str | None = None) -> dict:
    return {
        "itemId": item_id,
        "title": title or f"Listing {item_id}",
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
    respx.post(url__regex=VIP_URL_NL).mock(return_value=httpx.Response(503))
    data = await call("check_new_listings", {"query": "racefiets", "limit": 3})
    assert data["new_count"] == 3
    assert [listing["id"] for listing in data["listings"]] == ["m39", "m40", "m41"]
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
        assert data["next_offset"] > offset
        offset = data["next_offset"]
    assert seen == [f"m{i}" for i in range(110, 160)]
    # pages are cached between calls, so walking 50 listings hits the API twice
    assert route.call_count == 2


@respx.mock
async def test_deep_offsets_fetch_one_page_and_never_loop():
    """Regression: offsets past the per-call page budget used to return nothing
    with next_offset == offset, so an agent following the note paged forever."""
    route = respx.get(SEARCH_URL_NL).mock(side_effect=fake_search_api(2000, organic_from=0))
    data = await call("search_listings", {"query": "fiets", "limit": 20, "offset": 1234})
    assert [listing["id"] for listing in data["listings"]] == [f"m{i}" for i in range(1234, 1254)]
    assert data["next_offset"] == 1254
    assert route.call_count == 1  # straight to the page that holds position 1234
    last = await call("search_listings", {"query": "fiets", "limit": 20, "offset": 1990})
    assert data["returned"] == 20
    assert last["returned"] == 10
    assert "next_offset" not in last  # the result set is exhausted


@respx.mock
async def test_offset_walk_terminates_when_everything_left_is_promoted():
    route = respx.get(SEARCH_URL_NL).mock(side_effect=fake_search_api(1000, organic_from=900))
    data = await call("search_listings", {"query": "fiets", "limit": 5, "offset": 0})
    # five promo-only pages: nothing to return yet, but the cursor moved past them
    assert data["returned"] == 0
    assert data["next_offset"] == 500
    assert route.call_count == 5
    data = await call("search_listings", {"query": "fiets", "limit": 5, "offset": 500})
    assert [listing["id"] for listing in data["listings"]] == [f"m{i}" for i in range(900, 905)]


@respx.mock
async def test_exclude_terms_filter_client_side():
    rows = [
        _fake_listing("m1", title="iPhone 15 hoesje"),
        _fake_listing("m2", title="iPhone 15 128GB"),
        _fake_listing("m3", title="GEZOCHT: iphone 15"),
    ]
    respx.get(SEARCH_URL_NL).mock(
        return_value=httpx.Response(200, json={"totalResultCount": 3, "listings": rows})
    )
    data = await call("search_listings", {"query": "iphone 15", "exclude": ["hoesje", "gezocht"]})
    assert [listing["id"] for listing in data["listings"]] == ["m2"]
    assert "next_offset" not in data


@respx.mock
async def test_spelling_suggestion_is_surfaced():
    respx.get(SEARCH_URL_NL).mock(
        return_value=httpx.Response(
            200, json={"totalResultCount": 0, "listings": [], "suggestedQuery": "racefiets"}
        )
    )
    data = await call("search_listings", {"query": "racefitse"})
    assert data["suggested_query"] == "racefiets"


async def test_search_listings_requires_query_or_category():
    with pytest.raises(ToolError, match="query and/or a category"):
        await call("search_listings", {"query": ""})


@respx.mock
async def test_search_listings_surfaces_api_failure_as_tool_error():
    respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(403))
    with pytest.raises(ToolError, match="rate-limiting or blocking"):
        await call("search_listings", {"query": "fiets"})


# --- get_listing_details -------------------------------------------------------


@respx.mock
async def test_get_listing_details_uses_app_endpoint(listing_vip):
    route = respx.post(url__regex=VIP_URL_NL).mock(
        return_value=httpx.Response(200, json=listing_vip)
    )
    data = await call("get_listing_details", {"listing_id": "m2444371973"})
    assert route.calls[0].request.url.path.endswith("/m2444371973")
    assert data["id"] == "m2444371973"
    assert data["status"] == "ACTIVE"
    assert data["attributes"]["Conditie"] == "Gebruikt"
    assert data["seller"]["response_rate_percent"] == 74
    assert data["bidding"]["minimum_bid_euros"] == 150.0
    assert len(data["image_urls"]) == 5
    assert data["image_count"] == 7


@respx.mock
async def test_get_listing_details_accepts_urls_and_bare_ids(listing_vip):
    route = respx.post(url__regex=VIP_URL_NL).mock(
        return_value=httpx.Response(200, json=listing_vip)
    )
    be_route = respx.post(url__regex=r"https://app\.2dehands\.be/app/vip/v4/item/.*").mock(
        return_value=httpx.Response(200, json=listing_vip)
    )
    await call("get_listing_details", {"listing_id": "2444371973"})
    assert route.calls[-1].request.url.path.endswith("/m2444371973")
    await call(
        "get_listing_details",
        {"listing_id": "https://www.marktplaats.nl/v/fietsen/racefietsen/m2444371973-baan-fiets"},
    )
    assert route.calls[-1].request.url.path.endswith("/m2444371973")
    # the site is inferred from a 2dehands URL even if the site param says otherwise
    await call("get_listing_details", {"listing_id": "https://link.2dehands.be/m2443283582"})
    assert be_route.called
    await call("get_listing_details", {"listing_id": "www.2ememain.be/v/velos/m2443283582-velo"})
    assert be_route.call_count == 2
    # ...but only from the hostname, not from a word in the slug
    await call(
        "get_listing_details",
        {"listing_id": "https://www.marktplaats.nl/v/fietsen/m2444371973-2dehands-racefiets"},
    )
    assert route.calls[-1].request.url.host == "app.marktplaats.nl"
    assert be_route.call_count == 2


def test_rate_limit_bucket_uses_the_proxy_added_forwarded_hop(monkeypatch):
    """A client can put anything at the front of X-Forwarded-For; only the address
    the reverse proxy appended identifies it."""
    import fastmcp.server.dependencies as deps

    from marktplaats_mcp.server import _client_key

    monkeypatch.setattr(deps, "get_http_headers", lambda: {"x-forwarded-for": "1.2.3.4, 10.0.0.9"})
    assert _client_key(None) == "10.0.0.9"
    monkeypatch.setattr(deps, "get_http_headers", lambda: {"x-forwarded-for": "10.0.0.9"})
    assert _client_key(None) == "10.0.0.9"


@respx.mock
async def test_get_listing_details_falls_back_to_page_when_app_api_fails(listing_page_html):
    respx.post(url__regex=VIP_URL_NL).mock(return_value=httpx.Response(503))
    respx.get(url__regex=PAGE_URL_NL).mock(return_value=httpx.Response(200, text=listing_page_html))
    data = await call("get_listing_details", {"listing_id": "m2420210707"})
    assert data["title"]
    assert data["description"]


@respx.mock
async def test_get_listing_details_not_found_is_actionable():
    respx.post(url__regex=VIP_URL_NL).mock(
        return_value=httpx.Response(404, json={"code": "NOT_FOUND"})
    )
    with pytest.raises(ToolError, match="sold or removed"):
        await call("get_listing_details", {"listing_id": "m9999999999"})


async def test_get_listing_details_rejects_garbage_ids():
    with pytest.raises(ToolError, match="Invalid listing_id"):
        await call("get_listing_details", {"listing_id": "not-an-id"})


# --- sellers -------------------------------------------------------------------


@respx.mock
async def test_get_seller_profile_contract(seller_response):
    respx.get(url__regex=r"https://www\.marktplaats\.nl/v/api/seller-profile/\d+").mock(
        return_value=httpx.Response(200, json=seller_response)
    )
    data = await call("get_seller_profile", {"seller_id": 12345})
    assert data["seller_id"] == 12345
    assert data["phone_number_verified"] is True
    assert data["bank_account_verified"] is False
    # unknown signals are explicit nulls, so "no data" and "0 reviews" differ
    assert "business_verified" in data
    assert "number_of_reviews" in data


@respx.mock
async def test_list_seller_listings_searches_by_seller_id(search_response):
    route = respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=search_response))
    data = await call("list_seller_listings", {"seller_id": 518777, "limit": 5})
    params = str(route.calls[0].request.url)
    assert "sellerIds%5B%5D=518777" in params
    assert "sortBy=SORT_INDEX" in params
    assert data["returned"] == 5


# --- categories & filters -------------------------------------------------------


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
async def test_list_category_filters_contract(facets_bikes):
    route = respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=facets_bikes))
    data = await call("list_category_filters", {"subcategory": "Fietsen | Racefietsen"})
    params = str(route.calls[0].request.url)
    assert "limit=1" in params
    assert "l2CategoryIds%5B%5D=464" in params
    assert data["category"] == "Fietsen en Brommers"
    assert data["subcategory"] == "Fietsen | Racefietsen"
    by_key = {f["key"]: f for f in data["filters"]}
    assert by_key["brand"]["label"] == "Merk"
    assert by_key["brand"]["options"][0]["label"]
    assert "attributes=" in data["note"]


async def test_list_category_filters_needs_a_category_or_query():
    with pytest.raises(ToolError, match="category"):
        await call("list_category_filters", {})


# --- check_new_listings --------------------------------------------------------


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
    assert "truncated" not in data
    # promos never appear in monitoring results
    assert all("is_sponsored" not in listing for listing in data["listings"])


@respx.mock
async def test_check_new_listings_keeps_cursor_when_oldest_ad_cannot_be_timed():
    respx.get(SEARCH_URL_NL).mock(side_effect=fake_search_api(500, organic_from=0))
    respx.post(url__regex=VIP_URL_NL).mock(return_value=httpx.Response(503))
    data = await call(
        "check_new_listings", {"query": "fiets", "since": "2026-07-14T00:00:00Z", "limit": 3}
    )
    assert data["new_count"] == 3
    assert data["truncated"] is True
    assert data["cursor"] == data["since"]  # nothing is skipped on the next poll
    assert "Raise the limit" in data["note"]


async def test_check_new_listings_rejects_bad_timestamp():
    with pytest.raises(ToolError, match="ISO 8601"):
        await call("check_new_listings", {"query": "fiets", "since": "yesterday"})


# --- analyze_prices ------------------------------------------------------------


@respx.mock
async def test_price_sort_and_bounds_skip_unpriced_ads():
    def priced(item_id: str, cents: int, price_type: str = "FIXED") -> dict:
        row = _fake_listing(item_id)
        row["priceInfo"] = {"priceType": price_type, "priceCents": cents}
        return row

    rows = [
        priced("m1", 0, "FREE"),
        priced("m2", 0, "FAST_BID"),
        priced("m3", 5000),
        priced("m4", 9000),
    ]
    respx.get(SEARCH_URL_NL).mock(
        return_value=httpx.Response(200, json={"totalResultCount": 4, "listings": rows})
    )
    data = await call("search_listings", {"query": "x", "sort_by": "price", "sort_order": "asc"})
    assert [item["id"] for item in data["listings"]] == ["m3", "m4"]
    data = await call("search_listings", {"query": "x", "price_to": 100})
    assert [item["id"] for item in data["listings"]] == ["m3", "m4"]
    data = await call(
        "search_listings", {"query": "x", "sort_by": "price", "include_unpriced": True}
    )
    assert len(data["listings"]) == 4
    data = await call("search_listings", {"query": "x"})  # relevance: unpriced ads stay
    assert len(data["listings"]) == 4


@respx.mock
async def test_check_new_listings_advances_cursor_to_oldest_returned_ad(listing_vip):
    respx.get(SEARCH_URL_NL).mock(side_effect=fake_search_api(500, organic_from=0))
    vip = respx.post(url__regex=VIP_URL_NL).mock(
        return_value=httpx.Response(200, json=listing_vip)  # listed 2026-09-19T13:01:54
    )
    data = await call(
        "check_new_listings", {"query": "fiets", "since": "2026-07-14T00:00:00Z", "limit": 3}
    )
    assert data["truncated"] is True
    assert vip.calls[0].request.url.path.endswith("/m2")  # the oldest of the three returned
    assert data["cursor"].startswith("2026-09-19T13:01:54")
    assert "oldest ad" in data["note"]


@respx.mock
async def test_analyze_prices_trims_outliers_and_accepts_bounds():
    def priced(item_id: str, cents: int) -> dict:
        row = _fake_listing(item_id)
        row["priceInfo"] = {"priceType": "FIXED", "priceCents": cents}
        return row

    rows = [priced(f"m{i}", 40000 + i * 1000) for i in range(10)] + [priced("mac", 4300)]
    route = respx.get(SEARCH_URL_NL).mock(
        return_value=httpx.Response(200, json={"totalResultCount": 11, "listings": rows})
    )
    data = await call("analyze_prices", {"query": "iphone 15", "price_to": 600})
    assert "PriceCents%3A%3A60000" in str(route.calls[0].request.url)
    assert data["excluded_outliers"] == 1
    assert data["min"] == 400.0
    assert [item["id"] for item in data["cheapest"]] == ["m0", "m1", "m2"]


@respx.mock
async def test_list_category_filters_limits_options(facets_bikes):
    respx.get(SEARCH_URL_NL).mock(return_value=httpx.Response(200, json=facets_bikes))
    data = await call(
        "list_category_filters", {"subcategory": "Fietsen | Racefietsen", "max_options": 2}
    )
    brand = next(f for f in data["filters"] if f["key"] == "brand")
    assert len(brand["options"]) == 2
    assert brand["options"][0]["count"] >= brand["options"][1]["count"]


@respx.mock
async def test_analyze_prices_contract():
    def priced(item_id: str, cents: int, price_type: str = "FIXED", reserved: bool = False) -> dict:
        row = _fake_listing(item_id)
        row["priceInfo"] = {"priceType": price_type, "priceCents": cents}
        row["reserved"] = reserved
        return row

    rows = [
        priced("m1", 10000),
        priced("m2", 20000),
        priced("m3", 30000),
        priced("m4", 40000),
        priced("m5", 0, "FAST_BID"),  # bidding without amount: excluded
        priced("m6", 500, reserved=True),  # reserved: excluded
        priced("m7", 0, "FREE"),  # free: excluded
    ]
    respx.get(SEARCH_URL_NL).mock(
        return_value=httpx.Response(200, json={"totalResultCount": 7, "listings": rows})
    )
    data = await call("analyze_prices", {"query": "fiets"})
    assert data["sample_size"] == 4
    assert data["total_count"] == 7
    assert "excluded_outliers" not in data
    assert (data["min"], data["median"], data["max"]) == (100.0, 250.0, 400.0)
    assert data["p25"] == 175.0
    assert data["p75"] == 325.0
    assert data["mean"] == 250.0
    assert [item["id"] for item in data["cheapest"]] == ["m1", "m2", "m3"]
    assert "not sold prices" in data["note"]


@respx.mock
async def test_analyze_prices_without_priced_ads():
    respx.get(SEARCH_URL_NL).mock(
        return_value=httpx.Response(200, json={"totalResultCount": 0, "listings": []})
    )
    data = await call("analyze_prices", {"query": "unobtainium"})
    assert data["sample_size"] == 0
    assert "median" not in data
