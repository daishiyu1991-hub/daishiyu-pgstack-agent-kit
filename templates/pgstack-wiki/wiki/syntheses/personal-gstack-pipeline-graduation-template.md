---
title: Personal GStack Pipeline Graduation Template
type: synthesis
created: 2026-04-24
updated: 2026-04-24
status: starter
confidence: medium-high
scope: local_pgstack
source_of_truth:
  - ../../jobs/RESOLVER.md
  - ../../brain/pipelines/README.md
---

# Personal GStack Pipeline Graduation Template

## Compiled Truth

A PGStack pipeline should not be called `graduated-v1` until it passes a staged
verification ladder.

This starter template exists so the repo-level skill resolver has a stable local
pointer without importing one person's private validation history.

## Graduation Ladder

1. Level 1: deterministic dry-run with no production side effects.
2. Level 2: report generation or durable artifact generation.
3. Level 3: controlled delivery test with explicit human approval.
4. Level 4: unattended scheduled run with state, evidence, and recovery path.

## Required Evidence

- job spec in `jobs/`
- pipeline object in `brain/pipelines/`
- state path
- evidence path
- failure behavior
- human review boundary
- `PGBrain doctor` result

## Current Open Threads

- Replace this starter page with the node owner's real pipeline graduation
  history after their first real pipeline passes Level 1-4.

## Timeline

- 2026-04-24: Added as a portable starter template for PGStack Agent Kit.
