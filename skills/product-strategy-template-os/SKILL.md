---
name: product-strategy-template-os
description: Run a fixed-template consumer-product strategy research pipeline from category signal to product planning. Use when Codex should reproduce the wake-up-light style workflow: chapter-by-chapter template routing, evidence acquisition, zero-hallucination reporting, red-team review, human decision stops, low-saturation HTML reports, process JSON ledgers, and reusable example artifacts for Amazon/consumer-electronics category research.
---

# Product Strategy Template OS

This skill runs a fixed-template category strategy research pipeline without drifting between chapters. It is designed for consumer electronics and Amazon-led category research, but it can be adapted to other physical-product categories.

The operating philosophy is:

```text
AI collects and organizes static quality.
Human judges dynamic quality.
The pipeline never turns evidence into an automatic product decision.
```

## When To Use

Use this skill when the user asks to:

- start a category strategy research run from a keyword, product category, ASIN, or template;
- reproduce the wake-up-light workflow or a `爆品战略用研` workflow;
- create one chapter at a time with complete HTML reports and process files;
- keep data 100% traceable and mark missing evidence honestly;
- force human decisions before unlocking the next chapter.

Do not use this skill for quick one-off market summaries unless the user explicitly wants the full template pipeline.

## Required Inputs

Minimum:

- category or seed keyword;
- marketplace or target channel;
- the fixed template to follow, or permission to use the default 7-chapter template;
- output run directory.

Recommended:

- 1-3 seed ASINs;
- uploaded ABA/reverse keyword exports, review exports, market-product exports, supplier quotes, or BOM sheets;
- known company capability boundaries;
- preferred data tools/MCPs.

## Global Files

Read `references/global-rules.md` at the start of every strategy-research run. It is the portable global contract for this pipeline.

If the user wants this workflow to become the default behavior inside a project or workspace, copy or adapt `assets/AGENTS.product-strategy-template-os.example.md` into that project's `AGENTS.md`. That file is not loaded automatically by the skill installer; it is a portable global-rule template.

## Core Loop

For every chapter, run this exact loop:

```text
1. Template Router
2. Chapter Preamble
3. Evidence Contract
4. Evidence Acquisition Router
5. Processing Framework: Input -> Processing -> Output
6.補證 Review
7. Red-team Argue
8. Complete HTML Report
9. Human Decision Stop
10. Artifact & Memory Ledger
```

The chapter page is not complete until it has a field-level evidence audit, a red-team section, and a human decision stop.

## Architecture

Read `references/pipeline-architecture.md` before changing the pipeline, creating a new run type, or explaining how the skill keeps a long research project consistent across chapters.

The architecture has three layers:

- governance architecture: global rules -> skill runtime -> run architecture -> checkpoint ledger -> artifacts -> memory;
- complete-report architecture: previous artifact review + latest evidence + red-team + human decision in one primary report;
- node-loop protocol: every template node runs its own `Input -> Processing -> Output -> review -> red-team -> revised conclusion` cycle.

## Default Template

Use the default seven chapters unless the user provides another template:

```text
1. 品类本质小结
2. 市场竞争分析
3. 头部品牌竞争&竞品分析
4. 用户场景&需求分析
5. 营销分析&社媒传播
6. 供应链管理
7. 产品规划
```

Read `references/template-structure.zh.md` before creating a chapter execution plan.

## Non-Negotiable Rules

- Do not skip from a chapter to a later chapter because the later topic feels useful.
- Do not write a conclusion before the evidence router has run.
- Do not fabricate data, ASINs, quotes, prices, supplier facts, growth rates, reviews, or citations.
- Missing data must be written as `not_collected`, `manual_required`, `not_available_in_current_session`, or `unknown`.
- Inferred claims must be labeled as inference.
- Every chapter gets one primary complete report. Older drafts are process history, not the main report.
- The index page is a roadmap, not a decision page. Keep it stable after accepted.
- Do not unlock the next chapter without explicit human choice.
- If a user chooses `pause`, write a decision record and do not unlock the next chapter.

## Evidence Routing

Read `references/data-source-router.md` when deciding how to collect evidence.

Default routing categories:

- `mcp_available`: use available MCP/API tools first.
- `browser_required`: inspect frontstage pages, listing images, A+, video, five bullets, coupons, official sites, or channel pages.
- `uploaded_file_required`: use spreadsheets, docx, PDFs, review exports, ABA exports.
- `manual_input_required`: supplier quotes, MOQ, tooling, internal BOM, factory capability, offline truth.
- `web_research_required`: public market reports, official brand pages, independent reviews.
- `not_collectable_now`: unavailable tools, blocked auth, or missing credentials.

Record source provenance for every evidence packet:

```text
source_type
source_ref
collected_at
raw_available
transformation
confidence
```

## Red-Team Basis

Read `references/red-team-company-baseline.md` when the research has company-fit implications.

Default company-fit red-team questions:

- Does this opportunity fit a quality-led company rather than a lowest-cost seller?
- Can the team win through real product/marketing strength without gray-hat tactics?
- Which capabilities are internal strengths, and which require ODM/external suppliers first?
- Does the opportunity still work if competitors copy the visible feature?

## Artifacts

Each run should have:

```text
quality-review-index.html
quality-review-template-ch{n}-execution-plan-v1.html
quality-review-template-ch{n}-{slug}-complete-v1.html
process/
  pipeline-run-state-v1.json
  section{n}-execution-plan-v1.json
  section{n}-{slug}-evidence-v1.json
  section{n}-{slug}-analysis-v1.md
  section{n}-human-decision-*.json
```

If GBrain is available, write only compact durable outputs or queue them in `process/gbrain/`. Do not write raw supplier secrets or every HTML draft into memory.

## Frontend Output

Read `references/frontend-report-style.md` before rendering HTML.

Default visual style:

- Chinese report;
- conclusion first, process below;
- low-saturation colors;
- quiet typography;
- enough charts/tables for judgment;
- sources at the bottom like a paper;
- no modal popups in HTML unless the user asks; collect decisions in Codex when possible.

## Scripts

- `scripts/init_run.py`: create a new run skeleton with index, process state, and chapter placeholders.
- `scripts/sanitize_check.py`: scan the skill package for common secrets before publishing.
- `scripts/validate_run.py`: validate a run folder has the required state, decision, evidence, and report files.

## Stability Files

For stable pipeline operation, this skill ships:

- `schemas/`: JSON schemas for run state, evidence ledgers, human decisions, and execution plans.
- `templates/`: reusable starter files for index, complete reports, execution plans, evidence ledgers, decisions, and GBrain sync queues.
- `references/global-rules.md`: portable global rules.
- `references/pipeline-architecture.md`: full architecture.
- `gbrain/`: native GBrain handoff packet and brain-ready pages for Hermes-admin.

## Example

Use `examples/wake-up-light/` as the reference case for how the artifacts fit together. It is a sanitized example of the workflow shape, not a claim that future runs should copy its conclusions.

## Publishing

This folder is installable as a Codex skill from GitHub when the repository root is this skill folder or when the installer points to this subdirectory.

Expected install pattern:

```bash
npx skills add https://github.com/<owner>/<repo> --skill product-strategy-template-os
```

If the installer expects the skill at repo root, publish this folder as the repository root.
