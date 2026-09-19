import json
from pathlib import Path
from typing import Any

import pytest

from marktplaats_mcp import server

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def _fresh_caches() -> None:
    """The server's client and facet cache are process-wide singletons; never let
    one test's cached page or filters leak into the next."""
    client = server.get_client()
    client.cache.clear()
    client.min_interval = 0
    client.backoff_base = 0.001
    client.backoff_cap = 0.002
    server._facets.clear()


@pytest.fixture(scope="session")
def facets_bikes() -> dict[str, Any]:
    """Recorded search response for Fietsen | Racefietsen (facets only)."""
    return json.loads((FIXTURES / "facets_bikes.json").read_text())


@pytest.fixture(scope="session")
def facets_cars() -> dict[str, Any]:
    """Recorded facets for Auto's: range facets and car-specific condition ids."""
    return json.loads((FIXTURES / "facets_cars.json").read_text())


@pytest.fixture(scope="session")
def listing_vip() -> dict[str, Any]:
    """Recorded app/vip/v4/item payload (seller name scrubbed)."""
    return json.loads((FIXTURES / "listing_vip.json").read_text())


@pytest.fixture(scope="session")
def search_response() -> dict[str, Any]:
    """Recorded lrp/api/search response from marktplaats.nl (query 'fiets', limit 5)."""
    return json.loads((FIXTURES / "search_marktplaats.json").read_text())


@pytest.fixture(scope="session")
def search_response_be() -> dict[str, Any]:
    """Recorded lrp/api/search response from 2dehands.be."""
    return json.loads((FIXTURES / "search_2dehands.json").read_text())


@pytest.fixture(scope="session")
def seller_response() -> dict[str, Any]:
    """Recorded v/api/seller-profile response."""
    return json.loads((FIXTURES / "seller_profile.json").read_text())


@pytest.fixture(scope="session")
def listing_page_html() -> str:
    """Recorded listing detail page (trimmed to the window.__CONFIG__ payload)."""
    return (FIXTURES / "listing_page.html").read_text()
