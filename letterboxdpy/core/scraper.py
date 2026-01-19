if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from bs4 import BeautifulSoup, Tag
import requests
from urllib.parse import quote

from letterboxdpy.utils.utils_file import JsonFile
from pykit.terminal_utils import get_input
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.exceptions import (
    PageLoadError,
    InvalidResponseError,
    PrivateRouteError
)

class Scraper:
    """A class for scraping and parsing web pages."""

    headers = {
        "referer": DOMAIN,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    builder = "lxml"
    timeout = (10, 30)  # (connect, read) in seconds; set None to disable

    def __init__(self, domain: str = headers['referer'], user_agent: str = headers["user-agent"]):
        """Initialize the scraper with the specified domain and user-agent."""
        self.headers = {
            "referer": domain,
            "user-agent": user_agent
        }

    @classmethod
    def get_page(cls, url: str) -> BeautifulSoup:
        """Fetch, check, and parse the HTML content from the specified URL."""
        response = cls._fetch(url)
        cls._check_for_errors(url, response)
        return cls._parse_html(response)

    @classmethod
    def _fetch(cls, url: str) -> requests.Response:
        """Fetch the HTML content from the specified URL."""
        try:
            return requests.get(url, headers=cls.headers, timeout=cls.timeout)
        except requests.RequestException as e:
            raise PageLoadError(url, str(e))

    @classmethod
    def _check_for_errors(cls, url: str, response: requests.Response) -> None:
        """Check the response for errors and raise an exception if found."""
        if response.status_code != 200:
            error_message = cls._get_error_message(response)
            formatted_error_messagge = cls._format_error(url, response, error_message)
            if response.status_code == 403:
                raise PrivateRouteError(formatted_error_messagge)
            raise InvalidResponseError(formatted_error_messagge)

    @classmethod
    def _get_error_message(cls, response: requests.Response) -> str:
        """Extract the error message from the response, if available."""
        dom = BeautifulSoup(response.text, cls.builder)
        message_section = dom.find("section", {"class": "message"})
        
        if isinstance(message_section, Tag):
            strong = message_section.find("strong")
            if strong:
                return strong.get_text()
                
        return "Unknown error occurred"

    @classmethod
    def _format_error(cls, url: str, response: requests.Response, message: str) -> str:
        """Format the error message for logging or raising exceptions."""
        return JsonFile.stringify({
            'code': response.status_code,
            'reason': str(response.reason),
            'url': url,
            'message': message
        }, indent=2)

    @classmethod
    def _parse_html(cls, response: requests.Response) -> BeautifulSoup:
        """Parse the HTML content from the response."""
        try:
            return BeautifulSoup(response.text, cls.builder)
        except Exception as e:
            raise InvalidResponseError(f"Error parsing response: {e}")

def parse_url(url: str) -> BeautifulSoup:
    """Fetch and parse the HTML content from the specified URL using the Scraper class."""
    return Scraper.get_page(url)

def url_encode(query: str, safe: str = '') -> str:
    """URL encode the given query."""
    return quote(query, safe=safe)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8') # type: ignore

    input_domain = ''
    while not len(input_domain.strip()):
        input_domain = get_input('Enter url: ', index=0)

    print(f"Parsing {input_domain}...")

    parsed_dom = parse_url(input_domain)
    
    title_text = "No Title"
    if parsed_dom.title and parsed_dom.title.string:
        title_text = parsed_dom.title.string
        
    print(f"Title: {title_text}")

    input("Click Enter to see the DOM...")
    print(f"HTML: {parsed_dom.prettify()}")
    print("*" * 20 + "\nDone!")