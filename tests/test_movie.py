import unittest

from letterboxdpy.core.exceptions import MovieNotFoundError, ResourceNotFoundError
from letterboxdpy.movie import Movie


class TestMovie(unittest.TestCase):
    def setUp(self):
        self.movie = Movie("v-for-vendetta")

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


if __name__ == "__main__":
    unittest.main()
