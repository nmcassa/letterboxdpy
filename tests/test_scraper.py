import unittest

from bs4 import BeautifulSoup

from letterboxdpy.core.exceptions import ResourceNotFoundError
from letterboxdpy.core.scraper import Scraper, url_encode


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper("letterboxd.com")

        self.valid_film_url = "https://letterboxd.com/film/dune-part-two/"
        self.invalid_film_url = "https://letterboxd.com/film/duneparttwo/"

    def test_valid_film_url(self):
        self.assertIsInstance(self.scraper.get_page(self.valid_film_url), BeautifulSoup)

    def test_invalid_film_url(self):
        with self.assertRaises(ResourceNotFoundError):
            self.scraper.get_page(self.invalid_film_url)

    def test_url_encode(self):
        query = "Dune: Part Two"
        encoded_query = url_encode(query)
        self.assertEqual(encoded_query, "Dune%3A%20Part%20Two")


if __name__ == "__main__":
    unittest.main()
