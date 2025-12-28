"""
Letterboxd User Data Exporter

Exports comprehensive user data from Letterboxd profiles.
- Export all user data (films, reviews, lists, followers, etc.)
- Automatic JSON file generation
- Organized directory structure
- Progress tracking and timing
"""

import time
import os

from letterboxdpy import user
from letterboxdpy.utils.utils_string import strip_prefix
from letterboxdpy.utils.utils_terminal import get_input
from letterboxdpy.utils.utils_file import build_path, JsonFile, build_click_url
from letterboxdpy.utils.utils_directory import check_and_create_dirs

# -- MAIN --

username = get_input('Enter username: ', index=1)
user_instance = user.User(username)

# Get the directory where this script is located (examples folder)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Export directories
EXPORTS_DIR = build_path(script_dir, 'exports')
USERS_FOLDER = build_path(EXPORTS_DIR, 'users')
USER_FOLDER = build_path(USERS_FOLDER, user_instance.username)
directories = [EXPORTS_DIR, USERS_FOLDER, USER_FOLDER]
check_and_create_dirs(directories)

start_time = time.time()

# Save user instance data
user_data_path = build_path(USER_FOLDER, 'user')
JsonFile.save(user_data_path, user_instance.jsonify())

# Export data for each method
# If you want to add a new method, add it here
# With arg: [user.User.user_watchlist, {'filters': {'genre': ['action', '-drama']}}],
methods = [
    user.User.get_activity,
    user.User.get_activity_following,
    user.User.get_diary,
    user.User.get_wrapped,
    user.User.get_films,
    [user.User.get_films_by_rating, {'rating':5}],
    user.User.get_films_not_rated,
    user.User.get_genre_info,
    user.User.get_liked_films,
    user.User.get_liked_reviews,
    user.User.get_lists,
    user.User.get_following,
    user.User.get_followers,
    user.User.get_reviews,
    user.User.get_user_tags,
    user.User.get_watchlist_movies,
    user.User.get_watchlist,
]
methods_str_length = len(str(len(methods)))

print('\nExporting data...')
for no, method in enumerate(methods, 1):
    method_start_time = time.time()

    args = {}
    if isinstance(method, list):
        method, args = method

    method_name = method.__name__
    method_name_without_prefix = strip_prefix(method_name)

    os.system(f'title [{len(methods)}/{no:0>{methods_str_length}}] Exporting {method_name}...')
    print(f'[{len(methods)}/{no:0>{methods_str_length}}]: Processing "{method_name}" method',
          end=f' with args: {args}...\r' if args else '...\r')

    data = method(user_instance, **args) if args else method(user_instance)

    file_path = build_path(USER_FOLDER, method_name_without_prefix)
    JsonFile.save(file_path, data)

    print(f'{time.time() - method_start_time:<7.2f} seconds - {method_name:<22} - {build_click_url(file_path)}.json')

os.system('title Completed!')
print('\nProcessing complete!')
print(f'\tTotal time: {time.time() - start_time:.2f} seconds')

print('\tAt', build_click_url(USER_FOLDER), end='\n\n')
os.system('pause')