"""
Movie extraction utilities for different Letterboxd page layouts.

This module provides generic functions to extract movie data from various
Letterboxd page types that display movies in different layouts.
"""

def extract_movies_from_horizontal_list(dom, max_items=12*6) -> dict:
    """
    Extract movies from horizontal movie lists.
    
    Used in:
    - /films/popular/, /films/genre/action/, etc.
    - Film discovery pages
    - Similar movies sections
    
    Args:
        dom: BeautifulSoup DOM object
        max_items: Maximum number of items to extract
        
    Returns:
        dict: Movie data with film IDs as keys
    """
    items = dom.find_all("li")

    rating_key = "data-average-rating"
    movies = {}
    for item in items:
        if len(movies) >= max_items:
            break
            
        movie_rating = float(item[rating_key]) if rating_key in item.attrs else None
        movie_id = item.div['data-film-id']
        movie_slug = item.div['data-item-slug'] 
        movie_name = item.img['alt']

        movies[movie_id] = {
            "slug": movie_slug,
            "name": movie_name,
            "rating": movie_rating,
            'url': f'https://letterboxd.com/film/{movie_slug}/'
        }

    return movies


def extract_movies_from_vertical_list(dom, max_items=20*5) -> dict:
    """
    Extract movies from vertical movie lists.
    
    Used in:
    - User watchlists (/user/username/watchlist/)
    - User lists (/user/username/list/list-name/)
    - User films pages
    - Search results
    
    Args:
        dom: BeautifulSoup DOM object
        max_items: Maximum number of items to extract
        
    Returns:
        dict: Movie data with film IDs as keys
    """
    def get_movie_data(item):
        """Extract movie ID, slug, and name from container element."""
        react_component = item.find("div", {"class": "react-component"}) if item.name == "li" else item
        if not react_component or 'data-film-id' not in react_component.attrs:
            return None
            
        movie_id = react_component['data-film-id']
        movie_slug = react_component.get('data-item-slug') or react_component.get('data-film-slug')
        movie_name = react_component.get('data-item-name') or react_component.img['alt']

        return movie_id, {
            "slug": movie_slug,
            "name": movie_name,
            'url': f'https://letterboxd.com/film/{movie_slug}/'
        }

    items = dom.find_all("li", {"class": "posteritem"}) or dom.find_all("li", {"class": "griditem"})
    movies = {}
    for item in items:
        if len(movies) >= max_items:
            break
            
        movie_data = get_movie_data(item)
        if movie_data:
            movie_id, data = movie_data
            movies[movie_id] = data

    return movies
