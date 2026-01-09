from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Director:
    name: str

@dataclass
class MovieJSON:
    """
    Data model for the Letterboxd movie JSON endpoint.
    Source: https://letterboxd.com/film/{slug}/json/
    Associated URL function: letterboxdpy.url.FilmURL.json(slug)
    """
    result: bool
    csrf: str
    lid: str # short id (e.g. "dfdk")
    uid: str # prefixed id (e.g. "film:315675")
    type: str # e.g. "film"
    type_name: str # e.g. "film"
    id: int # numeric id
    name: str # title
    image_125: str # relative path to small poster
    image_150: str # relative path to medium poster
    release_year: int
    run_time: int # in minutes
    slug: str
    url: str # relative path
    original_name: Optional[str] = None
    filmlist_action: str = ""
    watchlist_action: str = ""
    directors: List[Director] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'MovieJSON':
        """Creates a MovieJSON instance from a dictionary."""
        directors_data = data.get('directors', [])
        # Ensure directors is always a list of Director objects
        directors = [Director(name=d['name']) for d in directors_data if isinstance(d, dict) and 'name' in d]
        
        return cls(
            result=data.get('result', False),
            csrf=data.get('csrf', ''),
            lid=data.get('lid', ''),
            uid=data.get('uid', ''),
            type=data.get('type', ''),
            type_name=data.get('typeName', ''),
            id=data.get('id', 0),
            name=data.get('name', ''),
            image_125=data.get('image125', ''),
            image_150=data.get('image150', ''),
            release_year=data.get('releaseYear', 0),
            run_time=data.get('runTime', 0),
            slug=data.get('slug', ''),
            url=data.get('url', ''),
            original_name=data.get('originalName'),
            filmlist_action=data.get('filmlistAction', ''),
            watchlist_action=data.get('watchlistAction', ''),
            directors=directors
        )
