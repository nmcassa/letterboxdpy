from datetime import datetime
from letterboxdpy.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN, CURRENT_YEAR


class UserDiary:

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{username}/diary"
        
    def get_diary(self, year: int=None, page: int=None) -> dict:
        return extract_user_diary(self.username, year, page)

    def get_wrapped(self, year: int=CURRENT_YEAR) -> dict:
        return extract_user_wrapped(self.username, year)

def extract_user_diary(username: str, year: int=None, page: int=None) -> dict:
    '''
    Returns:
      Returns a list of dictionaries with the user's diary'
      Each entry is represented as a dictionary with details such as movie name,
      release information,rewatch status, rating, like status, review status,
      and the date of the entry.
    '''
    BASE_URL = f"{DOMAIN}/{username}/films/diary/{f'for/{year}/'*bool(year)}"
    pagination = page if page else 1
    ret = {'entries': {}}

    while True:
        url = BASE_URL + f"page/{pagination}/"

        dom = parse_url(url)
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

# dependency: extract_user_diary()
def extract_user_wrapped(username: str, year: int=CURRENT_YEAR) -> dict:
    """Wraps user diary data for the specified year and calculates statistics."""

    def retrieve_diary() -> dict:
        """Retrieves the diary for the given user and year."""
        try:
            diary = extract_user_diary(username, year)
        except Exception as e:
            raise ValueError(f"Failed to retrieve diary for user {username}: {e}") from e
        
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
