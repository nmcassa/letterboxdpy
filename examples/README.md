# Letterboxd Examples

Example scripts demonstrating `letterboxdpy` library features.

## Installation

```bash
pip install -e .
pip install -r examples/requirements.txt
```

## Examples

**[`compare_watchlists.py`](compare_watchlists.py)**
Compare your watchlist with people you follow. Find films that friends also want to watch!
```bash
python examples/compare_watchlists.py --user <username>
```

**[`user_rating_plot.py`](user_rating_plot.py)**  
Creates a rating distribution histogram with Letterboxd styling.
```bash
python examples/user_rating_plot.py --user <username>
```

**[`user_plot_statistics.py`](user_plot_statistics.py)**  
Visualizes movie watching patterns over time with monthly and daily statistics.
```bash
python examples/user_plot_statistics.py --user <username> --start-year 2020 --end-year 2024
```

**[`follow_stats.py`](follow_stats.py)**  
Analyzes follow relationships, followback ratios, and mutual follows.
```bash
echo <username> | python examples/follow_stats.py
```

**[`export_user_data.py`](export_user_data.py)**  
Exports all user data (films, reviews, lists, followers, etc.) to JSON files.
```bash
echo <username> | python examples/export_user_data.py
```

**[`export_user_diary_posters.py`](export_user_diary_posters.py)**  
Downloads movie posters from diary entries and organizes them by year.
```bash
echo <username> | python examples/export_user_diary_posters.py
```

**[`search_and_export_lists.py`](search_and_export_lists.py)**  
Searches for lists by query and exports them to CSV format.
```bash
echo -e "query\n3" > input.txt
Get-Content input.txt | python examples/search_and_export_lists.py
```

## Requirements

**letterboxdpy dependencies** (auto-installed with `pip install -e .`):
- requests, beautifulsoup4, lxml, validators

**Example-specific dependencies** (install with `pip install -r examples/requirements.txt`):
- matplotlib, numpy, pillow — *used by visualization scripts*

See [`requirements.txt`](requirements.txt) for details.
