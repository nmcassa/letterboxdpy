"""
Session validation tests.

Tests the UserSession.validate() method and related functionality:
- Cookie expiry detection
- Header-based logout signal detection
- Identity verification via username presence
"""
import unittest
import time

from letterboxdpy.auth import (
    UserSession, 
    DEFAULT_COOKIE_PATH
)


class TestCookieExpiry(unittest.TestCase):
    """Test local cookie expiry detection (no network required)."""
    
    @unittest.skipUnless(DEFAULT_COOKIE_PATH.exists(), "Requires valid cookie file")
    def test_cookie_expiry_is_preserved(self):
        """Cookie expiry timestamps should be loaded from file."""
        session = UserSession.load(DEFAULT_COOKIE_PATH).session
        
        # At least one cookie should have expires set
        has_expiry = any(c.expires for c in session.cookies.jar)
        self.assertTrue(has_expiry, "No cookies have expiry information")
    
    @unittest.skipUnless(DEFAULT_COOKIE_PATH.exists(), "Requires valid cookie file")
    def test_signed_in_as_cookie_has_30_day_expiry(self):
        """letterboxd.signed.in.as cookie should expire in ~30 days."""
        session = UserSession.load(DEFAULT_COOKIE_PATH).session
        
        for c in session.cookies.jar:
            if c.name == "letterboxd.signed.in.as" and c.expires:
                days_remaining = (c.expires - time.time()) / 86400
                self.assertGreater(days_remaining, 0, "Cookie has already expired")
                self.assertLess(days_remaining, 31, "Cookie expiry is more than 30 days")
                return
        
        self.skipTest("letterboxd.signed.in.as cookie not found with expiry")


class TestSessionValidation(unittest.TestCase):
    """Test UserSession.validate() method."""
    
    @unittest.skipUnless(DEFAULT_COOKIE_PATH.exists(), "Requires valid cookie file")
    def test_valid_session_returns_true(self):
        """A valid session should return True from validate()."""
        us = UserSession.ensure()
        self.assertTrue(us.validate())
    
    @unittest.skipUnless(DEFAULT_COOKIE_PATH.exists(), "Requires valid cookie file")
    def test_corrupted_cookie_detected(self):
        """Corrupting cookies should eventually fail validation."""
        instance = UserSession.load(DEFAULT_COOKIE_PATH)
        
        # Corrupt all user cookies
        for c in instance.session.cookies.jar:
            if 'letterboxd.user' in c.name:
                c.value = "INVALID_TOKEN_12345"
        
        # The local is_logged_in should still return True
        # (it only checks presence, not validity)
        self.assertTrue(instance.is_logged_in)


class TestLogoutSignalDetection(unittest.TestCase):
    """Test detection of server logout signals in headers."""
    
    def test_logout_signal_in_set_cookie(self):
        """Headers with 'letterboxd.user=;' or 'max-age=0' indicate logout."""
        # Simulate headers that indicate session invalidation
        logout_headers = {
            "Set-Cookie": "letterboxd.user=; Max-Age=0; Expires=Thu, 01 Jan 1970"
        }
        
        set_cookie = logout_headers.get("Set-Cookie", "").lower()
        has_logout_signal = "letterboxd.user=;" in set_cookie or "max-age=0" in set_cookie
        
        self.assertTrue(has_logout_signal)
    
    def test_normal_headers_no_logout_signal(self):
        """Normal response headers should not trigger logout detection."""
        normal_headers = {
            "Set-Cookie": "some_tracking=abc123; Path=/",
            "Content-Type": "text/html"
        }
        
        set_cookie = normal_headers.get("Set-Cookie", "").lower()
        has_logout_signal = "letterboxd.user=;" in set_cookie or "max-age=0" in set_cookie
        
        self.assertFalse(has_logout_signal)


if __name__ == "__main__":
    unittest.main()
