"""
Trace-locked Letterboxd session + user wrapper.

All behavior is derived ONLY from captured requests:
  - GET https://letterboxd.com/sign-in/
  - POST https://letterboxd.com/user/login.do
  - Cookie-based validation

FEATURES:
  - Automatic session synchronization with global Scraper instance.
  - Interactive and programmatic authentication support via UserSession.ensure().
  - CLI usage: python -m letterboxdpy.auth --login

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
from letterboxdpy.core.exceptions import (
    LoginFailedError,
    SessionError,
    MissingCredentialsError
)
from letterboxdpy.utils.utils_file import JsonFile

from letterboxdpy.constants.project import (
    DOMAIN as BASE_URL,
    SIGNIN_URL,
    LOGIN_POST_URL,
    CSRF_COOKIE,
    USER_COOKIE,
    DEFAULT_IMPERSONATE as IMPERSONATE,
    DEFAULT_COOKIE_PATH,
    COOKIE_SET_SUPPORTED,
    SETTINGS_URL,
    ACTIVITY_URL,
    LOGOUT_INDICATORS,
    COOKIE_FILE_CHMOD,
    REMEMBER_ME
)


# ----------------------------
# Internal Utilities
# ----------------------------

def _apply_cookie_extras(jar, name, domain, fields):
    """Apply extended fields (like expires) to matching cookie."""
    for cookie in jar:
        if cookie.name == name and cookie.domain == domain:
            for key, val in fields.items():
                if val is not None:
                    setattr(cookie, key, val)
            return

def _scan_cookies_for(name_substr: str, session):
    jar = getattr(getattr(session, "cookies", None), "jar", None)
    if not jar:
        raise SessionError("No cookie jar present")
    
    matches = [c for c in jar if name_substr in c.name.lower() and c.value]
    if matches:
        return matches[0]

    raise SessionError(f"No cookie containing '{name_substr}' found")

# ----------------------------
# UserSession
# ----------------------------

@dataclass
class UserSession:
    session: requests.Session

    def __post_init__(self):
        # Synchronize this session with the global Scraper instance
        Scraper.set_instance(self.session)

    @property
    def is_logged_in(self) -> bool:
        """Lightweight local check for authentication cookies."""
        jar = getattr(self.session.cookies, "jar", [])
        names = {c.name for c in jar}
        return any(n.startswith("letterboxd.user") for n in names) or (USER_COOKIE in names)

    def save(self, path: Path = DEFAULT_COOKIE_PATH):
        """Save current session to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        
        cookies = [{
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "secure": bool(c.secure),
            "expires": c.expires,
        } for c in self.session.cookies.jar]
        
        JsonFile.save(str(path), cookies)
        try:
            path.chmod(COOKIE_FILE_CHMOD)
        except OSError:
            pass

    @classmethod
    def load(cls, path: Path = DEFAULT_COOKIE_PATH) -> "UserSession":
        """Load session from disk and return a UserSession instance."""
        s = requests.Session(impersonate=IMPERSONATE)
        cookies = JsonFile.load(str(path))
        
        for c in cookies or []:
            set_kwargs = {k: v for k, v in c.items() if k in COOKIE_SET_SUPPORTED}
            extra = {k: v for k, v in c.items() if k not in COOKIE_SET_SUPPORTED}
            
            s.cookies.set(**set_kwargs)
            
            if extra:
                _apply_cookie_extras(s.cookies.jar, c["name"], c["domain"], extra)
        
        return cls(s)

    @classmethod
    def login(cls, username: str, password: str, path: Path = DEFAULT_COOKIE_PATH) -> "UserSession":
        """Perform a fresh login and return a UserSession instance."""
        if not username or not password:
             raise MissingCredentialsError("Username and password are required")

        s = requests.Session(impersonate=IMPERSONATE)

        # STEP 1 — GET sign-in
        r = s.get(SIGNIN_URL, allow_redirects=True)
        r.raise_for_status()

        csrf = s.cookies.get(CSRF_COOKIE)
        if not csrf:
            raise SessionError("Missing CSRF cookie")

        # STEP 2 — POST login
        form = {
            "__csrf": csrf,
            "username": username,
            "password": password,
            "remember": REMEMBER_ME,
        }
        headers = {"Referer": SIGNIN_URL, "Origin": BASE_URL}

        pr = s.post(LOGIN_POST_URL, data=form, headers=headers, allow_redirects=True)
        pr.raise_for_status()

        # STEP 3 — Initial Validation
        act = s.get(ACTIVITY_URL, allow_redirects=True)
        act.raise_for_status()

        instance = cls(s)
        if not instance.is_logged_in:
             raise LoginFailedError("Login failed: Session not active")

        instance.save(path)
        return instance

    def validate(self) -> bool:
        """Return False only when session is CERTAINLY invalid."""
        import time
        
        def is_cookie_expired() -> bool:
            """Check if the session cookie has passed its expiry date."""
            for c in self.session.cookies.jar:
                if c.name == USER_COOKIE and c.expires:
                    return time.time() > c.expires
            return False  # No expiry info = assume valid
        
        def has_logout_signal(headers) -> bool:
            """Check if server is telling us to clear cookies."""
            set_cookie = headers.get("Set-Cookie", "").lower()
            return any(sig in set_cookie for sig in LOGOUT_INDICATORS)

        def is_cookie_causing_error() -> bool:
            """When we got a server error, check if a clean session works."""
            clean = requests.Session(impersonate=IMPERSONATE)
            clean_resp = clean.get(BASE_URL, allow_redirects=True)
            return clean_resp.status_code == 200

        # NOTE: Body check can be added for stricter validation:
        # def has_identity(text) -> bool:
        #     return self.username in text

        # Fast path: Check local cookie expiry (no network needed)
        if is_cookie_expired():
            return False

        try:
            # Letterboxd serves login content on the same URL instead of redirecting (302),
            # making simple status code checks unreliable.
            resp = self.session.get(SETTINGS_URL, allow_redirects=True)
            
            if resp.status_code == 200:
                return not has_logout_signal(resp.headers)
            
            if resp.status_code >= 500:
                return not is_cookie_causing_error()
            
            return True  # Uncertain cases
        except Exception:
            return True

    @cached_property
    def csrf(self) -> str:
        """Extract CSRF token from session cookies."""
        # 1) Fast path
        val = self.session.cookies.get(CSRF_COOKIE)
        if val:
            return val
        # 2) Fallback scan
        return _scan_cookies_for("csrf", self.session).value

    @cached_property
    def username(self) -> str:
        """Extract currently signed-in username from session cookies."""
        # 1) Fast path
        val = self.session.cookies.get(USER_COOKIE)
        if val:
            return val
        # 2) Fallback scan
        return _scan_cookies_for("signed.in", self.session).value

    @classmethod
    def ensure(
        cls,
        cookie_path: Path = DEFAULT_COOKIE_PATH,
        username: str | None = None,
        password: str | None = None
    ) -> "UserSession":
        if cookie_path.exists():
            instance = cls.load(cookie_path)
            if instance.validate():
                return instance

        if username is None:
            username = input("Letterboxd username: ").strip()
        if password is None:
            password = getpass.getpass("Letterboxd password: ")

        return cls.login(username, password, cookie_path)


# ----------------------------
# CLI Entry Point
# ----------------------------

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Letterboxd Session Manager")
    parser.add_argument("--login", action="store_true", help="Force login prompts")
    parser.add_argument("--path", type=Path, default=DEFAULT_COOKIE_PATH, help="Cookie storage path")
    parser.add_argument("-u", "--username", help="Letterboxd username or email")
    
    args = parser.parse_args()

    try:
        if args.login:
            # Force re-authentication
            username = args.username or input("Letterboxd username: ").strip()
            password = getpass.getpass("Letterboxd password: ")
            
            print(f"Logging in as {username}...")
            session = UserSession.login(username, password, args.path)
            print(f"[OK] Session saved to {args.path}")
        else:
            # Normal ensure check (load if exists, else prompt)
            print(f"Checking session at {args.path}...")
            session = UserSession.ensure(args.path, username=args.username)
            print(f"[OK] Authenticated as {session.username}")
            
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)