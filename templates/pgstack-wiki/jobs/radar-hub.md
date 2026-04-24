---
title: Radar Hub Job
type: job
created: 2026-04-24
updated: 2026-04-24
status: starter
confidence: medium
scope: local_pgstack
job_id: radar-hub
runtime_host: Hermes
schedule: Before daily brief or on demand
source_of_truth:
  - ../wiki/syntheses/personal-gstack-radar-hub.md
---

# Radar Hub Job

## Compiled Truth

`Radar Hub` is the shared discovery and routing layer that feeds daily brief, research brief, and long-running topic pipelines.

## Job Contract

Normalize multiple radars into one signal queue.

## Trigger

- Suggested cadence: before the daily brief.
- Manual trigger is acceptable for early installs.

## Inputs

- Watchlists from official, social, GitHub, skills, and policy/capital radars.
- Local config paths under `$PGSTACK_HOME/config/` or Hermes skill scripts.

## Outputs

- Signal queue: `$HOME/.hermes/state/pgstack-radar/latest_signals.json`
- Promoted candidates for the daily brief and research sidecars.

## Runtime Contract

Hermes can run deterministic radar collection. Codex owns scoring and routing policy.

## State

- State path: `$HOME/.hermes/state/pgstack-radar/`
- Queue files should be compact JSON, not raw page archives.

## Evidence

- A healthy run produces a small signal queue with clear route labels.
- Evidence path: `$HOME/.hermes/state/pgstack-radar/latest_signals.json`.

## Failure Behavior

If a radar source fails, keep the previous state and mark the source as unavailable.

## Persistence Rule

Persist only routed candidates, suppressed duplicate counts, and durable scoring changes.

## Verification

Run:

```bash
python3 engine/pgbrain_engine.py query "Radar Hub Job"
python3 engine/pgbrain_engine.py doctor
```

## Typed Edges

- implements: [[../wiki/syntheses/personal-gstack-radar-hub|Personal GStack Radar Hub]]
- runs_on: [[../adapters/hermes|Hermes Adapter]]
- writes_to: [[../brain/pipelines/radar-hub|Radar Hub Pipeline]]
- promotes_to: [[ai-daily-brief|AI Daily Brief Job]]

## Timeline

- 2026-04-24: Added starter job spec for the unified radar layer.
