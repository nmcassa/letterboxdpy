# Contributing Guidelines

Thank you for contributing to letterboxdpy! Please follow these guidelines to keep the codebase clean, consistent, and maintainable.

## Branch Strategy

We follow a structured branch workflow:

- **`develop`**: Main integration branch for active development and pull requests.
- **`staging`**: Pre-release testing branch, merged from `develop`.
- **`main`**: Production-ready release branch, tagged for PyPI releases.

Please submit all pull requests to `develop`, not `main`.

## Development Setup

See the [Development Guide](docs/development.md) for environment setup, linting, and testing. Always ensure offline unit tests and Ruff checks pass before creating a pull request.

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
