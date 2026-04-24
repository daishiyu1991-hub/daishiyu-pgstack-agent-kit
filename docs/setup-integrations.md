# Setup Integrations

`PGStack Agent Kit` installs the local PGStack rails. It does not bundle every dependency or account integration.

This is intentional.

## Boundary

The kit installs:

- PGStack/PGBrain starter wiki
- PGBrain Engine
- Codex-side skills
- Hermes runtime skills
- example configuration
- local smoke tests

The kit does not install or copy:

- personal SSH keys
- API keys or tokens
- Feishu channels or bot secrets
- MemTensor databases or memory dumps
- NotebookLM cookies or browser sessions
- local Hermes state
- machine-specific paths

## Recommended Setup Order

1. Run the one-click installer.
2. Verify the local node with `PGBrain doctor`.
3. Connect only the integrations the teammate actually needs.
4. Run the matching health check.
5. Enable recurring jobs only after the integration works.

## Core Check

```bash
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" doctor
```

Expected:

```text
doctor passed: 0 error(s), 0 warning(s)
```

## Codex

The installer copies skills into:

```text
$CODEX_HOME/skills
```

After install, restart or refresh the agent host if it does not immediately see the new skills.

## Hermes

The installer copies runtime skills into:

```text
$HERMES_HOME/skills/research
```

It also writes examples to:

```text
$HERMES_HOME/cron/pgstack-jobs.example.json
```

Do not enable cron jobs until delivery channels and required state paths are configured.

## MemTensor

MemTensor is an optional persistence and team-sharing layer.

The kit provides:

- team-memory writing rules
- team-memory gate rules
- adapter notes
- PGBrain sharing policy

It does not install a MemTensor daemon or copy memory data.

Suggested health checks after the teammate installs or connects MemTensor:

```text
ping local memory service
write one local test memory
search for that test memory
delete or ignore the test item according to local policy
```

Team sharing should stay disabled until the team owner confirms:

- allowed knowledge classes
- review gate
- source-of-truth rules
- rollback path

## Feishu

Feishu delivery is intentionally not bundled.

Each teammate should configure their own channel or DM target and then update the Hermes cron config.

Keep channel IDs and bot secrets out of git.

## GitHub

GitHub is needed only when the teammate wants remote version control or GitHub radar workflows.

Recommended flow:

```bash
git remote -v
ssh -T git@github.com
```

Use deploy keys, SSH keys, GitHub CLI, or the teammate's preferred GitHub plugin. Do not commit credentials.

## NotebookLM

NotebookLM remains a supervised research sidecar.

Do not make NotebookLM a required install step. Connect it only when the teammate wants deeper research briefs and accepts that NotebookLM auth/API behavior may change.

## Safe Default

If no integrations are connected, the local PGStack Node should still work as:

```text
Codex skills + starter wiki + PGBrain Engine + local docs
```

That is enough to start learning and evolving the system.
