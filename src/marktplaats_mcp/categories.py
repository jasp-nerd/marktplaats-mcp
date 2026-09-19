"""Category lookup backed by JSON vendored from jensjeflensje/marktplaats-py (MIT).

The data is refreshed by the scheduled update-categories workflow. IDs come
from marktplaats.nl; 2dehands.be shares the same category tree.
"""

from __future__ import annotations

import json
from functools import cache
from importlib import resources
from typing import Any


@cache
def _load(name: str) -> dict[str, dict[str, Any]]:
    path = resources.files("marktplaats_mcp.data").joinpath(name)
    data: dict[str, dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    return data


def l1_categories() -> list[dict[str, Any]]:
    return [
        {"id": entry["id"], "name": entry["name"]} for entry in _load("l1_categories.json").values()
    ]


def l2_categories(parent: str | int | None = None) -> list[dict[str, Any]]:
    parent_name: str | None = None
    if parent is not None:
        parent_name = _find_l1(parent)["name"]
    return [
        {"id": entry["id"], "name": entry["name"], "parent": entry["parent"]}
        for entry in _load("l2_categories.json").values()
        if parent_name is None or entry["parent"] == parent_name
    ]


def resolve_category_ids(
    category: str | int | None,
    subcategory: str | int | None,
) -> tuple[int | None, list[int]]:
    """Resolve category/subcategory (name or numeric id) to (l1CategoryId, [l2CategoryIds]).

    The API requires the parent id alongside a subcategory, so a subcategory
    given on its own resolves its parent from the vendored tree.
    """
    l2_entry = _find_l2(subcategory) if subcategory is not None else None
    l1_id = _find_l1(category)["id"] if category is not None else None
    if l2_entry is not None:
        parent_id = _find_l1(l2_entry["parent"])["id"]
        if l1_id is not None and l1_id != parent_id:
            raise ValueError(
                f"Subcategory {l2_entry['name']!r} belongs to {l2_entry['parent']!r}, "
                f"not to category {category!r}."
            )
        l1_id = parent_id
    return l1_id, [l2_entry["id"]] if l2_entry else []


def category_names(l1_id: int | None, l2_ids: list[int]) -> tuple[str | None, str | None]:
    l1_name = next(
        (e["name"] for e in _load("l1_categories.json").values() if e["id"] == l1_id), None
    )
    l2_name = next(
        (
            e["name"]
            for e in _load("l2_categories.json").values()
            if l2_ids and e["id"] == l2_ids[0]
        ),
        None,
    )
    return l1_name, l2_name


def _find_l1(ref: str | int) -> dict[str, Any]:
    table = _load("l1_categories.json")
    if _is_int(ref):
        for entry in table.values():
            if entry["id"] == int(ref):
                return entry
    else:
        found = table.get(str(ref).strip().lower())
        if found:
            return found
    raise ValueError(f"Unknown category {ref!r}. Use list_categories to see valid names and ids.")


def _find_l2(ref: str | int) -> dict[str, Any]:
    table = _load("l2_categories.json")
    if _is_int(ref):
        for entry in table.values():
            if entry["id"] == int(ref):
                return entry
    else:
        needle = str(ref).strip().lower()
        if needle in table:
            return table[needle]
        # Keys look like "antiek | bestek"; also accept just "bestek".
        matches = [entry for key, entry in table.items() if key.split("|")[-1].strip() == needle]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            names = ", ".join(m["name"] for m in matches[:5])
            raise ValueError(f"Ambiguous subcategory {ref!r}; matches: {names}. Use an id.")
    raise ValueError(
        f"Unknown subcategory {ref!r}. Use list_categories with a parent to see valid names."
    )


def _is_int(ref: str | int) -> bool:
    if isinstance(ref, int):
        return True
    return ref.strip().lstrip("-").isdigit()
