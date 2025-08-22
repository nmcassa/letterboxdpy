"""
Shared list extraction utilities for Letterboxd list pages.
This module provides common functionality for extracting list data
from user lists, movie lists, and individual list pages.
"""

from letterboxdpy.utils.utils_parser import extract_and_convert_shorthand
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN


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
    def from_url(cls, base_url: str) -> dict:
        """
        Extract lists collection from URL.
        
        Args:
            base_url: Base URL without page parameter
            
        Returns:
            dict: Contains 'lists', 'count', 'last_page'
        """
        data = {'lists': {}}
        page = 1
        
        while True:
            list_set = cls._fetch_page_data(base_url, page)
            if not list_set:
                break

            lists = list_set.find_all(*cls.SELECTORS['lists'])
            for item in lists:
                list_data = cls._extract_list_data(item)
                data['lists'] |= list_data

            if len(lists) < cls.LISTS_PER_PAGE:
                break
            page += 1

        data['count'] = len(data['lists'])
        data['last_page'] = page

        return data
    
    @classmethod
    def _fetch_page_data(cls, base_url: str, page: int):
        """Fetch and parse page data."""
        dom = parse_url(f'{base_url}/page/{page}')
        list_set = dom.find(*cls.SELECTORS['list_set'])
        return list_set

    @classmethod
    def _extract_list_data(cls, item) -> dict:
        """Extract data from a list item."""

        def get_id() -> str:
            return item['data-film-list-id']

        def get_title() -> str:
            return item.find(*cls.SELECTORS['title']).text.strip()

        def get_description() -> str:
            description = item.find(*cls.SELECTORS['description'])
            if description:
                paragraphs = description.find_all('p')
                return '\n'.join([p.text for p in paragraphs])
            return description

        def get_url() -> str:
            return DOMAIN + item.find(*cls.SELECTORS['title']).a['href']

        def get_slug() -> str:
            return get_url().split('/')[-2]

        def get_count() -> int:
            return int(item.find(*cls.SELECTORS['value']).text.split()[0].replace(',', ''))

        def get_likes() -> int:
            likes = item.find(*cls.SELECTORS['likes'])
            likes = extract_and_convert_shorthand(likes)
            return likes

        def get_comments() -> int:
            comments = item.find(*cls.SELECTORS['comments'])
            comments = int(comments.text.split()[0].replace(',','')) if comments else 0
            return comments

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


