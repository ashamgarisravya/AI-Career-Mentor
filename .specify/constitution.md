# AI Career Mentor Constitution

## Purpose

AI Career Mentor exists to help users make informed career decisions through clear guidance, resume insights, skill-gap analysis, and learning roadmap planning.

## Product Principles

1. User guidance must be explainable and actionable.
2. Recommendations must avoid overclaiming certainty.
3. User-provided profile and resume information must be treated as sensitive.
4. Features should be specified before implementation when they affect user workflows.
5. Quality gates for tests, security, formatting, typing, and linting must remain active in CI.

## Engineering Principles

- Keep backend interfaces simple and typed.
- Prefer small, reviewable changes.
- Maintain documentation alongside behavior changes.
- Avoid committing generated artifacts, dependency folders, or secrets.

## Governance

Changes to product behavior should include an updated specification under `specs/`. Changes to this constitution should be reviewed with the same care as production code.
