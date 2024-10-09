from letterboxdpy.utils.utils_parser import extract_and_convert_shorthand
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN


class UserLists:

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{self.username}/lists"
        
    def get_lists(self) -> dict: return extract_user_lists(self.username)

def extract_user_lists(username: str) -> dict:
    BASE_URL = f"{DOMAIN}/{username}/lists/"
    LISTS_PER_PAGE = 12
    SELECTORS = {
        'list_set': ('section', {'class': 'list-set'}),
        'lists': ('section', {'class': 'list'}),
        'title': ('h2', {'class': 'title'}),
        'description': ('div', {'class': 'body-text'}),
        'value': ('small', {'class': 'value'}),
        'likes': ('a', {'class': 'icon-like'}),
        'comments': ('a', {'class': 'icon-comment'}),
    }

    def fetch_page_data(page: int) -> dict:
        """Fetch and parse page data."""
        dom = parse_url(f'{BASE_URL}/page/{page}')
        list_set = dom.find(*SELECTORS['list_set'])
        return list_set

    def extract_list_data(item) -> dict:
        """Extract data from a list item."""

        def get_id() -> str:
            return item['data-film-list-id']

        def get_title() -> str:
            return item.find(*SELECTORS['title']).text.strip()

        def get_description() -> str:
            description = item.find(*SELECTORS['description'])
            if description:
                paragraphs = description.find_all('p')
                return '\n'.join([p.text for p in paragraphs])
            return description

        def get_url() -> str:
            return DOMAIN + item.find(*SELECTORS['title']).a['href']

        def get_slug() -> str:
            return get_url().split('/')[-2]

        def get_count() -> int:
            return int(item.find(*SELECTORS['value']).text.split()[0].replace(',', ''))

        def get_likes() -> int:
            likes = item.find(*SELECTORS['likes'])
            likes = extract_and_convert_shorthand(likes)
            return likes

        def get_comments() -> int:
            comments = item.find(*SELECTORS['comments'])
            comments = int(comments.text.split()[0].replace(',','')) if comments else 0
            return comments

        return {
             get_id(): {
                'title': get_title(),
                'slug': get_slug(),
                'description': get_description(),
                'url': get_url(),
                'count': get_count(),
                'likes': get_likes(),
                'comments': get_comments()
                }
            }

    data = {'lists': {}}
    page = 1
    while True:
        list_set = fetch_page_data(page)
        if not list_set:
            break

        lists = list_set.find_all(*SELECTORS['lists'])
        for item in lists:
            list_data = extract_list_data(item)
            data['lists'] |= list_data

        if len(lists) < LISTS_PER_PAGE:
            break
        page += 1

    data['count'] = len(data['lists'])
    data['last_page'] = page

    return data
