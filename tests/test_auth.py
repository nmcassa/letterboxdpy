#!/usr/bin/env python3
"""
Minimal smoke test for user_list.UserSession

No HTML parsing
No undocumented endpoints
No special headers
Only behavior already used in user_list
"""

from pathlib import Path
from letterboxdpy.auth import UserSession, BASE_URL, DEFAULT_COOKIE_PATH


def _summarize_auth_state(us: UserSession):
    print("\n=== UserSession smoke check ===")

    # These lines validate cached_property + cookie scan fallback.
    u = us.username
    c = us.csrf

    c_prev = (c[:10] + "…") if c else "(missing)"
    print(f"[OK] username resolved from cookies: {u!r}")
    print(f"[OK] csrf resolved from cookies:     {c_prev} (len={len(c)})")

    # Reuse ONLY an endpoint already present in the module
    url = f"{BASE_URL}/activity/"
    r = us.session.get(url, allow_redirects=True)

    print(f"\n[CHECK] GET {url}")
    print(f"  status: {r.status_code}")
    print(f"  final:  {r.url}")

    if r.history:
        print("  redirects:")
        for h in r.history:
            print(f"    {h.status_code} → {h.url}")
    else:
        print("  redirects: (none)")

    if "/sign-in" in r.url or "/user/login" in r.url:
        print("[WARN] Looks unauthenticated (ended at sign-in/login). Cookies may be stale/expired.")
    else:
        print("[OK] Looks authenticated (did not end at sign-in/login).")


if __name__ == "__main__":
    us = UserSession.ensure(DEFAULT_COOKIE_PATH)
    _summarize_auth_state(us)
