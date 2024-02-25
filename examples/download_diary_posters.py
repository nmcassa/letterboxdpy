import requests
import sys
import os

try:
    from letterboxdpy import user # package is installed
except ImportError: # not installed
    try:
        sys.path.append(sys.path[0] + '/..')
        from letterboxdpy import user # use local copy
    except (ImportError, ValueError):
        print("letterboxdpy not installed, would you like to install it?")
        response = input("y/n: ").lower()
        if response == "y":
            os.system("pip install letterboxdpy --force")
            print("Installation complete, running script again...")
            sys.exit(0)
        print("Exiting...")
        sys.exit(1)


class Settings:
    def __init__(self, foldering=True, size_check=False):
        self.foldering = foldering # Create folders for each day
        self.size_check = size_check  # Check if file size already exists

class Path:
    @staticmethod
    def check_path(*paths):
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)
                print('Directory created:', path)
            else:
                print('Directory found:', path)

    @staticmethod
    def save(file_path, data):
        with open(file_path, 'wb') as f:
            f.write(data)

class App:
    EXPORTS_DIR = "exports"
    EXPORTS_USERS_DIR = os.path.join(EXPORTS_DIR, "users")

    def __init__(self, username):
        self.username = username
        self.USER_FOLDER = os.path.join(self.EXPORTS_USERS_DIR, self.username)
        self.USER_POSTERS_DIR = os.path.join(self.USER_FOLDER, "posters")

        self.me = user.User(self.username)
        self.data = user.user_diary(self.me)
        self.config = Settings()
        
        self.foldering = self.config.foldering
        self.size_check = self.config.size_check

    def get_poster_url(self, slug):
        poster_ajax = f"https://letterboxd.com/ajax/poster/film/{slug}/std/500x750/"
        poster_page = self.me.get_parsed_page(poster_ajax)
        return poster_page.img['srcset'].split('?')[0]

    def run(self):
        
        count = self.data['count']
        entrys = self.data['entrys']
        already_start = 0

        if not count:
            print('No entries found')
            return

        print(f'Processing {count} entries..')

        Path.check_path(
            self.EXPORTS_DIR,
            self.EXPORTS_USERS_DIR,
            self.USER_FOLDER,
            self.USER_POSTERS_DIR
            )
        
        if self.foldering:
            years_dir = os.path.join(self.USER_POSTERS_DIR, 'years')
            Path.check_path(years_dir)
            previous_year = None

        for v in entrys.values():
            date = v["date"]

            file_date = "-".join(map(str, date.values()))
            file_dated_name = f"{file_date}_{v['slug']}.jpg"

            if self.foldering:
                current_year = str(date['year'])     
                year_dir = os.path.join(years_dir, current_year)
                if previous_year != current_year:
                    previous_year = current_year
                    Path.check_path(year_dir)    
                file_path = os.path.join(year_dir, file_dated_name)
            else:
                file_path = os.path.join(self.USER_POSTERS_DIR, file_dated_name)

            if os.path.exists(file_path):
                if not self.size_check:
                    if not already_start:
                        already_start = count
                    count -= 1
                    continue
                
                print(f'{count} - Poster file already exists, checking size..')
            
            if (already_start - count) > 1:
                print(f'Have already processed {already_start - count} entries, skipping {count}..')
                already_start = 0

            poster_url = self.get_poster_url(v['slug'])
            response = requests.get(poster_url)

            if os.path.exists(file_path):
                if int(os.stat(file_path).st_size) == int(response.headers['Content-Length']):
                    print(f'{count} - File already exists and has same size as new file, skipping..')
                    count -= 1
                    continue
                print(f'Rewriting {file_path}..')

            Path.save(file_path, response.content)
            print(f'{count} - Wrote {file_path}')
            count -= 1

        print('Processing complete!')
        click_url = 'file:///' + os.path.join(os.getcwd(), self.USER_POSTERS_DIR).replace("\\", "/")
        print('At', click_url)
        

if __name__ == '__main__':
    username = ''

    if not len(username):   
        try:
            username = sys.argv[1]
        except IndexError:
            print(f'Quick usage: python {sys.argv[0]} <username>')
            username = input('Enter username: ')

        app = App(username.lower())
        app.run()