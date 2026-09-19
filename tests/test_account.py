"""Account mode: credentials, the authenticated client and the account tools,
with HTTP mocked by respx. Response shapes follow the site's front-end and
open-source captures; live verification needs a real session cookie."""

import json

import httpx
import pytest
import respx
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError

from marktplaats_mcp.account import (
    AccountClient,
    AccountCredentials,
    AuthError,
    normalize_conversation,
    register_account_tools,
)
from marktplaats_mcp.sites import SITES

NL = SITES["marktplaats"]
BASE = NL.base_url
COOKIE = "MpSession=abc123; luckynumber=42"
HOME_HTML = '<script>window.__HEADER_CONFIG__ = {"xsrfToken":"1789842030783.deadbeef"}</script>'


def account_client(cookies: dict[str, str] | None = None) -> AccountClient:
    return AccountClient(
        cookies if cookies is not None else {"marktplaats": COOKIE},
        max_retries=1,
        backoff_base=0.001,
        backoff_cap=0.002,
        cache_ttl=0,
        min_interval=0,
    )


def server_with(client: AccountClient, allow_writes: bool) -> FastMCP:
    server = FastMCP("test")
    register_account_tools(server, client, allow_writes)
    return server


async def call(server: FastMCP, tool: str, args: dict) -> dict:
    async with Client(server) as mcp_client:
        result = await mcp_client.call_tool(tool, args)
        assert result.data is not None
        return dict(result.data)


# --- credentials ----------------------------------------------------------------


def test_credentials_from_env_and_file(tmp_path):
    cookie_file = tmp_path / "cookie.txt"
    cookie_file.write_text("MpSession=from-file\n")
    creds = AccountCredentials.load(
        {
            "MARKTPLAATS_COOKIE": "MpSession=nl",
            "TWEEDEHANDS_COOKIE_FILE": str(cookie_file),
            "MARKTPLAATS_SESSION_FILE": str(tmp_path / "missing.json"),
        }
    )
    assert creds is not None
    assert creds.cookies == {"marktplaats": "MpSession=nl", "2dehands": "MpSession=from-file"}
    assert creds.allow_writes is True  # writes are on by default; every write previews first


def test_credentials_from_session_file_and_read_only_flag(tmp_path):
    session = tmp_path / "session.json"
    session.write_text(
        json.dumps(
            {"version": 1, "read_only": True, "sites": {"2dehands": {"cookie": "MpSession=be"}}}
        )
    )
    creds = AccountCredentials.load({"MARKTPLAATS_SESSION_FILE": str(session)})
    assert creds is not None
    assert creds.cookies == {"2dehands": "MpSession=be"}
    assert creds.allow_writes is False
    # env cookies win over the file, and MARKTPLAATS_READ_ONLY also disables writes
    creds = AccountCredentials.load(
        {"MARKTPLAATS_SESSION_FILE": str(session), "TWEEDEHANDS_COOKIE": "MpSession=env"}
    )
    assert creds is not None
    assert creds.cookies["2dehands"] == "MpSession=env"
    creds = AccountCredentials.load(
        {
            "MARKTPLAATS_COOKIE": "x",
            "MARKTPLAATS_READ_ONLY": "1",
            "MARKTPLAATS_SESSION_FILE": "/nonexistent",
        }
    )
    assert creds is not None
    assert creds.allow_writes is False


def test_no_credentials_when_nothing_configured(tmp_path):
    env = {"MARKTPLAATS_SESSION_FILE": str(tmp_path / "none.json")}
    assert AccountCredentials.load(env) is None
    assert AccountCredentials.load({**env, "MARKTPLAATS_COOKIE": "  "}) is None


# --- client -----------------------------------------------------------------------


