from letterboxdpy.user import (
    User,
    user_followers,
    user_following,
    user_films_liked
)
import unittest


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("nmcassa")

    def test_get_all_liked_films(self):
        movies = user_films_liked(self.user)['movies']
        values = movies.values()

        self.assertTrue(all(value['liked'] for value in values))
    
    def test_network_data(self):
        followers = user_followers(self.user)
        following = user_following(self.user)

        self.assertTrue(self.user.stats['followers'] == len(followers))
        self.assertTrue(self.user.stats['following'] == len(following))

if __name__ == '__main__':
    unittest.main()