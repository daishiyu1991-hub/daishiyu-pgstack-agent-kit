# PGBrain Engine

`pgbrain_engine.py` is the deterministic local engine for this starter node.

Commands:

```bash
python3 engine/pgbrain_engine.py status
python3 engine/pgbrain_engine.py doctor
python3 engine/pgbrain_engine.py query "AI Daily Brief Job"
python3 engine/pgbrain_engine.py related "AI Daily Brief Job"
python3 engine/pgbrain_engine.py maintenance
python3 engine/pgbrain_engine.py maintenance --remote-mcp-smoke
node engine/gbrain_remote_mcp_health.mjs
node engine/gbrain_remote_mcp_health.mjs --write-smoke
node engine/gbrain_remote_mcp_http_server.mjs
python3 engine/skillpack_check.py
```

The engine is filesystem-backed and intentionally small.

`skillpack_check.py` validates the canonical repo-level skill manifest, resolver
coverage, and required `skills/*/SKILL.md` files. `PGBrain Engine` validate and
doctor also call this check.

## Optional GBrain Remote MCP

The kit includes Remote MCP commands:

- `gbrain_remote_mcp_health.mjs`: checks a configured GBrain Remote MCP route
  and returns `SKIP` when no token is configured.
- `gbrain_remote_mcp_http_server.mjs`: host-side HTTP MCP wrapper for a cloud
  GBrain memory center.

Configuration is explicit and never guessed:

```bash
export PGSTACK_GBRAIN_REMOTE_MCP_URL="https://your-host/gbrain/mcp"
export PGSTACK_GBRAIN_REMOTE_MCP_TOKEN="..."
```

See `docs/gbrain-remote-mcp.md` in the kit checkout.
