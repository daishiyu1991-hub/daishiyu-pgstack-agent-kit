#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${PGSTACK_KIT_REPO_URL:-https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit.git}"
INSTALL_DIR="${PGSTACK_KIT_INSTALL_DIR:-$HOME/.pgstack-agent-kit}"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required for one-click remote install" >&2
  exit 2
fi

if [[ -d "$INSTALL_DIR/.git" ]]; then
  git -C "$INSTALL_DIR" pull --ff-only
else
  rm -rf "$INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

exec "$INSTALL_DIR/install.sh" "$@"
