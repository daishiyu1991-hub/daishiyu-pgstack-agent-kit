# PGStack Agent Kit Rules

This repository is a portable starter kit. Keep it generic.

Do not commit:

- personal Obsidian content
- MemTensor memory dumps
- Feishu channel IDs
- Hermes cron state
- cookies, tokens, or browser profiles
- absolute paths from one person's machine

When changing the kit:

- keep `templates/pgstack-wiki` installable on a new machine
- keep `skills/` free of private runtime assumptions
- run `./scripts/smoke_test.sh`
- prefer examples over live credentials
- update `README.md` when installation behavior changes

The canonical architecture is a native-first personal node:

```text
original GStack + original GBrain + Brain Repo + host adapters + PGStack add-ons
```

Skill behavior resolves through the original GStack/GBrain resolver first.
PGStack skills are thin extensions for policy, packaging, memory governance,
and host boundaries; they should not duplicate native skills that already cover
the job.

Private agent work should use native `GStack -> GBrain` first. Use MultiCA /
AgentHost only when routing to another person's agent, company/team runtime,
target-agent self-repair, or an explicitly requested remote-agent coordination
case.

Cloud runtime mutations are Hermes-owned by default. For cloud Hermes Admin,
cloud GBrain, cloud Brain Repo assets, GBrain jobs/minions, graph/link repair,
or cloud runtime config changes, Codex should write the intent, constraints,
acceptance checks, and ACP prompt; Hermes Admin should perform the cloud-side
change through native GBrain CLI/MCP/Brain Repo/jobs/minions paths; Codex
should verify externally. Direct SSH/docker mutation by Codex is a bypass
allowed only for explicit one-off user request, accepted emergency
intervention, read-only inspection, or non-mutating external verification.

Durable memory flow defaults to:

```text
compiled Markdown knowledge object
-> Brain Repo / GBrain sync/embed/query
-> optional MemTensor personal pointer
-> optional governed TeamHub publication
```

Native `gstack-brain-sync` is the default sync boundary. Skills and pipelines
should drain or enqueue through original `gstack-brain-enqueue` /
`gstack-brain-sync` at start/end boundaries before falling back to Hermes Admin
handoff. Do not turn GBrain sync into a repeated manual user request. Ask only
when sync is not initialized, sync mode is `off`, credentials/permissions are
missing, or privacy/team-publication scope needs human choice.

Each teammate owns their own node. Nodes share compiled knowledge through
GBrain/Brain Repo, MemTensor TeamHub, or GitHub, not raw chat logs. MemTensor is
a continuity and TeamHub adapter, not a second semantic brain.
