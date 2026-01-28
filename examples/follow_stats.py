"""
Letterboxd Follow Statistics Analyzer

Analyzes follow relationships (followers/following) and identifies:
- Mutual follows (Friends)
- Fans (They follow you, you don't follow back)
- Not Following Back (You follow them, they don't follow back)

Generates interactive HTML report and JSON data.
"""

__title__ = "Follow Statistics"
__description__ = "Analyze follow relationships (followers/following) to identify mutuals, fans, and unrequited follows."
__version__ = "0.1.1"
__author__ = "fastfingertips"
__author_url__ = "https://github.com/fastfingertips"
__created_at__ = "2024-09-06"

import argparse
import os
from datetime import datetime
from json import dumps as json_dumps

from fastfingertips.terminal_utils import get_input
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from letterboxdpy import user
from letterboxdpy.utils.utils_directory import Directory
from letterboxdpy.utils.utils_file import build_path


class FollowStatsHtmlRenderer:
    """Handles HTML report generation for follow statistics using external Jinja2 templates."""
    
    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
    TEMPLATE_NAME = 'follow_stats.html'

    def __init__(self, username):
        self.username = username

    def _calculate_ratio_info(self, section_id, count, stats):
        total_following = len(stats['details']['all_following'])
        total_followers = len(stats['details']['all_followers'])
        
        if section_id in ['mutual', 'notback']:
            pct = round(count / total_following * 100, 1) if total_following else 0
            return f"<strong>{pct}%</strong> of Following"
        elif section_id == 'fans':
            pct = round(count / total_followers * 100, 1) if total_followers else 0
            return f"<strong>{pct}%</strong> of Followers"
        return ""


    def render(self, filepath, stats):
        try:
            env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIR))
            template = env.get_template(self.TEMPLATE_NAME)
        except Exception as e:
            print(f"Error loading template: {e}")
            return

        sections = [
            {'id': 'mutual', 'title': 'Mutual Follows', 'data': stats['details']['followback']},
            {'id': 'fans', 'title': 'Fans (Reviewers)', 'data': stats['details']['fans']},
            {'id': 'notback', 'title': 'Not Following Back', 'data': stats['details']['not_followback']},
            {'id': 'all_following', 'title': 'Following', 'data': stats['details']['all_following']},
            {'id': 'all_followers', 'title': 'Followers', 'data': stats['details']['all_followers']}
        ]
        
        for section in sections:
            section['ratio_label'] = self._calculate_ratio_info(section['id'], len(section['data']), stats)

        generated_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        rendered_html = template.render(
            username=self.username,
            stats=stats,
            sections=sections,
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
            f.write(rendered_html)
            
            
class FollowStatsAnalyzer:
    """Analyze follow statistics for Letterboxd users."""
    
    EXPORTS_DIR = build_path(os.path.dirname(__file__), 'exports', 'users')
    
    def __init__(self, username: str):
        self.username = username
        self.console = Console()
        self.user_instance = user.User(username)
        
        # Setup directories
        self.user_dir = build_path(self.EXPORTS_DIR, self.username)
        Directory.create(self.user_dir)

    def print_welcome(self):
        """Prints a welcome banner."""
        welcome_text = (
            f"[bold white]{__description__.split(' to ')[0]} for[/bold white] [bold cyan]@{self.username}[/bold cyan]\n"
            f"[dim]{__description__.split(' to ')[1] if ' to ' in __description__ else __description__}[/dim]"
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

    def analyze(self):
        """Analyze follow statistics for the user."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            progress.add_task(description=f"[bold blue]Fetching[/bold blue] followers and following for [cyan]@{self.username}[/cyan]...", total=None)
            followers = self.user_instance.get_followers()
            following = self.user_instance.get_following()
        
        self.console.print(f"[bold green][OK][/bold green] Data fetched successfully: [white]{len(followers)}[/white] followers, [white]{len(following)}[/white] following")
        
        stats = self._calculate_stats(following, followers)
        self._save(stats)
        return stats
    
    def _calculate_stats(self, following: dict, followers: dict) -> dict:
        """Calculate follow statistics preserving original order."""
        following_list = list(following.keys())
        followers_list = list(followers.keys())
        
        following_set = set(following_list)
        followers_set = set(followers_list)
        
        # Lists preserving order
        not_followback = [u for u in following_list if u not in followers_set]
        followback = [u for u in following_list if u in followers_set]
        fans = [u for u in followers_list if u not in following_set]
        
        return {
            'summary': {
                'total_following': len(following_list),
                'total_followers': len(followers_list),
                'mutual_follows': len(followback),
                'not_followback_count': len(not_followback),
                'fans_count': len(fans),
                'followback_ratio': round(len(followback) / len(following_list) * 100, 2) if following_list else 0
            },
            'details': {
                'not_followback': not_followback,
                'followback': followback,
                'fans': fans,
                'all_following': following_list,
                'all_followers': followers_list
            }
        }

    def _save(self, stats: dict):
        # Save JSON
        json_path = os.path.join(self.user_dir, 'follow_stats.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json_dumps(stats, indent=4))
        
        # Save HTML
        html_path = os.path.join(self.user_dir, 'follow_stats.html')
        renderer = FollowStatsHtmlRenderer(self.username)
        renderer.render(html_path, stats)

        # FINAL SUMMARY PANEL
        summary_grid = Table.grid(expand=True)
        summary_grid.add_column(style="cyan", justify="right", width=20)
        summary_grid.add_column(style="white")
        
        summary_grid.add_row("Mutual Follows:", f" [bold green]{stats['summary']['mutual_follows']}[/bold green]")
        summary_grid.add_row("Fans (Reviewers):", f" [bold yellow]{stats['summary']['fans_count']}[/bold yellow]")
        summary_grid.add_row("Not Following Back:", f" [bold red]{stats['summary']['not_followback_count']}[/bold red]")
        summary_grid.add_row("Success Rate:", f" [bold blue]{stats['summary']['followback_ratio']}%[/bold blue]")
        summary_grid.add_row("JSON Export:", f" [dim]{json_path}[/dim]")
        summary_grid.add_row("HTML Report:", f" [bold blue]{html_path}[/bold blue]")
        
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

if __name__ == "__main__":
    # 1. Parse command line arguments
    parser = argparse.ArgumentParser(description="Analyze follow stats and generate interactive HTML report")
    parser.add_argument("--user", "-u", help="Letterboxd username")
    args = parser.parse_args()

    # Identfy target user
    username = args.user if args.user else get_input("Enter username: ", index=1)
        
    # Run analysis
    analyzer = FollowStatsAnalyzer(username)
    analyzer.print_welcome()
    analyzer.analyze()
