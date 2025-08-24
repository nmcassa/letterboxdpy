if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import re
from json import (
  dumps as json_dumps,
  loads as json_loads
)

from letterboxdpy.core.encoder import SecretsEncoder
from letterboxdpy.constants.project import CURRENT_YEAR, CURRENT_MONTH, CURRENT_DAY
from letterboxdpy.list import List as LetterboxdList
from letterboxdpy.pages import (
    user_activity,
    user_diary,
    user_films,
    user_likes,
    user_lists,
    user_network,
    user_profile,
    user_reviews,
    user_tags,
    user_watchlist
)


class User:

    class UserPages:

        def __init__(self, username: str) -> None:
            self.activity = user_activity.UserActivity(username)
            self.diary = user_diary.UserDiary(username)
            self.films = user_films.UserFilms(username)
            self.likes = user_likes.UserLikes(username)
            self.lists = user_lists.UserLists(username)
            self.network = user_network.UserNetwork(username)
            self.profile = user_profile.UserProfile(username)
            self.reviews = user_reviews.UserReviews(username)
            self.tags = user_tags.UserTags(username)
            self.watchlist = user_watchlist.UserWatchlist(username)

    def __init__(self, username: str) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid username"

        self.username = username.lower()
        self.pages = self.UserPages(self.username)

        self.url = self.get_url()
        self.id = self.get_id()
        self.is_hq = self.get_hq_status()
        self.display_name = self.get_display_name()
        self.bio = self.get_bio()
        self.location = self.get_location()
        self.website = self.get_website()
        self.watchlist_length = self.get_watchlist_length()
        self.stats = self.get_stats()
        self.favorites = self.get_favorites()
        self.avatar = self.get_avatar()
        self.recent = {
            'watchlist': self.get_watchlist_recent(),
            'diary': self.get_diary_recent()
        }

    def __str__(self) -> str:
        return json_dumps(self, indent=2, cls=SecretsEncoder, secrets=['pages'])

    def jsonify(self) -> dict:
        return json_loads(self.__str__())

    def get_activity(self) -> dict:
        return self.pages.activity.get_activity()
    def get_activity_following(self) -> dict:
        return self.pages.activity.get_activity_following()

    def get_diary(self, year: int = None, month: int = None, day: int = None, page: int = None) -> dict:
        return self.pages.diary.get_diary(year, month, day, page)
    def get_diary_year(self, year: int = CURRENT_YEAR) -> dict:
        return self.pages.diary.get_year(year)
    def get_diary_month(self, year: int = CURRENT_YEAR, month: int = CURRENT_MONTH) -> dict:
        return self.pages.diary.get_month(year, month)
    def get_diary_day(self, year: int = CURRENT_YEAR, month: int = CURRENT_MONTH, day: int = CURRENT_DAY) -> dict:
        return self.pages.diary.get_day(year, month, day)
    def get_wrapped(self, year: int = CURRENT_YEAR) -> dict:
        return self.pages.diary.get_wrapped(year)

    def get_films(self) -> dict:
        return self.pages.films.get_films()
    def get_films_by_rating(self, rating: float | int) -> dict:
        return self.pages.films.get_films_rated(rating)
    def get_films_not_rated(self) -> dict:
        return self.pages.films.get_films_not_rated()
    def get_genre_info(self) -> dict:
        return self.pages.films.get_genre_info()
    
    def get_liked_films(self) -> dict:
        return self.pages.likes.get_liked_films()
    def get_liked_reviews(self) -> dict:
        return self.pages.likes.get_liked_reviews()
    def get_liked_lists(self) -> dict:
        return self.pages.likes.get_liked_lists()
    
    def get_list(self, slug: str) -> LetterboxdList: 
        return LetterboxdList(self.username, slug)
    
    def get_lists(self) -> dict:
        return self.pages.lists.get_lists()
    
    def get_following(self) -> dict:
        return self.pages.network.get_following()
    def get_followers(self) -> dict:
        return self.pages.network.get_followers()

    def get_url(self) -> str:
        return self.pages.profile.url
    def get_id(self) -> str:
        return self.pages.profile.get_id()
    def get_hq_status(self) -> bool:
        return self.pages.profile.get_hq_status()
    def get_display_name(self) -> str:
        return self.pages.profile.get_display_name()
    def get_bio(self) -> str:
        return self.pages.profile.get_bio()
    def get_location(self) -> str:
        return self.pages.profile.get_location()
    def get_website(self) -> str:
        return self.pages.profile.get_website()
    def get_watchlist_length(self) -> int:
        return self.pages.profile.get_watchlist_length()
    def get_stats(self) -> dict:
        return self.pages.profile.get_stats()
    def get_favorites(self) -> dict:
        return self.pages.profile.get_favorites()
    def get_avatar(self) -> str:
        return self.pages.profile.get_avatar()
    def get_watchlist_recent(self) -> dict:
        return self.pages.profile.get_watchlist_recent()
    def get_diary_recent(self) -> dict:
        return self.pages.profile.get_diary_recent()
    
    def get_reviews(self) -> dict:
        return self.pages.reviews.get_reviews()
    
    def get_user_tags(self) -> dict:
        return self.pages.tags.get_user_tags()
    
    def get_watchlist_count(self) -> int:
        return self.pages.watchlist.get_count()
    def get_watchlist_movies(self) -> dict:
        return self.pages.watchlist.get_movies()
    def get_watchlist(self, filters:dict=None) -> dict:
        return self.pages.watchlist.get_watchlist(filters)

if __name__ == "__main__":
    import argparse
    import sys

    # Reconfigure stdout encoding to UTF-8 to support non-ASCII characters
    sys.stdout.reconfigure(encoding='utf-8')

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest="user", help="Username to gather stats on")
    args = parser.parse_args()

    # Extract username from command-line arguments or prompt user for input
    username = args.user or ''

    # Keep prompting user until a valid username is provided
    while not len(username.strip()):
        username = input('Enter username: ')

    # Display the username being processed
    print(f"Processing username: {username}")

    # Initialize a User instance with the provided username
    user_instance = User(username)

    # Print user instance(profile) data
    print(user_instance)

    # Iterate over user's film data and print each movie
    for item in user_instance.get_films()['movies'].items():
        print(item)
