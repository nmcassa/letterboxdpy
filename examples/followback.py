from json import dumps as json_dumps

try:
    from letterboxdpy import user # package is installed
except ImportError: # not installed
    import sys
    try:
        sys.path.append(sys.path[0] + '/..')
        from letterboxdpy import user # use local copy
    except (ImportError, ValueError):
        import os
        print("letterboxdpy not installed, would you like to install it?")
        response = input("y/n: ").lower()
        if response == "y":
            os.system("pip install letterboxdpy --force")
            print("Installation complete, running script again...")
            sys.exit(0)
        print("Exiting...")
        sys.exit(1)

# -- FUNCTIONS --

def follow_stats(following_data, followers_data):
  not_followback = []
  followback = []
  fans = []

  following = list(following_data.keys())
  followers = list(followers_data.keys())

  for uname in following:
    if uname in followers:
      followback.append(uname)
    else:
      not_followback.append(uname)

  for uname in followers:
    if uname not in following:
      fans.append(uname)

  data = {
    'not_followback': not_followback,
    'followback': followback,
    'fans': fans
  }
  return data

def get_username(username: str='') -> str:
  if not len(username):
      try:
          username = sys.argv[1]
      except IndexError:
          print(f'Quick usage: python {sys.argv[0]} <username>')
          username = input('Enter username: ')
  return username

# -- MAIN --

user_instance = user.User(get_username().lower())

data = follow_stats(
  user.user_followers(user_instance),
  user.user_following(user_instance)
)

print(json_dumps(data, indent=4))