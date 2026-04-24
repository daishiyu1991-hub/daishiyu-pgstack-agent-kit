# Karpathy LLM Wiki Local Protocol

This reference instantiates Andrej Karpathy's LLM Wiki pattern for local Codex + Obsidian work.

Primary source: `references/karpathy-llm-wiki.md`.

Reference implementation boundary: `Pratiyush/llm-wiki` is a community implementation that turns agent session histories into static sites and AI exports. This skill borrows the implementation vocabulary where useful, but keeps the local workflow simple and editable inside Obsidian.

## Mental Model

Karpathy's analogy:

- Obsidian is the IDE.
- The LLM is the programmer.
- The wiki is the codebase.
- Raw sources are source of truth.
- `AGENTS.md` is the schema that turns a generic chatbot into a disciplined wiki maintainer.

## Directory Contract

```text
<wiki-slug>/
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

## Page Types

| Page type | Folder | Purpose |
|---|---|---|
| Source page | `wiki/sources/` | Summary of one raw source, with provenance and takeaways |
| Entity page | `wiki/entities/` | Person, org, project, tool, repo, place, product |
| Concept page | `wiki/concepts/` | Durable idea, distinction, principle, pattern |
| Synthesis page | `wiki/syntheses/` | Integrated thesis across many sources |
| Comparison page | `wiki/comparisons/` | Side-by-side analysis |
| Question page | `wiki/questions/` | Open question, answer history, evidence gaps |

## Frontmatter

Use enough metadata to support Dataview/search, but avoid ceremony:

```yaml
---
title: Page Title
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
sources:
  - ../sources/source-page.md
status: draft
---
```

Recommended `status`: `draft`, `reviewed`, `verified`, `stale`, `archived`.

Recommended `confidence`: `low`, `medium`, `medium-high`, `high`.

## `wiki/index.md`

`index.md` is content-oriented. It should list pages with one-line summaries and enough category structure for future agents to quickly decide what to read.

Minimum sections:

- Overview
- Sources
- Entities
- Concepts
- Syntheses
- Comparisons
- Questions
- Recently updated

## `wiki/log.md`

`log.md` is chronological and append-only.

Use parseable headings:

```markdown
## [YYYY-MM-DD] ingest | Source Title

- Raw source:
- Pages created:
- Pages updated:
- Key decisions:
- Open questions:
```

Other valid actions: `query`, `lint`, `refactor`, `schema`, `memory`.

## Ingest Checklist

1. Source preserved in `raw/sources/` or linked as immutable source.
2. Source page created/updated in `wiki/sources/`.
3. At least one concept/entity/synthesis page updated if the source matters.
4. New contradictions or changed claims recorded.
5. `wiki/index.md` updated.
6. `wiki/log.md` appended.
7. Durable outcomes written to MemTensor when relevant.

## Query Checklist

1. Read `AGENTS.md`.
2. Read `wiki/index.md`.
3. Read only relevant pages.
4. Answer with links to wiki pages or raw sources.
5. File durable new synthesis back into `wiki/` if it should compound.
6. Append `query` entry to `wiki/log.md` when a durable page is created or updated.

## Lint Checklist

Look for:

- Contradictions between pages.
- Stale claims superseded by newer sources.
- Orphan pages with no inbound links.
- Important concepts mentioned but lacking a page.
- Missing cross-references.
- Duplicate pages that should be merged.
- Data gaps that need web search or user input.
- Open questions that should be promoted into `wiki/questions/`.

## AGENTS.md Template

```markdown
# <Wiki Title> Agent Schema

You are maintaining a Karpathy-style LLM Wiki.

## Contract

- Never modify `raw/` sources except to add new immutable source files requested by the user.
- Maintain generated knowledge in `wiki/`.
- Read `wiki/index.md` before answering questions.
- Update `wiki/index.md` and `wiki/log.md` after any durable change.
- Prefer many focused pages over one giant page.
- Use `[[wikilinks]]` for internal wiki connections.
- Distinguish facts, inferences, opinions, and open questions.

## Operations

### Ingest

### Query

### Lint

## Local Memory

When durable project knowledge changes, write a compact summary to MemTensor with the wiki path and read order.
```