@respx.mock
async def test_reads_send_cookie_and_no_xsrf():
    route = respx.get(f"{BASE}/header/messages/message-count").mock(
        return_value=httpx.Response(200, json={"unreadMessagesCount": 3})
    )
    respx.get(f"{BASE}/header/notifications/notification-count").mock(
        return_value=httpx.Response(200, json={"unreadNotificationsCount": 1})
    )
    client = account_client()
    try:
        assert await client.unread_counts(NL) == (3, 1)
    finally:
        await client.aclose()
    request = route.calls[0].request
    assert request.headers["Cookie"] == COOKIE
    assert request.headers["X-Requested-With"] == "XMLHttpRequest"
    assert "x-mp-xsrf" not in request.headers


@respx.mock
async def test_writes_fetch_a_fresh_xsrf_token_each_time():
    home = respx.get(f"{BASE}/").mock(return_value=httpx.Response(200, text=HOME_HTML))
    post = respx.post(f"{BASE}/v/api/favourite-listing").mock(
        return_value=httpx.Response(200, json={"isFavourite": True})
    )
    client = account_client()
    try:
        await client.set_favorite(NL, "m1", True)
        await client.set_favorite(NL, "m1", True)
    finally:
        await client.aclose()
    assert home.call_count == 2  # token rotates per page load, so never cached
    request = post.calls[0].request
    assert request.headers["x-mp-xsrf"] == "1789842030783.deadbeef"
    assert request.headers["Origin"] == BASE
    assert request.headers["Referer"] == "https://link.marktplaats.nl/m1"
    assert json.loads(request.content) == {"itemId": "m1", "favourite": True}


@respx.mock
async def test_401_becomes_actionable_auth_error():
    respx.get(f"{BASE}/header/messages/message-count").mock(
        return_value=httpx.Response(401, text="Unauthorized")
    )
    client = account_client()
    try:
        with pytest.raises(AuthError, match="MARKTPLAATS_COOKIE"):
            await client.unread_counts(NL)
    finally:
        await client.aclose()


@respx.mock
async def test_missing_xsrf_token_means_stale_session():
    respx.get(f"{BASE}/").mock(return_value=httpx.Response(200, text="<html>login page</html>"))
    client = account_client()
    try:
        with pytest.raises(AuthError, match="rejected the session"):
            await client.set_favorite(NL, "m1", True)
    finally:
        await client.aclose()


@respx.mock
async def test_conversations_fall_back_to_legacy_endpoint():
    respx.get(url__regex=rf"{BASE}/messages/api/rpc/conversations\.getConversations.*").mock(
        return_value=httpx.Response(404)
    )
    legacy = respx.get(url__regex=rf"{BASE}/messages/api/conversations/\?.*").mock(
        return_value=httpx.Response(
            200,
            json={
                "_embedded": {
                    "mc:conversations": [
                        {
                            "id": "14s06:4cd8wk3:2kl3h37b0",
                            "title": "Racefiets",
                            "unreadMessagesCount": 1,
                            "itemId": "m123",
                            "otherParticipant": {"id": 77, "name": "Piet"},
                        }
                    ]
                }
            },
        )
    )
    client = account_client()
    try:
        rows = await client.conversations(NL, 20, 0)
    finally:
        await client.aclose()
    assert legacy.called
    conversation = normalize_conversation(rows[0])
    assert conversation.id == "14s06:4cd8wk3:2kl3h37b0"
    assert conversation.other_party == "Piet"
    assert conversation.other_party_id == 77
    assert conversation.unread_count == 1
    assert conversation.listing_id == "m123"


