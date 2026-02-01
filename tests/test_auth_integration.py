from letterboxdpy.auth import UserSession, DEFAULT_COOKIE_PATH
from letterboxdpy.user import User
from letterboxdpy.core.scraper import Scraper
import unittest


class TestAuthIntegration(unittest.TestCase):
    """
    Integration tests for library-wide session synchronization.
    
    These tests verify that UserSession correctly propagates
    authentication to other library components (Scraper, User class).
    
    For basic UserSession functionality tests, see test_auth.py
    """

    @classmethod
    def setUpClass(cls):
        cls.us = UserSession.ensure(DEFAULT_COOKIE_PATH)

    def test_scraper_sync(self):
        """Scraper.instance() must have user cookies after UserSession.ensure()."""
        scraper = Scraper.instance()
        scraper_cookies = {c.name for c in scraper.cookies.jar}
        has_user_cookie = any("user" in name.lower() for name in scraper_cookies)
        self.assertTrue(has_user_cookie, "Scraper not synchronized with UserSession")

    def test_user_class_inherits_session(self):
        """User class must automatically use the authenticated Scraper."""
        user_me = User(self.us.username)
        self.assertEqual(user_me.username, self.us.username)

    def test_protected_route_via_scraper(self):
        """Scraper.instance() must be able to access protected routes."""
        from bs4 import BeautifulSoup
        
        scraper = Scraper.instance()
        r = scraper.get("https://letterboxd.com/activity/", allow_redirects=True)
        soup = BeautifulSoup(r.text, 'lxml')
        title_tag = soup.title
        title = str(title_tag.string) if title_tag and title_tag.string else ""
        
        self.assertIn("activity stream", title.lower(), 
                      "Scraper could not access protected route - session inheritance failed")


if __name__ == '__main__':
    unittest.main()
