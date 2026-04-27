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

Durable memory flow defaults to:

```text
compiled Markdown knowledge object
-> Brain Repo / GBrain sync/embed/query
-> optional MemTensor personal pointer
-> optional governed TeamHub publication
```

Each teammate owns their own node. Nodes share compiled knowledge through
GBrain/Brain Repo, MemTensor TeamHub, or GitHub, not raw chat logs. MemTensor is
a continuity and TeamHub adapter, not a second semantic brain.
