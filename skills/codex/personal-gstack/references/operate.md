# Operate Mode

Use `operate` when a workflow has moved beyond design and now needs runtime ownership, cadence, monitoring, or maintenance rules.

## Role

You are an operator. Your job is to define how a recurring workflow runs reliably over time.

## Example Triggers

- "把它变成长期运行的流程。"
- "这个以后怎么跑？"
- "帮我把运行规则定下来。"

## Inputs

- Verified workflow or artifact.
- Runtime owner and cadence preferences.
- Known delivery and failure-handling rules.

## Workflow

1. State what will operate continuously.
2. Confirm runtime ownership:
   - `Hermes`
   - `Codex`
   - manual
3. Define:
   - trigger or cadence
   - inputs
   - outputs
   - fallback behavior
   - monitoring signals
   - escalation rules
4. Mark what belongs in unattended runtime vs human review.
5. Recommend `persist` if rules need storing, or `retro` if the workflow has enough runtime history to review.

## Output Shape

```markdown
# Operating Model

## Operated Workflow

## Runtime Owner

## Cadence Or Trigger

## Inputs And Outputs

## Monitoring Signals

## Escalation Rules

## Recommended Next Mode
```

## Gate

Operate mode is complete when a future run knows who owns the workflow, how it starts, what it produces, and when a human should step in.

## Wiki Update

For durable tasks:

- update the workflow synthesis page
- append `## [YYYY-MM-DD] operate | <task>` to `wiki/log.md`

## Memory Update

Save runtime ownership, delivery rules, and escalation boundaries when they are part of an ongoing system.
