# MEMORY.md

## Project overview

This repository is a LangChain-based local development project running inside WSL.
The main goal is to build and maintain a RAG-oriented CLI/application workflow while using multiple coding agents safely and consistently.

This repo is developed primarily in WSL, with Cursor connected through WSL Remote.
Coding agents are used from inside WSL and operate on isolated git branches.

## Repository structure

Key paths:

- `main.py`
  - top-level entrypoint candidate
- `src/app/cli.py`
  - CLI entrypoint
- `src/rag/`
  - RAG-related modules
  - `config.py`
  - `ingest.py`
  - `loaders.py`
  - `prompts.py`
  - `query.py`
  - `utils.py`
- `tests/test_smoke.py`
  - minimum smoke test
- `.env`
  - local runtime environment variables
- `.env.example`
  - environment variable template
- `memory/`
  - persistent project memory and workflow docs

## Core operating principles

### 1. WSL-first development

All CLI agent work is expected to run inside WSL.

Typical working directory:
`~/projects/langchain_agent`

### 2. Agent branch isolation

Each coding agent must work on its own branch namespace.

Examples:

- `claude/<task-name>`
- `codex/<task-name>`
- `gemini/<task-name>`

No agent should work directly on `main`.

### 3. Subscription mode for coding agents

Coding agents are expected to run using their own subscription/login-based CLI mode where applicable.

The default policy is:

- CLI coding agents do **not** use API keys for normal coding tasks
- CLI coding agents do **not** rely on project `.env` authentication for their own agent login
- CLI coding agents are used as coding assistants, not as API clients inside this repo

### 4. API usage separation

OpenAI API usage is reserved for application/runtime tasks such as:

- RAG chains
- eval workflows
- code paths that explicitly require API access
- document/query pipelines that are part of the app itself

To make this separation explicit, the OpenAI API variable is intentionally named:

`RAG_OPENAI_API_KEY`

This variable exists to support repo/application logic, not agent CLI login.

### 5. No API mode mixing

Avoid mixing these two modes:

- agent CLI subscription mode
- repo/application API mode

That means:

- do not casually export `OPENAI_API_KEY` for agent CLI usage
- do not rename `RAG_OPENAI_API_KEY` back to `OPENAI_API_KEY` without an explicit reason
- do not blur the distinction between "tooling authentication" and "application runtime authentication"

### 6. Minimal and targeted edits

Agents should prefer small, focused edits.
Avoid broad refactors unless the task explicitly requires them.

### 7. Protect local secrets

Never commit secrets.
Be careful with:

- `.env`
- shell profile files
- tokens or login artifacts
- copied terminal outputs containing credentials

## Current status

As of the latest update:

Completed:

1. WSL setup, Node/npm install
2. Git setup
3. Repo clone into WSL home
4. Per-agent branch separation
5. Cursor WSL Remote setup mostly prepared
6. API mode separation policy defined
7. `RAG_OPENAI_API_KEY` policy applied in code/docs
8. Claude Code CLI setup completed and tested on small tasks

In progress / planned:
9. Codex CLI setup in WSL
10. Gemini CLI setup in WSL

## Claude status

Claude Code CLI has already been set up and tested with a few practical tasks such as scaffolding-related work and fixing deprecated warnings.
Claude branch separation is already in use.

## Codex and Gemini target state

Codex CLI and Gemini CLI should follow the same high-level principles as Claude:

- install in WSL
- use subscription/login mode where applicable
- avoid using project API keys for agent login
- follow isolated branch workflow
- optionally read agent-specific memory docs before work

## Editing rules for all agents

Before making changes, understand the local context first.

Preferred order:

1. inspect repo status
2. inspect current branch
3. move to `main`
4. pull latest changes
5. create a fresh agent branch
6. inspect relevant files
7. make minimal changes
8. run the smallest relevant validation
9. review diff before commit

## Validation guidance

Prefer the smallest relevant validation first.

Examples:

- smoke tests
- targeted test file
- CLI help/output check
- import check
- minimal run path verification

Do not introduce unrelated changes just because they look improvable.

## What to preserve

The following must be preserved unless explicitly changed by the user:

- WSL-first workflow
- agent-specific branch isolation
- subscription-mode preference for coding agents
- `RAG_OPENAI_API_KEY` naming and separation intent
- minimal-change philosophy
- no direct work on `main`

## If context is unclear

When starting work, agents should consult:

- `memory/MEMORY.md`
- `memory/WORKFLOW.md`
- their own agent-specific memory file

## Notes

This file is the shared long-term project memory.
Agent-specific behavior should be placed in separate files:

- `memory/CLAUDE.md`
- `memory/CODEX.md`
- `memory/GEMINI.md`