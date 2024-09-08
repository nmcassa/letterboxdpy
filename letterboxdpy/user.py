if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from letterboxdpy.utils.utils_parser import parse_review_date
from letterboxdpy.parser import get_movies_from_user_watched
from letterboxdpy.decorators import assert_instance
from letterboxdpy.scraper import Scraper
from letterboxdpy.encoder import Encoder
from letterboxdpy.avatar import Avatar
from datetime import datetime
import re

from json import (
  dumps as json_dumps,
  loads as json_loads
)


class User:
    DOMAIN = "https://letterboxd.com"
    MONTH_ABBREVIATIONS = [
        "Jan", "Feb", "Mar",
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
        ]

    def __init__(self, username: str) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid username"

        self.scraper = Scraper(self.DOMAIN)
        self.username = username.lower()
        self.url = f"{self.DOMAIN}/{self.username}"

        dom = self.scraper.get_parsed_page(self.url)

        self.user_details(dom)
        self.user_avatar(dom)
        self.user_recent(dom)

    def __str__(self) -> str:
        return json_dumps(self, indent=2, cls=Encoder)

    def jsonify(self) -> dict:
        return json_loads(self.__str__())

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
                    'slug': item['data-film-slug'],
                }
        
        # diary
        sections = dom.find_all("section", {"class": ["section"]})
        for section in sections:
            if section.h2 is None:
                continue
    
            if section.h2.text == "Diary":
                entry_list = section.find_all("li", {"class": ["listitem"]})

                for entry in entry_list:
                    month = entry.h3.text
                    month_index = self.MONTH_ABBREVIATIONS.index(month) + 1
                    diary_recent['months'] |= {month_index: []}
                    days = entry.find_all("dt")
                    items = entry.find_all("dd")
                    for day, item in zip(days, items):
                        diary_recent['months'][month_index].append([day.text, item.text])
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

# letterboxd.com/?/films/
@assert_instance(User)
def user_films(user: User) -> dict:
    url = f"{user.url}/films"
    return extract_user_films(user, url)

# letterboxd.com/?/likes/films
@assert_instance(User)
def user_films_liked(user: User) -> dict:
    url = f"{user.url}/likes/films/"
    return extract_user_films(user, url)

# letterboxd.com/?/films/rated/?
@assert_instance(User)
def user_films_rated(user: User, rating: float | int) -> dict:
    assert rating in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], "Invalid rating"
    url = "{user.url}/films/rated/{rating}/by/date"
    return extract_user_films(user, url)

# user:films
@assert_instance(User)
def extract_user_films(user: User, url: str = None) -> dict:
    """Extracts user films and their details from the given URL or returns all watched films."""
    if not url:
        """If the url is not specified, all the movies that the user has watched
        will be checked, you can use the user_films function to do this"""
        return user_films(user)

    FILMS_PER_PAGE = 12 * 6

    def process_page(page_number: int) -> dict:
        """Fetches and processes a page of user films."""
        dom = user.scraper.get_parsed_page(f"{url}/page/{page_number}/")
        return get_movies_from_user_watched(dom)

    def calculate_statistics(movies: dict) -> dict:
        """Calculates film statistics including liked and rating percentages."""
        liked_count = sum(movie['liked'] for movie in movies.values())
        rating_count = len([movie['rating'] for movie in movies.values() if movie['rating'] is not None])

        count = len(movies)
        liked_percentage = round(liked_count / count * 100, 2) if liked_count else 0.0
        rating_percentage = 0.0
        rating_average = 0.0

        if rating_count:
            ratings = [movie['rating'] for movie in movies.values() if movie['rating']]
            rating_percentage = round(rating_count / count * 100, 2)
            rating_average = round(sum(ratings) / rating_count, 2)

        return {
            'count': count,
            'liked_count': liked_count,
            'rating_count': rating_count,
            'liked_percentage': liked_percentage,
            'rating_percentage': rating_percentage,
            'rating_average': rating_average
        }

    movie_list = {'movies': {}}
    page = 0

    while True:
        page += 1
        movies = process_page(page)
        movie_list['movies'] |= movies

        if len(movies) < FILMS_PER_PAGE:
            stats = calculate_statistics(movie_list['movies'])
            movie_list.update(stats)
            break

    return movie_list

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
            return user.scraper.get_parsed_page(f"{BASE_URL}/page/{page_num}")
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

