"""The login/status/logout CLI, with browsers and HTTP faked."""

import json
import sys
import types

import httpx
import pytest
import respx

from marktplaats_mcp import cli
from marktplaats_mcp.sites import SITES

NL = SITES["marktplaats"]


def fake_rookiepy(monkeypatch, cookies_by_browser: dict[str, list[dict]]) -> None:
    module = types.ModuleType("rookiepy")

    def loader_for(name: str):
        def loader(domains=None):
            if name not in cookies_by_browser:
                raise RuntimeError("Can't find cookies file")
            return cookies_by_browser[name]

        return loader

    for name in cli.BROWSERS:
        setattr(module, name, loader_for(name))
    monkeypatch.setitem(sys.modules, "rookiepy", module)


def mock_verification(ok: bool = True) -> None:
    status = 200 if ok else 401
    respx.get(f"{NL.base_url}/header/messages/message-count").mock(
        return_value=httpx.Response(status, json={"unreadMessagesCount": 2})
    )
    respx.get(f"{NL.base_url}/header/notifications/notification-count").mock(
        return_value=httpx.Response(status, json={"unreadNotificationsCount": 0})
    )
    respx.get(f"{SITES['2dehands'].base_url}/header/messages/message-count").mock(
        return_value=httpx.Response(401)
    )


def test_cookie_header_requires_session_cookie():
    cookies = [
        {"domain": ".marktplaats.nl", "name": "luckynumber", "value": "1"},
        {"domain": "www.marktplaats.nl", "name": "MpSession", "value": "abc"},
        {"domain": ".2dehands.be", "name": "MpSession", "value": "other-site"},
    ]
    assert cli.cookie_header(cookies, NL) == "luckynumber=1; MpSession=abc"
    assert cli.cookie_header(cookies[:1], NL) is None


@respx.mock
def test_login_imports_from_first_browser_with_a_session(monkeypatch, tmp_path, capsys):
    session_path = tmp_path / "session.json"
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(session_path))
    mock_verification()
    fake_rookiepy(
        monkeypatch,
        {
            "chrome": [{"domain": ".marktplaats.nl", "name": "other", "value": "x"}],
            "firefox": [{"domain": ".marktplaats.nl", "name": "MpSession", "value": "s3cret"}],
        },
    )
    assert cli.main(["login"]) == 0
    saved = json.loads(session_path.read_text())
    assert saved["sites"]["marktplaats"]["cookie"] == "MpSession=s3cret"
    assert saved["sites"]["marktplaats"]["source"] == "firefox"
    assert saved["read_only"] is False
    assert "2dehands" not in saved["sites"]
    assert oct(session_path.stat().st_mode & 0o777) == "0o600"
    out = capsys.readouterr().out
    assert "www.marktplaats.nl: logged in via firefox (2 unread messages)" in out


@respx.mock
def test_login_fails_cleanly_when_no_browser_has_a_session(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(tmp_path / "s.json"))
    mock_verification()
    fake_rookiepy(monkeypatch, {})
    assert cli.main(["login", "--site", "marktplaats"]) == 1
    assert "No working session found" in capsys.readouterr().err


@respx.mock
def test_login_rejects_stale_cookie(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(tmp_path / "s.json"))
    mock_verification(ok=False)
    fake_rookiepy(
        monkeypatch,
        {"chrome": [{"domain": ".marktplaats.nl", "name": "MpSession", "value": "old"}]},
    )
    assert cli.main(["login", "--site", "marktplaats", "--browser", "chrome"]) == 1
    assert "rejected it" in capsys.readouterr().out


@respx.mock
def test_login_paste_and_read_only(monkeypatch, tmp_path):
    session_path = tmp_path / "session.json"
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(session_path))
    mock_verification()
    monkeypatch.setattr("getpass.getpass", lambda prompt="": "MpSession=pasted; luckynumber=1")
    assert cli.main(["login", "--paste", "--site", "marktplaats", "--read-only"]) == 0
    saved = json.loads(session_path.read_text())
    assert saved["sites"]["marktplaats"]["source"] == "paste"
    assert saved["read_only"] is True


def test_login_without_rookiepy_explains_the_extra(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(tmp_path / "s.json"))
    monkeypatch.setitem(sys.modules, "rookiepy", None)  # simulate ImportError
    assert cli.main(["login", "--site", "marktplaats"]) == 1
    assert "marktplaats-mcp[login]" in capsys.readouterr().err


@respx.mock
def test_status_and_logout(monkeypatch, tmp_path, capsys):
    session_path = tmp_path / "session.json"
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(session_path))
    assert cli.main(["status"]) == 1
    cli.write_session(
        session_path,
        {"version": 1, "read_only": False, "sites": {"marktplaats": {"cookie": "MpSession=x"}}},
    )
    mock_verification()
    assert cli.main(["status"]) == 0
    assert "OK, 2 unread" in capsys.readouterr().out
    assert cli.main(["logout"]) == 0
    assert not session_path.exists()
    assert cli.main(["logout"]) == 0


@pytest.mark.parametrize("command", ["login", "status", "logout"])
def test_server_entry_point_dispatches_to_cli(monkeypatch, command):
    from marktplaats_mcp import server

    called: list[list[str]] = []
    monkeypatch.setattr(sys, "argv", ["marktplaats-mcp", command])
    monkeypatch.setattr(cli, "main", lambda argv: called.append(argv) or 0)
    with pytest.raises(SystemExit) as exit_info:
        server.main()
    assert exit_info.value.code == 0
    assert called == [[command]]
