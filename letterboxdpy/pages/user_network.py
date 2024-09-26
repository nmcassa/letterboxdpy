from letterboxdpy.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.exceptions import PageFetchError


class UserNetwork:

    def __init__(self, username: str) -> None:
        self.username = username
        self.following_url = f"{DOMAIN}/{self.username}/following"
        self.followers_url = f"{DOMAIN}/{self.username}/followers"

    def get_following(self) -> dict: return extract_network(self.username, 'following')
    def get_followers(self) -> dict: return extract_network(self.username, 'followers')

def extract_network(username: str, section: str) -> dict:
    """
    Fetches the specified network section ('followers' or 'following') for the user.
    """
    assert section in ['followers', 'following'], "Section must be either 'followers' or 'following'"

    BASE_URL = f"{DOMAIN}/{username}/{section}"
    PERSONS_PER_PAGE = 25

    def fetch_page(page_num: int):
        """Fetches a single page of the user's network section."""
        try:
            return parse_url(f"{BASE_URL}/page/{page_num}")
        except Exception as e:
            raise PageFetchError(f"Failed to fetch page {page_num}: {e}") from e

    def extract_persons(dom) -> dict:
        """Extracts persons from a DOM object and returns them as a dictionary."""
        persons = dom.find_all("img", attrs={'height': '40'})
        persons_dict = {}

        for person in persons:
            profile_url = person.parent['href'].replace('/', '')
            persons_dict[profile_url] = {'display_name': person['alt']}

        return persons_dict

    users_list = {}
    page_num = 1

    while True:
        dom = fetch_page(page_num)
        persons = extract_persons(dom)
        users_list.update(persons)

        # Break if the number of persons fetched is less than a full page (end of list)
        if len(persons) < PERSONS_PER_PAGE :
            break

        page_num += 1

    return users_list