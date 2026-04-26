# PGBrain Engine

`pgbrain_engine.py` is the deterministic local engine for this starter node.

Commands:

```bash
python3 engine/pgbrain_engine.py status
python3 engine/pgbrain_engine.py doctor
python3 engine/pgbrain_engine.py query "AI Daily Brief Job"
python3 engine/pgbrain_engine.py related "AI Daily Brief Job"
python3 engine/pgbrain_engine.py maintenance
python3 engine/pgbrain_engine.py maintenance --central-brain-smoke
python3 engine/central_brain_health.py
python3 engine/central_brain_lookup.py smoke --memory-owner central
node engine/central_brain_mcp_server.mjs
python3 engine/skillpack_check.py
```

The engine is filesystem-backed and intentionally small.

`skillpack_check.py` validates the canonical repo-level skill manifest, resolver
coverage, and required `skills/*/SKILL.md` files. `PGBrain Engine` validate and
doctor also call this check.

## Optional Central Brain

The kit includes read-only central-brain commands:

- `central_brain_lookup.py`: queries a configured Central Brain Host GBrain
  first, then MemTensor as `memory_context`.
- `central_brain_health.py`: runs the central-brain smoke and returns `SKIP`
  when no SSH target is configured.
- `central_brain_mcp_server.mjs`: optional Codex-compatible MCP bridge over the
  lookup adapter.

Configuration is explicit and never guessed:

```bash
export PGSTACK_CENTRAL_BRAIN_SSH_TARGET="user@host"
export PGSTACK_CENTRAL_BRAIN_SSH_KEY="$HOME/.ssh/your_key"
export PGSTACK_CENTRAL_BRAIN_MEMORY_OWNER="central"
```

See `docs/central-brain.md` in the kit checkout.
