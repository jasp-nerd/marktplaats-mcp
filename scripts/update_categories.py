# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.32", "beautifulsoup4>=4.12"]
# ///
"""Refresh the vendored category JSON by scraping marktplaats.nl.

Approach adapted from jensjeflensje/marktplaats-py (MIT), see
THIRD_PARTY_NOTICES.md. Run with: uv run scripts/update_categories.py
"""

from __future__ import annotations

import json
from pathlib import Path
from string import ascii_lowercase

import requests
from bs4 import BeautifulSoup, Tag

DATA_DIR = Path(__file__).parent.parent / "src" / "marktplaats_mcp" / "data"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
}


def parse(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_l1() -> dict[str, dict[str, object]]:
    print("Finding L1 categories...", flush=True)
    l1: dict[str, dict[str, object]] = {}
    soup = parse("https://www.marktplaats.nl/")
    ul = soup.find("ul", {"class": "CategoriesBlock-list"})
    assert isinstance(ul, Tag), "homepage category block not found"
    for li in ul.children:
        assert isinstance(li, Tag)
        a = next(iter(li.children))
        assert isinstance(a, Tag)
        href = a["href"]
        assert isinstance(href, str)
        _, _, id_, _ = href.split("/", 3)
        l1[a.text.lower()] = {"id": int(id_), "name": a.text}
    print(f"Found {len(l1)} L1 categories")
    return l1


def scrape_l2(l1: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    l2: dict[str, dict[str, object]] = {}
    for entry in l1.values():
        name = entry["name"]
        assert isinstance(name, str)
        stub = name.lower().replace(" | ", "-").replace(" ", "-").replace("'", "-")
        stub = "".join(c for c in stub if c in ascii_lowercase + "-")
        soup = parse(f"https://www.marktplaats.nl/l/{stub}/")
        data_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        assert isinstance(data_tag, Tag), f"__NEXT_DATA__ missing for {name}"
        data = json.loads(data_tag.text)
        options = data["props"]["pageProps"]["searchRequestAndResponse"]["searchCategoryOptions"]
        found = 0
        for cat in options:
            if cat["id"] == entry["id"]:
                continue
            l2[cat["fullName"].lower()] = {
                "id": cat["id"],
                "name": cat["fullName"],
                "parent": name,
            }
            found += 1
        print(f"{name}: {found} subcategories")
        if found == 0:
            raise RuntimeError(f"Found no L2 categories for {name}")
    print(f"Found {len(l2)} L2 categories in total")
    return l2


def main() -> None:
    l1 = scrape_l1()
    l2 = scrape_l2(l1)
    (DATA_DIR / "l1_categories.json").write_text(
        json.dumps(l1, ensure_ascii=False), encoding="utf-8"
    )
    (DATA_DIR / "l2_categories.json").write_text(
        json.dumps(l2, ensure_ascii=False), encoding="utf-8"
    )
    print("Category data written")


if __name__ == "__main__":
    main()
