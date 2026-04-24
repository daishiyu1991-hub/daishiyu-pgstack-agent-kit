---
title: PGBrain Engine v1
type: skill
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../../engine/pgbrain_engine.py
---

# PGBrain Engine v1

## Compiled Truth

`PGBrain Engine v1` is the deterministic local engine for the starter node.
It indexes Markdown, extracts typed edges, validates kernel structure, runs smoke queries, and prints maintenance reports.

## Current State

Commands:

```bash
python3 engine/pgbrain_engine.py doctor
python3 engine/pgbrain_engine.py query "AI Daily Brief Job"
python3 engine/pgbrain_engine.py related "AI Daily Brief Job"
python3 engine/pgbrain_engine.py maintenance
```

## Current Open Threads

- Keep the engine filesystem-backed until real pipeline use requires a heavier graph or retrieval layer.

## Source Of Truth

- [[../../engine/README|PGBrain Engine README]]

## Timeline

- 2026-04-24: Added engine object to the portable starter kernel.

