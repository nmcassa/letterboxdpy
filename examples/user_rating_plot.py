import argparse
import sys
import os
import matplotlib.pyplot as plt
import json
import numpy as np

try:
    from letterboxdpy.user import User
except ImportError:
    try:
        sys.path.append(os.path.join(sys.path[0], '..'))
        from letterboxdpy.user import User
    except (ImportError, ValueError) as e:
        raise ImportError(f"Error importing 'letterboxdpy': {e}. Please install the package.") from e


def create_rating_distribution_plot(user_ratings: dict):
    mean_rating = round(sum(rating * count for rating, count in user_ratings.items()) / sum(user_ratings.values()), 2)
    all_ratings = [rating for rating, count in user_ratings.items() for _ in range(count)]
    
    plt.style.use('dark_background')
    figure, axis = plt.subplots(figsize=(12, 6))
    
    rating_intervals = np.arange(0.25, 5.75, 0.5)
    rating_counts, _, histogram_bars = axis.hist(all_ratings, bins=rating_intervals, color="#5A5F71", rwidth=0.8)
    
    plot_statistics_text = f"Average: {mean_rating}★     Total Ratings: {len(all_ratings):,}"
    plt.text(0.5, 1.05, plot_statistics_text, 
             ha='center', transform=axis.transAxes, fontsize=12, color='white', weight='bold')
    
    highest_count = max(rating_counts)
    for bar, rating_frequency in zip(histogram_bars, rating_counts):
        if rating_frequency == highest_count:
            bar.set_color("#4CAF50")
        
        if rating_frequency > 0:
            bar_center_x = bar.get_x() + bar.get_width()/2
            text_y_position = rating_frequency + highest_count*0.02
            axis.text(bar_center_x, text_y_position,
                     str(int(rating_frequency)), 
                     ha="center", va="bottom", fontsize=10,
                     color="white", weight='bold')
    
    axis.set_xlim(0.25, 5.25)
    axis.set_ylim(0, highest_count * 1.15)
    
    rating_labels = np.arange(0.5, 5.5, 0.5)
    axis.set_xticks(rating_labels)
    axis.set_xticklabels([f"{rating:.1f}★" for rating in rating_labels], fontsize=10)
    axis.set_yticks([])
    
    axis.set_title("Letterboxd Rating Distribution", fontsize=16, weight="bold", pad=35)
    
    for spine_location in ["top", "right", "left"]:
        axis.spines[spine_location].set_visible(False)
    axis.spines["bottom"].set_color("#FFFFFF")
    
    plt.subplots_adjust(top=0.88, bottom=0.15)
    plt.tight_layout()
    plt.show()

def fetch_letterboxd_ratings(username: str) -> dict:
    rating_distribution = {rating: 0 for rating in np.arange(0.5, 5.5, 0.5)}
    
    user_movies = User(username).get_films()["movies"]
    for movie_data in user_movies.values():
        if movie_rating := movie_data.get("rating"):
            converted_rating = movie_rating/2  
            rating_distribution[converted_rating] = rating_distribution.get(converted_rating, 0) + 1
            
    return rating_distribution

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    argument_parser = argparse.ArgumentParser(description="Visualize Letterboxd user rating distribution.")
    argument_parser.add_argument("--user", help="Letterboxd username to analyze")
    
    letterboxd_username = argument_parser.parse_args().user or input("Enter Letterboxd username: ").strip()
    
    user_rating_data = fetch_letterboxd_ratings(letterboxd_username)
    if user_rating_data:
        create_rating_distribution_plot(user_rating_data)
    else:
        print(f"No ratings found for Letterboxd user: {letterboxd_username}")

if __name__ == "__main__":
    main()