from bs4 import BeautifulSoup
from typing import List
import requests
import json

class Search:
    DOMAIN = "https://letterboxd.com"
    SEARCH_URL = f"{DOMAIN}/search"
    FILTERS = [
       'films', 'reviews', 'lists', 'original-lists',
       'stories', 'cast-crew', 'members', 'tags',
       'articles', 'episodes', 'full-text'
       ]

    def __init__(self, query: str, search_filter: str=None):

      if search_filter and search_filter not in self.FILTERS:
          raise ValueError(f"Invalid filter: {search_filter}")

      url = "/".join(filter(None, [
        self.SEARCH_URL,
        search_filter,
        query,
        '?adult'
        ]))
      self.query = query
      self.search_filter = search_filter
      page = self.get_parsed_page(url)
      self.results = self.get_results(page)

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)
    
    def get_parsed_page(self, url: str) -> BeautifulSoup:
      headers = {
        "referer": self.DOMAIN,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
      }
      response = requests.get(url, headers=headers)
      return BeautifulSoup(response.text, "lxml")

    def get_results(self, page) -> List:

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

      data = {
        'available': False,
        'query': self.query,
        'filter': self.search_filter,
        'count': 0,
        'results': []
        }
      results = page.find("ul", {"class": "results"})

      if not results:
        return data

      # recursive: pass list posters
      results = results.find_all("li", recursive=False)
      no = 0
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
        no += 1
        result_content = self.parse_result(item, item_type)
        result_content[item_type] = {'no': no} | result_content[item_type]
        data['results'].append(result_content)
      
      # return content
      count = len(data['results'])
      data['available'] = bool(count)
      data['count'] = count

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
          list_title = result.h2.text.strip()
          list_count = result.find('small', {'class': 'value'})
          list_count = int(
             list_count.text.split('f')[0].strip().replace(',', '')
             ) if list_count else None
          data[result_type] = {
             'type': result_type,
             'id': list_id,
             'title': list_title,
             'count': list_count
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
            actor_url = self.DOMAIN + result.a['href']
            data[result_type] = {
               'type': result_type,
               'name': actor_name,
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
      return query.results['results'][0]['film']['slug']
    except IndexError:
      return None

if __name__ == "__main__":
  import sys
  sys.stdout.reconfigure(encoding='utf-8')

  # todo: multiple page parsing

  # tests
  """
  print('slug 1:', get_film_slug_from_title("V for Vendetta"))
  print('slug 2:', get_film_slug_from_title("v for"))
  print('slug 3:', get_film_slug_from_title("VENDETTA"))
  """
  # tests
  """
  from letterboxdpy import movie
  movie_slug = get_film_slug_from_title("V for Vendetta")
  movie_instance = movie.Movie(movie_slug)
  print(movie_instance.description)
  """
  # tests
  """
  q1 = Search("The") # general search
  q2 = Search("V for Vendetta", 'films')
  q3 = Search("MUBI", 'lists')
  """
  q4 = Search("Nolan", 'members')
  print(json.dumps(q4.results, indent=2))
