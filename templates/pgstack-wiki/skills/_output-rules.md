---
title: PGStack Output Rules
type: convention
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../AGENTS.md
  - conventions/quality.md
---

# PGStack Output Rules

## User-Facing Output

- Answer the active request first.
- Name what changed, what passed, and what remains open.
- Prefer concrete file paths and commands over abstract prose.
- Keep routine close-out concise.

## Durable Output

- Write durable structure to wiki/brain, not only chat.
- Update `wiki/index.md`, `wiki/log.md`, and relevant brain indexes after core changes.
- Use the configured cloud memory route for compact continuity when appropriate,
  or record `needs_cloud_memory_write`.
- Do not publish to team memory without gate and rewrite.
