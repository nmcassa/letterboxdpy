"""
Trace-locked Letterboxd session + user wrapper.

All behavior is derived ONLY from captured requests:
  - GET https://letterboxd.com/sign-in/
  - POST https://letterboxd.com/user/login.do
  - Cookie-based validation

FEATURES:
  - Automatic session synchronization with global Scraper instance.
  - Interactive and programmatic authentication support via UserSession.ensure().

No undocumented endpoints.
No HTML parsing.
No speculative headers.

SECURITY NOTE:
  - Cookies are stored in JSON (plaintext) by default.
  - File permissions are restricted (chmod 600) where supported.
  - Keep your cookie files private and never commit them to public repos.
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

def is_logged_in_by_cookie(session) -> bool:
    """Check if the session has valid Letterboxd user cookies."""
    cookies = getattr(session, "cookies", None)
    jar = getattr(cookies, "jar", None)
    if jar is None:
        return False
        
    names = {c.name for c in jar}
    return any(n.startswith("letterboxd.user") for n in names) or (USER_COOKIE in names)

def get_csrf(session) -> str:
    """Extract CSRF token from session cookies."""
    # 1) Fast path
    cookies = getattr(session, "cookies", None)
    if cookies is not None:
        val = getattr(cookies, "get", lambda x: None)(CSRF_COOKIE)
        if val:
            return val

    c = _scan_cookies_for("csrf", session)
    return c.value


def get_signed_in_user(session) -> str:
    """Extract currently signed-in username from session cookies."""
    # 1) Fast path
    cookies = getattr(session, "cookies", None)
    if cookies is not None:
        val = getattr(cookies, "get", lambda x: None)(USER_COOKIE)
        if val:
            return val

    # 2) Fallback scan
    c = _scan_cookies_for("signed.in", session)
    return c.value


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
    try:
        path.chmod(0o600)
    except OSError:
        # Some systems/filesystems might not support chmod
        pass


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
    s = requests.Session(impersonate=IMPERSONATE)

    # STEP 1 — GET sign-in
    r = s.get(SIGNIN_URL, allow_redirects=True)
    r.raise_for_status()

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

    # STEP 3 — Validate
    act = s.get(f"{BASE_URL}/activity/", allow_redirects=True)
    act.raise_for_status()

    if not is_logged_in_by_cookie(s):
        raise RuntimeError("Login failed")

    save_cookies(s, cookie_path)
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
        return get_csrf(self.session)

    @cached_property
    def username(self) -> str:
        return get_signed_in_user(self.session)

    @classmethod
    def ensure(
        cls,
        cookie_path: Path = DEFAULT_COOKIE_PATH,
        username: str | None = None,
        password: str | None = None
    ) -> "UserSession":
        if cookie_path.exists():
            s = load_session_from_cookies(cookie_path)
            if is_logged_in_by_cookie(s):
                return cls(s)

        if username is None:
            username = input("Letterboxd username: ").strip()
        if password is None:
            password = getpass.getpass("Letterboxd password: ")

        s = lb_login(username, password, cookie_path)
        return cls(s)