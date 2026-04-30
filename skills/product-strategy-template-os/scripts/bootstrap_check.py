#!/usr/bin/env python3
"""Bootstrap validator for Product Strategy Template OS.

This script is intentionally dependency-light so another agent can run it right
after installing the skill. It checks that the portable OS files are present and
can optionally initialize a new run skeleton.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = [
    "README.md",
    "SKILL.md",
    "references/global-rules.md",
    "references/pipeline-architecture.md",
    "references/template-structure.zh.md",
    "references/data-source-router.md",
    "references/red-team-company-baseline.md",
    "references/frontend-report-style.md",
    "schemas/pipeline-run-state.schema.json",
    "schemas/evidence-ledger.schema.json",
    "schemas/human-decision.schema.json",
    "schemas/execution-plan.schema.json",
    "templates/index.html",
    "templates/complete-report.html",
    "templates/chapter-execution-plan.json",
    "templates/evidence-ledger.json",
    "templates/human-decision.json",
    "scripts/init_run.py",
    "scripts/validate_run.py",
    "scripts/sanitize_check.py",
    "gbrain/HERMES_ADMIN_HANDOFF.md",
    "gbrain/gbrain-handoff-packet-v1.json",
    "gbrain/gbrain-sync-queue.jsonl",
    "gbrain/gbrain-sync-status.json",
]


def fail(message: str) -> None:
    print(f"BOOTSTRAP_ERROR\t{message}")
    raise SystemExit(1)


def check_json_files(root: Path) -> None:
    for path in root.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - CLI utility
            fail(f"invalid json: {path.relative_to(root)}: {exc}")


def check_required_files(root: Path) -> None:
    missing = [rel for rel in REQUIRED_FILES if not (root / rel).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def run_sanitize(root: Path) -> None:
    script = root / "scripts" / "sanitize_check.py"
    result = subprocess.run(
        [sys.executable, str(script), str(root)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout, end="")
        fail("sanitize check failed")


def init_run(root: Path, out: Path, category: str, marketplace: str) -> None:
    init_script = root / "scripts" / "init_run.py"
    validate_script = root / "scripts" / "validate_run.py"
    subprocess.run(
        [
            sys.executable,
            str(init_script),
            "--category",
            category,
            "--marketplace",
            marketplace,
            "--out",
            str(out),
        ],
        check=True,
    )
    subprocess.run([sys.executable, str(validate_script), str(out)], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skill-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Installed product-strategy-template-os skill directory.",
    )
    parser.add_argument("--category", help="Optional category for run init.")
    parser.add_argument("--marketplace", default="US", help="Optional marketplace for run init.")
    parser.add_argument("--init-run", help="Optional output run directory to initialize.")
    args = parser.parse_args()

    root = Path(args.skill_root).expanduser().resolve()
    if not root.exists():
        fail(f"skill root does not exist: {root}")

    check_required_files(root)
    check_json_files(root)
    run_sanitize(root)

    if args.init_run:
        if not args.category:
            fail("--category is required when --init-run is provided")
        init_run(root, Path(args.init_run).expanduser().resolve(), args.category, args.marketplace)

    print("OK_BOOTSTRAP")
    print(f"skill_root={root}")
    if args.init_run:
        print(f"run_dir={Path(args.init_run).expanduser().resolve()}")


if __name__ == "__main__":
    main()
