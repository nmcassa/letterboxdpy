"""Tests for the List class."""

import unittest

from letterboxdpy.list import List


class TestList(unittest.TestCase):
    """Integration tests for List scraping methods."""

    @classmethod
    def setUpClass(cls):
        cls.list_instance = List("official", "letterboxds-top-500-films")

    def test_list_url_format(self):
        """Test list URL ends with a trailing slash to prevent 403 Forbidden errors."""
        self.assertTrue(self.list_instance.url.endswith("/"))
        self.assertEqual(
            self.list_instance.url,
            "https://letterboxd.com/official/list/letterboxds-top-500-films/",
        )

    def test_list_metadata(self):
        """Test basic metadata extraction of a list."""
        self.assertTrue(bool(self.list_instance.title))
        self.assertEqual(self.list_instance.username, "official")
        self.assertTrue(bool(self.list_instance.author))
        self.assertGreater(self.list_instance.count, 0)

    def test_list_movies(self):
        """Test movie extraction from a list."""
        movies = self.list_instance.movies
        self.assertIsInstance(movies, dict)
        self.assertGreater(len(movies), 0)

    def test_list_pagination_constants(self):
        """Test pagination constant for UserList."""
        from letterboxdpy.pages.user_list import UserList

        self.assertEqual(UserList.FILMS_PER_PAGE, 100)


if __name__ == "__main__":
    unittest.main()
