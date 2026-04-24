#!/usr/bin/env python3
"""Validate the PGStack repo-level skillpack."""

from __future__ import annotations

from pgbrain_engine import REQUIRED_CANONICAL_SKILLS, ROOT, validate_skillpack


def main() -> int:
    errors, warnings = validate_skillpack()

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")

    if errors:
        print(f"skillpack check failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 2

    print(
        "skillpack check passed: "
        f"{len(REQUIRED_CANONICAL_SKILLS)} canonical skills, "
        f"0 error(s), {len(warnings)} warning(s)"
    )
    print(f"root: {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
