#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import html
import socket
import argparse
import os
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
from xml.etree import ElementTree as ET


TZ = ZoneInfo("Asia/Shanghai")
HOME = Path.home()
STATE_DIR = HOME / ".hermes" / "state" / "ai-daily-brief"
STATE_PATH = STATE_DIR / "last_success.json"
BUNDLE_PATH = STATE_DIR / "latest_bundle.json"
SOCIAL_RADAR_PATH = STATE_DIR / "latest_social_radar.json"
DRY_RUN_STATE_PATH = STATE_DIR / "dry_run_last_success.json"
DRY_RUN_BUNDLE_PATH = STATE_DIR / "latest_dry_run_bundle.json"
DRY_RUN_SOCIAL_RADAR_PATH = STATE_DIR / "latest_dry_run_social_radar.json"
SOURCES_PATH = Path(__file__).with_name("sources.json")
SOCIAL_WATCHLIST_PATH = Path(__file__).with_name("social_watchlist.json")
USER_AGENT = "PGStack-AI-Daily-Brief/1.0 (+https://github.com/)"
PAGE_PREVIEW_BYTES = 64000


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
    parser = argparse.ArgumentParser(description="Build the AI Daily Brief source bundle.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use dry-run note/state/bundle paths so production state and the official note are not touched.",
    )
    return parser.parse_args()


def fetch_text(url: str, max_bytes: int | None = None, timeout: int = 15) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(req, timeout=timeout) as resp:
        if max_bytes is None:
            payload = resp.read()
        else:
            payload = resp.read(max_bytes)
        return payload.decode("utf-8", errors="replace")


def clean_text(text: str, limit: int = 280) -> str:
    no_tags = re.sub(r"<[^>]+>", " ", (text or ""))
    normalized = re.sub(r"\s+", " ", html.unescape(no_tags)).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"


def clean_title(text: str) -> str:
    cleaned = clean_text(text, limit=140)
    for separator in (" | ", " \\ ", " - ", " — "):
        if separator not in cleaned:
            continue
        left, right = cleaned.rsplit(separator, 1)
        if right and len(right) <= 28:
            cleaned = left.strip()
            break
    return cleaned


def slug_to_title(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1] if path else url
    slug = slug.replace("-", " ").replace("_", " ").strip()
    if not slug:
        return url
    parts = [part.upper() if part.isupper() else part.capitalize() for part in slug.split()]
    return " ".join(parts)


def infer_category(title: str, url: str, tags: list[str]) -> str:
    haystack = f"{title} {url} {' '.join(tags)}".lower()
    if any(token in haystack for token in ["paper", "research", "benchmark", "arxiv", "evaluation"]):
        return "research"
    if any(token in haystack for token in ["pricing", "policy", "license", "legal", "safety"]):
        return "policy-capital"
    if any(token in haystack for token in ["github", "open-source", "open source", "hugging face", "tool", "sdk"]):
        return "open-source-tools"
    return "models-products"


def extract_meta_description(html_text: str) -> str:
    patterns = [
        r'<meta[^>]+(?:name|property)=["\']description["\'][^>]+content=["\'](.*?)["\']',
        r'<meta[^>]+content=["\'](.*?)["\'][^>]+(?:name|property)=["\']description["\']',
        r'<meta[^>]+(?:name|property)=["\']og:description["\'][^>]+content=["\'](.*?)["\']',
        r'<meta[^>]+content=["\'](.*?)["\'][^>]+(?:name|property)=["\']og:description["\']',
        r'<meta[^>]+(?:name|property)=["\']twitter:description["\'][^>]+content=["\'](.*?)["\']',
        r'<meta[^>]+content=["\'](.*?)["\'][^>]+(?:name|property)=["\']twitter:description["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return clean_text(match.group(1))
    return ""


def extract_page_preview(url: str) -> dict[str, str]:
    try:
        html_text = fetch_text(url, max_bytes=PAGE_PREVIEW_BYTES, timeout=5)
    except (HTTPError, URLError, TimeoutError, socket.timeout, ValueError):
        return {}

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_text, flags=re.IGNORECASE | re.DOTALL)

    title = clean_title(title_match.group(1)) if title_match else ""
    h1 = clean_title(h1_match.group(1)) if h1_match else ""
    summary = extract_meta_description(html_text)

    preview: dict[str, str] = {}
    if title:
        preview["title"] = title
    elif h1:
        preview["title"] = h1
    if summary:
        preview["summary"] = summary
    elif h1:
        preview["summary"] = h1
    return preview


