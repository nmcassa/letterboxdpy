# Letterboxd Examples

Example scripts demonstrating `letterboxdpy` library features.

## Installation

```bash
pip install -e .
pip install -r examples/requirements.txt
```

## Examples

| Script | Description | Usage |
|--------|-------------|-------|
| [`compare_watchlists.py`](compare_watchlists.py) | Compare watchlists from followed users (generates interactive HTML) | `python examples/compare_watchlists.py --user <username>` |
| [`follow_stats.py`](follow_stats.py) | Analyzes follow relationships and mutuals (generates interactive HTML) | `python examples/follow_stats.py --user <username>` |
| [`user_rating_plot.py`](user_rating_plot.py) | Creates a rating distribution histogram with Letterboxd styling | `python examples/user_rating_plot.py --user <username>` |
| [`user_plot_statistics.py`](user_plot_statistics.py) | Visualizes movie watching patterns over time | `python examples/user_plot_statistics.py --user <username> --start-year 2020 --end-year 2024` |
| [`export_user_data.py`](export_user_data.py) | Exports all user data to JSON files | `echo <username> \| python examples/export_user_data.py` |
| [`export_user_diary_posters.py`](export_user_diary_posters.py) | Downloads movie posters from diary entries | `echo <username> \| python examples/export_user_diary_posters.py` |
| [`search_and_export_lists.py`](search_and_export_lists.py) | Searches for lists and exports to CSV | `python examples/search_and_export_lists.py` |

## Adding New Examples

If you'd like to contribute a new example that generates a report, please use the following metadata standard at the top of your script:

```python
__title__ = "Your Tool Name"
__description__ = "What it does in one sentence."
__version__ = "0.1.0"
__author__ = "yourname"
__author_url__ = "https://github.com/yourname"
__created_at__ = "YYYY-MM-DD"
```

## Requirements

**letterboxdpy dependencies** (auto-installed with `pip install -e .`):
- curl_cffi, beautifulsoup4, lxml, fastfingertips

**Example-specific dependencies** (install with `pip install -r examples/requirements.txt`):
- matplotlib, numpy, pillow — *used by visualization scripts*
- Jinja2 — *used for HTML reports*

See [`requirements.txt`](requirements.txt) for details.
