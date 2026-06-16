<<<<<<< HEAD
# Contributing to AI Career Mentor

Thank you for your interest in contributing to AI Career Mentor.

## Getting Started

1. Fork the repository.
2. Clone your fork locally.
3. Create a new branch for your feature or bug fix.
4. Make your changes and test them.
5. Commit your changes with clear commit messages.
6. Push your branch and create a Pull Request.

## Coding Standards

* Follow Python best practices.
* Write clear and maintainable code.
* Add comments where necessary.
* Ensure all features are tested before submission.

## Reporting Issues

If you find a bug or have a feature request, please create an issue describing the problem and proposed solution.

## Pull Requests

All pull requests will be reviewed before being merged into the main branch.

Thank you for helping improve AI Career Mentor.
=======
# Contributing

Thank you for contributing to AI Career Mentor. This project values small, focused changes that are easy to review and safe to ship.

## Development Workflow

1. Create a branch from `main`.
2. Install runtime and development dependencies.
3. Make a focused change with tests or documentation updates.
4. Run the local quality checks before opening a merge request.
5. Keep merge requests concise and explain the reason for the change.

## Local Setup

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

## Required Checks

```bash
ruff check .
ruff format --check .
mypy .
pytest --cov=. --cov-fail-under=80
bandit -r .
pip-audit
```

## Code Style

- Use typed Python for new code.
- Prefer clear names and small functions.
- Keep public behavior covered by tests.
- Do not commit generated files, local caches, virtual environments, secrets, or build artifacts.

## Commit Messages

Use short imperative commit messages, for example:

```text
feat: add career recommendation endpoint
fix: validate empty resume uploads
chore: update compliance tooling
```

## Security

Never include credentials, tokens, API keys, private certificates, or production data in commits. Report vulnerabilities using the process in `SECURITY.md`.
>>>>>>> 7a22386f (chore: add compliance tooling and documentation)
