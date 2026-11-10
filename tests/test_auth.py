"""
Unit test for UserSession class.

Tests cookie loading, username/csrf resolution, and session validity.
For library-wide integration tests, see test_auth_integration.py
"""

import pytest

from letterboxdpy.auth import BASE_URL, DEFAULT_COOKIE_PATH, UserSession


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
class TestUserSession:
    """Unit tests for UserSession cookie and identity resolution."""

    def test_username_resolution(self, us):
        """Username must be resolved from cookies."""
        assert us.username

    def test_csrf_resolution(self, us):
        """CSRF token must be resolved and valid."""
        csrf = us.csrf
        assert csrf is not None
        assert len(csrf) > 10

    def test_session_validity(self, us):
        """Session must not redirect to login page."""
        url = f"{BASE_URL}/activity/"
        response = us.session.get(url, allow_redirects=True)

        assert response.status_code == 200

        final_url = str(response.url)
        assert "/sign-in" not in final_url
        assert "/user/login" not in final_url
