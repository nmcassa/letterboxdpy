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

    def __init__(self, url: str = ""):
        """Initialize Members with the base URL."""
        self.url = url

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

def top_users(max:int = 100) -> List:
    """Fetch the top n members from the Letterboxd popular members page."""
    # max 256 page?
    members_instance = Members()

    data = []
    page = 1
    while True:
        url = get_page_url(members_instance.MEMBERS_YEAR_TOP, page)
        dom = parse_url(url)

        table = dom.find_all('table', {"class": ["member-table"]})[0]
        avatars = table.find_all("a", {"class": ["avatar -a40"]})

        for avatar in avatars:
            user_url = avatar['href']
            user_name = user_url.replace('/', '')
            data.append(user_name)

            if len(data) >= max:
                return data

        if len(avatars) < members_instance.MEMBERS_PER_PAGE:
            break

        page += 1

    return data

if __name__=="__main__":
    data = top_users(max=200)
    JsonFile.save(f'top_members_{len(data)}', data, indent=2)