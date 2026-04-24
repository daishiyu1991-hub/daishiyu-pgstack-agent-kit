# PGStack Node Rules

This directory is the local `PGStack + PGBrain` wiki for one person or teammate.

## Canonical Architecture

- `PGStack` is the workflow and action surface.
- `PGBrain` is the durable knowledge and memory surface.
- `Codex` is the workbench for design, tuning, verification, and documentation.
- `Hermes` is the default host for recurring unattended pipelines.
- `MultiCA / AgentHost` is an optional orchestration layer for routing work across multiple agents.
- `MemTensor Team Hub` is optional shared compiled knowledge, not a raw transcript stream.
- The repo-level `skills/` directory is the canonical behavior layer.
- Substantive inbound messages should pass through `skills/signal-detector/SKILL.md`
  when the host supports ambient capture.
- Any brain read/write/lookup/citation should pass through
  `skills/brain-ops/SKILL.md`.

## Operating Rules

- Read `wiki/index.md` before durable work.
- Use `brain/RESOLVER.md` before creating durable brain objects.
- Use `skills/RESOLVER.md` before choosing a canonical skill.
- Update `wiki/index.md` and `wiki/log.md` after material changes.
- Prefer `Compiled Truth` plus `Timeline` for evolving durable objects.
- Run `python3 engine/skillpack_check.py` and
  `python3 engine/pgbrain_engine.py doctor` after shared-kernel skill changes.
- Keep private account state, tokens, and personal chat logs out of this wiki.
