---
title: PGStack Skill Resolver
type: skill
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../AGENTS.md
  - ../brain/schema.md
---

# PGStack Skill Resolver

## Compiled Truth

Skills are the reusable behavior layer for a PGStack Node.

Codex skills are used for design, verification, and durable documentation.
Hermes skills are used for recurring runtime execution.

## Current State

Starter skills installed by the kit:

- `personal-gstack`
- `llm-wiki`
- `ai-daily-brief`
- `team-memory-writing`
- `team-memory-gate`

Runtime skills installed for Hermes:

- `ai-daily-brief`
- `team-kb-curator`

## Current Open Threads

- Decide which local tools are stable enough to become unattended runtime dependencies.
- Keep NotebookLM as a supervised sidecar until authentication and API stability are proven.

## Source Of Truth

- `skills/codex/` in the install kit
- `skills/hermes/` in the install kit

## Timeline

- 2026-04-24: Initialized the portable skill resolver for PGStack Agent Kit.

