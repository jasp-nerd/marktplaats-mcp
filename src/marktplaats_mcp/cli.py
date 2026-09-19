"""``marktplaats-mcp login|status|logout``: manage the local account session.

``login`` copies the Marktplaats / 2dehands session from a browser the user is
already logged into (yt-dlp's cookies-from-browser approach), verifies it
against the site and stores it in a private file the server reads on startup.
Chromium browsers keep their cookie database locked while running, so it is
copied before reading. Alternatives: ``--window`` opens a browser window to
log in there, and ``--paste`` takes a Cookie header.
"""

from __future__ import annotations

import argparse
import asyncio
import concurrent.futures
import contextlib
import json
import os
import sys
import time
from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .client import ApiError
from .sites import SITES, Site

SESSION_FILE_ENV = "MARKTPLAATS_SESSION_FILE"
SESSION_COOKIE_NAME = "MpSession"
BROWSERS = (
    "chrome",
    "firefox",
    "safari",
    "edge",
    "brave",
    "arc",
    "chromium",
    "vivaldi",
    "opera",
    "librewolf",
)


def session_file(environ: Any = os.environ) -> Path:
    override = environ.get(SESSION_FILE_ENV, "").strip()
    if override:
        return Path(override).expanduser()
    base = Path(environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
    return base / "marktplaats-mcp" / "session.json"


def read_session(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def stored_sites(session: dict[str, Any]) -> dict[str, Any]:
    sites = session.get("sites")
    return dict(sites) if isinstance(sites, dict) else {}


def write_session(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    with contextlib.suppress(OSError):
        path.chmod(0o600)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="marktplaats-mcp",
        description="Manage the Marktplaats / 2dehands account session used by the MCP server.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    login = commands.add_parser(
        "login",
        help="Copy your session from a browser you are logged into and store it locally.",
    )
    login.add_argument(
        "--site",
        choices=["marktplaats", "2dehands", "both"],
        default="marktplaats",
        help="Which marketplace to log in to (default: marktplaats).",
    )
    login.add_argument(
        "--browser",
        choices=BROWSERS,
        help="Only read this browser (default: try them all).",
    )
    login.add_argument(
        "--window",
        action="store_true",
        help="Open a browser window to log in there instead of reading an existing session.",
    )
    login.add_argument(
        "--paste",
        action="store_true",
        help="Paste a Cookie header copied from your browser's developer tools instead.",
    )
    login.add_argument(
        "--read-only",
        action="store_true",
        help="Never send messages, place bids or change favorites from this session.",
    )
    commands.add_parser("status", help="Show the stored sessions and check that they work.")
    commands.add_parser("logout", help="Delete the stored sessions.")

    args = parser.parse_args(argv)
    path = session_file()
    if args.command == "login":
        return _login(args, path)
    if args.command == "status":
        return _status(path)
    return _logout(path)


def _login(args: argparse.Namespace, path: Path) -> int:
    sites = [
        SITES[key] for key in (["marktplaats", "2dehands"] if args.site == "both" else [args.site])
    ]
    session = read_session(path)
    stored = stored_sites(session)
    found = False
    for site in sites:
        if args.paste:
            result = _paste_cookie(site)
        elif args.window:
            result = _window_login(site)
        else:
            result = _import_cookie(site, args.browser)
        if result is None:
            continue
        cookie, source = result
        unread = _verify(site, cookie)
        if unread is None:
            print(f"  {site.host}: cookie found in {source} but the site rejected it.")
            continue
        stored[site.key] = {
            "cookie": cookie,
            "source": source,
            "saved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        found = True
        print(f"  {site.host}: logged in via {source} ({unread} unread messages).")
    if not found:
        print(
            "\nNo working session found. Log in at https://www.marktplaats.nl in your browser "
            "and run this again, or use --window or --paste.",
            file=sys.stderr,
        )
        return 1
    write_session(path, {"version": 1, "read_only": bool(args.read_only), "sites": stored})
    mode = "read-only" if args.read_only else "reads and writes (every write asks for confirmation)"
    print(f"\nSaved to {path} ({mode}). Restart your MCP client to load the account tools.")
    return 0


LOGIN_TIMEOUT_SECONDS = 600


def _window_login(site: Site) -> tuple[str, str] | None:
    """Open a real browser window on the login page and wait for a valid session.

    Uses the user's installed Chrome/Edge when available (a normal browser, so
    captcha and SMS verification behave as usual) and a persistent profile
    under the config directory, so "remember this device" survives.
    """
    try:
        from playwright.sync_api import (  # type: ignore[import-not-found,unused-ignore]
            Error as PlaywrightError,
        )
        from playwright.sync_api import (  # type: ignore[import-not-found,unused-ignore]
            sync_playwright,
        )
    except ImportError:
        print(
            "The login window needs the 'login' extra: run\n"
            "  uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login --window\n"
            "or use --paste.",
            file=sys.stderr,
        )
        return None

    profile_dir = session_file().parent / "browser-profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    login_url = f"{site.base_url}/identity/v2/login"
    print(f"Opening a browser window for {site.host}. Log in there as you normally do.")
    with sync_playwright() as playwright:
        context = _launch_browser(playwright, PlaywrightError, profile_dir)
        if context is None:
            return None
        try:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(login_url, wait_until="domcontentloaded")
            deadline = time.monotonic() + LOGIN_TIMEOUT_SECONDS
            last_header: str | None = None
            while time.monotonic() < deadline:
                try:
                    header = cookie_header(context.cookies(site.base_url), site)
                except PlaywrightError:  # window closed by the user
                    break
                if header and header != last_header:
                    last_header = header
                    if _verify(site, header) is not None:
                        return header, "browser window"
                try:
                    page.wait_for_timeout(2000)
                except PlaywrightError:
                    break
        finally:
            with contextlib.suppress(PlaywrightError):
                context.close()
    print(f"  {site.host}: no login detected before the window closed or timed out.")
    return None


def _launch_browser(playwright: Any, error_type: type[Exception], profile_dir: Path) -> Any:
    """Prefer the installed Chrome/Edge; fall back to Playwright's Chromium,
    downloading it on first use."""
    launch = playwright.chromium.launch_persistent_context
    options = {"headless": False, "viewport": {"width": 1100, "height": 900}}
    for channel in ("chrome", "msedge"):
        try:
            return launch(str(profile_dir), channel=channel, **options)
        except error_type:
            continue
    try:
        return launch(str(profile_dir), **options)
    except error_type as exc:
        if "install" not in str(exc).lower():
            print(f"  Could not start a browser: {str(exc).splitlines()[0]}", file=sys.stderr)
            return None
    print("  Downloading a browser for the login window (one-time, ~150 MB) ...")
    import subprocess

    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
    try:
        return launch(str(profile_dir), **options)
    except error_type as exc:
        print(f"  Could not start a browser: {str(exc).splitlines()[0]}", file=sys.stderr)
        return None


def _import_cookie(site: Site, browser: str | None) -> tuple[str, str] | None:
    try:
        import rookiepy  # type: ignore[import-not-found,unused-ignore]
    except ImportError:
        print(
            "Browser import needs the 'login' extra: run\n"
            "  uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login\n"
            "or paste the cookie with --paste.",
            file=sys.stderr,
        )
        return None
    names = [browser] if browser else list(BROWSERS)
    print(f"Looking for a {site.host} session in: {', '.join(names)} ...")
    print("  (macOS may ask for keychain access to read a browser's cookies; click Allow.)")
    blocked: list[str] = []
    domain = site.host.removeprefix("www.")
    for name in names:
        loader: Callable[..., Iterable[dict[str, Any]]] | None = getattr(rookiepy, name, None)
        if loader is None:
            continue
        try:
            cookies = list(loader([domain]))
        except Exception as exc:  # not installed, locked profile, or blocked by the OS
            recovered = _read_locked_chromium_cookies(rookiepy, name, domain)
            if recovered is None:
                if "unable to open database" in str(exc) or "Failed to open" in str(exc):
                    blocked.append(name)
                continue
            cookies = recovered
        header = cookie_header(cookies, site)
        if header:
            return header, name
    if blocked:
        print(
            f"  Could not read the cookies of: {', '.join(blocked)}. On macOS this means the "
            "app you ran this from has no permission to read browser data: run this command "
            "in the Terminal app and click Allow when macOS asks, or give your terminal "
            "Full Disk Access in System Settings > Privacy & Security.",
            file=sys.stderr,
        )
    return None


# Where Chromium-based browsers keep their cookie database. A running browser
# holds it locked, so it is copied to a temporary file first (as yt-dlp does).
_CHROMIUM_DIRS = {
    "chrome": ("Google/Chrome", "google-chrome", "Google/Chrome/User Data"),
    "brave": (
        "BraveSoftware/Brave-Browser",
        "BraveSoftware/Brave-Browser",
        "BraveSoftware/Brave-Browser/User Data",
    ),
    "edge": ("Microsoft Edge", "microsoft-edge", "Microsoft/Edge/User Data"),
    "chromium": ("Chromium", "chromium", "Chromium/User Data"),
    "vivaldi": ("Vivaldi", "vivaldi", "Vivaldi/User Data"),
    "arc": ("Arc/User Data", "", ""),
}


def _chromium_cookie_files(name: str) -> list[Path]:
    dirs = _CHROMIUM_DIRS.get(name)
    if dirs is None:
        return []
    mac, linux, windows = dirs
    if sys.platform == "darwin":
        base = Path.home() / "Library/Application Support" / mac
    elif sys.platform.startswith("win"):
        base = Path(os.environ.get("LOCALAPPDATA", "")) / windows if windows else Path()
    else:
        base = Path.home() / ".config" / linux if linux else Path()
    if not base.is_dir():
        return []
    return sorted(base.glob("*/Cookies")) + sorted(base.glob("*/Network/Cookies"))


def _read_locked_chromium_cookies(
    rookiepy: Any, name: str, domain: str
) -> list[dict[str, Any]] | None:
    """Copy each profile's cookie database and read the copy."""
    import shutil
    import tempfile

    for cookie_file in _chromium_cookie_files(name):
        try:
            with tempfile.TemporaryDirectory() as tmp:
                copy = Path(tmp) / "Cookies"
                shutil.copy2(cookie_file, copy)
                cookies = list(rookiepy.chromium_based(str(copy), [domain]))
        except Exception:  # unreadable profile; try the next one
            continue
        if cookies:
            return cookies
    return None


def _paste_cookie(site: Site) -> tuple[str, str] | None:
    print(
        f"\nIn your browser, open {site.base_url}, log in, open developer tools (F12) -> "
        "Network, click any request to the site, and copy the value of the 'Cookie' request "
        "header. Paste it here (input is not shown):"
    )
    try:
        import getpass

        value = getpass.getpass("Cookie: ").strip()
    except (EOFError, KeyboardInterrupt):
        return None
    if not value:
        return None
    return value, "paste"


def cookie_header(cookies: Iterable[dict[str, Any]], site: Site) -> str | None:
    """Build the Cookie header for ``site`` from browser cookie records, or None
    when there is no session cookie for it."""
    domain_suffix = site.host.removeprefix("www.")
    parts: list[str] = []
    has_session = False
    for cookie in cookies:
        domain = str(cookie.get("domain", "")).lstrip(".")
        name = cookie.get("name")
        value = cookie.get("value")
        if not (domain == domain_suffix or domain.endswith(f".{domain_suffix}")):
            continue
        if not isinstance(name, str) or not isinstance(value, str):
            continue
        parts.append(f"{name}={value}")
        has_session = has_session or name == SESSION_COOKIE_NAME
    return "; ".join(parts) if has_session else None


def _verify(site: Site, cookie: str) -> int | None:
    """Return the unread message count when the cookie is accepted, else None."""
    from .account import AccountClient

    async def check() -> int | None:
        client = AccountClient({site.key: cookie})
        try:
            unread, _ = await client.unread_counts(site)
        except ApiError:
            return None
        finally:
            await client.aclose()
        return unread if unread is not None else 0

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(check())
    # Called from inside Playwright's sync API, which owns this thread's loop.
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(asyncio.run, check()).result()


def _status(path: Path) -> int:
    session = read_session(path)
    sites = stored_sites(session)
    if not sites:
        print(f"No stored session ({path}). Run 'marktplaats-mcp login'.")
        return 1
    mode = "read-only" if session.get("read_only") else "reads and writes"
    print(f"Session file: {path} ({mode})")
    ok = True
    for key, entry in sites.items():
        site = SITES.get(key)
        if site is None or not isinstance(entry, dict):
            continue
        unread = _verify(site, str(entry.get("cookie", "")))
        if unread is None:
            ok = False
            print(f"  {site.host}: STALE (saved {entry.get('saved_at')}); log in again.")
        else:
            saved = f"saved {entry.get('saved_at')} via {entry.get('source')}"
            print(f"  {site.host}: OK, {unread} unread messages ({saved}).")
    return 0 if ok else 1


def _logout(path: Path) -> int:
    try:
        path.unlink()
    except FileNotFoundError:
        print("No stored session.")
        return 0
    print(f"Removed {path}.")
    return 0
