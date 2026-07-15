"""Parse raw API listing objects into models; price formatting; promo filtering."""

from __future__ import annotations

from typing import Any

from .models import Listing, Seller
from .sites import Site

# priceType values observed on the API, with the labels the sites display.
PRICE_TYPE_LABELS = {
    "FIXED": "",
    "FAST_BID": "Bieden",
    "MIN_BID": "Bieden vanaf",
    "FREE": "Gratis",
    "RESERVED": "Gereserveerd",
    "EXCHANGE": "Ruilen",
    "NOTK": "Prijs op aanvraag (n.o.t.k.)",
    "ON_REQUEST": "Op aanvraag",
    "SEE_DESCRIPTION": "Zie omschrijving",
}

# priorityProduct values that mark paid promotions (stable noise on page 1
# of date-sorted results).
PROMOTED_PRIORITY = {"DAGTOPPER", "TOPADVERTENTIE"}

DESCRIPTION_LIMIT = 300


def format_price(price_info: dict[str, Any] | None) -> str:
    """Human/LLM-readable price string, e.g. '€ 12,50', 'Bieden vanaf € 10,00', 'Gratis'."""
    if not price_info:
        return "Onbekend"
    price_type = price_info.get("priceType") or "UNKNOWN"
    cents = price_info.get("priceCents")
    label = PRICE_TYPE_LABELS.get(price_type, price_type.title())
    amount = format_cents(cents) if isinstance(cents, int) and cents > 0 else None
    if amount and label:
        return f"{label} {amount}"
    if amount:
        return amount
    return label or "Onbekend"


def format_cents(cents: int) -> str:
    euros = cents // 100
    rest = cents % 100
    grouped = f"{euros:,}".replace(",", ".")
    return f"€ {grouped},{rest:02d}"


def is_promoted(raw: dict[str, Any]) -> bool:
    return raw.get("priorityProduct") in PROMOTED_PRIORITY


def image_urls(raw: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    for url in raw.get("imageUrls") or []:
        if isinstance(url, str):
            urls.append(f"https:{url}" if url.startswith("//") else url)
    if not urls:
        for picture in raw.get("pictures") or []:
            medium = picture.get("mediumUrl") if isinstance(picture, dict) else None
            if isinstance(medium, str):
                urls.append(medium)
    return urls


def listing_attributes(raw: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for attribute in raw.get("attributes") or []:
        if not isinstance(attribute, dict):
            continue
        key = attribute.get("key")
        value = attribute.get("value")
        if value is None and attribute.get("values"):
            value = ", ".join(str(v) for v in attribute["values"])
        if isinstance(key, str) and value is not None:
            result[key] = str(value)
    return result


def parse_listing(
    raw: dict[str, Any],
    site: Site,
    compact: bool = True,
    sponsored: bool = False,
) -> Listing:
    """Map one raw search-result listing onto the Listing model.

    Compact mode keeps the fields an agent needs to shortlist results
    (roughly 75% fewer tokens); full mode adds description, seller,
    images and attributes.
    """
    vip_url = raw.get("vipUrl")
    url = f"{site.base_url}{vip_url}" if vip_url else site.listing_url(str(raw.get("itemId")))
    location = raw.get("location") or {}
    distance = location.get("distanceMeters")
    distance_km = (
        round(distance / 1000, 1)
        if isinstance(distance, int) and 0 < distance < 1_000_000
        else None
    )

    listing = Listing(
        id=str(raw.get("itemId", "")),
        title=str(raw.get("title", "")),
        price=format_price(raw.get("priceInfo")),
        url=url,
        listed=raw.get("date"),
        city=location.get("cityName"),
        distance_km=distance_km,
    )
    if sponsored or is_promoted(raw):
        listing.is_sponsored = True
    if compact:
        return listing

    description = raw.get("description")
    if isinstance(description, str) and description:
        listing.description = (
            description[:DESCRIPTION_LIMIT] + "…"
            if len(description) > DESCRIPTION_LIMIT
            else description
        )
    seller_info = raw.get("sellerInformation") or {}
    if seller_info:
        listing.seller = Seller(
            id=seller_info.get("sellerId"),
            name=seller_info.get("sellerName"),
            is_verified=seller_info.get("isVerified"),
        )
    listing.image_urls = image_urls(raw) or None
    listing.attributes = listing_attributes(raw) or None
    listing.category_id = raw.get("categoryId")
    return listing
