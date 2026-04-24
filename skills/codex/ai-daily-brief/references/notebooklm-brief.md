# NotebookLM Brief

Use NotebookLM as a research workbench, not as the primary daily collector.

## Current Boundary

As of `2026-04-24`, this workflow assumes:

- NotebookLM is useful for deeper synthesis over a curated source set
- NotebookLM is not the primary collector for the unattended Hermes daily brief
- NotebookLM should receive already confirmed sources rather than raw rumor or noisy social chatter
- a stable official NotebookLM MCP/API is not assumed in the production path

NotebookLM is therefore downstream of confirmation and triage, not upstream of them.

## Best Position In The Pipeline

```text
social-radar
-> official-confirm
-> deterministic candidate bundle
-> Hermes daily digest
-> NotebookLM research brief for deeper follow-up
```

This means NotebookLM is a focused search-and-synthesis window for topics that deserve a second pass.

## When To Use

Create a NotebookLM handoff when:

- one story has unusually large strategic implications
- several sources need to be compared and reconciled
- the user wants a deeper explanation than the daily brief should carry
- the event could affect future decisions, investments, or workflow design

Do not create a NotebookLM handoff for every ordinary daily item.

## Recommended Inputs

Pass `5-15` confirmed sources, such as:

- official announcement pages
- docs or release notes
- papers
- model cards
- official GitHub repos or releases
- official YouTube videos
- one or two high-credibility secondary analyses if they add real context

## Recommended Notebook Naming

Use a clear topic-specific notebook name, for example:

- `AI Frontier Watch | 2026-04-24`
- `DeepMind Agent Launch | 2026-04`
- `OpenAI Pricing Shift | 2026-04`

## Recommended Research Questions

Ask NotebookLM questions like:

- What actually changed here?
- Which claims are directly supported by the sources?
- How does this compare with the last similar launch?
- What are the strategic implications for builders, labs, or platforms?
- What remains uncertain?
- What should be watched next?

## Recommended Output Artifact

Write the result back into Obsidian as a separate research note, for example:

```text
$HOME/Documents/PGStack/AI Daily Brief/Research/YYYY/YYYY-MM-DD Topic Brief.md
```

Suggested structure:

```md
# Topic Research Brief | YYYY-MM-DD

## Topic

One-sentence framing.

## Confirmed Sources

- title: URL

## What Changed

Short factual summary.

## Why It Matters

Short strategic summary.

## Competing Interpretations

- interpretation A
- interpretation B

## Open Questions

- question

## What To Watch Next

- signal
```

## Operational Rule

NotebookLM can deepen understanding, but it should not lower the factual bar for the daily brief.

The daily brief remains:

- short
- confirmed
- source-linked
- high-signal
