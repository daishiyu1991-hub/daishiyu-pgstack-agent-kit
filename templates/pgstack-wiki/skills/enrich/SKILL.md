---
name: enrich
title: PGBrain Enrich
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Apply tiered enrichment to durable objects and update compiled truth.
source_of_truth:
  - ../RESOLVER.md
  - ../../brain/skills/pgbrain-enrichment-protocol-v1.md
  - ../../engine/source_pack_enrich.py
---

# PGBrain Enrich

Use this skill when a durable object needs more context, source support, or
relationship structure.

## Protocol

```text
ingest -> brain-first lookup -> tier -> enrich -> raw/state pointer -> compiled truth -> timeline -> links/edges -> sync
```

## Tiers

- Tier 3: stub plus local cross-reference.
- Tier 2: bounded source check plus relationship update.
- Tier 1: full synthesis with source pointers, timeline, and verification.

## Rules

- Do not enrich everything equally.
- Do not invoke broad web research when bounded primary sources are enough.
- Preserve raw/state pointers for generated enrichment artifacts.
- Update `Compiled Truth` only when new evidence materially changes the object.
