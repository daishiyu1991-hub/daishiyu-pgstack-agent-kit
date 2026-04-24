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

The canonical architecture is a single local `PGStack Node`:

```text
agent host + workflow layer + PGBrain + Obsidian/wiki + optional MemTensor Team Hub
```

Each teammate owns their own node. Nodes share compiled knowledge through MemTensor or GitHub, not raw chat logs.

