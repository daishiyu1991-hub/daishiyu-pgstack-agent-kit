---
title: PGBrain Engine v1
type: skill
created: 2026-04-24
updated: 2026-04-26
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../../engine/README.md
  - ../../engine/pgbrain_engine.py
  - pgstack-pgbrain-shared-kernel-architecture.md
  - ../../wiki/syntheses/personal-gstack-foundation-v1-plan.md
---

# PGBrain Engine v1

## Compiled Truth

`PGBrain Engine v1` is the current deterministic local engine for the PGStack
shared kernel.

It remains file-backed and local-first, but it now does more than simple
index/query/validate:

- `doctor`
- link validation
- source discipline checks
- deeper job-spec validation
- typed-edge extraction
- relationship query with `related`
- maintenance report

It is still not a database, vector store, or full graph runtime.

## Current State

Engine path:

```text
engine/pgbrain_engine.py
```

Commands:

- `status`
- `index`
- `query`
- `related`
- `validate`
- `doctor`
- `maintenance`
- `gbrain_remote_mcp_health.mjs` for formal cloud GBrain Remote MCP smoke

Current successful doctor state:

- required kernel paths: ok
- docs indexed: `144`
- typed edges: `28`
- smoke query: `AI Daily Brief Job` ok
- smoke query: `Personal GStack Foundation v1 Plan` ok
- validation: `0 errors`, `0 warnings`

## Current Open Threads

- decide whether maintenance output should become a dated report artifact
- decide whether typed edges need a SQLite/PGLite backing store after more jobs
- add explicit tests if the engine grows beyond this single-file shape
- decide whether Remote MCP write smoke should run only after material changes
  or also in scheduled maintenance

## Source Of Truth

- [[../../engine/README|PGBrain Engine]]
- [[pgstack-pgbrain-shared-kernel-architecture|Shared Kernel Architecture]]
- [[../../wiki/syntheses/personal-gstack-foundation-v1-plan|Foundation v1 Plan]]

---

## Timeline

- 2026-04-24: v0 introduced local status, index, query, and validation.
- 2026-04-24: v1 added doctor, maintenance report, link/source checks, typed edges, relationship query, and deeper job validation.
- 2026-04-26: Replaced the transitional central bridge with the formal
  `gbrain-remote` MCP route and `gbrain_remote_mcp_health.mjs` maintenance
  smoke.