def parse_feed_datetime(raw: str | None) -> datetime | None:
    if not raw:
        return None
    raw = raw.strip()
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw).astimezone(TZ)
    except Exception:
        return parse_iso(raw)


def get_child_text(elem: ET.Element, candidates: list[str]) -> str:
    for candidate in candidates:
        child = elem.find(candidate)
        if child is not None:
            return "".join(child.itertext()).strip()
    return ""


def should_keep_social_title(title: str) -> bool:
    lowered = (title or "").strip().lower()
    if not lowered:
        return False
    low_signal_fragments = [
        " added ",
        " removed ",
        " created branch ",
        " deleted branch ",
        " pushed to ",
        " force-pushed ",
        " commented on ",
        " closed ",
        " reopened ",
        " merged ",
        " opened ",
        " reviewed ",
    ]
    if any(fragment in lowered for fragment in low_signal_fragments):
        return False
    return True


def parse_atom_feed_entries(feed_url: str) -> list[dict[str, Any]]:
    root = ET.fromstring(fetch_text(feed_url))
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns) or root.findall("{http://www.w3.org/2005/Atom}entry")
    parsed: list[dict[str, Any]] = []

    for entry in entries:
        title = clean_text(get_child_text(entry, ["{http://www.w3.org/2005/Atom}title", "title"]))
        published = parse_feed_datetime(
            get_child_text(
                entry,
                [
                    "{http://www.w3.org/2005/Atom}updated",
                    "{http://www.w3.org/2005/Atom}published",
                    "updated",
                    "published",
                ],
            )
        )
        link = ""
        for node in entry.findall("{http://www.w3.org/2005/Atom}link"):
            href = node.attrib.get("href", "").strip()
            rel = node.attrib.get("rel", "alternate")
            if href and rel in ("alternate", ""):
                link = href
                break
        summary = clean_text(
            get_child_text(
                entry,
                [
                    "{http://www.w3.org/2005/Atom}content",
                    "{http://www.w3.org/2005/Atom}summary",
                    "content",
                    "summary",
                ],
            )
        )

        parsed.append(
            {
                "title": title,
                "published": published,
                "url": link,
                "summary": summary,
            }
        )

    return parsed


