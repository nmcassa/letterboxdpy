if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import re
from json import (
  dumps as json_dumps,
  loads as json_loads
)

from letterboxdpy.utils.utils_parser import parse_review_date
from letterboxdpy.decorators import assert_instance
from letterboxdpy.scraper import parse_url
from letterboxdpy.encoder import Encoder
from letterboxdpy.constants.project import DOMAIN, CURRENT_YEAR
from letterboxdpy.pages import (
    user_activity,
    user_diary,
    user_films,
    user_likes,
    user_lists,
    user_network,
    user_profile
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
        return json_dumps(self, indent=2, cls=Encoder)

    def jsonify(self) -> dict:
        return json_loads(self.__str__())

    def get_activity(self) -> dict:
        return self.pages.activity.get_activity()
    def get_activity_following(self) -> dict:
        return self.pages.activity.get_activity_following()
    
    def get_diary(self, year: int = None, page: int = None) -> dict:
        return self.pages.diary.get_diary(year, page)
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

# -- FUNCTIONS --

# letterboxd.com/?/films/reviews/
@assert_instance(User)
def user_reviews(user: User) -> dict:
    '''
    Returns a dictionary containing user reviews. The keys are unique log IDs,
    and each value is a dictionary with details about the review,
    including movie information, review type, rating, review content, date, etc.
    '''
    LOGS_PER_PAGE = 12

    page = 0
    data = {'reviews': {}}
    while True:
        page += 1
        dom = parse_url(f"{user.url}/films/reviews/page/{page}/")
        logs = dom.find_all("li", {"class": ["film-detail"], })

        for log in logs:
            details = log.find("div", {"class": ["film-detail-content"], })

            movie_name = details.a.text
            slug = details.parent.div['data-film-slug']
            movie_id = details.parent.div['data-film-id']
            # str   ^^^--- movie_id: unique id of the movie.
            release = int(details.small.text) if details.small else None
            movie_link = f"{DOMAIN}/film/{slug}/"
            log_id = log['data-object-id'].split(':')[-1]
            # str ^^^--- log_id: unique id of the review.
            log_link = DOMAIN + details.a['href']
            log_no = log_link.split(slug)[-1]
            log_no = int(log_no.replace('/', '')) if log_no.count('/') == 2 else 0
            # int ^^^--- log_no: there can be multiple reviews for a movie.
            #            counting starts from zero.
            #            example for first review:  /username/film/movie_name/
            #            example for first review:  /username/film/movie_name/0/
            #            example for second review: /username/film/movie_name/1/
            #                the number is specified at the end of the url ---^
            rating = details.find("span", {"class": ["rating"], })
            rating = int(rating['class'][-1].split('-')[-1]) if rating else None
            # int ^^^--- rating: the numerical value of the rating given in the review (1-10)
            review = details.find("div", {"class": ["body-text"], })
            spoiler = bool(review.find("p", {"class": ["contains-spoilers"], }))
            # bool ^^^--- spoiler: whether the review contains spoiler warnings
            review = review.find_all('p')[1 if spoiler else 0:]
            review = '\n'.join([p.text for p in review])
            # str ^^^--- review: the text content of the review.
            #            spoiler warning is checked to include or exclude the first paragraph.
            date = details.find("span", {"class": ["_nobr"], })
            log_type = date.previous_sibling.text.strip()
            # str   ^^^--- log_type: Types of logs, such as:
            #              'Rewatched': (in diary) review, watched and rewatched 
            #              'Watched':   (in diary) review and watched
            #              'Added': (not in diary) review 
            date = parse_review_date(log_type, date)
            # dict ^^^--- date: the date of the review.
            #             example: {'year': 2024, 'month': 1, 'day': 1}

            data['reviews'][log_id] = {
                # static
                'movie': {
                    'name': movie_name,
                    'slug': slug,
                    'id': movie_id,
                    'release': release,
                    'link': movie_link,
                },
                # dynamic
                'type': log_type,
                'no': log_no,
                'link': log_link,
                'rating': rating,
                'review': {
                    'content': review,
                    'spoiler': spoiler
                },
                'date': date,
                'page': page,
            }

        if len(logs) < LOGS_PER_PAGE:
            data['count'] = len(data['reviews'])
            data['last_page'] = page
            break

    return data

# https://letterboxd.com/?/watchlist/
@assert_instance(User)
def user_watchlist(user: User, filters: dict=None) -> dict:
    """
    filter examples:
        - keys: decade, year, genre

        # positive genre & negative genre (start with '-')
        - {genre: ['mystery']}  <- same -> {genre: 'mystery'}
        - {genre: ['-mystery']} <- same -> {genre: '-mystery'}

        # multiple genres
        - {genre: ['mystery', 'comedy'], decade: '1990s'}
        - {genre: ['mystery', '-comedy'], year: '2019'}
        - /decade/1990s/genre/action+-drama/
          ^^---> {'decade':'1990s','genre':['action','-drama']}
    """
    data = {
        'available': None,
        'count': user.watchlist_length,
        'data_count': None,
        'last_page': None,
        'filters': filters,
        'data': {}
        }

    if user.watchlist_length is None:
        # user watchlist is private
        return data | {'available': False}
    elif user.watchlist_length == 0:
        # user watchlist is empty
        return data | {'available': True}

    FILMS_PER_PAGE = 7*4
    BASE_URL = f"{user.url}/watchlist/"

    if filters and isinstance(filters, dict):
        f = ""
        for key, values in filters.items():
            if not isinstance(values, list):
                values = [values]
            f += f"{key}/"
            f += "+".join([str(v) for v in values]) + "/"

        BASE_URL += f

    page = 1
    no = user.watchlist_length
    while True:
        dom = parse_url(f'{BASE_URL}/page/{page}')

        poster_containers = dom.find_all("li", {"class": ["poster-container"], })
        for poster_container in poster_containers:
            poster = poster_container.div
            img = poster_container.div.img

            film_id = poster['data-film-id']
            slug = poster['data-film-slug']
            name = img['alt']

            data['data'][film_id] = {
                'name': name,
                'slug': slug,
                'no': no,
                'page': page,
                'url': f"{DOMAIN}/films/{slug}/",
            }

            no -= 1

        if len(poster_containers) < FILMS_PER_PAGE:
            # last page
            break
        page += 1

    data_count = len(data['data'])

    if filters:
        if data_count != data['count']:
            no = data_count
            for item in data['data'].keys():
                data['data'][item]['no'] = no
                no -= 1

    data = data | {
        'available': True,
        'data_count': data_count,
        'last_page': page,
        }

    return data

# https://letterboxd.com/?/tags/*
@assert_instance(User)
def user_tags(user: User) -> dict:
    BASE_URL = f"{user.url}/tags"
    PAGES = ['films', 'diary', 'reviews', 'lists']

    def extract_tags(page: str) -> dict:
        """Extract tags from the page."""
        
        def fetch_dom() -> any:
            """Fetch and return the DOM for the page."""
            return parse_url(f"{BASE_URL}/{page}")

        def parse_tag(tag) -> dict:
            """Extract tag information from a single tag element."""
            name = tag.a.text.strip()
            title = tag.a['title']
            link = tag.a['href']
            slug = link.split('/')[-3]
            count = int(tag.span.text.strip() or 1)
            return {
                'name': name,
                'title': title,
                'slug': slug,
                'link': DOMAIN + link,
                'count': count,
            }

        dom = fetch_dom()
        tags_ul = dom.find("ul", {"class": "tags-columns"})
        data = {}

        if not tags_ul:
            return data

        tags = tags_ul.find_all("li")
        index = 1
        for tag in tags:
            if 'href' in tag.a.attrs:
                tag_info = parse_tag(tag)
                tag_info['no'] = index
                data[tag_info['slug']] = tag_info
                index += 1

        return data

    data = {}
    for page in PAGES:
        tags = extract_tags(page)
        data[page] = {
            'tags': tags,
            'count': len(tags)
        }

    data['total_count'] = sum(data[page]['count'] for page in PAGES)

    return data

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
    user_instance = User(username.lower())

    # Print user statistics
    print(user_instance)

    # Iterate over user's film data and print each movie
    for item in user_films(user_instance)['movies'].items():
        print(item)
