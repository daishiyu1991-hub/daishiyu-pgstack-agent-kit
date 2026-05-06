# Product Strategy Template OS Global Rules

These rules make Product Strategy Template OS the default behavior for product/category strategy research in this workspace.

Higher-priority system, developer, and explicit user instructions still win.

## Default Pipeline Mode

When the user asks for product/category strategy research, Amazon opportunity analysis, consumer-electronics product definition, or a `爆品战略用研` workflow, use the Product Strategy Template OS pipeline by default.

Do not answer with a loose market summary unless the user explicitly asks for a lightweight informal answer.

## Fixed Template

Use this chapter order unless the user provides another template:

```text
1. 品类本质小结
2. 市场竞争分析
3. 头部品牌竞争&竞品分析
4. 用户场景&需求分析
5. 营销分析&社媒传播
6. 产品规划
7. 供应链实现
8. 项目计划
```

Do not jump chapters. If a useful point belongs to a later chapter, record it as a later-chapter input.

## Mandatory Chapter Loop

Every chapter must run:

```text
Template Router
-> Chapter Preamble
-> Evidence Contract
-> Evidence Acquisition Router
-> Input -> Processing -> Output
-> Evidence Sufficiency Review
-> Red-team Argue
-> Complete HTML Report
-> Human Decision Stop
-> Decision Record
-> Index / Ledger Update
```

## Native GBrain Sync Boundary

GBrain sync is automatic at skill boundaries. Do not ask the human to request
sync each time.

At Product Strategy Template OS start and end, first use the original native
GStack/GBrain path:

```text
gstack-brain-sync / gstack-brain-enqueue
-> allowlisted projects/product-strategy-template-os/learnings.jsonl
-> GBrain sync/embed/query
```

If native `gstack-brain-sync` is unavailable, fall back to the Hermes Admin
handoff queue and clearly mark the cloud write as pending, not completed.

Ask the human only when native sync is not initialized, sync mode is `off`,
credentials/permissions are missing, or privacy/team-publication scope must be
chosen.

## Data Integrity

All factual claims must be source-backed.

Never fabricate data, ASINs, prices, reviews, quotes, sales, keyword volume, supplier facts, COGS, MOQ, tooling cost, or citations.

Use these labels for missing fields:

```text
not_collected
manual_required
not_available_in_current_session
unknown
```

Label inference as inference.

## Evidence Responsibility

The pipeline should automatically collect evidence from available MCP/API/browser/file routes. Do not ask the human whether to run standard evidence collection if the user has already told the pipeline to continue.

Ask the human only for:

- dynamic product judgment;
- supplier/offline truth;
- credentials/permissions;
- internal company capability boundaries;
- explicit decisions.

## Complete Report Requirement

The primary chapter output must be one complete report. It must include:

- conclusion first;
- key charts/tables;
- `Input -> Processing -> Output`;
- evidence review;
- red-team argue;
- human decision stop;
- sources at the bottom.

Raw evidence, debug logs, execution plans, and process docs stay outside the product index unless explicitly requested.

## Human Decision Stop

Do not unlock the next chapter without explicit human choice.

If the user chooses pause, record the pause and do not continue.

Write decision records into:

```text
process/section{n}-human-decision-*.json
```

## Index Contract

The index page is a roadmap, not a report. Once accepted, do not redesign it.

Allowed index changes:

- chapter status;
- chapter links;
- decision record links;
- concise summaries.

Blocked:

- reordering chapters;
- changing the accepted layout;
- adding AI product verdicts;
- adding process/runtime/debug pages as primary product pages.

## Red-Team Baseline

Before a conclusion, argue against it from:

- data quality;
- consumer perception;
- competitive copy risk;
- company capability fit.

Company fit means: quality-led, white-hat, design/R&D/production full chain, strongest around lighting-related craft unless the user says otherwise.

## Product Planning / Explosive USP Rule

In Chapter 6 Product Planning, do not only choose the safest or easiest-to-build track.

Run the explosive USP loop:

```text
opportunity points
-> user task and competitor purchase reason
-> vivid scene-level USP candidates
-> capability boundary check
-> red-team argue
-> user task effect -> functional conditions -> key components topology
-> Human Decision Stop
```

Company capability is not a static boundary. A strong USP may require adjacent capability growth if the difficulty is controllable. Separate:

```text
core capability: must use
adjacent capability: may grow
hard capability: do not jump into without explicit approval
```

Do not treat generic benefits such as better looking, more reliable, no subscription, cheaper, or more modes as final USP by default. Compress them into a vivid scene-level proposition that can be tested through frontstage expression and prototypes.

## Memory Boundary

Local run folder is the raw source of truth.

Memory/GBrain should receive only compact durable summaries, decision records, reusable analysis models, and unresolved blockers. Do not store raw credentials or sensitive supplier details.
