import re
from bs4 import Tag
from typing import Dict, Literal, Optional

MONTH_ABBREVIATIONS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

def extract_numeric_text(text: str) -> Optional[int]:
    """
    Extracts numeric characters from a string and returns them as an integer.
    Returns None if an error occurs.
    """
    try:
        numeric_value = int(re.sub(r"[^0-9]", '', text))
        return numeric_value
    except ValueError:
        return None

def parse_iso_date(iso_date_str: str) -> Dict[str, int]:
    """Parses an ISO 8601 formatted date string."""
    try:
        # ISO 8601 format example: '2025-01-01T00:00:00Z'
        date_parts = list(map(int, iso_date_str[:10].split('-')))
        return {'year': date_parts[0], 'month': date_parts[1], 'day': date_parts[2]}
    except (IndexError, ValueError) as e:
        raise ValueError(f"Error parsing ISO date format: {e}")

def parse_written_date(written_date_str: str) -> Dict[str, int]:
    """Parses a written date string (e.g., '01 Jan 2025')."""
    try:
        date_parts = written_date_str.split()
        return {
            'year': int(date_parts[2]),
            'month': MONTH_ABBREVIATIONS.index(date_parts[1]) + 1,
            'day': int(date_parts[0])
        }
    except (IndexError, ValueError) as e:
        raise ValueError(f"Error parsing written date format: {e}")

def parse_review_date(
        review_log_type: Literal['Rewatched', 'Watched', 'Added'],
        review_date: Tag) -> Dict[str, int]:
    """Parses the review date based on log type."""
    if review_log_type == 'Added':
        return parse_iso_date(review_date.time['datetime'])
    return parse_written_date(review_date.text)
