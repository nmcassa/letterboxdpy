from json import dump as json_dump
import time
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

def get_username(username: str = '') -> str:
    """Get the username from command line or input."""
    if not len(username):
        try:
            username = sys.argv[1]
        except IndexError:
            print(f'Quick usage: python {sys.argv[0]} <username>')
            username = input('Enter username: ')
    return username

def save_data(path: str, data: dict) -> None:
    """Save data to a file as JSON."""
    with open(f'{path}.json', 'w') as f:
        json_dump(data, f, indent=2)

def check_and_create_dirs(directories: list) -> None:
    """Checks if directories exist, creates them if not."""
    print('\nChecking directories...')
    for directory in directories:
        if not os.path.exists(directory):
            print(f'\tCreating {directory}')
            os.mkdir(directory)
        else:
            print(f'\tFound {directory}')
    print('\tAll directories checked, continuing...', end='\n\n')

def strip_prefix(method_name: str, prefix: str = 'get_') -> str:
    """Removes a specific prefix from a method name if it exists."""
    return method_name[len(prefix):] if method_name.startswith(prefix) else method_name

def build_path(*segments: str) -> str:
    """Dynamically build and format file paths from given segments."""
    path = os.path.join(*segments)
    return path.replace("\\", "/") # Ensure correct slashes

def build_click_url(file_path: str) -> str:
    """Dynamically build clickable file URL."""
    return f"file:///{build_path(os.getcwd(), file_path)}"

# -- MAIN --

user_instance = user.User(get_username().lower())
current_directory = os.getcwd()

# Export directories
EXPORTS_DIR = build_path(current_directory, 'exports')
USERS_FOLDER = build_path(EXPORTS_DIR, 'users')
USER_FOLDER = build_path(USERS_FOLDER, user_instance.username)
directories = [EXPORTS_DIR, USERS_FOLDER, USER_FOLDER]
check_and_create_dirs(directories)

start_time = time.time()

# Save user instance data
user_data_path = build_path(USER_FOLDER, 'user')
save_data(user_data_path, user_instance.jsonify())

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
    save_data(file_path, data)

    print(f'{time.time() - method_start_time:<7.2f} seconds - {method_name:<22} - {build_click_url(file_path)}.json')

os.system('title Completed!')
print('\nProcessing complete!')
print(f'\tTotal time: {time.time() - start_time:.2f} seconds')

print('\tAt', build_click_url(USER_FOLDER), end='\n\n')
os.system('pause')