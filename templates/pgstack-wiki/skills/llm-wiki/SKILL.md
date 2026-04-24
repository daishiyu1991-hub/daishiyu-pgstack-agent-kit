---
name: llm-wiki
title: LLM Wiki
type: skill
version: 0.1.0
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
description: Compile raw sources and durable conclusions into the Obsidian wiki.
source_of_truth:
  - ../RESOLVER.md
  - ../../AGENTS.md
  - ../../wiki/index.md
---

# LLM Wiki

Use this skill when raw material, memories, run outputs, or conclusions should
become durable Obsidian knowledge.

## Contract

```text
raw source -> wiki source page -> synthesis/entity/concept/runbook -> index -> log
```

## Rules

- Do not modify existing raw sources except to add new immutable source files.
- Prefer focused pages over giant dumps.
- Use wikilinks for important relationships.
- Distinguish facts, inferences, preferences, and open questions.
- Update `wiki/index.md` and `wiki/log.md` after durable changes.

## Host Adapter

Codex adapter: `$CODEX_HOME/skills/llm-wiki/SKILL.md`
