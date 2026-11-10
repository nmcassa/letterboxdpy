"""Tests for the Search class."""

import pytest

from letterboxdpy.search import Search, get_film_slug_from_title


@pytest.mark.smoke()
class TestSearch:
    """Integration tests for Search functionality."""

    movie_name = "V for Vendetta"
    q = Search(movie_name, "films")

    def test_film_search(self):
        assert len(self.q.get_results()["results"]) > 0

    def test_film_search_with_max(self):
        data = self.q.get_results(1)
        assert data["count"] == 1
        assert len(data["results"]) == 1

    def test_get_film_slug_from_title(self):
        assert get_film_slug_from_title(self.movie_name) == "v-for-vendetta"
