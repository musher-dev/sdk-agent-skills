#!/usr/bin/env python3
"""Rewrite the Catalog index in the musher skill from the live, anonymous Catalog API.

    python3 scripts/gen_catalog_index.py            # rewrite the index
    python3 scripts/gen_catalog_index.py --check    # exit 1 when the index is out of date

The index sits between two markers in
plugins/musher/skills/musher/references/catalog.md, and only that part of the
file is rewritten. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

API = "https://api.musher.dev/v1/catalog/listings"
TARGET = Path(__file__).resolve().parent.parent / "plugins/musher/skills/musher/references/catalog.md"
BEGIN = "<!-- catalog-index:begin -->"
END = "<!-- catalog-index:end -->"


def fetch() -> list[dict]:
    listings: list[dict] = []
    cursor = None
    while True:
        url = f"{API}?limit=100" + (f"&cursor={cursor}" if cursor else "")
        request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "sdk-agent-skills"})
        with urllib.request.urlopen(request, timeout=30) as response:
            page = json.load(response)
        listings.extend(page["data"])
        cursor = (page.get("meta") or {}).get("nextCursor")
        if not cursor:
            return listings


def render(listings: list[dict]) -> str:
    rows = [
        "| Slug | Name | Deploys on its own | Stage | Category |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in sorted(listings, key=lambda listing: listing["slug"]):
        deployable = "yes" if item["itemType"] == "BLUEPRINT" else "no: a component for a blueprint"
        rows.append(
            f"| `{item['slug']}` | {item['displayName']} | {deployable} | {item['lifecycleStage'].lower()} "
            f"| {item['category'].replace('_', ' ').lower()} |"
        )
    return "\n".join([BEGIN, *rows, END])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="fail when the index differs from the live Catalog")
    args = parser.parse_args()

    text = TARGET.read_text(encoding="utf-8")
    head, _, rest = text.partition(BEGIN)
    _, _, tail = rest.partition(END)
    updated = head + render(fetch()) + tail
    if args.check:
        if updated != text:
            print(f"{TARGET.name} is out of date; run python3 scripts/gen_catalog_index.py", file=sys.stderr)
            return 1
        return 0
    TARGET.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
