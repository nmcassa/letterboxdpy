import re
from bs4 import Tag
from typing import Dict, Literal, Optional, Union

from letterboxdpy.utils.utils_transform import month_to_index
from letterboxdpy.constants.project import DOMAIN_SHORT
from letterboxdpy.constants.selectors import PageSelectors


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

def get_body_content(dom, attribute: str) -> Optional[str]:
    """
    Extract attribute value from body tag.

    Args:
        dom: BeautifulSoup DOM object
        attribute: Body tag attribute name (e.g., 'data-owner', 'class')

    Returns:
        Attribute value from body tag or None if not found
    """
    try:
        body = dom.find('body')
        return body.get(attribute) if body else None
    except (AttributeError, KeyError):
        return None

def get_movie_count_from_meta(dom, default=None) -> int:
    # Instead of making a GET request to the last page to retrieve the number of movies,
    # which could slow down the program, an alternative approach is employed.
    # The meta description of the list page is retrieved to obtain the count of movies.

    movie_count = default

    try:
        meta_description = get_meta_content(dom, name='description')

        for item in meta_description.split(' '):
            if item[0].isdigit():
                movie_count = item
                for char in item:
                    if not char.isdigit():
                        movie_count = movie_count.replace(char, '')
                break

        movie_count = int(movie_count)
        if movie_count is not None:
            # print(f"Found the movie count in the meta description as {movie_count}.")
            return int(movie_count)
        else:
            # handle the case where no digit is found in the meta description
            print("Error: No digit found in the meta description.")
            return None
    except (AttributeError, TypeError) as e:
        print(f"Error while getting movie count from meta: {e}")
        return default

def get_list_last_page(dom, default=None) -> int:
    """
    Get the number of pages in the list (last page no).
    Note: Pagination link not created when 100 or fewer films in list.
    """
    try:
        # Find last page number from pagination container
        return int(dom.find('div', class_='paginate-pages').find_all("li")[-1].a.text)
    except AttributeError:  # No pagination (≤100 films)
        return 1
    except Exception as e:
        print(f'Error checking page count: {e}')
        return default or 1


def get_list_short_url(dom, domain=DOMAIN_SHORT, default=None) -> str:
    """
    Get the short URL of the list from input field.

    Args:
        dom: BeautifulSoup DOM object
        domain: Short domain to search for (default: DOMAIN_SHORT)
        default: Default value if short URL cannot be found

    Returns:
        Short URL as string or default value
    """
    try:
        # Find input field containing short URL
        input_field = dom.find('input', type='text', value=lambda x: x and domain in x)
        if input_field:
            return input_field.get('value')
        return default
    except Exception as e:
        print(f'Error obtaining short URL: {e}')
        return default

def is_list(dom) -> bool:
    """
    Checks if the current page is a valid Letterboxd list.

    Args:
        dom: BeautifulSoup DOM object

    Returns:
        bool: True if the page is a valid list, False otherwise
    """
    try:
        meta_content = get_meta_content(dom, property='og:type')
        return meta_content == 'letterboxd:list'
    except Exception as e:
        print(f"Error checking list type: {e}")
        return False


def catch_error_message(dom) -> Union[bool, str]:
    """
    Checks if the page contains an error message.
    Returns the error message as a string if found, False otherwise.
    """
    error_body = dom.find(*PageSelectors.ERROR_BODY)
    if error_body:
        error_section = dom.find(*PageSelectors.ERROR_MESSAGE)
        if error_section:
            err = error_section.p.get_text()
            return err.split('\n')[0].strip()
    return False

def parse_review_text(dom_element):
    """
    Parse review text from a DOM element, handling spoiler warnings.
    
    Args:
        dom_element: DOM element containing the review (BeautifulSoup element)
        
    Returns:
        tuple: (review_text, has_spoiler)
            - review_text (str): Parsed review text with spoiler warnings properly handled.
                                Returns empty string if no review content found.
            - has_spoiler (bool): True if spoiler warning is present, False otherwise.
             
    Note:
        If spoiler warning is present, skips the first paragraph.
        Otherwise includes all paragraphs starting from the first one.
    """
    if not dom_element:
        return "", False
        
    review = dom_element.find("div", {"class": ["body-text"]})
    if not review:
        return "", False
        
    spoiler = bool(review.find("p", {"class": ["contains-spoilers"]}))
    review_paragraphs = review.find_all('p')[1 if spoiler else 0:]
    review_text = '\n'.join([p.text for p in review_paragraphs])
    return review_text, spoiler

def extract_json_ld_script(dom):
    """
    Extract JSON-LD script safely from DOM.
    
    Args:
        dom: BeautifulSoup DOM object
        
    Returns:
        Parsed JSON object or None if extraction fails
        
    Example:
        >>> script_data = extract_json_ld_script(dom)
        >>> movie_rating = script_data.get('aggregateRating', {}).get('ratingValue')
    """
    from json import loads as json_loads
    
    try:
        script_elem = dom.find("script", type="application/ld+json")
        if not script_elem or not script_elem.text:
            return None
        
        script_text = script_elem.text.strip()
        
        # Handle comment format: /* ... */
        if '/*' in script_text and '*/' in script_text:
            try:
                script_text = script_text.split('*/')[1].split('/*')[0]
            except IndexError:
                return None
        
        return json_loads(script_text)
    except (ValueError, IndexError, Exception):  # ValueError covers JSONDecodeError in older Python
        return None

def extract_list_id_from_url(url: str) -> Optional[str]:
    """
    Extract list ID from a Letterboxd list URL.
    
    Args:
        url: Full URL to a Letterboxd list (e.g., 'https://letterboxd.com/user/list/name/')
        
    Returns:
        List ID as string or None if extraction fails
        
    Example:
        >>> list_id = extract_list_id_from_url('https://letterboxd.com/nmcassa/list/def-con-movie-list/')
        >>> print(list_id)  # '30052453'
    """
    from letterboxdpy.core.scraper import parse_url
    from letterboxdpy.pages.user_list import extract_list_id
    
    try:
        dom = parse_url(url)
        return extract_list_id(dom)
    except Exception as e:
        print(f"Error extracting list ID from URL: {e}")
        return None