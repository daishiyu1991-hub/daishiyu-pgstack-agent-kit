---
title: MultiCA AgentHost Adapter
type: source
created: 2026-04-24
updated: 2026-04-26
status: candidate
confidence: medium
scope: local_pgstack
source_of_truth:
  - ../AGENTS.md
  - ../brain/skills/pgstack-pgbrain-shared-kernel-architecture.md
  - ../brain/memory/team-hub-sharing.md
  - ../brain/agents/pgstack-agent-layer-stage35.md
---

# MultiCA AgentHost Adapter

MultiCA and AgentHost are optional orchestration layers for a PGStack Node.
They can route work across Codex, Hermes, and other agents, but they should not
be treated as the durable memory layer.

After Agent Layer Stage 3.5, MultiCA/ACP is an orchestration channel. The
shared kernel remains the source of truth.

## Compiled Truth

The safe default path is:

```text
MultiCA / AgentHost
-> dispatch work to Codex, Hermes, or another agent
-> receive artifact or status
-> write durable conclusions into PGBrain
-> promote only governed candidates into MemTensor
```

Do not write raw chat logs, transient process output, or private account state
to MemTensor team space.

## Timeline

- 2026-04-24: Added as an optional orchestration adapter in the public starter kit.
- 2026-04-26: Linked to Agent Layer Stage 3.5.

## Health Check

```text
run one no-op task through the host
confirm the target agent receives the task
write one harmless test artifact into PGBrain
run PGBrain doctor
verify MemTensor writes pass team-memory gate rules
```
