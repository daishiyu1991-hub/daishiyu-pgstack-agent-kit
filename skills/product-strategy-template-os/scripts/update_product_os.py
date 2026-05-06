#!/usr/bin/env python3
"""Update Product Strategy Template OS from GitHub and verify the install.

This script is intentionally small so teammate agents can run it when the
human says `/update product-os`. It does not touch research run folders.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_REPO = "https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit"
DEFAULT_SKILL = "product-strategy-template-os"


def run(cmd: list[str], *, dry_run: bool = False) -> None:
    print("$ " + " ".join(cmd))
    if dry_run:
        return
    subprocess.run(cmd, check=True)


def default_skill_root(skill_name: str) -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    return codex_home / "skills" / skill_name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=os.environ.get("PRODUCT_OS_REPO_URL", DEFAULT_REPO))
    parser.add_argument("--skill", default=os.environ.get("PRODUCT_OS_SKILL", DEFAULT_SKILL))
    parser.add_argument("--skill-root", help="Installed skill root after update.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).expanduser() if args.skill_root else default_skill_root(args.skill)

    run(["npx", "skills", "add", args.repo, "--skill", args.skill], dry_run=args.dry_run)

    bootstrap = skill_root / "scripts" / "bootstrap_check.py"
    if not args.dry_run and not bootstrap.exists():
        raise SystemExit(f"BOOTSTRAP_ERROR\tupdated skill missing bootstrap_check.py: {bootstrap}")

    run([sys.executable, str(bootstrap), "--skill-root", str(skill_root)], dry_run=args.dry_run)

    print("OK_UPDATE_PRODUCT_OS")
    print(f"repo={args.repo}")
    print(f"skill={args.skill}")
    print(f"skill_root={skill_root}")


if __name__ == "__main__":
    main()
