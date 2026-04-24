---
name: query
title: PGBrain Query
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Answer from PGBrain and the local wiki using brain-first lookup.
source_of_truth:
  - ../RESOLVER.md
  - ../conventions/brain-first.md
  - ../../engine/README.md
---

# PGBrain Query

Use this skill when the user asks what PGStack knows, how systems relate, or
where durable context lives.

## Protocol

1. Run targeted `PGBrain Engine` query when local context is needed.
2. Read the matching canonical pages.
3. Answer from current `Compiled Truth` first.
4. Use `Timeline` only to explain how the state evolved.
5. Say when an answer is memory-derived or stale.

## Commands

```bash
python3 engine/pgbrain_engine.py query "<question>"
python3 engine/pgbrain_engine.py related "<object>"
```
