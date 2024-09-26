if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import re
from json import (
  dumps as json_dumps,
  loads as json_loads
)

from letterboxdpy.utils.utils_transform import month_to_index
from letterboxdpy.utils.utils_parser import parse_review_date, extract_and_convert_shorthand
from letterboxdpy.decorators import assert_instance
from letterboxdpy.scraper import parse_url
from letterboxdpy.encoder import Encoder
from letterboxdpy.avatar import Avatar
from letterboxdpy.constants.project import DOMAIN, CURRENT_YEAR
from letterboxdpy.pages import (
    user_activity,
    user_diary,
    user_films,
    user_likes,
    user_lists
)


class User:

    class UserPages:

        def __init__(self, username: str) -> None:
            self.activity = user_activity.UserActivity(username)
            self.diary = user_diary.UserDiary(username)
            self.films = user_films.UserFilms(username)
            self.likes = user_likes.UserLikes(username)
            self.lists = user_lists.UserLists(username)

    def __init__(self, username: str) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid username"

        self.username = username.lower()
        self.url = f"{DOMAIN}/{self.username}"
        self.pages = self.UserPages(self.username)

        dom = parse_url(self.url)

        self.user_details(dom)
        self.user_avatar(dom)
        self.user_recent(dom)

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

    # letterboxd.com/?
    def user_avatar(self, dom) -> str:
        elem_avatar = dom.find("div", {"class": ["profile-avatar"]})
        avatar_url = elem_avatar.img['src']
        self.avatar = Avatar(avatar_url).upscaled_data

    # letterboxd.com/?
    def user_recent(self, dom) -> list:
        watchlist_recent = {}
        diary_recent = {'months':{}}

        # watchlist
        if self.watchlist_length:
            section_watchlist = dom.find("section", {"class": ["watchlist-aside"]})
            watchlist_items = section_watchlist.find_all("li", {"class": ["film-poster"]})
            for item in watchlist_items:
                watchlist_recent[item['data-film-id']] = {
                    'name': item.img['alt'],
                    'slug': item['data-film-slug']
                }
        
        # diary
        sections = dom.find_all("section", {"class": ["section"]})
        for section in sections:
            if section.h2 is None:
                continue
    
            if section.h2.text == "Diary":
                entry_list = section.find_all("li", {"class": ["listitem"]})

                for entry in entry_list:
                    month_index = month_to_index(entry.h3.text)

                    diary_recent['months'] |= {month_index: {}}

                    days = entry.find_all("dt")
                    items = entry.find_all("dd")

                    for day, item in zip(days, items):
                        movie_index = day.text
                        movie_slug = item.a['href'].split('/')[-2]
                        movie_name = item.text 

                        if movie_index not in diary_recent['months'][month_index]:
                            diary_recent['months'][month_index][movie_index] = []

                        diary_recent['months'][month_index][movie_index].append({
                            'name': movie_name,
                            'slug': movie_slug
                        })
                else:
                    break

        data = {
            'watchlist': watchlist_recent,
            'diary': diary_recent
        }
        
        self.recent = data

    # letterboxd.com/?/
    def user_details(self, dom) -> dict:
        """
        methods:
        .id, .display_name, .bio, .location,
        .website, .watchlist_length, .stats, .favorites
        """

        # id
        """ alternative:
        button_report = page.find("button", {"data-js-trigger": ["report"]})
        self.id = int(button_report['data-report-url'].split(':')[-1].split('/')[0])
        """
        pattern = r"/ajax/person:(\d+)/report-for"
        self.id  = re.search(
            pattern,
            dom.prettify()
        ).group(1)

        # hq check
        self.is_hq = bool(dom.find("body", {'class': 'profile-hq'}))
        #:alternative
        # data = dom.find("div", {'class': 'profile-summary'})
        # data = data['data-profile-summary-options'] if 'data-profile-summary-options'in data.attrs else None
        # self.is_hq = json_loads(data)['isHQ']

        # display name
        data = dom.find("meta", attrs={'property': 'og:title'})
        self.display_name = data['content'][:-10]

        # bio
        data = dom.find("meta", attrs={'property': 'og:description'})
        self.bio = data['content'].split('Bio: ')[-1] if data['content'].find('Bio: ') != -1 else None

        # location and website
        data = dom.find("div", {"class": ["profile-metadata"], })
        location = data.find("div", {"class": ["metadatum"], }) if data else None
        website = data.find("a") if data else None
        self.location = location.find("span").text if location else None
        self.website = website['href'] if website else None         

        # watchlist_length
        nav_links = dom.find_all("a", {"class": ["navlink"]})
        for link in nav_links:
            if "Watchlist" in link.text:
               if "rel" in link.attrs:
                    # 'User watchlist is not visible'
                    self.watchlist_length = None # feature: PrivateData(Exception)
                    break
               else:
                    # 'User watchlist is visible'
                    widget = dom.find("section", {"class": ["watchlist-aside"]})
                    self.watchlist_length = int(
                        widget.find("a", {"class": ["all-link"]}).text.replace(',','')
                        ) if widget else 0
                    break
            else:
                # hq members
                self.watchlist_length = None

        # stats
        stats = dom.find_all("h4", {"class": ["profile-statistic"]})
        self.stats = {} if stats else None
        # e.g: "films", "this_year", "lists", "following", "followers"
        for stat in stats:
            value = stat.span.text
            key = stat.text.lower().replace(value,'').replace(' ','_')
            self.stats[key]= int(value.replace(',',''))

        # favorites
        data = dom.find("section", {"id": ["favourites"], })
        data = data.findChildren("div") if data else []
        self.favorites = {}
        for div in data:
            poster = div.find("img")
            movie_slug = poster.parent['data-film-slug']
            movie_id = poster.parent['data-film-id']
            movie_name = poster['alt']
            self.favorites[movie_id] = {
                'slug': movie_slug,
                'name': movie_name
            }

# -- FUNCTIONS --

# letterboxd.com/?/?/
@assert_instance(User)
def user_network(user: User, section: str) -> dict:
    """
    Fetches followers or following based on the section and returns them as a dictionary
    - The section to scrape, must be either 'followers' or 'following'.
    """
    BASE_URL = f"{user.url}/{section}"
    PERSONS_PER_PAGE = 25

    def fetch_page(page_num: int):
        """Fetches a single page of the user's network section."""
        try:
            return parse_url(f"{BASE_URL}/page/{page_num}")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch page {page_num}: {e}")

    def extract_persons(dom) -> dict:
        """Extracts persons from a DOM object and returns them as a dictionary."""
        persons = dom.find_all("img", attrs={'height': '40'})
        persons_dict = {}

        for person in persons:
            profile_url = person.parent['href'].replace('/', '')
            persons_dict[profile_url] = {'display_name': person['alt']}

        return persons_dict

    users_list = {}
    page_num = 1

    while True:
        dom = fetch_page(page_num)
        persons = extract_persons(dom)
        users_list.update(persons)

        if len(persons) < PERSONS_PER_PAGE :
            break

        page_num += 1

    return users_list

# letterboxd.com/?/following/
@assert_instance(User)
def user_following(user: User) -> dict:
    """Fetches following and returns them as a dictionary"""
    return user_network(user, 'following')

# letterboxd.com/?/followers/
@assert_instance(User)
def user_followers(user: User) -> dict:
    """Fetches followers and returns them as a dictionary"""
    return user_network(user, 'followers')

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
