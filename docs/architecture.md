# Architecture

`PGStack Agent Kit` installs one local `PGStack Node`.

```text
Human steward
-> Codex workbench
-> PGStack workflow layer
-> PGBrain durable knowledge layer
-> Hermes recurring runtime
-> optional MemTensor Team Hub
```

## Core Surfaces

- `skills/codex`: agent-facing design and governance skills
- `skills/hermes`: runtime skills for scheduled work
- `templates/pgstack-wiki`: starter Obsidian/Markdown wiki and PGBrain kernel
- `engine/pgbrain_engine.py`: deterministic local index, query, validation, and maintenance tool
- `config`: examples only, never live secrets

## Pipeline Shape

```text
radars
-> signal queue
-> dedupe and scoring
-> confirmation gate
-> triage
-> daily brief
-> optional research sidecar
-> PGBrain
-> optional MemTensor team candidate
```

## Why The Kit Is A Starter

Every teammate should install their own node and connect their own accounts.
The kit provides the rails. It does not ship anyone's private runtime state.

Third-party dependencies and account-backed services are guided in
`docs/setup-integrations.md`; they are not vendored into the kit.
