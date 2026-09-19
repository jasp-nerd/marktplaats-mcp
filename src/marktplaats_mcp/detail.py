"""Build ListingDetails from the app's JSON listing endpoint, with the
server-rendered listing page (``window.__CONFIG__``, pattern from
gjoris/marktplaats-2dehands-mcp, MIT) as a fallback."""

from __future__ import annotations

import html
import json
import re
from typing import Any

from .models import Bidding, ListingDetails, Seller, SellerDetails
from .parsing import IMAGE_LIMIT, format_price, normalize_image_url, price_euros
from .sites import Site

_CONFIG_RE = re.compile(r"window\.__CONFIG__\s*=\s*(\{.*?\});</script>", re.DOTALL)
_DESCRIPTION_RE = re.compile(r'data-collapsable="description"[^>]*>(.*?)</div>', re.DOTALL)
_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_BLANK_LINES_RE = re.compile(r"\n{3,}")


class ListingNotFoundError(Exception):
    """The listing does not exist (any more)."""


def parse_listing_payload(
    payload: dict[str, Any], item_id: str, site: Site, max_images: int = IMAGE_LIMIT
) -> ListingDetails:
    """Map the ``/app/vip/v4/item/{id}`` payload onto ListingDetails."""
    core = payload.get("adCore")
    if not isinstance(core, dict):
        raise ListingNotFoundError(f"Listing {item_id} not found on {site.key}.")
    price = core.get("price") or {}
    meta = payload.get("metaData") or {}
    address = core.get("adAddress") or {}
    flags = payload.get("flags") or {}

    details = ListingDetails(
        id=item_id,
        site=site.key,
        url=core.get("link") or site.listing_url(item_id),
        title=core.get("title"),
        description=_strip_html(core["description"])
        if isinstance(core.get("description"), str)
        else None,
        price=format_price(_as_price_info(price)),
        price_euros=price_euros(price.get("priceAmount")),
        price_type=price.get("priceType"),
        status=meta.get("adStatus"),
        listed_at=meta.get("startDateTime"),
        category_id=core.get("categoryId"),
        city=address.get("city"),
        postcode=address.get("zipCode"),
        country=address.get("countryAbbreviation"),
        view_count=_as_int(meta.get("viewAdCount")),
        favorited_count=_as_int(meta.get("adFavoritedCount")),
        reserved=True if flags.get("reserved") else None,
        shippable=flags.get("shippable") if isinstance(flags.get("shippable"), bool) else None,
        buy_it_now=True if flags.get("buyItNowEnabled") else None,
    )

    if flags.get("allowBids"):
        bids = payload.get("bids") or []
        amounts = [
            bid.get("amount") or bid.get("bidAmountCents") or bid.get("priceCents")
            for bid in bids
            if isinstance(bid, dict)
        ]
        cents = [amount for amount in amounts if isinstance(amount, int)]
        details.bidding = Bidding(
            enabled=True,
            minimum_bid_euros=price_euros(payload.get("currentMinimumBid")),
            bids_count=len(bids) if bids else None,
            highest_bid_euros=price_euros(max(cents)) if cents else None,
        )

    attributes: dict[str, str] = {}
    for attribute in core.get("attributes") or []:
        if not isinstance(attribute, dict):
            continue
        name = attribute.get("name") or attribute.get("key")
        values = [
            str(v.get("name") if isinstance(v, dict) else v)
            for v in attribute.get("values") or []
            if v is not None
        ]
        if isinstance(name, str) and values:
            attributes[name] = ", ".join(values)
    details.attributes = attributes or None

    car_attributes: dict[str, str] = {}
    for group in core.get("carAttributes") or []:
        for attribute in (group.get("attributes") or []) if isinstance(group, dict) else []:
            if not isinstance(attribute, dict):
                continue
            label = attribute.get("label") or attribute.get("key")
            value = attribute.get("value")
            if isinstance(label, str) and value not in (None, ""):
                unit = attribute.get("unit")
                car_attributes[label] = f"{value} {unit}".strip() if unit else str(value)
    details.car_attributes = car_attributes or None

    pictures = [p for p in core.get("pictures") or [] if isinstance(p, dict)]
    urls = [
        normalize_image_url(url)
        for url in (p.get("large") or p.get("medium") or p.get("extraExtraLarge") for p in pictures)
        if isinstance(url, str)
    ]
    details.image_count = len(urls) or None
    details.image_urls = urls[:max_images] or None

    seller = payload.get("sellerInformation") or {}
    if seller:
        reviews = seller.get("reviewSummary") or {}
        response = seller.get("responseData") or {}
        active_since = seller.get("activeSince") or {}
        details.seller = SellerDetails(
            id=_as_int(seller.get("id")),
            name=seller.get("name"),
            type=seller.get("type"),
            active_since=_date_part(active_since.get("timestamp")),
            response_rate_percent=_as_int(response.get("rate")),
            response_label=response.get("label"),
            average_score=reviews.get("averageScore")
            if isinstance(reviews.get("averageScore"), (int, float))
            else None,
            number_of_reviews=_as_int(reviews.get("numberOfReviews")),
            listings_count=_as_int(seller.get("totalAmountOfListings")),
        )
    return details


def parse_listing_page(
    html: str, item_id: str, site: Site, max_images: int = IMAGE_LIMIT
) -> ListingDetails:
    """Fallback: extract the listing from the server-rendered page."""
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

    price_info = listing.get("priceInfo") or {}
    details = ListingDetails(
        id=item_id,
        site=site.key,
        url=site.listing_url(item_id),
        title=listing.get("title"),
        price=format_price(price_info),
        price_euros=price_euros(price_info.get("priceCents")),
        price_type=price_info.get("priceType"),
        reserved=True if listing.get("isReserved") else None,
    )
    details.description = _extract_description(listing, html)

    stats = listing.get("stats") or {}
    details.view_count = _as_int(stats.get("viewCount"))
    details.favorited_count = _as_int(stats.get("favoritedCount"))
    since = stats.get("since")
    if isinstance(since, str):
        details.since = since
        details.listed_at = since

    bids_info = listing.get("bidsInfo") or {}
    if bids_info.get("isBiddingEnabled"):
        details.bidding = Bidding(
            enabled=True,
            minimum_bid_euros=price_euros(bids_info.get("currentMinimumBid")),
            bids_count=len(bids_info.get("bids") or []) or None,
        )

    seller = listing.get("seller") or {}
    if seller:
        details.seller = Seller(id=_as_int(seller.get("id")), name=seller.get("name"))
        seller_location = seller.get("location") or {}
        details.city = seller_location.get("cityName")

    gallery = listing.get("gallery") or {}
    urls = [
        normalize_image_url(url) for url in gallery.get("imageUrls") or [] if isinstance(url, str)
    ]
    details.image_count = len(urls) or None
    details.image_urls = urls[:max_images] or None
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
    text = html.unescape(text)
    text = _BLANK_LINES_RE.sub("\n\n", text)
    return text.strip()


def _as_price_info(price: dict[str, Any]) -> dict[str, Any]:
    return {"priceType": price.get("priceType"), "priceCents": price.get("priceAmount")}


def _as_int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _date_part(value: Any) -> str | None:
    return value[:10] if isinstance(value, str) and len(value) >= 10 else None
