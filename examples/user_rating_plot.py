"""
Letterboxd Ratings Histogram

Recreates the ratings distribution section of a Letterboxd profile with a clean, professional layout.
- Half-star tick labels (½, ★, ★½, …, ★★★★★)
- Shows username, total ratings, average, and most given rating
- Letterboxd-inspired color scheme
"""

import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np

from letterboxdpy.user import User
from letterboxdpy.utils.utils_terminal import get_input
from letterboxdpy.utils.utils_validators import is_whitespace_or_empty


class Constants:
    # Letterboxd-inspired colors
    BG_COLOR = "#14181C"        # Letterboxd dark background
    BAR_COLOR = "#456"          # Letterboxd blue
    HIGHLIGHT_COLOR = "#00C030" # Letterboxd green
    TEXT_COLOR = "#9AB"         # Letterboxd text gray


class LetterboxdRatingPlotter:
    def __init__(self, username: str = None):
        self.username = username
        
    def create_plot(self, ratings: dict):
        """Create Letterboxd-style rating distribution plot with enhancements"""
        rating_positions = np.arange(0.5, 5.5, 0.5)
        rating_counts = np.array([ratings.get(rating, 0) for rating in rating_positions])
        total_ratings = int(rating_counts.sum())
        average_rating = round(float((rating_positions * rating_counts).sum() / total_ratings), 2) if total_ratings else 0.0
        most_given_rating = float(rating_positions[rating_counts.argmax()]) if total_ratings else 0.5

        # Nested helpers for readability
        def draw_header_and_stats(axis, stats_axis, total_count: int) -> None:
            axis.text(0.02, 0.98, "R A T I N G S", transform=axis.transAxes,
                      fontsize=12, color=Constants.TEXT_COLOR, weight='bold', va='top', family='monospace')
            axis.text(0.98, 0.98, f"{total_count:,}", transform=axis.transAxes,
                      fontsize=12, color=Constants.TEXT_COLOR, weight='bold', va='top', ha='right')
            axis.text(0.02, 0.92, f"@{self.username}", transform=axis.transAxes,
                      fontsize=11, color='white', weight='bold', va='top')
            stats_axis.text(0.5, 0.5, f"Average: {average_rating}★  •  Total: {total_ratings:,}  •  Most Given: {most_given_rating}★",
                            ha='center', va='center', fontsize=11, color=Constants.TEXT_COLOR, weight='bold')

        def get_star_labels():
            positions = np.arange(0.5, 5.5, 0.5)
            labels = [
                ("½★" if r == 0.5 else ("★" * int(r) + "½" if r % 1 == 0.5 else "★" * int(r)))
                for r in positions
            ]
            return positions, labels

        def label_bars(axis, bars_, counts_) -> None:
            if len(counts_) == 0:
                return
            max_count = max(counts_)
            for bar, count in zip(bars_, counts_):
                if count == max_count:
                    bar.set_color(Constants.HIGHLIGHT_COLOR)
                    bar.set_alpha(1.0)
                if count > 0:
                    axis.text(bar.get_x() + bar.get_width() / 2, count + max_count * 0.01,
                              str(int(count)), ha="center", va="bottom", fontsize=8,
                              color=Constants.TEXT_COLOR, alpha=0.9)

        def style_axes(axis, counts_) -> None:
            axis.set_xlim(0.25, 5.25)
            max_count = max(counts_) if len(counts_) else 0
            axis.set_ylim(0, max_count * 1.12)
            tick_positions, tick_labels = get_star_labels()
            axis.set_xticks(tick_positions)
            axis.set_xticklabels(tick_labels, fontsize=9, color=Constants.TEXT_COLOR)
            axis.set_yticks([])
            for spine in axis.spines.values():
                spine.set_visible(False)
            axis.grid(True, axis='y', alpha=0.1, color=Constants.TEXT_COLOR, linestyle='-')

        # Create Letterboxd-style plot
        fig, (ax, ax_stats) = plt.subplots(
            2, 1,
            figsize=(12, 8),
            gridspec_kw={"height_ratios": [0.86, 0.14], "hspace": 0},
            facecolor=Constants.BG_COLOR,
        )
        for a in (ax, ax_stats):
            a.set_facecolor(Constants.BG_COLOR)
        ax_stats.axis('off')
        fig.canvas.manager.set_window_title(f"RATINGS - {self.username}")

        bars = ax.bar(rating_positions, rating_counts, width=0.45, color=Constants.BAR_COLOR, alpha=0.85)

        # Header and bottom stats
        draw_header_and_stats(ax, ax_stats, total_ratings)

        # Bar labels and highlight
        label_bars(ax, bars, rating_counts)

        # Axes styling and ticks
        style_axes(ax, rating_counts)

        # Layout handled by GridSpec; light tightening only
        plt.tight_layout()
        plt.show()

    def fetch_ratings(self, username: str = None) -> dict:
        """Fetch user ratings from Letterboxd"""
        username = username or self.username
        ratings = {r: 0 for r in np.arange(0.5, 5.5, 0.5)}
        
        print(f"Fetching ratings for @{username}...")
        movies = User(username).get_films()["movies"]
        print(f"Processing {len(movies)} rated movies...")
        
        for movie in movies.values():
            if rating := movie.get("rating"):
                ratings[rating/2] += 1
        
        total_ratings = sum(ratings.values())
        print(f"Found {total_ratings} ratings. Creating plot...")
        return ratings

    def plot(self, username: str = None):
        """Fetch ratings and create plot"""
        if username:
            self.username = username

        ratings = self.fetch_ratings()
        if sum(ratings.values()) > 0:
            self.create_plot(ratings)
        else:
            print(f"No ratings found for user: {self.username}")

    def run(self):
        """Main program loop"""
        sys.stdout.reconfigure(encoding="utf-8")
        parser = argparse.ArgumentParser(description="Visualize Letterboxd user rating distribution.")
        parser.add_argument("--user", help="Letterboxd username to analyze")

        args = parser.parse_args()
        
        username = None if is_whitespace_or_empty(args.user) else args.user
        if not username:
            username = get_input("Enter Letterboxd username: ")
        self.plot(username)


def main():
    """Legacy function compatibility"""
    LetterboxdRatingPlotter().run()

if __name__ == "__main__":
    main()