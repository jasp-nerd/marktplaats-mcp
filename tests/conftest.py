import json
from pathlib import Path
from typing import Any

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


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
