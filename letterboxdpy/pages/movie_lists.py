from letterboxdpy.utils.lists_extractor import ListsExtractor
from letterboxdpy.constants.project import DOMAIN


class MovieLists:
    """Movie lists page operations - lists containing this movie."""
    
    def __init__(self, slug: str):
        """Initialize MovieLists with a movie slug."""
        self.slug = slug
        self.url = f"{DOMAIN}/film/{slug}/lists"
    
    def get_lists(self) -> dict: return ListsExtractor.from_url(self.url)