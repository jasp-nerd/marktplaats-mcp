"""Daily live canary: exercise every read-only tool against the real sites.

The upstream API is undocumented and changes silently (the subcategory
parameter was a no-op for months before anyone noticed), so CI runs this on a
schedule and opens an issue when it fails. It performs a handful of polite
requests and never touches an account.

Run locally: uv run python scripts/e2e_smoke.py
"""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timezone
from typing import Any

from fastmcp import Client

from marktplaats_mcp.server import mcp

TOOLS_EXPECTED = {
    "search_listings",
    "get_listing_details",
    "get_seller_profile",
    "list_seller_listings",
    "list_categories",
    "list_category_filters",
    "check_new_listings",
    "analyze_prices",
}
SITES_TO_PROBE = (("marktplaats", "racefiets", "1011 AB"), ("2dehands", "koersfiets", "2000"))


class Check:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.passed = 0

    def ok(self, condition: bool, message: str) -> None:
        if condition:
            self.passed += 1
        else:
            self.failures.append(message)
            print(f"  FAIL: {message}")


async def run() -> int:
    check = Check()
    async with Client(mcp) as client:
        tools = {tool.name for tool in await client.list_tools()}
        check.ok(tools >= TOOLS_EXPECTED, f"tools missing: {TOOLS_EXPECTED - tools}")
        for site, query, postcode in SITES_TO_PROBE:
            await probe_site(client, check, site, query, postcode)
        await probe_filters(client, check)
        await probe_derived(client, check)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"\n{check.passed} checks passed, {len(check.failures)} failed at {stamp}")
    return 1 if check.failures else 0


async def probe_site(client: Client, check: Check, site: str, query: str, postcode: str) -> None:
    print(f"== {site}: search_listings")
    args = {"query": query, "site": site, "postcode": postcode, "distance_km": 50, "limit": 5}
    data = await call(client, "search_listings", args)
    check.ok(data["returned"] > 0, f"{site}: no listings for {query!r}")
    check.ok(data["total_count"] > 100, f"{site}: low total_count {data['total_count']}")
    listing = data["listings"][0]
    check.ok(listing["url"].startswith("https://"), f"{site}: bad url {listing['url']}")
    check.ok(listing["listed"][:4].isdigit(), f"{site}: date not normalised: {listing['listed']}")
    has_distance = any("distance_km" in item for item in data["listings"])
    check.ok(has_distance, f"{site}: no distances with postcode")

    print(f"== {site}: get_listing_details")
    args = {"listing_id": listing["id"], "site": site, "max_images": 1}
    details = await call(client, "get_listing_details", args)
    check.ok(details.get("status") == "ACTIVE", f"{site}: status {details.get('status')!r}")
    check.ok(bool(details.get("attributes")), f"{site}: details without attributes")
    check.ok(bool(details.get("listed_at")), f"{site}: details without listed_at")
    seller = details.get("seller") or {}
    check.ok(isinstance(seller.get("id"), int), f"{site}: details without seller id")

    print(f"== {site}: get_seller_profile / list_seller_listings")
    profile = await call(client, "get_seller_profile", {"seller_id": seller["id"], "site": site})
    check.ok("phone_number_verified" in profile, f"{site}: seller profile shape changed")
    args = {"seller_id": seller["id"], "site": site, "limit": 3}
    mine = await call(client, "list_seller_listings", args)
    check.ok(mine["returned"] >= 1, f"{site}: seller {seller['id']} has no listings")


async def probe_filters(client: Client, check: Check) -> None:
    print("== subcategory filter really applies")
    broad = await call(client, "search_listings", {"query": "", "category": "Fietsen en Brommers"})
    args = {"query": "", "subcategory": "Fietsen | Racefietsen", "limit": 1}
    narrow = await call(client, "search_listings", args)
    check.ok(
        0 < narrow["total_count"] < broad["total_count"] / 2,
        f"subcategory filter ignored: {narrow['total_count']} vs {broad['total_count']}",
    )

    print("== list_category_filters + attributes")
    filters = await call(client, "list_category_filters", {"category": "Auto's"})
    keys = {f["key"] for f in filters["filters"]}
    check.ok({"mileage", "constructionYear", "fuel"} <= keys, f"car facets changed: {sorted(keys)}")
    args = {
        "query": "",
        "category": "Auto's",
        "attributes": {"Bouwjaar": "2018-2022", "Brandstof": "Elektrisch"},
        "condition": "used",
        "limit": 2,
    }
    cars = await call(client, "search_listings", args)
    check.ok(cars["returned"] > 0, "car attribute search returned nothing")


async def probe_derived(client: Client, check: Check) -> None:
    print("== analyze_prices")
    args = {"query": "iphone 15", "exclude": ["hoesje"], "sample_size": 30}
    stats = await call(client, "analyze_prices", args)
    plausible = stats["sample_size"] >= 5 and stats.get("median", 0) > 50
    check.ok(plausible, f"price stats look wrong: {stats}")

    print("== check_new_listings")
    new = await call(client, "check_new_listings", {"query": "fiets", "limit": 5})
    check.ok(new["new_count"] > 0, "no new 'fiets' listings in 24h (promo padding regression?)")
    clean = all("is_sponsored" not in item for item in new["listings"])
    check.ok(clean, "promoted ads leaked into monitoring")


async def call(client: Client, tool: str, args: dict[str, Any]) -> dict[str, Any]:
    result = await client.call_tool(tool, args)
    assert result.structured_content is not None, f"{tool} returned no data"
    return dict(result.structured_content)


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
