"""
Trace-locked Letterboxd session + user wrapper.

All behavior is derived ONLY from captured requests:
  - GET https://letterboxd.com/sign-in/
  - POST https://letterboxd.com/user/login.do
  - Cookie-based validation

No undocumented endpoints.
No HTML parsing.
No speculative headers.
"""

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
import getpass

from letterboxdpy.core.scraper import Scraper, requests
from letterboxdpy.utils.utils_file import JsonFile

from letterboxdpy.constants.project import (
    DOMAIN as BASE_URL,
    SIGNIN_URL,
    LOGIN_POST_URL,
    CSRF_COOKIE,
    USER_COOKIE,
    DEFAULT_IMPERSONATE as IMPERSONATE
)

# Or whatever we decide to have as a cookie path
DEFAULT_COOKIE_PATH = Path(".lb_cookies.json")

# ----------------------------
# Debug helpers (unchanged)
# ----------------------------

def dump_response(resp, label):
    print(f"\n[DEBUG] {label}")
    print(f"  Final URL: {resp.url}")
    print(f"  Status: {resp.status_code}")
    if resp.history:
        print("  Redirect chain:")
        for h in resp.history:
            print(f"    {h.status_code} → {h.url}")
    else:
        print("  Redirect chain: (none)")
    print(f"  Content length: {len(resp.text)}")
    print(f"  Snippet: {resp.text[:140]!r}")


def debug_set_cookie(resp, label):
    print(f"\n[DEBUG] Set-Cookie headers in {label}:")
    found = False
    for k, v in resp.headers.items():
        if k.lower() == "set-cookie":
            found = True
            print(f"  {v}")
    if not found:
        sc = resp.headers.get("set-cookie") or resp.headers.get("Set-Cookie")
        print(f"  {sc}" if sc else "  (none)")


def debug_cookies(session, label):
    print(f"\n[DEBUG] Cookies after {label}:")
    jar = list(session.cookies.jar)
    if not jar:
        print("  (no cookies)")
        return
    for c in jar:
        v = c.value
        v_disp = (v[:60] + "...") if len(v) > 60 else v
        print(f"  {c.name}={v_disp} domain={c.domain} path={c.path} secure={bool(c.secure)}")


# ----------------------------
# Cookie utilities
# ----------------------------

def is_logged_in_by_cookie(session) -> bool:
    names = {c.name for c in session.cookies.jar}
    return any(n.startswith("letterboxd.user") for n in names) or (USER_COOKIE in names)


def get_csrf(session) -> str:
    # 1) Dict-like fast path
    if hasattr(session, "cookies") and hasattr(session.cookies, "get"):
        val = session.cookies.get(CSRF_COOKIE)
        if val:
            return val

    # 2) Jar scan fallback (cookie objects)
    jar = getattr(getattr(session, "cookies", None), "jar", None)
    if jar is not None:
        matches = []
        for cookie in jar:
            # I'm concerned about the permanence of the rest of the c.name
            if "csrf" in cookie.name.lower() and cookie.value:
                matches.append(cookie)

        if matches:
            found = matches[0]
            print(f"[WARN] CSRF cookie name changed → using '{found.name}'")
            return found.value

        print("[ERROR] No CSRF cookie found. Available cookies:")
        for cookie in jar:
            print(f"  - {cookie.name}")
    else:
        print("[ERROR] session.cookies.jar not available; cannot scan cookies.")

    raise RuntimeError("Missing CSRF cookie")


def get_signed_in_user(session) -> str:
    if hasattr(session.cookies, "get"):
        val = session.cookies.get(USER_COOKIE)
        if val:
            return val
    raise RuntimeError("Not signed in")


# ----------------------------
# Cookie persistence
# ----------------------------

def save_cookies(session, path: Path):
    cookies = []
    for c in session.cookies.jar:
        cookies.append({
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "secure": bool(c.secure),
        })
    JsonFile.save(str(path), cookies)


