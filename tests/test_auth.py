#!/usr/bin/env python3
"""
Unit test for UserSession class.

Tests cookie loading, username/csrf resolution, and session validity.
For library-wide integration tests, see test_auth_integration.py
"""

from letterboxdpy.auth import UserSession, BASE_URL, DEFAULT_COOKIE_PATH
import unittest


class TestUserSession(unittest.TestCase):
    """Unit tests for UserSession cookie and identity resolution."""

    @classmethod
    def setUpClass(cls):
        cls.us = UserSession.ensure(DEFAULT_COOKIE_PATH)

    def test_username_resolution(self):
        """Username must be resolved from cookies."""
        self.assertTrue(self.us.username)

    def test_csrf_resolution(self):
        """CSRF token must be resolved and valid."""
        csrf = self.us.csrf
        self.assertIsNotNone(csrf)
        self.assertGreater(len(csrf), 10)

    def test_session_validity(self):
        """Session must not redirect to login page."""
        url = f"{BASE_URL}/activity/"
        response = self.us.session.get(url, allow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        final_url = str(response.url)
        self.assertNotIn("/sign-in", final_url)
        self.assertNotIn("/user/login", final_url)


if __name__ == '__main__':
    unittest.main()
