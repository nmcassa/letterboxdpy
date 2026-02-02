if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import re
from letterboxdpy.core.encoder import Encoder
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_file import JsonFile
from letterboxdpy.utils.utils_url import get_page_url


class Members:
    """Class for handling member data from Letterboxd."""

    MEMBERS_YEAR_TOP = "https://letterboxd.com/members/popular/this/year/"
    MEMBERS_PER_PAGE = 30

    def __init__(self, url: str = "", max: int = None):
        """Initialize Members with the base URL."""
        self.url = url or self.MEMBERS_YEAR_TOP
        self.max = max
        self._members = None

    @property
    def members(self) -> list:
        """Return the list of members."""
        if self._members is None:
            self._members = self.get_members()
        return self._members

    def get_members(self) -> list:
        """Fetch members from the provided URL."""
        data = []
        page = 1
        while True:
            url = get_page_url(self.url, page)
            dom = parse_url(url)

            tables = dom.find_all('table', {"class": ["member-table"]})
            if not tables: break

            avatars = tables[0].find_all("a", {"class": ["avatar -a40"]})

            for avatar in avatars:
                user_url = avatar['href']
                user_name = user_url.replace('/', '')
                data.append(user_name)

                if self.max and len(data) >= self.max:
                    return data

            if len(avatars) < self.MEMBERS_PER_PAGE:
                break

            page += 1

        return data

    def self_check_value(self, value: str) -> None:
        """Check if the value contains only valid characters."""
        if not re.match("^[A-Za-z0-9_]+$", value):
            raise ValueError(f"Invalid {self.__class__.__name__}")

    def __str__(self) -> str:
        """Return a JSON string representation of the instance."""
        return JsonFile.stringify(self, indent=2, encoder=Encoder)

    def jsonify(self) -> dict:
        """Convert the instance to a JSON dictionary."""
        return JsonFile.parse(self.__str__())

# -- FUNCTIONS --

def top_users(max: int = 100) -> list:
    """Fetch the top n members from the Letterboxd popular members page."""
    return Members(max=max).members

if __name__=="__main__":
    data = top_users(max=200)
    JsonFile.save(f'top_members_{len(data)}', data, indent=2)
