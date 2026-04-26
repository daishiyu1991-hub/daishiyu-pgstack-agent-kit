---
title: PGStack Agent Routing Convention
type: convention
created: 2026-04-24
updated: 2026-04-26
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../../AGENTS.md
  - ../agent-router/SKILL.md
  - ../../brain/skills/pgstack-pgbrain-shared-kernel-architecture.md
---

# PGStack Agent Routing Convention

## Split

- `Codex`: interactive design, implementation, verification, wiki compilation.
- `Hermes`: unattended runtime, cron, notifications, recurring pipeline execution.
- `MultiCA / AgentHost`: future coordination and multi-agent dispatch surfaces.
- `MemTensor Team Hub`: compiled team knowledge sharing, not raw task execution.

## Rule

Use deterministic scripts for bounded checks and repeatable transforms.
Use judgment agents for ambiguity, synthesis, and review.

Do not add a new agent role when an existing skill, job, or adapter can own the
work cleanly.

Every subagent handoff must name a stop condition, artifact contract,
verification gate, and memory write-back rule. If those cannot be named, keep
the work in the foreground agent until the task is clearer.
