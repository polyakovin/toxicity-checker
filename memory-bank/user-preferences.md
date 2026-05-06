---
updated: 2026-05-07
---
# User Preferences
Style, naming, libraries, and prohibitions.
## Communication
- Be concise — no preamble, no summaries after code
- Answer directly
- Use the language of the user's query
## Code Style
- Mimic existing code style, not personal preferences
- Read conventions before editing
- Edit surgically — prefer `edit` over `write`
- Never add comments unless the project style requires them
- Do not create documentation files unless explicitly asked
## Prohibited
- Never commit unless explicitly asked
- Never introduce secrets or credentials into code
- Never guess library versions — check the project's config files
- Never add a library without checking if it's already in the project
## Memory
- Proactively save deployment/infrastructure/setup details to project memory-bank without being asked
- After creating servers, configuring tools, deploying — update relevant memory files immediately
- Never wait for the user to ask «запомни это»
## Verification
- Run linter + typechecker before declaring done
- Run tests (at least the relevant subset)
