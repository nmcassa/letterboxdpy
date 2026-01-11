from letterboxdpy.constants.project import LETTERBOXD_COLUMNS


def create_movie_data(**kwargs) -> dict:
    """
    Create movie data dictionary following Letterboxd import format.

    Supports all official Letterboxd CSV import fields:
    https://letterboxd.com/about/importing-data/

    Args:
        **kwargs: Movie data fields (letterboxd_uri, title, year, rating, etc.)

    Returns:
        dict: Filtered movie data with Letterboxd column names
    """
    def _is_valid_value(value):
        """Check if value is valid for Letterboxd import."""
        return value and isinstance(value, (str, int, bool))

    movie_data = {}
    for field_name, value in kwargs.items():
        if field_name in LETTERBOXD_COLUMNS and _is_valid_value(value):
            column_name = LETTERBOXD_COLUMNS[field_name]
            movie_data[column_name] = value

    return movie_data


def transform_to_ranked_movies(letterboxd_movies: dict) -> list:
    """
    Transform letterboxd movies to ranked list format.

    Args:
        letterboxd_movies: Dictionary of movies from letterboxdpy

    Returns:
        List of movies with rank, title, and URI
    """
    movies = []
    for rank, (_, movie_data) in enumerate(letterboxd_movies.items(), 1):
        movie = {
            "Rank": rank,
            "Title": movie_data.get('name', ''),
            "LetterboxdURI": movie_data.get('url', '')
        }
        movies.append(movie)
    return movies
