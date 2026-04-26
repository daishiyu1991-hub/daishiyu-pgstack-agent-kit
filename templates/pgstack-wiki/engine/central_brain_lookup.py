#!/usr/bin/env python3
"""Cloud-centered PGStack brain lookup adapter.

This is the Stage 2 thin adapter and Stage 3 runtime entry for:

GBrain source-of-truth pages first -> MemTensor memory_context fallback.

It is intentionally read-only. It does not mutate cloud GBrain, MemTensor, or
local Obsidian state.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import socket
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_CONTAINER = "hermes-admin"
DEFAULT_GBRAIN_BIN = "/opt/data/.bun/bin/gbrain"
DEFAULT_GBRAIN_CWD = "/opt/data/gbrain"
DEFAULT_MEMTENSOR_HOST = "127.0.0.1"
DEFAULT_MEMTENSOR_PORT = 18992
DEFAULT_MEMORY_OWNER = "hermes"
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_SMOKE_MARKER = os.environ.get("PGSTACK_CENTRAL_BRAIN_SMOKE_MARKER", "")
BASE_STAGE = "stage2-thin-adapter"
CURRENT_STAGE = "stage3-runtime-entry"
MEMORY_OWNER_ALIASES = {
    "central": "hermes",
    "cloud": "hermes",
    "hermes-admin": "hermes",
    "hermes_admin": "hermes",
}


@dataclass
class CentralBrainConfig:
    ssh_target: str
    ssh_key: str
    container: str
    gbrain_bin: str
    gbrain_cwd: str
    memtensor_host: str
    memtensor_port: int
    requested_memory_owner: str
    memory_owner: str
    timeout_seconds: int


class LookupErrorWithContext(RuntimeError):
    def __init__(self, message: str, *, command: list[str] | None = None, output: str = "") -> None:
        super().__init__(message)
        self.command = command or []
        self.output = output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query the cloud Central Brain Host using GBrain first and MemTensor second.",
    )
    parser.add_argument("command", choices=("lookup", "smoke"), help="Run one lookup or acceptance smoke tests.")
    parser.add_argument("--query", default="", help="Query text for lookup mode.")
    parser.add_argument(
        "--ssh-target",
        default=os.environ.get("PGSTACK_CENTRAL_BRAIN_SSH_TARGET", ""),
        help="SSH target for the Central Brain Host, or PGSTACK_CENTRAL_BRAIN_SSH_TARGET.",
    )
    parser.add_argument(
        "--ssh-key",
        default=os.environ.get("PGSTACK_CENTRAL_BRAIN_SSH_KEY", ""),
        help="SSH private key path, or PGSTACK_CENTRAL_BRAIN_SSH_KEY.",
    )
    parser.add_argument("--container", default=os.environ.get("PGSTACK_CENTRAL_BRAIN_CONTAINER", DEFAULT_CONTAINER))
    parser.add_argument("--gbrain-bin", default=os.environ.get("PGSTACK_CENTRAL_BRAIN_GBRAIN_BIN", DEFAULT_GBRAIN_BIN))
    parser.add_argument("--gbrain-cwd", default=os.environ.get("PGSTACK_CENTRAL_BRAIN_GBRAIN_CWD", DEFAULT_GBRAIN_CWD))
    parser.add_argument(
        "--memory-owner",
        default=os.environ.get("PGSTACK_CENTRAL_BRAIN_MEMORY_OWNER", DEFAULT_MEMORY_OWNER),
        help="MemTensor owner route. Aliases: central/cloud/hermes-admin -> hermes.",
    )
    parser.add_argument("--max-results", type=int, default=6)
    parser.add_argument("--min-score", type=float, default=0.0)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument(
        "--smoke-marker",
        default=DEFAULT_SMOKE_MARKER,
        help=(
            "Optional known memory marker for testing MemTensor fallback. "
            "If omitted, smoke verifies cloud GBrain reachability and skips the marker-specific memory assertion."
        ),
    )
    parser.add_argument("--no-memory", action="store_true", help="Only query cloud GBrain.")
    parser.add_argument("--no-brain", action="store_true", help="Only query cloud MemTensor.")
    return parser.parse_args()


def resolve_memory_owner(owner: str) -> str:
    normalized = (owner or DEFAULT_MEMORY_OWNER).strip()
    return MEMORY_OWNER_ALIASES.get(normalized.lower(), normalized)


def config_from_args(args: argparse.Namespace) -> CentralBrainConfig:
    if not args.ssh_target:
        raise SystemExit(
            "Missing --ssh-target or PGSTACK_CENTRAL_BRAIN_SSH_TARGET. "
            "This adapter defaults to the cloud center but never guesses a host."
        )
    ssh_key = args.ssh_key
    if ssh_key:
        ssh_key = str(Path(ssh_key).expanduser())
    requested_memory_owner = (args.memory_owner or DEFAULT_MEMORY_OWNER).strip()
    memory_owner = resolve_memory_owner(requested_memory_owner)
    return CentralBrainConfig(
        ssh_target=args.ssh_target,
        ssh_key=ssh_key,
        container=args.container,
        gbrain_bin=args.gbrain_bin,
        gbrain_cwd=args.gbrain_cwd,
        memtensor_host=DEFAULT_MEMTENSOR_HOST,
        memtensor_port=DEFAULT_MEMTENSOR_PORT,
        requested_memory_owner=requested_memory_owner,
        memory_owner=memory_owner,
        timeout_seconds=args.timeout,
    )


def remote_command(remote_args: list[str]) -> str:
    return " ".join(shlex.quote(str(arg)) for arg in remote_args)


def run_ssh(cfg: CentralBrainConfig, remote_args: list[str]) -> str:
    cmd = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        "StrictHostKeyChecking=no",
    ]
    if cfg.ssh_key:
        cmd.extend(["-i", cfg.ssh_key])
    cmd.extend([cfg.ssh_target, remote_command(remote_args)])

    try:
        completed = subprocess.run(
            cmd,
            check=False,
            text=True,
            capture_output=True,
            timeout=cfg.timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise LookupErrorWithContext("SSH command timed out", command=cmd, output=str(exc)) from exc

    if completed.returncode != 0:
        output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
        raise LookupErrorWithContext("SSH command failed", command=cmd, output=output)
    return completed.stdout


def parse_gbrain_query(output: str, max_results: int) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for line in output.splitlines():
        stripped = line.strip()
        match = re.match(r"^\[([0-9.]+)\]\s+(.+?)\s*$", stripped)
        if not match:
            continue
        target = match.group(2).strip()
        title = ""
        if " -- " in target:
            target, title = [part.strip() for part in target.split(" -- ", 1)]
        if " | " in target:
            target, title = [part.strip() for part in target.split(" | ", 1)]
        hits.append(
            {
                "authority": "brain_page",
                "source": "gbrain",
                "score": float(match.group(1)),
                "path": target,
                "title": title or target.rsplit("/", 1)[-1],
            }
        )
        if len(hits) >= max_results:
            break
    return hits


def gbrain_lookup(cfg: CentralBrainConfig, query: str, max_results: int) -> dict[str, Any]:
    remote_args = [
        "docker",
        "exec",
        "-w",
        cfg.gbrain_cwd,
        cfg.container,
        cfg.gbrain_bin,
        "query",
        query,
    ]
    try:
        output = run_ssh(cfg, remote_args)
    except LookupErrorWithContext as exc:
        return {
            "ok": False,
            "authority": "brain_page",
            "error": str(exc),
            "output": exc.output[-1200:],
            "hits": [],
        }

    return {
        "ok": True,
        "authority": "brain_page",
        "hits": parse_gbrain_query(output, max_results),
        "raw_preview": output[:1200],
    }


def memtensor_rpc(cfg: CentralBrainConfig, method: str, params: dict[str, Any]) -> dict[str, Any]:
    payload = {"jsonrpc": "2.0", "id": method, "method": method, "params": params}
    code = r"""
