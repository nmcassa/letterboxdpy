from letterboxdpy.user import User
import unittest


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("nmcassa")

    def test_get_all_liked_films(self):
        movies = self.user.get_liked_films()['movies']
        values = movies.values()

        self.assertTrue(all(value['liked'] for value in values))
    
    def test_network_data(self):
        followers = self.user.get_followers()
        following = self.user.get_following()

        self.assertEqual(self.user.stats['followers'], len(followers))
        self.assertEqual(self.user.stats['following'], len(following))

if __name__ == '__main__':
    unittest.main()