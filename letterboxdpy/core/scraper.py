if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import time
from urllib.parse import quote

from bs4 import BeautifulSoup
from curl_cffi import requests as curl_requests
from curl_cffi.requests.exceptions import RequestException

from letterboxdpy.utils.utils_file import JsonFile
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.exceptions import (
    PageLoadError,
    InvalidResponseError,
    PrivateRouteError
)

DEFAULT_IMPERSONATE = "chrome124"
DEFAULT_TIMEOUT = 15
DEFAULT_MAX_RETRIES = 2
DEFAULT_BACKOFF = 0.75

DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br, zstd",
    "referer": DOMAIN,
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}


class Scraper:
    """A class for scraping and parsing web pages.

    Uses curl_cffi to impersonate a real Chrome TLS/HTTP2 fingerprint, which
    bypasses Cloudflare's JA3/JA4 fingerprinting that blocks plain `requests`.
    A single Session is reused for connection pooling and cookie persistence.
    """

    builder = "lxml"
    impersonate = DEFAULT_IMPERSONATE
    timeout = DEFAULT_TIMEOUT
    max_retries = DEFAULT_MAX_RETRIES
    backoff = DEFAULT_BACKOFF

    _session: curl_requests.Session | None = None

    def __init__(self, domain: str = DOMAIN, user_agent: str | None = None):
        """Compatibility shim: most code uses Scraper as a classmethod-only API."""
        self.headers = dict(DEFAULT_HEADERS)
        self.headers["referer"] = domain
        if user_agent:
            self.headers["user-agent"] = user_agent

    @classmethod
    def _get_session(cls) -> curl_requests.Session:
        if cls._session is None:
            session = curl_requests.Session(impersonate=cls.impersonate)
            session.headers.update(DEFAULT_HEADERS)
            cls._session = session
        return cls._session

    @classmethod
    def get_page(cls, url: str) -> BeautifulSoup:
        """Fetch, check, and parse the HTML content from the specified URL."""
        response = cls._fetch(url)
        cls._check_for_errors(url, response)
        return cls._parse_html(response)

    @classmethod
    def _fetch(cls, url: str):
        """Fetch the HTML content with retry on transient errors."""
        session = cls._get_session()
        last_exc: Exception | None = None
        for attempt in range(cls.max_retries + 1):
            try:
                response = session.get(url, timeout=cls.timeout)
            except RequestException as e:
                last_exc = e
            else:
                if response.status_code in (429, 502, 503, 504) and attempt < cls.max_retries:
                    time.sleep(cls.backoff * (2 ** attempt))
                    continue
                return response
            if attempt < cls.max_retries:
                time.sleep(cls.backoff * (2 ** attempt))
        raise PageLoadError(url, str(last_exc) if last_exc else "Request failed")

    @classmethod
    def _check_for_errors(cls, url: str, response) -> None:
        """Check the response for errors and raise an exception if found."""
        if response.status_code != 200:
            error_message = cls._get_error_message(response)
            formatted_error_messagge = cls._format_error(url, response, error_message)
            if response.status_code == 403:
                raise PrivateRouteError(formatted_error_messagge)
            raise InvalidResponseError(formatted_error_messagge)

    @classmethod
    def _get_error_message(cls, response) -> str:
        """Extract the error message from the response, if available."""
        dom = BeautifulSoup(response.text, cls.builder)
        message_section = dom.find("section", {"class": "message"})
        return message_section.strong.text if message_section else "Unknown error occurred"

    @classmethod
    def _format_error(cls, url: str, response, message: str) -> str:
        """Format the error message for logging or raising exceptions."""
        return JsonFile.stringify({
            'code': response.status_code,
            'reason': str(getattr(response, 'reason', '')),
            'url': url,
            'message': message
        }, indent=2)

    @classmethod
    def _parse_html(cls, response) -> BeautifulSoup:
        """Parse the HTML content from the response."""
        try:
            return BeautifulSoup(response.text, cls.builder)
        except Exception as e:
            raise Exception(f"Error parsing response: {e}")

    @classmethod
    def close(cls) -> None:
        """Close the shared session. Call on shutdown to release sockets."""
        if cls._session is not None:
            try:
                cls._session.close()
            finally:
                cls._session = None


def parse_url(url: str) -> BeautifulSoup:
    """Fetch and parse the HTML content from the specified URL using the Scraper class."""
    return Scraper.get_page(url)


def url_encode(query: str, safe: str = '') -> str:
    """URL encode the given query."""
    return quote(query, safe=safe)


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
