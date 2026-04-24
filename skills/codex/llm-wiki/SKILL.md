---
name: llm-wiki
description: Instantiate Andrej Karpathy's LLM Wiki knowledge-management pattern as a local Codex/Obsidian workflow. Use when the user asks to compile memories, raw sources, notes, research, agent sessions, or project conclusions into a persistent, interlinked Markdown wiki that compounds over time; also use when ingesting sources, querying a wiki, linting a wiki, or creating the AGENTS.md schema for a wiki.
metadata:
  short-description: Build Karpathy-style LLM wikis
---

# LLM Wiki

Use this skill to implement Andrej Karpathy's LLM Wiki pattern locally: raw sources stay immutable, the LLM maintains a generated Markdown wiki, and an `AGENTS.md` schema teaches future agents how to keep it healthy.

## Core Pattern

Karpathy's pattern has three layers:

1. `raw/`: curated source material. Treat this as source of truth and do not modify it.
2. `wiki/`: LLM-generated Markdown pages: sources, entities, concepts, syntheses, comparisons, questions, `index.md`, and `log.md`.
3. `AGENTS.md`: the schema and operating manual for future Codex agents working in that wiki.

The human curates sources, asks questions, and steers emphasis. The LLM does the bookkeeping: summaries, links, contradictions, index updates, log entries, and consistency maintenance.

## Default Local Layout

Create durable wikis under:

```text
$PGSTACK_WIKI_ROOT/<wiki-slug>/
├── AGENTS.md
├── raw/
│   ├── sources/
│   └── assets/
└── wiki/
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── sources/
    ├── entities/
    ├── concepts/
    ├── syntheses/
    ├── comparisons/
    └── questions/
```

## Operations

### Ingest

Use when adding a new source, memory, transcript, article, or note.

1. Preserve the source in `raw/sources/` or reference its immutable location.
2. Read the source and discuss key takeaways with the user when emphasis is ambiguous.
3. Create or update `wiki/sources/<source>.md`.
4. Update relevant `wiki/entities/`, `wiki/concepts/`, `wiki/syntheses/`, `wiki/comparisons/`, or `wiki/questions/` pages.
5. Update `wiki/index.md`.
6. Append an entry to `wiki/log.md`.
7. If MemTensor is available, store the wiki path and durable conclusions.

### Query

Use when answering questions against an existing wiki.

1. Read `AGENTS.md`, then `wiki/index.md`, then relevant pages.
2. Answer with citations/links to wiki pages or raw sources.
3. If the answer creates durable synthesis, file it back into `wiki/` and log it.

### Lint

Use periodically or when the wiki feels stale.

Check for contradictions, stale claims, orphan pages, missing cross-links, duplicate concepts, absent source pages, data gaps, and unanswered questions that deserve their own page.

## References

- Read `references/karpathy-llm-wiki.md` when you need the original idea text.
- Read `references/protocol.md` when you need concrete page templates and maintenance rules.

## Skeleton Script

To create a new local wiki skeleton:

```bash
python3 $CODEX_HOME/skills/llm-wiki/scripts/init_wiki.py --root "$PGSTACK_WIKI_ROOT" --slug "<wiki-slug>" --title "<Wiki Title>"
```
