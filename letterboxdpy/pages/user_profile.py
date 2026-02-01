import re

from letterboxdpy.utils.utils_file import JsonFile
from letterboxdpy.utils.utils_transform import month_to_index
from letterboxdpy.utils.utils_parser import get_meta_content, get_body_content
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.avatar import Avatar
from letterboxdpy.utils.utils_url import extract_path_segment
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.constants.forms.favorites import FAVORITE_ATTRS


class UserProfile:

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{self.username}"
        self.dom = parse_url(self.url)

    def __str__(self) -> str:
        return f"Not printable object of type: {self.__class__.__name__}"

    def get_id(self) -> int: return extract_id(self.dom)
    def get_hq_status(self) -> bool: return extract_hq_status(self.dom)
    def get_display_name(self) -> str: return extract_display_name(self.dom)
    def get_bio(self) -> str | None: return extract_bio(self.dom)
    def get_location(self) -> str | None: return extract_location(self.dom)
    def get_website(self) -> str | None: return extract_website(self.dom)
    def get_watchlist_length(self) -> int | None: return extract_watchlist_length(self.dom)
    def get_stats(self) -> dict: return extract_stats(self.dom)
    def get_favorites(self) -> dict: return extract_favorites(self.dom)
    def get_avatar(self) -> dict | None: return extract_avatar(self.dom)
    def get_watchlist_recent(self) -> dict: return extract_watchlist_recent(self.dom)
    def get_diary_recent(self) -> dict: return extract_diary_recent(self.dom)


def extract_id(dom) -> int:
    """Extracts the user ID from the DOM and returns it."""
    try:
        # Alternative method using the report button data attribute
        button_report = dom.find("button", {"data-js-trigger": "report"})
        if button_report:
            report_url = button_report['data-report-url']
            return int(extract_path_segment(report_url, after='person:', before='/'))
        else:
            # Fallback method using regex if button is not found
            pattern = r"/ajax/person:(\d+)/report-for"
            match = re.search(pattern, dom.prettify())
            if match:
                return int(match.group(1))
            else:
                raise ValueError("User ID not found in the DOM")
    except (AttributeError, ValueError) as e:
        raise RuntimeError("Failed to extract user ID from DOM") from e

def extract_hq_status(dom) -> bool:
    """Checks if the user has a high-quality account and returns the status."""
    try:
        data = dom.find("div", {'class': 'profile-summary'})
        if data and 'data-profile-summary-options' in data.attrs:
            profile_summary = data['data-profile-summary-options']
            return JsonFile.parse(profile_summary)['isHQ']
        else:
            return 'profile-hq' in (get_body_content(dom, 'class') or [])
    except Exception as e:
        raise RuntimeError("Failed to check HQ status from DOM") from e

def extract_display_name(dom) -> str:
    """Extracts the display name from the DOM using the Open Graph title property."""
    try:
        content = get_meta_content(dom, property='og:title')
        if content:
            return content[:-10]  # Remove the last 10 characters (e.g., " | Letterboxd")
        else:
            raise ValueError("Display name not found in the DOM")
    except Exception as e:
        raise RuntimeError("Failed to extract display name from DOM") from e

def extract_bio(dom) -> str | None:
    """Extracts the bio from the DOM using the Open Graph description property."""
    try:
        content = get_meta_content(dom, property='og:description')
        if content:
            return content.split('Bio: ')[-1] if 'Bio: ' in content else None
        else:
            raise ValueError("Bio not found in the DOM")
    except Exception as e:
        raise RuntimeError("Failed to extract bio from DOM") from e

def extract_location(dom) -> str | None:
    """Extracts the location from the DOM and returns it."""
    try:
        data = dom.find("div", {"class": ["profile-metadata"]})
        if data:
            location = data.find("div", {"class": ["metadatum"]})
            return location.find("span").text if location else None
        return None
    except Exception as e:
        raise RuntimeError("Failed to extract location from DOM") from e

def extract_website(dom) -> str | None:
    """Extracts the website from the DOM."""
    try:
        data = dom.find("div", {"class": ["profile-metadata"]})
        if data:
            website = data.find("a")
            return website['href'] if website else None
        return None
    except Exception as e:
        raise RuntimeError("Failed to extract website from DOM") from e

def extract_watchlist_length(dom) -> int | None:
    """Extracts the watchlist length from the DOM."""
    try:
        nav_links = dom.find_all("a", {"class": ["navlink"]})
        for link in nav_links:
            if "Watchlist" in link.text:
                if "rel" in link.attrs:
                    # 'User watchlist is not visible'
                    return None  # feature: PrivateData(Exception)
                else:
                    # 'User watchlist is visible'
                    widget = dom.find("section", {"class": ["watchlist-aside"]})
                    return int(
                        widget.find("a", {"class": ["all-link"]}).text.replace(',', '')
                    ) if widget else 0
        else:
            # HQ members
            # If no matching link found, return None
            return None
    except Exception as e:
        raise RuntimeError("Failed to extract watchlist length from DOM") from e

def extract_stats(dom) -> dict:
    """Extracts user statistics from the parsed DOM."""
    def extract_stat(stat_element) -> tuple:
        """Extracts the key-value pair from a stat element."""
        value = stat_element.span.text
        key = stat_element.text.lower().replace(value, '').replace(' ', '_').strip()
        return key, int(value.replace(',', ''))

    try:
        stats_elements = dom.find_all("h4", {"class": ["profile-statistic"]})
        if not stats_elements:
            raise ValueError("No statistics found in the DOM")

        return dict(extract_stat(stat) for stat in stats_elements)
    except AttributeError as e:
        raise RuntimeError("Error while parsing DOM structure") from e

