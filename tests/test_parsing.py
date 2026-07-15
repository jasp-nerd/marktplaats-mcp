"""Parsing tests against recorded real API payloads: if Marktplaats changes its
response shape, these are the tests that catch it."""

from marktplaats_mcp.parsing import (
    format_cents,
    format_price,
    is_promoted,
    parse_listing,
)
from marktplaats_mcp.sites import SITES

NL = SITES["marktplaats"]
BE = SITES["2dehands"]


class TestFormatPrice:
    def test_fixed_price(self):
        assert format_price({"priceType": "FIXED", "priceCents": 12550}) == "€ 125,50"

    def test_thousands_grouping_dutch_style(self):
        assert format_cents(123456789) == "€ 1.234.567,89"

    def test_bidding_without_amount(self):
        assert format_price({"priceType": "FAST_BID", "priceCents": 0}) == "Bieden"

    def test_bidding_from_amount(self):
        assert format_price({"priceType": "MIN_BID", "priceCents": 1000}) == "Bieden vanaf € 10,00"

    def test_free(self):
        assert format_price({"priceType": "FREE", "priceCents": 0}) == "Gratis"

    def test_missing_price_info(self):
        assert format_price(None) == "Onbekend"

    def test_unknown_price_type_passes_through(self):
        assert format_price({"priceType": "SOMETHING_NEW", "priceCents": 0}) == "Something_New"


class TestPromoFilter:
    def test_real_response_contains_promoted_listings(self, search_response):
        promoted = [raw for raw in search_response["listings"] if is_promoted(raw)]
        organic = [raw for raw in search_response["listings"] if not is_promoted(raw)]
        assert promoted, "fixture should contain DAGTOPPER promos"
        assert organic, "fixture should contain organic listings"
        assert all(raw["priorityProduct"] in {"DAGTOPPER", "TOPADVERTENTIE"} for raw in promoted)

    def test_none_priority_is_not_promoted(self):
        assert not is_promoted({"priorityProduct": "NONE"})
        assert not is_promoted({})


class TestParseListing:
    def test_compact_listing_from_real_payload(self, search_response):
        raw = search_response["listings"][0]
        listing = parse_listing(raw, NL, compact=True)
        assert listing.id.startswith("m")
        assert listing.title
        assert listing.price
        assert listing.url.startswith("https://www.marktplaats.nl/v/")
        assert listing.city
        # compact mode must not carry the heavy fields
        assert listing.description is None
        assert listing.image_urls is None
        assert listing.seller is None

    def test_full_listing_from_real_payload(self, search_response):
        raw = search_response["listings"][0]
        listing = parse_listing(raw, NL, compact=False)
        assert listing.seller is not None
        assert listing.seller.id
        assert listing.image_urls
        assert all(url.startswith("https://") for url in listing.image_urls)
        assert listing.category_id

    def test_negative_distance_means_no_distance(self, search_response):
        raw = search_response["listings"][0]
        assert raw["location"]["distanceMeters"] < 0  # recorded without postcode
        listing = parse_listing(raw, NL, compact=True)
        assert listing.distance_km is None

    def test_2dehands_urls_use_belgian_host(self, search_response_be):
        raw = search_response_be["listings"][0]
        listing = parse_listing(raw, BE, compact=True)
        assert "2dehands.be" in listing.url

    def test_description_is_truncated_in_full_mode(self):
        raw = {
            "itemId": "m1",
            "title": "t",
            "priceInfo": {"priceType": "FIXED", "priceCents": 100},
            "description": "x" * 500,
        }
        listing = parse_listing(raw, NL, compact=False)
        assert listing.description is not None
        assert len(listing.description) <= 301
        assert listing.description.endswith("…")

    def test_promoted_flag_set(self, search_response):
        promoted_raw = next(raw for raw in search_response["listings"] if is_promoted(raw))
        listing = parse_listing(promoted_raw, NL)
        assert listing.is_sponsored is True
