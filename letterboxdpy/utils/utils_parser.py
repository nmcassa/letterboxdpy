import re
from bs4 import Tag
from typing import Dict, Literal, Optional

from letterboxdpy.utils.utils_transform import month_to_index


def try_parse(value, target_type):
    """Attempt to convert the given value to the specified target type."""
    if isinstance(value, target_type):
        return value
    
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return False

def extract_and_convert_shorthand(tag) -> int:
    """Extracts text from a tag and converts shorthand notation (e.g., '6.3K') to an integer."""
    if tag and tag.text:
        count_str = tag.text.strip().replace(',', '')
        if 'K' in count_str:
            count_str = float(count_str.replace('K', ''))
            count_str *= 1000
        return int(count_str)
    return 0

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
            'month': month_to_index(date_parts[1]),
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

def get_meta_content(dom, property: str = None, name: str = None) -> Optional[str]:
    """
    Extract content from meta tag by property or name attribute.

    Args:
        dom: BeautifulSoup DOM object
        property: Meta tag property attribute (e.g., 'og:title')
        name: Meta tag name attribute (e.g., 'description')

    Returns:
        Content of the meta tag or None if not found
    """
    try:
        if property:
            elem = dom.find('meta', attrs={'property': property})
        elif name:
            elem = dom.find('meta', attrs={'name': name})
        else:
            return None

        return elem.get('content') if elem else None
    except (AttributeError, KeyError):
        return None
