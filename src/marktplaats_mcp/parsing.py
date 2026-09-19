"""Parse raw API listing objects into models; price and date normalisation;
promotion filtering."""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
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

DESCRIPTION_LIMIT = 300
IMAGE_LIMIT = 5

# The image CDN leaves a literal "#" size placeholder in some URLs; "85" is
# the extra-large rendition the site itself uses on listing pages.
_IMAGE_PLACEHOLDER = "$_#."
_IMAGE_SIZE = "$_85."

DUTCH_MONTHS = {
    "jan": 1,
    "feb": 2,
    "mrt": 3,
    "apr": 4,
    "mei": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "okt": 10,
    "nov": 11,
    "dec": 12,
}
_DUTCH_DATE_RE = re.compile(r"^(\d{1,2})\s+([a-z]{3})\.?\s+'?(\d{2}|\d{4})$")
_RELATIVE_DAYS = {"vandaag": 0, "gisteren": 1, "eergisteren": 2}


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


def price_euros(cents: Any) -> float | None:
    return cents / 100 if isinstance(cents, int) and cents > 0 else None


def is_promoted(raw: dict[str, Any]) -> bool:
    """Paid placements (DAGTOPPER, TOPADVERTENTIE, ...) carry a priorityProduct."""
    return raw.get("priorityProduct") not in (None, "NONE")


def is_business_listing(item_id: str) -> bool:
    """Admarkt (professional seller) ads have 'a'-prefixed ids; consumer ads 'm'."""
    return item_id.startswith("a")


def normalize_image_url(url: str) -> str:
    if url.startswith("//"):
        url = f"https:{url}"
    return url.replace(_IMAGE_PLACEHOLDER, _IMAGE_SIZE)


def image_urls(raw: dict[str, Any]) -> list[str]:
    urls = [normalize_image_url(url) for url in raw.get("imageUrls") or [] if isinstance(url, str)]
    if not urls:
        for picture in raw.get("pictures") or []:
            medium = picture.get("mediumUrl") if isinstance(picture, dict) else None
            if isinstance(medium, str):
                urls.append(normalize_image_url(medium))
    return urls


def listing_attributes(raw: dict[str, Any]) -> dict[str, str]:
    """Merge ``attributes`` (condition, delivery) with the category-specific
    ``extendedAttributes`` (brand, storage, frame height, ...)."""
    result: dict[str, str] = {}
    for attribute in list(raw.get("attributes") or []) + list(raw.get("extendedAttributes") or []):
        if not isinstance(attribute, dict):
            continue
        key = attribute.get("key")
        value = attribute.get("value")
        if value is None and attribute.get("values"):
            value = ", ".join(str(v) for v in attribute["values"])
        if isinstance(key, str) and value is not None:
            result.setdefault(key, str(value))
    return result


def parse_listing_date(value: Any, today: date | None = None) -> str | None:
    """Normalise the site's Dutch relative/short dates ('Vandaag', '3 jul 26')
    and ISO timestamps to an ISO date string, so agents can compare them."""
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().lower()
    today = today or datetime.now(timezone.utc).date()
    if text in _RELATIVE_DAYS:
        return (today - timedelta(days=_RELATIVE_DAYS[text])).isoformat()
    match = _DUTCH_DATE_RE.match(text)
    if match:
        day, month_name, year = match.groups()
        month = DUTCH_MONTHS.get(month_name)
        if month:
            year_number = int(year) + (2000 if len(year) == 2 else 0)
            try:
                return date(year_number, month, int(day)).isoformat()
            except ValueError:
                return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


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
    item_id = str(raw.get("itemId", ""))
    vip_url = raw.get("vipUrl")
    url = f"{site.base_url}{vip_url}" if vip_url else site.listing_url(item_id)
    location = raw.get("location") or {}
    distance = location.get("distanceMeters")
    distance_km = (
        round(distance / 1000, 1)
        if isinstance(distance, int) and 0 < distance < 1_000_000
        else None
    )
    price_info = raw.get("priceInfo") or {}

    listing = Listing(
        id=item_id,
        title=str(raw.get("title", "")),
        price=format_price(price_info),
        price_euros=price_euros(price_info.get("priceCents")),
        url=url,
        listed=parse_listing_date(raw.get("date")) or raw.get("date"),
        city=location.get("cityName"),
        distance_km=distance_km,
        reserved=True if raw.get("reserved") else None,
        is_business=True if is_business_listing(item_id) else None,
    )
    if sponsored or is_promoted(raw):
        listing.is_sponsored = True
    if compact:
        return listing

    description = raw.get("categorySpecificDescription") or raw.get("description")
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
    listing.image_urls = image_urls(raw)[:IMAGE_LIMIT] or None
    listing.attributes = listing_attributes(raw) or None
    listing.category_id = raw.get("categoryId")
    return listing


def matches_exclusions(raw: dict[str, Any], exclude: list[str]) -> bool:
    """True when any excluded term occurs in the title or description."""
    if not exclude:
        return False
    haystack = " ".join(
        str(raw.get(field) or "")
        for field in ("title", "description", "categorySpecificDescription")
    ).lower()
    return any(term.strip().lower() in haystack for term in exclude if term.strip())
