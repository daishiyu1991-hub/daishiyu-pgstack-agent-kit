---
title: PGStack Repo Skillpack Protocol v1
type: skill
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../../skills/RESOLVER.md
  - ../../skills/manifest.json
  - gbrain-operating-logic-compatibility-matrix.md
  - pgstack-pgbrain-shared-kernel-architecture.md
---

# PGStack Repo Skillpack Protocol v1

## Compiled Truth

PGStack now follows the original `gbrain` skillpack shape more directly:

```text
AGENTS.md
-> skills/RESOLVER.md
-> skills/manifest.json
-> skills/*/SKILL.md
-> engine/jobs/brain/adapters
```

The repo-level `skills/` directory is the canonical behavior layer.

Codex, Hermes, and future AgentHost/MultiCA runtimes may have their own installed
skills, but those host files are adapters or mirrors. Durable behavior changes
should land in the repo-level skillpack first.

## Current State

The first canonical PGStack skillpack now includes:

- always-on `signal-detector`
- always-on `brain-ops`
- workflow skills: `personal-gstack`, `llm-wiki`, `ai-daily-brief`
- brain operation skills: `query`, `ingest`, `enrich`, `maintain`,
  `repo-architecture`
- runtime skill: `minion-orchestrator`
- intelligence sidecar skills: `source-discovery`, `research-brief`
- memory governance skills: `team-memory-writing`, `team-memory-gate`
- evolution and verification skills: `skillify`, `testing`

`engine/skillpack_check.py` and `PGBrain Engine validate/doctor` now verify that
required canonical skills exist and match `skills/manifest.json`.

## Operating Rules

- Read `skills/RESOLVER.md` before selecting a host adapter.
- Read the selected `skills/<name>/SKILL.md` before acting.
- Keep host-specific `.codex` and Hermes skills thin where possible.
- If a recurring workflow needs background execution, route through `jobs/` and
  `minion-orchestrator`.
- If a workflow repeats or fails in a reusable way, route through `skillify`.

## Current Constraints

- This is not a wholesale copy of Garry Tan's personal domains.
- The domain schema remains PGStack-specific.
- Team-memory governance remains an intentional PGStack extension.
- Existing `.codex/skills` and Hermes runtime skills are not deleted or moved in
  this phase.

## Current Open Threads

- host-sync generation from repo-level skills into Codex/Hermes adapters
- whether `manifest.json` should become generated from frontmatter
- how much host adapter text should remain after mirrors exist
- whether future MultiCA/AgentHost dispatch should read this resolver directly

## Source Of Truth

- [[../../skills/RESOLVER|PGStack Skill Resolver]]
- `../../skills/manifest.json`
- [[gbrain-operating-logic-compatibility-matrix|GBrain Operating Logic Compatibility Matrix]]
- [[pgstack-pgbrain-shared-kernel-architecture|PGStack PGBrain Shared Kernel Architecture]]
- [[pgbrain-engine-v1|PGBrain Engine v1]]

## Typed Edges

- implements: [[gbrain-operating-logic-compatibility-matrix|GBrain Operating Logic Compatibility Matrix]]
- depends_on: [[pgstack-pgbrain-shared-kernel-architecture|PGStack PGBrain Shared Kernel Architecture]]
- validated_by: [[pgbrain-engine-v1|PGBrain Engine v1]]
- reads_from: [[../../skills/RESOLVER|PGStack Skill Resolver]]

---

## Timeline

- 2026-04-24: Created after the decision to align PGStack with original
  `gbrain`'s repo-level skillpack model.
