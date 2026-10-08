#!/usr/bin/env python3
"""Refresh references/base/ from the framework folder (the source of truth). No dependencies.

  sync_base.py [--framework PATH]

Copies concepts/*.md, cross-reference-map.md, flagged-claims.md, situation-playbooks.md and 00-index.md.
Drops lines that talk about the old skill or its audit (not useful inside the skill). Entries (OF-/LD-/MM-)
are NOT bundled; they are cited by ID and live in the framework folder.
Writes references/base/VERSION.txt with the date and file count.
"""
import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

DEFAULT_FRAMEWORK = str(Path(__file__).resolve().parents[3] / "framework")  # repo layout: <repo>/skill/growth-strategy-coach/scripts/
BASE = Path(__file__).resolve().parent.parent / "references" / "base"
SINGLE_FILES = ["cross-reference-map.md", "flagged-claims.md", "situation-playbooks.md", "00-index.md"]
DROP_IF_CONTAINS = ("offer-growth-coach", "skill-audit", "new-skill-design")
README = """# Bundled copy of the framework base

A snapshot of the strategy knowledge base (three Hormozi books, checked entries, concept files).
- Entry IDs (OF-###, LD-###, MM-###) refer to the framework folder's `entries/`, which is **not** bundled.
  In strategist mode, quote the ID; open the entry only if the framework folder is present.
- Do not edit these files here. Edit the framework folder and run `scripts/sync_base.py`.
- Start with `concepts/01-growth-and-unit-economics.md`, then `flagged-claims.md`, then `situation-playbooks.md`.
"""


def clean(text):
    """Drop sentences (or whole lines) that talk about the old skill; keep the rest of the line."""
    out = []
    for line in text.splitlines(keepends=True):
        if not any(k in line for k in DROP_IF_CONTAINS):
            out.append(line)
            continue
        parts = re.split(r"(?<=[.!?])\s+", line.rstrip("\n"))
        kept = [p for p in parts if not any(k in p for k in DROP_IF_CONTAINS) and not re.search(r"\baudit\b", p, re.I)]
        text_left = " ".join(kept).strip()
        # drop the line if nothing but a bullet or note marker is left
        if re.sub(r"^(?:[-*]\s*)?(?:\[our note\]\s*)?", "", text_left).strip():
            out.append(text_left + "\n")
    return "".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--framework", default=DEFAULT_FRAMEWORK)
    args = p.parse_args(argv)
    fw = Path(args.framework)
    if not (fw / "concepts").is_dir():
        print(f"error: {fw}/concepts not found", file=sys.stderr)
        return 2
    if BASE.exists():
        shutil.rmtree(BASE)
    (BASE / "concepts").mkdir(parents=True)
    count = 0
    for src in sorted((fw / "concepts").glob("*.md")):
        (BASE / "concepts" / src.name).write_text(clean(src.read_text(encoding="utf-8")), encoding="utf-8")
        count += 1
    for name in SINGLE_FILES:
        src = fw / name
        if not src.exists():
            print(f"error: missing {src}", file=sys.stderr)
            return 2
        (BASE / name).write_text(clean(src.read_text(encoding="utf-8")), encoding="utf-8")
        count += 1
    (BASE / "README.md").write_text(README, encoding="utf-8")
    (BASE / "VERSION.txt").write_text(f"synced {dt.date.today().isoformat()} from {fw}\nfiles: {count}\n", encoding="utf-8")
    print(f"synced {count} files into {BASE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
