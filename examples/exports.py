import os
import sys
import json
sys.path.append("../")
from letterboxdpy import user

nick = user.User("nmcassa")

methods = [
    user.user_films,
    user.user_following,
    user.user_followers,
    user.user_genre_info,
    user.user_reviews,
    user.user_diary,
    user.user_wrapped
]

exports_dir = 'exports'

for method in methods:
    data = method(nick)
    file_path = os.path.join(exports_dir, f'{method.__name__}.json')

    if not os.path.exists(exports_dir):
        print('Creating exports directory..')
        os.mkdir(exports_dir)
        
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f'Exported {file_path}')

print('Processing complete!')
print(f'At {os.path.join(os.getcwd(), exports_dir)}')