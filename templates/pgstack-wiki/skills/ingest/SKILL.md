---
name: ingest
title: PGStack Ingest
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Route source material into raw, wiki, brain, state, or runbook surfaces.
source_of_truth:
  - ../RESOLVER.md
  - ../../AGENTS.md
  - ../../brain/RESOLVER.md
---

# PGStack Ingest

Use this skill when new source material should enter PGStack.

## Routing

- Immutable source material -> `raw/sources/`
- Source summary and attribution -> `wiki/sources/`
- Durable MECE object -> `brain/`
- Runtime state/output -> host state directory, then pointer in wiki/brain
- Recovery procedure -> `wiki/runbooks/` or `brain/runbooks/`

## Protocol

```text
preserve source -> classify -> brain-first lookup -> enrich or opt out -> write -> link -> log
```

If the material is transient, do not force it into the durable system.
