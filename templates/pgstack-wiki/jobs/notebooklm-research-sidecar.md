---
title: NotebookLM Research Sidecar Job
type: job
created: 2026-04-24
updated: 2026-04-24
status: candidate
confidence: medium
scope: local_pgstack
job_id: notebooklm-research-sidecar
runtime_host: Manual
schedule: On demand after triage
source_of_truth:
  - ../adapters/notebooklm.md
  - ../wiki/syntheses/personal-gstack-radar-hub.md
---

# NotebookLM Research Sidecar Job

## Compiled Truth

NotebookLM is a supervised sidecar for confirmed high-value topics.
It is not a primary unattended collector.

## Job Contract

Turn a confirmed topic and source bundle into a research brief that can be written back to Obsidian and PGBrain.

## Trigger

- Trigger after daily brief triage.
- Use only for topics with strategic depth, multiple sources, or long-running relevance.

## Inputs

- Source bundle path: `$HOME/.hermes/state/ai-daily-brief/notebooklm-source-bundles/`
- Confirmed URLs, papers, model cards, docs, release notes, or official repo releases.

## Outputs

- Research note path: `$HOME/Documents/PGStack/AI Daily Brief/Research/YYYY/YYYY-MM-DD Topic Brief.md`
- Optional long-running topic candidate in `brain/ai-knowledge/` or `brain/pipelines/`.

## Runtime Contract

Manual or supervised agent run until NotebookLM auth and API behavior are proven stable.
Failure must not block the daily brief.

## State

- Sidecar state path: `$HOME/.hermes/state/notebooklm-research-sidecar/`
- Store bundle metadata and output pointers, not cookies or browser state.

## Evidence

- A successful run produces a research brief with confirmed sources and open questions.

## Failure Behavior

If NotebookLM auth fails, keep the source bundle and mark the sidecar as blocked.

## Persistence Rule

Persist the final research brief and durable conclusions. Do not persist raw NotebookLM chat dumps by default.

## Verification

Run:

```bash
python3 engine/pgbrain_engine.py query "NotebookLM Research Sidecar Job"
python3 engine/pgbrain_engine.py doctor
```

## Typed Edges

- depends_on: [[ai-daily-brief|AI Daily Brief Job]]
- runs_on: [[../adapters/notebooklm|NotebookLM Adapter]]
- writes_to: [[../brain/pipelines/notebooklm-research-sidecar|NotebookLM Research Sidecar Pipeline]]
- promotes_to: [[../brain/ai-knowledge/README|AI Knowledge]]

## Timeline

- 2026-04-24: Added as supervised research sidecar, not daily main-chain dependency.

