import pytest

from letterboxdpy.auth import DEFAULT_COOKIE_PATH, UserSession
from letterboxdpy.core.scraper import Scraper
from letterboxdpy.user import User


@pytest.fixture(scope="module")
def us():
    if not DEFAULT_COOKIE_PATH.exists():
        pytest.skip(f"Missing cookie file: {DEFAULT_COOKIE_PATH}")

    # Load and validate session without calling interactive ensure()
    try:
        session = UserSession.load(DEFAULT_COOKIE_PATH)
        if not session.validate():
            pytest.skip("Existing session cookie is invalid or expired")
    except Exception as e:
        pytest.skip(f"Could not load session: {e}")
    return session


@pytest.mark.smoke()
@pytest.mark.usefixtures("us")
class TestAuthIntegration:
    """
    Integration tests for library-wide session synchronization.

    These tests verify that UserSession correctly propagates
    authentication to other library components (Scraper, User class).

    For basic UserSession functionality tests, see test_auth.py
    """

    def test_scraper_sync(self):
        """Scraper.instance() must have user cookies after UserSession.ensure()."""
        scraper = Scraper.instance()
        scraper_cookies = {c.name for c in scraper.cookies.jar}
        has_user_cookie = any("user" in name.lower() for name in scraper_cookies)
        assert has_user_cookie, "Scraper not synchronized with UserSession"

    def test_user_class_inherits_session(self, us):
        """User class must automatically use the authenticated Scraper."""
        user_me = User(us.username)
        assert user_me.username == us.username

    def test_protected_route_via_scraper(self):
        """Scraper.instance() must be able to access protected routes."""
        from bs4 import BeautifulSoup

        scraper = Scraper.instance()
        r = scraper.get("https://letterboxd.com/activity/", allow_redirects=True)
        soup = BeautifulSoup(r.text, "lxml")
        title_tag = soup.title
        title = str(title_tag.string) if title_tag and title_tag.string else ""

        assert "activity stream" in title.lower(), (
            "Scraper could not access protected route - session inheritance failed"
        )
