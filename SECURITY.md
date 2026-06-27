# Security Policy

## Supported Versions

This project is currently maintained for the active Streamlit application in the main repository.

| Version | Supported |
| --- | --- |
| Current main branch | Yes |
| Older FastAPI/Next.js prototypes | No |

## Responsible Disclosure

Please report suspected vulnerabilities privately. Do not publish exploit details, screenshots, database contents, API keys, or user data in public issues.

Good-faith security research is welcome when it avoids:

- Accessing data that is not yours.
- Disrupting service availability.
- Exfiltrating secrets or database files.
- Running destructive tests against deployed instances.

## Reporting Vulnerabilities

When reporting a vulnerability, include:

- A clear summary of the issue.
- Steps to reproduce.
- Expected and actual behavior.
- Affected files, pages, or environment settings.
- Potential impact.
- Suggested remediation, if known.

If this project is hosted in a private or educational environment, report vulnerabilities to the repository owner or maintainer directly.

## Security Best Practices

- Never commit `.env` files or real API keys.
- Use `OPENAI_API_KEY` and `GEMINI_API_KEY` only through environment variables or platform secrets.
- Keep `DATABASE_PATH` and `LOG_PATH` in writable but non-public locations.
- Do not expose SQLite database files through static hosting.
- Back up the database before deployment changes.
- Keep dependencies pinned in `requirements.txt`.
- Rebuild deployment images after dependency or security updates.
- Limit PDF upload size with `MAX_PDF_UPLOAD_MB`.
- Treat uploaded resumes as sensitive personal data.
- Review logs before sharing because they may include operational details.
- Use HTTPS and authentication for public deployments.

## Known Data Handling Notes

- The default app stores data locally in SQLite.
- Resume text, ATS history, recommendations, roadmaps, interview scores, and activities are persisted.
- Optional AI provider requests may send prompt content to OpenAI or Gemini when keys are configured.
- With no API keys, the app uses local rule-based fallback logic.
