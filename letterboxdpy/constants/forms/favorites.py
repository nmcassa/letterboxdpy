"""Favorite film extraction attributes."""

from dataclasses import dataclass

@dataclass  
class FavoriteFilmAttributes:
    """HTML attributes for favorite film extraction."""
    COMPONENT_CLASS: str = "react-component"
    FILM_ID_ATTR: str = "data-film-id"
    FILM_NAME_ATTR: str = "data-item-name"
    FILM_SLUG_ATTR: str = "data-item-slug"
    FILM_LINK_ATTR: str = "data-item-link"

# Convenience instances
FAVORITE_ATTRS = FavoriteFilmAttributes()
