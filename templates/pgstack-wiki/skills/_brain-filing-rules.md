---
title: PGStack Brain Filing Rules
type: convention
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../brain/RESOLVER.md
  - ../brain/schema.md
---

# PGStack Brain Filing Rules

Use `brain/RESOLVER.md` before creating durable brain objects.

## Primary Homes

- `brain/business/`: durable business, strategy, market, customer knowledge.
- `brain/ai-knowledge/`: reusable AI knowledge, papers, tools, model behavior.
- `brain/skills/`: reusable workflows, rules, protocols, gates, templates.
- `brain/pipelines/`: recurring workflows with cadence, state, inputs, outputs.
- `brain/agents/`: agent roles and responsibility boundaries.
- `brain/entities/`: stable referenced systems, tools, people, orgs, surfaces.
- `brain/memory/`: memory transport, MemTensor, scope, promotion rules.
- `brain/runbooks/`: operational recovery and rerouted incidents.
- `brain/sources/`: source maps, repos, evidence bundles, raw-source pointers.
- `brain/inbox/`: durable but unclassified objects.
- `brain/archive/`: superseded or historical objects.

## Rule

One primary home. Cross-link freely. Do not duplicate the same object across
multiple directories.
