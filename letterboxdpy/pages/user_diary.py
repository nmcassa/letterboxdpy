import warnings
from datetime import datetime
from functools import lru_cache
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

from letterboxdpy.constants.project import DOMAIN, CURRENT_YEAR, CURRENT_MONTH, CURRENT_DAY
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_url import get_page_url


class UserDiary:

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{username}/diary"
        
    def get_diary(
        self,
        year: int=None,
        month: int=None,
        day: int=None,
        page: int=None,
        fetch_runtime: bool=False,
        max_workers: int=None
    ) -> dict:
        return extract_user_diary(self.username, year, month, day, page, fetch_runtime, max_workers)

    def get_year(self, year: int=CURRENT_YEAR, fetch_runtime: bool=False, max_workers: int=None) -> dict:
        return extract_user_diary(self.username, year, fetch_runtime=fetch_runtime, max_workers=max_workers)

    def get_month(self, year: int=CURRENT_YEAR, month: int=CURRENT_MONTH, fetch_runtime: bool=False, max_workers: int=None) -> dict:
        return extract_user_diary(self.username, year, month, fetch_runtime=fetch_runtime, max_workers=max_workers)

    def get_day(self, year: int=CURRENT_YEAR, month: int=CURRENT_MONTH, day: int=CURRENT_DAY, fetch_runtime: bool=False, max_workers: int=None) -> dict:
        return extract_user_diary(self.username, year, month, day, fetch_runtime=fetch_runtime, max_workers=max_workers)

    def get_wrapped(self, year: int=CURRENT_YEAR, fetch_runtime: bool=False, max_workers: int=None) -> dict:
        return extract_user_wrapped(self.username, year, fetch_runtime, max_workers)

@lru_cache(maxsize=1024)
def _get_runtime(slug: str) -> Optional[int]:
    """Internal cached function to fetch runtime from Letterboxd JSON endpoint."""
    try:
        from letterboxdpy.url import FilmURL
        movie_json = FilmURL.json(slug)
        return movie_json.run_time if movie_json.run_time else None
    except Exception:
        return None

def clear_runtime_cache():
    """Clears the internal movie runtime cache."""
    _get_runtime.cache_clear()

def get_runtime_cache_info():
    """Returns information about the runtime cache (hits, misses, etc)."""
    return _get_runtime.cache_info()

def _fetch_missing_runtimes(entries: dict, pagination: int, max_workers: int = None) -> None:
    """
    Fetches missing runtime data for diary entries.
    
    Args:
        entries: Dictionary of diary entries to update (mutated in place).
        pagination: Current page number to filter entries.
        max_workers: Max threads for parallel fetching. None = sequential.
    """
    entries_to_update = [
        (log_id, entry["slug"]) 
        for log_id, entry in entries.items() 
        if entry["runtime"] is None and entry["slug"] and entry["page"]["no"] == pagination
    ]
    
    if not entries_to_update:
        return
    
    slugs = [str(slug) for _, slug in entries_to_update]
    
    if max_workers and max_workers > 1:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(_get_runtime, slugs))
    else:
        results = [_get_runtime(slug) for slug in slugs]
    
    for (log_id, _), fetched_runtime in zip(entries_to_update, results):
        if fetched_runtime:
            entries[log_id]["runtime"] = fetched_runtime

