"""Parsing tests against recorded real API payloads: if Marktplaats changes its
response shape, these are the tests that catch it."""

from datetime import date

from marktplaats_mcp.parsing import (
    format_cents,
    format_price,
    is_promoted,
    listing_attributes,
    matches_exclusions,
    normalize_image_url,
    parse_listing,
    parse_listing_date,
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

    def test_unknown_priority_products_count_as_promoted(self):
        # allowlist: anything the site marks with a priority product is a paid placement
        assert is_promoted({"priorityProduct": "OPVALLER"})


class TestListingDate:
    TODAY = date(2026, 9, 19)

    def test_relative_dutch_words(self):
        assert parse_listing_date("Vandaag", self.TODAY) == "2026-09-19"
        assert parse_listing_date("Gisteren", self.TODAY) == "2026-09-18"
        assert parse_listing_date("Eergisteren", self.TODAY) == "2026-09-17"

    def test_short_dutch_date(self):
        assert parse_listing_date("3 jul 26", self.TODAY) == "2026-07-03"
        assert parse_listing_date("17 mei 26", self.TODAY) == "2026-05-17"
        assert parse_listing_date("10 mrt. 2024", self.TODAY) == "2024-03-10"

    def test_iso_timestamp(self):
        assert parse_listing_date("2024-09-02T22:08:20Z", self.TODAY) == "2024-09-02"

    def test_garbage_is_none(self):
        assert parse_listing_date("morgen", self.TODAY) is None
        assert parse_listing_date(None, self.TODAY) is None

    def test_every_fixture_date_parses(self, search_response):
        for raw in search_response["listings"]:
            assert parse_listing_date(raw["date"], self.TODAY), raw["date"]


class TestImageUrls:
    def test_size_placeholder_is_replaced(self):
        url = "https://images.marktplaats.com/api/v1/x/images/abc?rule=ecg_mp_eps$_#.jpg"
        assert normalize_image_url(url).endswith("rule=ecg_mp_eps$_85.jpg")

    def test_protocol_relative_url_gets_https(self):
        assert (
            normalize_image_url("//images.2dehands.com/a.jpg")
            == "https://images.2dehands.com/a.jpg"
        )


class TestAttributes:
    def test_extended_attributes_are_merged(self):
        raw = {
            "attributes": [{"key": "condition", "value": "Gebruikt"}],
            "extendedAttributes": [
                {"key": "brand", "value": "Trek"},
                {"key": "condition", "value": "ignored duplicate"},
                {"key": "sizes", "values": ["S", "M"]},
            ],
        }
        assert listing_attributes(raw) == {
            "condition": "Gebruikt",
            "brand": "Trek",
            "sizes": "S, M",
        }


class TestExclusions:
    def test_matches_title_and_description_case_insensitively(self):
        raw = {"title": "iPhone 15 Hoesje", "description": "nieuw"}
        assert matches_exclusions(raw, ["hoesje"])
        assert matches_exclusions(raw, ["NIEUW"])
        assert not matches_exclusions(raw, ["defect"])
        assert not matches_exclusions(raw, [])


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

    def test_listed_is_normalised_to_iso_date(self, search_response):
        listing = parse_listing(search_response["listings"][0], NL)
        assert listing.listed == date.today().isoformat()  # fixture says "Vandaag"

    def test_price_euros_and_flags(self):
        raw = {
            "itemId": "a123",
            "title": "t",
            "priceInfo": {"priceType": "FIXED", "priceCents": 12550},
            "reserved": True,
        }
        listing = parse_listing(raw, NL)
        assert listing.price_euros == 125.5
        assert listing.reserved is True
        assert listing.is_business is True  # 'a' prefix = Admarkt business ad

    def test_bidding_without_amount_has_no_price_euros(self):
        raw = {
            "itemId": "m1",
            "title": "t",
            "priceInfo": {"priceType": "FAST_BID", "priceCents": 0},
        }
        listing = parse_listing(raw, NL)
        assert listing.price == "Bieden"
        assert listing.price_euros is None
        assert listing.reserved is None
        assert listing.is_business is None

    def test_full_mode_prefers_category_specific_description(self):
        raw = {
            "itemId": "m1",
            "title": "t",
            "priceInfo": {"priceType": "FIXED", "priceCents": 100},
            "description": "short",
            "categorySpecificDescription": "longer and better",
        }
        assert parse_listing(raw, NL, compact=False).description == "longer and better"