def test_normalize_live_conversation_shape():
    """Shape recorded from a real inbox on 2026-09-19 (values replaced)."""
    conversation = normalize_conversation(
        {
            "title": "Boek",
            "unreadMessagesCount": 1,
            "itemId": "m1",
            "otherParticipant": {"id": 14545042, "name": "Watson", "userId": 14545042},
            "sellerId": 46236448,
            "latestMessage": {
                "senderId": -1,
                "text": "Geef vandaag je pakket af",
                "receivedDate": "2026-09-19T19:00:09.801Z",
                "messageType": "systemMessage",
                "from": "system",
            },
            "conversationId": "pj39:5871xhr:2psmwk4mr",
            "latestReceivedDate": "2026-09-19T19:00:09.801Z",
            "latestPaymentRequest": {"status": "RESERVED"},
        }
    )
    assert conversation.id == "pj39:5871xhr:2psmwk4mr"
    assert conversation.role == "seller"  # the other party is not the seller, so I am
    assert conversation.last_message_from == "system"
    assert conversation.last_message_at == "2026-09-19T19:00:09.801Z"
    assert conversation.payment_status == "RESERVED"
    assert conversation.unread_count == 1


def test_normalize_live_listing_favorite_bid_and_saved_search_shapes():
    from marktplaats_mcp.account import (
        normalize_bid,
        normalize_favorite,
        normalize_my_listing,
        normalize_saved_search,
    )

    listing = normalize_my_listing(
        {
            "itemId": "m2",
            "categoryName": "Kattenvoerbakken",
            "title": "Voerbak",
            "vipUrl": "/v/dieren/m2-voerbak",
            "highestBid": 1250,
            "viewCount": 37,
            "closeDate": "2026-09-23T17:13:23Z",
            "reserved": False,
            "priceCents": 7000,
            "priceType": "MIN_BID",
            "biddingEnabled": True,
            "status": "EXPIRING",
            "expiring": True,
        },
        NL,
    )
    assert listing.price == "Bieden vanaf € 70,00"
    assert listing.price_euros == 70.0
    assert listing.highest_bid_euros == 12.5
    assert listing.expires_at == "2026-09-23T17:13:23Z"
    assert listing.category == "Kattenvoerbakken"
    assert listing.bidding_enabled is True

    row = {
        "itemId": "m3",
        "title": "MacBook",
        "pricing": {"label": "€ 1.800,00", "type": "min_bid"},
        "published": True,
        "bidding": {
            "userPlacedHighestBid": False,
            "highestUserBidValue": "€ 1.300,00",
            "userPlacedBid": True,
            "highestBidValue": "€ 1.350,00",
            "allowPlaceBid": True,
        },
        "category": {"id": 339, "name": "Windows Laptops"},
        "location": {"label": "Zutphen", "type": "city"},
        "vipUrl": "/v/computers/m3-macbook",
        "seller": {"name": "Pods"},
    }
    favorite = normalize_favorite(row, NL)
    assert favorite.city == "Zutphen"
    assert favorite.category == "Windows Laptops"
    assert favorite.my_bid == "€ 1.300,00"
    assert favorite.my_bid_is_highest is False
    bid = normalize_bid(row, NL)
    assert bid.my_bid_euros == 1300.0
    assert bid.highest_bid == "€ 1.350,00"
    assert bid.status == "outbid"
    assert bid.available is True

    saved = normalize_saved_search(
        {
            "id": "17675195584363",
            "title": "Danielle",
            "url": "https://www.marktplaats.nl/s/17675195584363.html",
            "searchType": "seller",
            "emailEnabled": True,
            "pushEnabled": False,
        }
    )
    assert saved.name == "Danielle"
    assert saved.type == "seller"
    assert saved.email_alerts is True
    assert saved.push_alerts is False


def test_normalize_trpc_conversation():
    conversation = normalize_conversation(
        {
            "id": "abc",
            "itemId": "m9",
            "title": "Lamp",
            "otherParticipant": {"userId": 5, "displayName": "Anna"},
            "lastMessage": {"text": "Is deze nog beschikbaar?"},
            "lastMessageAt": "2026-09-19T10:00:00Z",
            "unreadCount": 0,
        }
    )
    assert conversation.other_party == "Anna"
    assert conversation.other_party_id == 5
    assert conversation.last_message == "Is deze nog beschikbaar?"
    assert conversation.unread_count == 0


# --- tools --------------------------------------------------------------------------


