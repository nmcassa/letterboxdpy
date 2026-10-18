"""
Network Balance

Analyzes the followers/following ratio of users in your network
to produce a "follower share" — a percentage indicating how many
of their connections are followers vs. following.

Generates:
- JSON data for further analysis
- HTML report with interactive table and score bars

Exports saved to: exports/users/{username}/network_balance.*

Usage: python network_balance.py [username] [--force]
"""

__title__ = "Network Balance"
__description__ = (
    "Analyze follower/following ratios and mutual relationships in your network."
)
__version__ = "0.1.1"
__author__ = "fastfingertips"
__author_url__ = "https://github.com/fastfingertips"
__created_at__ = "2026-05-10"

import argparse
import json
import os
import sys
import time
from datetime import datetime

from fastfingertips.terminal_utils import get_input
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.text import Text

from letterboxdpy.user import User

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")
EXPORTS_DIR = os.path.join(SCRIPT_DIR, "exports")


# ── Helpers ────────────────────────────────────────────────────────────────────


def _follower_share(followers: int, following: int) -> float:
    """Followers / (Followers + Following) * 100, or 0 if both are zero."""
    total = followers + following
    return round(followers / total * 100, 2) if total > 0 else 0.0


def analyze_list(
    username_list: list[str],
    list_name: str,
    *,
    progress: Progress,
    overall_task,
) -> list[dict]:
    """Fetch stats for each user and compute their follower share."""
    results = []
    if not username_list:
        return results

    task = progress.add_task(list_name, total=len(username_list), current="")

    for i, username in enumerate(username_list):
        progress.update(task, current=f"@{username:<20}")
        try:
            u = User(username)
            f_count = u.stats.get("followers", 0)
            fing_count = u.stats.get("following", 0)
            score = _follower_share(f_count, fing_count)

            results.append(
                {
                    "user": username,
                    "follow_order": len(username_list) - i,
                    "follower_share_percentage": f"{score:.1f}%",
                    "follower_share": score,
                    "stats": f"{f_count} F / {fing_count} Fing",
                }
            )

            if (i + 1) % 15 == 0:
                time.sleep(2)

        except Exception:
            pass  # silently skip; overall still advances

        progress.advance(task)
        progress.advance(overall_task)

    progress.update(task, current="")
    results.sort(key=lambda x: x["follower_share"], reverse=True)
    for rank, entry in enumerate(results, 1):
        entry["network_rank"] = rank
    return results


# ── HTML Export ────────────────────────────────────────────────────────────────


