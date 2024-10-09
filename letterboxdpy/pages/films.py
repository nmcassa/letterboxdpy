class Films:
    ...


def extract_movies_from_horizontal_list(dom, max=12*6) -> dict:
    """
    supports all horizontal lists
    ... films section, ...
    """
    items = dom.find_all("li")

    rating_key = "data-average-rating"
    movies = {}
    for item in items:
        movie_rating = float(item[rating_key]) if rating_key in item.attrs else None
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