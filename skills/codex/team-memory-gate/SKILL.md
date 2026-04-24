---
name: team-memory-gate
description: Govern what enters the curated MemTensor team knowledge base. Use when deciding whether a memory should stay local, become team_candidate, become team_shared, be rewritten into compact knowledge, or be unshared because it is noisy, personal, operational, or overlong.
metadata:
  short-description: Gate, rewrite, and clean team-facing memory
---

# Team Memory Gate

Use this skill when the team layer should behave like a knowledge base instead of "save everything and hope retrieval sorts it out."

This skill is for:

- deciding whether a memory belongs in `local_pgstack`, `team_candidate`, or `team_shared`
- rewriting long material into compact business, AI, or skill knowledge
- identifying denylist content that should not be team-facing
- cleaning up noisy shared memories from the live Hub
- reviewing whether a team memory has enough evidence and source-of-truth support

## Read First

Load these references before making a promotion or cleanup decision:

1. `references/standard.md`
2. `references/rewrite-examples.md` when replacing or compressing a memory

If the work touches the canonical wiki, also read:

- `$PGSTACK_HOME/wiki/syntheses/personal-gstack-memtensor-team-space-cleanup-policy.md`

## Workflow

### 1. Inspect The Right Surface

When a live Hub connection exists, check both:

- local `team_shared_chunks`
- remote Hub memory list

Do not assume the team page is driven only by local DB state.

### 2. Classify The Candidate

Put the memory in one of four buckets:

- `deny`: should not be team-facing
- `rewrite`: useful idea, wrong current form
- `promote`: ready for `team_shared`
- `keep-local`: valuable, but not ready for team-facing use
- `reroute`: useful, but belongs in local/ops/runbook rather than the curated team knowledge base

### 3. Apply The Gate

A memory can become team-facing only if it is:

- durable
- reusable
- compact
- non-sensitive
- linked to a source of truth

If any of those are missing, rewrite it or keep it local.

For `team_shared`, it must also fit one of:

- `business`
- `ai_knowledge`
- `skills`

### 4. Rewrite Before Promotion

If the memory is useful but noisy, rewrite it into this shape:

```text
context
-> durable conclusion
-> why it matters
-> recovery pointer
-> scope
-> kb_domain
-> source of truth
```

Prefer one compact operating memory over a long incident transcript.

### 5. Replace, Do Not Pile Up

When a new compact rewrite supersedes an old verbose shared memory:

1. create the compact rewrite
2. share the replacement
3. unshare the verbose original
4. record the change in the local wiki/log

Do not leave both versions hanging around unless the long version is still the canonical source.

### 6. Respect Ownership Boundaries

If the noisy memory belongs to another team member, do not pretend local cleanup is enough.

Escalate as:

- owner cleanup
- admin moderation
- shared policy update

## Practical Denylist

Default denylist items include:

- raw user turns by default
- save-review prompts
- `Review the conversation above...`
- `Nothing to save.`
- `Saved to memory.`
- `There is something worth saving...`
- `Worth saving...`
- transient command noise
- long uncompiled troubleshooting transcripts
- personal model choices
- one-host defaults
- cleanup diaries
- support-chat style replies

Operational incident knowledge that has not yet been rewritten into `business`, `ai_knowledge`, or `skills` should be rerouted, not published.

## Output Expectation

When you use this skill, produce:

- the promotion decision
- the reason
- the rewritten memory if needed
- the proposed `kb_domain` if relevant
- the source-of-truth pointer
- the cleanup action if an old shared memory should be removed

## Related Files

- `$PGSTACK_HOME/wiki/syntheses/personal-gstack-memtensor-team-space-cleanup-policy.md`
- `$PGSTACK_HOME/wiki/syntheses/personal-gstack-memory-promotion-policy.md`
- `$PGSTACK_HOME/wiki/syntheses/personal-gstack-team-sharing-model.md`
- `$PGSTACK_HOME/wiki/syntheses/personal-gstack-team-knowledge-base-operating-model.md`
