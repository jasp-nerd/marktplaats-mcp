# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.32", "beautifulsoup4>=4.12"]
# ///
"""Refresh the vendored category JSON from marktplaats.nl.

Top-level categories come from the homepage's /cp/<id>/<slug>/ links (no CSS
class names, which change with every redesign); subcategories come from the
same JSON search API the server uses. Originally adapted from
jensjeflensje/marktplaats-py (MIT), see THIRD_PARTY_NOTICES.md.
Run with: uv run scripts/update_categories.py
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).parent.parent / "src" / "marktplaats_mcp" / "data"
SEARCH_URL = "https://www.marktplaats.nl/lrp/api/search"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
}
L1_HREF = re.compile(r"^/cp/(\d+)/[^/]+/?$")


def get(url: str, **params: str) -> requests.Response:
    for attempt in range(3):
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if response.status_code < 500 and response.status_code != 429:
            response.raise_for_status()
            return response
        time.sleep(5 * (attempt + 1))
    response.raise_for_status()
    return response


def scrape_l1_ids() -> list[int]:
    print("Finding L1 categories...", flush=True)
    soup = BeautifulSoup(get("https://www.marktplaats.nl/").text, "html.parser")
    ids: list[int] = []
    for a in soup.find_all("a", href=L1_HREF):
        match = L1_HREF.match(str(a["href"]))
        if match and int(match.group(1)) not in ids:
            ids.append(int(match.group(1)))
    print(f"Found {len(ids)} L1 categories")
    if len(ids) < 20:
        raise RuntimeError(f"Only {len(ids)} L1 categories on the homepage; layout changed?")
    return ids


def scrape(l1_ids: list[int]) -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    """Each L1 search lists the category itself plus its subcategories."""
    l1: dict[str, dict[str, object]] = {}
    l2: dict[str, dict[str, object]] = {}
    for l1_id in l1_ids:
        data = get(SEARCH_URL, l1CategoryId=str(l1_id), limit="1", offset="0").json()
        options = data.get("searchCategoryOptions") or []
        own = next((cat for cat in options if cat["id"] == l1_id), None)
        if own is None:
            raise RuntimeError(f"Category {l1_id} missing from its own search options")
        name = own["fullName"]
        l1[name.lower()] = {"id": l1_id, "name": name}
        children = [cat for cat in options if cat.get("parentId") == l1_id]
        for cat in children:
            l2[cat["fullName"].lower()] = {"id": cat["id"], "name": cat["fullName"], "parent": name}
        print(f"{name}: {len(children)} subcategories")
        if not children:
            raise RuntimeError(f"Found no L2 categories for {name}")
        time.sleep(0.5)
    print(f"Found {len(l2)} L2 categories in total")
    return l1, l2


def main() -> None:
    l1, l2 = scrape(scrape_l1_ids())
    (DATA_DIR / "l1_categories.json").write_text(
        json.dumps(l1, ensure_ascii=False), encoding="utf-8"
    )
    (DATA_DIR / "l2_categories.json").write_text(
        json.dumps(l2, ensure_ascii=False), encoding="utf-8"
    )
    print("Category data written")


if __name__ == "__main__":
    main()
