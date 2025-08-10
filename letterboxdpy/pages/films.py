from typing import Generator
class Films:
    ...


def extract_movies_from_horizontal_list(dom, max=12*6) -> dict:
    """
    supports all horizontal lists
    ... films section, ...
    """
    return dict(_extract_movies_from_horizontal_list_lazy(dom, max))

def _extract_movies_from_horizontal_list_lazy(dom, max=12*6) -> Generator[tuple[str, dict], None, None]:
    items = dom.find_all("li")

    rating_key = "data-average-rating"
    for item in items:
        movie_rating = float(item[rating_key]) if rating_key in item.attrs else None
        movie_id = item.div['data-film-id']
        movie_slug = item.div['data-film-slug']
        movie_name = item.img['alt']

        movie_data = {
            "slug": movie_slug,
            "name": movie_name,
            "rating": movie_rating,
            'url': f'https://letterboxd.com/film/{movie_slug}/'
        }
        yield (movie_id, movie_data)
