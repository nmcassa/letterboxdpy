from letterboxdpy.utils.utils_file import JsonFile
from letterboxdpy.utils.utils_parser import extract_and_convert_shorthand
from letterboxdpy.core.encoder import Encoder
from letterboxdpy.avatar import Avatar
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.scraper import (
  parse_url,
  url_encode
)

class Search:
    SEARCH_URL = f"{DOMAIN}/s/search"
    MAX_RESULTS = 20 # 250
    MAX_RESULTS_PER_PAGE = 20
    MAX_RESULTS_PAGE = MAX_RESULTS // MAX_RESULTS_PER_PAGE
    FILTERS = ['films', 'reviews', 'lists', 'original-lists',
               'stories', 'cast-crew', 'members', 'tags',
               'articles', 'episodes', 'full-text']

    def __init__(self, query: str, search_filter: str=None):
      assert all([
          isinstance(query, str),
          not search_filter or search_filter in self.FILTERS
          ]), " ".join([
             "query and search_filter must be strings and",
             "search_filter must be one of the following:",
             ", ".join(self.FILTERS)
             ])

      self.query = url_encode(query)
      self.search_filter = search_filter
      self._results = None # .results
      self.url = "/".join(filter(None, [
          self.SEARCH_URL,
          search_filter,
          self.query
          ]))

    @property
    def results(self):
      if not self._results:
          self._results = self.get_results()
      return self._results

    def __str__(self):
      return JsonFile.stringify(self.__dict__, indent=2, encoder=Encoder)

    def get_results(self, end_page: int=MAX_RESULTS_PAGE, max: int=MAX_RESULTS):
      data = {
         'available': False,
         'query': self.query,
         'filter': self.search_filter,
         'end_page': end_page,
         'count': 0,
         'results': []
         }

      for current_page in range(1, end_page+1):
        url = f"{self.url.rstrip('/')}/page/{current_page}/?adult"
        dom = parse_url(url)
        results = self.get_page_results(dom)

        if not results:
          # no more results
          break

        for result in results:
          data['count'] += 1
      
          data['results'].append({
             'no':  data['count'],
             'page': current_page,
             **result
             })

          if  data['count'] >= max:
            break

        if  data['count'] >= max:
          break

      data['available'] = data['count'] > 0

      return data

    def get_page_results(self, dom) -> list:
      """
      Parse search results from DOM structure.
      
      DOM Structure:
      <ul class="results">
        <li class="search-result -production"> <!-- Film -->
        <li class="search-result -person"> <!-- Member -->
        <li class="search-result -viewing"> <!-- Review -->
        <li class="list-set"> <!-- List -->
        <li class="search-result -tag"> <!-- Tag -->
        <li class="search-result -contributor -actor"> <!-- Actor -->
        <li class="search-result -contributor -director"> <!-- Director -->
      </ul>
      """
      result_types = {
        # More specific types first to avoid false matches
        # Format: 'type': [class_to_check_on_li, [class_to_check_on_children]]
        'list': ["search-result", "-list"],  # <li class="search-result -list">
        'review': ["search-result", "-viewing"],  # <li class="search-result -viewing">
        'member': ["search-result", "-person"],  # <li class="search-result -person">
        'tag': ["search-result", "-tag"],  # <li class="search-result -tag">
        'actor': ["search-result", "-contributor", "-actor"],  # <li class="search-result -contributor -actor">
        'director': ["search-result", "-contributor", "-director"],  # <li class="search-result -contributor -director">
        'studio': ["search-result", "-contributor", "-studio"],  # <li class="search-result -contributor -studio">
        'story': [None, ['card-summary']],  # <li><div class="card-summary">
        'journal': [None, ["card-summary-journal-article"]],  # <li><div class="card-summary-journal-article">
        'podcast': [None, ["card-summary", "-graph"]],  # <li><div class="card-summary -graph">
        # Film - NOTE: Also has classes! search-result -production
        'film': ["search-result", "-production"],  # <li class="search-result -production">
      }

      # Find main results container: <ul class="results">
      elem_results = dom.find("ul", {"class": "results"})
      data = []

      if not elem_results:
        return data

      # Get all direct <li> children (recursive=False to avoid nested li elements)
      results = elem_results.find_all("li", recursive=False)
      
      for item in results:
        item_type = None

        # Determine result type by checking classes on <li> or child elements
        for r_type in result_types:
          if result_types[r_type][0]:
            # Check if <li> has specific class (e.g., "search-result -person")
            if 'class' in item.attrs and result_types[r_type][-1] in item.attrs['class']:
              item_type = r_type
              break
          else:
            # Check if <li> contains child with specific class (e.g., div.film-poster)
            keys = result_types[r_type][1][-1]
            child_elem = item.find(attrs={"class": lambda x: x and keys in x})
            if child_elem:
              item_type = r_type
              break
          
          if item_type:
            break
            
        # Parse the result content based on detected type
        result = self.parse_result(item, item_type)
        data.append(result)

      return data

    def parse_result(self, result, result_type):
      """
      Parse individual search result based on its type.
      Each type has a different DOM structure that needs specific parsing logic.
      """
      data = {'type': result_type}
      match result_type:
        case "film":
          """
          Letterboxd search result structure:
          <li class="search-result -production">
            <div class="react-component figure" data-component-class="LazyPoster" 
                 data-item-name="Film Title (Year)" data-item-slug="film-slug" 
                 data-item-link="/film/film-slug/" data-target-link="/film/film-slug/"
                 data-film-id="12345">
              <div class="poster film-poster">
                <img alt="Film Title" class="image" src="..." />
              </div>
            </div>
          </li>
          """
          # Find film container div
          film_container = result.find("div", {"class": "react-component"})
          
          if film_container:
            # Get basic film info from container
            slug = film_container.get('data-item-slug')
            name = film_container.get('data-item-name')
            url = DOMAIN + film_container.get('data-target-link')
            
            # Get poster from nested img element
            poster_img = film_container.find("img", {"class": "image"})
            poster = poster_img.get('src') if poster_img else None
            
            # Extract year from metadata
            movie_year = result.find("small", {"class": "metadata"})
            if movie_year and movie_year.a:
              movie_year = int(movie_year.a.text) if movie_year.a.text.isdigit() else None
            else:
              movie_year = None
          
          # Extract directors from film-metadata paragraph
          directors = []
          film_metadata = result.find("p", {"class": "film-metadata"})
          if film_metadata:
            for a in film_metadata.find_all("a"):
              director_slug = a.get('href', '').split('/')[-2]
              director_name = a.text.strip()
              director_url = DOMAIN + a.get('href', '')

              directors.append({
                'name': director_name,
                'slug': director_slug,
                'url': director_url
              })

          data |= {
             'slug': slug,
             'name': name,
             'year': movie_year,
             'url': url,
             'poster': poster,
             'directors': directors
             }
        case "member":
          """
          Member DOM Structure:
          <li class="search-result -person">
            <div class="person-summary -search">
              <a class="avatar -a40" href="/username/">
                <img alt="Display Name" src="avatar_url">
              </a>
              <h3 class="title-2">
                <a class="name" href="/username/">Display Name</a>
              </h3>
              <small class="metadata">Username</small>
            </div>
          </li>
          Note: followers/following counts no longer available in search results
          """
          # Navigate: li > div.person-summary > h3 > a
          person_link = result.find("h3", {"class": "title-2"}).a
          member_username = person_link['href'].split('/')[-2]
          member_name = person_link.text.strip()
          
          # Check for badge (might not exist)
          member_badge = person_link.find("span")
          member_badge = member_badge.text if member_badge else None
          
          # Get avatar from img tag
          member_avatar = result.find("img")['src']
          member_avatar = Avatar(member_avatar).upscaled_data

          # followers, following - no longer available in search results
          followers, following = None, None

          data |= {
             'username': member_username,
             'name': member_name,
             'badge': member_badge,
             'avatar': member_avatar,
             'followers': followers,
             'following': following
             }
        case "review":
          """
          Review DOM Structure:
          <li class="search-result -viewing">
            <div class="film-poster" data-film-slug="..." data-target-link="/film/...">
              <img alt="Film Title">
            </div>
            <!-- Review content -->
          </li>
          """
          # Review parsing - reviews show the film being reviewed
          # Get film info from the film-poster
          film_poster = result.find("div", {"class": lambda x: x and "film-poster" in x})
          if film_poster:
            slug = film_poster.get('data-film-slug')
            name = film_poster.img.get('alt') if film_poster.img else None
            url = DOMAIN + film_poster.get('data-target-link', '')
            
            # Get year from release date if available
            year = None  # Review search doesn't typically show year
            
            data |= {
               'slug': slug,
               'name': name,
               'year': year,
               'url': url,
               'poster': None,
               'directors': []
            }
        case "list":
          """
          List DOM Structure:
          <li class="search-result -list">
            <article class="list-summary" data-film-list-id="..." data-person="username">
              <div class="layout">
                <div class="body">
                  <div class="masthead">
                    <h2 class="name prettify">
                      <a href="/user/list/">List Title</a>
                    </h2>
                    <div class="attribution-block">
                      <div class="body">
                        <span class="attribution-detail">
                          <a class="owner" href="/user/">
                            <strong class="displayname">Owner Name</strong>
                          </a>
                        </span>
                        <span class="content-reactions-strip -filmlist">
                          <span class="value">X films</span>
                          <a class="inlineicon icon-like" href="/user/list/likes/">50K</a>
                          <a class="inlineicon icon-comment" href="/user/list/#comments">256</a>
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </article>
          </li>
          """
          # Real DOM structure parsing
          article = result.find('article', {'class': 'list-summary'})
          if not article:
            return data
          
          # Basic list info from article attributes
          list_id = article.get('data-film-list-id')
          owner_slug = article.get('data-person')
          
          # Title and URL from h2 > a
          title_link = article.find('h2', {'class': 'name'}).find('a')
          list_url = title_link['href']
          list_title = title_link.text.strip()
          list_slug = list_url.split('/')[-2]
          list_url = DOMAIN + list_url
          
          # Extract film count from span.value
          value_span = article.find('span', {'class': 'value'})
          item_count = None
          if value_span:
            text = value_span.text.strip()
            if 'film' in text:
              item_count = int(text.split('film')[0].strip().replace(',', ''))

          # Extract likes count from inlineicon icon-like
          like_elem = article.find('a', {'class': ['inlineicon', 'icon-like']})
          like_count = extract_and_convert_shorthand(like_elem)
          
          # Extract comments count from inlineicon icon-comment  
          comment_elem = article.find('a', {'class': ['inlineicon', 'icon-comment']})
          comment_count = extract_and_convert_shorthand(comment_elem)

          # Extract owner info from strong.displayname
          owner_strong = article.find('strong', {'class': 'displayname'})
          owner_name = owner_strong.text.strip() if owner_strong else owner_slug
          owner_slug = owner_slug.lower() if owner_slug else None
          owner_url = f"{DOMAIN}/{owner_slug}/" if owner_slug else None

          data |= {
             'id': list_id,
             'slug': list_slug,
             'url': list_url,
             'title': list_title,
             'count': item_count,
             'likes': like_count,
             'comments': comment_count,
             'owner': {
               'username': owner_slug,
               'name': owner_name,
               'url': owner_url
             }
          }
        case "tag":
          """
          Tag DOM Structure:
          <li class="search-result -tag">
            <h2><a href="/tag/...">Tag Name</a></h2>
          </li>
          """
          tag_url = DOMAIN + result.h2.a['href']
          tag_name = result.h2.a.text.strip()
          data |= {
             'name': tag_name,
             'url': tag_url
          }
        case "actor":
          """
          Actor DOM Structure:
          <li class="search-result -contributor -actor">
            <div class="icon-container"></div>
            <div class="content">
              <h2 class="title-2"><a href="/actor/...">Actor Name</a></h2>
              <p class="film-metadata">Star of X films, including...</p>
            </div>
          </li>
          """
          # Navigate: li > div.content > h2 > a
          content_div = result.find("div", {"class": "content"})
          actor_link = content_div.find("h2").a
          actor_name = actor_link.text.strip()
          actor_slug = actor_link['href']
          actor_url = DOMAIN + actor_slug
          actor_slug = actor_slug.split('/')[-2]
          data |= {
             'name': actor_name,
             'slug': actor_slug,
             'url': actor_url
          }
        case "director":
          """
          Director DOM Structure:
          <li class="search-result -contributor -director">
            <div class="icon-container"></div>
            <div class="content">
              <h2 class="title-2"><a href="/director/...">Director Name</a></h2>
              <p class="film-metadata">Director of X films, including...</p>
            </div>
          </li>
          """
          # Navigate: li > div.content > h2 > a
          content_div = result.find("div", {"class": "content"})
          director_link = content_div.find("h2").a
          director_name = director_link.text.strip()
          director_slug = director_link['href']
          director_url = DOMAIN + director_slug
          director_slug = director_slug.split('/')[-2]
          data |= {
             'name': director_name,
             'slug': director_slug,
             'url': director_url
          }
        case "studio":
          """
          Studio DOM Structure:
          <li class="search-result -contributor -studio">
            <a href="/studio/...">Studio Name</a>
          </li>
          """
          studio_name = result.a.text.strip()
          studio_url = DOMAIN + result.a['href']
          data |= {
             'name': studio_name,
             'url': studio_url
          }
        case "story":
          """
          Story DOM Structure:
          <li>
            <div class="card-summary">
              <figure><a href="/story/..."></a></figure>
              <h3><span>Story Title</span></h3>
              <p class="attribution"><a href="/user/...">Writer</a></p>
            </div>
          </li>
          """
          story_title = result.h3.span.text
          story_writer = result.find("p", {"class": "attribution"})
          story_writer_url = DOMAIN + story_writer.a['href'] if story_writer else None
          story_writer = story_writer.text.strip() if story_writer else None
          story_url = DOMAIN + result.figure.a['href']
          data |= {
             'title': story_title,
             'url': story_url,
             'writer': {
                'name': story_writer,
                'url': story_writer_url
             }
          }
        case "journal":
          """
          Journal DOM Structure:
          <li>
            <div class="card-summary-journal-article">
              <figure><a href="/journal/..."></a></figure>
              <time datetime="..."></time>
              <h3>Journal Title</h3>
              <div class="teaser">Journal excerpt...</div>
              <p class="attribution"><a href="/user/...">Writer</a></p>
            </div>
          </li>
          """
          journal_url = result.figure.a['href']
          journal_time = result.time['datetime']
          journal_title = result.h3.text
          journal_teaser = result.find("div", {"class": "teaser"})
          journal_teaser = journal_teaser.text.strip() if journal_teaser else None
          writer = result.find("p", {"class": "attribution"})
          writer_url = DOMAIN + writer.a['href'] if writer else None
          writer_name = writer.text.strip() if writer else None
          data |= {
             'title': journal_title,
             'url': journal_url,
             'time': journal_time,
             'writer': {
                'name': writer_name,
                'url': writer_url
             }
          }
        case _:
          # Unknown type or parsing not implemented yet
          pass

      return data

