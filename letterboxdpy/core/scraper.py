if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import random
import time
from typing import Optional, Tuple
from urllib.parse import quote

from bs4 import BeautifulSoup, Tag
from curl_cffi import requests
from fastfingertips.terminal_utils import get_input

from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.exceptions import (
    AccessDeniedError,
    InvalidResponseError,
    PageLoadError,
    PrivateRouteError,
)
from letterboxdpy.utils.utils_file import JsonFile


class Scraper:
    """A class for scraping and parsing web pages."""

    # Error Detection Patterns
    BLOCK_KEYWORDS = [
        "cloudflare", "permission denied", "security challenge", 
        "captcha", "verify you are human", "checking your browser",
        "access denied", "ddos protection"
    ]
    
    # Standard Error Messages
    ERR_VPN_BLOCK = "IP or VPN Blocked: Letterboxd is blocking this request. Try disabling your VPN/Proxy."
    ERR_FORBIDDEN_FALLBACK = "Forbidden: Access denied. Your network might be restricted or IP is flagged."
    ERR_UNKNOWN = "Unknown error occurred"

    _session = None
    headers = {
        "referer": DOMAIN,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "connection": "keep-alive"
    }
    builder = "lxml"
    timeout = (10, 30)  # (connect, read) in seconds; set None to disable

    def __init__(self, domain: str = headers['referer'], user_agent: Optional[str] = None):
        """Initialize the scraper with the specified domain and user-agent."""
        self.headers = self.headers.copy()
        self.headers["referer"] = domain
        if user_agent:
            self.headers["user-agent"] = user_agent

    @classmethod
    def instance(cls) -> requests.Session:
        """Returns a singleton session instance."""
        if cls._session is None:
            cls._session = requests.Session()
        return cls._session

    @classmethod
    def set_instance(cls, session: requests.Session) -> None:
        """Sets the singleton session instance."""
        cls._session = session

    @classmethod
    def get_page(cls, url: str) -> BeautifulSoup:
        """Fetch, check, and parse the HTML content from the specified URL."""
        response = cls._fetch(url)
        cls._check_for_errors(url, response)
        return cls._parse_html(response)

    @classmethod
    def _fetch(cls, url: str) -> requests.Response:
        """Fetch the HTML content from the specified URL using a session with robust retry logic."""
        max_retries = 5
        last_exception = None
        response = None
        
        for attempt in range(max_retries):
            try:
                session = cls.instance()
                # Progressive timeout: increase timeout on each attempt
                current_timeout: Tuple[int, int] = (cls.timeout[0] + attempt * 2, cls.timeout[1] + attempt * 5)
                
                response = session.get(url, headers=cls.headers, timeout=current_timeout, impersonate="chrome")
                
                # Success
                if response.status_code == 200:
                    return response

                # Cloudflare or temporary block (403)
                if response.status_code == 403:
                    # If it's the first few attempts, might be a transient block, let's wait longer
                    if attempt < max_retries - 1:
                        wait = 2 * (attempt + 1) + random.random()
                        time.sleep(wait)
                        continue
                
                # Other status codes (404, 500 etc.) handled in _check_for_errors after loop
                return response

            except requests.errors.RequestsError as e:
                last_exception = e
                if attempt < max_retries - 1:
                    # Network instability (like VPN switching) needs longer waits
                    # Attempt 0: ~3s, 1: ~6s, 2: ~9s... etc.
                    wait = 3 * (attempt + 1) + random.random()
                    time.sleep(wait)
                    continue
                break
        
        if last_exception:
            raise PageLoadError(url, f"Network error ({type(last_exception).__name__}): {str(last_exception)}")
            
        if response is not None:
            return response
            
        raise PageLoadError(url, "Failed to fetch page after multiple attempts")

    @classmethod
    def _check_for_errors(cls, url: str, response: requests.Response) -> None:
        """Check the response for errors and raise an exception if found."""
        if response.status_code != 200:
            error_message = cls._get_error_message(response)
            formatted_error_message = cls._format_error(url, response, error_message)
            
            if response.status_code == 403:
                # Differentiate between VPN/IP blocks and private profiles
                is_blocked = (error_message == cls.ERR_VPN_BLOCK or 
                             error_message.startswith("Forbidden:"))
                
                if is_blocked:
                    raise AccessDeniedError(formatted_error_message)
                
                raise PrivateRouteError(formatted_error_message)
                
            raise InvalidResponseError(formatted_error_message)

    @classmethod
    def _get_error_message(cls, response: requests.Response) -> str:
        """Extract the error message from the response, if available."""
        # 1. Header-based detection (More reliable than text-matching)
        server_header = response.headers.get("Server", "").lower()
        has_cf_header = any(h in response.headers for h in ["cf-ray", "cf-cache-status"])
        
        if response.status_code == 403 and (server_header == "cloudflare" or has_cf_header):
            return cls.ERR_VPN_BLOCK

        # 2. Text-based detection (Fallback)
        if response.status_code == 403 and any(kw in response.text.lower() for kw in cls.BLOCK_KEYWORDS):
            return cls.ERR_VPN_BLOCK

        # 3. Try to find Letterboxd's official error message in the DOM
        dom = BeautifulSoup(response.text, cls.builder)
        message_section = dom.find("section", {"class": "message"})
        
        if isinstance(message_section, Tag):
            strong = message_section.find("strong")
            if strong:
                return strong.get_text()
                
        if response.status_code == 403:
             return f"{cls.ERR_FORBIDDEN_FALLBACK} URL: {response.url}"

        return cls.ERR_UNKNOWN

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
