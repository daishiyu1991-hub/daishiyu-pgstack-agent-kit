#!/usr/bin/env bash
set -euo pipefail

KIT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PGSTACK_HOME="${PGSTACK_HOME:-$HOME/Documents/PGStack/personal-gstack}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"

INSTALL_CODEX=1
INSTALL_HERMES=1
FORCE=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: ./install.sh [options]

Options:
  --no-codex     Skip installing Codex skills
  --no-hermes    Skip installing Hermes skills
  --force        Overwrite existing installed files
  --dry-run      Print actions without copying
  -h, --help     Show help

Environment:
  PGSTACK_HOME   Default: ~/Documents/PGStack/personal-gstack
  CODEX_HOME     Default: ~/.codex
  HERMES_HOME    Default: ~/.hermes
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-codex) INSTALL_CODEX=0 ;;
    --no-hermes) INSTALL_HERMES=0 ;;
    --force) FORCE=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

copy_dir() {
  local src="$1"
  local dst="$2"
  local label="$3"

  if [[ ! -d "$src" ]]; then
    echo "missing source: $src" >&2
    exit 2
  fi

  if [[ -e "$dst" && "$FORCE" != "1" ]]; then
    echo "skip existing $label: $dst"
    return 0
  fi

  echo "install $label: $dst"
  if [[ "$DRY_RUN" == "1" ]]; then
    return 0
  fi

  mkdir -p "$(dirname "$dst")"
  rm -rf "$dst"
  mkdir -p "$dst"
  cp -R "$src"/. "$dst"/
}

copy_file() {
  local src="$1"
  local dst="$2"
  local label="$3"

  if [[ -e "$dst" && "$FORCE" != "1" ]]; then
    echo "skip existing $label: $dst"
    return 0
  fi

  echo "install $label: $dst"
  if [[ "$DRY_RUN" == "1" ]]; then
    return 0
  fi

  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
}

copy_dir "$KIT_ROOT/templates/pgstack-wiki" "$PGSTACK_HOME" "PGStack starter wiki"

if [[ "$INSTALL_CODEX" == "1" ]]; then
  for skill in "$KIT_ROOT"/skills/codex/*; do
    [[ -d "$skill" ]] || continue
    copy_dir "$skill" "$CODEX_HOME/skills/$(basename "$skill")" "Codex skill $(basename "$skill")"
  done
  copy_file "$KIT_ROOT/config/codex-global-rules.example.md" "$CODEX_HOME/AGENTS.pgstack.example.md" "Codex PGStack rules example"
fi

if [[ "$INSTALL_HERMES" == "1" ]]; then
  for skill in "$KIT_ROOT"/skills/hermes/research/*; do
    [[ -d "$skill" ]] || continue
    copy_dir "$skill" "$HERMES_HOME/skills/research/$(basename "$skill")" "Hermes skill $(basename "$skill")"
  done
  copy_file "$KIT_ROOT/config/hermes-cron.example.json" "$HERMES_HOME/cron/pgstack-jobs.example.json" "Hermes cron examples"
fi

if [[ "$DRY_RUN" != "1" ]]; then
  python3 "$PGSTACK_HOME/engine/pgbrain_engine.py" doctor
fi

cat <<EOF

PGStack Agent Kit installed.

PGSTACK_HOME=$PGSTACK_HOME
CODEX_HOME=$CODEX_HOME
HERMES_HOME=$HERMES_HOME

Next:
1. Review $PGSTACK_HOME/AGENTS.md
2. Configure Hermes cron from $HERMES_HOME/cron/pgstack-jobs.example.json
3. Connect your own Feishu/MemTensor/GitHub/NotebookLM credentials if desired.
EOF

