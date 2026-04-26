# GBrain Remote MCP Setup

The kit supports one formal cloud memory-center route:

```text
local agent
-> gbrain-remote MCP
-> cloud GBrain Remote MCP endpoint
-> cloud Brain Repo
```

MemTensor can still exist as TeamHub or retrieval context, but it is not a
fallback hidden inside this route.

## Required Configuration

Do not commit real values.

```bash
export PGSTACK_GBRAIN_REMOTE_MCP_URL="https://your-host/gbrain/mcp"
export PGSTACK_GBRAIN_REMOTE_MCP_TOKEN="..."
```

For Codex:

```bash
codex mcp add gbrain-remote \
  --url "$PGSTACK_GBRAIN_REMOTE_MCP_URL" \
  --bearer-token-env-var PGSTACK_GBRAIN_REMOTE_MCP_TOKEN
```

## Commands

```bash
node "$PGSTACK_HOME/engine/gbrain_remote_mcp_health.mjs"
node "$PGSTACK_HOME/engine/gbrain_remote_mcp_health.mjs" --require-config
node "$PGSTACK_HOME/engine/gbrain_remote_mcp_health.mjs" --require-config --write-smoke
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" maintenance --remote-mcp-smoke
```

Expected local-only result before configuration:

```text
verdict: SKIP
```

Expected configured result:

```text
verdict: PASS
```

## Host-Side Wrapper

If a cloud host needs to expose a local GBrain installation through HTTP MCP,
install the wrapper as a host service and proxy it through an approved route:

```text
:8480/gbrain/mcp
-> 127.0.0.1:8787
-> /opt/pgstack-gbrain/gbrain_remote_mcp_http_server.mjs
-> docker exec hermes-admin
-> /opt/data/gbrain src/cli.ts
```

The wrapper must require a bearer token and should stay on loopback behind the
approved reverse proxy.

## Safety Boundary

- Remote MCP is the canonical GBrain route.
- Do not install a second hidden memory center.
- Do not call MemTensor as an implicit fallback inside this route.
- Do not commit tokens, host-specific URLs, Feishu channels, cookies, or private
  notes.
- Run write smoke only when changing the cloud route or accepting a new memory
  center.
