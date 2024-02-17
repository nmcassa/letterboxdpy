from avatar import Avatar
from bs4 import BeautifulSoup
from typing import List
import requests
import json

class Search:
    DOMAIN = "https://letterboxd.com"
    SEARCH_URL = f"{DOMAIN}/search"
    MAX_RESULTS = 250
    MAX_RESULTS_PER_PAGE = 20
    MAX_RESULTS_PAGE = MAX_RESULTS // MAX_RESULTS_PER_PAGE + 1

    FILTERS = [
       'films', 'reviews', 'lists', 'original-lists',
       'stories', 'cast-crew', 'members', 'tags',
       'articles', 'episodes', 'full-text'
       ]

    def __init__(self, query: str, search_filter: str=None):

      if search_filter and search_filter not in self.FILTERS:
          raise ValueError(f"Invalid filter: {search_filter}")

      self.url = "/".join(filter(None, [
        self.SEARCH_URL,
        search_filter,
        query
        ]))
      self.query = query
      self.search_filter = search_filter
      self._results = None

    @property
    def results(self):
      if not self._results:
          self._results = self.get_results()
      return self._results

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

    def get_parsed_page(self, url: str) -> BeautifulSoup:
      headers = {
        "referer": self.DOMAIN,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
      }
      response = requests.get(url, headers=headers)
      return BeautifulSoup(response.text, "lxml")

    def get_results(self, end_page: int=MAX_RESULTS_PAGE, max: int=None):
      data = {
        'available': False,
        'query': self.query,
        'filter': self.search_filter,
        'end_page': end_page,
        'count': 0,
        'results': []
        }

      no = 1
      for current_page in range(1, end_page+1):
        url = "/".join(map(str, [
           self.url, "page", current_page, "?adult"
           ]))
        page = self.get_parsed_page(url)
        results = self.get_page_results(page)

        if not results:
          # no more results
          break

        for result in results:
          key, value = list(result.items())[0]
          data['results'].append({
            key: {
               'no': no,
               'page': current_page 
               } | value
            })
          if max and no >= max:
            break
          no += 1
        if max and no >= max:
          break
  
      count = len(data['results'])
      data['available'] = bool(count)
      data['count'] = count

      return data

    def get_page_results(self, page) -> List:
      result_types = {
        'film': [None, ["film-poster"]],
        'review': ["film-detail"],
        'list': ["list-set"],
        'story': [None, ['card-summary']],
        # Cast, Crew or Studios
        # 'cast': ["search-result", "-contributor",],
        'actor': ["search-result", "-contributor", "-actor"],
        'director': ["search-result", "-contributor", "-director"],
        'studio': ["search-result", "-contributor", "-studio"],
        # Members or HQs
        'member': ["search-result", "-person"],
        'tag': ["search-result", "-tag"],
        'journal': [None, ["card-summary-journal-article"]],
        'podcast': [None, ["card-summary", "-graph"]],
      }

      elem_results = page.find("ul", {"class": "results"})
      data = []

      if not elem_results:
        return data

      # recursive: pass list posters
      results = elem_results.find_all("li", recursive=False)
      for item in results:
        item_type = None

        # parsing result type
        for r_type in result_types:
          if 'class' in item.attrs:
            if result_types[r_type][0]:
              if result_types[r_type][-1] in item.attrs['class']:
                  item_type = r_type
                  #:print(item.attrs['class'])
                  break
          else:
            if not result_types[r_type][0]:
              keys = result_types[r_type][1][-1]
              if keys in item.find_next().attrs['class']:
                item_type = r_type
                #:print(item.find_next().attrs['class'])
                break

        # result content
        result_content = self.parse_result(item, item_type)
        result_content[item_type] = result_content[item_type]
        data.append(result_content)

      return data

    def parse_result(self, result, result_type):
      data = {result_type: {}}
      match result_type:
        case "film":
          film_poster = result.div
          film_metadata = result.find("p", {"class": "film-metadata"})
          # slug, name, url, poster
          slug = film_poster['data-film-slug']
          name = film_poster.img['alt']
          url = self.DOMAIN + film_poster['data-target-link']
          poster = None # film_poster.img['src']
          # movie year
          movie_year = result.h2.small
          movie_year = int(movie_year.text) if movie_year else None
          # directors
          film_metadata = film_metadata if film_metadata else None
          directors = {}
          if film_metadata:
            for a in film_metadata.find_all("a"):
              director_slug = a['href'].split('/')[-2]
              director_name = a.text
              director_url = self.DOMAIN + a['href']
      
              directors[director_slug] = {
                'name':director_name,
                'url': director_url
                }             

          data[result_type] = {
              "slug": slug,
              "name": name,
              "year": movie_year,
              "url": url,
              "poster": poster,
              "directors": directors
              }
        case "member":
          member_username = result.h3.a['href'].split('/')[-2]
          member_name = result.h3.a
          member_badge = member_name.span
          member_name = member_name.contents[0].text.strip()
          member_badge = member_badge.text if member_badge else None
          member_avatar = result.img['src']
          member_avatar = Avatar(member_avatar).upscaled_data

          # followers, following
          followers, following = [a.text for a in result.small.find_all("a")]
          followers = followers.split('f')[0].strip().replace(',', '')
          following = following.split('g')[1].strip().replace(',', '')
          followers = int(followers) if followers.isdigit() else None
          following = int(following) if following.isdigit() else None

          data[result_type] = {
             'username': member_username,
             'name': member_name,
             'badge': member_badge,
             'avatar': member_avatar,
             'followers': followers,
             'following': following,
             }
        case "list":
          list_id = result.section['data-film-list-id']
          list_url = result.a['href']
          list_slug = list_url.split('/')[-2]
          list_url = self.DOMAIN + list_url
          list_title = result.h2.text.strip()
          item_count = result.find('small', {'class': 'value'})
          item_count = int(
             item_count.text.split('f')[0].strip().replace(',', '')
             ) if item_count else None

          # likes
          like_count = result.find('a', {'class': 'icon-like'})
          like_count = like_count if like_count else 0
          if like_count:
            like_count = like_count.text.strip().replace(',', '')
            if 'K' in like_count:
                # example: 6.3K -> 6300
                like_count = float(like_count.replace('K', ''))
                like_count *= 1000
            like_count = int(like_count)

          # comments
          comment_count = result.find('a', {'class': 'icon-comment'})
          comment_count = comment_count if comment_count else 0
          if comment_count:
            comment_count = comment_count.text.strip().replace(',', '')
            if 'K' in comment_count:
                comment_count = float(comment_count.replace('K', ''))
                comment_count *= 1000
            comment_count = int(comment_count)

          # owner
          owner = result.find('strong', {'class': 'name'}).a
          owner_name = owner.text
          owner_url = owner['href']
          owner_slug = owner_url.split('/')[-2]
          owner_url = self.DOMAIN + owner_url

          data[result_type] = {
             'type': result_type,
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
            tag_url = self.DOMAIN + result.h2.a['href']
            tag_name = result.h2.a.text.strip()
            data[result_type] = {
               'type': result_type,
               'name': tag_name,
               'url': tag_url
            }
        case "actor":
            actor_name = result.a.text.strip()
            actor_slug = result.a['href']
            actor_url = self.DOMAIN + actor_slug
            actor_slug = actor_slug.split('/')[-2]
            data[result_type] = {
               'type': result_type,
               'name': actor_name,
               'slug': actor_slug,
               'url': actor_url
            }
        case "studio":
            studio_name = result.a.text.strip()
            studio_url = self.DOMAIN + result.a['href']
            data[result_type] = {
               'type': result_type,
               'name': studio_name,
               'url': studio_url
            }
        case "story":
            story_title = result.h3.span.text
            story_writer = result.find("p", {"class": "attribution"})
            story_writer_url = self.DOMAIN + story_writer.a['href'] if story_writer else None
            story_writer = story_writer.text.strip() if story_writer else None
            story_url = self.DOMAIN + result.figure.a['href']
            data[result_type] = {
               'type': result_type,
               'title': story_title,
               'url': story_url,
               'writer': {
                  'name': story_writer,
                  'url': story_writer_url
               }
            }
        case "journal":
            journal_url = result.figure.a['href']
            journal_time = result.time['datetime']
            journal_title = result.h3.text
            journal_teaser = result.find("div", {"class": "teaser"})
            journal_teaser = journal_teaser.text.strip() if journal_teaser else None
            writer = result.find("p", {"class": "attribution"})
            writer_url = self.DOMAIN + writer.a['href'] if writer else None
            writer_name = writer.text.strip() if writer else None
            data[result_type] = {
               'type': result_type,
               'title': journal_title,
               'url': journal_url,
               'time': journal_time,
               'writer': {
                  'name': writer_name,
                  'url': writer_url
               }
            }
        case _:
          # unknown type or not ready yet
          pass

      return data

def get_film_slug_from_title(title: str) -> str:
    try:
      query = Search(title, 'films')
      # return first page first result
      return query.get_results(1)['results'][0]['film']['slug']
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
  # print(json.dumps(q3.results, indent=2))
  # print(json.dumps(q4.get_results(), indent=2))
  print(json.dumps(q3.get_results(2), indent=2)) # max 2 page result
  print("\n- - -\n"*10)
  print(json.dumps(q4.get_results(max=5), indent=2)) #  max 5 result

  # test: slug
  print('slug 1:', get_film_slug_from_title("V for Vendetta"))
  print('slug 2:', get_film_slug_from_title("v for"))
  print('slug 3:', get_film_slug_from_title("VENDETTA"))

  # test: combined
  from letterboxdpy import movie
  movie_slug = get_film_slug_from_title("V for Vendetta")
  movie_instance = movie.Movie(movie_slug)
  print(movie_instance.description)