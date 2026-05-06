#!/usr/bin/env python3
"""Validate a Product Strategy Template OS run folder.

This validator is intentionally dependency-light. It checks the invariants that
make the workflow reproducible across different agents:

- canonical chapter order;
- state/checkpoint consistency;
- source-backed numeric claims;
- raw/tag/effective review ledgers for review-derived counts;
- Chapter 6 USP pages separating review frequency from strategic USP weight.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CANONICAL_CHAPTERS = [
    "1. 品类本质小结",
    "2. 市场竞争分析",
    "3. 头部品牌竞争&竞品分析",
    "4. 用户场景&需求分析",
    "5. 营销分析&社媒传播",
    "6. 产品规划",
    "7. 供应链实现",
    "8. 项目计划",
]

LEGACY_CHAPTER_HINTS = [
    "6. 供应链管理",
    "7. 产品规划",
]

COMPLETED_STATUSES = {
    "approved",
    "completed",
    "completed_before_latest_pipeline",
}

ACTIVE_STATUSES = {
    "planned",
    "evidence_ready",
    "analysis_draft",
    "reviewed",
    "awaiting_human_decision",
    "execution_plan_rendered_awaiting_human_go",
    "paused_by_human_decision",
    "in_progress",
}

REVIEW_NUMERIC_PATTERNS = [
    re.compile(r"\d+\s*条(?:有效)?评论"),
    re.compile(r"\d+\s*条(?:正面|负面|中性)?(?:评论|评价)"),
    re.compile(r"\d+\s*reviews?", re.IGNORECASE),
    re.compile(r"\d+\s*(?:positive|negative|neutral)\s+reviews?", re.IGNORECASE),
    re.compile(r"~\s*\d+\s*次"),
    re.compile(r"\d+\+\s*(?:次|条|个)?(?:提及|负面|正面|痛点|场景|评论)"),
]

USP_PAGE_PATTERNS = [
    "quality-review-visible-value-thesis*.html",
    "quality-review-template-ch6-*.html",
]

REQUIRED_USP_MARKERS = [
    "评论提及频次",
    "USP 战略权重",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_path(root: Path, rel: str, errors: list[str]) -> None:
    if not (root / rel).exists():
        fail(errors, f"missing path: {rel}")


def chapter_number(chapter_name: str) -> int | None:
    match = re.match(r"\s*(\d+)\.", chapter_name)
    if not match:
        return None
    return int(match.group(1))


def file_exists_for_chapter(root: Path, chapter_no: int) -> bool:
    process = root / "process"
    candidates = list(root.glob(f"quality-review-template-ch{chapter_no}-*.html"))
    if process.exists():
        candidates.extend(process.glob(f"section{chapter_no}-*"))
    return any(path.exists() for path in candidates)


def check_canonical_chapter_order(state: dict[str, Any], errors: list[str]) -> None:
    chapter_order = state.get("chapter_order")
    if chapter_order != CANONICAL_CHAPTERS:
        fail(
            errors,
            "chapter_order must match canonical 8-chapter order: "
            + " | ".join(CANONICAL_CHAPTERS),
        )
        if isinstance(chapter_order, list) and any(item in chapter_order for item in LEGACY_CHAPTER_HINTS):
            fail(
                errors,
                "legacy chapter order detected: product planning must be chapter 6, "
                "supply chain implementation chapter 7, project plan chapter 8",
            )

    chapters = state.get("chapters")
    if isinstance(chapters, list):
        names = [chapter.get("chapter") for chapter in chapters]
        if names != CANONICAL_CHAPTERS:
            fail(errors, "chapters[].chapter must match canonical chapter order exactly")


def check_top_level_status(state: dict[str, Any], errors: list[str]) -> None:
    status = str(state.get("status", ""))
    if not status:
        return
    chapter_statuses = state.get("chapters", [])
    if not isinstance(chapter_statuses, list):
        return
    active_numbers = []
    for chapter in chapter_statuses:
        if not isinstance(chapter, dict):
            continue
        chapter_no = chapter_number(str(chapter.get("chapter", "")))
        if chapter_no is None:
            continue
        chapter_status = str(chapter.get("status", ""))
        if chapter_status in ACTIVE_STATUSES:
            active_numbers.append(chapter_no)
    match = re.search(r"ch(\d+)", status)
    if match and active_numbers:
        top_level_no = int(match.group(1))
        max_active = max(active_numbers)
        if top_level_no != max_active:
            fail(
                errors,
                f"top-level status {status!r} conflicts with active chapter {max_active}",
            )


def check_chapter_refs(root: Path, state: dict[str, Any], errors: list[str]) -> None:
    chapters = state.get("chapters")
    if not isinstance(chapters, list):
        fail(errors, "pipeline run state must contain chapters list")
        return

    seen_locked = False
    for chapter in chapters:
        if not isinstance(chapter, dict):
            fail(errors, "each chapter entry must be an object")
            continue

        chapter_name = str(chapter.get("chapter", "unknown"))
        chapter_no = chapter_number(chapter_name)
        status = str(chapter.get("status", ""))
        checkpoints = chapter.get("checkpoints", {})
        if not isinstance(checkpoints, dict):
            fail(errors, f"{chapter_name}: checkpoints must be object")
            checkpoints = {}

        for ref in chapter.get("process_refs", []):
            check_path(root, ref, errors)
        for key in ("primary_plan", "primary_report", "decision_record"):
            if chapter.get(key):
                check_path(root, str(chapter[key]), errors)

        if status == "locked":
            seen_locked = True
            if chapter_no is not None and file_exists_for_chapter(root, chapter_no):
                fail(errors, f"{chapter_name}: locked chapter has generated artifacts")
        elif seen_locked and status != "locked":
            fail(errors, f"{chapter_name}: chapter unlocked after a locked chapter")

        if status in COMPLETED_STATUSES and status != "completed_before_latest_pipeline":
            human_done = checkpoints.get("stop_for_human_decision") == "completed"
            decision_done = checkpoints.get("write_decision_record") == "completed"
            legacy_human_done = checkpoints.get("human_decision") in {"approved", "completed"}
            if not (human_done or legacy_human_done):
                fail(errors, f"{chapter_name}: completed/approved chapter must have human decision stop")
            if not (decision_done or chapter.get("decision_record") or legacy_human_done):
                fail(errors, f"{chapter_name}: completed/approved chapter must have decision record")


def collect_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in ("quality-review-*.html", "process/*.md", "process/*.json"):
        files.extend(root.glob(pattern))
    return sorted({path for path in files if path.is_file()})


def has_review_numeric_claim(root: Path) -> bool:
    for path in collect_text_files(root):
        text = read_text(path)
        if any(pattern.search(text) for pattern in REVIEW_NUMERIC_PATTERNS):
            return True
    return False


def json_contains_review_row(value: Any) -> bool:
    if isinstance(value, dict):
        keys = set(value.keys())
        if {"review_id", "content_text"} & keys:
            return True
        if {"review_text", "comment_text", "text", "rating", "asin"} & keys and (
            "review" in " ".join(keys).lower() or "rating" in keys
        ):
            return True
        return any(json_contains_review_row(child) for child in value.values())
    if isinstance(value, list):
        return any(json_contains_review_row(child) for child in value)
    return False


def find_review_ledgers(root: Path) -> list[Path]:
    process = root / "process"
    if not process.exists():
        return []
    ledgers = []
    for pattern in (
        "*review*raw*ledger*.json",
        "*review*tagged*ledger*.json",
        "*review*effective*ledger*.json",
        "*raw*review*.json",
        "*tagged*review*.json",
        "*review*ledger*.json",
    ):
        ledgers.extend(process.glob(pattern))
    return sorted({path for path in ledgers if path.is_file()})


def check_review_claim_reproducibility(root: Path, errors: list[str]) -> None:
    if not has_review_numeric_claim(root):
        return

    ledgers = find_review_ledgers(root)
    if not ledgers:
        fail(
            errors,
            "review-derived numeric claims require raw/tag/effective review ledger JSON in process/",
        )
        return

    has_recomputable_row = False
    for ledger in ledgers:
        try:
            data = load_json(ledger)
        except Exception:
            continue
        if json_contains_review_row(data):
            has_recomputable_row = True
            break

    if not has_recomputable_row:
        fail(
            errors,
            "review ledgers exist but do not expose recomputable review rows "
            "(review_id/content_text or equivalent fields)",
        )


def check_usp_weight_markers(root: Path, errors: list[str]) -> None:
    pages: list[Path] = []
    for pattern in USP_PAGE_PATTERNS:
        pages.extend(root.glob(pattern))
    pages = sorted({path for path in pages if path.is_file()}, key=version_sort_key)
    if not pages:
        return

    latest = pages[-1]
    text = read_text(latest)
    missing = [marker for marker in REQUIRED_USP_MARKERS if marker not in text]
    if missing:
        fail(
            errors,
            f"{latest.name}: Chapter 6/USP report must separate comment frequency "
            f"from USP strategic weight; missing markers: {', '.join(missing)}",
        )


def version_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"-v(\d+)", path.name)
    if match:
        return (int(match.group(1)), path.name)
    return (-1, path.name)


def check_source_raw_flags(root: Path, errors: list[str]) -> None:
    process = root / "process"
    if not process.exists():
        return
    ledgers = find_review_ledgers(root)
    for path in sorted(process.glob("*evidence*.json")):
        try:
            data = load_json(path)
        except Exception:
            continue
        file_reported = False
        for source in data.get("sources", []):
            if not isinstance(source, dict):
                continue
            source_ref = str(source.get("source_ref", ""))
            used_for = " ".join(str(item) for item in source.get("used_for", []))
            looks_review = bool(
                re.search(r"review|评论|评价|voc", source_ref + " " + used_for, re.IGNORECASE)
            )
            if looks_review and source.get("raw_available") == "yes" and not ledgers:
                fail(
                    errors,
                    f"{path.relative_to(root)} declares review raw_available=yes but no "
                    "review raw/tag/effective ledger is present in process/",
                )
                file_reported = True
            if file_reported:
                break


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

    check_canonical_chapter_order(state, errors)
    check_top_level_status(state, errors)
    check_chapter_refs(root, state, errors)
    check_review_claim_reproducibility(root, errors)
    check_source_raw_flags(root, errors)
    check_usp_weight_markers(root, errors)
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
