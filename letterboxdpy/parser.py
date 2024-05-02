from bs4 import BeautifulSoup

def get_movies_from_user_watched(dom: BeautifulSoup, max=12*6) -> dict:
    """
    supports user watched films section
    """
    poster_containers = dom.find_all("li", {"class": ["poster-container"]})

    movies = {}
    for poster_container in poster_containers:
        poster = poster_container.div
        poster_viewingdata = poster_container.p
        rating = None
        liked = False

        if poster_viewingdata.span:
            for span in poster_viewingdata.find_all("span"):
                if 'rating' in span['class']:
                    rating = int(poster_viewingdata.span['class'][-1].split('-')[-1])
                elif 'like' in span['class']:
                    liked = True

        movies[poster["data-film-slug"]] = {
            'name': poster.img["alt"],
            "id": poster["data-film-id"],
            "rating": rating,
            "liked": liked
        }

    return movies

def get_movies_from_vertical_list(dom: BeautifulSoup, max=20*5) -> dict:
    """
    supports all vertical lists
    ... users' watchlists, users' lists, ...
    """
    items = dom.find_all("div", {"class": "film-poster"})

    movies = {}
    for item in items:
        movie_id = item['data-film-id']
        movie_slug = item['data-film-slug'] 
        movie_name = item.img['alt']

        movies[movie_id] = {
            "slug": movie_slug,
            "name": movie_name,
            'url': f'https://letterboxd.com/film/{movie_slug}/'
        }

    return movies

def get_movies_from_horizontal_list(dom: BeautifulSoup, max=12*6) -> dict:
    """
    supports all horizontal lists
    ... films section, ...
    """
    items = dom.find_all("li")

    movies = {}
    for item in items:
        rating_key = "data-average-rating"
        movie_rating = float(
            item['data-average-rating']) if rating_key in item.attrs else None
        movie_id = item.div['data-film-id']
        movie_slug = item.div['data-film-slug'] 
        movie_name = item.img['alt']

        movies[movie_id] = {
            "slug": movie_slug,
            "name": movie_name,
            "rating": movie_rating,
            'url': f'https://letterboxd.com/film/{movie_slug}/'
        }

    return movies

if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0] + '/..')
    from letterboxdpy.scraper import Scraper

    scraper = Scraper("https://www.letterboxd.com")

    movies = get_movies_from_user_watched(
        scraper.get_parsed_page("https://letterboxd.com/nmcassa/films/")
    )
    print(len(movies))

    movies = get_movies_from_horizontal_list(
        scraper.get_parsed_page("https://letterboxd.com/films/popular/this/week/".replace('films/', 'films/ajax/'))
    )
    print(len(movies))

    movies = get_movies_from_vertical_list(
        scraper.get_parsed_page("https://letterboxd.com/nmcassa/list/def-con-movie-list/")
    )
    print(len(movies))