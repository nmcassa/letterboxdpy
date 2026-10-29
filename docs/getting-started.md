# Getting Started

This guide walks you through installing `letterboxdpy` and making your first queries.

---

## Requirements

- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- Active internet connection (Letterboxd requests are sent over HTTPS)

---

## Installation

Install the package via pip:

```bash
pip install letterboxdpy
```

If you plan to run the included examples (which use `matplotlib`, `rich`, `pillow`, etc.):

```bash
pip install "letterboxdpy[examples]"
```

---

## Cloudflare & Network Resilience

Letterboxd is protected by Cloudflare WAF. `letterboxdpy` includes built-in safeguards to ensure reliable data retrieval:

1. **Browser Impersonation**: Uses `curl_cffi` to mimic real browser TLS fingerprints (`chrome120`).
2. **Canonical URL Normalization**: Automatically validates and appends canonical trailing slashes (`/`) per Letterboxd routing standards, preventing 403 challenge blocks and redundant redirects.
3. **Retry Strategy**: Automatically retries transient network interruptions with progressive backoff timeouts.

---

## Core Classes at a Glance

| Class | Description | Primary Method / Property | Guide |
| :--- | :--- | :--- | :--- |
| `User` | User profiles, watched movies, diary, network, and stats | `user.get_films()`, `user.stats` | [User Guide](guides/user.md) |
| `Movie` | Movie metadata, ratings, cast, reviews, similar movies | `movie.rating`, `movie.pages.similar` | [Movie Guide](guides/movie.md) |
| `Search` | Query films, lists, users, reviews, or tags | `search.results`, `search.get_results()` | [Search Guide](guides/search.md) |
| `List` | User-curated lists and film rankings | `list.movies`, `list.count` | [List Guide](guides/list.md) |
| `Watchlist` | User watchlist extraction with filter support | `watchlist.movies`, `watchlist.count` | [Watchlist Guide](guides/watchlist.md) |
| `Members` | Community leaderboards and popular members | `members.members`, `members.get_members()` | [Members Guide](guides/members.md) |
| `Films` | High-level discovery by genre, year, decade, or theme | `get_movies_by_genre()`, `get_upcoming_movies()` | [Films Guide](guides/films.md) |
| `UserSession` | Trace-locked authenticated session management | `UserSession.ensure()`, `session.login()` | [Auth Guide](guides/auth.md) |
| `UserSettings` | Account profile metadata and notification preferences | `settings.get_profile()`, `settings.update_profile()` | [Auth Guide](guides/auth.md) |

Check out the **Guides** and **API Reference** sections to learn more about each component.

