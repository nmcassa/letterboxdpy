from letterboxdpy.movie import Movie
import unittest


class TestMovie(unittest.TestCase):

    def setUp(self):
        self.movie = Movie("v-for-vendetta")

    def test_get_not_exists_banner_movie(self):
        instance = Movie("avatar-4") # upcoming 2029
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
    
    
if __name__ == '__main__':
    unittest.main()