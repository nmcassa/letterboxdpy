if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from json import dumps as json_dumps
from bs4 import BeautifulSoup
import requests

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
        try:
            response = requests.get(url, headers=cls.headers)
        except requests.RequestException as e:
            raise Exception(f"Error connecting to {url}: {e}")

        try:
            dom = BeautifulSoup(response.text, cls.builder)
        except Exception as e:
            raise Exception(f"Error parsing response from {url}: {e}")

        if response.status_code != 200:
            message = cls.extract_error_message(response)
            raise Exception(cls.format_error_message(url, response, message))
        return dom

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

    # Using the class method to get the parsed page
    parsed_dom_class_method = Scraper.get_parsed_page(input_domain)
    print(f"Title (using class method): {parsed_dom_class_method.title.string}")

    # Creating an instance of Scraper and using it to get the parsed page
    scraper_instance = Scraper(input_domain)
    parsed_dom_instance_method = scraper_instance.get_parsed_page(input_domain)
    print(f"Title (using instance method): {parsed_dom_instance_method.title.string}")

    input("Click Enter to see the DOM...")
    print(f"HTML: {parsed_dom_instance_method.prettify()}")
    print("*" * 20 + "\nDone!")