# letterboxd.com/?/films/genre/*/
@assert_instance(User)
def user_genre_info(user: User) -> dict:
    genres = ["action", "adventure", "animation", "comedy", "crime",
              "documentary","drama", "family", "fantasy", "history",
              "horror", "music", "mystery", "romance", "science-fiction",
              "thriller", "tv-movie", "war", "western"]
    ret = {}
    for genre in genres:
        dom = user.scraper.get_parsed_page(f"{user.url}/films/genre/{genre}/")
        data = dom.find("span", {"class": ["replace-if-you"], })
        data = data.next_sibling.replace(',', '')
        try:
            ret[genre] = [int(s) for s in data.split() if s.isdigit()][0]
        except IndexError:
            ret[genre] = 0

    return ret

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
        dom = user.scraper.get_parsed_page(f"{user.url}/films/reviews/page/{page}/")
        logs = dom.find_all("li", {"class": ["film-detail"], })

        for log in logs:
            details = log.find("div", {"class": ["film-detail-content"], })

            movie_name = details.a.text
            slug = details.parent.div['data-film-slug']
            movie_id = details.parent.div['data-film-id']
            # str   ^^^--- movie_id: unique id of the movie.
            release = int(details.small.text) if details.small else None
            movie_link = f"{user.DOMAIN}/film/{slug}/"
            log_id = log['data-object-id'].split(':')[-1]
            # str ^^^--- log_id: unique id of the review.
            log_link = user.DOMAIN + details.a['href']
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

# letterboxd.com/?/films/diary/
@assert_instance(User)
def user_diary(user: User, year: int=None, page: int=None) -> dict:
    '''
    Returns:
      Returns a list of dictionaries with the user's diary'
      Each entry is represented as a dictionary with details such as movie name,
      release information,rewatch status, rating, like status, review status,
      and the date of the entry.
    '''
    BASE_URL = f"{user.url}/films/diary/{f'for/{year}/'*bool(year)}"
    pagination = page if page else 1
    ret = {'entries': {}}

    while True:
        url = BASE_URL + f"page/{pagination}/"

        dom = user.scraper.get_parsed_page(url)
        table = dom.find("table", {"id": ["diary-table"], })

        if table:
            # extract the headers class of the table to use as keys for the entries
            # ['month','day','film','released','rating','like','rewatch','review', actions']
            headers = [elem['class'][0].split('-')[-1] for elem in table.find_all("th")]
            rows = dom.tbody.find_all("tr")

            for row in rows:
                # create a dictionary by mapping headers class
                # to corresponding columns in the row
                cols = dict(zip(headers, row.find_all('td')))

                # <tr class="diary-entry-row .." data-viewing-id="516951060" ..>
                log_id = row["data-viewing-id"]

                # day column
                date = dict(zip(
                        ["year", "month", "day"],
                        map(int, cols['day'].a['href'].split('/')[-4:])
                    ))
                # film column
                poster = cols['film'].div
                name = poster.img["alt"] or row.h3.text
                slug = poster["data-film-slug"]
                id = poster["data-film-id"]
                # released column
                release = cols["released"].text
                release = int(release) if len(release) else None
                # rewatch column
                rewatched = "icon-status-off" not in cols["rewatch"]["class"]
                # rating column
                rating = cols["rating"].span
                is_rating = 'rated-' in ''.join(rating["class"])
                rating = int(rating["class"][-1].split("-")[-1]) if is_rating else None
                # like column
                liked = bool(cols["like"].find("span", attrs={"class": "icon-liked"}))
                # review column
                reviewed = bool(cols["review"].a)
                # actions column
                actions = cols["actions"]
                """
                id = actions["data-film-id"] # !film col
                name = actions["data-film-name"] !# film col
                slug = actions["data-film-slug"] # !film col
                release = actions["ddata-film-release-year"] # !released col
                """
                runtime = actions["data-film-run-time"]
                runtime = int(runtime) if runtime else None

                # create entry
                ret["entries"][log_id] = {
                    "name": name,
                    "slug": slug,
                    "id":  id,
                    "release": release,
                    "runtime": runtime,
                    "actions": {
                        "rewatched": rewatched,
                        "rating": rating,
                        "liked": liked,
                        "reviewed": reviewed,
                    },
                    "date": date,
                    "page": {
                        'url': url,
                        'no': pagination
                        }
                }
            if len(rows) < 50 or pagination == page:
                    # no more entries
                    # or reached the requested page
                    break
            pagination += 1
        else: # no table
            break

    ret['count'] = len(ret['entries'])
    ret['last_page'] = pagination

    return ret

