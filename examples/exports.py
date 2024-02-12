import os
import sys
import json
import time
sys.path.append("../")
from letterboxdpy import user

username = ''

if not len(username):
    try:
        username = sys.argv[1]
    except IndexError:
        print(f'Quick usage: python {sys.argv[0]} <username>')
        username = input('Enter username: ')

user_instance = user.User(username.lower())

# Export directories
EXPORTS_DIR = 'exports'
USERS_FOLDER = os.path.join(EXPORTS_DIR, 'users')
USER_FOLDER = os.path.join(USERS_FOLDER, user_instance.username)

# Export methods
# If you want to add a new method, add it here
methods = [
    user.user_films,
    user.user_following,
    user.user_followers,
    user.user_genre_info,
    user.user_reviews,
    user.user_diary,
    user.user_wrapped,
    user.user_activity,
    user.user_lists,
    [user.user_watchlist, {'filters': {'genre': ['action', '-drama']}}],
    user.user_tags
]

print('\nChecking directories...')
for dir in [EXPORTS_DIR, USERS_FOLDER, USER_FOLDER]:
    if not os.path.exists(dir):
        print(f'\tCreating {dir}')
        os.mkdir(dir)
    else:
        print(f'\tFound {dir}')
else:
    print('All directories checked, continuing...', end='\n\n')

total_time = time.time()
methods_str_length = len(str(len(methods)))
for no, method in enumerate(methods, 1):
    method_start_time = time.time()

    args = {}
    if isinstance(method, list):
        method, args = method

    os.system(f'title [{len(methods)}/{no:0>{methods_str_length}}] Exporting {method.__name__}...')
    print(f'[{len(methods)}/{no:0>{methods_str_length}}]: Processing "{method.__name__}" method',
          end=f' with args: {args}...\r' if args else '...\r')

    data = method(user_instance, **args) if args else method(user_instance)

    file_path = os.path.join(USER_FOLDER, f'{method.__name__}.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

    # Clickable path
    click_url = f"file:///{os.path.join(os.getcwd(), file_path)}".replace("\\", "/")
    print(f'{time.time() - method_start_time:<7.2f} seconds - {method.__name__:<16} - {click_url}')

# Finish
os.system('title Completed!')
print('\nProcessing complete!')
print(f'\tTotal time: {time.time() - total_time:.2f} seconds')
# Clickable path
click_url = f'file:///{os.path.join(os.getcwd(), USER_FOLDER)}'.replace("\\", "/")
print('\tAt', click_url, end='\n\n')
os.system('pause') # for title