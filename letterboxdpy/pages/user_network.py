from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.exceptions import PageFetchError
from letterboxdpy.avatar import Avatar


class UserNetwork:

    def __init__(self, username: str) -> None:
        self.username = username
        self.following_url = f"{DOMAIN}/{self.username}/following"
        self.followers_url = f"{DOMAIN}/{self.username}/followers"

    def get_following(self, page: int = 1, limit: int = None) -> dict: return extract_network(self.username, 'following', page=page, limit=limit)
    def get_followers(self, page: int = 1, limit: int = None) -> dict: return extract_network(self.username, 'followers', page=page, limit=limit)

def extract_network(username: str, section: str, limit: int = None, page: int = 1) -> dict:
    """
    Fetches the specified network section ('followers' or 'following') for the user.
    limit: Optional maximum number of pages to fetch.
    page: Optional starting page number.
    """
    assert section in ['followers', 'following'], "Section must be either 'followers' or 'following'"

    BASE_URL = f"{DOMAIN}/{username}/{section}"
    PERSONS_PER_PAGE = 25

    def fetch_page(page_num: int):
        """Fetches a single page of the user's network section."""
        try:
            return parse_url(f"{BASE_URL.rstrip('/')}/page/{page_num}/")
        except Exception as e:
            raise PageFetchError(f"Failed to fetch page {page_num}: {e}") from e

    def extract_persons(dom) -> dict:
        """Extracts persons from a DOM object and returns them as a dictionary."""
        persons_dict = {}
        
        # Find the member table
        member_table = dom.find('table', class_='member-table')
        if not member_table:
            return persons_dict
            
        # Find all user rows
        user_rows = member_table.find_all('tr')
        
        for row in user_rows:
            # Get the person summary div
            person_summary = row.find('div', class_='person-summary')
            if not person_summary:
                continue
                
            # Extract avatar info
            avatar_link = person_summary.find('a', class_='avatar')
            if not avatar_link:
                continue
                
            # Extract basic info
            username = avatar_link['href'].replace('/', '')
            avatar_img = avatar_link.find('img')
            display_name = avatar_img['alt'] if avatar_img else username
            avatar_url = avatar_img['src'] if avatar_img else ''
            
            # Process avatar with Avatar class
            avatar_data = Avatar(avatar_url).upscaled_data if avatar_url else {'exists': False, 'upscaled': False, 'url': ''}
            
            # Extract name link
            name_link = person_summary.find('a', class_='name')
            if name_link:
                display_name = name_link.get_text(strip=True)
            
            # Extract metadata (followers, following)
            metadata = person_summary.find('small', class_='metadata')
            followers_count = None
            following_count = None
            
            if metadata:
                followers_link = metadata.find('a', href=lambda x: x and 'followers' in x)
                if followers_link:
                    followers_text = followers_link.get_text(strip=True)
                    # Extract number from "5 followers"
                    import re
                    followers_match = re.search(r'(\d+)', followers_text)
                    if followers_match:
                        followers_count = int(followers_match.group(1))
                
                following_link = metadata.find('a', href=lambda x: x and 'following' in x)
                if following_link:
                    following_text = following_link.get_text(strip=True)
                    # Extract number from "following 6"
                    following_match = re.search(r'(\d+)', following_text)
                    if following_match:
                        following_count = int(following_match.group(1))
            
            # Extract stats from other columns
            watched_cell = row.find('td', class_='col-watched')
            watched_count = None
            if watched_cell:
                watched_link = watched_cell.find('a')
                if watched_link:
                    watched_text = watched_link.get_text(strip=True)
                    import re
                    watched_match = re.search(r'(\d+)', watched_text)
                    if watched_match:
                        watched_count = int(watched_match.group(1))
            
            lists_cell = row.find('td', class_='col-lists')
            lists_count = None
            if lists_cell:
                lists_link = lists_cell.find('a')
                if lists_link:
                    lists_text = lists_link.get_text(strip=True)
                    import re
                    lists_match = re.search(r'(\d+)', lists_text)
                    if lists_match:
                        lists_count = int(lists_match.group(1))
            
            likes_cell = row.find('td', class_='col-likes')
            likes_count = None
            if likes_cell:
                likes_link = likes_cell.find('a')
                if likes_link:
                    likes_text = likes_link.get_text(strip=True)
                    import re
                    likes_match = re.search(r'(\d+)', likes_text)
                    if likes_match:
                        likes_count = int(likes_match.group(1))
            
            persons_dict[username] = {
                'username': username,
                'name': display_name,
                'url': f"{DOMAIN}/{username}",
                'avatar': avatar_data,
                'followers': followers_count,
                'following': following_count,
                'watched': watched_count,
                'lists': lists_count,
                'likes': likes_count
            }

        return persons_dict

    users_list = {}
    page_num = page
    fetched_count = 0

    while True:
        if limit is not None and fetched_count >= limit:
            break

        dom = fetch_page(page_num)
        persons = extract_persons(dom)
        users_list.update(persons)

        fetched_count += 1

        # Break if the number of persons fetched is less than a full page (end of list)
        if len(persons) < PERSONS_PER_PAGE :
            break

        page_num += 1

    return users_list