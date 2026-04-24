---
name: team-kb-curator
description: Curate the MemTensor team knowledge base as a narrow shared library. Keep only business, ai_knowledge, and skills in team_shared; rewrite, reroute, or flag everything else; and update the pgstack wiki when the operating model changes.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [team-memory, knowledge-base, memtensor, obsidian, curation, pgstack]
    category: research
    related_skills: []
---

# Team Knowledge Base Curator

This skill is the portable Hermes runtime for ongoing curation of the Personal GStack
team knowledge base.

Use it for unattended daily or periodic runs when Hermes should keep the shared team
layer clean, compact, and useful.

## Mission

Treat `team_shared` as a curated team knowledge base, not as a generic memory stream.

Only these three `kb_domain` classes belong in the shared shelf:

- `business`
- `ai_knowledge`
- `skills`

Everything else should be:

- kept local
- staged as `team_candidate`
- rewritten into a compact allowed-domain object
- rerouted to the pgstack runbook surface when available:
  - `$PGSTACK_HOME/wiki/runbooks/`
- or flagged for admin review

## Preferred Surfaces

When available, inspect both:

1. the live MemTensor shared surface
2. the local Personal GStack wiki

Canonical local wiki:

```text
$PGSTACK_HOME
```

If the local vault is mounted, read these first when they exist:

- `wiki/syntheses/personal-gstack-team-knowledge-base-operating-model.md`
- `wiki/syntheses/personal-gstack-memtensor-team-space-cleanup-policy.md`
- `wiki/syntheses/personal-gstack-team-memory-skill-usage-guide.md`
- `wiki/index.md`
- recent `wiki/log.md`

If the vault is not mounted, follow the rules embedded in this skill directly and
emit a concise curation report instead of assuming a wiki write is possible.

## Cron Discipline

For unattended cron runs, stay narrow and deterministic.

- Do **not** load or invoke the generic `llm-wiki` skill.
- Do **not** run broad `search_files` passes across the whole wiki.
- Do **not** run broad `grep`, `find`, or whole-vault Obsidian searches.
- Do **not** invoke generic wiki lint behavior unless the user explicitly asked for a wiki audit.
- Read the specific policy pages, `wiki/index.md`, and recent `wiki/log.md` first.
- Only do one small targeted lookup if a concrete ambiguity blocks a safe curation decision.
- If nothing materially changed, return `[SILENT]` quickly.

When the cron job provides script output from `team-kb-curator-context.py`, treat
that output as the canonical local wiki context for the run. Use live
MemTensor/team-memory tools only for the memory delta itself; do not rediscover
the pgstack operating model by searching the vault.

Hard runtime budget:

- finish the no-op path in under 90 seconds when there is no meaningful memory delta
- prefer one compact final report over exploratory analysis
- if a broad audit feels necessary, report `BLOCKED: needs supervised Codex audit`
  instead of trying to do it inside unattended Hermes cron

## Obsidian Compile Contract

This skill should still compile durable changes into the Obsidian-backed `pgstack` wiki.

It does **not** need the generic `llm-wiki` runtime skill to do that.

For this curator workflow, "compile into Obsidian" means:

1. read the named canonical pages
2. update only the directly relevant page when the operating model or recurring pattern truly changed
3. update `wiki/index.md` only if navigation changed
4. append a concise entry to `wiki/log.md`
5. keep all edits compatible with the existing `llm-wiki` schema and wikilink style

In other words:

- keep the **llm-wiki pattern**
- avoid the **generic llm-wiki heavy search/lint workflow**

Use the local `pgstack` wiki as a narrow known surface, not as a giant open-ended wiki to explore.

## Core Workflow

### 1. Inspect

Review newly available shared knowledge, new candidate memories, and recent durable
pgstack notes that may deserve promotion.

### 2. Classify

Put each candidate into one of these buckets:

- `keep`
- `rewrite`
- `reroute`
- `keep-local`
- `unshare`
- `flag-admin`

### 3. Apply The Gate

A team-facing memory must be:

- durable
- reusable
- compact
- non-sensitive
- traceable to a source of truth

If any of those are missing, do not let it stay in the curated team shelf unchanged.

### 4. Enforce The Team KB Boundary

Only publish or keep shared items that clearly fit one of:

- `business`
- `ai_knowledge`
- `skills`

Default denylist examples:

- personal model choices
- host-specific defaults
- one-machine setup notes
- operational cleanup diaries
- long troubleshooting transcripts
- support-chat style replies
- raw transcript fragments
- save-review prompts
- temporary status chatter

### 5. Rewrite Before Promotion

Rewrite worthwhile material into this shape:

```text
context
-> durable conclusion
-> why it matters
-> recovery pointer
-> kb_domain
-> source of truth
```

One primary rule per shared memory is better than one long mixed incident writeup.

### 6. Replace, Do Not Pile Up

When a compact rewrite supersedes a verbose shared memory:

1. create the compact replacement
2. publish the replacement
3. unshare or downgrade the verbose original when ownership permits
4. record the change in the local wiki/log when available

### 7. Respect Ownership

If noisy shared content belongs to another member:

- do not pretend local cleanup is enough
- flag it for owner or admin review
- capture a short moderation note if helpful

## Output Contract

For unattended runs, return a compact curation report with:

1. what was inspected
2. what was kept
3. what was rewritten
4. what was rerouted or downgraded
5. what needs admin review
6. whether the operating model or wiki was updated

If no meaningful action is needed, say so briefly without padding.

## Safe Operating Rules

- Keep the shared shelf narrow.
- Prefer replacement over accumulation.
- Do not bulk-publish from generic local continuity memory.
- Do not delete or unshare another member's item unless you clearly have authority.
- When in doubt, stage as `team_candidate` or keep local.
- If the shared layer starts to feel like a timeline, tighten the gate instead of
  broadening the shelf.
