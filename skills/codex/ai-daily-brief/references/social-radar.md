# Social Radar

This layer exists to catch weak signals early without polluting the final daily brief.

## Role

`social-radar` is a discovery layer, not a publishing layer.

Use it to notice:

- major announcements before the official blog or docs feed updates
- keynote clips or product demos that point to a same-day launch
- GitHub release or maintainer posts that reveal a meaningful new capability
- important discussion spikes around a new model, tool, benchmark, or policy move

Do not use it to treat social chatter as settled fact.

## Expanded Pipeline

The production brief should now be understood as:

```text
social-radar
-> official-confirm
-> deterministic candidate bundle
-> Hermes ranking + writing
-> Feishu digest + Obsidian deep report
-> optional NotebookLM research brief
```

The unattended Hermes runtime still starts from the deterministic candidate bundle. `social-radar` is a sidecar discovery layer until a stable collector exists.

Current GitHub rule:

- prefer official `repo release feeds` when available
- treat `org activity feeds` as a weaker fallback signal
- do not let org-activity events outrank a repo release pointing at the same underlying artifact

## Good Social Inputs

Prefer sources that point to an underlying artifact:

- official company or lab accounts
- official YouTube channels or keynote uploads
- official GitHub repos, releases, and maintainer announcements
- technical staff posts that link to a paper, repo, demo, model card, or official page
- Hacker News or Reddit only when they surface a concrete artifact worth confirming

## Weak Or Unsafe Inputs

Do not promote these directly into the final brief:

- leaks
- rumor accounts
- repost farms
- screenshots without a source artifact
- hot takes without a linked announcement, paper, demo, docs page, or repo

## Confirmation Rule

A social signal is only eligible for the final daily brief if it is confirmed by one of:

1. an official announcement page
2. official docs or release notes
3. a model card or paper page
4. an official repo or release entry
5. a first-party product page or API update page

If no primary source is available but the signal is still strategically important, allow one high-credibility secondary source and label it `二手源`.

## Suggested Social Watchlist

Good candidates for future sidecar monitoring:

- X accounts for major labs and founders
- official YouTube channels for OpenAI, Google DeepMind, Anthropic, NVIDIA, Microsoft, Meta, Qwen, DeepSeek
- GitHub release feeds for major model and agent repos
- selective Reddit / Hacker News threads only after an artifact has been identified

## Output Of This Layer

The output should be a small queue of candidate signals, each with:

- actor
- post URL
- timestamp
- one-sentence claim
- linked artifact if present
- confirmation status

Useful confirmation statuses:

- `official_repo_release`: already confirmed by an official GitHub release feed
- `needs_official_confirm`: still needs a first-party page beyond the social signal

Only confirmed items should be promoted into the main candidate bundle or the final brief.

After confirmation, use `references/triage.md` to decide whether the item:

- stays in the daily brief only
- gets a separate research brief
- becomes part of a long-running topic notebook
