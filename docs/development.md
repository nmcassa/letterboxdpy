# Development Guide

This guide covers setting up your development environment, running tests, linting, building documentation, and contributing to `letterboxdpy`.

---

## Environment Setup

`letterboxdpy` requires **Python 3.10 or higher**.

Clone the repository and install all optional development dependencies:

```bash
git clone https://github.com/nmcassa/letterboxdpy.git
cd letterboxdpy

# Install in editable mode with development, docs, and example dependencies
pip install -e ".[dev,docs,examples]"
```

---

## Code Quality & Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and formatting.

```bash
# Check for lint issues
ruff check .

# Automatically fix fixable issues
ruff check --fix .

# Format code
ruff format .
```

---

## Testing

The test suite separates fast, deterministic offline unit tests from live external network tests against Letterboxd (marked as `smoke`).

### Run Offline Unit Tests (Default)

Executes parser and model tests in ~0.5 seconds without any external network calls:

```bash
python -m pytest
```

### Run Live Network Tests (Smoke Marker)

Executes integration tests directly against live Letterboxd endpoints:

```bash
python -m pytest -m smoke
```

### Run All Tests

```bash
python -m pytest -m "smoke or not smoke"
```

> [!NOTE]
> Tests that require an authenticated Letterboxd session (e.g. `test_auth.py`) are automatically skipped if no valid `.cookie` file is present. This ensures the suite runs cleanly in CI environments without credentials.

---

## Documentation

The documentation site is built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and [mkdocstrings](https://mkdocstrings.github.io/).

### Local Preview

To preview the documentation locally with hot-reloading:

```bash
mkdocs serve
```

Open `http://127.0.0.1:8000` in your browser.

### Strict Verification

To verify that all cross-references, docstrings, and navigation links build without warnings:

```bash
mkdocs build --strict
```

---

## Pre-commit Hooks

Pre-commit hooks automatically check linting rules with Ruff and validate commit title length before each commit:

- **Ruff & Ruff-Format:** Runs on commit to verify and auto-format staged files.
- **Commit Title Length:** Validates that the first line of the commit message follows [Conventional Commits](https://www.conventionalcommits.org/) and is at or under **62 characters** (checked on `commit-msg`).

```bash
# Install hooks for both pre-commit and commit-msg stages
pre-commit install --hook-type pre-commit --hook-type commit-msg

# Run manually against all files
pre-commit run --all-files
```

---

## CI / CD Pipeline

GitHub Actions automatically runs on every push and pull request against the `main` branch:

1. **Lint & Test:** Validates formatting with Ruff and executes the pytest offline test suite across all supported Python versions (3.10, 3.11, 3.12, 3.13, 3.14).
2. **Verify Docs:** Runs `mkdocs build --strict` to ensure zero broken links or documentation errors.
3. **Deploy Docs:** Builds and deploys the site to GitHub Pages on every push to `main`.

