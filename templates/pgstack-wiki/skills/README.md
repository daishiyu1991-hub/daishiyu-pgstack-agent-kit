---
title: PGStack Kernel Skills
type: resolver
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
---

# PGStack Kernel Skills

This directory is the shared-kernel skillpack.

It is the canonical behavior layer for `PGStack + PGBrain`.

Installed host skills under `.codex/skills`, Hermes runtime skills, and future
agent-host skills are adapters or mirrors. Durable skill behavior should be
authored here first, then synced outward when needed.

Start with:

- [[RESOLVER|PGStack Skill Resolver]]
- `manifest.json`

## Compiled Truth

`skills/` is now the repo-level equivalent of original `gbrain`'s skillpack:

```text
skills/RESOLVER.md -> skills/*/SKILL.md -> engine/jobs/brain/adapters
```

Agents should not treat the wiki as the only place where operating rules live.
If a rule changes how work is performed, route it through this skillpack.

## Current Rule

Host-specific skill files are adapters.

Shared-kernel skill routing belongs here.

Core always-on skills:

- `skills/signal-detector/SKILL.md`
- `skills/brain-ops/SKILL.md`

Core operation skills:

- `skills/personal-gstack/SKILL.md`
- `skills/llm-wiki/SKILL.md`
- `skills/ai-daily-brief/SKILL.md`
- `skills/query/SKILL.md`
- `skills/ingest/SKILL.md`
- `skills/enrich/SKILL.md`
- `skills/maintain/SKILL.md`
- `skills/repo-architecture/SKILL.md`
- `skills/agent-router/SKILL.md`
- `skills/minion-orchestrator/SKILL.md`
- `skills/source-discovery/SKILL.md`
- `skills/research-brief/SKILL.md`
- `skills/team-memory-writing/SKILL.md`
- `skills/team-memory-gate/SKILL.md`
- `skills/skillify/SKILL.md`
- `skills/testing/SKILL.md`

## Timeline

- 2026-04-24: Created as a resolver-only shared-kernel skill surface.
- 2026-04-24: Upgraded to a canonical repo-level skillpack modeled on
  original `gbrain`'s resolver plus thick skills pattern.
- 2026-04-26: Added `agent-router` for host ownership, MultiCA/ACP handoff,
  and agent-layer parity routing.
