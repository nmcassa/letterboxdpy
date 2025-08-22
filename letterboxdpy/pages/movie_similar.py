from letterboxdpy.constants.project import DOMAIN


class MovieSimilar:
    """Movie similar page operations - similar movies functionality."""
    
    def __init__(self, slug: str):
        """Initialize MovieSimilar with a movie slug."""
        self.slug = slug
        self.url = f"https://letterboxd.com/films/ajax/like/{slug}"
    
    def get_similar_movies(self) -> dict:
        """Get movies similar to this movie."""
        return extract_similar_movies(self.url)


def extract_similar_movies(url: str) -> dict:
    """Extract movies similar to the given movie."""
    from letterboxdpy.films import Films  # Avoid circular import
    
    # Using the AJAX endpoint for similar movies
    return Films(url).movies

if __name__ == "__main__":
    similar_instance = MovieSimilar("v-for-vendetta")

    print(f"Movie: {similar_instance.slug}")
    for id, data in similar_instance.get_similar_movies().items():
        print(id, data)