def load_session_from_cookies(path: Path):
    s = requests.Session(impersonate=IMPERSONATE)
    cookies = JsonFile.load(str(path))
    if cookies:
        for c in cookies:
            s.cookies.set(**c)
    return s


# ----------------------------
# Login
# ----------------------------

def lb_login(username: str, password: str, cookie_path: Path):
    print(f"[DEBUG] Starting session (impersonate={IMPERSONATE})")
    s = requests.Session(impersonate=IMPERSONATE)

    # STEP 1 — GET sign-in
    r = s.get(SIGNIN_URL, allow_redirects=True)
    r.raise_for_status()
    dump_response(r, "GET /sign-in/")
    debug_set_cookie(r, "GET /sign-in/")
    debug_cookies(s, "GET /sign-in/")

    csrf = s.cookies.get(CSRF_COOKIE)
    if not csrf:
        raise RuntimeError("Missing CSRF cookie")

    # STEP 2 — POST login
    form = {
        "__csrf": csrf,
        "username": username,
        "password": password,
        "remember": "true",
    }

    headers = {
        "Referer": SIGNIN_URL,
        "Origin": BASE_URL,
    }

    pr = s.post(LOGIN_POST_URL, data=form, headers=headers, allow_redirects=True)
    pr.raise_for_status()
    dump_response(pr, "POST /user/login.do")
    debug_set_cookie(pr, "POST /user/login.do")
    debug_cookies(s, "POST /user/login.do")

    # STEP 3 — Validate
    act = s.get(f"{BASE_URL}/activity/", allow_redirects=True)
    act.raise_for_status()
    dump_response(act, "GET /activity/")
    debug_set_cookie(act, "GET /activity/")
    debug_cookies(s, "GET /activity/")

    if not is_logged_in_by_cookie(s):
        raise RuntimeError("Login failed")

    save_cookies(s, cookie_path)
    print(f"[OK] Logged in as {get_signed_in_user(s)}")
    return s

def _scan_cookies_for(name_substr: str, session):
    jar = getattr(getattr(session, "cookies", None), "jar", None)
    if not jar:
        raise RuntimeError("No cookie jar present")

    matches = [c for c in jar if name_substr in c.name.lower() and c.value]
    if matches:
        return matches[0]

    raise RuntimeError(f"No cookie containing '{name_substr}' found")


# ----------------------------
# UserSession
# ----------------------------

@dataclass
class UserSession:
    session: requests.Session

    def __post_init__(self):
        # Synchronize this session with the global Scraper instance
        Scraper.set_instance(self.session)

    @cached_property
    def csrf(self) -> str:
        # Fast path
        if hasattr(self.session.cookies, "get"):
            val = self.session.cookies.get(CSRF_COOKIE)
            if val:
                return val

        # Fallback scan
        c = _scan_cookies_for("csrf", self.session)
        print(f"[WARN] CSRF cookie name changed → using '{c.name}'")
        return c.value

    @cached_property
    def username(self) -> str:
        if hasattr(self.session.cookies, "get"):
            val = self.session.cookies.get(USER_COOKIE)
            if val:
                return val

        c = _scan_cookies_for("signed.in", self.session)
        print(f"[WARN] User cookie name changed → using '{c.name}'")
        return c.value

    @classmethod
    def ensure(cls, cookie_path: Path = DEFAULT_COOKIE_PATH) -> "UserSession":
        if cookie_path.exists():
            s = load_session_from_cookies(cookie_path)
            if is_logged_in_by_cookie(s):
                print("[OK] Using existing cookies")
                return cls(s)
            print("[WARN] Cookie jar invalid or expired")

        print("[ACTION] Login required")
        username = input("Letterboxd username: ").strip()
        password = getpass.getpass("Letterboxd password: ")
        s = lb_login(username, password, cookie_path)
        return cls(s)