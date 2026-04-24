# Output Format

The daily brief has two outputs with different jobs.

An optional third artifact can be produced for deeper follow-up:

- `NotebookLM Research Brief`

## Feishu DM Digest

Audience goal: fast scan in `2-3` minutes.

Structure:

```md
# AI Daily Brief | YYYY-MM-DD

今日最重要的 3-5 条：

1. 标题
   - 为什么重要：一句话讲影响
   - 链接：URL

2. 标题
   - 为什么重要：一句话讲影响
   - 链接：URL

3. 标题
   - 为什么重要：一句话讲影响
   - 链接：URL

完整深度版：
$HOME/Documents/PGStack/AI Daily Brief/YYYY/YYYY-MM-DD AI Daily Brief.md
```

Rules:

- keep only the most important `3-5` items
- every item must include `为什么重要`
- every item must include a source link
- end with the Obsidian note path

## Obsidian Deep Report

Audience goal: deeper read in `5-8` minutes.

Structure:

```md
# AI Daily Brief | YYYY-MM-DD

时间窗：START -> END

## 今日最重要的 5 条

### 标题
- 为什么重要：...
- 事实：...
- 链接：...

## 模型 / 产品发布

- 标题
  - 为什么重要：...
  - 链接：...

## 研究 / 论文

- 标题
  - 为什么重要：...
  - 链接：...

## 开源 / 工具 / Agent

- 标题
  - 为什么重要：...
  - 链接：...

## 资本 / 政策

- 标题
  - 为什么重要：...
  - 链接：...

## 今日判断

一段话，总结今天真正值得注意的趋势或竞争态势。

## 全部原始链接

- 标题：URL
- 标题：URL
```

Rules:

- total kept items should usually stay within `10-15`
- the top section should emphasize the day's true center of gravity
- use `二手源` labels where needed
- keep interpretation short and clearly separated from facts

## Optional NotebookLM Research Brief

Audience goal: deeper topic analysis when one story deserves a second pass.

Use this only for selected high-value topics, not for every day.

Structure:

```md
# Topic Research Brief | YYYY-MM-DD

## Topic

## Confirmed Sources

- 标题：URL

## What Changed

## Why It Matters

## Competing Interpretations

## Open Questions

## What To Watch Next
```

Rules:

- only use confirmed sources or clearly labeled `二手源`
- keep this artifact separate from the main daily brief
- prefer topic-specific notes over giant omnibus notebooks
