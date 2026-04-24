---
name: skillify
title: PGStack Skillify
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Turn repeated successful work into reusable skills.
source_of_truth:
  - ../RESOLVER.md
  - ../../wiki/syntheses/personal-gstack-skill-tree-evolution-rules.md
  - ../../brain/skills/gbrain-operating-logic-compatibility-matrix.md
---

# PGStack Skillify

Use this skill when repeated work should become a reusable protocol.

## Gate

Create or update a skill when at least one is true:

- The user will repeat the workflow.
- Another agent or teammate should be able to run it.
- A failure produced a reusable operating rule.
- A pipeline needs a stable human/agent handoff.

## Protocol

```text
detect pattern -> draft skill -> add resolver route -> add manifest entry -> verify -> log
```

Do not grow the skill tree just because a topic is interesting.
