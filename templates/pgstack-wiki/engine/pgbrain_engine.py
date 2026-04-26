#!/usr/bin/env python3
"""PGBrain Engine v1.

A deterministic local engine for the PGStack shared kernel.

The engine intentionally remains filesystem-backed. It indexes Markdown,
checks core structure, validates job specs, extracts typed edges, validates
wikilinks, and runs a local doctor command. Heavier graph/vector/database
infrastructure should be added only after this interface proves too weak for
real operations.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = ROOT.parents[1]
STATE_DIR = ROOT / "engine" / "state"
INDEX_PATH = STATE_DIR / "pgbrain-index.json"
INDEX_DIRS = ("brain", "wiki", "skills", "jobs", "adapters", "engine")
HERMES_JOBS_PATH = Path(
    os.environ.get("PGSTACK_HERMES_JOBS_PATH", Path.home() / ".hermes" / "cron" / "jobs.json")
).expanduser()
SKILL_MANIFEST_PATH = ROOT / "skills" / "manifest.json"

REQUIRED_KERNEL_PATHS = (
    "AGENTS.md",
    "brain/RESOLVER.md",
    "brain/schema.md",
    "brain/index.md",
    "brain/log.md",
    "skills/RESOLVER.md",
    "skills/README.md",
    "skills/manifest.json",
    "skills/signal-detector/SKILL.md",
    "skills/brain-ops/SKILL.md",
    "engine/README.md",
    "engine/pgbrain_engine.py",
    "engine/skillpack_check.py",
    "jobs/RESOLVER.md",
    "adapters/README.md",
)

CORE_TWO_LAYER_PAGES = (
    "brain/skills/pgstack-pgbrain-shared-kernel-architecture.md",
    "brain/skills/gbrain-operating-logic-compatibility-matrix.md",
    "brain/skills/pgstack-gbrain-compatibility-layer.md",
    "brain/skills/pgbrain-engine-v1.md",
    "skills/RESOLVER.md",
)

REQUIRED_CANONICAL_SKILLS = (
    "signal-detector",
    "brain-ops",
    "personal-gstack",
    "llm-wiki",
    "ai-daily-brief",
    "query",
    "ingest",
    "enrich",
    "maintain",
    "repo-architecture",
    "minion-orchestrator",
    "source-discovery",
    "research-brief",
    "team-memory-writing",
    "team-memory-gate",
    "skillify",
    "testing",
)

REQUIRED_JOB_METADATA = (
    "title",
    "type",
    "updated",
    "status",
    "confidence",
    "scope",
    "job_id",
    "runtime_host",
    "source_of_truth",
)

REQUIRED_JOB_SECTIONS = (
    "## Compiled Truth",
    "## Job Contract",
    "## Trigger",
    "## Inputs",
    "## Outputs",
    "## Runtime Contract",
    "## State",
    "## Evidence",
    "## Failure Behavior",
    "## Persistence Rule",
    "## Verification",
    "## Timeline",
)

JOB_SECTION_PATH_HINTS = {
    "## State": ("state", "path", "/"),
    "## Evidence": ("evidence", "output", "source", "path", "/"),
    "## Inputs": ("input", "skill", "script", "source", "/"),
    "## Outputs": ("output", "note", "report", "digest", "path", "/"),
}

ALLOWED_RUNTIME_HOSTS = {
    "Codex",
    "Hermes",
    "Manual",
    "MultiCA",
    "AgentHost",
    "Future",
}

EDGE_TYPES = {
    "implements",
    "depends_on",
    "owned_by",
    "runs_on",
    "writes_to",
    "reads_from",
    "delivers_to",
    "validated_by",
    "promotes_to",
    "supersedes",
    "persists_to",
}

SOURCE_REQUIRED_TYPES = {
    "agent",
    "adapter",
    "job",
    "memory",
    "pipeline",
    "runbook",
    "skill",
}

SMOKE_QUERIES = (
    "AI Daily Brief Job",
    "Personal GStack Foundation v1 Plan",
)


@dataclass
class Doc:
    path: str
    title: str
    metadata: dict[str, object]
    headings: list[str]
    links: list[str]
    edges: list[dict[str, str]]
    text: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_markdown_files() -> Iterable[Path]:
    for dirname in INDEX_DIRS:
        base = ROOT / dirname
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
                continue
            yield path


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    raw = text[4:end].splitlines()
    body = text[end + 5 :]
    metadata: dict[str, object] = {}
    current_key: str | None = None

    for line in raw:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_key:
            metadata.setdefault(current_key, [])
            if isinstance(metadata[current_key], list):
                metadata[current_key].append(stripped[2:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value == "":
            metadata[key] = []
        else:
            metadata[key] = value.strip('"')

    return metadata, body


def first_heading(body: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else None


def section_body(text: str, heading: str) -> str:
    pattern = re.compile(rf"^{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_edges(body: str) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    edge_body = section_body(body, "## Typed Edges")
    if not edge_body:
        return edges

    for line in edge_body.splitlines():
        match = re.match(r"\s*-\s*([a-z_]+)\s*:\s*(.+?)\s*$", line)
        if not match:
            continue
        edges.append({"type": match.group(1), "target": match.group(2)})
    return edges


def parse_doc(path: Path) -> Doc:
    text = read_text(path)
    metadata, body = parse_frontmatter(text)
    rel = path.relative_to(ROOT).as_posix()
    headings = [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.+)$", body, re.MULTILINE)]
    links = sorted(set(m.group(1).strip() for m in re.finditer(r"\[\[([^\]]+)\]\]", body)))
    title = str(metadata.get("title") or first_heading(body) or path.stem)
    edges = extract_edges(body)
    return Doc(path=rel, title=title, metadata=metadata, headings=headings, links=links, edges=edges, text=body)


def build_index() -> dict[str, object]:
    docs = [parse_doc(path) for path in iter_markdown_files()]
    generated_at = datetime.now(timezone.utc).isoformat()
    return {
        "engine": "pgbrain-engine-v1",
        "root": ROOT.as_posix(),
        "generated_at": generated_at,
        "doc_count": len(docs),
        "edge_count": sum(len(doc.edges) for doc in docs),
        "docs": [
            {
                "path": doc.path,
                "title": doc.title,
                "type": doc.metadata.get("type"),
                "status": doc.metadata.get("status"),
                "confidence": doc.metadata.get("confidence"),
                "scope": doc.metadata.get("scope"),
                "updated": doc.metadata.get("updated"),
                "headings": doc.headings[:24],
                "links": doc.links,
                "edges": doc.edges,
                "excerpt": compact(doc.text, 420),
            }
            for doc in docs
        ],
    }


def compact(text: str, limit: int) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    return normalized[:limit].rstrip()


def write_index() -> dict[str, object]:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    index = build_index()
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index


def load_or_build_index() -> dict[str, object]:
    if INDEX_PATH.exists():
        return json.loads(read_text(INDEX_PATH))
    return write_index()


def score_doc(doc: dict[str, object], terms: list[str]) -> int:
    haystack = " ".join(
        [
            str(doc.get("path", "")),
            str(doc.get("title", "")),
            " ".join(str(x) for x in doc.get("headings", []) or []),
            str(doc.get("excerpt", "")),
        ]
    ).lower()
    score = 0
    for term in terms:
        if term in str(doc.get("title", "")).lower():
            score += 8
        if term in str(doc.get("path", "")).lower():
            score += 5
        score += haystack.count(term)
    return score


def query_index(query: str, limit: int) -> list[tuple[int, dict[str, object]]]:
    terms = [term.lower() for term in re.findall(r"[\w\-]+", query) if len(term) > 1]
    if not terms:
        return []
    index = load_or_build_index()
    scored = [(score_doc(doc, terms), doc) for doc in index.get("docs", [])]
    return [(score, doc) for score, doc in sorted(scored, key=lambda item: (-item[0], item[1]["path"])) if score > 0][:limit]


def markdown_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for path in iter_markdown_files():
        rel = path.relative_to(ROOT).as_posix()
        doc = parse_doc(path)
        keys = {
            rel,
            rel[:-3] if rel.endswith(".md") else rel,
            path.name,
            path.stem,
            doc.title,
        }
        for key in keys:
            lookup[normalize_link_key(key)] = rel
    return lookup


def normalize_link_key(value: str) -> str:
    return value.strip().replace("\\", "/").strip("/").lower()


def clean_wikilink_target(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    return target


def resolve_wikilink(doc_path: str, raw: str, lookup: dict[str, str]) -> str | None:
    target = clean_wikilink_target(raw)
    if not target:
        return "anchor-only"
    if re.match(r"^[a-z]+://", target):
        return "external"
    if target.startswith("/"):
        path = Path(target)
        if path.exists():
            return path.as_posix()
        return None

    doc_dir = (ROOT / doc_path).parent
    candidates: list[str] = []

    if target.startswith(".") or "/" in target:
        rel_path = (doc_dir / target).resolve()
        for existing in (rel_path, rel_path.with_suffix(".md")):
            if existing.exists():
                try:
                    return existing.relative_to(ROOT).as_posix()
                except ValueError:
                    return existing.as_posix()
        try:
            rel = rel_path.relative_to(ROOT).as_posix()
        except ValueError:
            rel = ""
        if rel:
            candidates.append(rel)
            if not rel.endswith(".md"):
                candidates.append(f"{rel}.md")

        vault_path = VAULT_ROOT / target
        if vault_path.exists() or vault_path.with_suffix(".md").exists():
            return vault_path.as_posix()

    candidates.extend(
        [
            target,
            f"{target}.md",
            f"wiki/{target}",
            f"wiki/{target}.md",
            f"brain/{target}",
            f"brain/{target}.md",
        ]
    )

    for candidate in candidates:
        hit = lookup.get(normalize_link_key(candidate))
        if hit:
            return hit
    return None


def load_hermes_jobs() -> dict[str, dict[str, object]]:
    if not HERMES_JOBS_PATH.exists():
        return {}
    try:
        data = json.loads(read_text(HERMES_JOBS_PATH))
    except json.JSONDecodeError:
        return {}
    jobs = data.get("jobs", data if isinstance(data, list) else [])
    return {str(job.get("id")): job for job in jobs if isinstance(job, dict) and job.get("id")}


def validate_skillpack() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not SKILL_MANIFEST_PATH.exists():
        return [f"missing skill manifest: {SKILL_MANIFEST_PATH.relative_to(ROOT).as_posix()}"], warnings

    try:
        manifest = json.loads(read_text(SKILL_MANIFEST_PATH))
    except json.JSONDecodeError as exc:
        return [f"invalid skill manifest JSON: {exc}"], warnings

    resolver = str(manifest.get("resolver", "")).strip()
    resolver_text = ""
    if resolver and not (ROOT / resolver).exists():
        errors.append(f"skill manifest resolver path missing: {resolver}")
    elif resolver:
        resolver_text = read_text(ROOT / resolver)

    skills = manifest.get("skills")
    if not isinstance(skills, list):
        return ["skill manifest skills must be a list"], warnings

    manifest_names: set[str] = set()
    manifest_paths: set[str] = set()

    for item in skills:
        if not isinstance(item, dict):
            errors.append("skill manifest contains a non-object skill entry")
            continue

        name = str(item.get("name", "")).strip()
        path = str(item.get("path", "")).strip()
        if not name:
            errors.append("skill manifest entry missing name")
        if not path:
            errors.append(f"skill manifest entry missing path: {name or '<unnamed>'}")
            continue

        if name in manifest_names:
            errors.append(f"duplicate skill name in manifest: {name}")
        if path in manifest_paths:
            errors.append(f"duplicate skill path in manifest: {path}")
        manifest_names.add(name)
        manifest_paths.add(path)
        full_path = ROOT / path
        if not full_path.exists():
            errors.append(f"skill manifest path missing: {path}")
            continue

        metadata, body = parse_frontmatter(read_text(full_path))
        skill_name = str(metadata.get("name", "")).strip()
        if not skill_name:
            errors.append(f"skill missing frontmatter name: {path}")
        elif name and skill_name != name:
            errors.append(f"skill name mismatch manifest={name} frontmatter={skill_name}: {path}")

        if metadata.get("type") != "skill":
            warnings.append(f"skill frontmatter type is not skill: {path}")
        if "description" not in metadata:
            warnings.append(f"skill missing description: {path}")
        if "## Contract" not in body and "## Protocol" not in body:
            warnings.append(f"skill may lack explicit Contract/Protocol section: {path}")

    for required in REQUIRED_CANONICAL_SKILLS:
        if required not in manifest_names:
            errors.append(f"required canonical skill missing from manifest: {required}")
        expected_path = f"skills/{required}/SKILL.md"
        if expected_path not in manifest_paths:
            errors.append(f"required canonical skill path missing from manifest: {expected_path}")
        elif not (ROOT / expected_path).exists():
            errors.append(f"required canonical skill file missing: {expected_path}")
        if resolver_text and expected_path not in resolver_text:
            errors.append(f"resolver does not route canonical skill path: {expected_path}")

    declared_required = manifest.get("required", [])
    if not isinstance(declared_required, list):
        errors.append("skill manifest required must be a list")
    else:
        missing_declared = sorted(set(REQUIRED_CANONICAL_SKILLS) - {str(item) for item in declared_required})
        for name in missing_declared:
            warnings.append(f"skill manifest required list omits canonical skill: {name}")

    return errors, warnings


def validate() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    lookup = markdown_lookup()
    hermes_jobs = load_hermes_jobs()

    for rel in REQUIRED_KERNEL_PATHS:
        if not (ROOT / rel).exists():
            errors.append(f"missing required kernel path: {rel}")

    skill_errors, skill_warnings = validate_skillpack()
    errors.extend(skill_errors)
    warnings.extend(skill_warnings)

    for rel in CORE_TWO_LAYER_PAGES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing core two-layer page: {rel}")
            continue
        text = read_text(path)
        if "## Compiled Truth" not in text:
            errors.append(f"missing Compiled Truth section: {rel}")
        if "## Timeline" not in text:
            errors.append(f"missing Timeline section: {rel}")

    for path in (ROOT / "brain").rglob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        metadata, _ = parse_frontmatter(read_text(path))
        if path.name == "README.md":
            continue
        for field in ("title", "type", "updated", "status", "confidence"):
            if field not in metadata:
                warnings.append(f"brain page missing {field}: {rel}")

    for path in iter_markdown_files():
        doc = parse_doc(path)
        for link in doc.links:
            resolved = resolve_wikilink(doc.path, link, lookup)
            if resolved is None:
                warnings.append(f"unresolved wikilink in {doc.path}: [[{link}]]")
        for edge in doc.edges:
            edge_type = edge.get("type", "")
            if edge_type not in EDGE_TYPES:
                errors.append(f"unknown typed edge {edge_type}: {doc.path}")
            if not edge.get("target", "").strip():
                errors.append(f"empty typed edge target: {doc.path}")

    for path in (ROOT / "jobs").glob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path)
        metadata, _ = parse_frontmatter(text)
        if metadata.get("type") != "job":
            continue
        for field in REQUIRED_JOB_METADATA:
            if field not in metadata:
                errors.append(f"job spec missing {field}: {rel}")
        for section in REQUIRED_JOB_SECTIONS:
            if section not in text:
                errors.append(f"job spec missing section {section}: {rel}")
        runtime_host = str(metadata.get("runtime_host", "")).strip()
        if runtime_host and runtime_host not in ALLOWED_RUNTIME_HOSTS:
            errors.append(f"job spec has unknown runtime_host {runtime_host}: {rel}")
        source_of_truth = metadata.get("source_of_truth")
        if not isinstance(source_of_truth, list) or not source_of_truth:
            errors.append(f"job spec source_of_truth must be a non-empty list: {rel}")
        for heading, hints in JOB_SECTION_PATH_HINTS.items():
            body = section_body(text, heading)
            if body and not any(hint in body.lower() for hint in hints):
                warnings.append(f"job spec section may lack concrete pointer {heading}: {rel}")
        if runtime_host == "Hermes" and metadata.get("runtime_job_id"):
            runtime_job_id = str(metadata.get("runtime_job_id"))
            if HERMES_JOBS_PATH.exists() and runtime_job_id not in hermes_jobs:
                errors.append(f"Hermes job id not found in jobs.json: {runtime_job_id} ({rel})")
            elif runtime_job_id in hermes_jobs:
                job = hermes_jobs[runtime_job_id]
                schedule = str(metadata.get("schedule", "")).strip()
                actual_schedule = str(job.get("schedule_display") or "").strip()
                if schedule and actual_schedule and schedule != actual_schedule:
                    warnings.append(
                        f"Hermes schedule mismatch for {rel}: spec={schedule} actual={actual_schedule}"
                    )

    for path in iter_markdown_files():
        doc = parse_doc(path)
        doc_type = str(doc.metadata.get("type", ""))
        if doc_type in SOURCE_REQUIRED_TYPES and path.name != "README.md":
            source_of_truth = doc.metadata.get("source_of_truth")
            if not isinstance(source_of_truth, list) or not source_of_truth:
                warnings.append(f"{doc_type} page missing source_of_truth: {doc.path}")

    return errors, warnings


def print_status() -> int:
    print(f"root: {ROOT}")
    print(f"index: {INDEX_PATH}")
    print("kernel paths:")
    for rel in REQUIRED_KERNEL_PATHS:
        marker = "ok" if (ROOT / rel).exists() else "missing"
        print(f"  {marker:7} {rel}")
    return 0


def print_query(query: str, limit: int) -> int:
    results = query_index(query, limit)
    for score, doc in results:
        print(f"{score:3} {doc['path']} | {doc['title']}")
    return 0 if results else 1


def print_related(query: str, limit: int) -> int:
    results = query_index(query, 1)
    if not results:
        print(f"no match for: {query}")
        return 1
    _, doc = results[0]
    print(f"{doc['path']} | {doc['title']}")
    edges = doc.get("edges", []) or []
    if not edges:
        print("no typed edges")
        return 0
    for edge in edges[:limit]:
        print(f"  {edge['type']}: {edge['target']}")
    return 0


def central_brain_maintenance_smoke(require_config: bool) -> dict[str, object]:
    cmd = [
        sys.executable,
        str(ROOT / "engine" / "central_brain_health.py"),
        "--json",
    ]
    if require_config:
        cmd.append("--require-config")
    try:
        completed = subprocess.run(
            cmd,
            check=False,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=70,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "verdict": "FAIL",
            "error": f"timed out after {exc.timeout}s",
        }

    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        result = {
            "verdict": "FAIL",
            "error": "central_brain_health.py returned non-JSON output",
            "stdout_preview": completed.stdout[-500:],
        }
    if completed.stderr.strip():
        result["stderr_preview"] = completed.stderr.strip()[-500:]
    result["returncode"] = completed.returncode
    return result


def print_maintenance(limit: int, central_brain_smoke: bool, require_central_brain: bool) -> int:
    docs = [parse_doc(path) for path in iter_markdown_files()]
    lookup = markdown_lookup()
    inbound: dict[str, int] = {doc.path: 0 for doc in docs}

    for doc in docs:
        for link in doc.links:
            resolved = resolve_wikilink(doc.path, link, lookup)
            if resolved in inbound:
                inbound[resolved] += 1

    orphan_candidates = [
        doc
        for doc in docs
        if inbound.get(doc.path, 0) == 0
        and doc.path not in {"wiki/index.md", "wiki/log.md", "brain/index.md", "brain/log.md"}
        and not doc.path.endswith("/README.md")
        and not doc.path.startswith("raw/")
    ]
    open_thread_docs = [doc for doc in docs if "## Current Open Threads" in doc.text]
    job_docs = [doc for doc in docs if doc.metadata.get("type") == "job"]
    edge_count = sum(len(doc.edges) for doc in docs)

    print("PGBrain maintenance report")
    print("--------------------------")
    print(f"docs: {len(docs)}")
    print(f"jobs: {len(job_docs)}")
    print(f"typed_edges: {edge_count}")
    print(f"open_thread_pages: {len(open_thread_docs)}")
    print(f"orphan_candidates: {len(orphan_candidates)}")

    if orphan_candidates:
        print("orphan candidates:")
        for doc in orphan_candidates[:limit]:
            print(f"  {doc.path} | {doc.title}")
        if len(orphan_candidates) > limit:
            print(f"  ... {len(orphan_candidates) - limit} more")

    if open_thread_docs:
        print("open-thread pages:")
        for doc in open_thread_docs[:limit]:
            print(f"  {doc.path} | {doc.title}")
        if len(open_thread_docs) > limit:
            print(f"  ... {len(open_thread_docs) - limit} more")

    if central_brain_smoke:
        smoke = central_brain_maintenance_smoke(require_central_brain)
        print("central-brain smoke:")
        print(f"  verdict: {smoke.get('verdict')}")
        route = smoke.get("memory_owner_route")
        if isinstance(route, dict):
            print(
                "  memory_owner_route: "
                f"{route.get('requested')} -> {route.get('resolved')} "
                f"(alias_applied={route.get('alias_applied')})"
            )
        checks = smoke.get("checks")
        if isinstance(checks, list):
            for check in checks:
                if isinstance(check, dict):
                    status = "SKIP" if check.get("skipped") else ("PASS" if check.get("passed") else "FAIL")
                    print(f"  {check.get('name')}: {status} (evidence_count={check.get('evidence_count')})")
        if smoke.get("missing"):
            for item in smoke.get("missing", []):
                print(f"  missing: {item}")
        if smoke.get("error"):
            print(f"  error: {smoke.get('error')}")
        if smoke.get("verdict") == "FAIL":
            return 2
        if smoke.get("verdict") == "SKIP" and require_central_brain:
            return 2

    return 0


def print_validate() -> int:
    errors, warnings = validate()
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")
    if errors:
        print(f"validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 2
    print(f"validation passed: 0 error(s), {len(warnings)} warning(s)")
    return 0


def print_doctor() -> int:
    print("PGBrain Engine doctor")
    print("---------------------")
    print_status()
    index = write_index()
    print(f"indexed: {index['doc_count']} docs, {index['edge_count']} typed edges")

    smoke_failures = 0
    for query in SMOKE_QUERIES:
        results = query_index(query, 3)
        if not results:
            smoke_failures += 1
            print(f"smoke query failed: {query}")
            continue
        _, doc = results[0]
        print(f"smoke query ok: {query} -> {doc['path']}")

    errors, warnings = validate()
    if errors:
        for error in errors:
            print(f"error: {error}")
    if warnings:
        print(f"warnings: {len(warnings)}")
        for warning in warnings[:20]:
            print(f"warning: {warning}")
        if len(warnings) > 20:
            print(f"warning: ... {len(warnings) - 20} more")

    if errors or smoke_failures:
        print(f"doctor failed: {len(errors)} error(s), {smoke_failures} smoke failure(s)")
        return 2
    print(f"doctor passed: 0 error(s), {len(warnings)} warning(s)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PGBrain Engine v1")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show shared-kernel status")
    subparsers.add_parser("index", help="Build the local Markdown index")
    subparsers.add_parser("validate", help="Validate shared-kernel structure")
    subparsers.add_parser("doctor", help="Run status, index, smoke queries, and validation")

    maintenance_parser = subparsers.add_parser("maintenance", help="Print a local maintenance report")
    maintenance_parser.add_argument("--limit", type=int, default=20)
    maintenance_parser.add_argument(
        "--central-brain-smoke",
        action="store_true",
        help="Include the optional cloud Central Brain maintenance smoke.",
    )
    maintenance_parser.add_argument(
        "--require-central-brain",
        action="store_true",
        help="Fail maintenance if the central brain smoke is skipped or fails.",
    )

    query_parser = subparsers.add_parser("query", help="Search the local index")
    query_parser.add_argument("query")
    query_parser.add_argument("--limit", type=int, default=10)

    related_parser = subparsers.add_parser("related", help="Show typed edges for the best matching page")
    related_parser.add_argument("query")
    related_parser.add_argument("--limit", type=int, default=20)

    args = parser.parse_args(argv)

    if args.command == "status":
        return print_status()

    if args.command == "index":
        index = write_index()
        print(f"indexed {index['doc_count']} docs, {index['edge_count']} edges -> {INDEX_PATH}")
        return 0

    if args.command == "query":
        return print_query(args.query, args.limit)

    if args.command == "related":
        return print_related(args.query, args.limit)

    if args.command == "maintenance":
        return print_maintenance(args.limit, args.central_brain_smoke, args.require_central_brain)

    if args.command == "validate":
        return print_validate()

    if args.command == "doctor":
        return print_doctor()

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
