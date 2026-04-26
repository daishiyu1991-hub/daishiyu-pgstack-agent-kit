---
name: brain-ops
title: PGStack Brain Ops
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Enforce brain-first lookup, source discipline, and durable write-back.
source_of_truth:
  - ../RESOLVER.md
  - ../conventions/brain-first.md
  - ../../brain/schema.md
  - ../../brain/skills/pgbrain-enrichment-protocol-v1.md
  - ../../brain/skills/pgstack-gbrain-compatibility-layer.md
  - ../../brain/skills/pgstack-upstream-parity-checklist.md
  - ../../brain/agents/pgstack-agent-layer-stage35.md
---

# PGStack Brain Ops

The ambient knowledge layer for PGStack and PGBrain.

## Contract

Before changing durable rules or answering from project context:

1. Read the relevant repo-level skill.
2. Search PGBrain with `engine/pgbrain_engine.py query`.
3. Read the highest-value wiki/brain pages.
4. Use MemTensor as governed supporting memory.
5. Use external sources only when freshness or missing evidence requires it.

Before changing GBrain, MemTensor, GBrain Remote MCP, Agent Kit packaging,
or unattended maintenance topology, also read
`brain/skills/pgstack-gbrain-compatibility-layer.md`.

Before answering whether PGStack is aligned to, merged with, complete against,
or faithfully replicating upstream `gstack + gbrain`, also read
`brain/skills/pgstack-upstream-parity-checklist.md`. Check the agent layer
explicitly; do not infer it from Codex, Hermes, MultiCA, or MCP tools alone.

Before routing work across Codex, Hermes, MultiCA/ACP, AgentHost, jobs, or
minions, also read `skills/agent-router/SKILL.md`.

After durable work:

1. Update the canonical page.
2. Update index/log surfaces.
3. Run `PGBrain Engine` validation when shared-kernel behavior changed.
4. Write a compact local memory pointer when appropriate.

## Write Discipline

- Use `Compiled Truth + Timeline` for evolving core pages.
- Preserve source pointers for material claims.
- Keep team-memory writes gated and compact.
- Do not bulk-migrate `wiki/` into `brain/` without explicit request.

## Verification

For shared-kernel changes, run:

```bash
python3 engine/pgbrain_engine.py doctor
```

When skillpack files changed, also run:

```bash
python3 engine/skillpack_check.py
```
