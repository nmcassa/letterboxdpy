"""
Activity Extractor Utilities
============================
Helper functions for extracting activity data from Letterboxd DOM elements.
"""

from typing import Any
from datetime import datetime
from letterboxdpy.utils.utils_parser import parse_review_text
from letterboxdpy.utils.date_utils import DateUtils
from letterboxdpy.utils.utils_url import extract_path_segment
from letterboxdpy.constants.project import DOMAIN


# -- Date/Time Utilities (Stateless) --

def parse_activity_datetime(date_string: str) -> datetime | None:
    """Parse datetime string from activity feed."""
    return DateUtils.parse_letterboxd_date(date_string)


def build_time_data(date_obj: datetime | None) -> str | None:
    """Build ISO timestamp string for activity data."""
    return DateUtils.format_to_iso(date_obj)


# -- Activity Processor Class --

class ActivityProcessor:
    """
    Handles processing of different activity types from a DOM section.
    Encapsulates all extraction logic utilizing the section element.
    """

    def __init__(self, section):
        self.section = section
    
    # -- Type Identification Methods --

    def get_event_type(self) -> str | None:
        """Extract event type from section classes."""
        if any(x.startswith('-') for x in self.section['class']):
            return list(filter(lambda x: x.startswith('-'), self.section['class']))[0][1:]
        return None

    def get_log_title(self) -> str:
        """Extract log title from section text."""
        return self.section.p.text.strip() if self.section.p else ""

    @staticmethod
    def _extract_review_type(log_title: str) -> str:
        """Extract log type from review activity text."""
        title_lower = log_title.lower()
        for action in ['rewatched', 'watched']:
            if action in title_lower:
                return action
        raise ValueError(f"Could not determine review type from: '{log_title}'")

    @staticmethod
    def _extract_basic_type(log_title: str) -> str:
        """Extract log type from basic activity text."""
        words = log_title.split()
        action_words = {'followed', 'rated', 'liked', 'watched', 'rewatched', 'added', 'commented', 'cloned'}

        if len(words) >= 3:
            for word in (words[2], words[1]):
                if word in action_words:
                    return word

        log_title_lower = log_title.lower()
        for action in action_words:
            if action in log_title_lower:
                return action

        raise ValueError(f"Unknown basic log type: '{log_title}'")

    def get_log_type(self) -> str:
        """Determine log type based on event category."""
        event_type = self.get_event_type()
        
        def filter_basic() -> str:
            return self._extract_basic_type(self.get_log_title())

        def filter_review() -> str:
            detail = self.section.find("div", {"class": "table-activity-viewing"}) or \
                     self.section.find("div", {"class": "film-detail-content"})
            
            review_log_title = detail.get_text().strip() if detail else ""
            return self._extract_review_type(review_log_title) if review_log_title else 'watched'

        match event_type:
            case 'basic': return filter_basic()
            case 'newlist': return 'newlist'
            case _: return filter_review()

    def get_log_item_slug(self) -> str | None:
        """Extract log item slug based on event type."""
        event_type = self.get_event_type()
        
        if event_type == "basic":
            targets = self.section.find_all("a", {"class": "target"})
            if targets:
                return targets[-1].attrs['href'].split('/')[-2]
        
        elif event_type == "review":
            if div := self.section.find("div", {"class": "react-component"}):
                return div.attrs.get("data-item-slug")
        
        return None

    # -- Data Extraction Helpers --

    def get_user_info(self) -> dict[str, str | None]:
        """Extract user information from section."""
        user_data: dict[str, str | None] = {
            'username': None,
            'display_name': None,
            'profile_url': None
        }
        
        if target := self.section.find("a", {"class": "target"}):
            href = target.get('href', '')
            user_data['username'] = extract_path_segment(href, after='/', before='/')
            user_data['display_name'] = target.get_text().strip()
            user_data['profile_url'] = f"{DOMAIN}{href}" if href.startswith('/') else href
        
        return user_data

    def get_film_info(self, item_slug: str | None = None) -> dict[str, str | int | None]:
        """Extract film information from section."""
        film_data: dict[str, str | int | None] = {
            'title': None,
            'year': None,
            'slug': item_slug,
            'url': None
        }
        
        if h2 := self.section.find("h2"):
            film_data['title'] = h2.get_text().strip()
            
            year_link = self.section.find("a", href=lambda x: x and "/films/year/" in str(x))
            if year_link:
                try:
                    film_data['year'] = int(year_link.get_text().strip())
                except ValueError:
                    pass
        
        if item_slug:
            film_data['url'] = f"{DOMAIN}/film/{item_slug}/"
        
        return film_data

    def get_film_name(self) -> str:
        """Extract film name from target link."""
        targets = self.section.find_all("a", {"class": ["target"]})
        if targets:
            return targets[-1].text.split('  ')[-1].strip().removeprefix("review of ")
        return ""

    def get_rating(self) -> float | None:
        """Extract user rating from section."""
        rating = self.section.find("span", {"class": ["rating"]})
        if rating:
            rating_val = extract_path_segment(rating['class'][-1], after='rated-')
            return float(rating_val) / 2 if rating_val else None
        return None

    def build_review_title(self, film: str | None, log_type: str | None, rating: float | None) -> str:
        """Build readable title for review activity."""
        if not (film and log_type):
            return ""
        
        def extract_username() -> str:
            def is_user(href):
                return href and href.startswith('/') and len(href.split('/')) == 3
            username_elem = self.section.find("a", href=is_user)
            return username_elem.get_text().strip() if username_elem else "User"
        
        def build_rating_stars() -> str:
            if not rating: return ""
            stars = "★" * int(rating)
            if not float(rating).is_integer(): stars += '½'
            return stars
        
        return f"{extract_username()} {log_type} {film} {build_rating_stars()}".strip()

    def get_comment_data(self) -> dict:
        """Extract comment content and target URL."""
        data = {}
        if comment_block := self.section.find("blockquote", {"class": "activity-comment-text"}):
            data['comment'] = comment_block.get_text().strip()
        
        if target_link := self.section.find("a", {"class": "target"}):
            data['target_url'] = target_link.get('href', '')
        return data

    def get_cloned_list(self) -> str:
        """Extract cloned list info."""
        target_link = self.section.find("a", {"class": "target"})
        return target_link.get_text().strip() if target_link else ""

    # -- Internal Processing Helpers --

    def _extract_list_reactions(self, list_section) -> dict[str, str]:
        """Helper to extract likes and comments from a list activity."""
        reactions_data = {}
        summary = self.section.find("p", {"class": "activity-summary"})
        reactions = summary.find("span", {"class": "content-reactions-strip"}) if summary else None
        
        if not reactions:
            reactions = list_section.find("span", {"class": "content-reactions-strip"})
        
        if reactions:
            like_link = reactions.find("a", {"class": lambda x: x and "icon-like" in x})
            if like_link and (like_count := like_link.find("span", {"class": "label"})):
                reactions_data['likes'] = like_count.get_text().strip()
            
            comment_link = reactions.find("a", {"class": lambda x: x and "icon-comment" in x})
            if comment_link and (comment_count := comment_link.find("span", {"class": "label"})):
                reactions_data['comments'] = comment_count.get_text().strip()
                
        return reactions_data

    @staticmethod
    def _extract_list_description(list_section) -> str | list[str] | None:
        """Helper to extract description paragraphs from a list activity."""
        if description_div := list_section.find("div", {"class": "activity-list-description"}):
            paragraphs = [p.get_text().strip() for p in description_div.find_all("p") if p.get_text().strip()]
            if paragraphs:
                return paragraphs[0] if len(paragraphs) == 1 else paragraphs
        return None

    def get_list_info(self) -> dict:
        """Extract detailed list information from newlist activity."""
        info = {}
        list_section = self.section.find("section", {"class": "list"})
        if not list_section:
            return info
        
        if film_count_span := list_section.find("span", {"class": "value"}):
            info['film_count'] = film_count_span.get_text().strip()
        
        # Extract reactions
        info.update(self._extract_list_reactions(list_section))
        
        # Extract description
        if description := self._extract_list_description(list_section):
            info['description'] = description
        
        # Extract target list info
        if target_link := self.section.find("a", {"class": "target"}):
            info['target_list'] = {
                'name': target_link.get_text().strip(),
                'url': target_link.get('href', '')
            }
        
        # Extract source list info from spans
        if nobr_span := self.section.find("span", {"class": "nobr"}):
            if source_link := nobr_span.find("a"):
                info['source_list'] = {
                    'name': source_link.get_text().strip(),
                    'url': source_link.get('href', '')
                }
        
        return info

    def _handle_follow_activity(self, activity_data: dict[str, Any]):
        """Internal helper to process follow activities."""
        targets = self.section.find_all("a", {"class": "target"})
        if targets:
            target = targets[-1]
            href = target.get('href', '')
            activity_data['user'] = {
                'username': extract_path_segment(href, after='/', before='/'),
                'display_name': target.get_text().strip(),
                'profile_url': f"{DOMAIN}{href}"
            }

    def _handle_item_activity(self, activity_data: dict[str, Any], item_slug: str | None):
        """Internal helper to process movie or list related activities."""
        targets = self.section.find_all("a", {"class": "target"})
        if not (target := targets[-1] if targets else None):
            return
        
        href = target.get('href', '')
        is_list = '/list/' in href
        
        item_data: dict[str, Any] = {
            'title': self.get_film_name()
        }
        if is_list:
            item_data['title'] = item_data['title'].removesuffix(" list")
        
        if item_slug:
            item_data['slug'] = item_slug
            item_data['url'] = f"{DOMAIN}{href}" if is_list else f"{DOMAIN}/film/{item_slug}/"
            if not is_list and (year := self.get_film_info(item_slug).get('year')):
                item_data['year'] = year
        
        activity_data['list' if is_list else 'movie'] = item_data
        if rating := self.get_rating():
            activity_data['rating'] = rating

    def _handle_comment_activity(self, activity_data: dict[str, Any]):
        """Internal helper to process comment activities."""
        comment_data = self.get_comment_data()
        if comment := comment_data.get('comment'):
            activity_data['comment'] = {
                'content': comment,
                'target_url': comment_data.get('target_url')
            }

    # -- Main Processors --

    def process_review(self, log_type: str, item_slug: str | None = None) -> dict:
        """Process review-specific log data."""
        detail = self.section.find("div", {"class": ["table-activity-viewing", "film-detail-content"]})
        if not detail:
            return {}

        film_info = self.get_film_info(item_slug)
        rating = self.get_rating()
        review, spoiler = parse_review_text(self.section)
        log_title = self.build_review_title(
            str(film_info.get('title')) if film_info.get('title') else None,
            log_type,
            rating
        )

        activity_data: dict[str, Any] = {
            'action': log_type,
            'description': log_title
        }

        if any(film_info.values()):
            activity_data['movie'] = {k: v for k, v in film_info.items() if v is not None}

        if rating: activity_data['rating'] = rating
        if review:
            activity_data['review'] = {
                'content': review,
                'contains_spoilers': spoiler if spoiler is not None else False
            }

        return activity_data

    def process_basic(self, title: str | None, log_type: str, item_slug: str | None = None) -> dict:
        """Process basic activity log data."""
        activity_data: dict[str, Any] = {
            'action': log_type,
            'description': title # log summary
        }

        match log_type:
            case 'followed': self._handle_follow_activity(activity_data)
            case 'commented': self._handle_comment_activity(activity_data)
            case 'cloned':
                activity_data['list'] = {
                    'name': self.get_cloned_list()
                }
            case _: self._handle_item_activity(activity_data, item_slug)

        return activity_data

    def process_newlist(self, title: str, log_type: str) -> dict:
        """Process newlist log data."""
        log_data = {
            'log_type': log_type,
            'title': title
        }
        list_info = self.get_list_info()
        if list_info:
            for key in ['film_count', 'description', 'likes', 'comments', 'target_list', 'source_list']:
                if val := list_info.get(key):
                    log_data[key] = val
        return log_data
