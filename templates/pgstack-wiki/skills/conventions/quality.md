---
title: PGStack Skill Quality Convention
type: convention
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../../AGENTS.md
  - ../../brain/schema.md
---

# PGStack Skill Quality Convention

## Required Qualities

- Prefer durable, reusable rules over one-off advice.
- Separate current truth from timeline/history.
- Preserve source pointers for material claims.
- Avoid team-memory transcript spillover.
- Keep host adapters thin and canonical behavior in repo-level skills.
- Update index and log after material shared-kernel changes.

## Anti-Patterns

- Writing personal defaults into team memory.
- Creating duplicate rules in Codex and Hermes without a repo-level source.
- Calling a pipeline graduated before Level 1-4 verification.
- Treating social or SEO material as primary evidence when a primary source exists.