def extract_user_diary(
        username: str,
        year: int=None,
        month: int=None,
        day: int=None,
        page: int=None,
        fetch_runtime: bool=False,
        max_workers: int=None) -> dict:
    """
    Extracts the user's diary entries, optionally filtering by year, month, and day.

    Args:
        username (str): The Letterboxd username.
        year (int, optional): The year of diary entries.
        month (int, optional): The month of diary entries.
        day (int, optional): The day of diary entries.
        page (int, optional): The page number for pagination.
        fetch_runtime (bool, optional): If True, fetches runtime for each film.
        max_workers (int, optional): Max threads for parallel runtime fetching. 
                                     If None, runs sequentially (safer).

    Returns:
        dict: A dictionary with diary entries, each containing movie details, rewatch status, rating, like status, review status, and entry date.
    """
    
    def extract_movie_name(react_div, default="Unknown"):
        if not react_div:
            return default

        raw_name = react_div.get("data-item-name", default)
        if not raw_name or not isinstance(raw_name, str):
            return default

        return raw_name.rsplit(' (', 1)[0] if ' (' in raw_name and raw_name.endswith(')') else raw_name

    date_filter = f"for/{year}/" if year else ""
    date_filter += f"{str(month).zfill(2)}/" if month else ""
    date_filter += f"{str(day).zfill(2)}/" if day else ""

    BASE_URL = f"{DOMAIN}/{username}/films/diary/{date_filter}"
    pagination = page if page else 1
    ret = {'entries': {}}

    while True:
        url = get_page_url(BASE_URL, pagination)

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

                # day column (updated for new HTML structure)
                if 'daydate' in cols:
                    date = dict(zip(
                            ["year", "month", "day"],
                            map(int, cols['daydate'].a['href'].split('/')[-4:])
                        ))
                elif 'day' in cols:  # fallback for old structure
                    date = dict(zip(
                            ["year", "month", "day"],
                            map(int, cols['day'].a['href'].split('/')[-4:])
                        ))
                else:
                    # Extract from monthdate if available
                    date = {"year": None, "month": None, "day": None}
                # Extract film data from react-component
                production_col = cols.get('production')
                react_div = production_col.find('div', {'class': 'react-component'}) if production_col else None
                
                name = extract_movie_name(react_div)
                slug = react_div.get("data-item-slug") if react_div else None
                id = react_div.get("data-film-id") if react_div else None
                # released column (updated for new HTML structure)
                if 'releaseyear' in cols:
                    release = cols["releaseyear"].text.strip()
                elif 'released' in cols:  # fallback for old structure
                    release = cols["released"].text.strip()
                else:
                    release = ""
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
                # runtime from actions (handle missing attribute)
                runtime = actions.get("data-film-run-time") or actions.get("data-film-runtime")
                runtime = int(runtime) if runtime else None

                # create entry
                entry = {
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
                ret["entries"][log_id] = entry

            # Fetch runtime data if requested
            if fetch_runtime:
                _fetch_missing_runtimes(ret["entries"], pagination, max_workers)

            if len(rows) < 50 or pagination == page:
                    # no more entries
                    # or reached the requested page
                    break
            pagination += 1
        else: # no table
            break

    ret['count'] = len(ret['entries'])
    ret['last_page'] = pagination

    if not fetch_runtime and any(entry['runtime'] is None for entry in ret['entries'].values()):
        warnings.warn(
            "Runtime data is missing for some entries. "
            "Pass `fetch_runtime=True` to retrieve it (may require extra network requests).",
            UserWarning
        )

    return ret

# dependency: extract_user_diary()
def extract_user_wrapped(username: str, year: int=CURRENT_YEAR, fetch_runtime: bool=False, max_workers: int=None) -> dict:
    """Wraps user diary data for the specified year and calculates statistics.
    
    Args:
        username (str): The Letterboxd username.
        year (int, optional): The year to wrap. Defaults to current year.
        fetch_runtime (bool, optional): If True, fetches runtime for each film.
        max_workers (int, optional): Max threads for parallel runtime fetching.
    """

    def retrieve_diary() -> dict:
        """Retrieves the diary for the given user and year."""
        try:
            diary = extract_user_diary(username, year, fetch_runtime=fetch_runtime, max_workers=max_workers)
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
    months = {}.fromkeys(range(1, 13), 0)  # 12 months
    days = {}.fromkeys(range(1, 8), 0)    # 7 days (1=Monday, 7=Sunday)
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
