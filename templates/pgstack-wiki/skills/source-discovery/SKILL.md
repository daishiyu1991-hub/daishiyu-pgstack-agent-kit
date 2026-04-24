---
name: source-discovery
title: PGStack Source Discovery
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Expand and test information sources through review-only source gates.
source_of_truth:
  - ../RESOLVER.md
  - ../../jobs/source-discovery.md
  - ../../brain/pipelines/source-discovery.md
  - ../../engine/source_discovery.py
  - ../../engine/source_gate_dry_run.py
---

# PGStack Source Discovery

Use this skill to propose new AI intelligence sources without directly mutating
production configs.

## Contract

```text
discover candidate -> source-gate dry run -> Radar Hub -> quality review -> human/agent decision
```

## Rules

- Proposed sources are review-only until accepted.
- Prefer official and primary sources.
- Do not mutate production `sources.json` automatically.
- Record why a source should be added, watched, or rejected.

## Commands

```bash
python3 engine/source_discovery.py --timeout 6
python3 engine/source_gate_dry_run.py --candidate "<source name>" --window-hours 168
```
