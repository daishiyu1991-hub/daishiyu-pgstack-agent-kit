---
name: personal-gstack
description: A personal complex-task operating system inspired by gstack and Karpathy's LLM Wiki. Use when the user has a fuzzy idea, complex project, research/decision task, personal/business workflow, or strategy problem that should be clarified, planned, red-teamed, and preserved into the local wiki and MemTensor memory.
metadata:
  short-description: Clarify, plan, and red-team complex tasks
---

# Personal GStack

Use this skill as the entry point for non-code complex tasks. It turns vague intent into a durable brief, plan, and risk review, then updates the local Karpathy-style wiki when the result should compound.

## Modes

Choose the smallest mode that matches the request:

- `clarify`: use when the goal, decision, success criteria, or constraints are unclear.
- `plan`: use when there is already a brief and the user needs stages, dependencies, outputs, and gates.
- `red-team`: use when there is already a brief/plan and the user needs assumptions, failure paths, contradictions, and evidence gaps.
- `implement`: use when an approved plan should be turned into concrete artifacts or workflow changes.
- `verify`: use when an implemented result needs acceptance checks or reality checks.
- `persist`: use when durable knowledge, decisions, or outputs should be saved into the right long-term layer.
- `operate`: use when a workflow needs runtime ownership, cadence, escalation rules, or monitoring.
- `retro`: use when completed or recurring work should be reviewed for rule changes and lessons.

Default sequence for substantial work:

```text
clarify -> plan -> red-team -> implement -> verify -> persist
```

For recurring systems:

```text
operate -> retro
```

## Local Wiki

Use the local wiki as the durable knowledge layer:

```text
$PGSTACK_HOME
```

Before durable work, read:

1. `AGENTS.md`
2. `wiki/index.md`
3. Any relevant page from `wiki/concepts/`, `wiki/syntheses/`, or `wiki/questions/`
4. Relevant MemTensor or team-memory context when the task touches long-lived operating rules, skills, or workflows
5. The relevant governance checklist when resuming work, graduating a pipeline, or changing a core rule

For long-lived operating questions, prefer brain-first lookup:

1. local wiki first
2. reviewed memory second
3. external research only when a real gap remains

After durable work, update:

1. The relevant wiki page(s)
2. `wiki/index.md`
3. `wiki/log.md`
4. MemTensor with a compact pointer, scope, and conclusion when appropriate

Default memory layer order:

1. local MemTensor for continuity
2. local wiki when the knowledge changes `pgstack` structure
3. team promotion only after rewrite and governance

## Live Team Memory

When MemTensor or team memory is reachable:

1. Query it before redesigning long-lived operating rules or repeating a known workflow problem.
2. Treat retrieved memory as governed context, not as automatic policy.
3. Let explicit scope, review status, evidence, and source-of-truth signals decide how much to trust it.
4. Rewrite durable conclusions back into the wiki and memory layers instead of relying on implicit recall alone.

## Conversation Memory

For substantive collaboration turns, prefer effective write-through into MemTensor:

1. Capture durable user preferences, decisions, verified outcomes, blockers, recovery instructions, and operating-rule changes.
2. Summarize compactly instead of dumping full transcripts.
3. Batch small back-and-forth turns when they belong to one durable conclusion.
4. Skip low-value chatter unless it materially changes future work.
5. Skip meta save-review prompts and noop save outcomes entirely.
6. Avoid saving raw user turns as team-facing memory unless the wording itself is the durable object.

## Mode References

- For clarification workflow, read `references/clarify.md`.
- For planning workflow, read `references/plan.md`.
- For red-team workflow, read `references/red-team.md`.
- For implementation workflow, read `references/implement.md`.
- For verification workflow, read `references/verify.md`.
- For persistence workflow, read `references/persist.md`.
- For operating workflow, read `references/operate.md`.
- For retrospective workflow, read `references/retro.md`.

## Operating Rules

- Do not create wiki pages for disposable chatter.
- Do create wiki pages for reusable frameworks, task briefs, plans, risk reviews, decisions, and patterns.
- Distinguish facts, assumptions, inferences, preferences, and open questions.
- For durable pages that evolve over time, prefer a two-layer knowledge object:
  - `Compiled Truth`
  - `Timeline`
- Ask at most three clarifying questions when blocked. Otherwise make reasonable assumptions and mark them.
- A good run changes task state; it does not merely produce a long answer.
- For durable tasks, prefer naming the current state and target state explicitly.
- For recurring automation pipelines, default runtime ownership belongs to `Hermes`.
- `Codex` remains the workbench for designing, tuning, red-teaming, and documenting those pipelines.
- For recurring pipelines that may graduate from experiment to operation, use the local wiki's `Personal GStack Pipeline Graduation Template` and verify the Level 1-4 ladder before calling the pipeline `graduated-v1`.
- For shared-kernel changes, verify with the local `PGBrain Engine v1`: run `doctor`, a targeted `query`, and `related` when relationships changed before treating the change as persisted.
- When team memory is available, use it as a supporting operating layer, but do not let weakly reviewed memory bypass local wiki governance.
- Use MemTensor as a write-through continuity layer for substantive collaboration, with the local wiki remaining the canonical design surface.
- Prefer brain-first lookup for durable work: read what `pgstack` already knows before creating new rules or reaching for external research.
- Keep team-facing MemTensor memory clean: compiled operating knowledge in, workflow exhaust out.
- Prefer the local-first memory default: continuity first, canonical wiki second, team promotion third.
- Use the governance checklist suite whenever resume clarity, pipeline graduation, or core-rule safety matters.
