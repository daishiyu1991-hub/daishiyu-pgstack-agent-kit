#!/usr/bin/env python3
"""Maintenance smoke check for the cloud Central Brain Host.

This is a thin wrapper around `central_brain_lookup.py smoke`.

It is intentionally read-only and configuration-sensitive:
- if the central brain SSH target is not configured, the default behavior is a
  non-failing SKIP so local-only maintenance can still run;
- `--require-config` turns missing configuration into a failure for production
  acceptance checks.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOOKUP_SCRIPT = ROOT / "engine" / "central_brain_lookup.py"
DEFAULT_MEMORY_OWNER = "central"
DEFAULT_TIMEOUT_SECONDS = 40


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the PGStack Central Brain maintenance smoke check.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON only.")
    parser.add_argument(
        "--require-config",
        action="store_true",
        help="Fail instead of SKIP when central brain SSH configuration is missing.",
    )
    parser.add_argument("--memory-owner", default=DEFAULT_MEMORY_OWNER)
    parser.add_argument("--max-results", type=int, default=3)
    parser.add_argument("--min-score", type=float, default=0.0)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--smoke-marker", default="")
    return parser.parse_args()


def has_required_config() -> tuple[bool, list[str]]:
    missing: list[str] = []
    if not os.environ.get("PGSTACK_CENTRAL_BRAIN_SSH_TARGET"):
        missing.append("PGSTACK_CENTRAL_BRAIN_SSH_TARGET")
    ssh_key = os.environ.get("PGSTACK_CENTRAL_BRAIN_SSH_KEY", "")
    if not ssh_key:
        missing.append("PGSTACK_CENTRAL_BRAIN_SSH_KEY")
    elif not Path(ssh_key).expanduser().exists():
        missing.append("PGSTACK_CENTRAL_BRAIN_SSH_KEY_EXISTS")
    return not missing, missing


def run_lookup_smoke(args: argparse.Namespace) -> tuple[int, dict[str, Any], str]:
    cmd = [
        sys.executable,
        str(LOOKUP_SCRIPT),
        "smoke",
        "--memory-owner",
        args.memory_owner,
        "--max-results",
        str(args.max_results),
        "--min-score",
        str(args.min_score),
        "--timeout",
        str(args.timeout),
    ]
    if args.smoke_marker:
        cmd.extend(["--smoke-marker", args.smoke_marker])

    completed = subprocess.run(
        cmd,
        check=False,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=max(args.timeout + 10, 20),
    )
    output = completed.stdout.strip()
    if not output:
        return completed.returncode or 2, {}, completed.stderr[-1200:]
    try:
        return completed.returncode, json.loads(output), completed.stderr[-1200:]
    except json.JSONDecodeError:
        return completed.returncode or 2, {"raw_output": output[-1200:]}, completed.stderr[-1200:]


def build_skip(missing: list[str]) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "check": "central_brain_health",
        "stage": "stage3.3-maintenance-smoke",
        "verdict": "SKIP",
        "reason": "central brain SSH configuration missing",
        "missing": missing,
        "read_only": True,
    }


def build_result(returncode: int, smoke: dict[str, Any], stderr: str) -> dict[str, Any]:
    verdict = "PASS" if returncode == 0 and smoke.get("verdict") == "PASS" else "FAIL"
    checks = smoke.get("checks", []) if isinstance(smoke.get("checks"), list) else []
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "check": "central_brain_health",
        "stage": "stage3.3-maintenance-smoke",
        "verdict": verdict,
        "read_only": True,
        "command_returncode": returncode,
        "memory_owner_route": smoke.get("memory_owner_route", {}),
        "checks": checks,
        "brain_hit_count": len(((smoke.get("brain_lookup") or {}).get("brain") or {}).get("hits", [])),
        "memory_hit_count": len(((smoke.get("memory_lookup") or {}).get("memory") or {}).get("hits", [])),
        "stderr_preview": stderr,
    }


def print_human(result: dict[str, Any]) -> None:
    print("Central Brain maintenance smoke")
    print("--------------------------------")
    print(f"stage: {result.get('stage')}")
    print(f"verdict: {result.get('verdict')}")
    route = result.get("memory_owner_route") or {}
    if route:
        print(
            "memory_owner_route: "
            f"{route.get('requested')} -> {route.get('resolved')} "
            f"(alias_applied={route.get('alias_applied')})"
        )
    if result.get("missing"):
        print("missing:")
        for item in result["missing"]:
            print(f"  {item}")
    checks = result.get("checks") or []
    if checks:
        print("checks:")
        for check in checks:
            print(
                f"  {check.get('name')}: "
                f"{'PASS' if check.get('passed') else 'FAIL'} "
                f"(evidence_count={check.get('evidence_count')})"
            )
    if "brain_hit_count" in result:
        print(f"brain_hit_count: {result.get('brain_hit_count')}")
    if "memory_hit_count" in result:
        print(f"memory_hit_count: {result.get('memory_hit_count')}")


def main() -> int:
    args = parse_args()
    configured, missing = has_required_config()
    if not configured:
        result = build_skip(missing)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_human(result)
        return 2 if args.require_config else 0

    try:
        returncode, smoke, stderr = run_lookup_smoke(args)
        result = build_result(returncode, smoke, stderr)
    except subprocess.TimeoutExpired as exc:
        result = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "check": "central_brain_health",
            "stage": "stage3.3-maintenance-smoke",
            "verdict": "FAIL",
            "read_only": True,
            "error": f"timed out after {exc.timeout}s",
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)
    return 0 if result.get("verdict") in {"PASS", "SKIP"} and not args.require_config else (0 if result.get("verdict") == "PASS" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
