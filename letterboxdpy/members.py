if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from json import (
    dump as json_dump,
    dumps as json_dumps,
    loads as json_loads
)
import re
from typing import List
from letterboxdpy.encoder import Encoder
from letterboxdpy.scraper import Scraper


class Members:
    """Class for handling member data from Letterboxd."""

    MEMBERS_YEAR_TOP = "https://letterboxd.com/members/popular/this/year/"
    MEMBERS_PER_PAGE = 30

    def __init__(self, url: str = ""):
        """Initialize Members with the base URL."""
        self.url = url

    def self_check_value(self, value: str) -> None:
        """Check if the value contains only valid characters."""
        if not re.match("^[A-Za-z0-9_]*$", value):
            raise ValueError(f"Invalid {self.__class__.__name__}")

    def __str__(self) -> str:
        """Return a JSON string representation of the instance."""
        return json_dumps(self, indent=2, cls=Encoder)

    def jsonify(self) -> dict:
        """Convert the instance to a JSON dictionary."""
        return json_loads(self.__str__())

# -- FUNCTIONS --

def top_users(max:int = 100) -> List:
    """Fetch the top n members from the Letterboxd popular members page."""
    # max 256 page?
    members_instance = Members()

    data = []
    page = 1
    while True:
        url = f"{members_instance.MEMBERS_YEAR_TOP}page/{page}/"
        dom = Scraper.get_parsed_page(url)

        table = dom.find_all('table', {"class": ["person-table"]})[0]
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
    with open(f'top_members_{len(data)}.json', 'w') as f:
        json_dump(data, f, indent=2)