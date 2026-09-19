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


def test_host_and_origin_guard_from_environment():
    from marktplaats_mcp.server import http_guard_config, mcp

    assert http_guard_config({}) == {}
    config = http_guard_config(
        {
            "MCP_ALLOWED_HOSTS": "marktplaats-mcp.jaspnerd.dev",
            "MCP_ALLOWED_ORIGINS": "https://claude.ai, https://*.claude.ai",
        }
    )
    init = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "p", "version": "0"},
        },
    }
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    with TestClient(mcp.http_app(**config), base_url="https://marktplaats-mcp.jaspnerd.dev") as c:
        assert c.post("/mcp", headers=headers, json=init).status_code == 200
        assert (
            c.post("/mcp", headers={**headers, "Host": "evil.example"}, json=init).status_code
            == 421
        )
        bad = {**headers, "Origin": "https://evil.example"}
        assert c.post("/mcp", headers=bad, json=init).status_code == 403
        good = {**headers, "Origin": "https://app.claude.ai"}
        assert c.post("/mcp", headers=good, json=init).status_code == 200