async def test_read_tools_registered_and_writes_gated():
    async with Client(server_with(account_client(), allow_writes=False)) as mcp_client:
        tools = {tool.name: tool for tool in await mcp_client.list_tools()}
    assert set(tools) == {
        "get_my_account",
        "list_conversations",
        "get_conversation",
        "list_my_listings",
        "list_favorites",
        "list_my_bids",
        "list_saved_searches",
    }
    assert all(tool.annotations.read_only_hint for tool in tools.values())

    async with Client(server_with(account_client(), allow_writes=True)) as mcp_client:
        tools = {tool.name: tool for tool in await mcp_client.list_tools()}
    assert {
        "send_message",
        "contact_seller",
        "set_favorite",
        "place_bid",
        "extend_my_listing",
    } <= set(tools)
    assert tools["place_bid"].annotations.destructive_hint is True
    assert tools["send_message"].annotations.read_only_hint is False
    assert tools["send_message"].annotations.idempotent_hint is False
    assert tools["set_favorite"].annotations.idempotent_hint is True


async def test_tools_refuse_sites_without_a_cookie():
    server = server_with(account_client({"marktplaats": COOKIE}), allow_writes=False)
    with pytest.raises(ToolError, match="TWEEDEHANDS_COOKIE"):
        await call(server, "get_my_account", {"site": "2dehands"})


@respx.mock
async def test_get_my_account_contract():
    respx.get(f"{BASE}/header/messages/message-count").mock(
        return_value=httpx.Response(200, json={"unreadMessagesCount": 2})
    )
    respx.get(f"{BASE}/header/notifications/notification-count").mock(
        return_value=httpx.Response(200, json={"unreadNotificationsCount": 0})
    )
    respx.get(f"{BASE}/identity/v2/api/user").mock(
        return_value=httpx.Response(200, json={"id": 42, "displayName": "Jasp"})
    )
    data = await call(server_with(account_client(), False), "get_my_account", {})
    assert data["logged_in"] is True
    assert data["unread_messages"] == 2
    assert data["user_id"] == 42
    assert data["user_name"] == "Jasp"
    assert data["writes_enabled"] is False
    assert "read-only" in data["note"]


@respx.mock
async def test_get_conversation_current_shape_with_payment_offer():
    respx.get(
        url__regex=rf"{BASE}/messages/api/rpc/conversations\.getMessagesForConversation.*"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "result": {
                    "data": {
                        "messages": [
                            {
                                "messageId": "1",
                                "text": "[Betaling]",
                                "receivedDate": "2026-09-19T18:20:16.776Z",
                                "isRead": True,
                                "from": "otherParticipant",
                                "type": "paymentOffer",
                                "attachment": {
                                    "type": "paymentOffer",
                                    "paymentOffer": {"status": "ACCEPTED", "offerPrice": 19000},
                                },
                            },
                            {"text": "Ok!", "from": "me", "type": "text", "isRead": True},
                            {"text": "Pakket verstuurd", "from": "system", "type": "text"},
                        ],
                        "actions": [],
                    }
                }
            },
        )
    )
    data = await call(
        server_with(account_client(), False),
        "get_conversation",
        {"conversation_id": "x", "limit": 2},
    )
    assert [m["sender"] for m in data["messages"]] == ["me", "system"]  # last two only
    full = await call(
        server_with(account_client(), False), "get_conversation", {"conversation_id": "x"}
    )
    assert full["messages"][0]["type"] == "paymentOffer"
    assert full["messages"][0]["offer_euros"] == 190.0
    assert full["messages"][0]["offer_status"] == "ACCEPTED"
    assert "type" not in full["messages"][1]


