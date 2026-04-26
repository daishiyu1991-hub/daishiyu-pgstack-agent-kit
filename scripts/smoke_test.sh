#!/usr/bin/env bash
set -euo pipefail

KIT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

export PGSTACK_HOME="$TMP_ROOT/pgstack"
export CODEX_HOME="$TMP_ROOT/codex"
export HERMES_HOME="$TMP_ROOT/hermes"

"$KIT_ROOT/install.sh" --force

python3 "$PGSTACK_HOME/engine/skillpack_check.py"
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" status
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" validate
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" query "AI Daily Brief Job" --limit 3
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" query "PGStack Repo Skillpack Protocol" --limit 5
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" query "PGStack GBrain Compatibility Layer" --limit 5
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" query "PGStack Upstream Parity Checklist" --limit 5
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" query "PGStack Agent Layer Stage 3.5 agent router" --limit 5
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" related "AI Daily Brief Job" --limit 10
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" related "PGStack Repo Skillpack Protocol" --limit 10
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" related "PGStack GBrain Compatibility Layer" --limit 10
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" related "PGStack Upstream Parity Checklist" --limit 10
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" related "PGStack Agent Layer Stage 3.5" --limit 10
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" maintenance --limit 10
python3 "$PGSTACK_HOME/engine/central_brain_health.py" --json
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" maintenance --central-brain-smoke --limit 10
node --check "$PGSTACK_HOME/engine/central_brain_mcp_server.mjs"

"$KIT_ROOT/scripts/sanitize_check.sh"

echo "smoke test passed"