# dependency: user_diary()
@assert_instance(User)
def user_wrapped(user: User, year: int=2024) -> dict:
    """Wraps user diary data for the specified year and calculates statistics."""

    def retrieve_diary() -> dict:
        """Retrieves the diary for the given user and year."""
        try:
            diary = user_diary(user, year)
        except Exception as e:
            raise ValueError(f"Failed to retrieve diary for user {user}: {e}") from e
        
        if 'entries' not in diary:
            raise KeyError("Diary data does not contain 'entries' key.")
        return diary

    def update_counters(date_info: dict, day_counter: dict, month_counter: dict) -> tuple:
        """Updates the day and month counters based on the watched date."""
        weekday = datetime(**date_info).isoweekday()
        day_counter[weekday] += 1
        month_counter[date_info['month']] += 1
        return day_counter, month_counter

    def process_entry(data: dict, total_runtime: int, total_review: int) -> tuple:
        """Processes a diary entry and returns updated runtime and review counts."""
        reviewed = data["actions"]['reviewed']
        total_review += 1 if reviewed else 0
        runtime = data['runtime']
        total_runtime += runtime if runtime else 0
        return total_runtime, total_review

    def update_milestones(entry_no: int, log_id: str, data: dict, milestones: dict) -> dict:
        """Updates milestones every 50 entries."""
        if entry_no % 50 == 0:
            milestones[entry_no] = {log_id: data}
        return milestones

    def update_watched_entries(log_id: str, data: dict, first_watched: dict, last_watched: dict) -> tuple:
        """Tracks the first and last watched entries."""
        if not last_watched:
            last_watched = {log_id: data}
        else:
            first_watched = {log_id: data}
        return first_watched, last_watched

    diary = retrieve_diary()

    movies = {}
    milestones = {}
    months = {}.fromkeys([1,2,3,4,5,6,7,8,9,10,11,12], 0)
    days = {}.fromkeys([1,2,3,4,5,6,7], 0)
    total_review = 0
    total_runtime = 0
    first_watched = None
    last_watched = None

    no = 0
    for log_id, data in diary['entries'].items():
        watched_date = data['date']

        if watched_date['year'] == year:
            no += 1

            movies[log_id] = data

            days, months = update_counters(watched_date, days, months)
            total_runtime, total_review = process_entry(data, total_runtime, total_review)
            milestones = update_milestones(no, log_id, data, milestones)
            first_watched, last_watched = update_watched_entries(log_id, data, first_watched, last_watched)
    
    wrapped = {
        'year': year,
        'logged': len(movies),
        'total_review': total_review,
        'hours_watched': total_runtime // 60,
        'total_runtime': total_runtime,
        'first_watched': first_watched,
        'last_watched': last_watched,
        'movies': movies,
        'months': months,
        'days': days,
        'milestones': milestones
    }

    return wrapped

