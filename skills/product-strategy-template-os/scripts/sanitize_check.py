#!/usr/bin/env python3
"""Scan a skill package for common secret patterns before GitHub publishing."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS = [
    re.compile(r"eyJ[a-zA-Z0-9_\-]{20,}\.[a-zA-Z0-9_\-]{20,}\.[a-zA-Z0-9_\-]{20,}"),
    re.compile(r"accessToken", re.IGNORECASE),
    re.compile(r"app_secret", re.IGNORECASE),
    re.compile(r"appSecret", re.IGNORECASE),
    re.compile(r"Authorization\s*:", re.IGNORECASE),
    re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}", re.IGNORECASE),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "dist"}
TEXT_EXTS = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".js",
    ".py",
    ".toml",
    "",
}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == "sanitize_check.py":
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix not in TEXT_EXTS:
            continue
        yield path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.path).resolve()
    hits = []
    for path in iter_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pattern in PATTERNS:
                if pattern.search(line):
                    hits.append((path, lineno, pattern.pattern))
    if hits:
        for path, lineno, pattern in hits:
            print(f"SECRET_PATTERN\t{path}:{lineno}\t{pattern}")
        raise SystemExit(1)
    print("OK_SANITIZE")


if __name__ == "__main__":
    main()
