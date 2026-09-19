import pytest

from marktplaats_mcp.categories import (
    category_names,
    l1_categories,
    l2_categories,
    resolve_category_ids,
)


def test_l1_categories_load_from_vendored_data():
    categories = l1_categories()
    assert len(categories) >= 30
    by_name = {category["name"]: category["id"] for category in categories}
    assert by_name["Fietsen en Brommers"] == 445
    assert by_name["Auto's"] == 91


def test_l2_categories_filtered_by_parent():
    subcategories = l2_categories("Antiek en Kunst")
    assert subcategories
    assert all(c["parent"] == "Antiek en Kunst" for c in subcategories)


def test_l2_categories_by_parent_id():
    assert l2_categories(1) == l2_categories("Antiek en Kunst")


def test_resolve_by_name_is_case_insensitive():
    l1_id, l2_ids = resolve_category_ids("fietsen EN brommers", None)
    assert l1_id == 445
    assert l2_ids == []


def test_resolve_by_numeric_id_and_numeric_string():
    assert resolve_category_ids(445, None) == (445, [])
    assert resolve_category_ids("445", None) == (445, [])


def test_resolve_subcategory_by_full_key_also_resolves_parent():
    # the API needs the parent id next to the subcategory id
    assert resolve_category_ids(None, "antiek | bestek") == (1, [2])


def test_resolve_subcategory_by_unique_suffix():
    l1_id, l2_ids = resolve_category_ids(None, "racefietsen")
    assert l1_id == 445
    assert l2_ids == [464]


def test_subcategory_under_wrong_parent_is_rejected():
    with pytest.raises(ValueError, match="belongs to"):
        resolve_category_ids("Auto's", "racefietsen")


def test_category_names_round_trip():
    assert category_names(445, [464]) == ("Fietsen en Brommers", "Fietsen | Racefietsen")
    assert category_names(None, []) == (None, None)


def test_ambiguous_subcategory_suffix_raises():
    # "bestek" exists under both Antiek and Keuken
    with pytest.raises(ValueError, match="Ambiguous"):
        resolve_category_ids(None, "bestek")


def test_unknown_category_raises_actionable_error():
    with pytest.raises(ValueError, match="list_categories"):
        resolve_category_ids("hoverboards from mars", None)


def test_unknown_subcategory_raises_actionable_error():
    with pytest.raises(ValueError, match="list_categories"):
        resolve_category_ids(None, "not-a-subcategory")
