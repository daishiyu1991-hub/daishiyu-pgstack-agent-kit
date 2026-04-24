---
name: ai-daily-brief
title: AI Daily Brief
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Maintain the Hermes-operated AI intelligence daily brief.
source_of_truth:
  - ../RESOLVER.md
  - ../../jobs/ai-daily-brief.md
  - ../../brain/pipelines/ai-daily-brief.md
  - ../../wiki/syntheses/hermes-ai-daily-brief-v1.md
---

# AI Daily Brief

Hermes runs the daily AI intelligence brief. Codex maintains the skill/spec.

## Contract

- Runtime host: Hermes.
- Default language: Chinese.
- Delivery: Feishu summary plus Obsidian deep report.
- Scope: high-signal AI model, product, research, open-source, policy, and capital updates.
- Quality: source-linked, deduped, reasoned, and concise.

## Related Pipeline

The current graduated pipeline is defined in:

- `jobs/ai-daily-brief.md`
- `brain/pipelines/ai-daily-brief.md`

Use `source-discovery`, `radar-hub`, `source-pack`, and `research-brief` skills
as upstream sidecars, not as replacements for the stable daily brief.
