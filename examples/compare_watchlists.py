"""
Compare Watchlists - Can't decide what to watch?

Shows which films from your watchlist are also wanted by people you follow.
Watch it before they do! Exports saved to: exports/users/{username}/

Usage: python compare_watchlists.py --user <username> [--refresh]
"""

import argparse
import os
import sys
from collections import Counter
from datetime import datetime

sys.path.insert(0, sys.path[0] + '/..')

from letterboxdpy.user import User
from letterboxdpy.pages.user_watchlist import UserWatchlist
from letterboxdpy.utils.utils_file import JsonFile, build_path
from letterboxdpy.utils.utils_directory import Directory


class WatchlistComparator:
    EXPORTS_DIR = build_path(os.path.dirname(__file__), 'exports', 'users')
    
    def __init__(self, username: str, force_refresh: bool = False):
        self.username = username
        self.force_refresh = force_refresh
        self.my_films = {}
        self.my_film_ids = set()
        self.following = []
        self.film_popularity = Counter()
        self.film_users = {}
    
    def run(self):
        print(f"\n{'='*60}")
        print(f"Watchlist Comparison for: {self.username}")
        print(f"{'='*60}\n")
        
        if not self._fetch_my_watchlist():
            print("User's watchlist is empty or private.")
            return
        
        self._fetch_following()
        self._analyze()
        self._display()
        self._save()
    
    def _fetch_my_watchlist(self) -> bool:
        print(f"Fetching {self.username}'s watchlist...")
        data = self._get_watchlist(self.username, force_refresh=True)
        self.my_films = data.get('data', {})
        self.my_film_ids = set(self.my_films.keys())
        print(f"  {len(self.my_film_ids)} films\n")
        return bool(self.my_film_ids)
    
    def _fetch_following(self):
        print("Fetching following list...")
        user = User(self.username)
        self.following = list(user.get_following().keys())
        print(f"  {len(self.following)} users\n")
    
    def _analyze(self):
        print("Analyzing...\n")
        
        for i, user in enumerate(self.following, 1):
            print(f"  [{i}/{len(self.following)}] {user}...", end=" ")
            
            their_ids = self._get_film_ids(user)
            common = self.my_film_ids & their_ids
            
            if common:
                print(f"{len(common)} common")
                for film_id in common:
                    self.film_popularity[film_id] += 1
                    self.film_users.setdefault(film_id, []).append(user)
            else:
                print("no common" if their_ids else "private")
    
    def _display(self):
        print(f"\n{'='*60}")
        print("RESULTS")
        print(f"{'='*60}\n")
        
        if not self.film_popularity:
            print("No common films found.")
            return
        
        for film_id, count in self.film_popularity.most_common(20):
            info = self.my_films.get(film_id, {})
            name = info.get('name', film_id)
            year = info.get('year', '')
            users = ", ".join(self.film_users[film_id][:3])
            if len(self.film_users[film_id]) > 3:
                users += f" +{len(self.film_users[film_id]) - 3}"
            
            print(f"  {count:2d}x | {name} ({year})" if year else f"  {count:2d}x | {name}")
            print(f"       by: {users}\n")
    
    def _save(self):
        if not self.film_popularity:
            return
        
        result = {
            'generated_at': datetime.now().isoformat(),
            'user': self.username,
            'watchlist_count': len(self.my_film_ids),
            'common_films_count': len(self.film_popularity),
            'films': {
                fid: {
                    'name': self.my_films.get(fid, {}).get('name', ''),
                    'count': cnt,
                    'users': self.film_users[fid]
                }
                for fid, cnt in self.film_popularity.items()
            }
        }
        
        filepath = build_path(self._user_dir(self.username), 'watchlist_comparison')
        JsonFile.save(filepath, result)
        
        print(f"{'='*60}")
        print(f"  {len(self.film_popularity)} common films")
        print(f"  Saved to: {filepath}.json")
        print(f"{'='*60}\n")
    
    # Helpers
    def _user_dir(self, username: str) -> str:
        path = build_path(self.EXPORTS_DIR, username)
        Directory.create(path, silent=True)
        return path
    
    def _get_watchlist(self, username: str, force_refresh: bool = False) -> dict:
        filepath = build_path(self._user_dir(username), 'watchlist')
        
        if not force_refresh:
            cached = JsonFile.load(filepath)
            if cached:
                return cached
        
        try:
            data = UserWatchlist(username).get_watchlist()
            JsonFile.save(filepath, data)
            return data
        except Exception:
            return {'data': {}}
    
    def _get_film_ids(self, username: str) -> set:
        data = self._get_watchlist(username, self.force_refresh)
        return set(data.get('data', {}).keys())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare watchlists")
    parser.add_argument('--user', '-u', required=True)
    parser.add_argument('--refresh', '-r', action='store_true')
    args = parser.parse_args()
    
    WatchlistComparator(args.user, args.refresh).run()