@respx.mock
async def test_get_conversation_marks_senders():
    respx.get(
        url__regex=rf"{BASE}/messages/api/rpc/conversations\.getMessagesForConversation.*"
    ).mock(return_value=httpx.Response(404))
    respx.get(url__regex=rf"{BASE}/messages/api/conversations/abc/messages/.*").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "_embedded": {
                    "otherParticipant": {"id": 77, "name": "Piet"},
                    "mc:message": [
                        {
                            "senderId": 77,
                            "receivedDate": "2026-09-19T09:00:00Z",
                            "isRead": True,
                            "text": "Hoi",
                        },
                        {
                            "senderId": 1,
                            "receivedDate": "2026-09-19T09:05:00Z",
                            "isRead": True,
                            "text": "Hallo!",
                        },
                    ],
                },
            },
        )
    )
    data = await call(
        server_with(account_client(), False), "get_conversation", {"conversation_id": "abc"}
    )
    assert data["other_party"] == "Piet"
    assert [m["sender"] for m in data["messages"]] == ["them", "me"]
    assert data["messages"][1]["text"] == "Hallo!"


@respx.mock
async def test_list_my_listings_contract():
    respx.get(url__regex=rf"{BASE}/my-account/sell/api/listings.*").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalNumberOfResults": 1,
                "ads": [
                    {
                        "itemId": "m555",
                        "title": "Lamp",
                        "priceInfo": {"priceCents": 2500, "priceType": "FIXED"},
                        "status": "ACTIVE",
                        "viewCount": 12,
                        "favoriteCount": 1,
                        "createdAt": "2026-09-01T10:00:00Z",
                        "expiresAt": "2026-10-01T10:00:00Z",
                        "vipUrl": "/v/huis/lampen/m555-lamp",
                        "expiring": False,
                    }
                ],
            },
        )
    )
    data = await call(server_with(account_client(), False), "list_my_listings", {})
    listing = data["listings"][0]
    assert listing["id"] == "m555"
    assert listing["price"] == "€ 25,00"
    assert listing["price_euros"] == 25.0
    assert listing["view_count"] == 12
    assert listing["url"] == f"{BASE}/v/huis/lampen/m555-lamp"
    assert data["total_count"] == 1


@respx.mock
async def test_list_favorites_and_bids_and_saved_searches():
    respx.get(url__regex=rf"{BASE}/my-account/favorites/favorites\.json.*").mock(
        return_value=httpx.Response(
            200,
            json={
                "favorites": [
                    {
                        "itemId": "m1",
                        "title": "Stoel",
                        "pricing": {"label": "€ 10,00", "type": "fixed"},
                        "published": True,
                        "location": {"cityName": "Gent"},
                        "seller": {"name": "Els"},
                        "vipUrl": "/v/x/m1-stoel",
                    }
                ],
                "moreFavoritesAvailable": False,
            },
        )
    )
    respx.get(f"{BASE}/my-account/bids/favorites.json").mock(
        return_value=httpx.Response(
            200,
            json={
                "favorites": [
                    {
                        "itemId": "m2",
                        "title": "Fiets",
                        "pricing": {"label": "Bieden vanaf € 100,00", "type": "min_bid"},
                        "myBid": {"amount": 120, "currency": "EUR", "status": "OPEN"},
                        "vipUrl": "/v/x/m2-fiets",
                    }
                ],
                "moreBidsAvailable": False,
            },
        )
    )
    respx.get(f"{BASE}/header/searches/saved").mock(
        return_value=httpx.Response(
            200,
            json=[{"id": 9, "name": "racefiets", "url": "/q/racefiets/", "newAdsCount": 4}],
        )
    )
    server = server_with(account_client(), False)
    favorites = await call(server, "list_favorites", {})
    assert favorites["favorites"][0]["seller"] == "Els"
    assert favorites["favorites"][0]["available"] is True
    assert favorites["more_available"] is False
    bids = await call(server, "list_my_bids", {})
    assert bids["bids"][0]["my_bid_euros"] == 120.0
    assert bids["bids"][0]["status"] == "unknown"  # legacy shape carries no highest-bid flag
    saved = await call(server, "list_saved_searches", {})
    assert saved["saved_searches"][0]["new_ads_count"] == 4


