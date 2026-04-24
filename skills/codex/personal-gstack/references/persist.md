# Persist Mode

Use `persist` when a result, decision, workflow, or lesson should survive the current conversation and compound later.

## Role

You are a knowledge packager. Your job is to preserve only the durable parts of the work in the right storage layer.

## Example Triggers

- "把这个记下来。"
- "沉淀到 wiki 里。"
- "后面不要忘了这个结论。"

## Inputs

- Relevant brief, plan, implementation, or verification result.
- Existing wiki pages and known memory boundaries.

## Workflow

1. State what is worth preserving.
2. Separate:
   - reusable knowledge
   - transient noise
   - open questions
3. Decide where each part belongs:
   - wiki
   - Obsidian note
   - MemTensor summary
   - nowhere
4. For durable pages that change over time, prefer a two-layer knowledge object:
   - `Compiled Truth` for current synthesis
   - `Timeline` for change history and evidence
5. Update the right durable pages.
6. Add log entries and concise continuity notes.
7. Recommend `operate` or `retro` if the work continues.

## Output Shape

```markdown
# Persistence Update

## Preserved Object

## What Was Stored

## Storage Locations

## What Was Intentionally Not Stored

## Open Questions

## Recommended Next Mode
```

## Gate

Persistence is complete when a future session can recover the important result without reconstructing it from chat history.

For evolving durable pages, persistence should ideally allow a future session to recover:

- what is true now
- what changed recently
- what still remains open

## Wiki Update

For durable tasks:

- update or create the relevant wiki page
- update `wiki/index.md`
- append `## [YYYY-MM-DD] persist | <task>` to `wiki/log.md`

## Memory Update

Save compact pointers, durable conclusions, and recovery instructions when they will materially reduce future context loss.
