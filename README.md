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
- example config for Hermes cron, MemTensor, optional MultiCA/AgentHost
  cross-agent orchestration, NotebookLM sidecars, and GitHub-backed
  collaboration
- optional GBrain Remote MCP health and host-wrapper commands that keep GBrain
  first and MemTensor as a separately labeled TeamHub/retrieval adapter
- local smoke tests so a teammate can verify the node before using it

This repo is a starter kit, not a full dependency bundle. It intentionally does not include private state, Feishu channels, personal Obsidian content, MemTensor memories, cookies, tokens, machine-specific paths, or third-party account logins.

## Install With Your Agent

The recommended teammate flow is agent-led installation.

Ask the teammate's local agent to install, verify, and report back using
[docs/agent-install.md](docs/agent-install.md). The human should approve target
directories, credentials, optional integrations, and cron activation. The agent
should handle cloning, running the installer, smoke testing, and producing the
acceptance report.

## Product Strategy Template OS Skill

For the fixed-template product/category research workflow, install:

```bash
npx skills add https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit --skill product-strategy-template-os
```

To update an existing install, tell the teammate's agent:

```text
/update product-os
```

The installed skill maps that phrase to:

```bash
SKILL_HOME="${CODEX_HOME:-$HOME/.codex}/skills/product-strategy-template-os"
python3 "$SKILL_HOME/scripts/update_product_os.py"
```

If the skill was installed through `npx skills add --global`, the usual path is:

```bash
SKILL_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/product-strategy-template-os"
python3 "$SKILL_HOME/scripts/update_product_os.py"
```

If the teammate has an older install without that script, the fallback is:

```bash
npx skills add https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit --skill product-strategy-template-os --yes --global
SKILL_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/product-strategy-template-os"
python3 "$SKILL_HOME/scripts/bootstrap_check.py" --skill-root "$SKILL_HOME"
```

After installation, the teammate's agent should read:

```text
skills/product-strategy-template-os/README.md
```

That README is the canonical bootstrap contract. It tells the agent how to:

- verify that all OS files were installed;
- initialize a new research run;
- follow the fixed chapter loop;
- enforce zero-hallucination evidence rules;
- stop for human decisions;
- queue the native GBrain/Hermes Admin handoff.

The minimum acceptance report is:

```text
OK_BOOTSTRAP
OK_VALIDATE_RUN
skill path
run path
current chapter
whether GBrain handoff is queued or synced
```

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
- MultiCA / AgentHost runtime and credentials, only if cross-agent or
  team-visible dispatch is needed
- GitHub account/plugin
- NotebookLM browser login or MCP bridge
- Hermes cron jobs
- GBrain Remote MCP endpoint and bearer token

Integration setup is guided, not bundled. See [docs/setup-integrations.md](docs/setup-integrations.md).

## Runtime Split

```text
Codex  = design, tuning, red-team, documentation, skill evolution
Hermes = recurring runtime execution and unattended pipelines
MultiCA / AgentHost = optional orchestration layer for other people's agents, team runtime, or explicit remote-agent routing
PGBrain = durable local knowledge engine
MemTensor Team Hub = optional shared compiled knowledge layer
GBrain Remote MCP = optional shared cloud GBrain memory center
```

## Quick Verification

```bash
./scripts/smoke_test.sh
```

The smoke test installs into a temporary directory, runs `skillpack_check.py`,
PGBrain validation/doctor checks, Remote MCP SKIP/PASS health checks, and
checks for obvious private-path leakage.

## First Real Pipeline

The starter node includes `AI Daily Brief` as the reference pipeline shape:

```text
radars -> signal queue -> confirmation -> triage -> daily brief
       -> optional NotebookLM research sidecar -> PGBrain
```

The production cron schedule and delivery channel are deliberately left as examples. Do not copy another person's Feishu channel or local state into a teammate node.
