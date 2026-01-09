from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.pages.user_films import extract_user_films
from letterboxdpy.utils.utils_parser import parse_review_date, parse_iso_date
from letterboxdpy.utils.utils_url import extract_path_segment


class UserLikes:
    """UserLikes class for extracting user's liked content from Letterboxd."""

    def __init__(self, username: str) -> None:
        self.username = username
        self._base_url = f"{DOMAIN}/{self.username}/likes"
        
        # Likes endpoints
        self.films_url = f"{self._base_url}/films"
        self.reviews_url = f"{self._base_url}/reviews/"
        self.lists_url = f"{self._base_url}/lists"

    def get_liked_films(self): 
        """Get user's liked films."""
        return extract_user_films(self.films_url)
    
    def get_liked_reviews(self): 
        """Get user's liked reviews with detailed structure."""
        return extract_liked_reviews(self.reviews_url)
    
    def get_liked_lists(self): 
        """Get user's liked lists with count and pagination info."""
        return extract_liked_lists(self.lists_url)

def extract_liked_reviews(url: str) -> dict:
    """Extracts liked reviews from the user's likes page."""
    REVIEWS_PER_PAGE = 12
    ret = {'reviews': {}}

    def process_page(page: int) -> list:
        """Process a single page and return list of review items."""
        page_url = f"{url}/page/{page}" if page > 1 else url
        dom = parse_url(page_url)
        return dom.find_all("article", {"class": ["production-viewing"]})

    page = 1
    while True:
        items = process_page(page)

        for item in items:
            # For production-viewing structure, the review detail is in the body div
            elem_review_detail = item.find("div", {"class": ["body"]})
            if not elem_review_detail:
                raise ValueError(f"Review detail is missing for review item")
                
            # Extract user data
            username = item.get('data-owner', '')
            
            if not username:
                raise ValueError(f"Username is missing for review item")
                
            avatar_link = elem_review_detail.find('a', {"class": "avatar"})
            user_url = DOMAIN + avatar_link['href'] if avatar_link else f"{DOMAIN}/{username}/"
            name_elem = elem_review_detail.find('strong', {'class': 'name'})
            display_name = name_elem.text.strip() if name_elem else username
            review_log_type = "Review"
            
            # Extract movie data
            header = elem_review_detail.find("header", {"class": "inline-production-masthead"})
            if not header:
                raise ValueError(f"Header is missing for review item")
                
            film_link = header.find("a", href=lambda x: x and "/film/" in x)
            if not film_link:
                raise ValueError(f"Film link is missing for review item")
                
            movie_name = film_link.text.strip()
            if not movie_name:
                raise ValueError(f"Movie name is missing for review by user '{username}'")
                
            movie_slug = extract_path_segment(film_link['href'], after='/film/')
            if not movie_slug:
                raise ValueError(f"Movie slug is missing for movie '{movie_name}' by user '{username}'")
                
            movie_url = f"{DOMAIN}/film/{movie_slug}/"
            
            react_component = item.find("div", {"class": "react-component"})
            movie_id = react_component.get('data-film-id') if react_component else None
            
            if not movie_id:
                raise ValueError(f"Movie ID is missing for review of '{movie_name}' by user '{username}'")
            
            # Extract release year
            movie_release = None
            if header:
                import re
                header_text = header.get_text()
                year_match = re.search(r'\b(19|20)\d{2}\b', header_text)
                if year_match:
                    movie_release = int(year_match.group())
            
            if not movie_release:
                raise ValueError(f"Movie release year is missing for '{movie_name}' (ID: {movie_id}) by user '{username}'")

            # Extract review data
            review_id = extract_path_segment(item.get('data-object-id', ''), after=':')
            if not review_id:
                raise ValueError(f"Review ID is missing for review of '{movie_name}' by user '{username}'")
                
            review_url = movie_url  # Default to movie URL
            review_no = 0  # Default value
            
            # Extract rating (optional)
            review_rating = None
            all_spans = elem_review_detail.find_all("span")
            for span in all_spans:
                classes = span.get('class', [])
                rating_classes = [cls for cls in classes if 'rated-' in str(cls)]
                if rating_classes:
                    try:
                        review_rating = int(extract_path_segment(rating_classes[0], after='rated-'))
                        break
                    except (ValueError, IndexError):
                        pass

            # Extract content and spoiler flag
            content_elem = elem_review_detail.find("div", {"class": "body-text"})
            spoiler = False
            review_content = ""
            
            if content_elem:
                spoiler_elem = content_elem.find("p", {"class": lambda x: x and any('spoiler' in str(cls) for cls in x)})
                spoiler = spoiler_elem is not None
                
                paragraphs = content_elem.find_all('p')
                if paragraphs:
                    review_content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            if not review_content or review_content.strip() == "":
                raise ValueError(f"Review content is missing for review ID '{review_id}' of '{movie_name}' by user '{username}'")

            # Extract date
            date_elem = elem_review_detail.find("span", {"class": "_nobr"}) or elem_review_detail.find("time")
            review_date = None
            if date_elem:
                try:
                    # If it's a time element with datetime attribute, use existing parser
                    if date_elem.name == 'time' and date_elem.get('datetime'):
                        review_date = parse_iso_date(date_elem['datetime'])
                    else:
                        # Use the original parsing method
                        review_date = parse_review_date(review_log_type, date_elem)
                except (ValueError, IndexError):
                    review_date = None
            
            if not review_date:
                raise ValueError(f"Review date is missing for review ID '{review_id}' of '{movie_name}' by user '{username}'")

            # Build review entry
            ret['reviews'][review_id] = {
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

def extract_liked_lists(url: str) -> dict:
    """Extract liked lists from user's likes page."""    
    LISTS_PER_PAGE = 12
    data = {'lists': {}}
    
    def process_page(page: int) -> list:
        """Process a single page and return list of list summaries."""
        page_url = f"{url}/page/{page}" if page > 1 else url
        dom = parse_url(page_url)
        return dom.find_all('article', {'class': 'list-summary'})
    
    def extract_list_data(item):
        """Extract data from a single list item."""
        list_id = item.get('data-film-list-id')
            
        # Extract title and URL
        title_elem = item.find('h2', {'class': 'name'})
            
        title_link = title_elem.find('a')
        title = title_link.text.strip()
        list_url = DOMAIN + title_link['href']
        slug = extract_path_segment(title_link['href'], after='/list/')
        
        # Extract description
        description = ""
        notes_div = item.find('div', {'class': ['notes', 'body-text', '-reset', '-prose']})
        if notes_div:
            paragraphs = notes_div.find_all('p')
            description = '\n'.join([p.get_text().strip() for p in paragraphs])
        
        # Extract other data
        value_elem = item.find('span', {'class': 'value'})
        count = int(value_elem.text.strip().split()[0].replace(',', '')) if value_elem else 0
        
        likes_elem = item.find('a', {'class': lambda x: x and 'icon-like' in x})
        likes = 0
        if likes_elem:
            likes_span = likes_elem.find('span', {'class': 'label'})
            if likes_span:
                try:
                    likes = int(likes_span.text.strip())
                except ValueError:
                    pass
        
        comments_elem = item.find('a', {'class': lambda x: x and 'icon-comment' in x})
        comments = 0
        if comments_elem:
            comments_span = comments_elem.find('span', {'class': 'label'})
            if comments_span:
                try:
                    comments = int(comments_span.text.strip())
                except ValueError:
                    pass
        
        return {
            'id': list_id,
            'title': title,
            'slug': slug,
            'description': description,
            'url': list_url,
            'count': count,
            'likes': likes,
            'comments': comments
        }
    
    page = 1
    while True:
        list_summaries = process_page(page)
        
        for item in list_summaries:
            try:
                list_data = extract_list_data(item)
                if list_data:
                    list_id = item.get('data-film-list-id')
                    data['lists'][list_id] = list_data
            except Exception:
                continue
        
        if len(list_summaries) < LISTS_PER_PAGE:
            break
        
        page += 1
    
    data['count'] = len(data['lists'])
    data['last_page'] = page
    
    return data