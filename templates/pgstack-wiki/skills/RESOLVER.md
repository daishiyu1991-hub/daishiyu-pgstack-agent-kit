---
title: PGStack Skill Resolver
type: resolver
created: 2026-04-24
updated: 2026-04-26
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../brain/skills/pgstack-pgbrain-shared-kernel-architecture.md
  - ../brain/skills/gbrain-operating-logic-compatibility-matrix.md
  - ../wiki/syntheses/personal-gstack-pipeline-graduation-template.md
---

# PGStack Skill Resolver

## Compiled Truth

`skills/RESOLVER.md` is the shared-kernel dispatcher for PGStack work.

It decides which canonical repo-level skill owns a task before any host adapter
starts doing work.

Codex, Hermes, and future agents may expose their own installed skill files, but
their durable behavior should resolve back to this contract. This is the local
PGStack equivalent of original `gbrain`'s `skills/RESOLVER.md`.

## Current State

### Always-On Skills

| Trigger | Canonical Skill | Runtime Note |
|---|---|---|
| Every substantive inbound message | `skills/signal-detector/SKILL.md` | Detect durable signal; do not block the main response. |
| Any brain read/write/lookup/citation | `skills/brain-ops/SKILL.md` | Enforce brain-first lookup, source discipline, and write-back rules. |

Pure acknowledgements, disposable UI chatter, and no-op turns may be skipped by
`signal-detector`, but the skip reason should be clear.

### Brain Operations

| Trigger | Canonical Skill |
|---|---|
| "What do we know", "search", "tell me about" | `skills/query/SKILL.md` |
| New durable page/file placement | `skills/repo-architecture/SKILL.md` |
| New entity/source/tool/pipeline needs context | `skills/enrich/SKILL.md` |
| Ingest a source, note, run output, or source bundle | `skills/ingest/SKILL.md` |
| Brain health, relink, maintenance, drift cleanup | `skills/maintain/SKILL.md` |
| Create or improve a reusable skill | `skills/skillify/SKILL.md` |
| Validate skillpack/kernel health | `skills/testing/SKILL.md` |

### Agent Operations

| Trigger | Canonical Skill |
|---|---|
| Decide which agent/host owns work | `skills/agent-router/SKILL.md` |
| MultiCA/ACP, AgentHost, remote repair, or multi-agent handoff | `skills/agent-router/SKILL.md` |
| Upstream parity question touches agent layer | `skills/agent-router/SKILL.md` plus `brain/skills/pgstack-upstream-parity-checklist.md` |

### PGStack Workflow

| Trigger | Canonical Skill |
|---|---|
| Fuzzy, complex, strategic, or durable work | `skills/personal-gstack/SKILL.md` |
| Compile raw material into Obsidian/wiki | `skills/llm-wiki/SKILL.md` |
| AI intelligence daily brief | `skills/ai-daily-brief/SKILL.md` |
| Source expansion and source-gate review | `skills/source-discovery/SKILL.md` |
| Convert high-signal source packs into a research brief | `skills/research-brief/SKILL.md` |

### Team Memory

| Trigger | Canonical Skill |
|---|---|
| Write compact reusable team knowledge | `skills/team-memory-writing/SKILL.md` |
| Decide local vs team_candidate vs team_shared | `skills/team-memory-gate/SKILL.md` |

### Runtime And Minions

| Trigger | Canonical Skill |
|---|---|
| Recurring jobs, cron/minion ownership, background work | `skills/minion-orchestrator/SKILL.md` |

### Host Adapter Fallback

If a host has a more specific installed adapter, read the repo-level skill here
first, then use the host adapter to execute.

### Canonical Host Adapters

| Kernel Skill | Codex Adapter | Hermes Adapter | Notes |
|---|---|---|---|
| `personal-gstack` | `$CODEX_HOME/skills/personal-gstack/SKILL.md` | future mirror | Codex is the current workbench adapter. |
| `llm-wiki` | `$CODEX_HOME/skills/llm-wiki/SKILL.md` | future mirror | Used for Obsidian compilation and maintenance. |
| `ai-daily-brief` | `$CODEX_HOME/skills/ai-daily-brief/SKILL.md` | Hermes runtime skill/spec | Hermes owns recurring execution. |
| `agent-router` | repo-level skill only for now | future Hermes/MultiCA mirror | Shared-kernel contract for agent ownership and handoff. |
| `team-memory-writing` | `$CODEX_HOME/skills/team-memory-writing/SKILL.md` | future curator support | Team memory must stay curated, not transcript-shaped. |
| `team-memory-gate` | `$CODEX_HOME/skills/team-memory-gate/SKILL.md` | future curator support | Gate before publication or cleanup. |

### Runtime Rule

Use the smallest skill set that covers the task, then write durable outcomes
back to the wiki, brain, Git, and configured cloud memory route as appropriate.

For recurring pipelines, do not call a pipeline `graduated-v1` unless it passes
the Level 1-4 ladder in [[../wiki/syntheses/personal-gstack-pipeline-graduation-template|Personal GStack Pipeline Graduation Template]].

## Current Open Threads

- Whether Hermes should receive generated thin mirror skills for all canonical
  repo-level skills.
- Whether future agent hosts should read this file directly or receive generated
  host-specific shims.
- Whether skill installation/sync should become a `jobs/` task.
- Whether `skills/manifest.json` should later be generated from frontmatter.

## Source Of Truth

- [[../brain/skills/pgstack-pgbrain-shared-kernel-architecture|PGStack PGBrain Shared Kernel Architecture]]
- [[../brain/skills/gbrain-operating-logic-compatibility-matrix|GBrain Operating Logic Compatibility Matrix]]
- [[../brain/skills/pgstack-repo-skillpack-protocol-v1|PGStack Repo Skillpack Protocol v1]]
- [[../wiki/syntheses/personal-gstack-pipeline-graduation-template|Personal GStack Pipeline Graduation Template]]

---

## Timeline

- 2026-04-24: Created as the first canonical shared-kernel skill dispatcher.
- 2026-04-24: Reworked to mirror original `gbrain`'s resolver pattern with
  always-on `signal-detector` and `brain-ops`, plus repo-level thick skills.
- 2026-04-26: Added `agent-router` as the canonical owner for agent host
  routing, MultiCA/ACP handoff, and agent-layer parity checks.
