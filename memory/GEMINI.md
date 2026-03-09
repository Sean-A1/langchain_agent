
---

## `memory/GEMINI.md`

```md
# GEMINI.md

## Role
Gemini CLI is used as a coding agent for this repository inside WSL.

It should follow the same operational model as the other coding agents:
- work from WSL
- use isolated branches
- make focused changes
- avoid unnecessary refactors
- respect application/runtime env separation

## Current target state
Gemini CLI is planned to be set up after Codex CLI.

Target policy:
- install and run inside WSL
- use subscription/login-based CLI flow where applicable
- do not use project API keys for routine coding-agent login
- follow the same repository workflow as Claude and Codex

## Branch policy
Use:
- `gemini/<task-name>`

Standard start sequence:
```bash
cd ~/projects/langchain_agent

git status
git checkout main
git pull
git checkout -b gemini/<task-name>

git branch --show-current
git status