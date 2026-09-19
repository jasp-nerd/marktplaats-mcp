"""Category-specific search filters, discovered live from the API's facets.

Every search response carries a ``facets`` array describing the filters the
site would show for that query/category (brand, frame height, mileage, ...)
with the value ids the API expects. Filters are per category, and even generic
ones differ between verticals (a used car is condition 14049, a used bike 32),
so we resolve human labels against the live facets instead of hardcoding ids.
"""

from __future__ import annotations

import re
import time
from typing import Any

from .client import Range
from .models import FilterOption, SearchFilter

FACET_TTL_SECONDS = 3600
# Facets that are exposed through dedicated tool parameters or are internal.
HIDDEN_FACETS = {"PriceCents", "RelevantCategories", "offeredSince", "Language"}

_RANGE_RE = re.compile(r"^\s*(\d[\d.\s]*)?\s*[-:]\s*(\d[\d.\s]*)?\s*$")


def parse_facets(data: dict[str, Any]) -> list[SearchFilter]:
    """Turn the raw ``facets`` array into a compact, label-first description."""
    filters: list[SearchFilter] = []
    for facet in data.get("facets") or []:
        if not isinstance(facet, dict):
            continue
        key = facet.get("key")
        if not isinstance(key, str) or key in HIDDEN_FACETS:
            continue
        label = facet.get("label") or key
        facet_type = facet.get("type")
        if facet_type == "AttributeGroupFacet":
            options = [
                FilterOption(
                    label=str(group["attributeValueLabel"]),
                    id=int(group["attributeValueId"]),
                    count=group.get("histogramCount"),
                )
                for group in facet.get("attributeGroup") or []
                if isinstance(group, dict)
                and group.get("attributeValueId") is not None
                and group.get("attributeValueLabel")
            ]
            if options:
                filters.append(
                    SearchFilter(key=key, label=str(label), type="choice", options=options)
                )
        elif facet_type == "AttributeRangeFacet":
            values = [
                option["value"]
                for option in (facet.get("options") or {}).get("from") or []
                if isinstance(option, dict) and isinstance(option.get("value"), int)
            ]
            filters.append(
                SearchFilter(
                    key=key,
                    label=str(label),
                    type="range",
                    min=min(values) if values else None,
                    max=max(values) if values else None,
                    unit=_unit_from_options(facet),
                )
            )
    return filters


def _unit_from_options(facet: dict[str, Any]) -> str | None:
    options = (facet.get("options") or {}).get("from") or []
    for option in options:
        label = option.get("label") if isinstance(option, dict) else None
        value = option.get("value") if isinstance(option, dict) else None
        if isinstance(label, str) and value:
            unit = label.replace(".", "").replace(",", "").lstrip("0123456789 ").strip()
            return unit or None
    return None


def resolve_attributes(
    filters: list[SearchFilter],
    attributes: dict[str, str | list[str]],
) -> tuple[list[int], dict[str, Range]]:
    """Map ``{filter: value}`` (labels or keys, case-insensitive) onto the API's
    numeric ids and ranges. Raises ValueError with the valid choices on a miss."""
    by_name = {f.key.lower(): f for f in filters} | {f.label.lower(): f for f in filters}
    ids: list[int] = []
    ranges: dict[str, Range] = {}
    for name, raw_value in attributes.items():
        search_filter = by_name.get(name.strip().lower())
        if search_filter is None:
            valid = ", ".join(f"{f.label} ({f.key})" for f in filters) or "none for this search"
            raise ValueError(f"Unknown filter {name!r}. Available filters: {valid}.")
        values = raw_value if isinstance(raw_value, list) else [raw_value]
        if search_filter.type == "range":
            if len(values) != 1:
                raise ValueError(f"Filter {name!r} takes one range like '2018-2022'.")
            ranges[search_filter.key] = _parse_range(name, values[0])
            continue
        for value in values:
            ids.append(_match_option(search_filter, str(value)))
    return ids, ranges


def _match_option(search_filter: SearchFilter, value: str) -> int:
    needle = value.strip().lower()
    for option in search_filter.options:
        if option.label.lower() == needle or str(option.id) == needle:
            return option.id
    valid = ", ".join(option.label for option in search_filter.options)
    raise ValueError(f"Unknown value {value!r} for filter {search_filter.label!r}. Valid: {valid}.")


def _parse_range(name: str, value: str) -> Range:
    match = _RANGE_RE.match(value)
    if not match or not (match.group(1) or match.group(2)):
        raise ValueError(
            f"Filter {name!r} is a range; write it as 'min-max', 'min-' or '-max' "
            "(e.g. '2018-2022')."
        )
    lower, upper = (_to_int(group) for group in match.groups())
    return lower, upper


def _to_int(text: str | None) -> int | None:
    if text is None:
        return None
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None


class FacetCache:
    """Facets change rarely; keep them for an hour per (site, category, query)."""

    def __init__(self, ttl: float = FACET_TTL_SECONDS) -> None:
        self.ttl = ttl
        self._entries: dict[Any, tuple[float, list[SearchFilter]]] = {}

    def get(self, key: Any) -> list[SearchFilter] | None:
        entry = self._entries.get(key)
        if entry and entry[0] > time.monotonic():
            return entry[1]
        self._entries.pop(key, None)
        return None

    def put(self, key: Any, filters: list[SearchFilter]) -> None:
        self._entries[key] = (time.monotonic() + self.ttl, filters)

    def clear(self) -> None:
        self._entries.clear()
