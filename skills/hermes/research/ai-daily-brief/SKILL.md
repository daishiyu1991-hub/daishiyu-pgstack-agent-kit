---
name: ai-daily-brief
description: Gather the highest-signal AI developments since the previous successful run, write a Chinese deep report into Obsidian, and return a compact Feishu-ready daily summary. Use for unattended Hermes cron runs and manual Hermes dry-runs.
version: 1.0.0
metadata:
  hermes:
    tags: [AI, Daily-Brief, Obsidian, Feishu, Research]
---

# AI Daily Brief

This skill is the Hermes runtime for the daily AI intelligence brief.

- The final response is the Feishu DM digest.
- The full report must be written to the Obsidian note path provided by the injected run context.
- Work in Chinese.

## Runtime Inputs

The cron job injects a script output block before each run. Read it first. It provides:

- `AI_DAILY_BRIEF_NOW`
- `AI_DAILY_BRIEF_WINDOW_START`
- `AI_DAILY_BRIEF_WINDOW_MODE`
- `AI_DAILY_BRIEF_DATE`
- `AI_DAILY_BRIEF_NOTE_PATH`
- `AI_DAILY_BRIEF_STATE_PATH`
- `AI_DAILY_BRIEF_BUNDLE_PATH`
- `AI_DAILY_BRIEF_SOCIAL_RADAR_PATH`
- `AI_DAILY_BRIEF_DRY_RUN`
- `AI_DAILY_BRIEF_SEND_FEISHU`
- `AI_DAILY_BRIEF_UPDATE_PRODUCTION_STATE`
- `AI_DAILY_BRIEF_PRODUCTION_STATE_PATH`

Run the exact export block from the injected context before writing files, then read the bundle file immediately:

```bash
cat "$AI_DAILY_BRIEF_BUNDLE_PATH"
```

Treat that bundle as the default source of truth for candidate items.
Use the bundle fields directly: `source`, `title`, `summary`, `url`, `published`, `category_hint`, and `tags`.

If `AI_DAILY_BRIEF_SOCIAL_RADAR_PATH` exists, you may read it after the main bundle as a secondary discovery sidecar:

```bash
cat "$AI_DAILY_BRIEF_SOCIAL_RADAR_PATH"
```

Use it carefully:

- social-radar items are discovery signals, not final facts
- do not let a social-radar item enter the final digest without official confirmation
- entries marked `confirmation_status: official_repo_release` are already anchored in an official GitHub release feed and may be used as confirmed sources when they are clearly material
- entries marked `confirmation_status: needs_official_confirm` still require a separate official page, release note, model page, docs update, or product page before promotion
- if the main bundle already gives you enough strong confirmed material, do not expand scope just because the social sidecar exists

## Signal Bar

This brief is not a full news crawl. Keep only high-signal developments.

Prioritize:

1. major model, API, product, or platform releases
2. major research or open-source advances with practical impact
3. distribution, pricing, ecosystem, or infrastructure moves
4. capital or policy shifts with real downstream consequences

Exclude:

- rumor and unverified leaks
- pure reposts
- low-quality SEO summaries
- small wrapper launches without broader importance
- padded filler on light-news days

## Source Rules

- Prefer official and primary sources first.
- If a primary page is blocked, use an accessible official mirror, RSS page, blog page, release note, or model card.
- If you must rely on a secondary source, label it `二手源`.
- Deduplicate the same event across multiple sources and keep one primary anchor link.

## Deterministic First Workflow

This skill must finish within a reasonable cron window. Use the injected bundle first and only supplement when genuinely needed.

1. Read `AI_DAILY_BRIEF_BUNDLE_PATH`.
2. Start from those candidates for deduping, ranking, and writing.
3. If `candidate_count >= 4`, do not search and do not fetch candidate pages.
4. Only if `candidate_count < 4`, do at most `1` supplemental search.
5. Do not `curl` or otherwise fetch individual candidate article pages unless the bundle is missing a usable title and summary for a single must-cover item.
6. Never paste raw HTML into your working context.
7. Skip blocked pages instead of retrying them.
8. Light-news days are valid. Do not keep searching just to reach a quota.

Do not use browser tools for this workflow.

## Output Contract

### Dry-Run Mode

If `AI_DAILY_BRIEF_DRY_RUN=1`:

- write the Obsidian report only to `AI_DAILY_BRIEF_NOTE_PATH`
- treat the final response as a digest draft, not a Feishu delivery payload
- do not update `AI_DAILY_BRIEF_PRODUCTION_STATE_PATH`
- do not write the official daily-note path
- do not send Feishu
- if a state file must be written, write only to `AI_DAILY_BRIEF_STATE_PATH`, which is a dry-run state path
- clearly mark the note and final response as `dry-run`

For deterministic structure checks, this helper can write a full test note from the existing bundle:

```bash
python3 $HERMES_HOME/skills/research/ai-daily-brief/scripts/write_dry_run_report.py
```

### Feishu Final Response

Return only the compact digest:

- title line with the date
- `3-5` most important items
- each item must include `为什么重要` and a link
- end with the Obsidian note path

### Obsidian Note

Write the full report to `AI_DAILY_BRIEF_NOTE_PATH` with these sections:

1. title and date
2. time window
3. `今日最重要的 5 条`
4. `模型 / 产品发布`
5. `研究 / 论文`
6. `开源 / 工具 / Agent`
7. `资本 / 政策`
8. `今日判断`
9. `全部原始链接`

Target total coverage: `10-15` items maximum.

## Safe Unattended Execution

Cron runs without a human present. Stay inside simple, safe commands.

Prefer:

- `curl`
- `rg`
- `sed`
- `find`
- `mkdir`
- `cat`
- `date`
- `web_search` for strictly limited supplemental checks
- `web_extract` for strictly limited supplemental checks

Avoid:

- destructive commands
- package installs
- login or auth flows
- `python -c`
- commands that require manual approval
- `browser_navigate` and the rest of the browser toolchain for routine source gathering
- bulk page fetching across candidate URLs

## File Writing Pattern

Use shell-friendly writes. Quote all paths because the vault path contains spaces.

```bash
NOTE_DIR="$(dirname "$AI_DAILY_BRIEF_NOTE_PATH")"
mkdir -p "$NOTE_DIR"
cat > "$AI_DAILY_BRIEF_NOTE_PATH" <<'EOF'
...final markdown note...
EOF
```

After the Obsidian note is written successfully, update the state file:

```bash
STATE_DIR="$(dirname "$AI_DAILY_BRIEF_STATE_PATH")"
mkdir -p "$STATE_DIR"
cat > "$AI_DAILY_BRIEF_STATE_PATH" <<EOF
{"last_success_end":"$AI_DAILY_BRIEF_NOW","last_note_path":"$AI_DAILY_BRIEF_NOTE_PATH"}
EOF
```

Only update the state file after the note content is complete.
