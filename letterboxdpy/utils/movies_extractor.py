"""
Movie extraction utilities for different Letterboxd page layouts.

This module provides generic functions to extract movie data from various
Letterboxd page types that display movies in different layouts.
"""

import json
import re

from letterboxdpy.utils.utils_string import (
    clean_movie_name,
    extract_year_from_movie_name,
)


def extract_movie_info(item):
    """
    Centralized function to extract movie information from a poster container.
    Supports both modern JSON identifiers and legacy data attributes.
    """
    # Find the element containing movie data (usually a react-component div)
    # Could be the item itself or a nested div
    data_div = (
        item
        if item.name == "div" and "react-component" in item.get("class", [])
        else item.find("div", class_="react-component")
    )

    # Fallback for horizontal lists or cases where react-component class is missing
    if not data_div:
        data_div = (
            item.find("div", attrs={"data-component-class": "LazyPoster"}) or item.div
        )

    if not data_div:
        return None

    # 1. Extract Movie ID
    movie_id = None
    if "data-postered-identifier" in data_div.attrs:
        try:
            identifier = json.loads(data_div["data-postered-identifier"])
            uid = identifier.get("uid", "")
            movie_id = uid.split(":")[-1] if ":" in uid else uid
        except (json.JSONDecodeError, KeyError):
            pass

    if not movie_id:
        movie_id = data_div.get("data-film-id")

    if not movie_id:
        return None

    # 2. Extract Slug, Name, Year
    movie_slug = data_div.get("data-item-slug") or data_div.get("data-film-slug")
    raw_name = data_div.get("data-item-name") or (
        data_div.img["alt"] if data_div.img else "Unknown"
    )
    movie_name = clean_movie_name(raw_name)
    year = extract_year_from_movie_name(raw_name)

    return movie_id, {
        "slug": movie_slug,
        "name": movie_name,
        "year": year,
        "url": f"https://letterboxd.com/film/{movie_slug}/",
    }


def extract_movies_from_horizontal_list(dom, max_items=12 * 6) -> dict:
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

    def get_movie_data(item):
        rating_key = "data-average-rating"
        movie_data = extract_movie_info(item)
        if not movie_data:
            return None

        movie_id, data = movie_data
        data["rating"] = float(item[rating_key]) if rating_key in item.attrs else None
        return movie_id, data

    items = dom.find_all(
        "li", class_=re.compile(r"posteritem|griditem|poster-container")
    ) or dom.find_all("li")
    movies = {}
    for item in items:
        if len(movies) >= max_items:
            break

        movie_data = get_movie_data(item)
        if movie_data:
            movie_id, data = movie_data
            movies[movie_id] = data

    return movies


def extract_movies_from_vertical_list(dom, max_items=20 * 5) -> dict:
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

    items = dom.find_all("li", {"class": "posteritem"}) or dom.find_all(
        "li", {"class": "griditem"}
    )
    movies = {}
    for item in items:
        if len(movies) >= max_items:
            break

        movie_data = extract_movie_info(item)
        if movie_data:
            movie_id, data = movie_data
            movies[movie_id] = data

    return movies
