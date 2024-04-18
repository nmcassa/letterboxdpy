from letterboxdpy.movie import Movie
import unittest


class TestMovie(unittest.TestCase):

    def setUp(self):
        self.movie = Movie("v-for-vendetta")

    def test_get_movie_title(self):
        data = self.movie.title
        self.assertEqual(data, "V for Vendetta")

    def test_get_movie_year(self):
        data = self.movie.year
        self.assertEqual(data, 2005)


if __name__ == '__main__':
    unittest.main()