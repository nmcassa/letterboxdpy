"""
Letterboxd Ratings Histogram

Recreates the ratings distribution section of a Letterboxd profile with a clean, professional layout.
- Half-star tick labels (½, ★, ★½, …, ★★★★★)
- Shows username, total ratings, average, and most given rating
- Letterboxd-inspired color scheme
"""

import argparse
import sys
import math
import matplotlib.pyplot as plt
import numpy as np

from letterboxdpy.user import User
from fastfingertips.terminal_utils import get_input
from fastfingertips.string_utils import is_whitespace_or_empty
from letterboxdpy.constants.project import Colors


class LetterboxdRatingPlotter:
    def __init__(self, username=None):
        self.username = username

    def _get_star_labels(self):
        positions = np.arange(0.5, 5.5, 0.5)
        labels = []
        for r in positions:
            if math.isclose(r, 0.5):
                labels.append("½★")
            elif math.isclose(r % 1, 0.5):
                labels.append("★" * int(r) + "½")
            else:
                labels.append("★" * int(r))
        return positions, labels

    def _draw_header_and_stats(self, axis, stats_axis, total_count: int, average: float, most_given: float) -> None:
        if not self.username:
            return

        axis.text(0.02, 0.98, "R A T I N G S", transform=axis.transAxes,
                  fontsize=12, color=Colors.TEXT, weight='bold', va='top', family='monospace')
        axis.text(0.98, 0.98, f"{total_count:,}", transform=axis.transAxes,
                  fontsize=12, color=Colors.TEXT, weight='bold', va='top', ha='right')
        axis.text(0.02, 0.92, f"@{self.username}", transform=axis.transAxes,
                  fontsize=11, color='white', weight='bold', va='top')
        
        stats_text = f"Average: {average}★  •  Total: {total_count:,}  •  Most Given: {most_given}★"
        stats_axis.text(0.5, 0.5, stats_text,
                        ha='center', va='center', fontsize=11, color=Colors.TEXT, weight='bold')

    def _label_bars(self, axis, bars_, counts_) -> None:
        if len(counts_) == 0:
            return
        max_count = max(counts_)
        for bar, count in zip(bars_, counts_):
            if count == max_count:
                bar.set_color(Colors.GREEN)
                bar.set_alpha(1.0)
            if count > 0:
                axis.text(bar.get_x() + bar.get_width() / 2, count + max_count * 0.01,
                          str(int(count)), ha="center", va="bottom", fontsize=8,
                          color=Colors.TEXT, alpha=0.9)

    def _style_axes(self, axis, max_count) -> None:
        axis.set_xlim(0.25, 5.25)
        axis.set_ylim(0, max_count * 1.12 if max_count else 1)
        
        tick_positions, tick_labels = self._get_star_labels()
        axis.set_xticks(tick_positions)
        axis.set_xticklabels(tick_labels, fontsize=9, color=Colors.TEXT)
        axis.set_yticks([])
        
        for spine in axis.spines.values():
            spine.set_visible(False)
        axis.grid(True, axis='y', alpha=0.1, color=Colors.TEXT, linestyle='-')

    def create_plot(self, ratings: dict):
        """Create Letterboxd-style rating distribution plot with enhancements"""
        rating_positions = np.arange(0.5, 5.5, 0.5)
        rating_counts = np.array([ratings.get(rating, 0) for rating in rating_positions])
        total_ratings = int(rating_counts.sum())
        
        if total_ratings > 0:
            avg_calc = (rating_positions * rating_counts).sum() / total_ratings
            average_rating = round(float(avg_calc), 2)
            most_given_rating = float(rating_positions[rating_counts.argmax()])
        else:
            average_rating = 0.0
            most_given_rating = 0.0

        # Create Letterboxd-style plot
        fig, (ax, ax_stats) = plt.subplots(
            2, 1,
            figsize=(12, 8),
            gridspec_kw={"height_ratios": [0.86, 0.14], "hspace": 0},
            facecolor=Colors.BG,
        )
        
        # Safe window title setting
        if fig.canvas.manager:
            fig.canvas.manager.set_window_title(f"RATINGS - {self.username}")

        for a in (ax, ax_stats):
            a.set_facecolor(Colors.BG)
        ax_stats.axis('off')

        bars = ax.bar(rating_positions, rating_counts, width=0.45, color=Colors.BLUE, alpha=0.85)

        self._draw_header_and_stats(ax, ax_stats, total_ratings, average_rating, most_given_rating)
        self._label_bars(ax, bars, rating_counts)
        self._style_axes(ax, max(rating_counts) if len(rating_counts) else 0)

        plt.tight_layout()
        plt.show()

    def fetch_ratings(self, username=None) -> dict:
        """Fetch user ratings from Letterboxd"""
        target_user = username or self.username
        
        if not target_user:
             raise ValueError("Username must be provided")

        # Initialize with 0
        ratings = dict.fromkeys(np.arange(0.5, 5.5, 0.5), 0)
        
        print(f"Fetching ratings for @{target_user}...")
        movies = User(target_user).get_films()["movies"]
        print(f"Processing {len(movies)} rated movies...")
        
        for movie in movies.values():
            if rating := movie.get("rating"):
                try:
                    ratings[float(rating)] += 1
                except KeyError:
                    pass
        
        total_ratings = sum(ratings.values())
        print(f"Found {total_ratings} ratings. Creating plot...")
        return ratings

    def plot(self, username=None):
        """Fetch ratings and create plot"""
        if username:
            self.username = username

        try:
            ratings = self.fetch_ratings()
            if sum(ratings.values()) > 0:
                self.create_plot(ratings)
            else:
                print(f"No ratings found for user: {self.username}")
        except ValueError as e:
            print(f"Error: {e}")

    def run(self):
        """Main program loop"""
        try:
            sys.stdout.reconfigure(encoding="utf-8") # type: ignore
        except AttributeError:
            pass # Python < 3.7 or non-standard stdout

        parser = argparse.ArgumentParser(description="Visualize Letterboxd user rating distribution.")
        parser.add_argument("--user", help="Letterboxd username to analyze")

        args = parser.parse_args()
        
        username = args.user if not is_whitespace_or_empty(args.user) else None
        
        if not username:
            username = get_input("Enter Letterboxd username: ")
            
        self.plot(username)


def main():
    """Legacy function compatibility"""
    LetterboxdRatingPlotter().run()

if __name__ == "__main__":
    main()
