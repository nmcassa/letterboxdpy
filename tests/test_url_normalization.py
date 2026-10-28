"""Unit tests for Letterboxd URL normalization and endpoint URL formats."""

import unittest
from unittest.mock import MagicMock, patch

from letterboxdpy.core.scraper import Scraper
from letterboxdpy.pages.movie_lists import MovieLists
from letterboxdpy.pages.movie_members import MovieMembers
from letterboxdpy.pages.movie_reviews import MovieReviews
from letterboxdpy.pages.movie_similar import MovieSimilar
from letterboxdpy.pages.user_diary import UserDiary
from letterboxdpy.pages.user_films import UserFilms
from letterboxdpy.pages.user_likes import UserLikes
from letterboxdpy.pages.user_lists import UserLists
from letterboxdpy.pages.user_network import UserNetwork
from letterboxdpy.pages.user_reviews import UserReviews
from letterboxdpy.pages.user_tags import UserTags
from letterboxdpy.pages.user_watchlist import UserWatchlist
from letterboxdpy.search import Search
from letterboxdpy.utils.utils_url import get_page_url, normalize_letterboxd_url


class TestNormalizeLetterboxdUrl(unittest.TestCase):
    """Tests for normalize_letterboxd_url function."""

    def test_plain_urls_missing_slash(self):
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/user"),
            "https://letterboxd.com/user/",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/film/dune"),
            "https://letterboxd.com/film/dune/",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com"),
            "https://letterboxd.com/",
        )

    def test_plain_urls_with_slash(self):
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/user/"),
            "https://letterboxd.com/user/",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/film/dune/"),
            "https://letterboxd.com/film/dune/",
        )

    def test_urls_with_query_params(self):
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/s/search?q=dune"),
            "https://letterboxd.com/s/search/?q=dune",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/s/search/?q=dune"),
            "https://letterboxd.com/s/search/?q=dune",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/films/popular?year=2024&sort=date"),
            "https://letterboxd.com/films/popular/?year=2024&sort=date",
        )

    def test_urls_with_fragments(self):
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/film/dune#reviews"),
            "https://letterboxd.com/film/dune/#reviews",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/film/dune/#reviews"),
            "https://letterboxd.com/film/dune/#reviews",
        )

    def test_static_asset_extensions_preserved(self):
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/avatar.jpg"),
            "https://letterboxd.com/avatar.jpg",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/export.csv"),
            "https://letterboxd.com/export.csv",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/feed.xml"),
            "https://letterboxd.com/feed.xml",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://letterboxd.com/image.png"),
            "https://letterboxd.com/image.png",
        )

    def test_short_domain(self):
        self.assertEqual(
            normalize_letterboxd_url("https://boxd.it/abc"),
            "https://boxd.it/abc/",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://boxd.it/abc/"),
            "https://boxd.it/abc/",
        )

    def test_external_urls_untouched(self):
        self.assertEqual(
            normalize_letterboxd_url("https://www.imdb.com/title/tt1234567"),
            "https://www.imdb.com/title/tt1234567",
        )
        self.assertEqual(
            normalize_letterboxd_url("https://www.themoviedb.org/movie/12345"),
            "https://www.themoviedb.org/movie/12345",
        )

    def test_invalid_and_empty_inputs(self):
        self.assertEqual(normalize_letterboxd_url(""), "")
        self.assertIsNone(normalize_letterboxd_url(None))
        self.assertEqual(normalize_letterboxd_url(12345), 12345)


class TestEndpointUrlsFormat(unittest.TestCase):
    """Tests ensuring that all endpoint classes expose canonical URLs with trailing slashes."""

    def test_user_tags_urls(self):
        tags = UserTags("testuser")
        self.assertTrue(tags.url.endswith("/"))
        self.assertTrue(tags.films_url.endswith("/"))
        self.assertTrue(tags.diary_url.endswith("/"))
        self.assertTrue(tags.reviews_url.endswith("/"))
        self.assertTrue(tags.lists_url.endswith("/"))

    def test_user_reviews_url(self):
        reviews = UserReviews("testuser")
        self.assertTrue(reviews.url.endswith("/"))

    def test_user_films_url(self):
        films = UserFilms("testuser")
        self.assertTrue(films.url.endswith("/"))

    def test_user_lists_url(self):
        lists = UserLists("testuser")
        self.assertTrue(lists.url.endswith("/"))

    def test_user_likes_urls(self):
        likes = UserLikes("testuser")
        self.assertTrue(likes._base_url.endswith("/"))
        self.assertTrue(likes.films_url.endswith("/"))
        self.assertTrue(likes.reviews_url.endswith("/"))
        self.assertTrue(likes.lists_url.endswith("/"))

    def test_user_diary_url(self):
        diary = UserDiary("testuser")
        self.assertTrue(diary.url.endswith("/"))

    def test_user_network_urls(self):
        network = UserNetwork("testuser")
        self.assertTrue(network.following_url.endswith("/"))
        self.assertTrue(network.followers_url.endswith("/"))

    def test_user_watchlist_url(self):
        watchlist = UserWatchlist("testuser")
        self.assertTrue(watchlist.url.endswith("/"))

    def test_movie_pages_urls(self):
        self.assertTrue(MovieLists("dune").url.endswith("/"))
        self.assertTrue(MovieReviews("dune").url.endswith("/"))
        self.assertTrue(MovieMembers("dune").url.endswith("/"))
        self.assertTrue(MovieSimilar("dune").url.endswith("/"))

    def test_search_url(self):
        search = Search("dune")
        self.assertTrue(search.url.endswith("/"))
        page_url = search.get_search_page_url("cursor_val")
        self.assertIn("/?", page_url)
        self.assertNotIn("//?", page_url)

    def test_get_page_url(self):
        url_page_1 = get_page_url("https://letterboxd.com/testuser/films", 1)
        self.assertEqual(url_page_1, "https://letterboxd.com/testuser/films/")
        url = get_page_url("https://letterboxd.com/testuser/films", 2)
        self.assertEqual(url, "https://letterboxd.com/testuser/films/page/2/")
        url_with_slash = get_page_url("https://letterboxd.com/testuser/films/", 2)
        self.assertEqual(url_with_slash, "https://letterboxd.com/testuser/films/page/2/")


class TestScraperNormalization(unittest.TestCase):
    """Tests verifying Scraper._fetch normalizes URLs before making HTTP requests."""

    @patch("letterboxdpy.core.scraper.requests.Session.get")
    def test_fetch_normalizes_letterboxd_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        # Call with un-slashed URL
        Scraper._fetch("https://letterboxd.com/testuser/tags")

        # Verify mock_get was called with normalized URL containing trailing slash
        called_url = mock_get.call_args[0][0]
        self.assertEqual(called_url, "https://letterboxd.com/testuser/tags/")


if __name__ == "__main__":
    unittest.main()
