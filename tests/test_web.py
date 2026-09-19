"""The static pages served next to the hosted endpoint."""

import json
import re

from fastmcp import FastMCP
from starlette.testclient import TestClient

from marktplaats_mcp.web import register_web_routes


def app_client() -> TestClient:
    server = FastMCP("test")
    register_web_routes(server)
    return TestClient(server.http_app())


def test_landing_page_has_structured_data_and_connector_url():
    response = app_client().get("/")
    assert response.status_code == 200
    body = response.text
    assert "https://marktplaats-mcp.jaspnerd.dev/mcp" in body
    assert "Is there an MCP server for Marktplaats?" in body
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.DOTALL)
    assert {json.loads(block)["@type"] for block in blocks} == {"SoftwareApplication", "FAQPage"}


def test_llms_txt_privacy_icons_and_health():
    client = app_client()
    llms = client.get("/llms.txt")
    assert llms.status_code == 200
    assert "search_listings" in llms.text
    assert "place_bid" in llms.text
    assert client.get("/privacy").status_code == 200
    assert client.get("/icon.png").headers["content-type"] == "image/png"
    assert client.get("/icon.svg").headers["content-type"].startswith("image/svg")
    assert client.get("/robots.txt").text.startswith("User-agent: *")
    assert "<urlset" in client.get("/sitemap.xml").text
    assert client.get("/health").text == "ok"
