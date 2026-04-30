#!/usr/bin/env python3
"""Best-effort native GBrain sync boundary for Product Strategy Template OS.

This mirrors the original gstack pattern: skill start/end should quietly try to
drain pending brain writes. If native gstack-brain-sync is not available, this
script does not invent a cloud write. It reports that the Hermes Admin handoff
queue is the active route.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


def find_gstack_brain_sync() -> str | None:
    gstack_bin = os.environ.get("GSTACK_BIN")
    if gstack_bin:
        candidate = Path(gstack_bin) / "gstack-brain-sync"
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)

    gstack_home = Path(os.environ.get("GSTACK_HOME", str(Path.home() / "gstack"))).expanduser()
    candidate = gstack_home / "bin" / "gstack-brain-sync"
    if candidate.exists() and os.access(candidate, os.X_OK):
        return str(candidate)

    found = shutil.which("gstack-brain-sync")
    return found


def run_command(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skill-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Installed product-strategy-template-os skill directory.",
    )
    parser.add_argument("--phase", choices=["start", "end", "manual"], default="manual")
    args = parser.parse_args()

    root = Path(args.skill_root).expanduser().resolve()
    sync_bin = find_gstack_brain_sync()
    if sync_bin:
        print(f"BRAIN_SYNC: native gstack-brain-sync detected ({args.phase})")
        for extra_args in (["--discover-new"], ["--once"]):
            code, output = run_command([sync_bin, *extra_args])
            if output:
                print(output)
            if code != 0:
                print(f"BRAIN_SYNC: command returned {code}: {sync_bin} {' '.join(extra_args)}")
        return

    status = read_json(root / "gbrain" / "gbrain-sync-status.json")
    packet = root / "gbrain" / "gbrain-handoff-packet-v1.json"
    queue = root / "gbrain" / "gbrain-sync-queue.jsonl"

    if packet.exists() and queue.exists():
        print(f"BRAIN_SYNC: native gstack-brain-sync not found ({args.phase})")
        print("BRAIN_SYNC: enterprise GBrain route is Hermes Admin -> gbrain-remote")
        print("BRAIN_SYNC: handoff queue is ready_for_hermes_admin")
        if status.get("verification_query"):
            print(f"BRAIN_SYNC: verification_query={status['verification_query']}")
    else:
        print(f"BRAIN_SYNC: no native sync tool and no handoff queue found ({args.phase})")


if __name__ == "__main__":
    main()
