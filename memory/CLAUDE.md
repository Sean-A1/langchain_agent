
---

## `memory/CLAUDE.md`

```md
# CLAUDE.md

## Role
Claude Code CLI is used as a coding agent for this repository inside WSL.

Its main purpose is to help with:
- small implementation tasks
- warning cleanup
- scaffolding improvements
- targeted refactors
- docs and workflow support
- safe code inspection and incremental edits

## Current status
Claude Code CLI setup is already complete.
It has already been used for practical tasks in this repository.

## Environment assumptions
- run inside WSL
- start from `~/projects/langchain_agent`
- use isolated Claude branches
- do not work directly on `main`

## Branch policy
Use:
- `claude/<task-name>`

Start from `main`, pull latest changes, then create a new Claude branch.

## Authentication policy
Claude CLI should use its own supported login/subscription flow where applicable.

Do not use project API keys as a substitute for agent login.

## API separation reminder
This repository intentionally separates:

- coding agent CLI usage
- application/runtime API usage

The variable `RAG_OPENAI_API_KEY` belongs to app/runtime workflows such as RAG and eval.
It is not a general-purpose agent CLI login variable.

## Editing preferences
Claude should:
- prefer focused changes
- avoid unrelated cleanup
- preserve existing architecture unless the task requires changes
- keep the user’s operating policies intact
- avoid renaming important env variables casually

## Repo context summary
Key paths:
- `main.py`
- `src/app/cli.py`
- `src/rag/`
- `tests/test_smoke.py`
- `memory/`

## Practical guidance
Before major edits:
1. inspect current branch and git status
2. confirm task scope
3. inspect the minimal relevant files
4. make targeted edits
5. run the smallest relevant validation
6. review diff

## Good Claude tasks
Examples:
- fix deprecated warnings
- tighten CLI behavior
- improve small docs
- patch failing smoke tests
- clean up narrow code paths
- improve prompts/config readability without broad rewrites

## Things Claude should avoid
- large speculative refactors
- mixing authentication modes
- modifying `.env` policy without explicit instruction
- introducing unrelated dependency churn
- making widespread formatting-only changes unless requested

## Persistent memory usage
If Claude supports persistent/local memory features, use them to reinforce:
- WSL-first workflow
- branch isolation
- API vs CLI separation
- minimal-diff editing
- `RAG_OPENAI_API_KEY` naming intent

But the repo’s source-of-truth documentation should remain inside:
- `memory/MEMORY.md`
- `memory/WORKFLOW.md`
- `memory/CLAUDE.md`