"""Tests for the Movie class."""

import pytest

from letterboxdpy.core.exceptions import MovieNotFoundError, ResourceNotFoundError
from letterboxdpy.movie import Movie


@pytest.fixture(scope="module")
def movie():
    return Movie("v-for-vendetta")


@pytest.mark.smoke()
@pytest.mark.usefixtures("movie")
class TestMovie:
    """Integration tests for Movie scraping and factory methods."""

    def test_get_not_exists_banner_movie(self):
        assert Movie("avatar-4").banner is None

    def test_get_exists_banner_movie(self, movie):
        assert movie.banner is not None

    def test_get_movie_title(self, movie):
        assert movie.title == "V for Vendetta"

    def test_get_movie_year(self, movie):
        assert movie.year == 2005

    def test_movie_original_title_nullable(self, movie):
        assert movie.original_title is None

    def test_non_english_movie_original_title(self):
        movie = Movie("parasite-2019")
        assert movie.title == "Parasite"
        assert movie.original_title is not None
        assert movie.title != movie.original_title
        assert movie.original_title == "기생충"

    def test_empty_init(self):
        with pytest.raises(AssertionError):
            Movie()

    def test_movie_not_found_slug(self):
        with pytest.raises(ResourceNotFoundError):
            Movie("this-movie-does-not-exist-999")

    def test_movie_not_found_tmdb(self):
        with pytest.raises(MovieNotFoundError):
            Movie(tmdb=999999999)

    def test_init_tmdb(self):
        movie = Movie(tmdb=27205)
        assert movie.title == "Inception"
        assert movie.year == 2010
        assert movie.slug == "inception"
        assert str(movie.tmdb_id) == "27205"

    def test_init_imdb(self):
        movie = Movie(imdb="tt0133093")
        assert movie.title == "The Matrix"
        assert movie.year == 1999
        assert movie.slug == "the-matrix"
        assert movie.imdb_id == "tt0133093"

    def test_from_tmdb_factory(self):
        movie = Movie.from_tmdb(603)
        assert movie.slug == "the-matrix"

    def test_from_imdb_factory(self):
        movie = Movie.from_imdb("tt0133093")
        assert movie.slug == "the-matrix"

    def test_get_details(self, movie):
        details = movie.get_details()
        expected_language = {
            "type": "language",
            "name": "English",
            "slug": "english",
            "url": "https://letterboxd.com/films/language/english/",
        }
        assert expected_language in details
        expected_studio = {
            "type": "studio",
            "name": "Warner Bros. Productions",
            "slug": "warner-bros-productions",
            "url": "https://letterboxd.com/studio/warner-bros-productions/",
        }
        assert expected_studio in details

    def test_get_genres(self, movie):
        genres = movie.get_genres()
        expected_genre = {
            "type": "genre",
            "name": "Thriller",
            "slug": "thriller",
            "url": "https://letterboxd.com/films/genre/thriller/",
        }
        assert expected_genre in genres

    def test_get_cast(self, movie):
        cast = movie.get_cast()
        expected_cast_member = {
            "name": "Natalie Portman",
            "role_name": "Evey",
            "slug": "natalie-portman",
            "url": "https://letterboxd.com/actor/natalie-portman/",
        }
        assert expected_cast_member in cast

    def test_get_crew(self, movie):
        directors = movie.get_crew()["director"]
        expected_director = {
            "name": "James McTeigue",
            "slug": "james-mcteigue",
            "url": "https://letterboxd.com/director/james-mcteigue/",
        }
        assert expected_director in directors

    def test_members(self, movie):
        stats = movie.get_watchers_stats()
        assert 1_500_000 < stats["members"] < 3_000_000
        assert 15_000 < stats["fans"] < 30_000
        assert 400_000 < stats["likes"] < 800_000
        assert 90_000 < stats["reviews"] < 180_000
        assert 150_000 < stats["lists"] < 300_000

    def test_popular_reviews(self, movie):
        reviews = movie.popular_reviews
        assert isinstance(reviews, list)
        assert len(reviews) > 0
        first_review = reviews[0]
        assert {"user", "link", "rating", "likes", "review"} <= first_review.keys()
        assert isinstance(first_review["rating"], float)
        assert isinstance(first_review["likes"], int)
