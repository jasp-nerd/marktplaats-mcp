"""``marktplaats-mcp login|status|logout``: manage the local account session.

``login`` imports the Marktplaats / 2dehands session from a browser the user is
already logged into (the same approach yt-dlp's ``--cookies-from-browser``
uses), verifies it against the site, and stores it in a private file the
server reads on startup. Pasting a ``Cookie`` header by hand is the fallback.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import os
import sys
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
        "login", help="Import your session from a browser you are logged into (or paste it)."
    )
    login.add_argument(
        "--site",
        choices=["marktplaats", "2dehands", "both"],
        default="both",
        help="Which marketplace account to import (default: both, whichever is logged in).",
    )
    login.add_argument(
        "--browser",
        choices=BROWSERS,
        help="Only read this browser (default: try them all).",
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
        result = _paste_cookie(site) if args.paste else _import_cookie(site, args.browser)
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
            "and run this again, or use --paste.",
            file=sys.stderr,
        )
        return 1
    write_session(path, {"version": 1, "read_only": bool(args.read_only), "sites": stored})
    mode = "read-only" if args.read_only else "reads and writes (every write asks for confirmation)"
    print(f"\nSaved to {path} ({mode}). Restart your MCP client to load the account tools.")
    return 0


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
    for name in names:
        loader: Callable[..., Iterable[dict[str, Any]]] | None = getattr(rookiepy, name, None)
        if loader is None:
            continue
        try:
            cookies = list(loader([site.host.removeprefix("www.")]))
        except Exception as exc:  # not installed, locked profile, or blocked by the OS
            if "unable to open database" in str(exc) or "Failed to open" in str(exc):
                blocked.append(name)
            continue
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

    return asyncio.run(check())


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
