# PGStack Agent Kit

Portable starter kit for installing a personal `PGStack Node` into a teammate's agent workspace.

It packages the reusable parts of the system:

- Codex skills for `personal-gstack`, `llm-wiki`, AI daily brief authoring, and team-memory governance
- Hermes runtime skills for AI daily brief and team knowledge curation
- a starter `PGStack + PGBrain` wiki kernel
- a gbrain-style repo-level canonical skillpack with `skills/RESOLVER.md`,
  `skills/manifest.json`, always-on `signal-detector` / `brain-ops`, and
  portable thick skills
- `PGBrain Engine v1` for local indexing, query, relation lookup, doctor checks, and maintenance reports
- example config for Hermes cron, MemTensor, MultiCA/AgentHost orchestration, NotebookLM sidecars, and GitHub-backed collaboration
- local smoke tests so a teammate can verify the node before using it

This repo is a starter kit, not a full dependency bundle. It intentionally does not include private state, Feishu channels, personal Obsidian content, MemTensor memories, cookies, tokens, machine-specific paths, or third-party account logins.

## Install With Your Agent

The recommended teammate flow is agent-led installation.

Ask the teammate's local agent to install, verify, and report back using
[docs/agent-install.md](docs/agent-install.md). The human should approve target
directories, credentials, optional integrations, and cron activation. The agent
should handle cloning, running the installer, smoke testing, and producing the
acceptance report.

## One-Click Install

After this repository is published, teammates can install with:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit/main/bin/install-remote.sh)"
```

For local testing from a checkout:

```bash
./install.sh
```

Useful environment variables:

```bash
export PGSTACK_HOME="$HOME/Documents/PGStack/personal-gstack"
export CODEX_HOME="$HOME/.codex"
export HERMES_HOME="$HOME/.hermes"
```

## What Gets Installed

Default install destinations:

```text
$PGSTACK_HOME                       starter PGStack/PGBrain wiki
$CODEX_HOME/skills                  Codex-side skills
$HERMES_HOME/skills/research        Hermes runtime skills
```

The installer never installs credentials. Each person must connect their own:

- Feishu or another delivery channel
- MemTensor local or team hub
- MultiCA / AgentHost runtime and credentials
- GitHub account/plugin
- NotebookLM browser login or MCP bridge
- Hermes cron jobs

Integration setup is guided, not bundled. See [docs/setup-integrations.md](docs/setup-integrations.md).

## Runtime Split

```text
Codex  = design, tuning, red-team, documentation, skill evolution
Hermes = recurring runtime execution and unattended pipelines
MultiCA / AgentHost = optional orchestration layer for multi-agent routing
PGBrain = durable local knowledge engine
MemTensor Team Hub = optional shared compiled knowledge layer
```

## Quick Verification

```bash
./scripts/smoke_test.sh
```

The smoke test installs into a temporary directory, runs `skillpack_check.py`,
PGBrain validation/doctor checks, and checks for obvious private-path leakage.

## First Real Pipeline

The starter node includes `AI Daily Brief` as the reference pipeline shape:

```text
radars -> signal queue -> confirmation -> triage -> daily brief
       -> optional NotebookLM research sidecar -> PGBrain
```

The production cron schedule and delivery channel are deliberately left as examples. Do not copy another person's Feishu channel or local state into a teammate node.