def build_social_radar(window_start: datetime) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not SOCIAL_WATCHLIST_PATH.exists():
        return [], []

    watchlist = json.loads(SOCIAL_WATCHLIST_PATH.read_text(encoding="utf-8"))
    candidates: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    for actor_entry in watchlist:
        actor = actor_entry["actor"]
        tier = actor_entry["tier"]
        for channel in actor_entry.get("channels", []):
            channel_type = channel.get("type", "")
            automation_support = channel.get("automation_support", "manual")

            if automation_support == "manual":
                diagnostics.append(
                    {
                        "actor": actor,
                        "channel_type": channel_type,
                        "status": "manual_only",
                        "automation_support": automation_support,
                        "items": 0,
                    }
                )
                continue

            if channel_type != "github":
                diagnostics.append(
                    {
                        "actor": actor,
                        "channel_type": channel_type,
                        "status": "unsupported_automation",
                        "automation_support": automation_support,
                        "items": 0,
                    }
                )
                continue

            repositories = channel.get("repositories", [])
            for repo in repositories:
                repo_feed_url = repo.get("feed_url")
                repo_automation = repo.get("automation_support", "github_release_atom")
                repo_signal_class = repo.get("signal_class", "repo_releases")
                if not repo_feed_url:
                    continue

                try:
                    entries = parse_atom_feed_entries(repo_feed_url)
                    kept = 0
                    for entry in entries:
                        title = entry["title"]
                        published = entry["published"]
                        link = entry["url"]
                        summary = entry["summary"]

                        if not link or published is None or published < window_start:
                            continue

                        candidates.append(
                            {
                                "actor": actor,
                                "tier": tier,
                                "source": f"{repo['name']} GitHub Releases",
                                "channel_type": channel_type,
                                "channel_url": channel["url"],
                                "repo_name": repo["name"],
                                "repo_url": repo["url"],
                                "feed_url": repo_feed_url,
                                "signal_class": repo_signal_class,
                                "published": published.isoformat(),
                                "title": title or slug_to_title(link),
                                "url": link,
                                "summary": summary,
                                "automation_support": repo_automation,
                                "confirmation_status": "official_repo_release",
                                "triage_hint": "candidate_for_digest",
                                "tags": [
                                    "social-radar",
                                    "github",
                                    "repo-release",
                                    tier,
                                    actor.lower().replace(" ", "-"),
                                    repo["name"].replace("/", "-").lower(),
                                ],
                            }
                        )
                        kept += 1

                    diagnostics.append(
                        {
                            "actor": actor,
                            "channel_type": channel_type,
                            "scope": repo["name"],
                            "status": "ok",
                            "automation_support": repo_automation,
                            "items": kept,
                        }
                    )
                except (HTTPError, URLError, TimeoutError, socket.timeout, ET.ParseError, ValueError) as exc:
                    diagnostics.append(
                        {
                            "actor": actor,
                            "channel_type": channel_type,
                            "scope": repo["name"],
                            "status": "error",
                            "automation_support": repo_automation,
                            "items": 0,
                            "error": clean_text(str(exc), limit=160),
                        }
                    )

            feed_url = channel.get("feed_url") or f"{channel['url']}.atom"

            try:
                entries = parse_atom_feed_entries(feed_url)
                kept = 0
                for entry in entries:
                    title = entry["title"]
                    published = entry["published"]
                    link = entry["url"]
                    summary = entry["summary"]

                    if not link or published is None or published < window_start:
                        continue
                    if not should_keep_social_title(title):
                        continue

                    candidates.append(
                        {
                            "actor": actor,
                            "tier": tier,
                            "source": f"{actor} GitHub Atom",
                            "channel_type": channel_type,
                            "channel_url": channel["url"],
                            "feed_url": feed_url,
                            "signal_class": channel.get("signal_class", "org_activity"),
                            "published": published.isoformat(),
                            "title": title or slug_to_title(link),
                            "url": link,
                            "summary": summary,
                            "automation_support": automation_support,
                            "confirmation_status": "needs_official_confirm",
                            "triage_hint": "social-radar-only",
                            "tags": ["social-radar", "github", "org-activity", tier, actor.lower().replace(" ", "-")],
                        }
                    )
                    kept += 1

                diagnostics.append(
                    {
                        "actor": actor,
                        "channel_type": channel_type,
                        "scope": actor.lower().replace(" ", "-"),
                        "status": "ok",
                        "automation_support": automation_support,
                        "items": kept,
                    }
                )
            except (HTTPError, URLError, TimeoutError, socket.timeout, ET.ParseError, ValueError) as exc:
                diagnostics.append(
                    {
                        "actor": actor,
                        "channel_type": channel_type,
                        "scope": actor.lower().replace(" ", "-"),
                        "status": "error",
                        "automation_support": automation_support,
                        "items": 0,
                        "error": clean_text(str(exc), limit=160),
                    }
                )

    deduped: dict[str, dict[str, Any]] = {}
    signal_rank = {
        "repo_releases": 2,
        "org_activity": 1,
    }
    for item in sorted(
        candidates,
        key=lambda item: (
            item["published"],
            signal_rank.get(item.get("signal_class", ""), 0),
        ),
        reverse=True,
    ):
        url = item["url"]
        if url not in deduped:
            deduped[url] = item

    ordered = sorted(
        deduped.values(),
        key=lambda item: (
            signal_rank.get(item.get("signal_class", ""), 0),
            item["published"],
        ),
        reverse=True,
    )
    return ordered[:30], diagnostics


