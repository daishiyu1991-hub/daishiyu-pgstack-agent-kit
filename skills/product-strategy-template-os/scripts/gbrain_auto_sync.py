#!/usr/bin/env python3
"""Best-effort native GBrain sync boundary for Product Strategy Template OS.

This mirrors the original gstack pattern: skill start/end should quietly try to
drain pending brain writes. If native gstack-brain-sync is not available, this
script does not invent a cloud write. It reports that the Hermes Admin handoff
queue is the active route.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def known_gstack_bin_dirs() -> list[Path]:
    dirs: list[Path] = []
    gstack_bin = os.environ.get("GSTACK_BIN")
    if gstack_bin:
        dirs.append(Path(gstack_bin).expanduser())
    dirs.append(Path.home() / "gstack" / "bin")
    return dirs


def find_gstack_tool(name: str) -> str | None:
    for directory in known_gstack_bin_dirs():
        candidate = directory / name
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    found = shutil.which(name)
    return found


def find_gstack_brain_sync() -> str | None:
    found = find_gstack_tool("gstack-brain-sync")
    if found:
        return found
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


def gstack_state_home() -> Path:
    return Path(os.environ.get("GSTACK_HOME", str(Path.home() / ".gstack"))).expanduser()


def gbrain_sync_mode() -> str:
    config_bin = find_gstack_tool("gstack-config")
    if not config_bin:
        return "unknown"
    code, output = run_command([config_bin, "get", "gbrain_sync_mode"])
    if code != 0:
        return "unknown"
    return output.strip() or "unknown"


def file_digest(root: Path, rels: list[str]) -> str:
    h = hashlib.sha256()
    for rel in rels:
        path = root / rel
        if path.exists():
            h.update(rel.encode("utf-8"))
            h.update(b"\0")
            h.update(path.read_bytes())
            h.update(b"\0")
    return h.hexdigest()


def register_global_rule_with_native_gbrain(root: Path) -> str:
    """Write a compact global-rule record into original gstack's allowlisted path.

    This is intentionally small and source-ref oriented. It lets native
    gstack-brain-sync receive the rule through its normal queue instead of
    relying on a custom cloud mutation.
    """

    state_home = gstack_state_home()
    if not (state_home / ".git").exists():
        return "skipped:not_initialized"

    mode = gbrain_sync_mode()
    if mode in {"off", "unknown"}:
        return f"skipped:mode={mode}"

    enqueue_bin = find_gstack_tool("gstack-brain-enqueue")
    if not enqueue_bin:
        return "skipped:no_enqueue_tool"

    source_refs = [
        "README.md",
        "SKILL.md",
        "references/global-rules.md",
        "scripts/gbrain_auto_sync.py",
        "gbrain/HERMES_ADMIN_HANDOFF.md",
    ]
    digest = file_digest(root, source_refs)

    project_dir = state_home / "projects" / "product-strategy-template-os"
    project_dir.mkdir(parents=True, exist_ok=True)
    marker = project_dir / ".global-rule.sha256"
    if marker.exists() and marker.read_text(encoding="utf-8").strip() == digest:
        return "unchanged"

    learning_path = project_dir / "learnings.jsonl"
    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": "global_rule",
        "source": "product-strategy-template-os",
        "scope": "team_candidate",
        "summary": (
            "Product Strategy Template OS must use native gstack-brain-sync at "
            "skill start/end. Do not ask the human to manually request GBrain "
            "sync each time. If native sync is unavailable, fall back to the "
            "Hermes Admin -> gbrain-remote handoff queue without claiming cloud "
            "write success."
        ),
        "source_refs": source_refs,
        "fingerprint": digest,
    }
    with learning_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    marker.write_text(digest + "\n", encoding="utf-8")

    rel = "projects/product-strategy-template-os/learnings.jsonl"
    run_command([enqueue_bin, rel])
    return f"queued:{rel}"


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
        global_rule_status = register_global_rule_with_native_gbrain(root)
        print(f"BRAIN_SYNC: global_rule={global_rule_status}")
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
