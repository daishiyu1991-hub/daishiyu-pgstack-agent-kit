#!/usr/bin/env python3
"""Validate a Product Strategy Template OS run folder.

This is intentionally dependency-light. It checks the invariants that keep the
pipeline stable without requiring jsonschema to be installed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_STATE_CHECKS = [
    "read_global_rules",
    "read_skill_runtime",
    "read_run_architecture",
    "read_previous_chapter_decision",
    "run_previous_artifact_review",
    "run_evidence_router",
    "collect_available_evidence",
    "write_analysis_package",
    "run_evidence_review",
    "run_red_team",
    "render_complete_report",
    "stop_for_human_decision",
    "write_decision_record",
    "update_index",
    "queue_or_sync_gbrain",
]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_path(root: Path, rel: str, errors: list[str]) -> None:
    if not (root / rel).exists():
        fail(errors, f"missing path: {rel}")


def validate_run(root: Path) -> list[str]:
    errors: list[str] = []
    check_path(root, "quality-review-index.html", errors)
    state_path = root / "process" / "pipeline-run-state-v1.json"
    check_path(root, "process/pipeline-run-state-v1.json", errors)
    if not state_path.exists():
        return errors

    state = load_json(state_path)
    if state.get("artifact") != "pipeline_run_state_v1":
        fail(errors, "pipeline-run-state-v1.json artifact must be pipeline_run_state_v1")
    chapters = state.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        fail(errors, "pipeline run state must contain non-empty chapters")
        return errors

    for chapter in chapters:
        chapter_name = chapter.get("chapter", "unknown")
        status = chapter.get("status", "")
        is_legacy_completed = status == "completed_before_latest_pipeline"
        checkpoints = chapter.get("checkpoints", {})
        if status.startswith("completed") or status in {"paused_by_human_decision", "execution_plan_rendered_awaiting_human_go"}:
            if not isinstance(checkpoints, dict):
                fail(errors, f"{chapter_name}: checkpoints must be object")
            for ref in chapter.get("process_refs", []):
                check_path(root, ref, errors)
            if chapter.get("primary_plan"):
                check_path(root, chapter["primary_plan"], errors)
            if chapter.get("primary_report"):
                check_path(root, chapter["primary_report"], errors)
            if chapter.get("decision_record"):
                check_path(root, chapter["decision_record"], errors)
        if status.startswith("completed") and not is_legacy_completed:
            if checkpoints.get("stop_for_human_decision") != "completed":
                fail(errors, f"{chapter_name}: completed chapter must have completed human decision stop")
            if checkpoints.get("write_decision_record") != "completed":
                fail(errors, f"{chapter_name}: completed chapter must have decision record")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    args = parser.parse_args()
    root = Path(args.run_dir).expanduser().resolve()
    errors = validate_run(root)
    if errors:
        for error in errors:
            print(f"VALIDATION_ERROR\t{error}")
        raise SystemExit(1)
    print("OK_VALIDATE_RUN")


if __name__ == "__main__":
    main()
