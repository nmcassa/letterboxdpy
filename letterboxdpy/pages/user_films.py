from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN, GENRES


class UserFilms:

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{self.username}/films"

    def get_films(self) -> dict:
        return extract_user_films(self.url)

    def get_films_rated(self, rating: float | int) -> dict:
        assert rating in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], "Invalid rating"
        url = f"{self.url}/rated/{rating}/by/date"
        return extract_user_films(url)
    
    def get_films_not_rated(self) -> dict:
        url = f"{self.url}/rated/none/by/date"
        return extract_user_films(url)

    def get_genre_info(self):
        return extract_user_genre_info(self.username)

def extract_user_films(url: str) -> dict:
    """Extracts user films and their details from the given URL"""
    FILMS_PER_PAGE = 12 * 6

    def process_page(page_number: int) -> dict:
        """Fetches and processes a page of user films."""
        dom = parse_url(f"{url}/page/{page_number}/")
        return extract_movies_from_user_watched(dom)

    def calculate_statistics(movies: dict) -> dict:
        """Calculates film statistics including liked and rating percentages."""
        liked_count = sum(movie['liked'] for movie in movies.values())
        rating_count = len([movie['rating'] for movie in movies.values() if movie['rating'] is not None])

        count = len(movies)
        liked_percentage = round(liked_count / count * 100, 2) if liked_count else 0.0
        rating_percentage = 0.0
        rating_average = 0.0

        if rating_count:
            ratings = [movie['rating'] for movie in movies.values() if movie['rating']]
            rating_percentage = round(rating_count / count * 100, 2)
            rating_average = round(sum(ratings) / rating_count, 2)

        return {
            'count': count,
            'liked_count': liked_count,
            'rating_count': rating_count,
            'liked_percentage': liked_percentage,
            'rating_percentage': rating_percentage,
            'rating_average': rating_average
        }

    movie_list = {'movies': {}}
    page = 0

    while True:
        page += 1
        movies = process_page(page)
        movie_list['movies'] |= movies

        if len(movies) < FILMS_PER_PAGE:
            stats = calculate_statistics(movie_list['movies'])
            movie_list.update(stats)
            break

    return movie_list

def extract_movies_from_user_watched(dom, max=12*6) -> dict:
    """
    supports user watched films section
    """
    def _extract_rating_and_like_status(container):
        """Parse rating and like status from viewing data spans."""
    
        def _extract_rating_from_span(span):
            """Extract rating from span using pattern matching."""
            classes = span.get('class', [])
            
            # Skip if no rating-related classes found
            if not any('rating' in cls or 'rated-' in cls for cls in classes):
                return None
            
            # Define extraction patterns (modern first, legacy as fallback)
            patterns = [
                lambda cls: cls.startswith('rated-') and cls.split('-')[-1],     # rated-X
                lambda cls: 'rating' in cls and '-' in cls and cls != 'rating' and cls.split('-')[-1]  # rating-color-X
            ]
            
            for pattern in patterns:
                for cls in classes:
                    try:
                        rating_str = pattern(cls)
                        if rating_str and rating_str.isdigit():
                            return int(rating_str)
                    except (ValueError, IndexError, AttributeError):
                        continue
                        
            return None
        
        def _extract_like_status(span):
            """Extract like status from span class."""
            return any('like' in cls for cls in span.get('class', []))

        poster_viewingdata = container.find("p", {"class": "poster-viewingdata"}) or container.p
        rating = None
        liked = False

        if poster_viewingdata and poster_viewingdata.span:
            for span in poster_viewingdata.find_all("span"):
                if rating is None:
                    rating = _extract_rating_from_span(span)
                if not liked:
                    liked = _extract_like_status(span)
        
        return rating, liked
    
    def _get_movie_details(container):
        """Extract complete movie information including rating and like status."""
        react_component = container.find("div", {"class": "react-component"}) or container.div
        if not react_component or 'data-film-id' not in react_component.attrs:
            return None
            
        rating, liked = _extract_rating_and_like_status(container)
        
        movie_slug = react_component.get('data-item-slug') or react_component.get('data-film-slug')
        movie_id = react_component['data-film-id']
        movie_name = react_component.get('data-item-name') or react_component.img['alt']

        return movie_slug, {
            'name': movie_name,
            "id": movie_id,
            "rating": rating,
            "liked": liked
        }

    def _find_movie_containers(dom):
        """Find movie containers using modern structure with legacy fallback."""
        container_selectors = [
            ("li", {"class": "griditem"}),      # Modern React structure
            ("li", {"class": "poster-container"}),  # Legacy structure
            ("li", {"class": "posteritem"})     # Liked films structure
        ]
        
        for tag, attrs in container_selectors:
            containers = dom.find_all(tag, attrs)
            if containers:
                return containers
        return []

    containers = _find_movie_containers(dom)

    movies = {}
    for container in containers:
        if len(movies) >= max:
            break
            
        movie_details = _get_movie_details(container)
        if movie_details:
            slug, data = movie_details
            movies[slug] = data

    return movies

def extract_user_genre_info(username: str) -> dict:
    ret = {}
    for genre in GENRES:
        dom = parse_url(f"{DOMAIN}/{username}/films/genre/{genre}/")
        data = dom.find("span", {"class": ["replace-if-you"], })
        data = data.next_sibling.replace(',', '')
        try:
            ret[genre] = [int(s) for s in data.split() if s.isdigit()][0]
        except IndexError:
            ret[genre] = 0

    return ret