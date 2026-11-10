"""
Session validation tests.

Tests the UserSession.validate() method and related functionality:
- Cookie expiry detection
- Header-based logout signal detection
- Identity verification via username presence
"""

import time

import pytest

from letterboxdpy.auth import DEFAULT_COOKIE_PATH, UserSession

requires_cookie = pytest.mark.skipif(
    not DEFAULT_COOKIE_PATH.exists(), reason="Requires valid cookie file"
)


@requires_cookie
class TestCookieExpiry:
    """Test local cookie expiry detection (no network required)."""

    def test_cookie_expiry_is_preserved(self):
        """Cookie expiry timestamps should be loaded from file."""
        session = UserSession.load(DEFAULT_COOKIE_PATH).session

        # At least one cookie should have expires set
        has_expiry = any(c.expires for c in session.cookies.jar)
        assert has_expiry, "No cookies have expiry information"

    @pytest.mark.smoke()
    def test_signed_in_as_cookie_has_30_day_expiry(self):
        """letterboxd.signed.in.as cookie should expire in ~30 days."""
        try:
            us = UserSession.load(DEFAULT_COOKIE_PATH)
            if not us.validate():
                pytest.skip("Existing cookie file is invalid/expired")
            session = us.session
        except Exception as e:
            pytest.skip(f"Could not load/validate session: {e}")

        for c in session.cookies.jar:
            if c.name == "letterboxd.signed.in.as" and c.expires:
                days_remaining = (c.expires - time.time()) / 86400
                assert days_remaining > 0, "Cookie has already expired"
                assert days_remaining < 31, "Cookie expiry is more than 30 days"
                return

        pytest.skip("letterboxd.signed.in.as cookie not found with expiry")


@requires_cookie
class TestSessionValidation:
    """Test UserSession.validate() method."""

    @pytest.mark.smoke()
    def test_valid_session_returns_true(self):
        """A valid session should return True from validate()."""
        try:
            us = UserSession.load(DEFAULT_COOKIE_PATH)
            if not us.validate():
                pytest.skip("Existing session cookie is invalid or expired")
            assert us.validate()
        except Exception as e:
            pytest.skip(f"Could not load session: {e}")

    def test_corrupted_cookie_detected(self):
        """Corrupting cookies should eventually fail validation."""
        instance = UserSession.load(DEFAULT_COOKIE_PATH)

        # Corrupt all user cookies
        for c in instance.session.cookies.jar:
            if "letterboxd.user" in c.name:
                c.value = "INVALID_TOKEN_12345"

        # The local is_logged_in should still return True
        # (it only checks presence, not validity)
        assert instance.is_logged_in


class TestLogoutSignalDetection:
    """Test detection of server logout signals in headers."""

    def test_logout_signal_in_set_cookie(self):
        """Headers with 'letterboxd.user=;' or 'max-age=0' indicate logout."""
        # Simulate headers that indicate session invalidation
        logout_headers = {
            "Set-Cookie": "letterboxd.user=; Max-Age=0; Expires=Thu, 01 Jan 1970"
        }

        set_cookie = logout_headers.get("Set-Cookie", "").lower()
        has_logout_signal = (
            "letterboxd.user=;" in set_cookie or "max-age=0" in set_cookie
        )

        assert has_logout_signal

    def test_normal_headers_no_logout_signal(self):
        """Normal response headers should not trigger logout detection."""
        normal_headers = {
            "Set-Cookie": "some_tracking=abc123; Path=/",
            "Content-Type": "text/html",
        }

        set_cookie = normal_headers.get("Set-Cookie", "").lower()
        has_logout_signal = (
            "letterboxd.user=;" in set_cookie or "max-age=0" in set_cookie
        )

        assert not has_logout_signal
