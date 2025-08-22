from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN


class MovieDetails:
    """Movie details page operations - production information from /details page."""
    
    def __init__(self, slug: str):
        """Initialize MovieDetails with a movie slug."""
        self.slug = slug
        self.url = f"{DOMAIN}/film/{slug}/details"
        self.dom = parse_url(self.url)
    
    def get_extended_details(self) -> dict:
        """Get extended details (country, studio, language) from details page."""
        return extract_movie_extended_details(self.dom)
    
def extract_movie_extended_details(dom) -> dict:
    """Extract detailed movie information from details page."""
    dom_details = dom.find("div", {"id": ["tab-details"]})

    data = {
        'country': [],
        'studio': [],
        'language': []
    }

    if dom_details:
        for a in dom_details.find_all("a"):
            text = a.text.strip()
            if a['href'][1:7] == 'studio':
                data['studio'].append(text)
            elif a['href'][7:14] == 'country':
                data['country'].append(text)
            elif a['href'][7:15] == 'language':
                data['language'].append(text)

    return data

if __name__ == "__main__":
    details = MovieDetails("v-for-vendetta")
    print(details.get_extended_details())