# Letterboxd Examples

Example scripts demonstrating `letterboxdpy` library features.

## Installation

```bash
# Standard install with example dependencies
pip install ".[examples]"

# Or for local development
pip install -e ".[examples]"
```

## Examples

Run commands from the repository root. Arguments shown in angle brackets are
values you provide.

| Script | Description | Usage | Output |
|--------|-------------|-------|--------|
| [`profile_editor.py`](profile_editor.py) | Interactive authenticated profile and favorites editor | `python examples/profile_editor.py [--path <cookies.json>]` | Updates the authenticated Letterboxd profile |
| [`notification_manager.py`](notification_manager.py) | Interactive authenticated notification settings manager | `python examples/notification_manager.py [--path <cookies.json>]` | Updates the authenticated account settings |
| [`compare_watchlists.py`](compare_watchlists.py) | Compares the target watchlist with followed users | `python examples/compare_watchlists.py <username> [--force]` | `exports/users/<username>/watchlist_comparison.json` and `.html` |
| [`follow_stats.py`](follow_stats.py) | Finds mutual follows, followers you do not follow, and unrequited follows | `python examples/follow_stats.py <username>` | `exports/users/<username>/follow_stats.json` and `.html` |
| [`user_rating_plot.py`](user_rating_plot.py) | Displays a Letterboxd-style rating distribution histogram | `python examples/user_rating_plot.py <username>` | Interactive Matplotlib window |
| [`user_plot_statistics.py`](user_plot_statistics.py) | Displays yearly movie-watching statistics | `python examples/user_plot_statistics.py <username> [--start-year <year>] [--end-year <year>]` | Interactive Matplotlib window |
| [`export_user_data.py`](export_user_data.py) | Exports profile, films, diary, reviews, lists, network, tags, and watchlist data | `python examples/export_user_data.py <username>` | JSON files under `exports/users/<username>/` |
| [`export_user_diary_posters.py`](export_user_diary_posters.py) | Downloads posters from a user's diary | `python examples/export_user_diary_posters.py <username>` | Images under `exports/users/<username>/posters/` |
| [`search_and_export_lists.py`](search_and_export_lists.py) | Searches Letterboxd lists and exports their films | `python examples/search_and_export_lists.py <query> <max-lists>` | CSV files under `exports/lists/` |

Most username-based scripts also prompt for a username when it is omitted.
Scripts that expose `--user` accept it as an alternative to the positional
username. Use each script's `--help` option to see its complete CLI where
available.

The profile and notification tools require an authenticated cookie file. Their
`--path` option defaults to the library's standard cookie location.

## Adding New Examples

If you'd like to contribute a new example that generates a report, use the
following metadata standard at the top of the script:

```python
__title__ = "Your Tool Name"
__description__ = "What it does in one sentence."
__version__ = "0.1.0"
__author__ = "yourname"
__author_url__ = "https://github.com/yourname"
__created_at__ = "YYYY-MM-DD"
```

## Requirements

Dependencies are managed via optional extras in `pyproject.toml`.

- **Standard Dependencies:** `curl_cffi`, `beautifulsoup4`, `lxml`, `fastfingertips`
- **Example Extras:** `rich`, `Jinja2`, `matplotlib`, `numpy`, `pillow`

To install everything needed for examples, run:

```bash
pip install ".[examples]"
```

