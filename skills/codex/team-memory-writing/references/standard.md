# Team Memory Writing Standard

## Core Rule

Write the memory future operators need, not the transcript you happen to have.

## Good Team Memory

A team memory should be:

- durable
- reusable
- compact
- non-sensitive
- linked to a source of truth

For the curated team knowledge base, it should also belong clearly to one of:

- `business`
- `ai_knowledge`
- `skills`

## Default Shape

```text
situation
-> durable conclusion
-> why it matters
-> recovery pointer
-> source of truth
```

## One Rule Per Memory

Prefer one crisp rule over a bundled paragraph of loosely related observations.

## Exclusions

Do not write:

- raw user turns
- personal preferences unless promoted into team policy
- host-specific model selections or local defaults
- temporary status reports
- conversational wrappers and spoken-style filler
- save-review prompts
- noop outcomes
- long chat transcripts
- command logs
- speculation that was not verified

## Promotion Hint

- local if it is still personal or unclear
- team_candidate if useful but not yet fully governed
- team_shared only when compact and source-linked

## Knowledge-Base Boundary

Do not publish to `team_shared` unless you can assign a clear `kb_domain`:

- `business`
- `ai_knowledge`
- `skills`

If the item is mainly:

- personal configuration
- local runtime behavior
- operational cleanup
- infra troubleshooting play-by-play

keep it local, stage it in `team_candidate`, or reroute it to:

- `$PGSTACK_HOME/wiki/runbooks/`

until it is rewritten into durable knowledge that fits one of the three domains.

## Source Page Quality Gate

If a shared memory depends on a durable source page such as:

- a team-facing policy page
- a runbook
- a core synthesis page

that source page should clearly separate:

- what is true or operative now
- what changed or happened historically

If the source page still mixes current rule and historical incident material together, prefer:

- local
- `team_candidate`
- or `reroute`

until the source page is rewritten into a cleaner durable object.
