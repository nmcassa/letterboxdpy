import re

MOVIE_TITLE_YEAR_PATTERN = re.compile(r"^(.+?)(?:\s*\((\d{4})\))?$")

def remove_prefix(text: str, prefix: str) -> str:
    """Remove a specific prefix from a string if it exists."""
    return text[len(prefix) :] if text.startswith(prefix) else text

def strip_prefix(method_name: str, prefix: str = "get_") -> str:
    """Remove the 'get_' prefix from a method name if it exists."""
    return remove_prefix(method_name, prefix)

def extract_year_from_movie_name(movie_name: str) -> int | None:
    """Extract year from movie name if it's in parentheses format.

    Example:
        extract_year_from_movie_name("The Matrix (1999)") -> 1999
        extract_year_from_movie_name("Inception") -> None
    """
    return extract_name_year_from_movie_title(movie_name)[1]

def clean_movie_name(movie_name: str) -> str:
    """Remove year from movie name if it's in parentheses format.

    Example:
        clean_movie_name("The Matrix (1999)") -> "The Matrix"
        clean_movie_name("Inception") -> "Inception"
    """
    return extract_name_year_from_movie_title(movie_name)[0]


def extract_name_year_from_movie_title(movie_name: str) -> tuple[str, int | None]:
    """Extract title and year from movie name if it's in parentheses format, else returns title and None.

    Example:
        extract_name_year_from_movie_title("The Matrix (1999)") -> ("The Matrix", 1999)
        extract_name_year_from_movie_title("The Matrix") -> ("The Matrix", None)
    """
    if movie_name is None:
        return "", None

    if (match := re.match(MOVIE_TITLE_YEAR_PATTERN, movie_name)) is not None:
        title, year = match.groups()
        return title, year if year is None else int(year)

    return movie_name, None
