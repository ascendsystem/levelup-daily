#!/usr/bin/env python3
"""Verify GTM installation and required routes in generated Pages output."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GTM_ID = "GTM-KC2GX2KQ"
GTM_SRC = f"https://www.googletagmanager.com/gtm.js?id={GTM_ID}"
GTM_SCRIPT = f'<script async src="{GTM_SRC}"></script>'
GTM_INITIALIZATION = (
    "window.dataLayer = window.dataLayer || [];",
    "function gtag(){dataLayer.push(arguments);}",
    "gtag('js', new Date());",
)
HEAD_RE = re.compile(r"<head\b[^>]*>.*?</head\s*>", re.IGNORECASE | re.DOTALL)
EXCLUDED_DIRS = {".git", "_site", "tmp"}


def audit(root: Path) -> list[str]:
    errors = []
    if not root.is_dir():
        return [f"Site directory does not exist: {root}"]

    pages = []
    for path in root.rglob("*.html"):
        relative = path.relative_to(root)
        if EXCLUDED_DIRS.intersection(relative.parts):
            continue
        content = path.read_text(encoding="utf-8")
        match = HEAD_RE.search(content)
        if not match:
            continue
        pages.append(path)
        head = match.group(0)
        if head.count(GTM_SCRIPT) != 1:
            errors.append(f"{relative}: expected exactly one GTM script, found {head.count(GTM_SCRIPT)}.")
        if content.count(GTM_ID) != 1:
            errors.append(f"{relative}: expected exactly one GTM container ID, found {content.count(GTM_ID)}.")
        for marker in GTM_INITIALIZATION:
            if head.count(marker) != 1:
                errors.append(f"{relative}: expected exactly one GTM initialization marker: {marker}")

    if not pages:
        errors.append(f"No complete HTML pages found in {root}.")
    if not (root / "curiosidades" / "index.html").is_file():
        errors.append(f"Missing required route: {root / 'curiosidades' / 'index.html'}")
    if errors:
        return errors

    print(f"Passed: {len(pages)} HTML pages have one GTM installation; curiosidades/index.html exists in {root}.")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.site_root.resolve()
    errors = audit(root)
    if errors:
        print(f"FAILED: {len(errors)} page deployment check(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