# -- FUNCTIONS --

def get_film_slug_from_title(title: str) -> str:
    """
    Helper function to get a film's slug from its title.
    Uses film search to find the best match and returns the slug of the first result.
    
    Args:
        title (str): The film title to search for
        
    Returns:
        str: The film slug if found, None if no results
        
    Example:
        >>> get_film_slug_from_title("The Matrix")
        'the-matrix'
    """
    try:
      query = Search(title, 'films')
      # return first page first result
      return query.get_results(max=1)['results'][0]['slug']
    except IndexError:
      return None

if __name__ == "__main__":
  import sys
  sys.stdout.reconfigure(encoding='utf-8')

  """
  phrase usage:
    q1 = Search("MUBI", 'lists')
    q2 = Search("'MUBI'", 'lists') 
    q1 searches for lists that contain the word 'MUBI' among other possible words
    q2 searches for lists that specifically contain the exact phrase 'MUBI' and
    ... exclude lists that don't contain this phrase

  results usage:
   all page:
    .results
    .get_results()
   filtering:
    .get_results(2)
    .get_results(max=10)

  Note: search pages may sometimes contain previous results. (for now)
  """

  q3 = Search("The") # general search
  q4 = Search("V for Vendetta", 'films')

  # test: instance printing
  print(q3)
  print(q4)

  # test: results
  # print(json.dumps(q3.results, indent=2))
  # print(json.dumps(q4.get_results(), indent=2))
  print(JsonFile.stringify(q3.get_results(2), indent=2)) # max 2 page result
  print("\n- - -\n"*10)
  print(JsonFile.stringify(q4.get_results(max=5), indent=2)) #  max 5 result

  # test: slug
  print('slug 1:', get_film_slug_from_title("V for Vendetta"))
  print('slug 2:', get_film_slug_from_title("v for"))
  print('slug 3:', get_film_slug_from_title("VENDETTA"))

  # test: combined
  from letterboxdpy.movie import Movie
  movie_slug = get_film_slug_from_title("V for Vendetta")
  movie_instance = Movie(movie_slug)
  print(movie_instance.description)