@respx.mock
async def test_send_message_previews_then_sends(tmp_path, monkeypatch):
    monkeypatch.setenv("MARKTPLAATS_AUDIT_LOG", str(tmp_path / "writes.jsonl"))
    respx.get(f"{BASE}/").mock(return_value=httpx.Response(200, text=HOME_HTML))
    post = respx.post(f"{BASE}/messages/api/conversations/abc/message").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    server = server_with(account_client(), allow_writes=True)
    preview = await call(server, "send_message", {"conversation_id": "abc", "text": " Hoi! "})
    assert preview["preview"] is True
    assert preview["target"]["text"] == "Hoi!"
    assert not post.called

    sent = await call(
        server, "send_message", {"conversation_id": "abc", "text": "Hoi!", "confirm": True}
    )
    assert sent["preview"] is False
    assert sent["success"] is True
    assert json.loads(post.calls[0].request.content) == {"text": "Hoi!"}
    audit = (tmp_path / "writes.jsonl").read_text().strip().splitlines()
    assert len(audit) == 1
    assert json.loads(audit[0])["action"] == "send_message"


@respx.mock
async def test_place_bid_checks_minimum_and_previews(listing_vip):
    respx.post(url__regex=r"https://app\.marktplaats\.nl/app/vip/v4/item/.*").mock(
        return_value=httpx.Response(200, json=listing_vip)  # minimum bid € 150
    )
    respx.get(f"{BASE}/").mock(return_value=httpx.Response(200, text=HOME_HTML))
    bid = respx.post(f"{BASE}/v/api/place-bid").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    server = server_with(account_client(), allow_writes=True)
    with pytest.raises(ToolError, match=r"below the minimum bid of €150\.00"):
        await call(server, "place_bid", {"listing_id": "m2444371973", "amount_euros": 100})

    preview = await call(server, "place_bid", {"listing_id": "m2444371973", "amount_euros": 160})
    assert preview["preview"] is True
    assert preview["target"]["minimum_bid_euros"] == 150.0
    assert preview["target"]["listing_title"] == "Baan fiets"
    assert "binding" in preview["note"]
    assert not bid.called

    placed = await call(
        server,
        "place_bid",
        {"listing_id": "m2444371973", "amount_euros": 160, "confirm": True, "message": "Ok"},
    )
    assert placed["success"] is True
    body = json.loads(bid.calls[0].request.content)
    assert body == {
        "itemId": "m2444371973",
        "bidAmountCents": 16000,
        "message": "Ok",
        "phoneNumber": "",
    }


@respx.mock
async def test_contact_seller_preview_includes_listing_context(listing_vip):
    respx.post(url__regex=r"https://app\.marktplaats\.nl/app/vip/v4/item/.*").mock(
        return_value=httpx.Response(200, json=listing_vip)
    )
    asq = respx.post(f"{BASE}/v/api/asq").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    respx.get(f"{BASE}/").mock(return_value=httpx.Response(200, text=HOME_HTML))
    server = server_with(account_client(), allow_writes=True)
    preview = await call(
        server,
        "contact_seller",
        {"listing_id": "2444371973", "message": "Is deze nog beschikbaar?", "offer_euros": 200},
    )
    assert preview["preview"] is True
    assert preview["target"]["listing_title"] == "Baan fiets"
    assert preview["target"]["seller"] == "Sample Seller"
    assert not asq.called
    await call(
        server,
        "contact_seller",
        {
            "listing_id": "m2444371973",
            "message": "Is deze nog beschikbaar?",
            "offer_euros": 200,
            "confirm": True,
        },
    )
    assert json.loads(asq.calls[0].request.content) == {
        "itemId": "m2444371973",
        "message": "Is deze nog beschikbaar?",
        "offerAmount": 20000,
    }


@respx.mock
async def test_write_tools_absent_without_allow_writes():
    server = server_with(account_client(), allow_writes=False)
    with pytest.raises(ToolError):
        await call(server, "send_message", {"conversation_id": "abc", "text": "x", "confirm": True})
