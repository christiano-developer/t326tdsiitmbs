#!/usr/bin/env python3
"""Generate docs/assignments.md from every section table (weeks/*/README.md).

Runs at build time (.github/workflows/pages.yml), so the docs site lists whatever sections
the built branch holds, and init never stores section content. Output is git-ignored.

Usage: python3 scripts/docs-assignments.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOB = "https://github.com/christiano-developer/t326tdsiitmbs/blob/main"
ROW = re.compile(r"^\|\s*\[(?P<q>q-[^\]]+)\]")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


out = ["# Assignments", "",
       "Each question links to its `final.md`: a teammate how-to plus the steps that reproduce the answer.", ""]
sections = sorted(ROOT.glob("weeks/*/README.md"), key=lambda p: p.parent.name)
for index in sections:
    sec = index.parent.name
    rows = [cells(l) for l in index.read_text().splitlines() if ROW.match(l)]
    if not rows:
        continue
    # Columns: Question | Marks | Deploy | Status | Answer
    solved = sum(r[3] == "solved" for r in rows)
    out += [f"## {sec.upper()}", "", f"{solved} of {len(rows)} solved.", "",
            "| Question | Marks | Deploy | Status | Approach |", "|---|---|---|---|---|"]
    for r in rows:
        q = ROW.match("| " + r[0]).group("q")
        link = f"[{q}]({BLOB}/weeks/{sec}/{q}/final.md)" if r[3] == "solved" else q
        out.append(f"| {link} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")
    out.append("")
if len(out) == 4:
    out.append("No sections on this branch yet.")

dest = ROOT / "docs" / "assignments.md"
dest.write_text("\n".join(out) + "\n")
print(f"wrote {dest.relative_to(ROOT)} ({len(sections)} sections)")
