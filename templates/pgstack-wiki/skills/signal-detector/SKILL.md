---
name: signal-detector
title: PGStack Signal Detector
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Detect durable inbound signal without blocking the main response.
source_of_truth:
  - ../RESOLVER.md
  - ../../AGENTS.md
  - ../../brain/skills/pgbrain-enrichment-protocol-v1.md
---

# PGStack Signal Detector

Always-on ambient signal capture for PGStack.

## Contract

Run on every substantive inbound message when the host can do so cheaply.

Capture:

- durable user preferences
- architecture decisions
- operating-rule changes
- verified outcomes
- blockers and recovery pointers
- reusable ideas, patterns, and skill candidates

Skip:

- acknowledgements
- phatic chatter
- repeated `go` turns unless they approve a durable transition
- raw transcripts that should be compacted first

## Output

No visible user output is required.

Write one compact internal capture only when the signal changes future behavior:

```text
Signals: <count> durable item(s), scope=<personal|local_pgstack|team_candidate>, action=<wiki|memory|none>
```

## Routing

- If the signal changes durable behavior, invoke `brain-ops`.
- If the signal should become a skill, invoke `skillify`.
- If the signal is team-reusable, invoke `team-memory-gate` before any team write.

## Anti-Patterns

- Blocking the main task to over-capture.
- Saving chat residue as team knowledge.
- Treating every user sentence as durable.
- Publishing raw user phrasing to team memory without rewrite and review.
