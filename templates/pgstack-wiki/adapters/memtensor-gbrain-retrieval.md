---
title: MemTensor as GBrain Retrieval Adapter
type: adapter
created: 2026-04-26
updated: 2026-04-26
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - memtensor.md
  - ../brain/skills/pgstack-gbrain-compatibility-layer.md
---

# MemTensor as GBrain Retrieval Adapter

## Compiled Truth

MemTensor may replace or augment GBrain's vector retrieval and team-sharing
subsystem for PGStack, but it must not become a second canonical brain.

Logical ownership:

```text
GBrain / PGBrain = brain repo + schema + skillpack + graph/timeline + jobs + operating protocol
MemTensor = retrieval delegate + compact continuity memory + governed team-sharing fabric
```

This is an infrastructure substitution, not a replacement for the original
GBrain operating contract.

## What Stays Native GBrain

- canonical Markdown brain repo
- MECE filing resolver
- page schema and two-layer knowledge objects
- skills resolver and thick skills
- brain-first operating protocol
- graph and timeline model
- jobs/minions
- GBrain MCP surface when configured
- maintenance cycle and doctor checks
- source/citation discipline

## What MemTensor May Replace

- semantic recall over compact memory objects
- cross-session continuity recall
- team-memory sharing through governed `team_candidate` / `team_shared`
- semantic retrieval delegation when the GBrain embedding layer is intentionally
  replaced by MemTensor
- compact write-through pointers from durable brain/wiki updates

It does not replace source-of-truth pages.

## Query Contract

An adapter should expose this conceptual contract:

```text
brain_lookup(query, scope, freshness, max_results)
```

Resolution order:

1. Query the configured GBrain Remote MCP / PGBrain first.
2. Query MemTensor only when the task explicitly needs TeamHub or continuity
   context.
3. Keep results separated by source authority.
4. Return answer candidates and source pointers with the boundary visible.

MemTensor hits are context, not canonical truth. A MemTensor result that changes
behavior must point back to a durable source: brain page, wiki page, repo
artifact, runbook, or verified external source.

## Included Commands

The starter kit includes a Remote MCP health check:

```bash
node engine/gbrain_remote_mcp_health.mjs
node engine/gbrain_remote_mcp_health.mjs --require-config
python3 engine/pgbrain_engine.py maintenance --remote-mcp-smoke
```

The commands require explicit environment configuration before they contact a
remote host:

```bash
export PGSTACK_GBRAIN_REMOTE_MCP_URL="https://your-host/gbrain/mcp"
export PGSTACK_GBRAIN_REMOTE_MCP_TOKEN="..."
```

If the target is not configured, `gbrain_remote_mcp_health.mjs` returns `SKIP` by
default so local-only nodes still pass their base smoke tests.

## Failure Modes

| Failure | Symptom | Rule |
|---|---|---|
| Dual center | agents treat memory as source of truth | require source-of-truth path |
| Local-center drift | local test state overrides configured production brain | make target explicit |
| Stale memory wins | old memory overrides newer page | prefer newer sourced brain/wiki |
| Raw-vector mismatch | adapter tries to store incompatible vectors in GBrain DB | forbidden without migration |
| Team hub pollution | raw chat or personal config enters team memory | apply team-memory gate |

## Typed Edges

- depends_on: [[memtensor|MemTensor Adapter]]
- depends_on: [[../brain/skills/pgstack-gbrain-compatibility-layer|PGStack GBrain Compatibility Layer]]
- reads_from: [[../brain/memory/team-hub-sharing|Team Hub Sharing]]

---

## Timeline

- 2026-04-26: Added to PGStack Agent Kit as the documented boundary for using
  MemTensor beside GBrain without creating a second center.
