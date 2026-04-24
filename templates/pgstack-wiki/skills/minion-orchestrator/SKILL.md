---
name: minion-orchestrator
title: PGStack Minion Orchestrator
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: medium-high
scope: local_pgstack
description: Route recurring or background work to Hermes, jobs, or future minions.
source_of_truth:
  - ../RESOLVER.md
  - ../conventions/cron-via-minions.md
  - ../../jobs/RESOLVER.md
---

# PGStack Minion Orchestrator

Use this skill when work should run outside the foreground conversation.

## Contract

- Hermes is the current scheduler and unattended runtime host.
- `jobs/` is the durable contract layer.
- Deterministic scripts should handle bounded collection and validation.
- Judgment work should be explicit and reviewable.

## Routing

- Daily/weekly recurring pipeline -> Hermes cron plus `jobs/<name>.md`.
- Long task with durable state -> split into stages and write state pointers.
- One-off interactive implementation -> Codex workbench.
- Future multi-agent dispatch -> AgentHost/MultiCA adapter, not a new core rule.

## Timeout Rule

If a job risks host idle timeout, split it into bounded phases with visible
state artifacts and avoid broad generic searches inside unattended runs.
