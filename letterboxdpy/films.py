if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from letterboxdpy.scraper import Scraper

def mini_films_parser(url: str, max = 100):
    domain = "https://letterboxd.com"
    scraper = Scraper(domain)
    page = 1
    movies = {}
    while True:
        page_url = url + f"/page/{page}"
        dom = scraper.get_parsed_page(page_url) 

        new_data = dom.find_all("div", {"class": "film-poster"})
        for item in new_data:
            movie_id = item['data-film-id']
            movie_slug = item['data-film-slug'] 
            movie_name = item.img['alt']

            movies[movie_id] = {
                "slug": movie_slug,
                "name": movie_name,
                'url': f'https://letterboxd.com/film/{movie_slug}/'
            }

        if len(new_data) < max:
            break
        page += 1
    
    return movies

def films_parser(url: str, max=12*6):
    domain = "https://letterboxd.com"
    scraper = Scraper(domain)
    page = 1
    movies = {}
    while True:
        page_url = url + f"/page/{page}"
        dom = scraper.get_parsed_page(page_url) 

        new_data = dom.find_all("li")
        for item in new_data:
            rating_key = "data-average-rating"
            movie_rating = float(
                item['data-average-rating']) if rating_key in item.attrs else None
            movie_id = item.div['data-film-id']
            movie_slug = item.div['data-film-slug'] 
            movie_name = item.img['alt']

            movies[movie_id] = {
                "slug": movie_slug,
                "name": movie_name,
                "rating": movie_rating,
                'url': f'https://letterboxd.com/film/{movie_slug}/'
            }

        if len(new_data) < max:
            break
        page += 1
    
    return movies

def get_with_genre(genre: str) -> dict:
    # letterboxd.com/films/genre/<genre>
    # > letterboxd.com/films/ajax/genre/<genre>
    url = f"https://letterboxd.com/films/ajax/genre/{genre}"
    return films_parser(url)

def get_with_theme(theme: str) -> dict:
    # letterboxd.com/films/theme/<theme>
    # > letterboxd.com/films/ajax/theme/<theme>
    url = f"https://letterboxd.com/films/ajax/theme/{theme}"
    return films_parser(url)

def get_with_nanogenre(nanogenre: str):
    # letterboxd.com/films/nanogenre/<nanogenre>
    # > letterboxd.com/films/ajax/nanogenre/<nanogenre>
    url = f"https://letterboxd.com/films/ajax/nanogenre/{nanogenre}/"
    return films_parser(url)

def get_with_mini_theme(theme: str):
    # letterboxd.com/films/theme/<theme>
    # > letterboxd.com/films/ajax/theme/<theme>
    url = f"https://letterboxd.com/films/ajax/mini-theme/{theme}"
    return films_parser(url)

def get_with_language(language: str):
    pass

def get_with_country(country: str):
    pass

def get_with_year(year: int):
    pass

def get_with_actor(actor: str):
    pass

def get_with_director(director: str):
    pass

def get_with_writer(writer: str):
    pass

def movie_similar(slug: str) -> dict:
    # letterboxd.com/film/<slug>/similar
    # letterboxd.com/films/like/<slug>
    # letterboxd.com/films/like/<slug>
    # > letterboxd.com/films/ajax/like/<slug>
    list_url = f"https://letterboxd.com/films/ajax/like/{slug}"
    return films_parser(list_url)

if __name__ == "__main__":
    from letterboxdpy.movie import Movie
    sys.stdout.reconfigure(encoding='utf-8')

    # naoogenre using:
    # print(json.dumps(get_with_nanogenre("chilling-fear-extreme"), indent=2))

    # genre, theme, mini-theme using (with Movie instance):
    movie_slug = "v-for-vendetta"
    movie_instance = Movie(movie_slug)

    print(movie_slug)
    for genre in movie_instance.genres:
        genre_type = genre['type']
        genre_name = genre['slug']
        genre_url = genre['url']

        if genre_type == 'genre':
            continue # long process

        print(len(films_parser(
            genre_url.replace(".com/films/", ".com/films/ajax/"))), genre_name)
        
        """
        :alternative
        if genre_type == "genre":
            print(genre_name, len(get_with_genre(genre_name)))
        elif genre_type == "theme":
            print(genre_name, len(get_with_theme(genre_name)))
        elif genre_type == "mini-theme":
            print(genre_name, len(get_with_mini_theme(genre_name)))
        """