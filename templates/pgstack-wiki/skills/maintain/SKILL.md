---
name: maintain
title: PGStack Maintain
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Run lint, relink, promote, reroute, log, and doctor cycles.
source_of_truth:
  - ../RESOLVER.md
  - ../../wiki/syntheses/personal-gstack-maintenance-cycle-v1.md
  - ../../jobs/pgstack-maintenance.md
---

# PGStack Maintain

Use this skill for entropy reduction.

## Contract

Keep the shared kernel recoverable, linked, and low-noise.

## Cycle

```text
lint -> relink -> promote -> reroute -> log
```

## Checks

- Orphan pages and missing links.
- Core pages missing `Compiled Truth` or `Timeline`.
- Team-facing memory drift.
- Runbooks mixed into team-shared knowledge.
- Skillpack resolver/manifest drift.
- Job specs missing runtime/state/evidence pointers.

## Commands

```bash
python3 engine/pgbrain_engine.py maintenance
python3 engine/pgbrain_engine.py doctor
python3 engine/skillpack_check.py
```
