---
title: MultiCA AgentHost Adapter
type: source
created: 2026-04-24
updated: 2026-04-27
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
They can route work across other people's agents, team-visible runtime lanes,
or explicitly delegated remote agents, but they should not be treated as the
durable memory layer or the default private-agent route.

After Agent Layer Stage 3.5, MultiCA/ACP is an orchestration channel. The
shared kernel remains the source of truth.

## Compiled Truth

The safe default path is:

```text
private user-owned work
-> native GStack/GBrain through Codex, Hermes, or the user's own agent
-> write durable conclusions into PGBrain

cross-agent or team-visible work
-> MultiCA / AgentHost
-> receive artifact or status from the target agent
-> write durable conclusions into PGBrain
-> promote only governed candidates into MemTensor
```

Do not write raw chat logs, transient process output, or private account state
to MemTensor team space.

## Timeline

- 2026-04-24: Added as an optional orchestration adapter in the public starter kit.
- 2026-04-26: Linked to Agent Layer Stage 3.5.
- 2026-04-27: Tightened default routing: native GStack/GBrain for private
  user-owned work, MultiCA/AgentHost for cross-agent or team-visible dispatch.

## Health Check

```text
run one no-op task through the host
confirm the target agent receives the task
write one harmless test artifact into PGBrain
run PGBrain doctor
verify MemTensor writes pass team-memory gate rules
```
