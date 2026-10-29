# Examples and CLI Tools

The `letterboxdpy` repository includes a collection of production-ready CLI tools, data exporters, and visual analytics scripts located in the `examples/` directory.

These scripts demonstrate real-world patterns for scraping, reporting, data visualization, and session management.

---

## Installation

Examples rely on optional third-party packages for visualization (`matplotlib`, `pillow`), interactive reporting (`Jinja2`, `rich`), and spreadsheet creation (`openpyxl`).

=== "Standard Install"
    ```bash
    pip install "letterboxdpy[examples]"
    ```

=== "Editable Development"
    ```bash
    pip install -e ".[examples]"
    ```

---

## Command-Line Conventions

- Run all commands from the repository root directory.
- Arguments in `<angle_brackets>` represent user-supplied values.
- Most username-driven scripts prompt for a username if omitted in the command.
- Scripts supporting the `--open` flag automatically launch generated HTML reports in your default browser.
- Authenticated scripts accept an optional `--path` parameter pointing to a `cookies.json` session file (defaults to `~/.letterboxdpy/cookies.json`).

---

## User Analytics and Visualizations

### Rating Distribution Plot (`user_rating_plot.py`)

Renders a Letterboxd-style histogram displaying the target user's ratings across all half-star increments (0.5 to 5.0 stars), along with mean rating and total rated film counts.

```bash
python examples/user_rating_plot.py bugracoskun
```

- **Output:** Interactive Matplotlib graphic window displaying rating frequency and distribution curve.
- **Dependencies:** `matplotlib`, `numpy`

---

### Yearly Watching Statistics (`user_plot_statistics.py`)

Plots annual movie-watching volume from diary entries across release years or logging years.

```bash
# Analyze all available years
python examples/user_plot_statistics.py bugracoskun

# Filter by release year range
python examples/user_plot_statistics.py bugracoskun --start-year 2015 --end-year 2025
```

- **Output:** Interactive Matplotlib bar chart of logged films per year.
- **Dependencies:** `matplotlib`

---

### Styled Excel Exporter (`export_user_data_excel.py`)

Exports complete user activity into an Excel workbook (`.xlsx`) featuring custom column formatting, header styles, and tabbed sheets for profile metadata, watched films, diary logs, and ratings.

```bash
python examples/export_user_data_excel.py bugracoskun --runtime --open
```

| Flag | Description |
| :--- | :--- |
| `--user <username>` | Alternative to positional username argument. |
| `--runtime` | Fetches runtime for each movie to calculate total hours watched. |
| `--force` | Overwrites existing exports without prompting. |
| `--open` | Automatically opens the generated `.xlsx` file upon completion. |

- **Output File:** `examples/exports/users/<username>/<username>_data.xlsx`
- **Dependencies:** `openpyxl`, `rich`

---

### Comprehensive JSON Exporter (`export_user_data.py`)

Extracts every major dataset from a user profile into structured JSON files under an organized folder hierarchy.

```bash
python examples/export_user_data.py bugracoskun
```

Exports generated under `examples/exports/users/<username>/`:

- `user.json`: Core profile details, follower counts, bio, website.
- `films.json`: Complete catalog of watched films.
- `watchlist.json`: Current watchlist entries.
- `diary.json`: Chronological diary logs and review snippets.
- `lists.json`: User-authored lists.
- `followers.json` and `following.json`: Social graph entries.

---

## Social and Network Insights

### Watchlist Comparison (`compare_watchlists.py`)

Compares a user's watchlist with the watchlists of users they follow, finding shared interests and common recommendations.

```bash
python examples/compare_watchlists.py bugracoskun --open
```

- **Output Files:**
  - `examples/exports/users/<username>/watchlist_comparison.json`
  - `examples/exports/users/<username>/watchlist_comparison.html`
- **Features:** Computes overlap score, common films, and unique recommendations rendered via responsive HTML.

---

### Follow Relationship Statistics (`follow_stats.py`)

Audits account connections to identify mutual follows, fans (users following you whom you do not follow back), and unrequited follows (users you follow who do not follow back).

```bash
python examples/follow_stats.py bugracoskun --open
```

- **Output Files:**
  - `examples/exports/users/<username>/follow_stats.json`
  - `examples/exports/users/<username>/follow_stats.html`
- **Interactive UI:** Searchable table of user avatars, badges, and follow states.

---

### Network Balance Analysis (`network_balance.py`)

Analyzes follow ratios, mutual percentages, and network reciprocity metrics for any public profile.

```bash
python examples/network_balance.py bugracoskun --open
```

- **Output Files:**
  - `examples/exports/users/<username>/network_balance.json`
  - `examples/exports/users/<username>/network_balance.html`

---

## Bulk Media and List Operations

### User Diary Poster Downloader (`export_user_diary_posters.py`)

Crawls a user's diary and downloads full-resolution movie posters into a local directory.

```bash
python examples/export_user_diary_posters.py bugracoskun
```

- **Output Directory:** `examples/exports/users/<username>/posters/`
- **Dependencies:** `pillow`, `curl_cffi`

---

### List Search and Film Exporter (`search_and_export_lists.py`)

Searches public Letterboxd lists matching a keyword query and exports all included film titles, release years, and URLs into CSV format.

```bash
python examples/search_and_export_lists.py "Cyberpunk" 5
```

- **Arguments:**
  1. Search query string (e.g. `"Cyberpunk"`).
  2. Maximum number of lists to scrape (e.g. `5`).
- **Output Directory:** `examples/exports/lists/`

---

## Interactive Account Management

> [!NOTE]
> Account management tools require an active Letterboxd session. Generate a `cookies.json` using `UserSession.login()` or export browser cookies before running these scripts.

### Profile and Favorites Editor (`profile_editor.py`)

Interactive command-line interface to view and modify Letterboxd profile fields and the four featured favorite films without using a web browser.

```bash
python examples/profile_editor.py
# or specify a custom cookies path
python examples/profile_editor.py --path /path/to/cookies.json
```

Editable fields include:

- Given Name / Family Name
- Bio / Description
- Location
- Website URL
- Pronoun Selection
- Top Four Featured Favorite Films

---

### Notification Settings Manager (`notification_manager.py`)

Interactive command-line tool to toggle site-wide notifications and email alert preferences.

```bash
python examples/notification_manager.py
```

Configurable options include:

- New follower email notifications
- Comments on reviews and lists
- Mentions and reply alerts
- Letterboxd newsletter and weekly digest subscriptions

---

## Contributing New Examples

New utility scripts and reports are welcomed. Contributions should adhere to the standard module metadata header:

```python
__title__ = "Tool Name"
__description__ = "Single sentence summary of what the script accomplishes."
__version__ = "0.1.0"
__author__ = "yourusername"
__author_url__ = "https://github.com/yourusername"
__created_at__ = "2026-10-29"
```

Guidelines for script contributions:

1. Rely on `letterboxdpy` core models for all scraping operations.
2. Put output files under `examples/exports/`.
3. Provide descriptive CLI arguments using `sys.argv` or standard library `argparse`.
4. Run `ruff check` and `ruff format` prior to submitting changes.