def extract_favorites(dom) -> dict:
    """Extracts favorite films from the DOM and returns them as a dictionary."""
    try:
        favorites_section = dom.find("section", {"id": "favourites"})
        if not favorites_section:
            return {}
        
        poster_list = favorites_section.find("ul", class_="poster-list")
        if not poster_list:
            return {}
            
        favorites = {}
        items = poster_list.find_all("li")
        
        for item in items:
            react_div = item.find("div", class_=FAVORITE_ATTRS.COMPONENT_CLASS)
            if not react_div:
                continue
                
            # Extract data from react component attributes
            movie_id = react_div.get(FAVORITE_ATTRS.FILM_ID_ATTR)
            movie_slug = react_div.get(FAVORITE_ATTRS.FILM_SLUG_ATTR)
            movie_name = react_div.get(FAVORITE_ATTRS.FILM_NAME_ATTR)
            
            # Clean movie name (remove year) like we did in diary
            if movie_name and ' (' in movie_name and movie_name.endswith(')'):
                movie_name = movie_name.rsplit(' (', 1)[0]
            
            if movie_id and movie_slug and movie_name:
                # Extract additional data
                full_display_name = react_div.get('data-item-full-display-name', '')
                target_link = react_div.get('data-target-link', '')
                
                # Extract release year from full display name
                release_year = None
                if full_display_name and '(' in full_display_name and ')' in full_display_name:
                    try:
                        year_part = full_display_name.split('(')[-1].split(')')[0]
                        release_year = int(year_part) if year_part.isdigit() else None
                    except (ValueError, IndexError):
                        pass
                
                favorites[movie_id] = {
                    'slug': movie_slug,
                    'name': movie_name,
                    'url': f'https://letterboxd.com/film/{movie_slug}/',
                    'year': release_year,
                    'log_url': f'https://letterboxd.com{target_link}' if target_link else None
                }
        
        return favorites
    except Exception as e:
        raise RuntimeError("Failed to extract favorites from DOM") from e

def extract_avatar(dom) -> dict | None:
    """Extracts the user's avatar URL from the DOM and returns it."""
    try:
        elem_avatar = dom.find("div", {"class": ["profile-avatar"]})
        if elem_avatar and elem_avatar.img:
            avatar_url = elem_avatar.img['src']
            return Avatar(avatar_url).upscaled_data
        return None  # Avatar not found
    except Exception as e:
        raise RuntimeError("Failed to extract avatar from DOM") from e

def extract_watchlist_recent(dom) -> dict:
    """Extracts recent watchlist items from the DOM, with error handling."""
    def extract_movie_info(item) -> dict:
        """Extracts movie information from a watchlist item."""
        from letterboxdpy.utils.utils_string import extract_year_from_movie_name, clean_movie_name
        
        # Look for data attributes in the nested react-component div
        react_div = item.find('div', {'class': FAVORITE_ATTRS.COMPONENT_CLASS})
        
        if react_div:
            film_id = react_div.get(FAVORITE_ATTRS.FILM_ID_ATTR)
            film_slug = react_div.get(FAVORITE_ATTRS.FILM_SLUG_ATTR)
            raw_name = react_div.get(FAVORITE_ATTRS.FILM_NAME_ATTR, "Unknown")
            film_name = clean_movie_name(raw_name)
            year = extract_year_from_movie_name(raw_name)
        else:
            # Fallback to original method (for backwards compatibility)
            film_id = item.get('data-film-id')
            film_slug = item.get('data-film-slug')
            raw_name = item.img.get('alt', "Unknown") if item.img else "Unknown"
            film_name = clean_movie_name(raw_name)
            year = extract_year_from_movie_name(raw_name)

        return {
            'id': film_id,
            'slug': film_slug,
            'name': film_name,
            'year': year
        }

    watchlist_recent = {}
    section = dom.find("section", {"class": ["watchlist-aside"]})

    if not section:
        # User watchlist is not visible or there are no items in the watchlist
        return watchlist_recent

    watchlist_items = section.find_all("li", {"class": ["posteritem"]})

    if not watchlist_items:
        raise ValueError("No watchlist items found in the DOM")

    for item in watchlist_items:
        movie = extract_movie_info(item)
        if movie['id']:
            watchlist_recent[movie['id']] = movie

    return watchlist_recent

def extract_diary_recent(dom) -> dict:
    """Extracts recent diary entries from the DOM."""
    diary_recent = {'months':{}}
    # diary
    sections = dom.find_all("section", {"class": ["section"]})
    for section in sections:
        if section.h2 is None:
            continue

        if section.h2.text == "Diary":
            entry_list = section.find_all("li", {"class": ["listitem"]})

            for entry in entry_list:
                month_index = month_to_index(entry.h3.text)

                if month_index not in diary_recent['months']:
                    diary_recent['months'][month_index] = {}

                days = entry.find_all("dt")
                items = entry.find_all("dd")

                for day, item in zip(days, items):
                    movie_index = day.text
                    movie_slug = extract_path_segment(item.a['href'], after='/film/')
                    movie_name = item.text 

                    if movie_index not in diary_recent['months'][month_index]:
                        diary_recent['months'][month_index][movie_index] = []

                    diary_recent['months'][month_index][movie_index].append({
                        'name': movie_name,
                        'slug': movie_slug
                    })
            else:
                break
    return diary_recent