# letterboxd.com/?/activity
# letterboxd.com/ajax/activity-pagination/?/
@assert_instance(User)
def user_activity(user: User) -> dict:
    BASE_URL = f"{user.DOMAIN}/ajax/activity-pagination/{user.username}"

    def get_event_type(section) -> tuple:
        """
        Extracts the event type and log ID from the section.
        """
        event_type = None
        if any(x.startswith('-') for x in section['class']):
            event_type = list(filter(lambda x: x.startswith('-'), section['class']))[0][1:]
        return event_type

    def process_activity_log(section, event_type) -> dict:
        """
        Processes the activity log depending on the event type.
        """
        def parse_datetime(date_string: str) -> datetime:
            """
            Parses a datetime string, handling microseconds if present.
            """
            try:
                return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')

        def process_review_log() -> dict:
            """
            Processes the review-specific log data.
            """
            detail = section.find("div", {"class": "film-detail-content"})
            log_title = detail.p.text.strip()
            log_type = log_title.split()[-1]
            film = detail.h2.find(text=True)

            rating = section.find("span", {"class": ["rating"], })
            rating = int(rating['class'][-1].split('-')[-1]) if rating else None

            film_year = detail.h2.small.text
            film_year = int(film_year) if film_year else None

            review = detail.find("div", {"class": ["body-text"], })
            spoiler = bool(review.find("p", {"class": ["contains-spoilers"], }))
            review = review.find_all('p')[1 if spoiler else 0:]
            review = '\n'.join([p.text for p in review])

            return {
                'type': log_type,
                'title': log_title,
                'film': film,
                'film_year': film_year,
                'rating': rating,
                'spoiler': spoiler,
                'review': review
            }

        def process_basic_log() -> dict:
            """
            Processes the basic log data.
            """
            log_title = section.p.text.strip()
            log_type = log_title.split()[1]
            log_data = {'log_type': log_type, 'title': log_title}

            if log_type == 'followed':
                username = section.find("a", {"class": "target"})['href'].replace('/', '')
                log_data['username'] = username
            elif log_type == 'liked':
                # display_name = section.find("strong",{"class":["name"]}).text.replace('\u2019s',"")
                username = section.find("a", {"class": "target"})['href'].split('/')[1]
                log_data['username'] = username
            elif log_type == 'watched':
                film = section.find("a",{"class":["target"]}).text.split('  ')[-1].strip()
                log_data['film'] = film if film else None

            return log_data

        log_id = section["data-activity-id"]
        date = parse_datetime(section.find("time")['datetime'])
        log_data = {
            'event_type': event_type,
            'time': {
                'year': date.year,
                'month': date.month,
                'day': date.day,
                'hour': date.hour,
                'minute': date.minute,
                'second': date.second
            }
        }

        if event_type == 'review':
            log_data.update(process_review_log())
        elif event_type == 'basic':
            log_data.update(process_basic_log())

        return {log_id: log_data}

    data = {
        'user': user.username,
        'logs': {},
        'total_logs': 0
    }

    dom = user.scraper.get_parsed_page(BASE_URL)
    sections = dom.find_all("section")

    if not sections:
        # User {user.username} has no activity.
        return data

    for section in sections:
        event_type = get_event_type(section)
        if event_type in ('review', 'basic'):
            log_data = process_activity_log(section, event_type)
            data['logs'].update(log_data)
            data['total_logs'] = len(data['logs'])
        elif 'no-activity-message' in section['class']:
            break

    return data

# https://letterboxd.com/?/lists/
@assert_instance(User)
def user_lists(user: User) -> dict:
    BASE_URL = f"{user.url}/lists/"
    LISTS_PER_PAGE = 12
    SELECTORS = {
        'list_set': ('section', {'class': 'list-set'}),
        'lists': ('section', {'class': 'list'}),
        'title': ('h2', {'class': 'title'}),
        'description': ('div', {'class': 'body-text'}),
        'value': ('small', {'class': 'value'}),
        'likes': ('a', {'class': 'icon-like'}),
        'comments': ('a', {'class': 'icon-comment'}),
    }

    def fetch_page_data(page: int) -> dict:
        """Fetch and parse page data."""
        dom = user.scraper.get_parsed_page(f'{BASE_URL}/page/{page}')
        list_set = dom.find(*SELECTORS['list_set'])
        return list_set

    def extract_list_data(item) -> dict:
        """Extract data from a list item."""

        def get_id() -> str:
            return item['data-film-list-id']

        def get_title() -> str:
            return item.find(*SELECTORS['title']).text.strip()

        def get_description() -> str:
            description = item.find(*SELECTORS['description'])
            if description:
                paragraphs = description.find_all('p')
                return '\n'.join([p.text for p in paragraphs])
            return description

        def get_url() -> str:
            return user.DOMAIN + item.find(*SELECTORS['title']).a['href']

        def get_slug() -> str:
            return get_url().split('/')[-2]

        def get_count() -> int:
            return int(item.find(*SELECTORS['value']).text.split()[0].replace(',', ''))

        def get_likes() -> int:
            likes = item.find(*SELECTORS['likes'])
            likes = likes if likes else 0
            if likes:
                likes = likes.text.split()[0].replace(',','')
                if 'K' in likes:
                    likes = likes.replace('K', '')
                    likes = float(likes) * 1000
                likes = int(likes)
            return likes

        def get_comments() -> int:
            comments = item.find(*SELECTORS['comments'])
            comments = int(comments.text.split()[0].replace(',','')) if comments else 0
            return comments

        return {
             get_id(): {
                'title': get_title(),
                'slug': get_slug(),
                'description': get_description(),
                'url': get_url(),
                'count': get_count(),
                'likes': get_likes(),
                'comments': get_comments()
                }
            }

    data = {'lists': {}}
    page = 1
    while True:
        list_set = fetch_page_data(page)
        if not list_set:
            break

        lists = list_set.find_all(*SELECTORS['lists'])
        for item in lists:
            list_data = extract_list_data(item)
            data['lists'] |= list_data

        if len(lists) < LISTS_PER_PAGE:
            break
        page += 1

    data['count'] = len(data['lists'])
    data['last_page'] = page

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
        dom = user.scraper.get_parsed_page(f'{BASE_URL}/page/{page}')

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
                'url': f"{user.DOMAIN}/films/{slug}/",
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
            return user.scraper.get_parsed_page(f"{BASE_URL}/{page}")

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
                'link': user.DOMAIN + link,
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

