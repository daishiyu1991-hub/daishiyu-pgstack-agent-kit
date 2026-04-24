---
name: repo-architecture
title: PGStack Repo Architecture
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Choose the correct PGStack/PGBrain filing surface.
source_of_truth:
  - ../RESOLVER.md
  - ../_brain-filing-rules.md
  - ../../brain/RESOLVER.md
  - ../../brain/skills/pgstack-pgbrain-shared-kernel-architecture.md
---

# PGStack Repo Architecture

Use this skill before adding new durable files or moving system boundaries.

## Contract

Every durable object should have one primary home and a clear adapter boundary.

## Filing Order

1. Is this behavior? Put it in `skills/`.
2. Is this recurring runtime? Put it in `jobs/` and `brain/pipelines/`.
3. Is this durable knowledge? Put it in `brain/` using `brain/RESOLVER.md`.
4. Is this human-readable compilation? Put it in `wiki/`.
5. Is this host glue? Put it in `adapters/`.
6. Is this deterministic local runtime? Put it in `engine/`.

## Rule

The shared kernel is:

```text
AGENTS.md + skills/ + engine/ + jobs/ + brain/ + adapters/
```

Do not make Codex or Hermes the identity of the core system.
