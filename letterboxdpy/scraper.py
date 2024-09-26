if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from json import dumps as json_dumps
from bs4 import BeautifulSoup
import requests

from letterboxdpy.exceptions import PageLoadError
from letterboxdpy.constants.project import DOMAIN


class Scraper:
    """A class for scraping and parsing web pages."""

    headers = {
        "referer": DOMAIN,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    builder = "lxml"

    def __init__(self, domain: str = headers['referer'], user_agent: str = headers["user-agent"]):
        """Initialize the scraper with the specified domain and user-agent."""
        self.headers = {
            "referer": domain,
            "user-agent": user_agent
        }

    @classmethod
    def get_parsed_page(cls, url: str) -> BeautifulSoup:
        """Get and parse the HTML content from the specified URL."""
        response = cls.fetch_page(url)
        return cls.handle_response(url, response)

    @classmethod
    def fetch_page(cls, url: str) -> requests.Response:
        """Fetch the HTML content from the specified URL."""
        try:
            return requests.get(url, headers=cls.headers)
        except requests.RequestException as e:
            raise PageLoadError(url, str(e))

    @classmethod
    def handle_response(cls, url: str, response: requests.Response) -> BeautifulSoup:
        """Handle the response and check for errors."""
        if response.status_code != 200:
            message = cls.extract_error_message(response)
            raise Exception(cls.format_error_message(url, response, message))
        return cls.parse_html(response)

    @classmethod
    def extract_error_message(cls, response: requests.Response) -> str:
        """Extract the error message from the response."""
        dom = BeautifulSoup(response.text, cls.builder)
        message_section = dom.find("section", {"class": "message"})
        return message_section.strong.text if message_section else "Unknown error occurred"

    @classmethod
    def format_error_message(cls, url: str, response: requests.Response, message: str) -> str:
        """Format the error message for failed responses."""
        return json_dumps({
            'code': response.status_code,
            'reason': str(response.reason),
            'url': url,
            'message': message
        }, indent=2)

    @classmethod
    def parse_html(cls, response: requests.Response) -> BeautifulSoup:
        """Parse the HTML content from the response."""
        try:
            return BeautifulSoup(response.text, cls.builder)
        except Exception as e:
            raise Exception(f"Error parsing response: {e}")


def parse_url(url: str) -> BeautifulSoup:
    """Fetch and parse the HTML content from the specified URL using the Scraper class."""
    return Scraper.get_parsed_page(url)

def url_encode(query: str, safe: str = '') -> str:
    """URL encode the given query."""
    return requests.utils.quote(query, safe=safe)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    input_domain = ''
    while not len(input_domain.strip()):
        input_domain = input('Enter url: ')

    print(f"Parsing {input_domain}...")

    parsed_dom_class_method = parse_url(input_domain)
    print(f"Title (using class method): {parsed_dom_class_method.title.string}")

    input("Click Enter to see the DOM...")
    print(f"HTML: {parsed_dom_class_method.prettify()}")
    print("*" * 20 + "\nDone!")