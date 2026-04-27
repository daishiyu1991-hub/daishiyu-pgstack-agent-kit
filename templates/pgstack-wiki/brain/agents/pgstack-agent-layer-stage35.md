---
title: PGStack Agent Layer Stage 3.5
type: agent
created: 2026-04-26
updated: 2026-04-27
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../../skills/agent-router/SKILL.md
  - ../skills/pgstack-upstream-parity-checklist.md
  - ../../adapters/multica-agenthost.md
---

# PGStack Agent Layer Stage 3.5

## Compiled Truth

The PGStack agent layer is an explicit operating layer, not an inference from the
existence of Codex, Hermes, MultiCA, AgentHost, MCP tools, or scripts.

Installed PGStack nodes adapt the original `gstack` agent logic by combining:

- portable skill roles
- Codex as workbench
- Hermes as unattended runtime
- native GStack/GBrain as the default private-agent path
- MultiCA/ACP and AgentHost as optional cross-agent/team execution surfaces
- PGBrain as the durable source-of-truth layer
- MemTensor as optional governed recall/team sharing

## Current State

Agent routes resolve through:

```text
AGENTS.md
-> skills/RESOLVER.md
-> skills/agent-router/SKILL.md
-> brain/agents/pgstack-agent-layer-stage35.md
-> relevant job / adapter / memory / pipeline page
```

| Host / Role | Status | Responsibility | Boundary |
|---|---|---|---|
| Human steward | active | direction, approval, promotion, pruning | does not operate every tool |
| Codex | active | workbench, edits, verification, Git, local memory | not unattended runtime by default |
| Hermes | active | recurring runtime, cron, notifications | must leave evidence |
| MultiCA / ACP | optional | operations channel for prompting other-person, team, self-repair, or explicitly delegated remote agents | not source of truth or default private route |
| AgentHost | optional | execution slots for additional agents | must return artifacts |
| PGBrain Engine / minions | active | deterministic index, query, doctor, smoke | not a judgment agent |
| MemTensor | optional | continuity and governed sharing | not the long-form brain repo |

## Routing Contract

For any non-trivial task, name:

- owner
- trigger
- inputs
- stop condition
- artifact contract
- verification gate
- memory write-back
- escalation path

## Acceptance Evidence

The agent layer is considered adapted when:

- this page exists
- `skills/agent-router/SKILL.md` exists
- resolver and manifest include `agent-router`
- PGBrain query recovers this page
- `pgbrain_engine.py validate` passes
- `pgbrain_engine.py doctor` passes
- `skillpack_check.py` passes
- Agent Kit smoke test queries this page

## Typed Edges

- implements: [[../skills/pgstack-upstream-parity-checklist|PGStack Upstream Parity Checklist]]
- depends_on: [[../../skills/agent-router/SKILL|PGStack Agent Router]]
- depends_on: [[../../skills/RESOLVER|PGStack Skill Resolver]]
- depends_on: [[../../jobs/RESOLVER|PGStack Jobs Resolver]]
- depends_on: [[../../adapters/multica-agenthost|MultiCA AgentHost Adapter]]
- validated_by: [[../skills/pgbrain-engine-v1|PGBrain Engine v1]]

---

## Timeline

- 2026-04-26: Added to the starter kit so installed nodes do not miss the agent
  layer when aligning to upstream `gstack + gbrain`.
