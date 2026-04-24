---
title: PGStack Brain Schema
type: source
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../AGENTS.md
---

# PGStack Brain Schema

## Domain

The brain contains durable operating knowledge for:

- business
- AI knowledge
- skills
- pipelines
- agents
- memory systems
- runbooks
- sources

## Required Page Shape

```yaml
---
title: Page Title
type: business | ai_knowledge | skill | pipeline | agent | entity | memory | runbook | source | inbox | archive
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active | candidate | draft | archived
confidence: low | medium | medium-high | high
scope: local_pgstack | team_candidate | team_shared | personal
source_of_truth:
  - path-or-url
---
```

## Two-Layer Knowledge Objects

Use this shape for evolving durable objects:

```markdown
## Compiled Truth

Current synthesis.

## Current State

Current operating details.

## Current Open Threads

Unresolved items.

## Source Of Truth

Links and paths.

---

## Timeline

- YYYY-MM-DD: What changed and why.
```

## Typed Edges

Allowed edge vocabulary:

- `implements`
- `depends_on`
- `owned_by`
- `runs_on`
- `writes_to`
- `reads_from`
- `delivers_to`
- `validated_by`
- `promotes_to`
- `supersedes`
- `persists_to`
