---
title: AI Daily Brief Job
type: job
created: 2026-04-24
updated: 2026-04-24
status: starter
confidence: medium-high
scope: local_pgstack
job_id: ai-daily-brief
runtime_host: Hermes
schedule: Every day at 08:00 local time
source_of_truth:
  - ../skills/RESOLVER.md
  - ../wiki/syntheses/personal-gstack-pipeline-template-family.md
---

# AI Daily Brief Job

## Compiled Truth

`AI Daily Brief` is the reference daily-brief pipeline for a PGStack Node.
It should run through Hermes after the owner configures their own sources and delivery channel.

## Job Contract

Collect high-signal AI updates, dedupe them, explain why they matter, write a full Obsidian report, and return a compact delivery digest.

## Trigger

- Suggested cadence: daily at 08:00 local time.
- Manual dry-runs are allowed before enabling cron.

## Inputs

- Hermes runtime skill: `ai-daily-brief`
- Source config: `~/.hermes/skills/research/ai-daily-brief/scripts/sources.json`
- Social watchlist config: `~/.hermes/skills/research/ai-daily-brief/scripts/social_watchlist.json`

## Outputs

- Daily note path: `$HOME/Documents/PGStack/AI Daily Brief/YYYY/YYYY-MM-DD AI Daily Brief.md`
- Optional delivery digest through the owner's chosen channel.

## Runtime Contract

Hermes runs the recurring job. Codex edits source policy, templates, and quality gates.

## State

- Production state: `$HOME/.hermes/state/ai-daily-brief/last_success.json`
- Bundle state: `$HOME/.hermes/state/ai-daily-brief/latest_bundle.json`

## Evidence

- Doctor query should find this job.
- Dry-run report should write a note without updating production state.
- Evidence path: `$HOME/.hermes/state/ai-daily-brief/latest_bundle.json`.

## Failure Behavior

If source fetching fails, the job should write a partial report or no-op summary rather than fabricate items.
NotebookLM sidecar failure must not block the daily brief.

## Persistence Rule

Persist only the daily report, compact run state, and durable lessons. Do not persist raw noisy feeds.

## Verification

Run:

```bash
python3 engine/pgbrain_engine.py query "AI Daily Brief Job"
python3 engine/pgbrain_engine.py doctor
```

## Typed Edges

- implements: [[../wiki/syntheses/personal-gstack-pipeline-template-family|Pipeline Template Family]]
- runs_on: [[../adapters/hermes|Hermes Adapter]]
- writes_to: [[../brain/pipelines/ai-daily-brief|AI Daily Brief Pipeline]]
- promotes_to: [[notebooklm-research-sidecar|NotebookLM Research Sidecar Job]]

## Timeline

- 2026-04-24: Added starter job spec for portable PGStack Agent Kit.
