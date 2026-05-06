---
updated: 2026-05-07
---
# Coding Standards
## Universal
- Favour small, pure functions
- Favour immutable data patterns
- No raw SQL — use parameterised queries or the project's ORM/DSL
- No domain entities in public API responses — map to a DTO
- Validate all public inputs before use
- No `console.log`/`System.out` in production — use the logging framework
- Never commit generated files or build artifacts
## Git
- Conventional Commits: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`
- Never amend pushed commits
- Never force push to main
