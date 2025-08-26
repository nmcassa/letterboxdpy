"""
Activity Extractor Utilities
============================
Helper functions for extracting activity data from Letterboxd DOM elements.
"""

from datetime import datetime
from letterboxdpy.utils.utils_parser import parse_review_text


def parse_activity_datetime(date_string: str) -> datetime:
    """Parse datetime string with microseconds support."""
    try:
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')


def build_time_data(date_obj: datetime) -> dict:
    """Build time data dictionary from datetime object."""
    return {
        'year': date_obj.year,
        'month': date_obj.month,
        'day': date_obj.day,
        'hour': date_obj.hour,
        'minute': date_obj.minute,
        'second': date_obj.second
    }


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
def get_film_info(section) -> tuple:
    """Extract film name and year from section."""
    film = None
    film_year = None
    h2 = section.find("h2")
    if h2:
        film = h2.get_text().strip()
        year_link = section.find("a", href=lambda x: x and "/films/year/" in str(x))
        if year_link:
            try:
                film_year = int(year_link.get_text().strip())
            except ValueError:
                film_year = None
    return film, film_year


def get_rating(section) -> int:
    """Extract user rating from section."""
    rating = section.find("span", {"class": ["rating"], })
    return int(rating['class'][-1].split('-')[-1]) if rating else None


def build_review_title(film: str, log_type: str, rating: int, section) -> str:
    """Build readable title for review activity."""
    if film and log_type:
        username = section.find("a", href=lambda x: x and x.startswith('/') and len(x.split('/')) == 3)
        username_text = username.get_text().strip() if username else "User"
        rating_text = "★" * rating if rating else ""
        return f"{username_text} {log_type} {film} {rating_text}".strip()
    return ""


def get_username(section) -> str:
    """Extract username from target link."""
    target = section.find("a", {"class": "target"})
    if target:
        href = target.get('href', '')
        return href.replace('/', '') if '/' not in href[1:] else href.split('/')[1]
    return ""


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
        return target.text.split('  ')[-1].strip()
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
def process_review_activity(section, log_type: str) -> dict:
    """Process review-specific log data."""
    detail = section.find("div", {"class": "table-activity-viewing"})
    if not detail:
        detail = section.find("div", {"class": "film-detail-content"})
        if not detail:
            return {}

    film, film_year = get_film_info(section)
    rating = get_rating(section)
    review, spoiler = parse_review_text(section)
    log_title = build_review_title(film, log_type, rating, section)

    return {
        'log_type': log_type,
        'title': log_title,
        'film': film,
        'film_year': film_year,
        'rating': rating,
        'review': review,
        'spoiler': spoiler
    }


def process_basic_activity(section, title: str, log_type: str) -> dict:
    """Process basic log data."""
    log_data = {'log_type': log_type, 'title': title}

    if log_type == 'followed':
        log_data['username'] = get_username(section)
    elif log_type == 'liked':
        log_data['username'] = get_username(section)
    elif log_type == 'watched':
        log_data['film'] = get_film_name(section)
    elif log_type == 'commented':
        comment_data = get_comment_data(section)
        if comment_data.get('comment'):
            log_data['comment'] = comment_data['comment']
        if comment_data.get('target_url'):
            log_data['target_url'] = comment_data['target_url']
    elif log_type == 'cloned':
        log_data['cloned_list'] = get_cloned_list(section)

    return log_data


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
