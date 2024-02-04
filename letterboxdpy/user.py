import json
from json import JSONEncoder
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class User:
    DOMAIN = "https://letterboxd.com"

    def __init__(self, username: str) -> None:
        if not re.match("^[A-Za-z0-9_]*$", username):
            raise Exception("Invalid username")

        self.username = username.lower()
        
        self.page = self.get_parsed_page(f"{self.DOMAIN}/{self.username}/")
        self.user_watchlist_length() # .watchlist_length feature: self._watchlist_length
        self.user_favorites() # .favorites feature: self._favorites
        self.user_stats() # .stats feature: self._stats
    
    def __str__(self):
        return self.jsonify()

    def jsonify(self) -> str:
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url: str) -> None:
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": self.DOMAIN,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        try:
            response = requests.get(url, headers=headers, timeout=30)
        except requests.exceptions.Timeout:
            raise Exception("Request timeout, site may be down")

        return BeautifulSoup(response.text, "lxml")

    # letterboxd.com/?/
    def user_favorites(self) -> list:        
        data = self.page.find("section", {"id": ["favourites"], }).findChildren("div")
        names = []

        for div in data:
            img = div.find("img")
            movie_url = img.parent['data-film-slug']
            names.append((img['alt'], movie_url))
            
        self.favorites = names

    # letterboxd.com/?/
    def user_stats(self) -> dict:
        span = []
        stats = {}

        data = self.page.find_all("h4", {"class": ["profile-statistic"], })

        for item in data:
            span.append(item.findChildren("span"))

        for item in span:
            stats[item[1].text.replace(u'\xa0', ' ')] = item[0].text

        self.stats = stats

    # letterboxd.com/?
    def user_watchlist_length(self) -> str:
        nav_links = self.page.find_all("a", {"class": ["navlink"]})

        for link in nav_links:
            if "Watchlist" in link.text:
               try: 
                    link['rel'] # nofollow
                    # 'User watchlist is not visible'
                    # feature: PrivateData(Exception)
                    self.watchlist_length = None
               except KeyError:
                    # 'User watchlist is visible'
                    widget = self.page.find("section", {"class": ["watchlist-aside"]})
                    self.watchlist_length = int(widget.find("a", {"class": ["all-link"], }).text) if widget else 0

