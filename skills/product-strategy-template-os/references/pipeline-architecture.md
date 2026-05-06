# Pipeline Architecture

This file is the durable architecture for Product Strategy Template OS. It explains how the skill keeps a long category research project consistent across chapters instead of relying on chat memory or one-off HTML pages.

## 1. Six-Layer Control Stack

```text
Global Rules
-> Skill Runtime
-> Run Architecture
-> Chapter Checkpoint Ledger
-> Local Artifacts
-> GBrain / Memory Sync
```

### 1.1 Global Rules

Purpose:

- enforce zero hallucination;
- preserve native GStack/GBrain first when available;
- separate Codex design work from Hermes runtime work when relevant;
- separate enterprise/team memory from personal memory;
- require durable artifacts for long-lived operating rules.

### 1.2 Skill Runtime

Purpose:

- define the fixed template;
- enforce evidence routing;
- enforce `Input -> Processing -> Output`;
- enforce complete reports;
- enforce human decision stops.

The skill runtime is the reusable operating rule. It should be updated only when a repeated workflow lesson has become durable.

### 1.3 Run Architecture

Purpose:

- adapt the skill runtime to one specific category run;
- record index lock, known evidence gaps, company-specific red-team baseline, and chapter boundaries;
- prevent a run from drifting after several turns.

Run architecture lives under the run folder's `process/` directory.

### 1.4 Chapter Checkpoint Ledger

Purpose:

- prove whether each chapter actually followed the pipeline;
- show what is complete, paused, blocked, or awaiting human decision;
- prevent a page from being treated as complete when evidence routing or red-team did not happen.

Default file:

```text
process/pipeline-run-state-v1.json
```

Required checklist:

```text
read_global_rules
read_skill_runtime
read_run_architecture
read_previous_chapter_decision
run_previous_artifact_review
run_evidence_router
collect_available_evidence
write_analysis_package
run_evidence_review
run_red_team
render_complete_report
stop_for_human_decision
write_decision_record
update_index
queue_or_sync_gbrain
```

### 1.5 Local Artifacts

Purpose:

- store HTML review surfaces;
- store raw process JSON/Markdown;
- store evidence ledgers;
- store decision records;
- support offline sharing with teammates.

Local artifacts are the source of truth for the run.

### 1.6 GBrain / Memory Sync

Purpose:

- preserve only compact, stable, reusable knowledge;
- avoid storing raw supplier secrets or noisy drafts;
- make durable decisions recoverable in future sessions.

If GBrain is unavailable, create a queue/status file. Do not pretend sync happened.

## 2. Complete Report Architecture

Each chapter should have one primary report. A report is complete only when it combines:

```text
old useful judgment structure
+ latest source-backed evidence
+ Input -> Processing -> Output
+ evidence sufficiency review
+ red-team argue
+ revised survivor conclusion
+ human decision stop
+ source list
```

### 2.1 Why Previous Artifact Review Exists

When a chapter is revised, newer is not automatically better. A prior page may have a clearer visual judgment structure, while a later page may have stronger evidence. The complete report must preserve the useful structure and replace only stale facts.

Previous artifact review asks:

- Which old page structures helped humans judge?
- Which facts are stale?
- Which pages are process history?
- Which structures must be inherited?
- Which pages should be sources rather than the primary report?

### 2.2 Primary Report vs Process Pages

Primary report:

- conclusion-first;
- visually readable;
- contains enough evidence to judge;
- points to sources and process details at the bottom.

Process pages:

- raw evidence;
- analysis packages;
- execution plans;
- decision records;
- debug or runtime notes.

The index should point to the primary report for each completed chapter.

## 2.3 Chapter 6 Explosive USP Architecture

Chapter 6 Product Planning has an additional rule: it must not stop at the safest opportunity track.

When the chapter is about USP, product definition, visible value, or product planning, run the explosive USP node before product architecture:

```text
Previous chapters
-> opportunity points
-> user task and competitor purchase reason
-> explosive USP candidates
-> company capability boundary
-> red-team argue
-> task/function/component topology
-> human decision stop
-> product architecture
```

The capability boundary is dynamic but controlled:

```text
core capability: must use
adjacent capability: may grow for a stronger USP
hard capability: do not jump into without explicit approval
```

The output is not a list of benefits. It must include:

- a vivid scene-level USP;
- evidence base and missing evidence;
- why common benefits are supporting roles rather than the main proposition;
- ability growth assumptions;
- red-team argument;
- `用户任务效果 -> 功能条件 -> 关键元器件` topology;
- a human decision stop.

Example:

```text
ordinary direction: 像灯具一样的日出光效
explosive USP: 先叫醒房间，再叫醒你
```

## 3. Chapter State Machine

```text
locked
-> planned
-> evidence_ready
-> analysis_draft
-> reviewed
-> awaiting_human_decision
-> unlocked_next / paused / evidence_requested
```

State meanings:

