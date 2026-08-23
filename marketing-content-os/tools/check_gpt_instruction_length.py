#!/usr/bin/env python3
"""Fail if a GPT Builder Instructions file exceeds the allowed character limit."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path)
    p.add_argument("--limit", type=int, default=8000)
    args = p.parse_args()

    text = args.path.read_text(encoding="utf-8")
    count = len(text)
    print(f"FILE={args.path}")
    print(f"CHARACTERS={count}")
    print(f"LIMIT={args.limit}")
    if count > args.limit:
        print("RESULT=FAIL")
        return 1
    print(f"HEADROOM={args.limit - count}")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
