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
  - ../../wiki/syntheses/garrytan-gstack-readme-atomic-analysis.md
  - ../../wiki/syntheses/gstack-gbrain-vanilla-completion-gate-2026-04-26.md
  - ../../wiki/syntheses/gstack-gbrain-pgstack-skill-inventory-parity-matrix-2026-04-26.md
  - ../../wiki/syntheses/cloud-gstack-gbrain-native-first-replica-v1.md
---

# PGStack GBrain Compatibility Layer

## Compiled Truth

PGStack now follows a native-first compatibility rule:

```text
original GStack + original GBrain are the base operating system
PGStack additions are adapters or add-ons only
```

PGStack is aligned to original `gstack + gbrain` at the operating-contract
layer, and the cloud target is a faithful GStack/GBrain replica with only
bounded adapter substitutions.

The compatibility rule is:

```text
copy the original operating contract
preserve GBrain ownership of durable brain structure
substitute only named subsystems through explicit adapters
prove every substitution with smoke tests
```

Strict vanilla alignment is partial today because cloud GStack is not yet
installed as a native base and cloud GBrain is currently behind the local
reference version. The target is no longer "PGStack grows its own parallel
architecture"; the target is the native-first cloud replica defined in
[[../../wiki/syntheses/cloud-gstack-gbrain-native-first-replica-v1|Cloud GStack GBrain Native-First Replica v1]].

This page is the boundary contract future agents should read before changing
GBrain, MemTensor, GBrain Remote MCP, PGStack Agent Kit packaging, or unattended
maintenance jobs.

## Compatibility Classes

### Native GStack / GBrain Contract

These pieces should remain directly aligned with original `gstack + gbrain`:

- host-agnostic agent operating wrapper
- `AGENTS.md` as universal entry protocol
- repo-level `skills/RESOLVER.md`
- thick canonical skills, thin host adapters
- native GStack thinking/coding/product skills remain available as base skills
- separate durable brain repo
- MECE resolver and schema discipline
- `Compiled Truth + Timeline` for evolving knowledge objects
- brain-first lookup before external research
- artifact chain from one workflow step to the next
- doctor, smoke, maintenance, and minion/job style health loops
- MCP surface for agent access
- git-backed audit and recovery

### PGStack Extensions

These pieces are intentional PGStack extensions beyond the upstream default:

- `PGStack Constellation`: multiple complete nodes connected to one cloud brain
- `Hermes` as unattended runtime host
- `Codex` as workbench and verifier host
- `MultiCA / ACP` as control and repair plane
- `Obsidian / llm-wiki` as human-readable compilation surface
- governed team-memory promotion
- `PGStack Agent Kit` as teammate install/distribution package
- PGStack domain skills such as `personal-gstack`, `ai-daily-brief`,
  `radar/source-discovery`, `team-memory-gate`, and `agent-router`, as add-ons
  that must not replace native GStack/GBrain skills

Extensions are allowed only when they map back to one of the original loops:

```text
workflow loop
artifact loop
verification loop
memory loop
```

### MemTensor Substitution

MemTensor replaces or augments only this part of GBrain for PGStack:

- semantic recall when original embeddings are unavailable or intentionally
  delegated
- cross-session continuity memory
- compact write-through pointers
- governed team-sharing through Team Hub
- labeled retrieval or TeamHub context outside the canonical GBrain Remote MCP
  route

MemTensor does not replace:

- brain repo
- resolver/schema
- source-of-truth pages
- skillpack
- graph/timeline model
- minions/jobs
- doctor and maintenance protocol
- GBrain MCP identity

The accepted production center is:

```text
ECS hermes-admin GBrain Remote MCP
-> GBrain over /opt/data/.gbrain
-> MemTensor Hub only as labeled retrieval/team-sharing adapter
```

The local Mac install is a Codex workbench and vanilla reference node, not the
production memory center.

Current cloud replica gap:

```text
/opt/data/gstack is missing
/opt/data/.hermes/skills/gstack-* is missing
cloud GBrain is 0.20.4 while the local reference is 0.21.0
```

These are replica-gate gaps, not reasons to invent a separate PGStack runtime.

## Agent Decision Gate

Before changing PGStack/GBrain/MemTensor topology, ask:

1. Is this a native GStack/GBrain contract we should preserve?
2. Is this a PGStack extension that clearly improves multi-agent operation?
3. Is this a MemTensor substitution with a documented boundary?
4. Is there a smoke test proving the substitution still answers the original
   GBrain question?
5. Does the change create a second center, hidden owner route, or uncited memory
   authority?

If the answer to 5 is yes, stop and redesign.

## Read Path

Production agents should use this order:

```text
1. original GBrain Remote MCP against the cloud Brain Repo
2. cloud GBrain query/search/get/write tools exposed by Remote MCP
3. cloud MemTensor TeamHub only as a separately labeled curated team-memory
   source, not as GBrain fallback
4. local wiki or local vanilla GBrain only for workbench/reference checks
5. external research only when the brain and memory are insufficient
```

