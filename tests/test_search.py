from letterboxdpy.search import Search, get_film_slug_from_title
import unittest


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.movie_name = "V for Vendetta"
        self.q = Search(self.movie_name, 'films')

    def test_film_search(self):
        data = self.q.get_results()
        self.assertGreater(len(data['results']), 0)

    def test_film_search_with_max(self):
        data = self.q.get_results(max=1)
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['results']), 1)

    def test_get_film_slug_from_title(self):
        slug = get_film_slug_from_title(self.movie_name)
        self.assertEqual(slug, 'v-for-vendetta')

if __name__ == '__main__':
    unittest.main()