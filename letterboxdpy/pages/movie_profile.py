from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.utils.utils_parser import extract_json_ld_script, get_meta_content


class MovieProfile:
    """Movie profile page operations - main movie details."""
    
    def __init__(self, slug: str):
        """Initialize MovieProfile with a movie slug."""
        self.slug = slug
        self.url = f"{DOMAIN}/film/{slug}"
        self.dom = parse_url(self.url)
        
        # Get script data for some fields
        self.script = extract_json_ld_script(self.dom)
    
    # one line contents
    def get_id(self) -> str: return extract_movie_id(self.dom)
    def get_title(self) -> str: return extract_movie_title(self.dom)
    def get_original_title(self) -> str: return extract_movie_original_title(self.dom)
    def get_runtime(self) -> int: return extract_movie_runtime(self.dom)
    def get_rating(self) -> float: return extract_movie_rating(self.dom, self.script)
    def get_year(self) -> int: return extract_movie_year(self.dom, self.script)
    def get_tmdb_link(self) -> str: return extract_movie_tmdb_link(self.dom)
    def get_imdb_link(self) -> str: return extract_movie_imdb_link(self.dom)
    def get_poster(self) -> str: return extract_movie_poster(self.script)
    def get_banner(self) -> str: return extract_movie_banner(self.dom)
    def get_tagline(self) -> str: return extract_movie_tagline(self.dom)
    
    # long contents
    def get_description(self) -> str: return extract_movie_description(self.dom)
    def get_trailer(self) -> dict: return extract_movie_trailer(self.dom)
    def get_alternative_titles(self) -> list: return extract_movie_alternative_titles(self.dom)
    def get_details(self) -> list: return extract_movie_details(self.dom)
    def get_genres(self) -> list: return extract_movie_genres(self.dom, self.slug)
    def get_cast(self) -> list: return extract_movie_cast(self.dom)
    def get_crew(self) -> dict: return extract_movie_crew(self.dom)
    def get_popular_reviews(self) -> list: return extract_movie_popular_reviews(self.dom)

# ONE LINE CONTENTS

def extract_movie_id(dom):
    """Extract movie ID from DOM."""
    from letterboxdpy.utils.utils_parser import extract_numeric_text
    elem = dom.find('span', 'block-flag-wrapper')
    elem = elem.find('a')
    return extract_numeric_text(elem.get('data-report-url'))

def extract_movie_title(dom):
    """Extract movie title from DOM."""
    h1_elem = dom.find("h1", {"class": ["primaryname"]})
    if h1_elem:
        span_elem = h1_elem.find("span", {"class": ["name"]})
        return span_elem.text if span_elem else h1_elem.text
    else:
        elem = dom.find("h1", {"class": ["filmtitle"]})
        return elem.text if elem else None

def extract_movie_original_title(dom):
    """Extract movie original title from DOM."""
    elem = dom.find("h2", {"class": ["originalname"]})
    return elem.text.strip() if elem else None

def extract_movie_runtime(dom):
    """Extract movie runtime from DOM."""
    elem = dom.find("p", {"class": ["text-footer"]})
    elem = elem.text if elem else None
    return int(
        elem.split('min')[0].replace(',', '').strip()
    ) if elem and 'min' in elem else None

def extract_movie_rating(dom, script=None):
    """Extract movie rating from DOM."""
    elem = dom.find('span', attrs={'class': 'average-rating'})
    rating = elem.text if elem else None
    try:
        rating = rating if rating else (
            script['aggregateRating']['ratingValue'] if script else None
        )
        return float(rating) if rating else None
    except (KeyError, ValueError):
        return None

def extract_movie_year(dom, script=None):
    """Extract movie year from DOM."""
    elem = dom.find('div', {'class': 'releaseyear'})
    year = elem.text if elem else None
    try:
        year = year if year else (
            script['releasedEvent'][0]['startDate'] if script else None
        )
        return int(year) if year else None
    except (KeyError, ValueError):
        return None

def extract_movie_tmdb_link(dom):
    """Extract TMDB link from DOM."""
    a = dom.find("a", {"data-track-action": ["TMDB"]})
    return a['href'] if a else None

def extract_movie_imdb_link(dom):
    """Extract IMDB link from DOM."""
    a = dom.find("a", {"data-track-action": ["IMDb"]})
    return a['href'] if a else None

def extract_movie_poster(script):
    """Extract movie poster from script."""
    # crop: list=(1500, 1000)
    # .replace('230-0-345', f'{crop[0]}-0-{crop[1]}')
    if script:
        poster = script['image'] if 'image' in script else None
        return poster.split('?')[0] if poster else None
    else:
        return None

def extract_movie_banner(dom):
    """Extract movie banner from DOM."""
    elem = dom.find("div", {"id": ["backdrop"]})
    exists = elem and "data-backdrop" in elem.attrs
    return elem['data-backdrop'].split('?')[0] if exists else None

