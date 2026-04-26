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
- optional central-brain lookup, health, and MCP bridge commands

The kit does not install or copy:

- personal SSH keys
- API keys or tokens
- Feishu channels or bot secrets
- MemTensor databases or memory dumps
- MultiCA / AgentHost runtime state
- NotebookLM cookies or browser sessions
- local Hermes state
- machine-specific paths
- Central Brain Host SSH targets or key paths

## Recommended Setup Order

1. Prefer agent-led install with `docs/agent-install.md`.
2. Run the one-click installer.
3. Verify the local node with `PGBrain doctor`.
4. Connect only the integrations the teammate actually needs.
5. Run the matching health check.
6. Enable recurring jobs only after the integration works.

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

## MultiCA And AgentHost

MultiCA and AgentHost are optional orchestration layers for teammates who want
one control plane to route work across Codex, Hermes, and other agents.

The kit provides:

- PGBrain runtime-host vocabulary for `MultiCA` and `AgentHost`
- adapter notes in the starter wiki
- a safe integration contract for writing back to PGBrain and MemTensor

The kit does not install:

- MultiCA servers
- AgentHost processes
- access tokens
- browser sessions
- teammate-specific agent routing rules

Suggested health checks after the teammate connects MultiCA or AgentHost:

```text
open the MultiCA or AgentHost dashboard
run one no-op or echo task through the target agent
write one test artifact to the local PGStack wiki
run PGBrain doctor
verify that any MemTensor write uses team-memory gate rules
```

Default routing:

```text
MultiCA / AgentHost
-> Codex for design and verification
-> Hermes for recurring runtime jobs
-> PGBrain for durable local conclusions
-> MemTensor only after scope/source/review checks
```

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

## Central Brain Host

Central Brain is optional. Use it when a teammate node should read from a
shared GBrain + MemTensor center.

The kit provides:

- `engine/central_brain_lookup.py`
- `engine/central_brain_health.py`
- `engine/central_brain_mcp_server.mjs`
- compatibility boundary docs in the starter wiki

It does not install:

- SSH keys
- cloud servers
- GBrain server state
- MemTensor databases
- MCP SDK dependencies

Before configuration, this should return `SKIP`:

```bash
python3 "$PGSTACK_HOME/engine/central_brain_health.py"
```

After the human approves the target and key:

```bash
export PGSTACK_CENTRAL_BRAIN_SSH_TARGET="user@host"
export PGSTACK_CENTRAL_BRAIN_SSH_KEY="$HOME/.ssh/your_key"
python3 "$PGSTACK_HOME/engine/central_brain_health.py" --require-config
```

See `docs/central-brain.md`.

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
