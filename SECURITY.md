# Security Policy

## Supported Versions

Security updates are provided for the `main` branch and the latest tagged release.

## Reporting a Vulnerability

Do not open public issues for suspected vulnerabilities. Report security issues privately to the repository maintainers with:

- A clear description of the issue.
- Steps to reproduce.
- Affected files, routes, or dependencies.
- Any known impact or exploitability.

Maintainers should acknowledge reports within 7 days and provide a remediation plan or status update when possible.

## Security Practices

- Secrets must be stored outside Git and represented only by placeholders in `.env.example`.
- Dependencies are scanned with `pip-audit`.
- Python code is scanned with Bandit.
- Secret patterns are scanned with Gitleaks.