def parse_feed(xml_text: str, source: dict[str, Any], window_start: datetime) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    items: list[dict[str, Any]] = []
    max_items = int(source.get("max_items", 8))
    tags = list(source.get("tags", []))
    keywords_any = [keyword.lower() for keyword in source.get("keywords_any", [])]

    if root.tag.endswith("rss"):
        channel = root.find("channel")
        if channel is None:
            return []
        for item in channel.findall("item"):
            title = clean_text(get_child_text(item, ["title"]))
            link = get_child_text(item, ["link"])
            summary = clean_text(get_child_text(item, ["description", "content:encoded"]))
            published = parse_feed_datetime(get_child_text(item, ["pubDate", "published", "updated"]))
            haystack = f"{title} {summary}".lower()
            if keywords_any and not any(keyword in haystack for keyword in keywords_any):
                continue
            if not link or published is None or published < window_start:
                continue
            items.append(
                {
                    "source": source["name"],
                    "source_kind": source["kind"],
                    "source_priority": source["source_priority"],
                    "title": title or slug_to_title(link),
                    "url": link,
                    "published": published.isoformat(),
                    "summary": summary,
                    "category_hint": infer_category(title, link, tags),
                    "tags": tags,
                }
            )
    elif root.tag.endswith("feed"):
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns) or root.findall("{http://www.w3.org/2005/Atom}entry")
        for entry in entries:
            title = clean_text(get_child_text(entry, ["{http://www.w3.org/2005/Atom}title", "title"]))
            summary = clean_text(
                get_child_text(
                    entry,
                    [
                        "{http://www.w3.org/2005/Atom}summary",
                        "{http://www.w3.org/2005/Atom}content",
                        "summary",
                        "content",
                    ],
                )
            )
            link = ""
            for node in entry.findall("{http://www.w3.org/2005/Atom}link"):
                href = node.attrib.get("href", "").strip()
                rel = node.attrib.get("rel", "alternate")
                if href and rel in ("alternate", ""):
                    link = href
                    break
            if not link:
                link = get_child_text(entry, ["{http://www.w3.org/2005/Atom}id", "id"])
            published = parse_feed_datetime(
                get_child_text(
                    entry,
                    [
                        "{http://www.w3.org/2005/Atom}updated",
                        "{http://www.w3.org/2005/Atom}published",
                        "updated",
                        "published",
                    ],
                )
            )
            haystack = f"{title} {summary}".lower()
            if keywords_any and not any(keyword in haystack for keyword in keywords_any):
                continue
            if not link or published is None or published < window_start:
                continue
            items.append(
                {
                    "source": source["name"],
                    "source_kind": source["kind"],
                    "source_priority": source["source_priority"],
                    "title": title or slug_to_title(link),
                    "url": link,
                    "published": published.isoformat(),
                    "summary": summary,
                    "category_hint": infer_category(title, link, tags),
                    "tags": tags,
                }
            )

    items.sort(key=lambda item: item["published"], reverse=True)
    return items[:max_items]


def parse_sitemap(xml_text: str, source: dict[str, Any], window_start: datetime) -> list[dict[str, Any]]:
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.fromstring(xml_text)
    items: list[dict[str, Any]] = []
    max_items = int(source.get("max_items", 8))
    tags = list(source.get("tags", []))
    allow_prefixes = tuple(source.get("allow_prefixes", []))
    exclude_prefixes = tuple(source.get("exclude_prefixes", []))

    for url_elem in root.findall(".//sm:url", ns):
        raw_loc = get_child_text(url_elem, ["sm:loc", "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"])
        raw_lastmod = get_child_text(
            url_elem,
            ["sm:lastmod", "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod"],
        )
        if not raw_loc:
            continue
        loc = urljoin(source["url"], raw_loc)
        path = urlparse(loc).path
        if allow_prefixes and not path.startswith(allow_prefixes):
            continue
        if exclude_prefixes and path.startswith(exclude_prefixes):
            continue
        published = parse_iso(raw_lastmod)
        if published is None or published < window_start:
            continue
        title = slug_to_title(loc)
        items.append(
            {
                "source": source["name"],
                "source_kind": source["kind"],
                "source_priority": source["source_priority"],
                "title": title,
                "url": loc,
                "published": published.isoformat(),
                "summary": "",
                "category_hint": infer_category(title, loc, tags),
                "tags": tags,
            }
        )

    items.sort(key=lambda item: item["published"], reverse=True)
    selected = items[:max_items]

    preview_budget = int(source.get("preview_budget", 2))
    for item in selected[:preview_budget]:
        if item["summary"]:
            continue
        preview = extract_page_preview(item["url"])
        if not preview:
            continue
        if preview.get("title") and item["title"] == slug_to_title(item["url"]):
            item["title"] = preview["title"]
        if preview.get("summary"):
            item["summary"] = preview["summary"]

    return selected