# letterboxd.com/?/films/
def user_films(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    count = 0
    rating_count = 0
    liked_count = 0
    movie_list = {'movies': {}}

    while True:
        count += 1
        page = user.get_parsed_page(f"{user.DOMAIN}/{user.username}/films/page/{count}/")

        poster_containers = page.find_all("li", {"class": ["poster-container"], })
        for poster_container in poster_containers:
            poster = poster_container.div
            poster_viewingdata = poster_container.p

            if '-rated-and-liked' in poster_viewingdata['class']:
                rating = int(poster_viewingdata.span['class'][-1].split('-')[-1])
                liked = True
                liked_count += 1
                rating_count += 1
            else:
                rating = None
                liked = False
                if poster_viewingdata.span:
                    if 'rating' in poster_viewingdata.span['class']:
                        # ['rating', '-tiny', '-darker', 'rated-9']
                        rating = int(poster_viewingdata.span['class'][-1].split('-')[-1])
                        rating_count += 1
                    elif 'like' in poster_viewingdata.span['class']:
                        # ['like', 'has-icon', 'icon-liked', 'icon-16']
                        liked = True
                        liked_count += 1

            movie_list["movies"][poster["data-film-slug"]] = {
                    'name': poster.img["alt"],
                    "id": poster["data-film-id"],
                    "rating": rating,
                    "liked": liked
                }

        if len(poster_containers) < 72:
            movie_list['count'] = len(movie_list['movies'])
            movie_list['liked_count'] = liked_count
            movie_list['rating_count'] = rating_count
            movie_list['liked_percentage'] = round(liked_count / movie_list['count'] * 100, 2)
            movie_list['rating_percentage'] = 0.0
            movie_list['rating_average'] = 0.0

            if rating_count:
                ratings = [movie['rating'] for movie in movie_list['movies'].values() if movie['rating'] is not None]
                movie_list['rating_percentage'] = round(rating_count / movie_list['count'] * 100, 2)
                movie_list['rating_average'] = round(sum(ratings) / rating_count, 2)

            break

    return movie_list

# letterboxd.com/?/following/
def user_following(user: User) -> dict:
    if type(user) != User:
        raise Exception("Improper parameter")

    # returns the first page of following
    page = user.get_parsed_page(f"{user.DOMAIN}/{user.username}/following/")
    data = page.find_all("img", attrs={'height': '40'})

    ret = {}

    for person in data:
        ret[person.parent['href'].replace('/', '')] = {
            'display_name': person['alt'],
        }

    return ret

# letterboxd.com/?/followers/
def user_followers(user: User) -> dict:
    if type(user) != User:
        raise Exception("Improper parameter")

    #returns the first page of followers
    page = user.get_parsed_page(f"{user.DOMAIN}/{user.username}/followers/")
    data = page.find_all("img", attrs={'height': '40'})

    ret = {}

    for person in data:
        ret[person.parent['href'].replace('/', '')] = {
            'display_name': person['alt'],
        }

    return ret

# letterboxd.com/?/films/genre/*/
def user_genre_info(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    genres = ["action", "adventure", "animation", "comedy", "crime", "documentary",
              "drama", "family", "fantasy", "history", "horror", "music", "mystery",
              "romance", "science-fiction", "thriller", "tv-movie", "war", "western"]
    ret = {}
    for genre in genres:
        page = user.get_parsed_page(f"{user.DOMAIN}/{user.username}/films/genre/{genre}/")
        data = page.find("span", {"class": ["replace-if-you"], })
        data = data.next_sibling.replace(',', '')
        try:
            ret[genre] = [int(s) for s in data.split() if s.isdigit()][0]
        except IndexError:
            ret[genre] = 0

    return ret

# letterboxd.com/?/films/reviews/
def user_reviews(user: User) -> dict:
    '''
    Returns a dictionary containing user reviews. The keys are unique log IDs,
    and each value is a dictionary with details about the review,
    including movie information, review type, rating, review content, date, etc.
    '''
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."
    
    LOGS_PER_PAGE = 12
    MONTH_ABBREVIATIONS = [
        "Jan", "Feb", "Mar",
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
        ]

    page = 0
    data = {'reviews': {}}
    while True:
        page += 1
        dom = user.get_parsed_page(f"{user.DOMAIN}/{user.username}/films/reviews/page/{page}/")
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
            if log_type == 'Added':
                # 2024-01-01T05:45:00.268Z
                date = dict(zip(
                    ['year', 'month', 'day'],
                    map(int, date.time['datetime'][:10].split('-')
                    )))
            else:
                # 01 Jan 2024
                date = date.text.split()
                date = {
                    'year': int(date[2]),
                    'month': MONTH_ABBREVIATIONS.index(date[1]) + 1,
                    'day': int(date[0])
                }
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
def user_diary(user: User, year: int=None, page: int=None) -> dict:
    '''
    Returns:
      Returns a list of dictionaries with the user's diary'
      Each entry is represented as a dictionary with details such as movie name,
      release information,rewatch status, rating, like status, review status,
      and the date of the entry.
    '''
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."
    
    BASE_URL = f"{user.DOMAIN}/{user.username}/films/diary/{f'for/{year}/'*bool(year)}"
    pagination = page if page else 1
    ret = {'entrys': {}}

    while True:
        url = BASE_URL + f"page/{pagination}/"

        dom = user.get_parsed_page(url)
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
                ret["entrys"][log_id] = {
                    "name": name,
                    "slug": slug,
                    "id":  id,
                    "release": release,
                    "runtime": runtime,
                    "rewatched": rewatched,
                    "rating": rating,
                    "liked": liked,
                    "reviewed": reviewed,
                    "date": date,
                    "page": page,
                }
            if len(rows) < 50 or pagination == page:
                    # no more entries
                    # or reached the requested page
                    break
            pagination += 1
        else: # no table
            break

    ret['count'] = len(ret['entrys'])
    ret['last_page'] = pagination

    return ret

# dependency: user_diary()
def user_wrapped(user: User, year: int=2024) -> dict:

    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    diary = user_diary(user, year)

    movies = {}
    milestones = {}
    months = {}.fromkeys([1,2,3,4,5,6,7,8,9,10,11,12], 0)
    days = {}.fromkeys([1,2,3,4,5,6,7], 0)
    total_review = 0
    total_runtime = 0
    first_watched = None
    last_watched = None

    no = 0
    for log_id, data in diary['entrys'].items():
        watched_date = data['date']

        if watched_date['year'] == year:
            no += 1

            movies[log_id] = data

            days[datetime(**watched_date).weekday()+1] += 1
            months[watched_date['month']] += 1

            reviewed = data['reviewed']
            total_review += 1 if reviewed else 0

            runtime = data['runtime']
            total_runtime += runtime if runtime else 0

            if not no % 50:
                milestones[no] = {log_id:data}

            if not last_watched:
                # first item is last watched
                last_watched = {log_id:data}
            else:
                # last item is first watched
                first_watched = {log_id:data}
    
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
def user_activity(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    BASE_URL = f"{user.DOMAIN}/ajax/activity-pagination/{user.username}"
    data = {'user': user.username, 'logs': {}}
    url = BASE_URL

    dom = user.get_parsed_page(url)
    sections = dom.find_all("section")
    if not sections:
        print(f"User {user.username} has no activity.")
        return data

    for section in sections:
        
        log_id = None
        event_type = None

        if any(x.startswith('-') for x in section['class']):
            event_type = list(filter(lambda x: x.startswith('-'), section['class']))[0][1:]

        if event_type == 'review' or event_type == 'basic':
            log_id = section["data-activity-id"]
            data['logs'][log_id] = {}
            # event time
            date = section.find("time")
            date = datetime.strptime(date['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            data['logs'][log_id] |= {
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
                # film
                detail = section.find("div", {"class": "film-detail-content"})
                log_title = detail.p.text.strip()
                log_type = log_title.split()[-1]
                film = detail.h2.find(text=True)
                # rating
                rating = section.find("span", {"class": ["rating"], })
                rating = int(rating['class'][-1].split('-')[-1]) if rating else None
                # year
                film_year = detail.h2.small.text
                film_year = int(film_year) if film_year else None
                # review
                review = detail.find("div", {"class": ["body-text"], })
                spoiler = bool(review.find("p", {"class": ["contains-spoilers"], }))
                review = review.find_all('p')[1 if spoiler else 0:]
                review = '\n'.join([p.text for p in review])
                data['logs'][log_id]|= {
                    'event': event_type,
                    'type': log_type,
                    'title': log_title,
                    'film': film,
                    'film_year': film_year,
                    'rating': rating,
                    'spoiler': spoiler,
                    'review': review
                }
            elif event_type == 'basic':
                log_title = section.p.text.strip()
                log_type = log_title.split()[1]
                data['logs'][log_id] |= {
                    'log_type': log_type,
                    'title': log_title
                    }

                # specials
                if log_type == 'followed':
                    username = section.find("a",{"class":["target"]})['href'].replace('/','')
                    data['logs'][log_id] |= {'username': username}
                elif log_type == 'liked':
                    # display name
                    # display_name = section.find("strong",{"class":["name"]}).text.replace('\u2019s',"")
                    username = section.find("a",{"class":["target"]})['href'].split('/')[1]
                    data['logs'][log_id] |= {'username': username}
                elif log_type == 'watched':
                    film = section.find("a",{"class":["target"]}).text.split('  ')[-1].strip()
                    film  = film if film else None
                    data['logs'][log_id] |= {'film': film}

        elif 'no-activity-message' in section['class']:
            break

    return data

# https://letterboxd.com/?/lists/
def user_lists(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    BASE_URL = f"{user.DOMAIN}/{user.username}/lists/"
    LISTS_PER_PAGE = 12

    selectors = {
        'list_set': ('section', {'class': 'list-set', }),
        'lists': ('section', {'class': 'list', }),
        'title': ('h2', {'class': 'title', }),
        'description': ('div', {'class': 'body-text', }),
        'value': ('small', {'class': 'value', }),
        'likes': ('a', {'class': 'icon-like', }),
        'comments': ('a', {'class': 'icon-comment', }),
    }

    page = 0
    data = {'lists': {}}
    while True:
        page += 1
        dom = user.get_parsed_page(f'{BASE_URL}/page/{page}')

        list_set = dom.find(*selectors['list_set'])
        if not list_set:
            break
        lists = list_set.find_all(*selectors['lists'])

        for item in lists:
            # id
            list_id = item['data-film-list-id']
            # title
            list_title = item.find(*selectors['title']).text.strip()
            # description
            description = item.find(*selectors['description'])
            if description:
                description = description.find_all('p')
                description = '\n'.join([p.text for p in description])
            # url
            list_url = item.find(*selectors['title']).a['href']
            # slug
            list_slug = list_url.split('/')[-2]
            # count
            count = int(item.find(*selectors['value']).text.split()[0].replace(',',''))
            # likes
            likes = item.find(*selectors['likes'])
            likes = int(likes.text.split()[0].replace(',','')) if likes else 0
            # comments
            # feature: https://letterboxd.com/ajax/filmlist:<list-id>/comments/
            comments = item.find(*selectors['comments'])
            comments = int(comments.text.split()[0].replace(',','')) if comments else 0

            data['lists'][list_id] = {
                'title': list_title,
                'slug': list_slug,
                'description': description,
                'url': user.DOMAIN + list_url,
                'count': count,
                'likes': likes,
                'comments': comments
                }

        if len(lists) < LISTS_PER_PAGE:
            break

    data['count'] = len(data['lists'])
    data['last_page'] = page
    return data

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest="user", help="Username to gather stats on")
    args = parser.parse_args()
    user = args.user

    if user:
        print(f"{user=}")
        userinfo = User(user)
        print(userinfo)
        print(user_films(userinfo))