from letterboxdpy.core.encoder import SecretsEncoder
from letterboxdpy.pages import (
    movie_details,
    movie_lists,
    movie_members,
    movie_profile,
    movie_reviews,
    movie_similar,
)
from letterboxdpy.utils.utils_file import JsonFile


class Movie:
    class MoviePages:
        def __init__(
            self,
            slug: str | None = None,
            *,
            tmdb: str | int | None = None,
            imdb: str | None = None,
        ) -> None:
            self.profile = movie_profile.MovieProfile(slug, tmdb=tmdb, imdb=imdb)
            self.details = movie_details.MovieDetails(self.profile.slug)
            self.lists = movie_lists.MovieLists(self.profile.slug)
            self.members = movie_members.MovieMembers(self.profile.slug)
            self.reviews = movie_reviews.MovieReviews(self.profile.slug)
            self.similar = movie_similar.MovieSimilar(self.profile.slug)

    @classmethod
    def from_tmdb(cls, tmdb_id: str | int) -> "Movie":
        """Initialize Movie using TMDB ID."""
        return cls(tmdb=tmdb_id)

    @classmethod
    def from_imdb(cls, imdb_id: str) -> "Movie":
        """Initialize Movie using IMDB ID."""
        return cls(imdb=imdb_id)

    def __init__(
        self,
        slug: str | None = None,
        *,
        tmdb: str | int | None = None,
        imdb: str | None = None,
    ) -> None:
        self.pages = self.MoviePages(slug, tmdb=tmdb, imdb=imdb)
        self.slug = self.pages.profile.slug

        self.url = self.get_url()

        # one line contents
        self.id = self.get_id()
        self.title = self.get_title()
        self.original_title = self.get_original_title()
        self.runtime = self.get_runtime()
        self.rating = self.get_rating()
        self.year = self.get_year()
        self.tmdb_link = self.get_tmdb_link()
        self.tmdb_id = str(tmdb) if tmdb else self.get_tmdb_id()
        self.imdb_link = self.get_imdb_link()
        self.imdb_id = str(imdb) if imdb else self.get_imdb_id()
        self.poster = self.get_poster()
        self.banner = self.get_banner()
        self.tagline = self.get_tagline()

        # long contents
        self.description = self.get_description()
        self.trailer = self.get_trailer()
        self.alternative_titles = self.get_alternative_titles()
        self.details = self.get_details()
        self.genres = self.get_genres()
        self.cast = self.get_cast()
        self.crew = self.get_crew()
        self.popular_reviews = self.get_popular_reviews()

    def __str__(self) -> str:
        return JsonFile.stringify(
            self, indent=2, encoder=SecretsEncoder, secrets=["pages"]
        )

    def jsonify(self) -> dict:
        return JsonFile.parse(self.__str__())

    # PROFILE PAGE
    def get_url(self) -> str:
        return self.pages.profile.url

    def get_id(self) -> str:
        return self.pages.profile.get_id()

    def get_title(self) -> str:
        return self.pages.profile.get_title()

    def get_original_title(self) -> str:
        return self.pages.profile.get_original_title()

    def get_runtime(self) -> int:
        return self.pages.profile.get_runtime()

    def get_rating(self) -> float:
        return self.pages.profile.get_rating()

    def get_year(self) -> int:
        return self.pages.profile.get_year()

    def get_tmdb_link(self) -> str:
        return self.pages.profile.get_tmdb_link()

    def get_tmdb_id(self) -> str:
        return self.pages.profile.get_tmdb_id()

    def get_imdb_link(self) -> str:
        return self.pages.profile.get_imdb_link()

    def get_imdb_id(self) -> str:
        return self.pages.profile.get_imdb_id()

    def get_poster(self) -> str:
        return self.pages.profile.get_poster()

    def get_banner(self) -> str:
        return self.pages.profile.get_banner()

    def get_tagline(self) -> str:
        return self.pages.profile.get_tagline()

    def get_description(self) -> str:
        return self.pages.profile.get_description()

    def get_trailer(self) -> dict:
        return self.pages.profile.get_trailer()

    def get_alternative_titles(self) -> list:
        return self.pages.profile.get_alternative_titles()

    def get_details(self) -> list:
        return self.pages.profile.get_details()

    def get_genres(self) -> list:
        return self.pages.profile.get_genres()

    def get_cast(self) -> list:
        return self.pages.profile.get_cast()

    def get_crew(self) -> dict:
        return self.pages.profile.get_crew()

    def get_popular_reviews(self) -> list:
        return self.pages.profile.get_popular_reviews()

    # DETAILS PAGE
    def get_details_from_details(self) -> dict:
        return self.pages.details.get_extended_details()

    # LISTS PAGE
    def get_lists(self) -> dict:
        return self.pages.lists.get_lists()

    # MEMBERS PAGE
    def get_watchers_stats(self) -> dict:
        return self.pages.members.get_watchers_stats()

    # REVIEWS PAGE
    def get_reviews(self) -> dict:
        return self.pages.reviews.get_reviews()

    def get_reviews_by_rating(self, rating: float) -> dict:
        return self.pages.reviews.get_reviews_by_rating(rating)

    # SIMILAR MOVIES
    def get_similar_movies(self) -> dict:
        return self.pages.similar.get_similar_movies()


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")

    movie_instance = Movie("v-for-vendetta")  # 132 mins
    # movie_instance_2 = Movie("honk-2013") # 1 min
    # movie_instance_3 = Movie("logistics-2011") # 51420 mins

    # Test basic functionality
    print(f"Movie Title: {movie_instance.title}")
    print(f"Movie Year: {movie_instance.year}")
    print(f"Movie Runtime: {movie_instance.runtime} minutes")
    print(f"Movie Rating: {movie_instance.rating}")

    print(f"Movie Details: {movie_instance.details}")

    # Test individual methods without JSON serialization
    print("\n--- Details (from details page) ---")
    details_from_details = movie_instance.get_details_from_details()
    print(JsonFile.stringify(details_from_details, indent=2))

    print("\n--- Watchers Stats ---")
    watchers_stats = movie_instance.get_watchers_stats()
    print(JsonFile.stringify(watchers_stats, indent=2))
