"""
Shared list extraction utilities for Letterboxd list pages.
This module provides common functionality for extracting list data
from user lists, movie lists, and individual list pages.
"""

from letterboxdpy.utils.utils_parser import extract_and_convert_shorthand
from pykit.string_utils import extract_number_from_text
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.utils.utils_url import extract_path_segment, get_page_url


class ListsExtractor:
    """Common lists collection extraction functionality.
    
    Extracts collections of lists from Letterboxd pages:
    - User's created lists
    - Lists containing a specific movie
    - Popular lists containing a movie
    """
    
    # Shared selectors for all list types
    SELECTORS = {
        'list_set': ('section', {'class': 'list-set'}),
        'lists': ('section', {'class': 'list'}),
        'title': ('h2', {'class': 'title'}),
        'description': ('div', {'class': 'body-text'}),
        'value': ('span', {'class': 'value'}),
        'likes': ('a', {'class': 'icon-like'}),
        'comments': ('a', {'class': 'icon-comment'}),
    }
    
    LISTS_PER_PAGE = 12
    
    @classmethod
    def from_url(cls, base_url: str, max_lists: int | None = None) -> dict:
        """
        Extract lists collection from URL.
        
        Args:
            base_url: Base URL without page parameter
            max_lists: Maximum number of lists to return (optional limit)
            
        Returns:
            dict: Contains 'lists', 'count', 'last_page'
        """
        data = {'limit': max_lists, 'count': 0, 'last_page': 1, 'lists': {}}
        page = 1
        
        while True:
            lists = cls._fetch_page_data(base_url, page)
            
            if not lists:
                break

            for item in lists:
                list_data = cls._extract_list_data(item)
                data['lists'] |= list_data

                if max_lists and len(data['lists']) >= max_lists:
                    # Limit reached
                    data['limit'] = True
                    break

            if data['limit'] or len(lists) < cls.LISTS_PER_PAGE:
                # Is last page or limit reached
                break

            page += 1

        data['count'] = len(data['lists'])
        data['last_page'] = page

        return data

    @classmethod
    def _fetch_page_data(cls, base_url: str, page: int):
        """Fetch and parse page data."""
        dom = parse_url(get_page_url(base_url, page))
        return dom.find_all('article', {'class': 'list-summary'})

    @classmethod
    def _extract_list_data(cls, item) -> dict:
        """Extract data from a list item."""

        def get_id() -> str:
            return item['data-film-list-id']

        def get_title() -> str:
            title_elem = item.find('h2', {'class': 'name'})
            return title_elem.text.strip()

        def get_description() -> str:
            description = item.find('div', {'class': ['notes', 'body-text']})
            if description:
                paragraphs = description.find_all('p')
                return '\n'.join([p.text for p in paragraphs])
            return ""

        def get_url() -> str:
            title_elem = item.find('h2', {'class': 'name'})
            return DOMAIN + title_elem.a['href']

        def get_slug() -> str | None:
            """
            extract list slug from url.
            example: 'https://letterboxd.com/user/list/my-list/' -> 'my-list'
            """
            return extract_path_segment(get_url(), after='/list/')

        def get_count() -> int:
            value_elem = item.find(*cls.SELECTORS['value'])
            if value_elem:
                # join=True: extracts and joins all digits (e.g. '1,234 films' -> 1234)
                count = extract_number_from_text(value_elem.text, join=True)
                return count if count is not None else 0
            return 0

        def get_likes() -> int:
            likes = item.find(*cls.SELECTORS['likes'])
            if likes:
                likes = extract_and_convert_shorthand(likes)
                return likes
            return 0

        def get_comments() -> int:
            comments = item.find(*cls.SELECTORS['comments'])
            if comments:
                return extract_and_convert_shorthand(comments)
            return 0

        return {
             get_id(): {
                'title': get_title(),
                'slug': get_slug(),
                'description': get_description(),
                'url': get_url(),
                'count': get_count(),
                'likes': get_likes(),
                'comments': get_comments()
                }
            }


