#!/usr/bin/env python3
from __future__ import annotations

import json
import argparse
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


TZ = ZoneInfo("Asia/Shanghai")
HOME = Path.home()
STATE_PATH = HOME / ".hermes" / "state" / "ai-daily-brief" / "last_success.json"
DRY_RUN_STATE_PATH = HOME / ".hermes" / "state" / "ai-daily-brief" / "dry_run_last_success.json"


def parse_iso(value: str) -> datetime | None:
    text = (value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    return dt.astimezone(TZ)


def load_last_success() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        loaded = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return loaded if isinstance(loaded, dict) else {}
    except Exception:
        return {}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit AI Daily Brief run context exports.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use dry-run note and state paths so production state and official notes are not touched.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dry_run = bool(args.dry_run)
    now = datetime.now(TZ)
    state = load_last_success()
    previous = parse_iso(str(state.get("last_success_end", "")))

    if previous and previous < now:
        window_start = previous
        window_mode = "since_last_success"
    else:
        window_start = now - timedelta(hours=24)
        window_mode = "fallback_24h"

    year = now.strftime("%Y")
    date_label = now.strftime("%Y-%m-%d")
    report_root = Path(
        os.environ.get(
            "PGSTACK_AI_DAILY_BRIEF_DIR",
            str(HOME / "Documents" / "PGStack" / "AI Daily Brief"),
        )
    ).expanduser()
    if dry_run:
        note_path = report_root / "Dry Runs" / year / f"{date_label} AI Daily Brief Dry Run.md"
        state_path = DRY_RUN_STATE_PATH
    else:
        note_path = report_root / year / f"{date_label} AI Daily Brief.md"
        state_path = STATE_PATH

    exports = {
        "AI_DAILY_BRIEF_NOW": now.isoformat(),
        "AI_DAILY_BRIEF_WINDOW_START": window_start.isoformat(),
        "AI_DAILY_BRIEF_WINDOW_MODE": window_mode,
        "AI_DAILY_BRIEF_DATE": date_label,
        "AI_DAILY_BRIEF_NOTE_PATH": str(note_path),
        "AI_DAILY_BRIEF_STATE_PATH": str(state_path),
        "AI_DAILY_BRIEF_DRY_RUN": "1" if dry_run else "0",
        "AI_DAILY_BRIEF_SEND_FEISHU": "0" if dry_run else "1",
        "AI_DAILY_BRIEF_UPDATE_PRODUCTION_STATE": "0" if dry_run else "1",
        "AI_DAILY_BRIEF_PRODUCTION_STATE_PATH": str(STATE_PATH),
    }

    print("AI Daily Brief run context:")
    print(f"- dry_run: {dry_run}")
    print(f"- now: {exports['AI_DAILY_BRIEF_NOW']}")
    print(f"- window_start: {exports['AI_DAILY_BRIEF_WINDOW_START']}")
    print(f"- window_mode: {exports['AI_DAILY_BRIEF_WINDOW_MODE']}")
    print(f"- note_path: {exports['AI_DAILY_BRIEF_NOTE_PATH']}")
    print(f"- state_path: {exports['AI_DAILY_BRIEF_STATE_PATH']}")
    print()
    print("Run this exact export block before writing files:")
    for key, value in exports.items():
        safe = value.replace("'", "'\"'\"'")
        print(f"export {key}='{safe}'")


if __name__ == "__main__":
    main()
