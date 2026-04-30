# Product Strategy Template OS File Contract

scope: team_candidate
source_of_truth: `skills/product-strategy-template-os`

## Required Files For A Stable Pipeline

## Rules

- `SKILL.md`
- `references/global-rules.md`
- `references/pipeline-architecture.md`
- project `AGENTS.md` or `assets/AGENTS.product-strategy-template-os.example.md`

## Template

- `references/template-structure.zh.md`
- `templates/index.html`
- `templates/complete-report.html`
- `templates/chapter-execution-plan.json`
- `templates/evidence-ledger.json`
- `templates/human-decision.json`

## Validation

- `schemas/pipeline-run-state.schema.json`
- `schemas/evidence-ledger.schema.json`
- `schemas/human-decision.schema.json`
- `schemas/execution-plan.schema.json`
- `scripts/validate_run.py`
- `scripts/sanitize_check.py`

## Runtime Run Folder

- `quality-review-index.html`
- `quality-review-template-ch{n}-execution-plan-v1.html`
- `quality-review-template-ch{n}-{slug}-complete-v1.html`
- `process/pipeline-run-state-v1.json`
- `process/section{n}-execution-plan-v1.json`
- `process/section{n}-{slug}-evidence-v1.json`
- `process/section{n}-{slug}-analysis-v1.md`
- `process/section{n}-human-decision-*.json`

## GBrain Boundary

GBrain stores compact durable knowledge and source refs. It does not replace GitHub or local process files.
