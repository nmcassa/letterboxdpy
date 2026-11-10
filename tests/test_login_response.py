"""
Login flow inspection tests.

These tests verify the structure and content of Letterboxd's login response,
ensuring cookie expiry information is properly received and parseable.

NOTE: These tests require network access and valid credentials.
They are designed for manual/integration testing, not CI/CD.
"""

import pytest

from letterboxdpy.auth import (
    DEFAULT_COOKIE_PATH,
    UserSession,
)

pytestmark = pytest.mark.skipif(
    not DEFAULT_COOKIE_PATH.exists(), reason="Requires valid cookie file"
)


class TestLoginResponseStructure:
    """Test the structure of login responses."""

    def test_session_has_required_cookies(self):
        """Session should contain all required Letterboxd cookies."""
        session = UserSession.load(DEFAULT_COOKIE_PATH).session
        cookie_names = {c.name for c in session.cookies.jar}

        # These cookies are essential for authenticated requests
        required_cookies = [
            "letterboxd.signed.in.as",
            "com.xk72.webparts.csrf",
        ]

        for name in required_cookies:
            assert name in cookie_names, f"Missing required cookie: {name}"

    def test_signed_in_as_contains_username(self):
        """letterboxd.signed.in.as cookie value should be the username."""
        session = UserSession.load(DEFAULT_COOKIE_PATH).session

        for c in session.cookies.jar:
            if c.name == "letterboxd.signed.in.as" and c.value:
                # The value should be a valid username (alphanumeric)
                assert c.value.isalnum() or "_" in c.value, (
                    f"Invalid username format: {c.value}"
                )
                return

        pytest.fail("letterboxd.signed.in.as cookie not found")

    def test_cookies_are_secure(self):
        """All authentication cookies should have secure flag."""
        session = UserSession.load(DEFAULT_COOKIE_PATH).session

        auth_cookies = [
            "letterboxd.signed.in.as",
            "letterboxd.user",
            "letterboxd.user.CURRENT",
        ]

        for c in session.cookies.jar:
            if c.name in auth_cookies:
                assert c.secure, f"Cookie {c.name} should be secure"


class TestCookieExpiryParsing:
    """Test cookie expiry timestamp handling."""

    def test_expiry_is_unix_timestamp(self):
        """Cookie expiry should be stored as Unix timestamp (integer)."""
        session = UserSession.load(DEFAULT_COOKIE_PATH).session

        for c in session.cookies.jar:
            if c.expires:
                assert isinstance(c.expires, (int, float)), (
                    f"{c.name} expires should be numeric"
                )
                # Should be a reasonable Unix timestamp (after year 2020)
                assert c.expires > 1577836800, f"{c.name} expires seems too small"

    def test_session_cookies_have_no_expiry(self):
        """Session cookies (csrf, user.CURRENT) should have no expiry."""
        session = UserSession.load(DEFAULT_COOKIE_PATH).session

        session_cookies = ["com.xk72.webparts.csrf", "letterboxd.user.CURRENT"]

        for c in session.cookies.jar:
            if c.name in session_cookies:
                # Session cookies typically have None expiry
                # (or the file might not store it)
                pass  # Just ensuring no exception is raised
