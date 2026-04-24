#!/usr/bin/env python3
"""Create a Karpathy-style llm-wiki skeleton without overwriting pages."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Karpathy-style llm-wiki skeleton.")
    parser.add_argument("--root", required=True, help="Directory that will contain the wiki slug.")
    parser.add_argument("--slug", required=True, help="Wiki folder name, e.g. gstack-skills-os.")
    parser.add_argument("--title", required=True, help="Human-readable wiki title.")
    args = parser.parse_args()

    today = date.today().isoformat()
    base = Path(args.root).expanduser() / args.slug

    dirs = [
        "raw/sources",
        "raw/assets",
        "wiki/sources",
        "wiki/entities",
        "wiki/concepts",
        "wiki/syntheses",
        "wiki/comparisons",
        "wiki/questions",
    ]
    for dirname in dirs:
        (base / dirname).mkdir(parents=True, exist_ok=True)

    write_if_missing(
        base / "AGENTS.md",
        f"""# {args.title} Agent Schema

You are maintaining a Karpathy-style LLM Wiki.

## Contract

- Never modify `raw/` sources except to add new immutable source files requested by the user.
- Maintain generated knowledge in `wiki/`.
- Read `wiki/index.md` before answering questions.
- Update `wiki/index.md` and `wiki/log.md` after any durable change.
- Prefer many focused pages over one giant page.
- Use `[[wikilinks]]` for internal wiki connections.
- Distinguish facts, inferences, opinions, and open questions.

## Operations

### Ingest

1. Preserve the source in `raw/sources/`.
2. Create or update a source page in `wiki/sources/`.
3. Update related entity, concept, synthesis, comparison, or question pages.
4. Update `wiki/index.md`.
5. Append to `wiki/log.md`.

### Query

1. Read `wiki/index.md`.
2. Read relevant pages.
3. Answer with wiki links or source links.
4. File durable synthesis back into `wiki/` when useful.

### Lint

Check contradictions, stale claims, orphan pages, missing links, duplicate concepts, and open questions.

## Local Memory

When durable project knowledge changes, write a compact summary to MemTensor with this wiki path and read order.
""",
    )

    write_if_missing(
        base / "wiki/index.md",
        f"""---
title: {args.title} Index
type: index
created: {today}
updated: {today}
---

# {args.title} Index

## Overview

TODO

## Sources

## Entities

## Concepts

## Syntheses

## Comparisons

## Questions

## Recently Updated
""",
    )

    write_if_missing(
        base / "wiki/overview.md",
        f"""---
title: {args.title} Overview
type: overview
created: {today}
updated: {today}
confidence: medium
status: draft
---

# {args.title} Overview

TODO
""",
    )

    write_if_missing(
        base / "wiki/log.md",
        f"""---
title: {args.title} Log
type: log
created: {today}
updated: {today}
---

# {args.title} Log

## [{today}] schema | Initialized wiki

- Created Karpathy-style llm-wiki skeleton.
- Raw source layer: `raw/`
- Generated wiki layer: `wiki/`
- Schema: `AGENTS.md`
""",
    )

    write_if_missing(
        base / "llms.txt",
        f"""# {args.title} LLM Context

This is a Karpathy-style LLM Wiki.

Read order:
1. AGENTS.md
2. wiki/index.md
3. wiki/overview.md
4. Relevant pages under wiki/sources, wiki/entities, wiki/concepts, wiki/syntheses, wiki/comparisons, or wiki/questions

Rule: raw/ is immutable source material. wiki/ is LLM-maintained synthesis.
""",
    )

    print(base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
