"""Static pages served next to the hosted MCP endpoint: a landing page,
llms.txt, a privacy policy and icons (the registry requires icons to live on
the server's own domain)."""

from __future__ import annotations

import html
import json
from importlib import resources
from string import Template

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse, Response

from .. import __version__

SITE_URL = "https://marktplaats-mcp.jaspnerd.dev"
REPO_URL = "https://github.com/jasp-nerd/marktplaats-mcp"
PYPI_URL = "https://pypi.org/project/marktplaats-mcp/"

TOOLS = [
    (
        "search_listings",
        "Search with category, attribute, price, condition, delivery, distance and recency.",
    ),
    (
        "get_listing_details",
        "Full ad: description, attributes, status, listing time, bids, shipping, seller signals.",
    ),
    (
        "get_seller_profile",
        "Verified bank account, identity, phone, business verification, reviews.",
    ),
    ("list_seller_listings", "Everything one seller currently offers."),
    ("list_categories", "The category tree used for filtering."),
    (
        "list_category_filters",
        "Category-specific filters (brand, frame height, mileage, RAM, ...) with valid values.",
    ),
    ("check_new_listings", "Stateless monitoring: only ads placed after a timestamp."),
    ("analyze_prices", "Median, quartiles, min and max asking prices, plus the cheapest matches."),
]
ACCOUNT_TOOLS = [
    "get_my_account",
    "list_conversations",
    "get_conversation",
    "list_my_listings",
    "list_favorites",
    "list_my_bids",
    "list_saved_searches",
    "send_message",
    "contact_seller",
    "set_favorite",
    "place_bid",
    "extend_my_listing",
]
FAQ = [
    (
        "Is there an MCP server for Marktplaats?",
        "Yes: this one. It is free, open source (MIT) and needs no API key. Add the hosted URL "
        "as a custom connector in claude.ai, or run it locally with uvx marktplaats-mcp.",
    ),
    (
        "Does it work with 2dehands.be and Belgium?",
        "Yes. Every tool takes a site parameter: marktplaats (Netherlands) or 2dehands (Belgium), "
        "including a language filter for Dutch- or French-language Belgian ads.",
    ),
    (
        "Can AI read and send my Marktplaats messages, place bids or manage my ads?",
        "Yes, with the local server and your own login: run marktplaats-mcp login once and the "
        "account tools appear. Sending and bidding always show a preview first. The hosted "
        "endpoint never offers account tools, so your session never leaves your machine.",
    ),
    (
        "Do I need a Marktplaats account or API key?",
        "No. Searching, listing details, seller checks, filters, price statistics and monitoring "
        "work without any account. An account is only needed for your own messages, favorites, "
        "bids and ads.",
    ),
    (
        "Does it work with ChatGPT, Cursor, Gemini, VS Code and Cline?",
        "It works with every MCP client over stdio (uvx marktplaats-mcp) and with clients that "
        "support remote Streamable HTTP servers via the hosted URL.",
    ),
    (
        "Is this official or affiliated with Marktplaats?",
        "No. It is an independent open source project with no ties to Marktplaats, 2dehands or "
        "Adevinta. It uses the same public JSON endpoints the websites use, backs off politely, "
        "and never rewrites listing links into affiliate or tracking URLs.",
    ),
]


