import re

from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.utils.utils_parser import get_meta_content, get_movie_count_from_meta, get_body_content
from pykit.url_utils import urls_match
from letterboxdpy.utils.movies_extractor import extract_movies_from_vertical_list
from letterboxdpy.utils.date_utils import DateUtils


class ListMetaData(dict):
    """Type definition for list metadata"""
    pass


class UserList:
    LIST_PATTERN = f'{DOMAIN}/%s/list/%s'
    LIST_ITEMS_PER_PAGE = 12*5

    def __init__(self, username: str, slug: str) -> None:
        assert re.match("^[A-Za-z0-9_]+$", username), "Invalid author"

        self.username = username
        self.slug = slug
        self.url = self.LIST_PATTERN % (username, slug) 
        self.dom = parse_url(self.url)

    def __str__(self) -> str:
        return f"Not printable object of type: {self.__class__.__name__}"

    def get_title(self) -> str: return extract_title(self.dom)
    def get_author(self) -> str: return extract_author(self.dom)
    def get_description(self) -> str: return extract_description(self.dom)
    def get_date_created(self) -> list: return extract_date_created(self.dom)
    def get_date_updated(self) -> list: return extract_date_updated(self.dom)
    def get_tags(self) -> list: return extract_tags(self.dom)
    def get_movies(self) -> dict: return extract_movies(self.url, self.LIST_ITEMS_PER_PAGE)
    def get_count(self) -> int: return extract_count(self.dom)
    def get_list_id(self) -> str | None: return extract_list_id(self.dom)
    def get_list_meta(self, url: str) -> ListMetaData: return extract_list_meta(self.dom, url)

def extract_list_id(dom) -> str | None:
    """
    Extracts the list ID from the list page DOM.
    
    Args:
        dom: BeautifulSoup DOM object of the list page
        
    Returns:
        List ID as string or None if not found
    """
    try:
        # Method 1: Look for data-report-url attribute in report link
        report_link = dom.find('span', {'data-report-url': True})
        if report_link:
            report_url = report_link.get('data-report-url')
            if report_url and 'filmlist:' in report_url:
                # Extract ID from pattern like "/ajax/filmlist:30052453/report-form"
                import re
                match = re.search(r'filmlist:(\d+)', report_url)
                if match:
                    return match.group(1)
        
        # Method 2: Look for data-popmenu-id attribute
        report_menu = dom.find('a', {'data-popmenu-id': True})
        if report_menu:
            popmenu_id = report_menu.get('data-popmenu-id')
            if popmenu_id and 'list-' in popmenu_id:
                # Extract ID from pattern like "report-member-username-list-30052453"
                import re
                match = re.search(r'list-(\d+)$', popmenu_id)
                if match:
                    return match.group(1)
        
        return None
    except Exception as e:
        print(f"Error extracting list ID: {e}")
        return None

def extract_count(dom) -> int:
    """Extracts the number of films from the list DOM."""
    try:
        count = get_movie_count_from_meta(dom)
        if count is None:
            raise ValueError("Meta description not found or missing 'content' attribute.")
        return count
    except ValueError as e:
        raise RuntimeError("Failed to extract film count: " + str(e)) from e

def extract_movies(list_url: str, items_per_page) -> dict:
    data = {}

    page = 1
    while True:
        dom = parse_url(f"{list_url.rstrip('/')}/page/{page}/")
        movies = extract_movies_from_vertical_list(dom)
        data |= movies

        if len(movies) < items_per_page:
            break

        page += 1

    return data

def extract_title(dom) -> str:
    return get_meta_content(dom, property='og:title')

def extract_author(dom) -> str:
    data = dom.find("span", attrs={'itemprop': 'name'})
    data = data.text if data else None
    return data

def extract_description(dom) -> str:
    return get_meta_content(dom, property='og:description')

def extract_date_created(dom) -> str | None:
    """Extract list creation date in ISO format."""
    # Look for published date span
    data = dom.find("span", {"class": "published is-updated"})
    if not data:
        data = dom.find("span", {"class": "published"})
    
    if data:
        time_element = data.findChild("time")
        if time_element and time_element.get('datetime'):
            return DateUtils.to_iso(time_element.get('datetime'))
    
    return None

def extract_date_updated(dom) -> str | None:
    """Extract list update date in ISO format."""
    # Look for updated date span
    data = dom.find("span", {"class": "updated"})
    if not data:
        # Use published date if no separate update date
        data = dom.find("span", {"class": "published"})
    
    if data:
        time_element = data.findChild("time")
        if time_element and time_element.get('datetime'):
            return DateUtils.to_iso(time_element.get('datetime'))
    
    return None

def extract_tags(dom) -> list:
    """
    Scraping the tag links from a Letterboxd list page and
    .. extracting just the tag names into a clean list.
    The decorator ensures a valid List instance is passed.
    """
    dom = dom.find("ul", {"class": ["tags"]})

    data = []

    if dom:
        dom = dom.findChildren("a")
        for item in dom:
            data.append(item.text)

    return data

def extract_list_meta(dom, url: str) -> ListMetaData:
    """
    Extracts metadata from a Letterboxd list page.
    Args:
        dom: BeautifulSoup DOM object
        url: The original URL of the list
    Returns:
        ListMetaData: A dictionary containing list metadata and status
    """
    data: ListMetaData = {
        'url': None,
        'title': None,
        'owner': None,
        'list_id': None,
        'is_available': False,
        'error': None
    }

    try:
        # Extract basic metadata
        list_url = get_meta_content(dom, property='og:url')
        list_title = get_meta_content(dom, property='og:title')
        list_owner = get_body_content(dom, 'data-owner')
        list_id = extract_list_id(dom)

        # Check for URL redirection
        # symmetric=False: checks if url == list_url or url + "/" == list_url
        if not urls_match(url, list_url, symmetric=False):
            print(f'Redirected to {list_url}')

        # Update metadata
        data.update({
            'url': list_url,
            'title': list_title,
            'owner': list_owner,
            'list_id': list_id,
            'is_available': True
        })

    except AttributeError as e:
        data['error'] = f"Missing required metadata: {str(e)}"
        print(f"Metadata extraction error: {e}")
    except Exception as e:
        data['error'] = f"Unexpected error: {str(e)}"
        print(f"Unexpected error while checking the list: {e}")

    return data

