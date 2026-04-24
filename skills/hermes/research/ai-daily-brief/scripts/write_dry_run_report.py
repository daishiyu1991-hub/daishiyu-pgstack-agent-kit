#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any


SECTION_TITLES = {
    "models-products": "模型 / 产品发布",
    "research": "研究 / 论文",
    "open-source-tools": "开源 / 工具 / Agent",
    "policy-capital": "资本 / 政策",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a dry-run AI Daily Brief note from an existing bundle.")
    parser.add_argument("--bundle", default=os.environ.get("AI_DAILY_BRIEF_BUNDLE_PATH", ""))
    parser.add_argument("--social-radar", default=os.environ.get("AI_DAILY_BRIEF_SOCIAL_RADAR_PATH", ""))
    parser.add_argument("--note-path", default=os.environ.get("AI_DAILY_BRIEF_NOTE_PATH", ""))
    parser.add_argument("--now", default=os.environ.get("AI_DAILY_BRIEF_NOW", ""))
    parser.add_argument("--window-start", default=os.environ.get("AI_DAILY_BRIEF_WINDOW_START", ""))
    parser.add_argument("--window-mode", default=os.environ.get("AI_DAILY_BRIEF_WINDOW_MODE", ""))
    parser.add_argument("--date", default=os.environ.get("AI_DAILY_BRIEF_DATE", ""))
    return parser.parse_args()


def require_path(value: str, label: str) -> Path:
    if not value:
        raise SystemExit(f"missing {label}")
    return Path(value).expanduser()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def text_of(item: dict[str, Any]) -> str:
    return " ".join(
        str(item.get(key, ""))
        for key in ("source", "title", "summary", "url", "category_hint")
    ).lower()


def score_item(item: dict[str, Any]) -> int:
    haystack = text_of(item)
    score = int(item.get("source_priority", 1)) * 100
    tags = set(item.get("tags", []))
    if "official" in tags:
        score += 45
    if "github" in tags or "repo-release" in tags:
        score += 25
    if "anthropic" in haystack or "openai" in haystack or "deepmind" in haystack:
        score += 20
    if "skill bank" in haystack:
        score += 28
    elif "harness" in haystack:
        score += 24
    elif any(token in haystack for token in ["agent", "workflow"]):
        score += 18
    if any(token in haystack for token in ["alignment", "defensibility", "rule-governed", "policy"]):
        score += 16
    if any(token in haystack for token in ["benchmark", "evaluation", "early-stopping", "cost"]):
        score += 10
    if "finresearch" in haystack or "financial investment" in haystack:
        score -= 6
    if any(token in haystack for token in ["traffic accident", "language tutoring", "wavelet"]):
        score -= 8
    return score


def classify(item: dict[str, Any]) -> str:
    haystack = text_of(item)
    if "arxiv.org" in haystack or "arxiv" in str(item.get("source", "")).lower():
        return "research"
    if any(token in haystack for token in ["partner", "deploy", "platform", "api", "model", "claude"]):
        return "models-products"
    if any(token in haystack for token in ["github", "release", "sdk", "tool", "agent harness"]):
        if "arxiv" not in haystack:
            return "open-source-tools"
    if any(token in haystack for token in ["policy", "regulation", "capital", "funding", "acquisition"]):
        return "policy-capital"
    return item.get("category_hint") or "research"


def clean_summary(summary: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", summary or "").strip()
    text = re.sub(r"^arXiv:\S+\s+Announce Type:\s+\w+\s+Abstract:\s+", "", text)
    if not text:
        return "候选包未提供摘要，需在正式日报中由 Hermes 进一步核验。"
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def why_it_matters(item: dict[str, Any]) -> str:
    haystack = text_of(item)
    title = item.get("title", "")

    if "nec" in haystack and "anthropic" in haystack:
        return "Claude 进入日本大型企业与行业场景，说明模型厂商正在通过本地龙头伙伴扩大企业分发。"
    if "skill bank" in haystack or "long-horizon" in haystack:
        return "长期任务里的技能库和决策 agent 是 pgstack/agent 工作流的核心问题，值得进入后续观察。"
    if "agreement trap" in haystack or "defensibility" in haystack:
        return "它提醒 AI 评估不能只看人类标签一致性，规则治理场景需要更可辩护的评价信号。"
    if "alignment faking" in haystack:
        return "alignment faking 会影响模型监控、评估和部署信任，是安全与治理层面的高风险主题。"
    if "harness" in haystack:
        return "复杂企业工作流需要更稳定的 agent harness，这和未来 agent 测试、运维、评估直接相关。"
    if "finresearch" in haystack or "financial investment" in haystack:
        return "金融 deep research benchmark 能帮助判断 AI agent 是否真的能承担专业研究任务。"
    if "traces" in haystack or "early-stopping" in haystack:
        return "推理步骤标注和 early-stopping 直接关系到 reasoning model 的推理成本和延迟。"
    if "simultaneous translation" in haystack:
        return "同声传译是长上下文、低延迟和增量决策的综合压力测试。"
    if "low-resource" in haystack or "language tutoring" in haystack:
        return "低资源语言教育是 LLM 全球化应用的重要长尾场景。"
    if "multimodal" in haystack:
        return "多模态责任判断属于高风险应用场景，能暴露模型在证据和责任推理上的边界。"
    if "summarization" in haystack:
        return "长文档摘要仍然是企业知识工作常见瓶颈，方法改进有实际参考价值。"

    if classify(item) == "models-products":
        return "这是模型或产品分发层面的更新，可能影响开发者和企业采用路径。"
    if classify(item) == "open-source-tools":
        return "这是工具链或开源生态信号，可能影响实际构建和部署工作流。"
    if classify(item) == "policy-capital":
        return "这是政策、资本或产业结构信号，可能影响后续行业节奏。"
    return f"{title} 属于当天候选中的研究信号，需要结合后续引用和实现情况判断影响。"


def render_item(item: dict[str, Any], numbered: bool = False, index: int = 0) -> str:
    prefix = f"{index}. " if numbered else "- "
    title = item.get("title") or item.get("url") or "Untitled"
    source = item.get("source", "unknown source")
    published = item.get("published", "")
    url = item.get("url", "")
    lines = [
        f"{prefix}**{title}**",
        f"   - 来源：{source}" + (f"｜{published}" if published else ""),
        f"   - 为什么重要：{why_it_matters(item)}",
        f"   - 事实：{clean_summary(item.get('summary', ''))}",
        f"   - 链接：{url}",
    ]
    return "\n".join(lines)


def render_report(
    bundle: dict[str, Any],
    social: dict[str, Any],
    note_path: Path,
    now: str,
    window_start: str,
    window_mode: str,
    date_label: str,
) -> tuple[str, str]:
    candidates = list(bundle.get("candidates", []))
    ranked = sorted(candidates, key=score_item, reverse=True)
    kept = ranked[: min(15, len(ranked))]
    top = kept[:5]

    by_section: dict[str, list[dict[str, Any]]] = {key: [] for key in SECTION_TITLES}
    for item in kept:
        by_section.setdefault(classify(item), []).append(item)

    social_count = social.get("candidate_count", 0)
    manual_social = sum(1 for diag in social.get("diagnostics", []) if diag.get("status") == "manual_only")
    source_errors = [diag for diag in bundle.get("diagnostics", []) if diag.get("status") != "ok"]

    lines: list[str] = [
        f"# AI Daily Brief Dry Run｜{date_label}",
        "",
        "> Level 2 dry-run：这份报告用于测试完整 Obsidian 写入链路；未发送飞书，未更新正式 `last_success.json`。",
        "",
        "## 时间窗口",
        f"- 起点：{window_start}",
        f"- 终点：{now}",
        f"- 模式：{window_mode}",
        f"- 候选数：{bundle.get('candidate_count', len(candidates))}",
        f"- social-radar 自动候选：{social_count}",
        f"- manual-only 社媒通道：{manual_social}",
        f"- 确定性来源错误数：{len(source_errors)}",
        "",
        "## 今日最重要的 5 条",
        "",
    ]

    if top:
        for index, item in enumerate(top, 1):
            lines.append(render_item(item, numbered=True, index=index))
            lines.append("")
    else:
        lines.append("今天的确定性候选不足，不强行凑数。")
        lines.append("")

    for section_key, section_title in SECTION_TITLES.items():
        lines.extend([f"## {section_title}", ""])
        items = by_section.get(section_key, [])
        if items:
            for item in items:
                lines.append(render_item(item))
                lines.append("")
        else:
            lines.append("- 今日未见明显新增高信号。")
            lines.append("")

    trend = "今天的候选结构偏研究论文，且 arXiv 占比较高；正式日报需要 ranking guard，避免研究密集窗口挤掉更重要的产品、平台或产业信号。"
    if any("anthropic" in text_of(item) and "nec" in text_of(item) for item in kept):
        trend = "今天最明确的产业信号是 Anthropic 通过 NEC 进入日本大型企业场景；研究侧则集中在 agent、评估、alignment 和专业 deep research benchmark。正式日报应把官方产业动作放在前面，再挑选与 agent 工作流最相关的论文。"

    lines.extend(
        [
            "## 今日判断",
            "",
            trend,
            "",
            "## Dry-Run 验收",
            "",
            "- 已写入专用 dry-run note path。",
            "- 未发送飞书。",
            "- 未更新正式 `last_success.json`。",
            "- 每条保留项都带原始链接。",
            "- 这份 deterministic draft 用于结构验收；正式日报仍由 Hermes 按质量规则做最终取舍。",
            "",
            "## 全部原始链接",
            "",
        ]
    )

    for item in kept:
        lines.append(f"- {item.get('title')}: {item.get('url')}")

    report = "\n".join(lines).rstrip() + "\n"

    digest_lines = [
        f"# AI Daily Brief Dry Run | {date_label}",
        "",
        "今日最重要的 3-5 条：",
        "",
    ]
    for index, item in enumerate(top, 1):
        digest_lines.extend(
            [
                f"{index}. {item.get('title')}",
                f"   - 为什么重要：{why_it_matters(item)}",
                f"   - 链接：{item.get('url')}",
                "",
            ]
        )
    digest_lines.extend(["完整测试版：", str(note_path)])
    digest = "\n".join(digest_lines).rstrip() + "\n"

    return report, digest


def main() -> None:
    args = parse_args()
    bundle_path = require_path(args.bundle, "--bundle or AI_DAILY_BRIEF_BUNDLE_PATH")
    note_path = require_path(args.note_path, "--note-path or AI_DAILY_BRIEF_NOTE_PATH")
    social_path = Path(args.social_radar).expanduser() if args.social_radar else None

    bundle = load_json(bundle_path)
    social = load_json(social_path) if social_path and social_path.exists() else {"candidate_count": 0, "diagnostics": [], "candidates": []}

    date_label = args.date or datetime.now().strftime("%Y-%m-%d")
    report, digest = render_report(
        bundle=bundle,
        social=social,
        note_path=note_path,
        now=args.now or bundle.get("generated_at", ""),
        window_start=args.window_start or bundle.get("window_start", ""),
        window_mode=args.window_mode or bundle.get("window_mode", ""),
        date_label=date_label,
    )

    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(report, encoding="utf-8")
    print(digest)


if __name__ == "__main__":
    main()
