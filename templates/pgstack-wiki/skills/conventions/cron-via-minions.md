---
title: PGStack Cron Via Minions Convention
type: convention
created: 2026-04-24
updated: 2026-04-24
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - ../../jobs/RESOLVER.md
  - ../../brain/skills/pgstack-pgbrain-shared-kernel-architecture.md
---

# PGStack Cron Via Minions Convention

Recurring work should be specified as a `jobs/` object and run by Hermes or a
future minion host.

## Rule

```text
job spec -> host adapter -> deterministic script/skill -> state artifact -> log
```

Hermes may be the scheduler, but the durable contract lives in this repo.

Long-running or timeout-prone work should split into bounded stages with durable
state pointers instead of one monolithic unattended run.
