#!/usr/bin/env bash
set -euo pipefail

KIT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

export PGSTACK_HOME="$TMP_ROOT/pgstack"
export CODEX_HOME="$TMP_ROOT/codex"
export HERMES_HOME="$TMP_ROOT/hermes"

"$KIT_ROOT/install.sh" --force

python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" status
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" query "AI Daily Brief Job" --limit 3
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" related "AI Daily Brief Job" --limit 10
python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" maintenance --limit 10

"$KIT_ROOT/scripts/sanitize_check.sh"

echo "smoke test passed"

