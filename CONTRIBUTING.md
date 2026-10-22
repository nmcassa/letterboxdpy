# Contributing Guidelines

Thank you for contributing to letterboxdpy! Please follow these guidelines to keep the codebase clean, consistent, and maintainable.

## Branch Strategy

We follow a structured branch workflow:

- **`develop`**: Main integration branch for active development and pull requests.
- **`staging`**: Pre-release testing branch, merged from `develop`.
- **`main`**: Production-ready release branch, tagged for PyPI releases.

Please submit all pull requests to `develop`, not `main`.

## Development Setup

1. **Python Requirement:** Python 3.10 or higher.
2. **Create a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install Editable Package with Extras:**
   ```bash
   pip install -e ".[examples]"
   ```
4. **Install Pre-commit Hooks:**
   ```bash
   pre-commit install --hook-type pre-commit --hook-type commit-msg
   ```

## Commit Message Guidelines

To maintain clean and readable git logs, all commits must adhere to the following rules:

- **Length Limit:** Keep the commit title (first line) at or under **62 characters**. This is enforced automatically via a pre-commit `commit-msg` hook.
- **Commit Type Prefix:** Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification using standard prefixes:
  - `feat:` for new features or user-facing additions.
  - `fix:` for bug fixes.
  - `docs:` for documentation updates.
  - `style:` for code style, formatting, and cleanup without behavior changes.
  - `refactor:` for code restructuring without changing external behavior.
  - `perf:` for performance optimizations.
  - `test:` for adding or updating tests.
  - `ci:` for CI/CD workflow and tooling changes.
  - `chore:` for dependency bumps, version updates, and maintenance.
- **No Emojis:** Do not use emojis in commit titles, commit messages, or pull request descriptions.
- **Commit Body:** Place detailed technical rationale, bullet points, or issue references in the commit body after a blank line.

## Code Style and Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and code formatting:

```bash
# Check code for linting errors
ruff check .

# Automatically apply safe fixes
ruff check --fix .

# Format code
ruff format .
```

## Testing Guidelines

The test suite is partitioned into offline unit tests and live network tests:

- **Offline Unit Tests (Default):**
  Validate parser utilities, models, and local decorators in ~0.5 seconds without network requests:
  ```bash
  python -m pytest
  ```
- **Live Smoke Tests:**
  Exercise real Letterboxd web pages and DOM structures:
  ```bash
  python -m pytest -m smoke
  ```
- **Full Test Suite:**
  ```bash
  python -m pytest -m "smoke or not smoke"
  ```

Always ensure offline unit tests and Ruff checks pass before creating a pull request.
