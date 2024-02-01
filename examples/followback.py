import sys
import json
sys.path.append("../")
from letterboxdpy import user

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

nick = user.User("Aade")

data = follow_stats(
  user.user_followers(nick),
  user.user_following(nick)
)

print(json.dumps(data, indent=4))