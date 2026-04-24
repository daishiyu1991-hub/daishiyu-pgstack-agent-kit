---
name: ai-daily-brief
description: Define, tune, or dry-run a Hermes-operated daily AI intelligence brief that filters high-signal model, product, research, open-source, policy, and capital updates into a Chinese Feishu summary plus an Obsidian deep report. Use when maintaining the brief's workflow, source map, ranking rules, formatting, or quality bar.
---

# AI Daily Brief

This skill is the editable Codex-side spec for the daily AI brief. Hermes is the runtime. Codex keeps the workflow, source hierarchy, formatting rules, and acceptance bar easy to inspect and revise.

## Runtime Boundary

- `Codex`: authoring surface for the brief's logic, source map, templates, and QA rules.
- `Hermes`: scheduled runtime that gathers updates, writes the Obsidian note, and delivers the Feishu DM summary.

When you change the brief's behavior, keep the Hermes runtime skill aligned with this spec:

```text
$HERMES_HOME/skills/research/ai-daily-brief
```

## When To Use

Use this skill when you need to:

- adjust the daily brief's source priorities or filters
- change the Feishu or Obsidian output format
- tighten or loosen the signal threshold
- inspect why a run included or excluded an item
- dry-run the brief manually before changing Hermes automation
- run Level 2 validation that writes a full test Obsidian report without Feishu delivery or production state updates

## Authoring Workflow

1. Read `references/sources.md` for source tiers, signal criteria, exclusions, and fallback rules.
2. Read `references/format.md` for the Feishu digest template and the Obsidian deep-report template.
3. Read `references/social-radar.md` and `references/social-watchlist.md` when changing discovery-layer behavior for social or community signals.
4. Read `references/notebooklm-brief.md` when changing the deeper research handoff into NotebookLM or the downstream brief format.
5. Read `references/triage.md` when deciding whether a confirmed item should stay in the daily brief only, become a deeper research brief, or be promoted into a long-running topic notebook.
6. Update rules conservatively. Prefer clearer ranking and filtering over adding more sources.
4. Keep the runtime contract stable:
   - Chinese output
   - Feishu gets the compact digest
   - Obsidian gets the full report
   - dry-run mode writes only to the dedicated dry-run note path
   - every item must carry a source link
   - secondary-only sourcing must be marked `二手源`
   - Hermes should prefer deterministic collector inputs before doing open web search
6. If the behavior changes materially, mirror that change in the Hermes runtime skill and cron prompt.

## Daily Brief Contract

The brief is not a full news crawl. It is a high-signal AI intelligence digest.

Required behavior:

- prioritize official and primary sources
- treat social signals as discovery inputs, not final truth
- deduplicate the same event across multiple writeups
- cap total coverage at roughly `10-15` items
- explain why each kept item matters
- allow light-news days to stay light

Explicitly avoid:

- rumor and unverified leaks
- pure reposts or SEO summaries
- low-signal wrapper launches
- padding the digest to hit an arbitrary count
- letting social-media chatter bypass official confirmation into the final digest

GitHub nuance:

- official repo release feeds can count as confirmation-quality sources
- generic GitHub org activity feeds are still discovery signals only

## Quality Gate

Before accepting a change to the brief, verify that it still produces:

- a Feishu digest that can be read in `2-3` minutes
- an Obsidian report that can be read in `5-8` minutes
- clear sectioning across product/model, research, open source, and policy/capital
- source attribution on every item
- a visible distinction between fact and interpretation

## Dry-Run Validation

Use dry-run mode before touching the live daily automation when you need to test report generation safely.

Required dry-run behavior:

- run the collector with `--dry-run`
- write to `$HOME/Documents/PGStack/AI Daily Brief/Dry Runs/YYYY/YYYY-MM-DD AI Daily Brief Dry Run.md`
- do not write the official daily note
- do not update `$HERMES_HOME/state/ai-daily-brief/last_success.json`
- do not send Feishu
- mark outputs as `dry-run`

## References

- Source strategy: [references/sources.md](references/sources.md)
- Output templates: [references/format.md](references/format.md)
- Social radar layer: [references/social-radar.md](references/social-radar.md)
- Social radar watchlist: [references/social-watchlist.md](references/social-watchlist.md)
- NotebookLM handoff: [references/notebooklm-brief.md](references/notebooklm-brief.md)
- Triage rules: [references/triage.md](references/triage.md)
