---
title: PGStack GBrain Compatibility Layer
type: skill
created: 2026-04-26
updated: 2026-04-26
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - gbrain-operating-logic-compatibility-matrix.md
  - pgstack-pgbrain-shared-kernel-architecture.md
  - ../../adapters/memtensor-gbrain-retrieval.md
---

# PGStack GBrain Compatibility Layer

## Compiled Truth

PGStack should align to original `gstack + gbrain` at the operating-contract
layer, while allowing explicitly documented infrastructure substitutions.

The compatibility rule is:

```text
copy the original operating contract
preserve GBrain ownership of durable brain structure
substitute only named subsystems through explicit adapters
prove every substitution with smoke tests
```

Strict vanilla alignment may be partial on a teammate node. Operating-contract
alignment should remain high.

## Native GStack / GBrain Contract

Keep these aligned with original `gstack + gbrain`:

- host-agnostic agent operating wrapper
- `AGENTS.md` as universal entry protocol
- repo-level `skills/RESOLVER.md`
- thick canonical skills and thin host adapters
- separate durable brain repo
- MECE resolver and schema discipline
- `Compiled Truth + Timeline` for evolving knowledge objects
- brain-first lookup before external research
- artifact chain from one workflow step to the next
- doctor, smoke, maintenance, and job/minion style health loops
- MCP surface for agent access when configured
- git-backed audit and recovery

## PGStack Extensions

These are intentional PGStack extensions beyond the upstream default:

- `PGStack Node`: one person's complete local system
- `PGStack Constellation`: multiple nodes connected through explicit contracts
- `Hermes` as unattended runtime host
- `Codex` as workbench and verifier host
- `MultiCA / AgentHost` as optional control and repair plane
- `Obsidian / llm-wiki` as human-readable compilation surface
- governed team-memory promotion
- `PGStack Agent Kit` as teammate install and distribution package

Extensions are allowed only when they map back to one of the original loops:

```text
workflow loop
artifact loop
verification loop
memory loop
```

## MemTensor Substitution

MemTensor may replace or augment only this part of GBrain:

- semantic recall when original embeddings are unavailable or intentionally
  delegated
- cross-session continuity memory
- compact write-through pointers
- governed team sharing through Team Hub
- retrieval fallback behind a central-brain adapter

MemTensor does not replace:

- brain repo
- resolver/schema
- source-of-truth pages
- skillpack
- graph/timeline model
- jobs/minions
- doctor and maintenance protocol
- GBrain MCP identity

## Agent Decision Gate

Before changing GBrain, MemTensor, central-brain lookup, Agent Kit packaging, or
unattended maintenance topology, ask:

1. Is this a native GStack/GBrain contract we should preserve?
2. Is this a PGStack extension that clearly improves multi-agent operation?
3. Is this a MemTensor substitution with a documented boundary?
4. Is there a smoke test proving the substitution still answers the original
   GBrain question?
5. Does the change create a second center, hidden owner route, or uncited memory
   authority?

If the answer to 5 is yes, stop and redesign.

## Read Path

Default read order for a configured central-brain node:

```text
1. Central Brain Host GBrain source-of-truth pages
2. Central Brain Host GBrain query/search/MCP
3. MemTensor retrieval delegate with explicit owner routing
4. local wiki or local GBrain only for workbench/reference checks
5. external research only when brain and memory are insufficient
```

Included adapter commands:

```text
engine/central_brain_lookup.py
engine/central_brain_health.py
engine/central_brain_mcp_server.mjs
```

## Write Path

Durable behavior changes should land in this order:

```text
1. canonical brain/wiki/source-of-truth page
2. index/log/current-priority surfaces
3. PGBrain validation or relevant smoke test
4. compact MemTensor pointer when configured
5. team promotion only through governance
```

Never write only to MemTensor when the object is a policy, skill, pipeline,
runbook, source map, architecture decision, or team-facing rule.

## Acceptance Tests

A compatibility change is accepted only when it can answer:

- Can an agent retrieve the current source-of-truth page?
- Can an agent get useful recall when GBrain embeddings are absent?
- Are MemTensor hits labeled as context rather than canonical truth?
- Is the intended production center explicit?
- Can the smoke test pass or skip safely without hand-picked local state?
- Is the relevant index/log surface updated?

## Forbidden Drift

Do not allow these patterns:

- treating MemTensor as a second canonical brain
- letting local reference state override the configured production brain
- changing GBrain schema just to fit a different embedding dimension without a
  migration gate
- storing raw chat or personal config as team knowledge
- creating host-specific skill behavior that bypasses repo-level skills
- enabling unattended cron/autopilot before the boundary and smoke test pass

## Typed Edges

- depends_on: [[gbrain-operating-logic-compatibility-matrix|GBrain Operating Logic Compatibility Matrix]]
- depends_on: [[pgstack-pgbrain-shared-kernel-architecture|PGStack PGBrain Shared Kernel Architecture]]
- depends_on: [[../../adapters/memtensor-gbrain-retrieval|MemTensor as GBrain Retrieval Adapter]]
- implements: [[../../skills/brain-ops/SKILL|PGStack Brain Ops]]
- depends_on: [[../../adapters/memtensor|MemTensor Adapter]]
- depends_on: [[../../engine/README|PGBrain Engine]]

## Current Open Threads

- Connect a real Central Brain Host only after the teammate approves SSH target
  and memory owner routing.
- Register the MCP bridge only when the local agent has a compatible MCP SDK.
- Enable scheduled central-brain maintenance only after smoke tests pass.

---

## Timeline

- 2026-04-26: Added to PGStack Agent Kit so installed nodes inherit the original
  GStack/GBrain alignment boundary before adding central-brain automation.