# letterboxd.com/?/likes/reviews/
@assert_instance(User)
def user_liked_reviews(user: User) -> dict:
    '''Returns a dict of the other users whose reviews were liked'''
    REVIEWS_PER_PAGE = 12

    BASE_URL = "https://letterboxd.com/" + user.username + "/likes/reviews"

    page = 1
    ret = {'reviews':{}}
    while True:
        dom = user.scraper.get_parsed_page(BASE_URL + f'/page/{page}')

        container = dom.find("ul", {"class": ["film-list"]})
        items = container.find_all("li", {"class": ["film-detail"]})

        for item in items:
            elem_review_detail = item.find("div", {"class": ["film-detail-content"]})

            user_url = user.DOMAIN + elem_review_detail.find('a', {"class": ["avatar"]})['href']
            username = item['data-owner']
            elem_display_name = elem_review_detail.find('strong', {'class': ['name']})
            review_log_type = elem_display_name.previous_sibling.text.strip()
            review_log_type = review_log_type.split()[0]
            display_name = elem_display_name.text
            
            # movie
            movie_name = elem_review_detail.a.text
            movie_slug = elem_review_detail.parent.div['data-film-slug']
            movie_id = elem_review_detail.parent.div['data-film-id']
            movie_release = int(elem_review_detail.small.text) if elem_review_detail.small else None
            movie_url = f"{user.DOMAIN}/film/{movie_slug}/"

            # review
            review_id = item['data-object-id'].split(':')[-1]
            review_url = user.DOMAIN + elem_review_detail.a['href']
            review_date = elem_review_detail.find("span", {"class": ["_nobr"]})
            review_no = review_url.split(movie_slug)[-1]
            review_no = int(review_no.replace('/', '')) if review_no.count('/') == 2 else 0
            
            # script req
            # review_likes = int(elem_review_detail.find('a', {"class": ["count"]}).text.replace('.', ''))
            
            # rating
            review_rating = elem_review_detail.find("span", {"class": ["rating"]})
            review_rating = int(review_rating['class'][-1].split('-')[-1]) if review_rating else None

            review_content = elem_review_detail.find("div", {"class": ["body-text"]})
            spoiler = bool(review_content.find("p", {"class": ["contains-spoilers"]}))

            review_content = review_content.find_all('p')[1 if spoiler else 0:]
            review_content = '\n'.join([p.text for p in review_content])

            review_date = parse_review_date(review_log_type, review_date)

            ret['reviews'][review_id] = {
                # 'likes': review_likes, script req
                'type': review_log_type,
                'no': review_no,
                'url': review_url,
                'rating': review_rating,
                'review': {
                    'content': review_content,
                    'spoiler': spoiler,
                    'date': review_date,
                },
                'user': {
                    'username': username,
                    'display_name': display_name,
                    'url': user_url
                },
                'movie': {
                    'name': movie_name,
                    'slug': movie_slug,
                    'id': movie_id,
                    'release': movie_release,
                    'url': movie_url,
                },
                'page': page,
            }

        if len(items) < REVIEWS_PER_PAGE:
            break

        page += 1

    return ret

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
