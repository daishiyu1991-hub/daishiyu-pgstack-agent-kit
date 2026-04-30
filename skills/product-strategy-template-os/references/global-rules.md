# Product Strategy Template OS Global Rules

This file is the portable global rule layer for the Product Strategy Template OS skill. Use it when a project wants this workflow to be the default research behavior, not just a one-off skill invocation.

## 1. Default Mode

When a user asks for product/category strategy research, category opportunity analysis, Amazon consumer-electronics product definition, or a `爆品战略用研` workflow, default to the Product Strategy Template OS pipeline unless the user explicitly requests a quick informal answer.

Default route:

```text
category / keyword / ASIN / template
-> fixed chapter router
-> evidence acquisition
-> Input -> Processing -> Output
-> evidence review
-> red-team argue
-> complete HTML report
-> human decision stop
-> state ledger update
```

## 1.1 Native GBrain Sync Boundary

GBrain sync is a skill-boundary behavior, not a separate human request.

At the start and end of every Product Strategy Template OS run, the agent must
try the original native GStack/GBrain path first:

```text
detect native gstack-brain-sync
-> register compact global-rule record in projects/product-strategy-template-os/learnings.jsonl
-> enqueue through gstack-brain-enqueue
-> run gstack-brain-sync --discover-new
-> run gstack-brain-sync --once
```

Only if native `gstack-brain-sync` is unavailable should the agent fall back to
the Hermes Admin handoff queue:

```text
gbrain/gbrain-sync-queue.jsonl
-> Hermes Admin
-> gbrain-remote
-> enterprise GBrain
```

Do not ask the human to request GBrain sync every time. Ask only when native
sync is not initialized, sync mode is `off`, credentials/permissions are
missing, or the user must choose privacy/team-publication scope.

Do not claim GBrain sync succeeded unless native sync or Hermes Admin write and
query verification actually passed.

## 2. Data Integrity

All data must be real and traceable.

Never fabricate:

- ASINs;
- prices;
- sales estimates;
- keyword volumes;
- trend growth;
- review quotes;
- supplier facts;
- COGS;
- MOQ;
- tooling cost;
- citations;
- source names.

Missing data must stay missing:

```text
not_collected
manual_required
not_available_in_current_session
unknown
```

Inferences must be labeled as inference. Calculations must show source rows or method.

## 3. Evidence Acquisition Is The Pipeline's Job

If a tool/API/MCP/file/browser route is available, use it before asking the human to judge. Do not ask the human whether to run a standard evidence collection step after they have asked the pipeline to continue.

Ask the human only for:

- dynamic-quality judgment;
- supplier/offline truth AI cannot verify;
- credentials/permissions;
- company-specific capability boundaries;
- explicit product decisions.

## 4. Fixed Chapter Order

Default template:

```text
1. 品类本质小结
2. 市场竞争分析
3. 头部品牌竞争&竞品分析
4. 用户场景&需求分析
5. 营销分析&社媒传播
6. 供应链管理
7. 产品规划
```

Do not merge chapters or jump ahead. If useful content belongs to a later chapter, record it as next-chapter input.

## 5. Complete Report Requirement

The primary chapter artifact must be a complete report, not scattered fragments.

Each complete report must include:

- conclusion first;
- key charts / comparison tables;
- template node `Input -> Processing -> Output`;
- evidence sufficiency review;
- red-team argue;
- human decision stop;
- source list at the bottom.

Execution plans and raw evidence pages are process artifacts, not substitutes for a complete report.

## 6. Previous Artifact Review

Before regenerating a chapter, review existing artifacts:

- which old structures helped human judgment;
- which facts are stale;
- which pages are only process history;
- which structures must be inherited;
- which page should be the primary report.

Do not lose a useful visual/judgment structure just because a later evidence page is stricter.

## 7. Human Decision Stop

Every chapter ends with human decision.

AI cannot:

- infer blank choices;
- mark `Go` automatically;
- unlock the next chapter without explicit human choice;
- continue after a `pause`.

Write decisions into:

```text
process/section{n}-human-decision-*.json
```

## 8. Index Contract

The index page is a roadmap.

Allowed:

- update chapter status;
- update primary report link;
- add execution plan / decision record links;
- update concise chapter summaries.

Blocked:

- redesign accepted index architecture;
- reorder template chapters;
- add AI verdicts as product decisions;
- put process/debug/runtime pages into the product index.

## 9. Red-Team Baseline

Every decision that touches market fit, product strategy, supply chain, or company fit must include red-team argue.

Default red-team positions:

- data skeptic;
- consumer skeptic;
- competition skeptic;
- company-fit skeptic.

Company-fit questions:

- Is the opportunity suitable for a quality-led company, not a lowest-cost seller?
- Can the company win with white-hat marketing and real product value?
- Which capabilities are internal strengths?
- Which modules require ODM or outside suppliers first?
- What happens when competitors copy the visible feature?

## 10. Frontstage Competition Baseline

For Amazon consumer products, always map competition back to what consumers see before buying:

```text
1. selling point and visual value: main image, video, A+, five bullets
2. price
3. review count
4. review quality
5. coupon / deals
```

The product question is not only whether defects are reduced. The core question is whether the consumer can quickly feel more value in the buying scene.

## 11. Trend Basis

Every trend claim must state comparison basis:

- first available period -> latest period;
- latest vs previous period;
- latest vs same period one year earlier when available;
- latest vs three periods earlier when available.

No hot-search data means `无热搜趋势数据`, not zero demand.

## 12. Artifact Layout

Default run layout:

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

## 13. Memory / GBrain Boundary

Local run folder is the source of truth for raw process artifacts.

GBrain or other memory systems should receive only compact durable outputs:

- chapter summaries;
- explicit human decision records;
- durable analysis models;
- unresolved evidence blockers;
- reusable company baselines.

Do not write:

- raw credentials;
- raw supplier secrets;
- every draft HTML;
- long chat transcript;
- unverified speculation.

If memory/GBrain is unavailable, write `pending` or `unavailable_in_current_session`. Do not claim sync succeeded.

## 14. Internal Skill Compliance

Local product skills must inherit this OS instead of becoming separate decision
systems.

- Product-definition skills own judgment, but must still obey the Template
  Router, Evidence Acquisition Router, red-team review, complete-report output,
  Human Decision Stop, and native GBrain sync.
- Product-analysis, marketplace, profit, competitor, review, and social modules
  are evidence suppliers. They can collect, normalize, calculate, render, and
  cite evidence, but cannot mark human Go/No-go decisions, unlock later
  chapters, or bypass the native GStack/GBrain path.
- When a repeated workflow becomes a skill, first check whether original
  GStack/GBrain or this Template OS already owns the behavior. Add a wrapper,
  adapter, or policy extension unless there is a real gap.

