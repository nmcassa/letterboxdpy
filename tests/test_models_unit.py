"""Unit tests for letterboxdpy/core/models.py data models."""

from letterboxdpy.core.models import Director, MovieJSON


class TestMovieJSONModel:
    """Tests for MovieJSON dataclass and from_dict parser."""

    def test_from_dict_complete_payload(self):
        payload = {
            "result": True,
            "csrf": "abc123csrf",
            "lid": "a7bx",
            "uid": "film:12345",
            "type": "film",
            "typeName": "Film",
            "id": 12345,
            "name": "Interstellar",
            "originalName": "Interstellar",
            "image125": "/resized/interstellar-125.jpg",
            "image150": "/resized/interstellar-150.jpg",
            "releaseYear": 2014,
            "runTime": 169,
            "slug": "interstellar",
            "url": "/film/interstellar/",
            "filmlistAction": "add",
            "watchlistAction": "add",
            "directors": [{"name": "Christopher Nolan"}],
        }

        movie = MovieJSON.from_dict(payload)
        assert movie.result is True
        assert movie.name == "Interstellar"
        assert movie.release_year == 2014
        assert movie.run_time == 169
        assert movie.slug == "interstellar"
        assert len(movie.directors) == 1
        assert isinstance(movie.directors[0], Director)
        assert movie.directors[0].name == "Christopher Nolan"

    def test_from_dict_sparse_or_empty_payload(self):
        movie = MovieJSON.from_dict({})
        assert movie.result is False
        assert movie.name == ""
        assert movie.release_year == 0
        assert movie.directors == []

    def test_from_dict_handles_corrupt_directors(self):
        payload = {
            "name": "Test Film",
            "directors": [
                "Not a dict",
                {"other_key": "val"},
                {"name": "Valid Director"},
            ],
        }
        movie = MovieJSON.from_dict(payload)
        assert len(movie.directors) == 1
        assert movie.directors[0].name == "Valid Director"
