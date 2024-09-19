from json import (
    dump as json_dump,
    dumps as json_dumps,
    loads as json_loads
)
from bs4 import BeautifulSoup
import requests
import re
from typing import List
from letterboxdpy.encoder import Encoder


MEMBERS_YEAR_TOP = "https://letterboxd.com/members/popular/this/year/"

class Members:

    def __init__(self, url=""):
        self.listing_base = url

    def self_check_value(self, value):
        if not re.match("^[A-Za-z0-9_]*$", value):
            raise Exception(f"Invalid {self.__class__.__name__}")

    def __str__(self):
      return json_dumps(self, indent=2, cls=Encoder)

    def jsonify(self):
      return json_loads(self.__str__())

    def get_parsed_page(self, url: str) -> BeautifulSoup:
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://letterboxd.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

# -- FUNCTIONS --

def top_users(n: int) -> List:
    ml = Members(url=MEMBERS_YEAR_TOP)
    page = ml.get_parsed_page(ml.listing_base)

    # returns all movies
    prev = -1
    count = 1
    curr = 0
    member_list = []

    while prev != curr and curr < n:
        count += 1
        prev = len(member_list)
        popular_members_table = page.find_all('table', {"class": ["person-table"], })[0]
        avatars = popular_members_table.find_all("a", {"class": ["avatar -a40"], })

        for avatar in avatars:
            acct_path = avatar['href']
            acct = acct_path.replace('/', '')
            member_list.append(acct)

        curr = len(member_list)
        page = ml.get_parsed_page(ml.listing_base + '/page/' + str(count) + "/")

    return member_list[:n]


if __name__=="__main__":
    N = 100
    member_list = top_users(N)

    with open(f'top_2023_members_{len(member_list)}.json', 'w') as f:
        json_dump(member_list, f, indent=2)