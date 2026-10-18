"""Tests for the Scraper class."""

import unittest

from bs4 import BeautifulSoup

from letterboxdpy.core.exceptions import (
    AccessDeniedError,
    PrivateRouteError,
    ResourceNotFoundError,
)
from letterboxdpy.core.scraper import Scraper, url_encode


class TestScraper(unittest.TestCase):
    """Integration tests for Scraper HTTP operations."""

    @classmethod
    def setUpClass(cls):
        cls.scraper = Scraper("letterboxd.com")
        cls.valid_film_url = "https://letterboxd.com/film/dune-part-two/"
        cls.invalid_film_url = "https://letterboxd.com/film/duneparttwo/"

    def test_valid_film_url(self):
        self.assertIsInstance(self.scraper.get_page(self.valid_film_url), BeautifulSoup)

    def test_invalid_film_url(self):
        with self.assertRaises(ResourceNotFoundError):
            self.scraper.get_page(self.invalid_film_url)

    def test_url_encode(self):
        query = "Dune: Part Two"
        encoded_query = url_encode(query)
        self.assertEqual(encoded_query, "Dune%3A%20Part%20Two")

    def test_private_route_error(self):
        url = "https://letterboxd.com/username/watchlist/"
        err = PrivateRouteError(url, "This watchlist is private")
        self.assertEqual(err.url, url)
        self.assertEqual(err.message, "This watchlist is private")
        self.assertEqual(str(err), f"This watchlist is private: {url}")

        err_default = PrivateRouteError(url)
        self.assertEqual(str(err_default), f"This resource is not public: {url}")

    def test_access_denied_error(self):
        url = "https://letterboxd.com/film/dune/"
        err = AccessDeniedError(message="Forbidden: Access denied", url=url)
        self.assertEqual(err.message, "Forbidden: Access denied")
        self.assertEqual(err.url, url)
        self.assertIn(
            "Forbidden: Access denied: https://letterboxd.com/film/dune/", str(err)
        )
        self.assertIn("Hint: If you are using a VPN or Proxy", str(err))

    def test_watchlist_url_format(self):
        """Test watchlist URL ends with a trailing slash to prevent Cloudflare 403 challenge."""
        from letterboxdpy.pages.user_watchlist import UserWatchlist

        watchlist = UserWatchlist("testuser")
        self.assertTrue(watchlist.url.endswith("/"))
        self.assertEqual(watchlist.url, "https://letterboxd.com/testuser/watchlist/")

    def test_private_resource_classified_error_message(self):
        """Test private resource WarGames quote is mapped to clean error message."""
        from unittest.mock import Mock

        fake_html = (
            '<section class="message"><p><strong>Greetings, Professor Falken. '
            "Shall we play a game?</strong><br/>The file you're attempting to access is "
            "classified...</p></section>"
        )
        fake_response = Mock()
        fake_response.text = fake_html
        fake_response.status_code = 403
        fake_response.headers = {}

        msg = Scraper._get_error_message(fake_response)
        self.assertEqual(msg, Scraper.ERR_PRIVATE_RESOURCE)


if __name__ == "__main__":
    unittest.main()
