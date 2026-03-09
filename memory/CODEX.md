# CODEX.md

## Role
Codex CLI is used as a coding agent for this repository inside WSL.

Its intended role is similar to Claude:
- inspect code safely
- make targeted edits
- help with implementation tasks
- support docs and workflow improvements
- run small validations when appropriate

## Current target state
Codex CLI is planned to be installed and used inside WSL with the same broad operating model as other agents.

Target policy:
- WSL execution
- separate Codex branches
- subscription/login-based usage where applicable
- no reliance on project API keys for routine coding-agent work

## Branch policy
Use:
- `codex/<task-name>`

Always begin from `main`.

Recommended start routine:
```bash
cd ~/projects/langchain_agent

git status
git checkout main
git pull
git checkout -b codex/<task-name>

git branch --show-current
git status