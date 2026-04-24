---
title: AI Daily Brief Pipeline
type: pipeline
created: 2026-04-24
updated: 2026-04-24
status: starter
confidence: medium-high
scope: local_pgstack
source_of_truth:
  - ../../jobs/ai-daily-brief.md
---

# AI Daily Brief Pipeline

## Compiled Truth

The daily brief converts confirmed AI signals into one concise daily report and one compact delivery digest.

## Current State

The starter pipeline is installed but not enabled until the owner configures sources and delivery.

## Current Open Threads

- Connect the owner's chosen delivery channel.
- Decide whether to enable social and GitHub radar sidecars.

## Source Of Truth

- [[../../jobs/ai-daily-brief|AI Daily Brief Job]]

## Typed Edges

- implements: [[../../jobs/ai-daily-brief|AI Daily Brief Job]]
- depends_on: [[radar-hub|Radar Hub Pipeline]]
- promotes_to: [[notebooklm-research-sidecar|NotebookLM Research Sidecar Pipeline]]

## Timeline

- 2026-04-24: Added starter pipeline mirror.

