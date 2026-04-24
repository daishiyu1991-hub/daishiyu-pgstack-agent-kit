# Architecture

`PGStack Agent Kit` installs one local `PGStack Node`.

```text
Human steward
-> optional MultiCA / AgentHost orchestration
-> Codex workbench + Hermes runtime adapters
-> PGStack workflow layer
-> PGBrain durable knowledge layer
-> optional MemTensor Team Hub
```

## Core Surfaces

- `skills/codex`: agent-facing design and governance skills
- `skills/hermes`: runtime skills for scheduled work
- `templates/pgstack-wiki`: starter Obsidian/Markdown wiki and PGBrain kernel
- `engine/pgbrain_engine.py`: deterministic local index, query, validation, and maintenance tool
- `config`: examples only, never live secrets

## MultiCA And AgentHost

MultiCA and AgentHost sit above a local PGStack Node when a teammate wants
multiple agents to work together.

They are orchestration surfaces, not the durable memory layer.

Recommended contract:

```text
MultiCA / AgentHost
-> dispatches work to Codex, Hermes, or other agents
-> receives artifacts or status
-> writes durable conclusions into PGBrain
-> promotes only governed knowledge candidates into MemTensor
```

The kit documents this path but does not install a MultiCA server, agent host,
tokens, browser sessions, or remote credentials.

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
