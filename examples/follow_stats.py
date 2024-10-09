import sys
import os
from json import dumps as json_dumps

try:
    from letterboxdpy import user
    from letterboxdpy.utils.utils_terminal import get_input, args_exists
except ImportError:
    try:
        sys.path.append(os.path.join(sys.path[0], '..'))
        from letterboxdpy import user
        from letterboxdpy.utils.utils_terminal import get_input, args_exists
    except (ImportError, ValueError) as e:
        raise ImportError(f"Error importing 'letterboxdpy': {e}. Please install the package.") from e

def analyze_follow_stats(username: str) -> dict:
    """Analyze follow statistics for a given username."""
    
    def calculate_stats(following: dict, followers: dict) -> dict:
        """Calculate follow statistics from followers and following data."""
        following_set = set(following.keys())
        followers_set = set(followers.keys())

        return {
            'not_followback': list(following_set - followers_set),
            'followback': list(following_set & followers_set),
            'fans': list(followers_set - following_set)
        }

    username = username.lower()
    user_instance = user.User(username)
    followers = user_instance.get_followers()
    following = user_instance.get_following()

    return calculate_stats(following, followers)

if __name__ == "__main__":
    if not args_exists():
        print(f'Quick usage: python {sys.argv[0]} <username>')

    username = get_input("Enter username: ", index=1)
    stats = analyze_follow_stats(username)
    print(json_dumps(stats, indent=4))