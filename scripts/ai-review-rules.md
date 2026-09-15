# AI Review Rules

## Python

- Follow PEP 8.
- Prefer type hints where they improve readability.
- Avoid unnecessary duplication.
- Don't use bare `except`.
- Prefer clear and readable code over clever solutions.

## Pytest

- Fixtures should have an appropriate scope.
- Tests should be independent.
- Avoid test ordering dependencies.
- Assertions should verify meaningful behavior.
- Avoid unnecessary parametrization or abstraction.

## UI Automation

- Avoid arbitrary `sleep()`.
- Prefer explicit waits.
- Prefer stable selectors.
- Avoid duplicated page interaction logic.
- Reuse Page Objects/helpers when the same interaction appears repeatedly.

## API Tests

- Validate HTTP status codes.
- Validate response body where appropriate.
- Validate important business rules.
- Avoid duplicating request-building logic.

## General

- Don't report minor stylistic issues.
- Prioritize real bugs, flaky tests, incorrect assertions and maintainability problems.
- Don't suggest changes without explaining why.
- Don't invent requirements that aren't stated in these rules.
- Don't require architectural changes for a small isolated piece of code.
- Only comment on changed lines in the PR.