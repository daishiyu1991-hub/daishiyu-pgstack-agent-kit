# Team Memory Standard

## Core Rule

Team memory should hold compiled operating knowledge, not workflow exhaust.

## Allowlist

- `business`
- `ai_knowledge`
- `skills`

Examples:

- durable business truths
- reusable AI workflow patterns
- pipeline templates and graduation decisions
- source-quality judgments
- review outcomes that changed future practice
- stable skill rules and governance rules

## Denylist

- raw user turns by default
- personal preferences unless promoted into a team rule
- host-specific model choices or local runtime defaults
- temporary status updates
- conversational wrappers such as `我查到了`, `你说得对`, or `行，那先按兵不动`
- `Review the conversation above...`
- `Nothing to save.`
- `Saved to memory.`
- `There is something worth saving...`
- `Worth saving...`
- greetings, acknowledgements, and command noise
- long incident transcripts that have not been rewritten

## Team Knowledge Base Rule

`team_shared` is the curated team knowledge base.

It should contain only memories that can be cleanly classified as:

- `business`
- `ai_knowledge`
- `skills`

If a memory is useful but does not fit one of these domains, do not let it enter `team_shared`.

Keep it:

- local
- in `team_candidate`
- or in the pgstack ops/runbook surface:
  - `$PGSTACK_HOME/wiki/runbooks/`

## Minimum Gate

A team-facing memory should be:

- durable
- reusable
- compact
- non-sensitive
- tied to a source of truth

## Promotion Ladder

- `personal`
- `local_pgstack`
- `team_candidate`
- `team_shared`

Default behavior:

- keep it local if unclear
- rewrite if useful but noisy
- share only when compact and governed

## Local vs Remote Rule

When a Hub connection exists, cleanup has two layers:

- local state
- remote team list

Fixing only one layer can leave the team page looking dirty.

## Backing Source Gate

If a team-facing memory depends on a runbook, policy page, or core synthesis page, that backing page should clearly distinguish:

- the current rule or protocol
- the historical incident or change record

If it does not, treat the item as:

- `needs_rewrite`
- `team_candidate`
- or `reroute`

rather than clean `team_shared`.
