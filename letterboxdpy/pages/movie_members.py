from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from fastfingertips.string_utils import extract_number_from_text


class MovieMembers:
    """Movie members page operations - watchers statistics."""
    
    def __init__(self, slug: str):
        """Initialize MovieMembers with a movie slug."""
        self.slug = slug        
        self.url = f"{DOMAIN}/film/{slug}/members"
        self.dom = parse_url(self.url)
    
    def get_watchers_stats(self) -> dict:
        """Get movie watchers' statistics."""
        return extract_movie_watchers_stats(self.dom)

# TODO: /fans, /likes, /reviews, /lists

def extract_movie_watchers_stats(dom) -> dict:
    """Extract movie watchers' statistics from members page."""
    try:
        # Extract watchers data from DOM.
        stats = {}
        content_nav = dom.find("div", {"id": "content-nav"})
        if content_nav:
            for a in content_nav.find_all("a", title=True):
                a_text = a.text.strip().lower()
                a_title = a['title']
                # join=True: extracts and joins all digits (e.g. '1,902 members' -> 1902)
                count = extract_number_from_text(a_title, join=True)
                stats[a_text] = count
        return stats
    except Exception as e:
        raise RuntimeError("Failed to retrieve movie watchers' statistics") from e

if __name__ == "__main__":
    members_instance = MovieMembers("v-for-vendetta")

    print(f"Movie: {members_instance.slug}")
    for key, value in members_instance.get_watchers_stats().items():
        print(f"{key}: {value}")
