"""Filter discovery and label→id resolution against recorded facets."""

import pytest

from marktplaats_mcp.facets import parse_facets, resolve_attributes


def test_parse_bike_facets_exposes_labels_and_counts(facets_bikes):
    filters = {f.key: f for f in parse_facets(facets_bikes)}
    # internal/dedicated facets are hidden
    assert "PriceCents" not in filters
    assert "RelevantCategories" not in filters
    assert "offeredSince" not in filters
    brand = filters["brand"]
    assert brand.label == "Merk"
    assert brand.type == "choice"
    assert all(option.id > 0 and option.label for option in brand.options)
    assert any(option.count for option in brand.options)
    assert filters["delivery"].options[0].label in {"Ophalen", "Verzenden"}


def test_parse_car_facets_has_ranges_and_vertical_condition_ids(facets_cars):
    filters = {f.key: f for f in parse_facets(facets_cars)}
    mileage = filters["mileage"]
    assert mileage.type == "range"
    assert mileage.label == "Kilometerstand"
    assert mileage.unit == "km"
    assert mileage.min == 0
    assert mileage.max is not None
    assert mileage.max > 100_000
    used = next(o for o in filters["condition"].options if o.label == "Gebruikt")
    assert used.id == 14049  # not the generic 32


def test_resolve_by_label_or_key_case_insensitively(facets_bikes):
    filters = parse_facets(facets_bikes)
    ids, ranges = resolve_attributes(filters, {"merk": "batavus", "Levering": "Verzenden"})
    assert ids == [3408, 34]
    assert ranges == {}


def test_resolve_multiple_values_and_numeric_ids(facets_bikes):
    filters = parse_facets(facets_bikes)
    ids, _ = resolve_attributes(filters, {"brand": ["Batavus", "3408"]})
    assert ids == [3408, 3408]


def test_resolve_ranges(facets_cars):
    filters = parse_facets(facets_cars)
    _, ranges = resolve_attributes(
        filters,
        {"Bouwjaar": "2018-2022", "Kilometerstand": "-100.000", "constructionYear": "2015-"},
    )
    assert ranges["mileage"] == (None, 100000)
    assert ranges["constructionYear"] == (2015, None)


def test_unknown_filter_lists_available_ones(facets_bikes):
    with pytest.raises(ValueError, match=r"Available filters: .*Merk \(brand\)"):
        resolve_attributes(parse_facets(facets_bikes), {"kleur": "rood"})


def test_unknown_value_lists_valid_values(facets_bikes):
    with pytest.raises(ValueError, match=r"Valid: .*Batavus"):
        resolve_attributes(parse_facets(facets_bikes), {"Merk": "Bianchi"})


def test_bad_range_syntax(facets_cars):
    with pytest.raises(ValueError, match="min-max"):
        resolve_attributes(parse_facets(facets_cars), {"mileage": "lots"})
