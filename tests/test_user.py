"""Tests for the User class."""

import pytest

from letterboxdpy.user import User


@pytest.fixture(scope="module")
def user():
    return User("nmcassa")


@pytest.mark.smoke()
class TestUser:
    """Integration tests for User scraping methods."""

    def test_get_all_liked_films(self, user):
        assert all(v["liked"] for v in user.get_liked_films()["movies"].values())

    def test_network_data(self, user):
        followers = user.get_followers()
        following = user.get_following()

        assert user.stats["followers"] == len(followers)
        assert user.stats["following"] == len(following)