def extract_movie_tagline(dom):
    """Extract movie tagline from DOM."""
    elem = dom.find(attrs={'class':'tagline'})
    return elem.text if elem else None

# LONG CONTENTS

def extract_movie_description(dom):
    """Extract movie description from DOM."""
    # elem_section = page.find("div", attrs={'class': 'truncate'}).text
    return get_meta_content(dom, name='description')

def extract_movie_popular_reviews(dom) -> list:
    """Extract popular reviews from main movie page."""
    container_section = dom.find("section", {"class": ["film-reviews"]})

    def get_text_or_none(element):
        return element.text.strip() if (element and element.text) else None

    def extract_reviewer_username(article):
        return article.get("data-person")

    def extract_reviewer_display_name(article):
        return get_text_or_none(article.find("strong", {"class": ["displayname"]}))

    def extract_review_link(article):
        context_link = article.find("a", {"class": ["context"]})
        href = context_link.get("href") if context_link else None
        return (DOMAIN + href) if href else None

    def extract_rating(article):
        rating_span = article.find("span", {"class": ["rating"]})
        if not (rating_span and rating_span.text):
            for span in article.find_all("span"):
                classes = span.get("class") or []
                if any((cls == "rating") or cls.startswith("rating") for cls in classes):
                    rating_span = span
                    break
        return get_text_or_none(rating_span)

    def extract_review_text(article):
        body_div = article.find("div", {"class": ["body-text"]})
        paragraph = body_div.find("p") if body_div else None
        return get_text_or_none(paragraph)

    reviews = []
    if container_section:
        article_elements = container_section.find_all("article", {"class": ["production-viewing"]})
        for article in article_elements:
            reviews.append({
                "user": {
                    "username": extract_reviewer_username(article),
                    "display_name": extract_reviewer_display_name(article)
                },  
                "link": extract_review_link(article),
                "rating": extract_rating(article),
                "review": extract_review_text(article),
            })

    return reviews

def extract_movie_trailer(dom):
    """Extract movie trailer from DOM."""
    elem = dom.find("p", {"class": ["trailer-link"]})

    if elem:
        elem = elem.a['href'].lstrip('/').split('?')[0]
        trailer_id = elem.split('/')[-1]

        return {
            'id': trailer_id,
            'link': f"https://www.youtube.com/watch?v={trailer_id}",
            'embed_url': f"https://{elem}",
        }
    return None

def extract_movie_alternative_titles(dom):
    """Extract movie alternative titles from DOM."""
    data = dom.find(attrs={'class': 'text-indentedlist'})
    text = data.text if data else None
    return [i.strip() for i in text.split(', ')] if text else None

def extract_movie_details(dom):
    """Extract movie details from DOM."""
    data = dom.find("div", {"id": ["tab-details"]})
    data = data.find_all("a") if data else []

    details = []
    for item in data:
        url_parts = item['href'].split('/')

        _ = url_parts[1] == 'films'
        item_type, slug = url_parts[1+_:3+_] 

        details.append({
            'type': item_type,
            'name': item.text.strip(),
            'slug': slug,
            'url': DOMAIN + "/".join(url_parts)
        })

    return details

def extract_movie_genres(dom, slug):
    """Extract movie genres from DOM."""
    data = dom.find(attrs={"id": ["tab-genres"]})
    data = data.find_all("a") if data else []

    genres = []
    for item in data:
        url_parts = item['href'].split('/')
        
        genres.append({
            'type': url_parts[2],
            'name': item.text,
            'slug': url_parts[3],
            'url': DOMAIN + "/".join(url_parts)
        })

    if genres and slug == genres[-1]['type']:
        genres.pop() # for show all button

    return genres


def extract_movie_cast(dom):
    """Extract movie cast from DOM."""
    data = dom.find("div", {"id": ["tab-cast"]})
    data = data.find_all("a", {"class": {"tooltip"}}) if data else []

    cast = []
    for person in data:
        name = person.text
        role_name = person['title'] if 'title' in person.attrs else None
        url = person['href']
        slug = url.split('/')[-2]
        
        cast.append({
            'name': name,
            'role_name': role_name,
            'slug': slug,
            'url': DOMAIN + url
        })

    return cast

def extract_movie_crew(dom):
    """Extract movie crew from DOM."""
    data = dom.find("div", {"id": ["tab-crew"]})
    data = data.find_all("a") if data else []

    crew = {}
    for person in data:
        name = person.text
        url = person['href']

        job, slug = filter(None, url.split('/'))
        job = job.replace('-', '_')

        if job not in crew:
            crew[job] = []

        crew[job].append({
            'name': name,
            'slug': slug,
            'url': DOMAIN + url
        })

    return crew
