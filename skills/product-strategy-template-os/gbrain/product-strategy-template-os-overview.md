# Product Strategy Template OS

scope: team_candidate
source_of_truth: GitHub skill repository
github_path: `skills/product-strategy-template-os`

## What It Is

Product Strategy Template OS is a fixed-template product/category research pipeline for consumer electronics and Amazon-led category strategy. It turns a keyword/category/ASIN signal into chapter-by-chapter research artifacts, evidence ledgers, complete HTML reports, and explicit human decisions.

## Core Operating Rule

AI collects and organizes static quality. Human judges dynamic quality. The pipeline never turns evidence into an automatic product decision.

## Fixed Chapter Order

1. 品类本质小结
2. 市场竞争分析
3. 头部品牌竞争&竞品分析
4. 用户场景&需求分析
5. 营销分析&社媒传播
6. 供应链管理
7. 产品规划

## Stability Contract

The stable file layers are:

- `SKILL.md`
- `references/global-rules.md`
- `references/pipeline-architecture.md`
- `references/template-structure.zh.md`
- `references/data-source-router.md`
- `references/red-team-company-baseline.md`
- `references/frontend-report-style.md`
- `schemas/`
- `templates/`
- `scripts/validate_run.py`
- `process/pipeline-run-state-v1.json` inside each run

## Memory Boundary

GitHub is the source of truth for executable files. GBrain should store a compact searchable overview, operating rules, and links to source refs. GBrain should not store raw supplier secrets, credentials, or every draft HTML.

## Handoff Status

This page is intended to be written by Hermes-admin into enterprise GBrain through the native GBrain route.
