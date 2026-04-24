---
title: Personal GStack Radar Hub
type: synthesis
created: 2026-04-24
updated: 2026-04-24
status: starter
confidence: medium-high
---

# Personal GStack Radar Hub

## Compiled Truth

Radar Hub is the upstream discovery layer.
It does not publish directly. It routes signals into daily brief, research sidecar, long-running topic, watch queue, or suppression.

## Flow

```text
official radar
social radar
GitHub radar
skills radar
policy/capital radar
-> unified signal queue
-> dedupe and scoring
-> confirmation gate
-> triage router
```

## Route Labels

- `daily_brief_candidate`
- `research_brief_candidate`
- `long_running_topic_candidate`
- `watch_only`
- `suppress`

## Timeline

- 2026-04-24: Added starter hub connecting radars to AI Daily Brief and NotebookLM sidecar.

