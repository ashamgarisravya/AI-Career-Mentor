# Feature Specification: Backend Health Response

## Summary

The backend should expose a simple root endpoint that confirms the AI Career Mentor API is running.

## Goals

- Provide a quick health signal for local development.
- Give CI a stable endpoint behavior to test.

## Non-Goals

- This feature does not replace a production readiness probe.
- This feature does not expose dependency health details.

## User Stories

- As a developer, I want to request the root endpoint so that I can verify the backend starts correctly.
- As a CI pipeline, I want a deterministic response so that tests can catch accidental API regressions.

## Functional Requirements

- The root endpoint must respond to `GET /`.
- The response must use HTTP 200.
- The response body must be JSON with the message `AI Career Mentor Backend Running`.

## Acceptance Criteria

- Given the backend application is loaded, when `GET /` is requested, then the response status is 200.
- Given the backend application is loaded, when `GET /` is requested, then the response JSON matches the documented message.

## Security and Privacy

The endpoint must not expose secrets, user data, environment variables, hostnames, tokens, or stack traces.

## Test Plan

- Add a pytest test using FastAPI `TestClient`.
- Assert the status code and JSON response.
