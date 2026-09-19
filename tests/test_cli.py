"""The login/status/logout CLI, with browsers and HTTP faked."""

import json
import os
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
    module.chromium_based = lambda db_path, domains=None: cookies_by_browser.get("copied", [])
    monkeypatch.setitem(sys.modules, "rookiepy", module)


@respx.mock
def test_login_copies_a_locked_chromium_database(monkeypatch, tmp_path):
    session_path = tmp_path / "session.json"
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(session_path))
    mock_verification()
    locked = [{"domain": ".marktplaats.nl", "name": "MpSession", "value": "copied"}]
    fake_rookiepy(monkeypatch, {"copied": locked})  # brave itself raises (locked)
    cookie_file = tmp_path / "Brave/Default/Cookies"
    cookie_file.parent.mkdir(parents=True)
    cookie_file.write_bytes(b"sqlite")
    monkeypatch.setattr(cli, "_chromium_cookie_files", lambda name: [cookie_file])
    assert cli.main(["login", "--browser", "brave", "--site", "marktplaats"]) == 0
    saved = json.loads(session_path.read_text())
    assert saved["sites"]["marktplaats"]["cookie"] == "MpSession=copied"
    assert saved["sites"]["marktplaats"]["source"] == "brave"


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
    assert cli.main(["login", "--site", "both"]) == 0
    saved = json.loads(session_path.read_text())
    assert saved["sites"]["marktplaats"]["cookie"] == "MpSession=s3cret"
    assert saved["sites"]["marktplaats"]["source"] == "firefox"
    assert saved["read_only"] is False
    assert "2dehands" not in saved["sites"]
    if os.name != "nt":  # Windows has no POSIX file modes
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
    assert cli.main(["login", "--browser", "chrome", "--site", "marktplaats"]) == 1
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


def fake_playwright(monkeypatch, cookies_after_login: list[dict], launches: list[str]) -> None:
    """A minimal stand-in for playwright.sync_api: the 'user' logs in on the second poll."""

    class Error(Exception):
        pass

    class Page:
        def goto(self, url, wait_until=None):
            self.url = url

        def wait_for_timeout(self, ms):
            pass

    class Context:
        def __init__(self):
            self.pages = [Page()]
            self.polls = 0

        def cookies(self, url=None):
            self.polls += 1
            return cookies_after_login if self.polls >= 2 else []

        def close(self):
            pass

    class Chromium:
        def launch_persistent_context(self, profile, channel=None, **kwargs):
            launches.append(channel or "bundled")
            if channel == "chrome":
                raise Error("chrome not installed")
            return Context()

    class Playwright:
        chromium = Chromium()

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    api = types.ModuleType("playwright.sync_api")
    api.Error = Error
    api.sync_playwright = lambda: Playwright()
    pkg = types.ModuleType("playwright")
    pkg.sync_api = api
    monkeypatch.setitem(sys.modules, "playwright", pkg)
    monkeypatch.setitem(sys.modules, "playwright.sync_api", api)


@respx.mock
def test_login_window_captures_session_after_user_logs_in(monkeypatch, tmp_path, capsys):
    session_path = tmp_path / "session.json"
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(session_path))
    mock_verification()
    launches: list[str] = []
    fake_playwright(
        monkeypatch,
        [{"domain": ".marktplaats.nl", "name": "MpSession", "value": "fromwindow"}],
        launches,
    )
    assert cli.main(["login", "--window"]) == 0
    saved = json.loads(session_path.read_text())
    assert saved["sites"]["marktplaats"]["cookie"] == "MpSession=fromwindow"
    assert saved["sites"]["marktplaats"]["source"] == "browser window"
    assert launches == ["chrome", "msedge"]  # chrome missing -> edge used
    assert (tmp_path / "browser-profile").is_dir()
    assert "Log in there" in capsys.readouterr().out


def test_login_window_without_playwright_explains_the_extra(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("MARKTPLAATS_SESSION_FILE", str(tmp_path / "s.json"))
    monkeypatch.setitem(sys.modules, "playwright", None)
    monkeypatch.setitem(sys.modules, "playwright.sync_api", None)
    assert cli.main(["login", "--window"]) == 1
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
    profile_dir = tmp_path / "browser-profile"
    (profile_dir / "Default").mkdir(parents=True)
    (profile_dir / "Default" / "Cookies").write_bytes(b"live login")
    assert cli.main(["logout"]) == 0
    assert not session_path.exists()
    assert not profile_dir.exists()  # the --window profile holds a login too
    assert cli.main(["logout"]) == 0
    assert "No stored session" in capsys.readouterr().out


def test_written_session_is_private_from_the_start(monkeypatch, tmp_path):
    """The file must never exist with the umask's default mode, not even briefly."""
    if sys.platform.startswith("win"):
        pytest.skip("POSIX file modes")
    calls: list[str] = []
    original = cli.Path.write_text

    def spy(self, *args, **kwargs):
        calls.append(oct(self.stat().st_mode & 0o777))
        return original(self, *args, **kwargs)

    monkeypatch.setattr(cli.Path, "write_text", spy)
    path = tmp_path / "session.json"
    cli.write_session(path, {"version": 1})
    assert calls == ["0o600"]  # already private when the content lands
    path.chmod(0o644)
    cli.write_session(path, {"version": 2})
    assert oct(path.stat().st_mode & 0o777) == "0o600"  # an old, looser mode is tightened


def test_browsers_without_a_profile_dir_on_this_platform_are_skipped(monkeypatch, tmp_path):
    """Arc has no Linux build: the empty entry must not make the lookup glob the
    current working directory for */Cookies."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Default").mkdir()
    (tmp_path / "Default" / "Cookies").write_bytes(b"")
    monkeypatch.setattr(sys, "platform", "linux")
    assert cli._chromium_cookie_files("arc") == []
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert cli._chromium_cookie_files("arc") == []
    monkeypatch.delenv("LOCALAPPDATA")
    assert cli._chromium_cookie_files("chrome") == []


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
