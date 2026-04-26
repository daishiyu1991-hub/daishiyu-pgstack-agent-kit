# Central Brain Setup

The kit includes optional read-only commands for connecting a node to a
Central Brain Host.

Use this only after the local starter node passes its base smoke test.

## What This Adds

```text
local PGStack Node
-> central_brain_lookup.py
-> configured Central Brain Host GBrain first
-> MemTensor retrieval delegate second
```

The local node remains useful without this integration. Central Brain is for
teams or multi-agent setups that want one durable shared brain host.

## Required Configuration

Set these in the agent/runtime environment. Do not commit real values.

```bash
export PGSTACK_CENTRAL_BRAIN_SSH_TARGET="user@host"
export PGSTACK_CENTRAL_BRAIN_SSH_KEY="$HOME/.ssh/your_key"
export PGSTACK_CENTRAL_BRAIN_CONTAINER="hermes-admin"
export PGSTACK_CENTRAL_BRAIN_MEMORY_OWNER="central"
```

Optional:

```bash
export PGSTACK_CENTRAL_BRAIN_GBRAIN_BIN="/opt/data/.bun/bin/gbrain"
export PGSTACK_CENTRAL_BRAIN_GBRAIN_CWD="/opt/data/gbrain"
export PGSTACK_CENTRAL_BRAIN_TIMEOUT="30"
export PGSTACK_CENTRAL_BRAIN_SMOKE_MARKER=""
```

`PGSTACK_CENTRAL_BRAIN_SMOKE_MARKER` is needed only if you want the smoke test
to verify a known MemTensor write-through marker. Without it, smoke verifies
GBrain reachability and safely skips marker-specific memory fallback.

## Commands

```bash
python3 "$PGSTACK_HOME/engine/central_brain_health.py"
python3 "$PGSTACK_HOME/engine/central_brain_health.py" --require-config
python3 "$PGSTACK_HOME/engine/central_brain_lookup.py" lookup --query "central brain host" --memory-owner central
python3 "$PGSTACK_HOME/engine/central_brain_lookup.py" smoke --memory-owner central
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" maintenance --central-brain-smoke
```

Expected local-only result before configuration:

```text
verdict: SKIP
```

Expected configured result:

```text
verdict: PASS
```

## Optional Codex MCP Bridge

The installed node includes:

```text
engine/central_brain_mcp_server.mjs
```

Register it only after the local agent has Node.js plus a compatible MCP SDK
and `zod` available. The bridge is read-only and calls
`central_brain_lookup.py`; it does not start a competing cloud `gbrain serve`
process and does not write MemTensor.

Generic command shape:

```bash
node "$PGSTACK_HOME/engine/central_brain_mcp_server.mjs"
```

If your MCP SDK is not installed as a normal Node package, provide explicit
entry paths:

```bash
export PGSTACK_MCP_SERVER_ENTRY="/path/to/@modelcontextprotocol/sdk/server/mcp.js"
export PGSTACK_MCP_STDIO_ENTRY="/path/to/@modelcontextprotocol/sdk/server/stdio.js"
export PGSTACK_ZOD_ENTRY="/path/to/zod/index.js"
```

## Safety Boundary

- The adapter is read-only.
- The SSH target is never guessed.
- Missing config returns `SKIP` unless `--require-config` is used.
- MemTensor is context, not source of truth.
- Durable rules still belong in PGBrain source pages.
