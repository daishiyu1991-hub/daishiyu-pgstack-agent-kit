---
title: PGStack PGBrain Shared Kernel Architecture
type: skill
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../../AGENTS.md
  - ../schema.md
---

# PGStack PGBrain Shared Kernel Architecture

## Compiled Truth

A `PGStack Node` uses one shared kernel with two named surfaces:

- `PGStack`: workflow, action, task progression, and pipeline operation
- `PGBrain`: durable knowledge, schema, relationships, memory discipline, and maintenance

The split is conceptual, not two disconnected repos by default.

## Current State

The shared kernel contains:

- `AGENTS.md`
- `brain/`
- `engine/`
- `jobs/`
- `skills/`
- `adapters/`
- `wiki/`

## Current Open Threads

- Decide when a team is large enough to split a separate brain repository.
- Keep the starter kit small until repeated use proves the need for heavier infrastructure.

## Source Of Truth

- [[../schema|PGStack Brain Schema]]
- [[../../wiki/syntheses/personal-gstack-foundation-v1-plan|Personal GStack Foundation v1 Plan]]

## Timeline

- 2026-04-24: Added starter architecture object for portable PGStack Agent Kit.

