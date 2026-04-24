---
name: team-memory-gate
title: Team Memory Gate
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Decide memory scope and promotion eligibility.
source_of_truth:
  - ../RESOLVER.md
  - ../../brain/memory/team-hub-sharing.md
  - ../../wiki/syntheses/personal-gstack-team-memory-gate-skill.md
  - ../../wiki/syntheses/personal-gstack-memory-promotion-policy.md
---

# Team Memory Gate

Use this skill before writing or promoting memory into team space.

## Contract

Protect `team_shared` from personal, noisy, unscoped, or weakly reviewed memory.

## Scope Classes

- `personal`
- `local_pgstack`
- `team_candidate`
- `team_shared`
- `private_sensitive`

## Promotion Rule

Promote to `team_shared` only when the knowledge is reusable, compact, source-
linked, non-personal, and belongs to `business`, `ai_knowledge`, or `skills`.

When uncertain, keep it in `local_pgstack` or `team_candidate`.
