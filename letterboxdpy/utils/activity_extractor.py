"""
Activity Extractor Utilities
============================
Helper functions for extracting activity data from Letterboxd DOM elements.
"""

from datetime import datetime
from letterboxdpy.utils.utils_parser import parse_review_text
from letterboxdpy.utils.date_utils import DateUtils

def parse_activity_datetime(date_string: str) -> datetime:
    """Parse datetime string from activity feed."""
    return DateUtils.parse_letterboxd_date(date_string)


def build_time_data(date_obj: datetime) -> str:
    """Build ISO timestamp string for activity data."""
    return DateUtils.format_to_iso(date_obj)


def get_event_type(section) -> str:
    """Extract event type from section classes."""
    if any(x.startswith('-') for x in section['class']):
        return list(filter(lambda x: x.startswith('-'), section['class']))[0][1:]
    return None


def get_log_title(section) -> str:
    """Extract log title from section."""
    return section.p.text.strip() if section.p else ""


def extract_review_type(log_title: str) -> str:
    """Extract log type from review activity text."""
    title_lower = log_title.lower()
    for action in ['rewatched', 'watched']:
        if action in title_lower:
            return action
    raise ValueError(f"Could not determine review type from: '{log_title}'")


def extract_basic_type(log_title: str) -> str:
    """Extract log type from basic activity text."""
    words = log_title.split()
    action_words = {'followed', 'rated', 'liked', 'watched', 'rewatched', 'added', 'commented', 'cloned'}

    # Check common word positions first
    if len(words) >= 3:
        for word in (words[2], words[1]):
            if word in action_words:
                return word

    # Search within the text
    log_title_lower = log_title.lower()
    for action in action_words:
        if action in log_title_lower:
            return action

    # Couldn't identify the action
    raise ValueError(
        f"Unknown basic log type: '{log_title}' "
        f"(words: {words}, expected: {sorted(action_words)})"
    )


def get_log_type(event_type: str, section) -> str:
    """Extract log type based on event type."""
    if event_type == 'basic':
        log_title = get_log_title(section)
        return extract_basic_type(log_title)
    elif event_type == 'newlist':
        return 'newlist'
    else:  # review
        detail = section.find("div", {"class": "table-activity-viewing"})
        if not detail:
            detail = section.find("div", {"class": "film-detail-content"})
        review_log_title = detail.get_text().strip() if detail else ""
        return extract_review_type(review_log_title) if review_log_title else 'watched'


# Film and User Info Extractors
def get_film_info(section, item_slug: str = None) -> dict:
    """Extract film information from section."""
    film_data = {
        'title': None,
        'year': None,
        'slug': item_slug,
        'url': None
    }
    
    h2 = section.find("h2")
    if h2:
        film_data['title'] = h2.get_text().strip()
        
        # Extract year
        year_link = section.find("a", href=lambda x: x and "/films/year/" in str(x))
        if year_link:
            try:
                film_data['year'] = int(year_link.get_text().strip())
            except ValueError:
                pass
    
    # Build URL from slug if available
    if item_slug:
        film_data['url'] = f"https://letterboxd.com/film/{item_slug}/"
    
    return film_data


def get_rating(section) -> int:
    """Extract user rating from section."""
    rating = section.find("span", {"class": ["rating"], })
    return int(rating['class'][-1].split('-')[-1]) / 2 if rating else None


def build_review_title(film: str, log_type: str, rating: int, section) -> str:
    """Build readable title for review activity."""
    if not (film and log_type):
        return ""
    
    def extract_username() -> str:
        """Extract username from section element."""
        def is_user_profile_link(href):
            """Check if href is a valid user profile link (e.g., '/username/')."""
            return href and href.startswith('/') and len(href.split('/')) == 3
        
        username_elem = section.find("a", href=is_user_profile_link)
        return username_elem.get_text().strip() if username_elem else "User"
    
    def build_rating_stars() -> str:
        """Build star rating text with half-star support."""
        if not rating:
            return ""
        
        stars = "★" * int(rating)
        if not float(rating).is_integer():
            stars += '½'
        return stars
    
    username = extract_username()
    rating_text = build_rating_stars()
    
    return f"{username} {log_type} {film} {rating_text}".strip()