import json
import socket
import sys

payload = json.loads(sys.argv[1])
host = sys.argv[2]
port = int(sys.argv[3])
sock = socket.create_connection((host, port), timeout=8)
sock.sendall((json.dumps(payload) + "\n").encode("utf-8"))
buf = b""
while not buf.endswith(b"\n"):
    chunk = sock.recv(65536)
    if not chunk:
        break
    buf += chunk
sock.close()
print(buf.decode("utf-8"), end="")
"""
    remote_args = [
        "docker",
        "exec",
        cfg.container,
        "python3",
        "-c",
        code,
        json.dumps(payload, ensure_ascii=True),
        cfg.memtensor_host,
        str(cfg.memtensor_port),
    ]
    output = run_ssh(cfg, remote_args)
    return json.loads(output)


def owner_route_match(hit: dict[str, Any], cfg: CentralBrainConfig) -> tuple[bool, str]:
    owner = str(hit.get("owner", ""))
    text = " ".join(
        str(hit.get(key, ""))
        for key in ("summary", "original_excerpt", "content", "excerpt")
    )
    exact_candidates = {
        cfg.memory_owner,
        cfg.requested_memory_owner,
    }
    if owner in exact_candidates:
        return True, "exact-owner-field"
    if any(candidate and candidate in owner for candidate in exact_candidates):
        return True, "owner-field-contains"
    for candidate in (cfg.memory_owner, cfg.requested_memory_owner):
        if candidate and (f"owner={candidate}" in text or f"owner: {candidate}" in text):
            return True, "content-owner-marker"
    if owner.startswith("hub-user:"):
        return False, "hub-user-owner-unresolved"
    return False, "no-owner-route-match"


def normalize_memory_hit(hit: dict[str, Any], cfg: CentralBrainConfig) -> dict[str, Any]:
    ref = hit.get("ref") if isinstance(hit.get("ref"), dict) else {}
    source = hit.get("source") if isinstance(hit.get("source"), dict) else {}
    matched, match_method = owner_route_match(hit, cfg)
    return {
        "authority": "memory_context",
        "source": "memtensor",
        "score": hit.get("score"),
        "summary": hit.get("summary", ""),
        "excerpt": hit.get("original_excerpt", ""),
        "owner": hit.get("owner", ""),
        "origin": hit.get("origin", ""),
        "ref": {
            "sessionKey": ref.get("sessionKey", ""),
            "chunkId": ref.get("chunkId", ""),
            "turnId": ref.get("turnId", ""),
            "seq": ref.get("seq", 0),
        },
        "source_role": source.get("role", ""),
        "source_ts": source.get("ts", ""),
        "owner_route": {
            "requested": cfg.requested_memory_owner,
            "resolved": cfg.memory_owner,
            "matched": matched,
            "match_method": match_method,
        },
    }


def memtensor_lookup(cfg: CentralBrainConfig, query: str, max_results: int, min_score: float) -> dict[str, Any]:
    params = {
        "query": query,
        "maxResults": max_results,
        "minScore": min_score,
        "owner": cfg.memory_owner,
    }
    try:
        rpc_result = memtensor_rpc(cfg, "search", params)
    except (LookupErrorWithContext, socket.timeout, json.JSONDecodeError, OSError) as exc:
        output = getattr(exc, "output", "")
        return {
            "ok": False,
            "authority": "memory_context",
            "memory_owner": cfg.memory_owner,
            "error": str(exc),
            "output": output[-1200:] if output else "",
            "hits": [],
        }

    if "error" in rpc_result:
        return {
            "ok": False,
            "authority": "memory_context",
            "memory_owner": cfg.memory_owner,
            "error": rpc_result["error"],
            "hits": [],
        }

    result = rpc_result.get("result", {})
    hits = result.get("hits", []) if isinstance(result, dict) else []
    return {
        "ok": True,
        "authority": "memory_context",
        "requested_memory_owner": cfg.requested_memory_owner,
        "memory_owner": cfg.memory_owner,
        "owner_route": {
            "requested": cfg.requested_memory_owner,
            "resolved": cfg.memory_owner,
            "alias_applied": cfg.requested_memory_owner != cfg.memory_owner,
        },
        "hits": [normalize_memory_hit(hit, cfg) for hit in hits[:max_results] if isinstance(hit, dict)],
        "meta": result.get("meta", {}) if isinstance(result, dict) else {},
    }


def merge_results(brain: dict[str, Any], memory: dict[str, Any], max_results: int) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for hit in brain.get("hits", []):
        if isinstance(hit, dict):
            merged.append(hit)
    for hit in memory.get("hits", []):
        if isinstance(hit, dict):
            merged.append(hit)
    return merged[: max_results * 2]


def lookup(cfg: CentralBrainConfig, args: argparse.Namespace, query: str) -> dict[str, Any]:
    if not query.strip():
        raise SystemExit("Missing --query for lookup mode.")

    brain = {"ok": True, "authority": "brain_page", "hits": [], "skipped": True}
    memory = {"ok": True, "authority": "memory_context", "hits": [], "skipped": True}

    if not args.no_brain:
        brain = gbrain_lookup(cfg, query, args.max_results)
    if not args.no_memory:
        memory = memtensor_lookup(cfg, query, args.max_results, args.min_score)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "adapter": "central_brain_lookup",
        "stage": CURRENT_STAGE,
        "base_stage": BASE_STAGE,
        "runtime": "cloud",
        "brain_target": "ECS hermes-admin Central Brain Host",
        "requested_memory_owner": cfg.requested_memory_owner,
        "memory_owner": cfg.memory_owner,
        "memory_owner_route": {
            "requested": cfg.requested_memory_owner,
            "resolved": cfg.memory_owner,
            "alias_applied": cfg.requested_memory_owner != cfg.memory_owner,
        },
        "query": query,
        "gates": {
            "cloud_first": True,
            "brain_first": not args.no_brain,
            "explicit_memory_owner": bool(cfg.memory_owner),
            "no_raw_vector_assumption": True,
            "read_only": True,
        },
        "brain": brain,
        "memory": memory,
        "merged": merge_results(brain, memory, args.max_results),
    }


def contains_text(hit: dict[str, Any], needle: str) -> bool:
    haystack = " ".join(str(hit.get(key, "")) for key in ("path", "title", "summary", "excerpt"))
    return needle in haystack


def smoke(cfg: CentralBrainConfig, args: argparse.Namespace) -> dict[str, Any]:
    brain_result = lookup(cfg, args, "central brain host")
    memory_result: dict[str, Any] = {
        "skipped": True,
        "reason": "no smoke marker configured",
        "hint": "Set PGSTACK_CENTRAL_BRAIN_SMOKE_MARKER or pass --smoke-marker to verify MemTensor fallback.",
    }

    brain_hits = brain_result.get("brain", {}).get("hits", [])
    brain_passed = any(
        contains_text(hit, "central-brain-host")
        or contains_text(hit, "central-brain-operating-model")
        for hit in brain_hits
        if isinstance(hit, dict)
    )
    memory_hits: list[dict[str, Any]] = []
    memory_passed = True
    memory_skipped = not bool(args.smoke_marker.strip())
    if not memory_skipped:
        memory_args = argparse.Namespace(**vars(args))
        memory_args.no_brain = True
        memory_args.no_memory = False
        memory_result = lookup(cfg, memory_args, args.smoke_marker)
        memory_hits = memory_result.get("memory", {}).get("hits", [])
        memory_passed = any(
            contains_text(hit, args.smoke_marker)
            and bool((hit.get("owner_route") or {}).get("matched"))
            for hit in memory_hits
            if isinstance(hit, dict)
        )

    checks = [
        {
            "name": "brain_first_central_page",
            "passed": brain_passed,
            "skipped": False,
            "evidence_count": len(brain_hits),
        },
        {
            "name": "memtensor_owner_routed_fallback",
            "passed": memory_passed,
            "skipped": memory_skipped,
            "requested_memory_owner": cfg.requested_memory_owner,
            "memory_owner": cfg.memory_owner,
            "evidence_count": len(memory_hits),
        },
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "adapter": "central_brain_lookup",
        "stage": CURRENT_STAGE,
        "base_stage": BASE_STAGE,
        "runtime": "cloud",
        "requested_memory_owner": cfg.requested_memory_owner,
        "memory_owner": cfg.memory_owner,
        "memory_owner_route": {
            "requested": cfg.requested_memory_owner,
            "resolved": cfg.memory_owner,
            "alias_applied": cfg.requested_memory_owner != cfg.memory_owner,
        },
        "verdict": "PASS" if all(check["passed"] for check in checks) else "FAIL",
        "checks": checks,
        "brain_lookup": brain_result,
        "memory_lookup": memory_result,
    }


def main() -> int:
    args = parse_args()
    cfg = config_from_args(args)
    result = smoke(cfg, args) if args.command == "smoke" else lookup(cfg, args, args.query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("verdict", "PASS") == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
