---
title: Radar Hub Pipeline
type: pipeline
created: 2026-04-24
updated: 2026-04-24
status: starter
confidence: medium
scope: local_pgstack
source_of_truth:
  - ../../jobs/radar-hub.md
---

# Radar Hub Pipeline

## Compiled Truth

Radar Hub normalizes multiple discovery streams into one signal queue and one routing decision.

## Current State

Starter radars:

- official-source radar
- social radar
- GitHub radar
- skills radar
- policy/capital radar

## Current Open Threads

- Decide which radars are stable enough for unattended capture.

## Source Of Truth

- [[../../jobs/radar-hub|Radar Hub Job]]

## Typed Edges

- implements: [[../../jobs/radar-hub|Radar Hub Job]]
- promotes_to: [[ai-daily-brief|AI Daily Brief Pipeline]]

## Timeline

- 2026-04-24: Added starter radar pipeline mirror.

