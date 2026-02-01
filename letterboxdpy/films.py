if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from letterboxdpy.utils.utils_transform import get_ajax_url
from letterboxdpy.core.decorators import assert_instance
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_url import get_page_url
from letterboxdpy.utils.movies_extractor import extract_movies_from_horizontal_list, extract_movies_from_vertical_list

class Films:
    """Fetch movies from Letterboxd based on different URLs."""
    VERTICAL_MAX = 20*5
    HORIZONTAL_MAX = 12*6

    def __init__(self, url: str, max: int = None):
        """Initialize Films class with a URL."""
        self.url = url
        self.max = max
        self.ajax_url = get_ajax_url(url)
        self._movies = None

    @property
    def movies(self) -> dict:
        """Get movies from the URL."""
        if self._movies is None:
            self._movies = self.get_movies()
        return self._movies

    @property
    def count(self) -> int:
        """Return the count of movies."""
        return len(self.movies)

    # Magic Methods
    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: str):
        return self.movies[key]

    def get_movies(self) -> dict:
        """Scrape and return a dictionary of movies from Letterboxd."""
        page = 1
        movies = {}

        while True:
            page_url = get_page_url(self.ajax_url, page)
            dom = parse_url(page_url)

            if '.com/films/' in self.url:
                # https://letterboxd.com/films/popular/
                # https://letterboxd.com/films/like/v-for-vendetta/
                new_movies = extract_movies_from_horizontal_list(dom)
                movies |= new_movies
                if len(new_movies) < self.HORIZONTAL_MAX:
                    break
            elif '.com/film/' in self.url:
                # https://letterboxd.com/film/the-shawshank-redemption/similar/
                new_movies = extract_movies_from_vertical_list(dom)
                movies |= new_movies
                if len(new_movies) < self.VERTICAL_MAX:
                    break

            if self.max and len(movies) >= self.max:
                break

            page += 1

        if self.max:
            movies = dict(list(movies.items())[:self.max])

        return movies

class Future:
    ARGS = ['name', 'release', 'release-earliest', 'rating',
          'rating-lowest', 'shortest', 'longest']

    def get_movies_with_args(args: list) -> dict:
        # by 
        pass

    def get_with_language(language: str):
        pass

    def get_with_country(country: str):
        pass

    def get_with_year(year: int):
        pass

    def get_with_actor(actor: str):
        pass

    def get_with_director(director: str):
        pass

    def get_with_writer(writer: str):
        pass

def get_upcoming_movies(max: int = None) -> dict:
    BASE_URL = "https://letterboxd.com/films/popular/this/week/upcoming/"
    return Films(BASE_URL, max).movies

@assert_instance(int)
def get_movies_by_decade(decade: int, max: int = None) -> dict:
    BASE_URL = f"https://letterboxd.com/films/ajax/popular/this/week/decade/{decade}s/"
    return Films(BASE_URL, max).movies

@assert_instance(int)
def get_movies_by_year(year: int, max: int = None) -> dict:
    BASE_URL = f"https://letterboxd.com/films/ajax/popular/this/week/year/{year}/"
    return Films(BASE_URL, max).movies

@assert_instance(str)
def get_movies_by_genre(genre: str, max: int = None) -> dict:
    """
    action, adventure, animation, comedy, crime, documentary,
    drama, family, fantasy, history, horror, music, mystery,
    romance, science-fiction, thriller, tv-movie, war, western
    """
    BASE_URL = f"https://letterboxd.com/films/ajax/genre/{genre}"
    return Films(BASE_URL, max).movies

@assert_instance(str)
def get_movies_by_service(service: str, max: int = None) -> dict:
    """
    netflix, hulu, prime-video, disney-plus, itv-play, apple-tv, 
    youtube-premium, amazon-prime-video, hbo-max, peacock, ...
    """
    BASE_URL = f"https://letterboxd.com/films/popular/this/week/on/{service}/"
    return Films(BASE_URL, max).movies

@assert_instance(str)
def get_movies_by_theme(theme: str, max: int = None) -> dict:
    BASE_URL = f"https://letterboxd.com/films/ajax/theme/{theme}"
    return Films(BASE_URL, max).movies

@assert_instance(str)
def get_movies_by_nanogenre(nanogenre: str, max: int = None) -> dict:
    BASE_URL = f"https://letterboxd.com/films/ajax/nanogenre/{nanogenre}/"
    return Films(BASE_URL, max).movies

@assert_instance(str)
def get_movies_by_mini_theme(theme: str, max: int = None) -> dict:
    BASE_URL = f"https://letterboxd.com/films/ajax/mini-theme/{theme}"
    return Films(BASE_URL, max).movies

def print_movies(movies, title=None, max_count=None):
    """Print movies in a formatted list."""
    if title:
        print(f"\n{title} -- ({len(movies)} movies)", end=f"\n{'*'*8*2*2}\n")
    for movie_no, (movie_id, movie) in enumerate(movies.items(), start=1):
        if max_count and movie_no > max_count:
            break
        print(f"{movie_no:<8} {movie_id:<8} {movie['name']}")
    print(f"{'*'*8*2*2}\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    # Movies similar to "V for Vendetta" are retrieved and printed.
    # https://letterboxd.com/films/like/v-for-vendetta/
    from letterboxdpy.movie import Movie
    movie_instance = Movie("v-for-vendetta")
    movies = movie_instance.get_similar_movies()
    print_movies(movies, title=f"Similar to {movie_instance.slug}")

    # Popular movies from the year 2027 are retrieved and displayed.
    # https://letterboxd.com/films/popular/this/week/year/2027/
    year = 2027
    movies = get_movies_by_year(year)
    print_movies(movies, title=f"Movies from {year}")