def register_web_routes(server: FastMCP) -> None:
    @server.custom_route("/", methods=["GET"], include_in_schema=False)
    async def landing(_: Request) -> Response:
        return HTMLResponse(landing_html())

    @server.custom_route("/llms.txt", methods=["GET"], include_in_schema=False)
    async def llms(_: Request) -> Response:
        return PlainTextResponse(llms_txt())

    @server.custom_route("/privacy", methods=["GET"], include_in_schema=False)
    async def privacy(_: Request) -> Response:
        return HTMLResponse(privacy_html())

    @server.custom_route("/robots.txt", methods=["GET"], include_in_schema=False)
    async def robots(_: Request) -> Response:
        return PlainTextResponse(
            f"User-agent: *\nAllow: /\nDisallow: /mcp\nSitemap: {SITE_URL}/sitemap.xml\n"
        )

    @server.custom_route("/sitemap.xml", methods=["GET"], include_in_schema=False)
    async def sitemap(_: Request) -> Response:
        urls = "".join(
            f"<url><loc>{SITE_URL}{path}</loc></url>" for path in ("/", "/privacy", "/llms.txt")
        )
        body = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
        return Response(body, media_type="application/xml")

    @server.custom_route("/icon.png", methods=["GET"], include_in_schema=False)
    async def icon_png(_: Request) -> Response:
        return Response(_asset("icon.png"), media_type="image/png", headers=_CACHE)

    @server.custom_route("/icon.svg", methods=["GET"], include_in_schema=False)
    async def icon_svg(_: Request) -> Response:
        return Response(_asset("icon.svg"), media_type="image/svg+xml", headers=_CACHE)

    @server.custom_route("/health", methods=["GET"], include_in_schema=False)
    async def health(_: Request) -> Response:
        return PlainTextResponse("ok")


_CACHE = {"Cache-Control": "public, max-age=86400"}


def _asset(name: str) -> bytes:
    return resources.files("marktplaats_mcp.web").joinpath(name).read_bytes()


def _json_ld() -> str:
    software = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Marktplaats & 2dehands MCP server",
        "alternateName": ["marktplaats-mcp", "Marktplaats MCP", "2dehands MCP"],
        "applicationCategory": "DeveloperApplication",
        "applicationSubCategory": "MCP server",
        "operatingSystem": "macOS, Linux, Windows",
        "softwareVersion": __version__,
        "description": (
            "MCP server for Marktplaats.nl and 2dehands.be: search, monitor and manage Dutch "
            "and Belgian second-hand classifieds from Claude, ChatGPT, Cursor and any MCP client."
        ),
        "url": SITE_URL,
        "downloadUrl": PYPI_URL,
        "codeRepository": REPO_URL,
        "license": "https://opensource.org/licenses/MIT",
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "inLanguage": ["en", "nl", "fr"],
        "author": {"@type": "Person", "name": "jasp-nerd", "url": "https://github.com/jasp-nerd"},
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in FAQ
        ],
    }
    return json.dumps(software) + '</script><script type="application/ld+json">' + json.dumps(faq)


def _template(name: str) -> Template:
    return Template(resources.files("marktplaats_mcp.web").joinpath(name).read_text("utf-8"))


def landing_html() -> str:
    tool_rows = "".join(
        f"<tr><td><code>{name}</code></td><td>{html.escape(text)}</td></tr>" for name, text in TOOLS
    )
    faq_html = "".join(
        f"<h3>{html.escape(question)}</h3><p>{html.escape(answer)}</p>" for question, answer in FAQ
    )
    return _template("landing.html").substitute(
        SITE_URL=SITE_URL,
        REPO_URL=REPO_URL,
        PYPI_URL=PYPI_URL,
        __version__=__version__,
        _json_ld=_json_ld(),
        tool_rows=tool_rows,
        faq_html=faq_html,
        account=", ".join(f"<code>{name}</code>" for name in ACCOUNT_TOOLS),
    )


def llms_txt() -> str:
    return _template("llms.txt.tmpl").substitute(
        SITE_URL=SITE_URL,
        REPO_URL=REPO_URL,
        PYPI_URL=PYPI_URL,
        __version__=__version__,
        tools="\n".join(f"- `{name}`: {text}" for name, text in TOOLS),
        account=", ".join(f"`{name}`" for name in ACCOUNT_TOOLS),
    )


def privacy_html() -> str:
    return _template("privacy.html").substitute(SITE_URL=SITE_URL, REPO_URL=REPO_URL)