def get_user_info(section) -> dict:
    """Extract user information from section."""
    user_data = {
        'username': None,
        'display_name': None,
        'profile_url': None
    }
    
    target = section.find("a", {"class": "target"})
    if target:
        href = target.get('href', '')
        username = href.replace('/', '') if '/' not in href[1:] else href.split('/')[1]
        user_data['username'] = username
        user_data['display_name'] = target.get_text().strip()
        user_data['profile_url'] = f"https://letterboxd.com{href}" if href.startswith('/') else href
    
    return user_data


def get_comment_data(section) -> dict:
    """Extract comment content and target URL."""
    data = {}
    comment_block = section.find("blockquote", {"class": "activity-comment-text"})
    if comment_block:
        data['comment'] = comment_block.get_text().strip()
    
    target_link = section.find("a", {"class": "target"})
    if target_link:
        data['target_url'] = target_link.get('href', '')
    return data


def get_film_name(section) -> str:
    """Extract film name from target link."""
    target = section.find("a", {"class": ["target"]})
    if target:
        return target.text.split('  ')[-1].strip().removeprefix("review of ")
    return ""


def get_cloned_list(section) -> str:
    """Extract cloned list info."""
    target_link = section.find("a", {"class": "target"})
    return target_link.get_text().strip() if target_link else ""


def get_list_info(section) -> dict:
    """Extract detailed list information from newlist activity."""
    info = {}
    
    # Find the list section
    list_section = section.find("section", {"class": "list"})
    if not list_section:
        return info
    
    # Extract film count
    film_count_span = list_section.find("span", {"class": "value"})
    if film_count_span:
        film_text = film_count_span.get_text().strip()
        info['film_count'] = film_text
    
    # Extract likes and comments count
    summary = section.find("p", {"class": "activity-summary"})
    reactions = summary.find("span", {"class": "content-reactions-strip"}) if summary else None
    if not reactions:
        reactions = list_section.find("span", {"class": "content-reactions-strip"})
    
    if reactions:
        # Extract like count
        like_link = reactions.find("a", {"class": lambda x: x and "inlineicon" in x and "icon-like" in x if x else False})
        if like_link:
            like_count = like_link.find("span", {"class": "label"})
            if like_count:
                info['likes'] = like_count.get_text().strip()
        
        # Extract comment count
        comment_link = reactions.find("a", {"class": lambda x: x and "inlineicon" in x and "icon-comment" in x if x else False})
        if comment_link:
            comment_count = comment_link.find("span", {"class": "label"})
            if comment_count:
                info['comments'] = comment_count.get_text().strip()
    
    # Extract list description
    description_div = list_section.find("div", {"class": "activity-list-description"})
    if description_div:
        paragraphs = description_div.find_all("p")
        descriptions = []
        for p in paragraphs:
            text = p.get_text().strip()
            if text:
                descriptions.append(text)
        
        if descriptions:
            info['description'] = descriptions[0] if len(descriptions) == 1 else descriptions
    
    # Extract source and target list info
    target_link = section.find("a", {"class": "target"})
    if target_link:
        info['target_list'] = {
            'name': target_link.get_text().strip(),
            'url': target_link.get('href', '')
        }
    
    # Extract source list info from spans
    nobr_span = section.find("span", {"class": "nobr"})
    if nobr_span:
        source_link = nobr_span.find("a")
        if source_link:
            info['source_list'] = {
                'name': source_link.get_text().strip(),
                'url': source_link.get('href', '')
            }
    
    return info