def build_bundle(window_start: datetime) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sources = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    candidates: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    for source in sources:
        try:
            payload = fetch_text(source["url"])
            if source["kind"] == "feed":
                source_items = parse_feed(payload, source, window_start)
            elif source["kind"] == "sitemap":
                source_items = parse_sitemap(payload, source, window_start)
            else:
                source_items = []
            candidates.extend(source_items)
            diagnostics.append(
                {
                    "source": source["name"],
                    "status": "ok",
                    "items": len(source_items),
                    "kind": source["kind"],
                }
            )
        except (HTTPError, URLError, TimeoutError, socket.timeout, ET.ParseError, ValueError) as exc:
            diagnostics.append(
                {
                    "source": source["name"],
                    "status": "error",
                    "kind": source["kind"],
                    "error": clean_text(str(exc), limit=160),
                }
            )

    deduped: dict[str, dict[str, Any]] = {}
    for item in sorted(
        candidates,
        key=lambda item: (
            item["published"],
            item["source_priority"],
        ),
        reverse=True,
    ):
        url = item["url"]
        if url not in deduped:
            deduped[url] = item

    ordered = sorted(
        deduped.values(),
        key=lambda item: (
            item["source_priority"],
            item["published"],
        ),
        reverse=True,
    )
    return ordered[:30], diagnostics


def main() -> None:
    args = parse_args()
    dry_run = bool(args.dry_run)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
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
        bundle_path = DRY_RUN_BUNDLE_PATH
        social_radar_path = DRY_RUN_SOCIAL_RADAR_PATH
    else:
        note_path = report_root / year / f"{date_label} AI Daily Brief.md"
        state_path = STATE_PATH
        bundle_path = BUNDLE_PATH
        social_radar_path = SOCIAL_RADAR_PATH

    candidates, diagnostics = build_bundle(window_start)
    social_candidates, social_diagnostics = build_social_radar(window_start)

    bundle = {
        "generated_at": now.isoformat(),
        "window_start": window_start.isoformat(),
        "window_mode": window_mode,
        "dry_run": dry_run,
        "candidate_count": len(candidates),
        "diagnostics": diagnostics,
        "candidates": candidates,
    }
    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

    social_bundle = {
        "generated_at": now.isoformat(),
        "window_start": window_start.isoformat(),
        "window_mode": window_mode,
        "dry_run": dry_run,
        "candidate_count": len(social_candidates),
        "diagnostics": social_diagnostics,
        "candidates": social_candidates,
    }
    social_radar_path.write_text(json.dumps(social_bundle, ensure_ascii=False, indent=2), encoding="utf-8")

    exports = {
        "AI_DAILY_BRIEF_NOW": now.isoformat(),
        "AI_DAILY_BRIEF_WINDOW_START": window_start.isoformat(),
        "AI_DAILY_BRIEF_WINDOW_MODE": window_mode,
        "AI_DAILY_BRIEF_DATE": date_label,
        "AI_DAILY_BRIEF_NOTE_PATH": str(note_path),
        "AI_DAILY_BRIEF_STATE_PATH": str(state_path),
        "AI_DAILY_BRIEF_BUNDLE_PATH": str(bundle_path),
        "AI_DAILY_BRIEF_SOCIAL_RADAR_PATH": str(social_radar_path),
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
    print(f"- bundle_path: {exports['AI_DAILY_BRIEF_BUNDLE_PATH']}")
    print(f"- social_radar_path: {exports['AI_DAILY_BRIEF_SOCIAL_RADAR_PATH']}")
    print()
    print("Run this exact export block before writing files:")
    for key, value in exports.items():
        safe = value.replace("'", "'\"'\"'")
        print(f"export {key}='{safe}'")
    print()
    print("Deterministic collector summary:")
    print(f"- candidates_within_window: {len(candidates)}")
    print("- source_status:")
    for diag in diagnostics:
        if diag["status"] == "ok":
            print(f"  - {diag['source']}: ok ({diag['items']} items)")
        else:
            print(f"  - {diag['source']}: error ({diag['error']})")
    print("- top_candidates:")
    for item in candidates[:10]:
        print(f"  - [{item['source']}] {item['title']} | {item['published']} | {item['url']}")
    print()
    print("Social radar summary:")
    print(f"- social_candidates_within_window: {len(social_candidates)}")
    print("- social_source_status:")
    for diag in social_diagnostics:
        label = f"{diag['actor']} {diag['channel_type']}"
        if diag.get("scope"):
            label = f"{label} ({diag['scope']})"
        if diag["status"] == "ok":
            print(f"  - {label}: ok ({diag['items']} items)")
        elif diag["status"] in ("manual_only", "unsupported_automation"):
            print(f"  - {label}: {diag['status']}")
        else:
            print(f"  - {label}: error ({diag['error']})")
    if social_candidates:
        print("- social_top_candidates:")
        for item in social_candidates[:10]:
            print(f"  - [{item['source']}] {item['title']} | {item['published']} | {item['url']}")


if __name__ == "__main__":
    main()
