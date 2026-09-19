"""Listing-detail parsing against recorded payloads from both sources."""

import pytest

from marktplaats_mcp.detail import ListingNotFoundError, parse_listing_page, parse_listing_payload
from marktplaats_mcp.sites import SITES

NL = SITES["marktplaats"]


def test_app_payload_maps_rich_fields(listing_vip):
    details = parse_listing_payload(listing_vip, "m2444371973", NL)
    assert details.title == "Baan fiets"
    assert details.description is not None
    assert "\n" in details.description  # <br/> became newlines
    assert "<" not in details.description
    assert details.price == "Bieden vanaf € 250,00"
    assert details.price_euros == 250.0
    assert details.price_type == "MIN_BID"
    assert details.status == "ACTIVE"
    assert details.listed_at is not None
    assert details.listed_at.startswith("2026-09-19T13:01:54")
    assert details.city == "Amsterdam"
    assert details.postcode == "1057KH"
    assert details.country == "NL"
    assert details.view_count == 23
    assert details.favorited_count == 0
    assert details.shippable is True
    assert details.reserved is None
    assert details.attributes == {
        "Conditie": "Gebruikt",
        "Merk": "Overige merken",
        "Aantal versnellingen": "Minder dan 10 versnellingen",
        "Materiaal": "Aluminium",
        "Framehoogte": "57 tot 61 cm",
        "Levering": "Ophalen",
    }
    assert details.car_attributes is None
    assert details.image_count == 7
    assert details.image_urls is not None
    assert len(details.image_urls) == 5
    assert all("$_#" not in url for url in details.image_urls)
    assert details.bidding is not None
    assert details.bidding.enabled is True
    assert details.bidding.minimum_bid_euros == 150.0
    assert details.bidding.bids_count is None
    seller = details.seller
    assert seller is not None
    assert seller.id == 58924831
    assert seller.name == "Sample Seller"
    assert seller.type == "CONSUMER"
    assert seller.active_since == "2026-02-16"
    assert seller.response_rate_percent == 74
    assert seller.average_score == 5
    assert seller.number_of_reviews == 1
    assert seller.listings_count == 1


def test_html_entities_are_unescaped(listing_vip):
    payload = {
        **listing_vip,
        "adCore": {**listing_vip["adCore"], "description": "Prijs &euro; 1.500 &amp; meer<br/>ok"},
    }
    details = parse_listing_payload(payload, "m1", NL)
    assert details.description == "Prijs € 1.500 & meer\nok"


def test_long_descriptions_are_clipped(listing_vip):
    payload = {**listing_vip, "adCore": {**listing_vip["adCore"], "description": "x" * 5000}}
    details = parse_listing_payload(payload, "m1", NL)
    assert details.description is not None
    assert len(details.description) == 4001
    assert details.description.endswith("…")
    assert details.note is not None


def test_app_payload_respects_max_images(listing_vip):
    assert parse_listing_payload(listing_vip, "m1", NL, max_images=0).image_urls is None
    details = parse_listing_payload(listing_vip, "m1", NL, max_images=2)
    assert details.image_urls is not None
    assert len(details.image_urls) == 2
    assert details.image_count == 7


def test_app_payload_without_ad_core_is_not_found():
    with pytest.raises(ListingNotFoundError):
        parse_listing_payload({"code": "NOT_FOUND"}, "m1", NL)


def test_page_fallback_still_parses_recorded_page(listing_page_html):
    details = parse_listing_page(listing_page_html, "m2420210707", NL)
    assert details.title
    assert details.description
    assert details.view_count is not None
    assert details.view_count >= 0
    assert details.listed_at == details.since
    assert details.seller is not None
    assert details.seller.id
