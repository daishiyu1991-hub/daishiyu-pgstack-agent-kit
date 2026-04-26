---
name: agent-router
title: PGStack Agent Router
type: skill
version: 0.1.0
created: 2026-04-26
updated: 2026-04-26
status: active
confidence: high
scope: local_pgstack
description: Route durable work across Codex, Hermes, MultiCA/ACP, AgentHost, jobs, minions, and memory write-back.
source_of_truth:
  - ../RESOLVER.md
  - ../../brain/agents/pgstack-agent-layer-stage35.md
  - ../../brain/skills/pgstack-upstream-parity-checklist.md
---

# PGStack Agent Router

Use this skill when a task asks who should do the work, which agent host should
own a step, whether to use Hermes or MultiCA/ACP, or whether the agent layer is
complete enough for an upstream-parity claim.

## Contract

Do not treat installed tools as an agent layer.

An agent route is valid only when it names:

- owner
- trigger
- stop condition
- artifact contract
- verification gate
- memory write-back rule
- escalation path

## Dispatch Order

Before routing durable work:

1. Read `AGENTS.md`.
2. Read `skills/RESOLVER.md`.
3. Read `brain/agents/pgstack-agent-layer-stage35.md`.
4. Read the relevant job, pipeline, adapter, or memory page.
5. If the route is an upstream-parity claim, read
   `brain/skills/pgstack-upstream-parity-checklist.md`.

## Routing Table

| Work Type | Primary Owner | Supporting Surface | Stop Condition |
|---|---|---|---|
| Ambiguous strategy, planning, architecture, skill design | Codex | `personal-gstack`, `brain-ops` | Durable page, verification, log, memory pointer |
| Code/workspace implementation | Codex | repo tests, Git, PGBrain doctor | Patch verified and committed when appropriate |
| Recurring unattended workflow | Hermes | `jobs/`, `minion-orchestrator` | Run evidence, state, notification or silent marker |
| Remote runtime repair | target agent via MultiCA/ACP prompt | Codex external verifier | target agent performs fix and Codex verifies smoke |
| Multi-agent dispatch | MultiCA / AgentHost | this router, source-of-truth job or agent page | Each delegated lane has artifact and review gate |
| Deterministic maintenance or indexing | PGBrain Engine / job minion | `engine/`, `jobs/` | Command output and updated state |
| Team knowledge publication | runtime curator first, Codex compile second | `team-memory-writing`, `team-memory-gate` | Curated memory or explicit reject/reroute |

## Verification Gate

Use the smallest real gate that proves the route worked:

- local kernel change: `pgbrain_engine.py validate`, `doctor`, targeted `query`
- skillpack change: `skillpack_check.py`
- Agent Kit change: `scripts/smoke_test.sh`
- runtime change: run evidence plus external verification
- memory change: write/read or search recall

## Output Shape

```text
Owner:
Supporting agents/tools:
Trigger:
Inputs:
Stop condition:
Artifacts:
Verification:
Memory write-back:
Escalation:
```

## Typed Edges

- implements: [[../../brain/agents/pgstack-agent-layer-stage35|PGStack Agent Layer Stage 3.5]]
- depends_on: [[../RESOLVER|PGStack Skill Resolver]]
- depends_on: [[../../jobs/RESOLVER|PGStack Jobs Resolver]]
- validated_by: [[../../brain/skills/pgbrain-engine-v1|PGBrain Engine v1]]
