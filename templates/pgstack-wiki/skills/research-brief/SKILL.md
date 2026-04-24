---
name: research-brief
title: PGStack Research Brief
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: medium-high
scope: local_pgstack
description: Convert enriched source packs into concise research briefs.
source_of_truth:
  - ../RESOLVER.md
  - ../../jobs/notebooklm-research-sidecar.md
  - ../../brain/pipelines/notebooklm-research-sidecar.md
  - ../../engine/source_pack_bundle.py
  - ../../engine/source_pack_enrich.py
---

# PGStack Research Brief

Use this skill when Radar Hub finds a signal that deserves deeper synthesis than
the daily brief.

## Contract

```text
quality-reviewed signal -> source pack -> bounded enrichment -> research brief candidate
```

NotebookLM is a supervised research window in v1. It is not an unattended
production dependency.

## Rules

- A source pack needs enough primary/source diversity before NotebookLM review.
- Keep source-pack artifacts in state and point to them from wiki/brain.
- Do not promote a research brief into operating truth until source support and
  relevance are clear.
