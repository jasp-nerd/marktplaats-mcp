"""Extract listing details from the server-rendered listing page.

The page embeds the full listing payload as JSON assigned to
``window.__CONFIG__`` (pattern from gjoris/marktplaats-2dehands-mcp, MIT),
which avoids fragile HTML scraping.
"""

from __future__ import annotations

import json
import re
from typing import Any

from .models import ListingDetails, Seller
from .parsing import format_price
from .sites import Site

_CONFIG_RE = re.compile(r"window\.__CONFIG__\s*=\s*(\{.*?\});</script>", re.DOTALL)
_DESCRIPTION_RE = re.compile(r'data-collapsable="description"[^>]*>(.*?)</div>', re.DOTALL)
_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_BLANK_LINES_RE = re.compile(r"\n{3,}")


class ListingNotFoundError(Exception):
    """The page did not contain a parseable listing payload."""


def parse_listing_page(html: str, item_id: str, site: Site) -> ListingDetails:
    match = _CONFIG_RE.search(html)
    if not match:
        raise ListingNotFoundError(f"Listing {item_id} not found on {site.key}.")
    try:
        config = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ListingNotFoundError(f"Listing {item_id}: invalid embedded payload.") from exc
    listing = config.get("listing")
    if not isinstance(listing, dict):
        raise ListingNotFoundError(f"Listing {item_id} not found on {site.key}.")

    details = ListingDetails(
        id=item_id,
        site=site.key,
        url=site.listing_url(item_id),
        title=listing.get("title"),
        price=format_price(listing.get("priceInfo")),
    )

    details.description = _extract_description(listing, html)

    stats = listing.get("stats") or {}
    details.view_count = _as_int(stats.get("viewCount"))
    details.favorited_count = _as_int(stats.get("favoritedCount"))
    since = stats.get("since")
    if isinstance(since, str):
        details.since = since

    seller = listing.get("seller") or {}
    if seller:
        details.seller = Seller(
            id=_as_int(seller.get("id")),
            name=seller.get("name"),
            is_verified=seller.get("isVerified"),
        )
        seller_location = seller.get("location") or {}
        details.city = seller_location.get("cityName")

    gallery = listing.get("gallery") or {}
    urls = [
        f"https:{url}" if url.startswith("//") else url
        for url in gallery.get("imageUrls") or []
        if isinstance(url, str)
    ]
    details.image_urls = urls or None

    attributes: dict[str, str] = {}
    for attribute in listing.get("attributes") or []:
        if isinstance(attribute, dict):
            key = attribute.get("key") or attribute.get("label")
            value = attribute.get("value")
            if isinstance(key, str) and value is not None:
                attributes[key] = str(value)
    details.attributes = attributes or None
    return details


def _extract_description(listing: dict[str, Any], html: str) -> str | None:
    description = listing.get("description")
    if isinstance(description, str) and description.strip():
        return _strip_html(description)
    match = _DESCRIPTION_RE.search(html)
    if match:
        return _strip_html(match.group(1))
    return None


def _strip_html(fragment: str) -> str:
    text = _BR_RE.sub("\n", fragment)
    text = _TAG_RE.sub("", text)
    text = _BLANK_LINES_RE.sub("\n\n", text)
    return text.strip()


def _as_int(value: Any) -> int | None:
    return value if isinstance(value, int) else None
