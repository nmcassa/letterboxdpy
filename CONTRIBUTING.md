# Contributing Guidelines

## Branch Strategy
We follow a structured branch workflow:

- **`develop`** → Main branch for integrating PRs.
- **`staging`** → Testing branch, merged from `develop`.
- **`main`** → Stable production branch, merged from `staging`.

Please submit PRs to `develop`, not `main`.

## Commit Guidelines
- Keep the commit title (first line) concise and at or under **62 characters**.
- Detailed explanations, rationale, or bullet points should be placed in the commit body after a blank line.
- Enable pre-commit hooks locally with: `pre-commit install --hook-type pre-commit --hook-type commit-msg`

Thank you for your contributions!