def save_html_report(report: dict, output_path: str) -> None:
    """Render the Jinja2 template and write the HTML file."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True,
    )
    template = env.get_template("network_balance.html")

    metadata = {
        "title": __title__,
        "description": __description__,
        "version": __version__,
        "author": __author__,
        "author_url": __author_url__,
        "created_at": __created_at__,
        "file_name": os.path.basename(__file__),
    }

    html = template.render(
        username=report["target"],
        summary=report["summary"],
        followers_analysis=report["followers_analysis"],
        following_analysis=report["following_analysis"],
        generated_at=report["timestamp"],
        metadata=metadata,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# ── Core ───────────────────────────────────────────────────────────────────────


def run_full_audit(
    target_user: str,
    force: bool = False,
    console: Console | None = None,
    open_browser: bool = False,
) -> None:
    console = console or Console()

    # ── Welcome banner ──
    console.print()
    console.print(
        Panel(
            Text.assemble(
                ("Compare follower/following balance and mutual status\n", ""),
                ("in your follower/following network for ", ""),
                (f"@{target_user}", "bold cyan"),
                (".", ""),
            ),
            title=f"[bold white] {__title__} v{__version__} [/bold white]",
            border_style="bright_black",
            padding=(1, 4),
        )
    )
    console.print()

    # ── Export paths ──
    user_export_dir = os.path.join(EXPORTS_DIR, "users", target_user)
    os.makedirs(user_export_dir, exist_ok=True)
    json_path = os.path.join(user_export_dir, "network_balance.json")
    html_path = os.path.join(user_export_dir, "network_balance.html")

    # ── Load or fetch ──
    if not force and os.path.exists(json_path):
        with open(json_path, encoding="utf-8") as f:
            report = json.load(f)
        console.print(f"[green][OK][/green] Loaded cached report for @{target_user}")
    else:
        try:
            main = User(target_user)
        except Exception as e:
            console.print(
                f"[bold red]Error:[/bold red] Could not fetch user @{target_user}: {e}"
            )
            sys.exit(1)

        console.print("[dim]Fetching followers…[/dim]")
        followers_list = list(main.get_followers().keys())
        console.print("[dim]Fetching following…[/dim]")
        following_list = list(main.get_following().keys())

        console.print()
        total_users = len(followers_list) + len(following_list)
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.description}[/bold]"),
            BarColumn(),
            MofNCompleteColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            TextColumn("[dim cyan]{task.fields[current]}[/dim cyan]"),
            console=console,
        ) as progress:
            overall_task = progress.add_task(
                "[dim]Overall[/dim]",
                total=total_users,
                current="",
            )
            followers_analysis = analyze_list(
                followers_list,
                "[1/2] Followers",
                progress=progress,
                overall_task=overall_task,
            )
            following_analysis = analyze_list(
                following_list,
                "[2/2] Following",
                progress=progress,
                overall_task=overall_task,
            )
        console.print()

        # Calculate mutual follow status
        followers_set = set(followers_list)
        following_set = set(following_list)
        for item in followers_analysis:
            item["mutual"] = item["user"] in following_set
        for item in following_analysis:
            item["mutual"] = item["user"] in followers_set

        report = {
            "target": target_user,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_followers": len(followers_list),
                "total_following": len(following_list),
                "mutual_count": len(followers_set & following_set),
            },
            "followers_analysis": followers_analysis,
            "following_analysis": following_analysis,
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        console.print(f"[green][OK][/green] JSON saved: {json_path}")

    # ── HTML report ──
    save_html_report(report, html_path)
    console.print(f"[green][OK][/green] HTML report: {html_path}")

    if open_browser:
        import webbrowser

        html_url = os.path.abspath(html_path)
        webbrowser.open(f"file:///{html_url.replace(os.sep, '/')}")

    # ── Summary ──
    console.print()
    top_n = report["followers_analysis"][:5]
    if top_n:
        from rich.table import Table

        table = Table(
            title="Top 5 Followers by Follower Share",
            border_style="bright_black",
            header_style="bold dim",
            show_lines=False,
            padding=(0, 1),
        )
        table.add_column("#", style="dim", width=4, justify="right")
        table.add_column("User", style="bold cyan")
        table.add_column("Score", justify="right")
        table.add_column("Stats", style="dim")

        for i, entry in enumerate(top_n, 1):
            score = entry["follower_share"]
            color = "green" if score >= 60 else ("yellow" if score >= 40 else "red")
            table.add_row(
                str(i),
                f"@{entry['user']}",
                f"[{color}]{entry['follower_share_percentage']}[/{color}]",
                entry["stats"],
            )
        console.print(table)
    console.print()


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze follower/following balance and mutual relationships"
    )
    parser.add_argument("username", nargs="?", help="Letterboxd username (positional)")
    parser.add_argument("--user", "-u", help="Letterboxd username (named)")
    parser.add_argument(
        "--force", "-f", action="store_true", help="Force refresh cached data"
    )
    parser.add_argument(
        "--open",
        "-o",
        action="store_true",
        help="Automatically open the HTML report in your browser when done",
    )
    args = parser.parse_args()

    username = args.user or args.username or get_input("Enter username: ")
    run_full_audit(username, force=args.force, open_browser=args.open)
