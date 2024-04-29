from letterboxdpy.user import User, user_films_liked
import unittest


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("nmcassa")

    def test_get_all_liked_films(self):
        movies = user_films_liked(self.user)['movies']
        values = movies.values()

        self.assertTrue(all(value['liked'] for value in values))

if __name__ == '__main__':
    unittest.main()