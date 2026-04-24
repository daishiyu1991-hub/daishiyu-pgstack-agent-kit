# Triage

This file answers one practical question:

> After a signal is confirmed, what happens next?

Use this three-layer model.

## Layer 1: Daily Brief Only

This is the default destination.

A confirmed item stays in the daily brief only when it is:

- important enough to mention today
- understandable in one short summary
- not likely to require cross-source comparison
- not obviously the start of a long thematic line

Examples:

- a meaningful but self-contained model update
- one notable paper
- one product launch with clear facts
- one infra or tooling release with limited strategic ambiguity

Output:

- Feishu digest item
- Obsidian daily brief item

## Layer 2: Research Brief

Promote a confirmed item into a separate research brief when at least one of these is true:

- the story has strategic implications beyond a same-day headline
- several first-party sources need to be reconciled
- the story is likely to evolve over days or weeks
- the user would benefit from a second-pass explanation
- the event raises nontrivial open questions or competing interpretations

Examples:

- Anthropic `Economic Index`
- a new platform or ecosystem move like `La Plateforme`
- a methods paper with direct agent or workflow implications
- a pricing or distribution shift that changes builder economics

Output:

- a topic-specific research note
- a NotebookLM-ready source bundle or question set

## Layer 3: Long-Running Topic Notebook

Promote a topic into a long-running notebook only when it is clearly durable.

Use this destination when:

- the topic will likely matter for months, not days
- repeated future updates are expected
- keeping historical continuity will make later analysis better
- the topic is relevant to the user's workflow, decisions, or strategy

Examples:

- Anthropic `Economic Index`
- frontier lab pricing and access changes
- agent tooling and tool-use methodology
- long-context inference infrastructure
- AI policy or export-control shifts

Output:

- a durable topic notebook or recurrent research track
- future daily items can attach back to the same theme

## Quick Decision Rules

Ask these in order:

1. Is the item confirmed?
   - If no: it stays in `social-radar` only.
2. Is the item actually fresh enough for today's workflow?
   - If no, or if page publication time conflicts with a newer sitemap/update signal, keep it in a verification bucket and do not promote it into a research brief or long-running notebook yet.
3. Is it worth mentioning today?
   - If yes: it enters the daily brief.
4. Does it need deeper synthesis to be useful?
   - If yes: create a research brief.
5. Is it likely to remain strategically relevant across multiple future updates?
   - If yes: promote it into a long-running topic notebook.

## Important Clarification

Picking a topic for the first research brief does **not** mean the system has automatically ranked it as the single most important item.

Sometimes a topic is chosen simply because it is the best example of:

- multi-source confirmation
- strategic depth
- good fit for second-pass synthesis

That is what happened with the first `Anthropic Economic Index` research brief.

## Mental Model

```text
signal
-> confirmed item
-> daily brief
-> optional research brief
-> optional long-running notebook
```

Most items stop at the daily brief.

Only a minority should become research briefs.

Only a smaller minority should become long-running notebooks.
