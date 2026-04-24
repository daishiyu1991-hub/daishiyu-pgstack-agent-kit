---
name: team-memory-writing
description: Write curated team-knowledge-base memories for MemTensor. Use when turning work, discoveries, decisions, AI knowledge, or workflow lessons into compact shared knowledge that is reusable, source-linked, and safe to publish.
metadata:
  short-description: Write compact, publishable team knowledge
---

# Team Memory Writing

Use this skill when the goal is not "save the conversation," but "write the memory that future teammates and agents will actually want to retrieve."

This skill is for:

- writing new curated team-knowledge-base memories
- rewriting a local note into a publishable team knowledge object
- compressing a reusable AI or workflow lesson into one compact memory
- deciding whether a memory is ready for `team_candidate` or `team_shared`

It is not for dumping the latest conversation into a shared layer.

## Read First

Load:

1. `references/standard.md`
2. `references/examples.md`

If the memory changes policy or system behavior, also point back to the canonical wiki page.

## Core Standard

A good team memory is:

- durable
- reusable
- compact
- non-sensitive
- traceable to a source of truth

If it is missing one of those, it should stay local or be rewritten.

For `team_shared`, it must also fit one of the three allowed team-knowledge domains:

- `business`
- `ai_knowledge`
- `skills`

## Writing Pattern

Default structure:

```text
situation
-> durable conclusion
-> why it matters
-> recovery pointer
-> kb_domain
-> source of truth
```

Keep it to one primary rule per memory.

`team_shared` is an explicit publication surface, not automatic spillover from local memory capture.

## What To Exclude

Do not write team memory as:

- raw user turns
- full chat transcripts
- user-specific preferences unless they were explicitly promoted into a team rule
- host-specific model choices or local runtime defaults
- one-off status updates or temporary connectivity reports
- conversational wrappers such as `我查到了`, `你说得对`, or `行，那先按兵不动`
- operational cleanup diaries
- one-machine setup notes
- local incident play-by-play
- save-review prompts
- `Nothing to save.`
- `Saved to memory.`
- `There is something worth saving...`
- `Worth saving...`
- long command-by-command incident logs
- speculation that did not survive verification

## Compression Rule

When compressing a long incident:

1. remove the play-by-play
2. keep the condition that future operators will see again
3. state the conclusion plainly
4. include the next recovery move
5. assign the right `kb_domain`
6. point to the source of truth

## Promotion Rule

Use this ladder:

- `local_pgstack`
- `team_candidate`
- `team_shared`

Default to `team_candidate` when:

- the idea is useful but still needs review
- the source of truth is weak
- the wording is not yet compact enough

Keep it local when:

- it mainly describes one person's setup
- it encodes one machine's preferred model or local defaults
- it is mostly a conversational status update
- it depends on ephemeral timing rather than a stable recurring condition

Use `team_shared` only when all of these are true:

- the memory is compact
- the source of truth is clear
- the item clearly belongs to `business`, `ai_knowledge`, or `skills`

If the item is useful but operational, local, or still messy:

- keep it in `local_pgstack`
- or stage it as `team_candidate`

## Output Expectation

When using this skill, produce:

- the rewritten memory text
- the proposed scope
- the proposed `kb_domain`
- the source-of-truth pointer
- whether it is ready for `team_shared` now, should stay `team_candidate`, or should remain local

## Related Files

- `$CODEX_HOME/skills/team-memory-gate/SKILL.md`
- `$PGSTACK_HOME/wiki/syntheses/personal-gstack-memtensor-team-space-cleanup-policy.md`
- `$PGSTACK_HOME/wiki/syntheses/personal-gstack-memory-promotion-policy.md`
- `$PGSTACK_HOME/wiki/syntheses/personal-gstack-team-knowledge-base-operating-model.md`
