---
name: testing
title: PGStack Testing
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Validate the shared kernel, skillpack, and PGBrain engine.
source_of_truth:
  - ../RESOLVER.md
  - ../../engine/README.md
  - ../../engine/pgbrain_engine.py
---

# PGStack Testing

Use this skill before calling a shared-kernel change complete.

## Contract

Shared-kernel changes are complete only after the relevant deterministic checks
pass and any remaining gaps are named.

## Checks

```bash
python3 engine/skillpack_check.py
python3 engine/pgbrain_engine.py validate
python3 engine/pgbrain_engine.py doctor
git status --short
```

For pipeline changes, add the pipeline's own dry-run or graduation checks.

## Rule

Verification should prove the contract still works, not merely that files exist.
