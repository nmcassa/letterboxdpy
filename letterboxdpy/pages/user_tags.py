from letterboxdpy.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN


class UserTags:

    def __init__(self, username: str) -> None:
        self.username = username
        self.films_url = f"{DOMAIN}/{self.username}/tags/films"
        self.diary_url = f"{DOMAIN}/{self.username}/tags/diary"
        self.reviews_url = f"{DOMAIN}/{self.username}/tags/reviews"
        self.lists_url = f"{DOMAIN}/{self.username}/tags/lists"
        
    def get_user_tags(self) -> dict: return extract_user_tags(self.username)

def extract_user_tags(username: str) -> dict:
    BASE_URL = f"{DOMAIN}/{username}/tags"
    PAGES = ['films', 'diary', 'reviews', 'lists']

    def extract_tags(page: str) -> dict:
        """Extract tags from the page."""
        
        def fetch_dom() -> any:
            """Fetch and return the DOM for the page."""
            return parse_url(f"{BASE_URL}/{page}")

        def parse_tag(tag) -> dict:
            """Extract tag information from a single tag element."""
            name = tag.a.text.strip()
            title = tag.a['title']
            link = tag.a['href']
            slug = link.split('/')[-3]
            count = int(tag.span.text.strip() or 1)
            return {
                'name': name,
                'title': title,
                'slug': slug,
                'link': DOMAIN + link,
                'count': count,
            }

        dom = fetch_dom()
        tags_ul = dom.find("ul", {"class": "tags-columns"})
        data = {}

        if not tags_ul:
            return data

        tags = tags_ul.find_all("li")
        index = 1
        for tag in tags:
            if 'href' in tag.a.attrs:
                tag_info = parse_tag(tag)
                tag_info['no'] = index
                data[tag_info['slug']] = tag_info
                index += 1

        return data

    data = {}
    for page in PAGES:
        tags = extract_tags(page)
        data[page] = {
            'tags': tags,
            'count': len(tags)
        }

    data['total_count'] = sum(data[page]['count'] for page in PAGES)

    return data