Current formal adapter:

```text
gbrain-remote MCP
engine/gbrain_remote_mcp_health.mjs
server /opt/pgstack-gbrain/gbrain_remote_mcp_http_server.mjs
server :8480/gbrain/mcp -> 127.0.0.1:8787
```

MemTensor boundary:

```text
MemTensor = retrieval and TeamHub adapter
GBrain Remote MCP = canonical brain interface
```

## Write Path

Durable behavior changes should land in this order:

```text
1. canonical brain/wiki/source-of-truth page
2. index/log/current-priority surfaces
3. PGBrain validation or relevant smoke test
4. compact MemTensor pointer
5. team promotion only through governance
```

Never write only to MemTensor when the object is a policy, skill, pipeline,
runbook, source map, architecture decision, or team-facing rule.

Cloud runtime changes should be executed by Hermes through MultiCA / ACP when
the user wants Hermes to own the result. Codex may verify externally but should
not silently mutate the cloud runtime path.

## Alignment Scorecard

| Area | Alignment |
|---|---|
| Operating wrapper | high |
| Skill resolver and thick skills | high |
| Host adapter model | high |
| Brain repo / schema / source pages | high |
| Doctor / smoke / maintenance loops | high |
| MCP access | original Remote MCP is active through `gbrain-remote` |
| Vector embeddings | substituted by MemTensor path unless strict vanilla key/runtime is enabled |
| Team sharing | PGStack extension through MemTensor Team Hub |
| Browser / pair-agent parity | partial |
| Original memory-sync parity | partial; Git/Agent Kit path still needs packaging maturity |

## Acceptance Tests

A compatibility change is not accepted until it can answer:

- Can an agent retrieve the current source-of-truth page?
- Can an agent get useful semantic recall when GBrain embeddings are absent?
- Are MemTensor hits labeled as context rather than canonical truth?
- Is the production center cloud `hermes-admin`, not the local reference node?
- Can the smoke test pass without hand-picked local state?
- Is the relevant index/log/current-priority surface updated?

Current accepted smoke chain:

```text
gbrain_remote_mcp_health.mjs --require-config
-> gbrain_remote_mcp_health.mjs --require-config --write-smoke
-> pgbrain_engine.py maintenance --remote-mcp-smoke --require-remote-mcp
-> Codex MCP registration `gbrain-remote`
```

## Forbidden Drift

Do not allow these patterns:

- treating MemTensor as a second canonical brain
- letting local Mac reference state override ECS production brain state
- changing GBrain schema just to fit a different embedding dimension without a
  migration gate
- storing raw chat or personal config as team knowledge
- creating host-specific skill behavior that bypasses repo-level skills
- enabling unattended cron/autopilot before the boundary and smoke test pass

## Typed Edges

- depends_on: [[gbrain-operating-logic-compatibility-matrix|GBrain Operating Logic Compatibility Matrix]]
- depends_on: [[pgstack-pgbrain-shared-kernel-architecture|PGStack PGBrain Shared Kernel Architecture]]
- depends_on: [[../../adapters/memtensor-gbrain-retrieval|MemTensor as GBrain Retrieval Adapter]]
- validated_by: [[../../wiki/syntheses/gstack-gbrain-vanilla-completion-gate-2026-04-26|GStack GBrain Vanilla Completion Gate 2026-04-26]]
- validated_by: [[../../wiki/syntheses/cloud-gstack-gbrain-native-first-replica-v1|Cloud GStack GBrain Native-First Replica v1]]
- implements: [[../../skills/brain-ops/SKILL|PGStack Brain Ops]]
- depends_on: [[../../adapters/memtensor|MemTensor Adapter]]
- depends_on: [[../../engine/README|PGBrain Engine]]

## Open Threads

- Complete the cloud native-first replica gate:
  - install/sync native GStack to `/opt/data/gstack`
  - expose native GStack skills to Hermes
  - decide and execute cloud GBrain version alignment
- Decide whether Remote MCP write smoke becomes scheduled automation after
  packaging.
- Build a conflict-handling fixture where stale MemTensor memory loses to a
  newer sourced brain page.
- Build a team-memory gate fixture for GBrain Remote MCP write-through
  pointers.
- Decide how much original GStack browser/pair-agent behavior should be copied
  into the PGStack central system.

---

## Timeline

- 2026-04-26: Created after comparing earlier cloud bridge work against the
  original `gstack + gbrain` operating model.
- 2026-04-26: Locked the distinction between strict vanilla alignment, high
  operating-contract alignment, and infrastructure-level MemTensor
  substitution.
- 2026-04-26: Updated after the Remote MCP cutover; `gbrain-remote` is now the
  formal active route and transitional central bridge commands are no longer
  part of the runtime surface.
