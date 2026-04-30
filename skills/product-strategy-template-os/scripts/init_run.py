#!/usr/bin/env python3
"""Create a Product Strategy Template OS run skeleton.

This script intentionally creates placeholders only. It does not invent
research evidence or conclusions.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


CHAPTERS = [
    "1. 品类本质小结",
    "2. 市场竞争分析",
    "3. 头部品牌竞争&竞品分析",
    "4. 用户场景&需求分析",
    "5. 营销分析&社媒传播",
    "6. 供应链管理",
    "7. 产品规划",
]


def slugify(text: str) -> str:
    return (
        text.strip()
        .lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("&", "and")
    )


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_index(path: Path, category: str, marketplace: str) -> None:
    rows = []
    for i, title in enumerate(CHAPTERS, start=1):
        rows.append(
            f"""
      <article class=\"chapter\">
        <b>{i:02d} · Locked</b>
        <h2>{title.split('. ', 1)[1]}</h2>
        <p>等待执行计划生成。</p>
      </article>"""
        )
    html = f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{category} · Product Strategy Template OS</title>
  <style>
    body{{margin:0;background:#f4f3ee;color:#20282d;font-family:-apple-system,BlinkMacSystemFont,\"PingFang SC\",sans-serif}}
    main{{max-width:1120px;margin:0 auto;padding:36px 24px 80px}}
    header,.chapter{{background:#fbfaf6;border:1px solid #d9dedc;border-radius:18px;padding:24px;margin:18px 0}}
    h1{{font-family:Georgia,\"Songti SC\",serif;font-size:42px;line-height:1.15;margin:0 0 12px}}
    p{{color:#647077;line-height:1.75}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}
    b{{color:#6f8392}}
  </style>
</head>
<body>
<main>
  <header>
    <b>Product Strategy Template OS</b>
    <h1>{category}</h1>
    <p>Marketplace: {marketplace}. This index is a roadmap only. It should not carry product verdicts.</p>
  </header>
  <section class=\"grid\">{''.join(rows)}
  </section>
</main>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", required=True, help="Category or keyword, e.g. wake up light")
    parser.add_argument("--marketplace", default="US", help="Target market/channel")
    parser.add_argument("--out", required=True, help="Output run directory")
    args = parser.parse_args()

    out = Path(args.out).expanduser().resolve()
    process = out / "process"
    process.mkdir(parents=True, exist_ok=True)

    create_index(out / "quality-review-index.html", args.category, args.marketplace)
    write_json(
        process / "pipeline-run-state-v1.json",
        {
            "artifact": "pipeline_run_state_v1",
            "created_at": str(date.today()),
            "category": args.category,
            "marketplace": args.marketplace,
            "status": "initialized",
            "chapter_order": CHAPTERS,
            "checklist_definition": [
                "read_skill_runtime",
                "read_template_structure",
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
            ],
            "chapters": [
                {
                    "chapter": chapter,
                    "status": "locked" if index > 1 else "ready_for_execution_plan",
                    "process_refs": [],
                    "checkpoints": {},
                }
                for index, chapter in enumerate(CHAPTERS, start=1)
            ],
        },
    )
    write_json(
        process / "index-structure-lock-v1.json",
        {
            "artifact": "index_structure_lock_v1",
            "created_at": str(date.today()),
            "rule": "Index is a roadmap. Do not redesign after accepted; only update chapter links and statuses.",
        },
    )
    print(f"Created run skeleton: {out}")


if __name__ == "__main__":
    main()
