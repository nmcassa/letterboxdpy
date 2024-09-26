from letterboxdpy.parser import get_movies_from_user_watched
from letterboxdpy.scraper import Scraper
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
        dom = Scraper.get_parsed_page(f"{url}/page/{page_number}/")
        return get_movies_from_user_watched(dom)

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

def extract_user_genre_info(username: str) -> dict:
    ret = {}
    for genre in GENRES:
        dom = Scraper.get_parsed_page(f"{DOMAIN}/{username}/films/genre/{genre}/")
        data = dom.find("span", {"class": ["replace-if-you"], })
        data = data.next_sibling.replace(',', '')
        try:
            ret[genre] = [int(s) for s in data.split() if s.isdigit()][0]
        except IndexError:
            ret[genre] = 0

    return ret