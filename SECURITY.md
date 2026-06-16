<<<<<<< HEAD
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

### How to Report

1. Do not disclose the vulnerability publicly.
2. Create a private report describing:
   - Vulnerability details
   - Steps to reproduce
   - Potential impact
3. Contact the project maintainer.

### Response Process

- Reports will be acknowledged within 7 days.
- Valid vulnerabilities will be investigated promptly.
- Security fixes will be released as soon as possible.

Thank you for helping keep this project secure.
=======
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
>>>>>>> 7a22386f (chore: add compliance tooling and documentation)