- `locked`: previous chapter has not unlocked this chapter.
- `planned`: execution plan exists.
- `evidence_ready`: evidence router has run and available evidence is collected.
- `analysis_draft`: process analysis exists.
- `reviewed`: evidence review and red-team have run.
- `awaiting_human_decision`: complete report is rendered and waiting for choice.
- `unlocked_next`: human explicitly chose to proceed.
- `paused`: human chose to pause.
- `evidence_requested`: human chose to fill a gap before continuing.

## 4. Template Node Loop

Every chapter contains smaller template nodes. Each node must run:

```text
Template Node
-> Question
-> Input Contract
-> Evidence Acquisition
-> Processing
-> Output Draft
-> Evidence Sufficiency Review
-> Red Team Argument
-> Revised Conclusion
-> Review Gates
-> Human Decision Stop
-> Next Node Unlock
```

### 4.1 Template Node

Record:

```text
chapter
node_id
node_title
template_source
belongs_to
does_not_belong_to
```

Purpose: prevent chapter drift.

### 4.2 Question

Translate the template title into a judgment question:

```text
what this node answers
what this node does not answer
what it gives the next node
```

### 4.3 Input Contract

Record:

```text
original template input
available input
MCP/API available
browser/frontstage available
uploaded-file available
manual required
not collectable now
```

Missing values must stay missing. Do not fill them with plausible guesses.

### 4.4 Evidence Acquisition

Each source gets:

```text
source_id
source_type
source_ref
collected_at
raw_data_path
used_for
status
```

Allowed statuses:

```text
collected_and_used
collected_not_expanded
missing_to_collect
manual_required
not_collectable_now
not_available_in_current_session
```

### 4.5 Processing

Record:

```text
processing_step
input_used
method
calculation_or_logic
chart_required
chart_type
output
```

Rules:

- trends need time basis: first-to-last, MoM, YoY, recent 3 periods when available;
- comparisons should become tables or charts;
- source rows or calculation method must be available for derived numbers.

### 4.6 Evidence Sufficiency Review

Record:

```text
required_inputs_complete
missing_inputs
most_important_missing_evidence
could_missing_evidence_change_conclusion
review_status
review_decision
```

Allowed review status:

```text
sufficient_for_this_node
usable_but_weak
insufficient_blocking
```

### 4.7 Red-Team Argument

Default red-team perspectives:

- data skeptic: evidence could mean something else;
- consumer skeptic: user may not understand or care;
- competition skeptic: competitors may copy or outspend;
- company-fit skeptic: the opportunity may not fit the company's strengths.

Record:

```text
current_thesis
strongest_counter_thesis
contradicting_evidence
missing_evidence_that_could_overturn
what_would_make_this_wrong
company_capability_fit
quality_advantage_can_be_seen
white_hat_viability
process_boundary_fit
knowhow_gap
entry_path
cost_disadvantage_risk
best_fit_entry_point
survivor_conclusion
confidence_after_red_team
```

### 4.8 Revised Conclusion

Only write the minimum conclusion that survives review:

```text
minimum_surviving_conclusion
what_is_fact
what_is_inference
what_is_not_collected
decision_impact
next_node_input
```

## 5. Review Gates

Before rendering the primary report:

```text
gate_1_evidence_sufficiency: pass / fail
gate_2_red_team: pass / fail
gate_3_template_alignment: pass / fail
gate_4_data_integrity: pass / fail
gate_5_chapter_boundary: pass / fail
gate_6_readability_for_html: pass / fail
```

Any fail blocks the formal report. The output becomes an execution plan, evidence request, or low-confidence hypothesis page instead.

## 6. Human Decision Stop

The human decision is not decoration. It changes pipeline state.

Common choices:

```text
A. pass and unlock next chapter
B. fill specified evidence gap
C. revise chapter boundary or sample set
D. pause
```

Every choice must create:

```text
process/section{n}-human-decision-*.json
```

If paused:

- do not unlock the next chapter;
- preserve resume conditions;
- update the index and run-state ledger.

## 7. Index Contract

The index is a roadmap, not a report.

Allowed updates:

- chapter status;
- primary report link;
- execution plan link;
- decision record link;
- concise boundary summary.

Blocked updates:

- changing accepted layout;
- reordering chapters;
- adding AI verdicts;
- adding runtime/debug pages as product-definition pages.

## 8. Default Artifact Layout

```text
run/
  quality-review-index.html
  quality-review-template-ch{n}-execution-plan-v1.html
  quality-review-template-ch{n}-{slug}-complete-v1.html
  process/
    pipeline-run-state-v1.json
    section{n}-execution-plan-v1.json
    section{n}-{slug}-evidence-v1.json
    section{n}-{slug}-analysis-v1.md
    section{n}-human-decision-*.json
    gbrain/
      README.md
      pages/
      gbrain-sync-queue.jsonl
      gbrain-sync-status.json
```

## 9. Reproducibility Contract

Another agent should be able to reproduce the work style by reading:

1. `SKILL.md`
2. `references/pipeline-architecture.md`
3. `references/template-structure.zh.md`
4. `references/data-source-router.md`
5. `references/red-team-company-baseline.md`
6. `references/frontend-report-style.md`
7. `examples/wake-up-light/`

The example is a shape reference, not a source of future conclusions.
