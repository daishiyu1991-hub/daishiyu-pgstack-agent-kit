---
title: NotebookLM Research Sidecar Pipeline
type: pipeline
created: 2026-04-24
updated: 2026-04-24
status: candidate
confidence: medium
scope: local_pgstack
source_of_truth:
  - ../../jobs/notebooklm-research-sidecar.md
---

# NotebookLM Research Sidecar Pipeline

## Compiled Truth

NotebookLM research is a supervised second pass for confirmed topics that need deeper synthesis.

## Current State

The starter kit defines the sidecar, but leaves the actual NotebookLM tool choice to the node owner.

## Current Open Threads

- Test a chosen NotebookLM MCP or CLI in supervised mode.
- Avoid making NotebookLM a daily main-chain dependency until auth stability is proven.

## Source Of Truth

- [[../../jobs/notebooklm-research-sidecar|NotebookLM Research Sidecar Job]]

## Typed Edges

- depends_on: [[ai-daily-brief|AI Daily Brief Pipeline]]
- implements: [[../../jobs/notebooklm-research-sidecar|NotebookLM Research Sidecar Job]]

## Timeline

- 2026-04-24: Added starter sidecar pipeline mirror.

