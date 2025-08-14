import sys
from json import dumps as json_dumps

from letterboxdpy import user
from letterboxdpy.utils.utils_terminal import get_input, args_exists

class FollowStatsAnalyzer:
    """Analyze follow statistics for Letterboxd users."""
    
    def __init__(self, username: str):
        self.username = username
        self.user_instance = user.User(username)
    
    def analyze(self) -> dict:
        """Analyze follow statistics for the user."""
        followers = self.user_instance.get_followers()
        following = self.user_instance.get_following()
        return self._calculate_stats(following, followers)
    
    def _calculate_stats(self, following: dict, followers: dict) -> dict:
        """Calculate follow statistics from followers and following data."""
        following_set = set(following.keys())
        followers_set = set(followers.keys())
        
        return {
            'not_followback': list(following_set - followers_set),
            'followback': list(following_set & followers_set),
            'fans': list(followers_set - following_set)
        }

if __name__ == "__main__":
    if not args_exists():
        print(f'Quick usage: python {sys.argv[0]} <username>')

    username = get_input("Enter username: ", index=1)
    analyzer = FollowStatsAnalyzer(username)
    stats = analyzer.analyze()
    print(json_dumps(stats, indent=4))