"""
Compare Watchlists - Can't decide what to watch?

Shows which films from your watchlist are also wanted by people you follow.
Watch it before they do! 

Generates:
- JSON data for analysis
- HTML report with Glassmorphism design for easy viewing

Exports saved to: exports/users/{username}/watchlist_comparison.*

Usage: python compare_watchlists.py --user <username> [--force]
"""

__title__ = "Watchlist Comparison"
__description__ = "Identify films from your watchlist that are also wanted by users you follow."
__version__ = "0.1.1"
__author__ = "fastfingertips"
__author_url__ = "https://github.com/fastfingertips"
__created_at__ = "2025-12-24"

import argparse
import os
import sys
import time
from collections import Counter
from datetime import datetime

from fastfingertips.terminal_utils import get_input
from jinja2 import Environment, FileSystemLoader
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn
)
from rich.table import Table
from rich.text import Text

# Add parent directory to path for local letterboxdpy

from letterboxdpy.pages.user_watchlist import UserWatchlist
from letterboxdpy.user import User
from letterboxdpy.utils.utils_directory import Directory
from letterboxdpy.utils.utils_file import JsonFile, build_path


class WatchlistHtmlRenderer:
    """Handles HTML report generation for watchlist comparison using Jinja2 templates."""

    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
    TEMPLATE_NAME = 'compare_watchlists.html'

    def __init__(self, username: str, my_films: dict, film_users: dict, user_totals: dict):
        self.username = username
        self.my_films = my_films
        self.film_users = film_users
        self.user_totals = user_totals

    def render(self, filepath: str, sorted_films: list, stats: dict) -> None:
        """Generates and saves the HTML report using Jinja2."""
        
        films_data, all_included_users = self._prepare_films_data(sorted_films)
        users_data = self._prepare_users_data()

        # Final stats
        generated_at = datetime.now().strftime('%Y-%m-%d %H:%M')

        # Load and render template
        try:
            env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIR))
            template = env.get_template(self.TEMPLATE_NAME)
        except Exception as e:
            print(f"\n[bold red]Error:[/bold red] Template loading failed: [yellow]{e}[/yellow]")
            sys.exit(1)

        html_content = template.render(
            username=self.username,
            stats=stats,
            all_users=list(all_included_users),
            results=films_data,
            user_rankings=users_data,
            generated_at=generated_at,
            metadata={
                'title': __title__,
                'description': __description__,
                'version': __version__,
                'author': __author__,
                'author_url': __author_url__,
                'created_at': __created_at__,
                'file_name': os.path.basename(__file__)
            }
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _get_film_info(self, film_id: str) -> dict:
        """Helper to get film details with fallbacks."""
        info = self.my_films.get(film_id, {})
        return {
            'url': info.get('url', f"https://letterboxd.com/film/{film_id}/"),
            'name': info.get('name', film_id),
            'year': info.get('year', '')
        }

    def _prepare_films_data(self, sorted_films: list) -> tuple:
        """Prepares the data structure for the 'Films' tab."""
        all_included_users = set()
        films_data = []
        
        for film_id, count in sorted_films:
            users = self.film_users[film_id]
            all_included_users.update(users)
            
            film_info = self._get_film_info(film_id)
            films_data.append({
                'users_csv': ",".join(users),
                'count': count,
                'url': film_info['url'],
                'name': film_info['name'],
                'year': film_info['year'],
                'users': users
            })
        return films_data, all_included_users

    def _prepare_users_data(self) -> list:
        """Prepares the data structure for the 'Users' tab."""
        user_matches = {} # {username: [film_ids]}
        for film_id, user_list in self.film_users.items():
            if film_id in self.my_films: 
                 for u in user_list:
                    user_matches.setdefault(u, []).append(film_id)
        
        sorted_user_list = sorted(user_matches.items(), key=lambda x: len(x[1]), reverse=True)
        
        users_data = []
        for user, fids in sorted_user_list:
            total_count = self.user_totals.get(user, 0)
            percentage = (len(fids) / total_count * 100) if total_count > 0 else 0
            
            shared_films = [self._get_film_info(fid) for fid in fids]

            users_data.append({
                'name': user,
                'url': f"https://letterboxd.com/{user}/",
                'matches_count': len(fids),
                'total_count': total_count,
                'percentage': f"{percentage:.1f}",
                'shared_films': shared_films
            })
        return users_data


class WatchlistComparator:
    """
    Compares the user's watchlist with the watchlists of users they follow.
    
    Identifies common films and ranks them by popularity (how many followed users want to watch them).
    Generates both JSON and detailed HTML reports.
    
    The HTML report includes:
    - Interactive filtering by user.
    - Two views: 'Films' (ranked by popularity) and 'Users' (ranked by shared films).
    - Modern, responsive design matching GitHub UI aesthetics.
    """
    EXPORTS_DIR = build_path(os.path.dirname(__file__), 'exports', 'users')
    
    STYLE_PRIMARY = "bold cyan"
    STYLE_SECONDARY = "bold yellow"
    STYLE_SUCCESS = "bold green"
    STYLE_CACHE = "dim cyan"
    PROGRESS_COLUMNS = [SpinnerColumn(), TextColumn("[progress.description]{task.description}")]

    def __init__(self, username: str, force_refresh: bool = False):
        self.username = username
        self.force_refresh = force_refresh
        self.my_films = {}
        self.my_film_ids = set()
        self.following = []
        self.film_popularity = Counter()
        self.film_users = {}
        self.user_total_counts = {}
        self.console = Console()
    
    def print_welcome(self):
        """Prints a welcome banner."""
        welcome_text = (
            f"[bold white]{__description__.split(' that ')[0]} for[/bold white] [bold cyan]@{self.username}[/bold cyan]\n"
            f"[dim]that {__description__.split(' that ')[1]}[/dim]"
        )
        self.console.print("\n")
        self.console.print(Panel(
            welcome_text,
            title=f"[bold white] {__title__} v{__version__} [/bold white]",
            border_style="blue",
            padding=(1, 2),
            expand=False
        ))
        self.console.print("\n")
    
    def fetch_user_watchlist(self) -> bool:
        """Fetches the target user's watchlist."""
        with Progress(
            *self.PROGRESS_COLUMNS,
            console=self.console,
            transient=True
        ) as progress:
            progress.add_task(description=f"[bold blue]Fetching[/bold blue] watchlist for [cyan]@{self.username}[/cyan]...", total=None)
            # use self.force_refresh to allow caching the user's own watchlist
            data, cache_info = self._get_watchlist(self.username, force_refresh=self.force_refresh)
            self.my_films = data.get('data', {})
            self.my_film_ids = set(self.my_films.keys())
        
        status_text = f"[bold green][OK][/bold green] Watchlist fetched: [white]{len(self.my_film_ids)}[/white] films"
        if cache_info:
            status_text += f" [dim](cached {cache_info})[/dim]"
        
        self.console.print(status_text)
        return bool(self.my_film_ids)
    
    def fetch_following(self):
        """Fetches the list of users followed by the main user."""
        with Progress(
            *self.PROGRESS_COLUMNS,
            console=self.console,
            transient=True
        ) as progress:
            progress.add_task(description=f"[bold blue]Fetching[/bold blue] following list for [cyan]@{self.username}[/cyan]...", total=None)
            user = User(self.username)
            self.following = list(user.get_following().keys())
        
        self.console.print(f"[bold green][OK][/bold green] Following fetched: [white]{len(self.following)}[/white] users")
    
    def analyze_watchlists(self):
        """Iterates through followed users to find common films in their watchlists."""
        self.console.print(f"\n[bold white]Analyzing {len(self.following)} watchlists for[/bold white] [bold cyan]@{self.username}[/bold cyan]:")
        
        total_following = len(self.following)
        idx_width = len(str(total_following))
        
        with Progress(
            *self.PROGRESS_COLUMNS,
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("[dim]Initializing...", total=total_following)
            
            for i, user in enumerate(self.following, 1):
                self._process_single_user(progress, task, user, i, total_following, idx_width)
                progress.advance(task)
            
            progress.update(task, description="[bold green]All users processed[/bold green]")

    def _process_single_user(self, progress, task, user, index, total, idx_width):
        """Analyzes a single user's watchlist and prints the result with perfect alignment."""
        progress.update(task, description=f"Processing [{self.STYLE_SECONDARY}]@{user}[/{self.STYLE_SECONDARY}]")
        start_time = time.time()
        
        their_ids, cache_info = self._get_film_ids(user)
        common = self.my_film_ids & their_ids
        duration = time.time() - start_time
        
        # 1. Prefix Column: [ 1/28] username (Fixed width: 2 + 1 + idx_width + 1 + idx_width + 2 + 20 + 1 = ~35 chars)
        prefix_markup = f"  [{index:>{idx_width}}/{total}] [bold]{user:<20}[/bold] "
        line_item = Text.from_markup(prefix_markup)
        
        # 2. Stats Column: common/total (perc%) or private (Fixed width: 26 chars)
        if their_ids:
            shared_count = len(common)
            total_count = len(their_ids)
            self.user_total_counts[user] = total_count
            percentage = (shared_count / total_count) * 100 if total_count > 0 else 0
            
            # Format: "   0/1234  common (  0.0%)" -> Total 26 chars
            stats_str = f"{shared_count:>4}/{total_count:<5} common ({percentage:>5.1f}%)"
            stats_color = self.STYLE_SUCCESS if common else "dim"
            
            for film_id in common:
                self.film_popularity[film_id] += 1
                self.film_users.setdefault(film_id, []).append(user)
        else:
            # Align "private" exactly to the end of the 26-char column
            stats_str = "private".rjust(26)
            stats_color = "red"
            
        line_item.append(stats_str, style=stats_color)
        
        # 3. Time Column: [ 0.0s] (Fixed width: 10 chars)
        line_item.append(f"   [{duration:>4.1f}s]", style="dim")
        
        # 4. Cache Info (Optional)
        if cache_info:
            line_item.append(f" [cache: {cache_info}]", style=self.STYLE_CACHE)
            
        progress.console.print(line_item)
    
    def display_recommendations(self):
        """Displays the top recommendations in the terminal."""
        if not self.film_popularity:
            self.console.print("\n[bold red]No common films found.[/bold red]")
            return

        table = Table(
            title=f"\n[{self.STYLE_PRIMARY}]Top Recommendations[/{self.STYLE_PRIMARY}]",
            title_style=self.STYLE_PRIMARY,
            box=box.HORIZONTALS,
            header_style="bold magenta",
            show_footer=True,
            border_style="dim"
        )
        
        table.add_column("#", style="dim", width=4)
        table.add_column("Matches", justify="center", footer=Text(f"{len(self.film_popularity)} films", style=self.STYLE_PRIMARY))
        table.add_column("Film Title", style=self.STYLE_SUCCESS)
        table.add_column("Wanted by")

        for i, (film_id, count) in enumerate(self.film_popularity.most_common(20), 1):
            users_list = self.film_users[film_id]
            users_display = ", ".join(users_list[:3])
            if len(users_list) > 3:
                users_display += f" [dim]+{len(users_list) - 3}[/dim]"
            
            table.add_row(str(i), str(count), self._format_film_title(film_id), users_display)

        self.console.print(table)

    def _format_film_title(self, film_id: str) -> str:
        """Helper to format film title with year for terminal display."""
        info = self.my_films.get(film_id, {})
        name = info.get('name', film_id)
        year = info.get('year', '')
        return f"{name} ({year})" if year else name

    def save_results(self):
        """
        Saves the comparison results to JSON and HTML files.
        """
        if not self.film_popularity:
            return
        
        # Prepare data
        sorted_films = self.film_popularity.most_common()
        
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
                for fid, cnt in sorted_films
            }
        }
        
        # Save JSON
        base_path = build_path(self._user_dir(self.username), 'watchlist_comparison')
        JsonFile.save(base_path, result)
        
        # Save HTML
        renderer = WatchlistHtmlRenderer(self.username, self.my_films, self.film_users, self.user_total_counts)
        stats = {
            'watchlist': len(self.my_film_ids),
            'following': len(self.following),
            'matches': len(self.film_popularity)
        }
        renderer.render(base_path + '.html', sorted_films, stats)
        
        # FINAL SUMMARY PANEL
        summary_grid = Table.grid(expand=True)
        summary_grid.add_column(style="cyan", justify="right", width=20)
        summary_grid.add_column(style="white")
        
        summary_grid.add_row("Common Films Found:", f" [bold green]{len(self.film_popularity)}[/bold green]")
        summary_grid.add_row("Scanned Users:", f" [bold yellow]{len(self.following)}[/bold yellow]")
        summary_grid.add_row("JSON Export:", f" [dim]{base_path}.json[/dim]")
        summary_grid.add_row("HTML Report:", f" [bold blue]{base_path}.html[/bold blue]")
        
        self.console.print("\n")
        self.console.print(Panel(
            summary_grid,
            title="[bold green] ANALYSIS COMPLETE [/bold green]",
            subtitle=f"[dim]letterboxdpy · {__title__.lower()}[/dim]",
            border_style="green",
            padding=(1, 2),
            expand=False
        ))
        self.console.print("\n")
    
    # Helpers
    def _user_dir(self, username: str) -> str:
        path = build_path(self.EXPORTS_DIR, username)
        Directory.create(path, silent=True)
        return path
    
    def _get_watchlist(self, username: str, force_refresh: bool = False) -> tuple:
        filepath = build_path(self._user_dir(username), 'watchlist')
        
        if not force_refresh and JsonFile.exists(filepath):
            cached = JsonFile.load(filepath)
            if cached:
                full_path = JsonFile._get_path(filepath)
                mtime = os.path.getmtime(full_path)
                age = time.time() - mtime
                return cached, self._format_age(age)
        
        try:
            data = UserWatchlist(username).get_watchlist()
            JsonFile.save(filepath, data)
            return data, None
        except Exception:
            return {'data': {}}, None
    
    def _format_age(self, seconds: float) -> str:
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m ago"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}h ago"
        else:
            return f"{int(seconds // 86400)}d ago"
    
    def _get_film_ids(self, username: str) -> tuple:
        data, cache_info = self._get_watchlist(username, self.force_refresh)
        return set(data.get('data', {}).keys()), cache_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare watchlists and generate interactive HTML report with filters")
    parser.add_argument('--user', '-u', help="Letterboxd username")
    parser.add_argument('--force', '-f', action='store_true', help="Force refresh cached data")
    args = parser.parse_args()

    username = args.user if args.user else get_input("Enter username: ", index=1)
    
    comparator = WatchlistComparator(username, args.force)
    
    # Visual workflow exposed in main
    comparator.print_welcome()
    
    if not comparator.fetch_user_watchlist():
        comparator.console.print("[bold red]Error:[/bold red] User's watchlist is empty or private.")
        sys.exit(1)
        
    comparator.fetch_following()
    comparator.analyze_watchlists()
    comparator.display_recommendations()
    comparator.save_results()
