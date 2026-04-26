---
name: personal-gstack
title: Personal GStack
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Clarify, plan, red-team, implement, verify, persist, operate, and retro durable work.
source_of_truth:
  - ../RESOLVER.md
  - ../../wiki/syntheses/personal-gstack-north-star.md
  - ../../wiki/syntheses/personal-gstack-completeness-map.md
  - ../../brain/skills/pgstack-upstream-parity-checklist.md
---

# Personal GStack

Use this skill for complex work that should improve PGStack rather than remain a
one-off answer.

## Modes

```text
clarify -> plan -> red-team -> implement -> verify -> persist
operate -> retro
```

## Contract

- Convert fuzzy work into explicit state, constraints, risks, and outputs.
- Prefer reusable operating improvements over isolated fixes.
- Keep Codex as workbench and Hermes as recurring runtime by default.
- Route durable knowledge through `brain-ops`.
- Preserve structural changes in wiki/brain and Git.
- Run the upstream parity checklist before claiming PGStack has aligned to,
  merged with, completed, or faithfully replicated original `gstack + gbrain`.

## Host Adapters

- Codex adapter: `$CODEX_HOME/skills/personal-gstack/SKILL.md`
- Hermes adapter: future thin mirror

The repo-level skill is the source-of-truth contract. Host adapters execute it.
