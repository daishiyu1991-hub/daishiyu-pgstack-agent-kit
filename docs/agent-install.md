# Install With Your Agent

This is the preferred installation path for teammates.

The human delegates the setup to their local agent. The agent installs the kit,
verifies it, and reports what is ready before any optional integration is
enabled.

## Copy This To Your Agent

```text
Please install PGStack Agent Kit for me.

Repository:
https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit

Requirements:
1. Check whether PGSTACK_HOME, CODEX_HOME, and HERMES_HOME are already set.
2. If any target directory already exists, report it before overwriting.
3. Run the official remote installer.
4. After install, run the smoke test if the checkout is available.
5. Run `python3 engine/skillpack_check.py` inside PGSTACK_HOME and confirm 0 errors and 0 warnings.
6. Run PGBrain doctor and confirm 0 errors and 0 warnings.
7. If I provide a GBrain Remote MCP URL and token, run
   `node engine/gbrain_remote_mcp_health.mjs --require-config`; otherwise
   report Remote MCP as intentionally disconnected.
8. Do not upload, commit, or copy my secrets, tokens, cookies, Feishu channels,
   MemTensor data, browser profiles, or private notes.
9. Do not enable recurring cron jobs until I approve delivery channels and
   runtime ownership.
10. Give me an acceptance report with:
   - PGStack install path
   - Codex skills path
   - Hermes skills path
   - skillpack check result
   - PGBrain doctor result
   - GBrain Remote MCP health result
   - smoke test result
   - optional integrations that are still disconnected
   - any blocker or permission needed from me
```

## Agent Command

The agent can use this command when the human approves the default install:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit/main/bin/install-remote.sh)"
```

Useful environment variables:

```bash
export PGSTACK_HOME="$HOME/Documents/PGStack/personal-gstack"
export CODEX_HOME="$HOME/.codex"
export HERMES_HOME="$HOME/.hermes"
```

## Expected Agent Flow

```text
inspect local environment
-> confirm target directories
-> run installer
-> run PGBrain doctor
-> run smoke test when checkout is present
-> check that no private state was copied into git
-> report readiness and optional integration gaps
```

## Acceptance Standard

The install is ready only when:

- PGStack starter wiki exists at `PGSTACK_HOME`
- Codex skills are installed or intentionally skipped
- Hermes runtime skills are installed or intentionally skipped
- `skillpack_check.py` returns `0 error(s), 0 warning(s)`
- `PGBrain doctor` returns `0 error(s), 0 warning(s)`
- smoke test passes when run from the checkout
- GBrain Remote MCP health returns `PASS` after approved URL/token, or is
  explicitly reported as disconnected before config
- no private secrets, Feishu channels, cookies, MemTensor memory dumps, or
  machine-specific private paths are committed or uploaded

## Optional Integrations

Do these after the core install is verified.

- `MemTensor`: connect local memory or team hub, then run a write/read health check.
- `GBrain Remote MCP`: configure only after the human approves endpoint, token,
  and memory-center boundary.
  See `docs/gbrain-remote-mcp.md`.
- `MultiCA / AgentHost`: connect only if cross-agent or team-visible dispatch
  is needed; run one no-op task, then verify the artifact can land in PGBrain.
- `Feishu`: connect only the teammate's own bot or DM target.
- `GitHub`: connect the teammate's own plugin, SSH key, deploy key, or CLI.
- `NotebookLM`: keep as a supervised research sidecar unless a stable bridge is
  explicitly available.
- `Hermes cron`: enable only after delivery channels and runtime state are ready.

## Human Responsibilities

The human should decide:

- where the node is installed
- which account-backed services are allowed
- whether team MemTensor sharing is enabled
- whether Hermes recurring jobs are activated
- whether MultiCA / AgentHost should route other agents' or team-visible work
  to this node

The agent should not guess these decisions silently.
