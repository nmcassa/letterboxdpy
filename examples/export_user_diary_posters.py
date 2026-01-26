"""
Letterboxd Diary Poster Downloader

Downloads movie posters from user's diary entries.
- Extract poster URLs from diary entries
- Download and organize posters by year
- Automatic directory structure creation
- Skip existing files with size checking
"""

from curl_cffi import requests
import sys
import os
from bs4 import Tag

from letterboxdpy import user
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_parser import extract_json_ld_script
from fastfingertips.terminal_utils import get_input, args_exists
from letterboxdpy.utils.utils_file import BinaryFile
from letterboxdpy.utils.utils_directory import Directory


class Settings:
    def __init__(self, foldering=True, size_check=False):
        self.foldering = foldering # Create folders for each day
        self.size_check = size_check  # Check if file size already exists

class App:
    def __init__(self, username):
        # Get the directory where this script is located
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.EXPORTS_DIR = os.path.join(self.script_dir, "exports")
        self.EXPORTS_USERS_DIR = os.path.join(self.EXPORTS_DIR, "users")

        self.username = username.lower()
        self.USER_FOLDER = os.path.join(self.EXPORTS_USERS_DIR, self.username)
        self.USER_POSTERS_DIR = os.path.join(self.USER_FOLDER, "posters")

        self.user = user.User(self.username)
        self.data = self.user.get_diary()
        self.config = Settings()

        self.foldering = self.config.foldering
        self.size_check = self.config.size_check

    def _extract_from_json_ld(self, page) -> str | None:
        data = extract_json_ld_script(page)
        if data and 'image' in data:
            return data['image']
        return None

    def _extract_from_meta(self, page) -> str | None:
        meta = page.find("meta", property="og:image")
        if isinstance(meta, Tag):
            content = meta.get('content')
            if isinstance(content, str):
                return content
        return None

    def _extract_from_dom(self, page) -> str | None:
        poster_div = page.find("div", class_="poster")
        if isinstance(poster_div, Tag):
            img = poster_div.find("img")
            if isinstance(img, Tag):
                src = img.get("src")
                if isinstance(src, str):
                    return src
        return None

    def _extract_from_ajax(self, slug: str) -> str | None:
        poster_ajax = f"https://letterboxd.com/ajax/poster/film/{slug}/std/500x750/"
        poster_page = parse_url(poster_ajax)
        img = poster_page.find('img')
        if isinstance(img, Tag):
            srcset = img.get('srcset')
            if isinstance(srcset, str):
                return srcset.split('?')[0]
        return None

    def get_poster_url(self, slug: str) -> str:
        # Method 1: Scrape film page
        try:
            film_url = f"https://letterboxd.com/film/{slug}/"
            page = parse_url(film_url)
            
            if url := self._extract_from_json_ld(page):
                return url
            if url := self._extract_from_meta(page):
                return url
            if url := self._extract_from_dom(page):
                return url
        except Exception:
            pass

        # Method 2: Legacy AJAX endpoint (fallback)
        try:
            if url := self._extract_from_ajax(slug):
                return url
        except Exception:
            pass

        raise LookupError(f"Poster not found: {slug}")

    def _download_poster(self, slug: str, file_path: str, count: int) -> None:
        """Download poster and save to file with size check."""
        poster_url = self.get_poster_url(slug)
        response = requests.get(poster_url)

        if os.path.exists(file_path):
            if int(os.stat(file_path).st_size) == int(response.headers['Content-Length']):
                print(f'{count} - File already exists and has same size as new file, skipping..')
                return
            print(f'Rewriting {file_path}..')

        BinaryFile.save(file_path, response.content)
        print(f'{count} - Wrote {file_path}')

    def _resolve_file_path(self, date: dict, slug: str, years_dir: str | None, previous_year: str | None) -> tuple[str, str | None]:
        """Calculate target file path and handle year directory creation."""
        file_date = "-".join(map(str, date.values()))
        filename = f"{file_date}_{slug}.jpg"
        
        updated_year = previous_year

        if self.foldering and years_dir:
            current_year = str(date['year'])
            year_dir = os.path.join(years_dir, current_year)
            
            if previous_year != current_year:
                Directory.check(year_dir)
                updated_year = current_year
                
            return os.path.join(year_dir, filename), updated_year
            
        return os.path.join(self.USER_POSTERS_DIR, filename), previous_year

    def _should_skip_download(self, file_path: str, count: int) -> bool:
        """Determines if the download should be skipped based on file existence."""
        if not os.path.exists(file_path):
            return False
            
        if not self.size_check:
            return True
            
        print(f'{count} - Poster file already exists, checking size..')
        return False

    def run(self):
        count = self.data['count']
        entries = self.data['entries']
        already_start = 0

        if not count:
            print('No entries found')
            return

        print(f'Processing {count} entries..')

        Directory.check(
            self.EXPORTS_DIR,
            self.EXPORTS_USERS_DIR,
            self.USER_FOLDER,
            self.USER_POSTERS_DIR
        )

        years_dir = None
        previous_year = None

        if self.foldering:
            years_dir = os.path.join(self.USER_POSTERS_DIR, 'years')
            Directory.check(years_dir)

        for v in entries.values():
            file_path, previous_year = self._resolve_file_path(
                v['date'], v['slug'], years_dir, previous_year
            )

            if self._should_skip_download(file_path, count):
                if not already_start:
                    already_start = count
                count -= 1
                continue

            if already_start and (already_start - count) > 1:
                print(f'Have already processed {already_start - count} entries, skipping {count}..')
                already_start = 0

            try:
                self._download_poster(v['slug'], file_path, count)
            except Exception as e:
                print(f"Error downloadable {v['slug']}: {e}")

            count -= 1

        print('Processing complete!')
        click_url = 'file:///' + self.USER_POSTERS_DIR.replace("\\", "/")
        print('At', click_url)


if __name__ == '__main__':
    if not args_exists():
        print(f'Quick usage: python {sys.argv[0]} <username>')

    username = get_input('Enter username: ', index=1)
    app = App(username)
    app.run()
