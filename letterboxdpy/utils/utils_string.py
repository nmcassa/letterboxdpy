def remove_prefix(text: str, prefix: str) -> str:
    """Remove a specific prefix from a string if it exists."""
    return text[len(prefix):] if text.startswith(prefix) else text

def strip_prefix(method_name: str, prefix: str = 'get_') -> str:
    """Remove the 'get_' prefix from a method name if it exists."""
    return remove_prefix(method_name, prefix)

def extract_year_from_movie_name(movie_name: str) -> int | None:
    """Extract year from movie name if it's in parentheses format.
    
    Example:
        extract_year_from_movie_name("The Matrix (1999)") -> 1999
        extract_year_from_movie_name("Inception") -> None
    """
    import re
    YEAR_PATTERN = r'\((\d{4})\)'
    match = re.search(YEAR_PATTERN, movie_name or '')
    return int(match.group(1)) if match else None

def clean_movie_name(movie_name: str) -> str:
    """Remove year from movie name if it's in parentheses format.
    
    Example:
        clean_movie_name("The Matrix (1999)") -> "The Matrix"
        clean_movie_name("Inception") -> "Inception"
    """
    import re
    YEAR_PATTERN = r'\((\d{4})\)'
    return re.sub(YEAR_PATTERN, '', movie_name or '').strip()