# Activity Processing Functions
def process_review_activity(section, log_type: str, item_slug: str = None) -> dict:
    """Process review-specific log data."""
    detail = section.find("div", {"class": "table-activity-viewing"})
    if not detail:
        detail = section.find("div", {"class": "film-detail-content"})
        if not detail:
            return {}

    # Get structured film information
    film_info = get_film_info(section, item_slug)
    rating = get_rating(section)
    review, spoiler = parse_review_text(section)
    log_title = build_review_title(film_info.get('title'), log_type, rating, section)

    activity_data = {
        'action': log_type,
        'description': log_title
    }

    # Add movie information if available
    if any(film_info.values()):
        activity_data['movie'] = {k: v for k, v in film_info.items() if v is not None}

    # Add rating information
    if rating:
        activity_data['rating'] = rating

    # Add review information
    if review:
        activity_data['review'] = {
            'content': review,
            'contains_spoilers': spoiler if spoiler is not None else False
        }

    return activity_data


def process_basic_activity(section, title: str, log_type: str, item_slug: str = None) -> dict:
    """Process basic activity log data."""
    activity_data = {
        'action': log_type,
        'description': title
    }

    if log_type == 'followed':
        # Extract user information for follow activities
        target = section.find("a", {"class": "target"})
        if target:
            href = target.get('href', '')
            username = href.replace('/', '') if '/' not in href[1:] else href.split('/')[1]
            activity_data['user'] = {
                'username': username,
                'display_name': target.get_text().strip(),
                'profile_url': f"https://letterboxd.com{href}" if href.startswith('/') else href
            }
    
    elif log_type in ['liked', 'watched', 'added', 'rated']:
        # Extract movie information for film-related activities
        movie_data = {}
        
        # Get film title from target link
        film_name = get_film_name(section)
        if film_name:
            movie_data['title'] = film_name
        
        # Add slug and URL when available
        if item_slug:
            movie_data['slug'] = item_slug
            movie_data['url'] = f"https://letterboxd.com/film/{item_slug}/"
        
        # Extract year information when available
        film_info = get_film_info(section, item_slug)
        if film_info.get('year'):
            movie_data['year'] = film_info['year']
        
        if movie_data:
            activity_data['movie'] = movie_data

        # Add rating
        rating = get_rating(section)
        if rating:
            activity_data['rating'] = rating
    
    elif log_type == 'commented':
        comment_data = get_comment_data(section)
        if comment_data.get('comment'):
            activity_data['comment'] = {
                'content': comment_data['comment'],
                'target_url': comment_data.get('target_url')
            }
    
    elif log_type == 'cloned':
        cloned_list_name = get_cloned_list(section)
        if cloned_list_name:
            activity_data['list'] = {'name': cloned_list_name}

    return activity_data


def process_newlist_activity(section, title: str, log_type: str) -> dict:
    """Process newlist log data."""
    log_data = {'log_type': log_type, 'title': title}
    
    list_info = get_list_info(section)
    if list_info:
        if list_info.get('film_count'):
            log_data['film_count'] = list_info['film_count']
        if list_info.get('description'):
            log_data['description'] = list_info['description']
        if list_info.get('likes'):
            log_data['likes'] = list_info['likes']
        if list_info.get('comments'):
            log_data['comments'] = list_info['comments']
        if list_info.get('target_list'):
            log_data['target_list'] = list_info['target_list']
        if list_info.get('source_list'):
            log_data['source_list'] = list_info['source_list']
    
    return log_data


def get_log_item_slug(event_type: str, section) -> str | None:
    """Extract log item slug based on event type."""

    if event_type == "basic":
        anchor_tag = section.find("a", {"class": "target"})
        item_slug = anchor_tag.attrs['href'].split('/')[-2]
        return item_slug
    
    elif event_type == "review":
        div = section.find("div", {"class": "react-component"})
        item_slug = div.attrs.get("data-item-slug")
        return item_slug
    
    return None