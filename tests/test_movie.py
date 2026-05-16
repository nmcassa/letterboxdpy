"""Tests for the Movie class."""

import unittest

from letterboxdpy.core.exceptions import MovieNotFoundError, ResourceNotFoundError
from letterboxdpy.movie import Movie


class TestMovie(unittest.TestCase):
    """Integration tests for Movie scraping and factory methods."""

    @classmethod
    def setUpClass(cls):
        cls.movie = Movie("v-for-vendetta")

    def test_get_not_exists_banner_movie(self):
        instance = Movie("avatar-4")
        data = instance.banner
        self.assertIsNone(data)

    def test_get_exists_banner_movie(self):
        data = self.movie.banner
        self.assertIsNotNone(data)

    def test_get_movie_title(self):
        data = self.movie.title
        self.assertEqual(data, "V for Vendetta")

    def test_get_movie_year(self):
        data = self.movie.year
        self.assertEqual(data, 2005)

    def test_movie_original_title_nullable(self):
        data = self.movie.original_title
        self.assertIsNone(data)

    def test_non_english_movie_original_title(self):
        movie = Movie("parasite-2019")
        self.assertEqual(movie.title, "Parasite")
        self.assertIsNotNone(movie.original_title)
        self.assertNotEqual(movie.title, movie.original_title)
        self.assertEqual(movie.original_title, "기생충")

    def test_empty_init(self):
        with self.assertRaises(AssertionError):
            Movie()

    def test_movie_not_found_slug(self):
        with self.assertRaises(ResourceNotFoundError):
            Movie("this-movie-does-not-exist-999")

    def test_movie_not_found_tmdb(self):
        with self.assertRaises(MovieNotFoundError):
            Movie(tmdb=999999999)

    def test_init_tmdb(self):
        movie = Movie(tmdb=27205)
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(movie.year, 2010)
        self.assertEqual(movie.slug, "inception")
        self.assertEqual(str(movie.tmdb_id), "27205")

    def test_init_imdb(self):
        movie = Movie(imdb="tt0133093")
        self.assertEqual(movie.title, "The Matrix")
        self.assertEqual(movie.year, 1999)
        self.assertEqual(movie.slug, "the-matrix")
        self.assertEqual(movie.imdb_id, "tt0133093")

    def test_from_tmdb_factory(self):
        movie = Movie.from_tmdb(603)
        self.assertEqual(movie.slug, "the-matrix")

    def test_from_imdb_factory(self):
        movie = Movie.from_imdb("tt0133093")
        self.assertEqual(movie.slug, "the-matrix")

    def test_get_details(self):
        details = self.movie.get_details()
        expected_language = {
            "type": "language",
            "name": "English",
            "slug": "english",
            "url": "https://letterboxd.com/films/language/english/",
        }
        self.assertIn(expected_language, details)
        expected_studio = {
            "type": "studio",
            "name": "Warner Bros. Productions",
            "slug": "warner-bros-productions",
            "url": "https://letterboxd.com/studio/warner-bros-productions/",
        }
        self.assertIn(expected_studio, details)

    def test_get_genres(self):
        genres = self.movie.get_genres()
        expected_genre = {
            "type": "genre",
            "name": "Thriller",
            "slug": "thriller",
            "url": "https://letterboxd.com/films/genre/thriller/",
        }
        self.assertIn(expected_genre, genres)

    def test_get_cast(self):
        cast = self.movie.get_cast()
        expected_cast_member = {
            "name": "Natalie Portman",
            "role_name": "Evey",
            "slug": "natalie-portman",
            "url": "https://letterboxd.com/actor/natalie-portman/",
        }
        self.assertIn(expected_cast_member, cast)

    def test_get_crew(self):
        directors = self.movie.get_crew()["director"]
        expected_director = {
            "name": "James McTeigue",
            "slug": "james-mcteigue",
            "url": "https://letterboxd.com/director/james-mcteigue/",
        }
        self.assertIn(expected_director, directors)

    def test_members(self):
        stats = self.movie.get_watchers_stats()
        self.assertGreater(stats["members"], 1_500_000)
        self.assertLess(stats["members"], 3_000_000)
        self.assertGreater(stats["fans"], 15_000)
        self.assertLess(stats["fans"], 30_000)
        self.assertGreater(stats["likes"], 400_000)
        self.assertLess(stats["likes"], 800_000)
        self.assertGreater(stats["reviews"], 90_000)
        self.assertLess(stats["reviews"], 180_000)
        self.assertGreater(stats["lists"], 150_000)
        self.assertLess(stats["lists"], 300_000)


if __name__ == "__main__":
    unittest.main()
