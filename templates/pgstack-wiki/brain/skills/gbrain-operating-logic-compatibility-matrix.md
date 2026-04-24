---
title: GBrain Operating Logic Compatibility Matrix
type: skill
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: medium-high
scope: local_pgstack
source_of_truth:
  - pgstack-pgbrain-shared-kernel-architecture.md
---

# GBrain Operating Logic Compatibility Matrix

## Compiled Truth

PGStack borrows the useful operating logic from `gbrain` without requiring every install to start as a heavy graph system.

Adopt:

- compiled truth
- timeline
- brain-first lookup
- write-time validation
- maintenance cycle
- fail-improve loop

Delay:

- full graph runtime
- heavy retrieval stack
- entity enrichment infrastructure

## Current State

The starter kit includes the light kernel and leaves heavier layers as future upgrades.

## Current Open Threads

- Revisit advanced graph runtime only after multiple mature pipelines need typed relationship depth beyond the current engine.

## Source Of Truth

- [[pgstack-pgbrain-shared-kernel-architecture|PGStack PGBrain Shared Kernel Architecture]]
- [[pgbrain-engine-v1|PGBrain Engine v1]]

## Timeline

- 2026-04-24: Added compatibility matrix as a conservative adoption guide.

