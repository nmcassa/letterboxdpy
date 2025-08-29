import time
import sys
import os

try:
    # package is installed
    from letterboxdpy import user
    from letterboxdpy.utils.utils_string import strip_prefix
    from letterboxdpy.utils.utils_terminal import get_input
    from letterboxdpy.utils.utils_file import build_path, check_and_create_dirs, save_json, build_click_url
except ImportError:
    # not installed
    try:
        # use local copy
        sys.path.append(sys.path[0] + '/..')
        from letterboxdpy import user
        from letterboxdpy.utils.utils_string import strip_prefix
        from letterboxdpy.utils.utils_terminal import get_input
        from letterboxdpy.utils.utils_file import build_path, check_and_create_dirs, save_json, build_click_url
    except (ImportError, ValueError):
        print("letterboxdpy not installed, would you like to install it?")
        response = input("y/n: ").lower()
        if response == "y":
            os.system("pip install letterboxdpy --force")
            print("Installation complete, running script again...")
            sys.exit(0)
        print("Exiting...")
        sys.exit(1)

# -- MAIN --

username = get_input('Enter username: ', index=1)
user_instance = user.User(username)

current_directory = os.getcwd()

# Export directories
EXAMPLES_DIR = build_path(current_directory, 'examples')
EXPORTS_DIR = build_path(EXAMPLES_DIR, 'exports')
USERS_FOLDER = build_path(EXPORTS_DIR, 'users')
USER_FOLDER = build_path(USERS_FOLDER, user_instance.username)
directories = [EXAMPLES_DIR, EXPORTS_DIR, USERS_FOLDER, USER_FOLDER]
check_and_create_dirs(directories)

start_time = time.time()

# Save user instance data
user_data_path = build_path(USER_FOLDER, 'user')
save_json(user_data_path, user_instance.jsonify())

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
    save_json(file_path, data)

    print(f'{time.time() - method_start_time:<7.2f} seconds - {method_name:<22} - {build_click_url(file_path)}.json')

os.system('title Completed!')
print('\nProcessing complete!')
print(f'\tTotal time: {time.time() - start_time:.2f} seconds')

print('\tAt', build_click_url(USER_FOLDER), end='\n\n')
os.system('pause')