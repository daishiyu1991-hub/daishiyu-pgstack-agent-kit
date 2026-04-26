#!/usr/bin/env bash
set -euo pipefail

KIT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if grep -RInE 'oc_[a-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|BEGIN (OPENSSH|RSA|EC|DSA) PRIVATE KEY|/Users/daishiyu|last_delivery_error|last_run_at' "$KIT_ROOT" \
  --exclude-dir .git \
  --exclude 'sanitize_check.sh'; then
  echo "sanitize check failed: private or machine-specific strings found" >&2
  exit 2
fi

echo "sanitize check passed"
