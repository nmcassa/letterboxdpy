from typing import TYPE_CHECKING
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.scraper import Scraper

if TYPE_CHECKING:
    from letterboxdpy.core.models import MovieJSON

class FilmURL:
    """Endpoints and Factory for movie-related data."""
    
    @staticmethod
    def json_url(slug: str) -> str:
        return f"{DOMAIN}/film/{slug}/json/"

    @classmethod
    def json(cls, slug: str) -> 'MovieJSON':
        """Factory: Returns MovieJSON model from film slug."""
        from letterboxdpy.core.models import MovieJSON
        url = cls.json_url(slug)
        
        # Use shared scraper session
        response = Scraper.instance().get(url, headers=Scraper.headers, impersonate="chrome")
        if response.status_code != 200:
            from letterboxdpy.core.exceptions import InvalidResponseError
            raise InvalidResponseError(f"Failed to fetch JSON from {url}: {response.status_code}")
            
        return MovieJSON.from_dict(response.json())

    # CSI (Client Side Includes) Endpoints
    @staticmethod
    def _csi(slug: str, endpoint: str) -> str:
        return f"{DOMAIN}/csi/film/{slug}/{endpoint}/"

    @classmethod
    def popular_lists(cls, slug: str) -> str: return cls._csi(slug, "popular-lists")
    @classmethod
    def recent_reviews(cls, slug: str) -> str: return cls._csi(slug, "recent-reviews")
    @classmethod
    def rating_histogram(cls, slug: str) -> str: return cls._csi(slug, "rating-histogram")
    @classmethod
    def user_actions(cls, slug: str) -> str: return cls._csi(slug, "sidebar-user-actions")
    @classmethod
    def stats(cls, slug: str) -> str: return cls._csi(slug, "stats")
    @classmethod
    def news(cls, slug: str) -> str: return cls._csi(slug, "news")
    @classmethod
    def availability(cls, slug: str) -> str: return cls._csi(slug, "availability")
    @classmethod
    def friend_reviews(cls, slug: str) -> str: return cls._csi(slug, "friend-reviews")
    @classmethod
    def friend_activity(cls, slug: str) -> str: return cls._csi(slug, "friend-activity")
    @classmethod
    def own_reviews(cls, slug: str) -> str: return cls._csi(slug, "own-reviews")
    @classmethod
    def liked_reviews(cls, slug: str) -> str: return cls._csi(slug, "liked-reviews")


class UserURL:
    """Endpoints for user-related data."""
    
    @staticmethod
    def homepage() -> str:
        return f"{DOMAIN}/ajax/user-homepage/"

    @staticmethod
    def live_feed() -> str:
        return f"{DOMAIN}/csi/films-live-feed/"


class GeneralURL:
    """General Letterboxd endpoints."""
    
    @staticmethod
    def metadata() -> str:
        return f"{DOMAIN}/ajax/letterboxd-metadata/"
