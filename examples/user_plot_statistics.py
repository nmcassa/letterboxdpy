"""
Letterboxd User Statistics Plotter

Creates visualizations of user movie watching patterns over time.
- Monthly and daily viewing statistics by year
- Multi-year comparison charts
- Letterboxd-inspired styling
"""

import argparse
import sys
from datetime import datetime

import matplotlib.pyplot as plt
from fastfingertips.terminal_utils import get_input

from letterboxdpy.constants.project import (
    DAY_ABBREVIATIONS,
    MONTH_ABBREVIATIONS,
    Colors,
)
from letterboxdpy.user import User


class LetterboxdStatisticsPlotter:
    """Class for plotting Letterboxd user statistics."""
    
    def __init__(self, username: str):
        self.username = username
        self.stats_by_year = {}
        
    def gather_statistics_by_year(self, start_year: int, end_year: int) -> dict:
        """Fetch user statistics for each year."""
        self.stats_by_year = {}
        year_count = end_year - start_year + 1
        
        print(f"Fetching statistics for @{self.username}...")
        print(f"Processing {year_count} year(s): {start_year}-{end_year}")
        
        for year in range(start_year, end_year + 1):
            try:
                print(f"Fetching data for {year}...", end=" ")
                user = User(self.username)
                stats = user.get_wrapped(year)
                self.stats_by_year[year] = {
                    "monthly": stats.get("months"),
                    "daily": stats.get("days")
                }
                print("✓")
            except Exception:
                print("✗ (using empty data)")
                self.stats_by_year[year] = {
                    "monthly": dict.fromkeys(range(1, 13), 0),  # 12 months with 0
                    "daily": dict.fromkeys(range(1, 8), 0)      # 7 days with 0
                }
        
        print("Data collection complete. Creating plot...")
        return self.stats_by_year
    
    def plot_statistics(self) -> None:
        if not self.stats_by_year:
            return
        
        num_years = len(self.stats_by_year)
        
        # squeeze=False ensures axes is always a 2D array, simplifying logic
        fig, axes = plt.subplots(
            num_years, 2, 
            figsize=(12, 3 * num_years), 
            facecolor=Colors.BG, 
            squeeze=False
        )

        years_range = f"{min(self.stats_by_year.keys())}-{max(self.stats_by_year.keys())}"
        
        # Safe window title access
        if fig.canvas.manager:
            fig.canvas.manager.set_window_title(f'Letterboxd Statistics - {self.username} ({years_range})')
            
        fig.suptitle(f'{self.username} - Movies Watched ({years_range})', fontsize=16, color='white')

        def style_axes(ax):
            ax.set_facecolor(Colors.BG)
            ax.tick_params(colors=Colors.TEXT)
            for spine in ax.spines.values():
                spine.set_color(Colors.TEXT)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(Colors.TEXT)
            ax.spines['bottom'].set_color(Colors.TEXT)

        days_labels = DAY_ABBREVIATIONS
        months_labels = MONTH_ABBREVIATIONS
        
        for i, (year, stats) in enumerate(self.stats_by_year.items()):
            daily_data = stats.get('daily', {})
            monthly_data = stats.get('monthly', {})
            
            daily_values = [daily_data.get(day, 0) for day in range(1, 8)]
            monthly_values = [monthly_data.get(month, 0) for month in range(1, 13)]

            # Access subplots safely from 2D array
            ax_daily = axes[i, 0]
            ax_monthly = axes[i, 1]

            for ax in [ax_daily, ax_monthly]:
                style_axes(ax)

            ax_daily.bar(days_labels, daily_values, color=Colors.BLUE, alpha=0.85)
            ax_daily.set_title(f'{year} - Daily', color='white')
            ax_daily.set_ylabel('Movies', color=Colors.TEXT)

            ax_monthly.bar(months_labels, monthly_values, color=Colors.GREEN, alpha=0.85)
            ax_monthly.set_title(f'{year} - Monthly', color='white')
            ax_monthly.set_ylabel('Movies', color=Colors.TEXT)

        plt.tight_layout(rect=(0, 0, 1, 0.95))
        plt.show()

    def plot(self, start_year=None, end_year=None):
        """Gather statistics and create plot"""
        if start_year is None:
            current_year = datetime.now().year
            start_year = current_year - 1
        if end_year is None:
            end_year = datetime.now().year
            
        self.gather_statistics_by_year(start_year, end_year)
        
        if self.stats_by_year:
            self.plot_statistics()
        else:
            print(f"No statistics found for user: {self.username}")

    def run(self):
        """Main program loop"""
        try:
             sys.stdout.reconfigure(encoding="utf-8") # type: ignore
        except AttributeError:
             pass

        parser = argparse.ArgumentParser(description="Visualize Letterboxd user statistics")
        parser.add_argument("--user", help="Letterboxd username")
        current_year = datetime.now().year
        parser.add_argument("--start-year", type=int, default=current_year-1, help=f"Start year (default: {current_year-1})")
        parser.add_argument("--end-year", type=int, default=current_year, help=f"End year (default: {current_year})")
        args = parser.parse_args()

        username = args.user if args.user else get_input("Enter Letterboxd username: ", index=1)
            
        self.username = username
        self.plot(args.start_year, args.end_year)


def main():
    """Legacy function compatibility"""
    LetterboxdStatisticsPlotter("").run()


if __name__ == "__main__":
    main()
