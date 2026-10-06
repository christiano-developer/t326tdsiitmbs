"""Local replica of the GA0 axis-scale grader (ported from exam-tds-2026-09-ga0.js).

Usage: python3 src/check.py src/corrected.html [expected_distortion] [type]
  expected_distortion  default 9.4 (type A: round(max / (max - axis_min), 1))
  type                 A truncated | B dual-axis | C inverted | D log   (default A)
"""
import re
import sys

path = sys.argv[1]
expected = float(sys.argv[2]) if len(sys.argv) > 2 else 9.4
kind = sys.argv[3] if len(sys.argv) > 3 else "A"
html = open(path).read()

# Phrase sets the grader accepts (function X in the quiz JS); type A/B/D embed the factor.
f = f"{expected:.1f}"
phrases = {
    "A": [f"inflates tiny deltas by {f}x", f"magnifies small movement about {f}x", f"makes mild change look {f}x"],
    "B": ["rescaled axis fakes synchronized trend", "dual-axis scaling manufactures false correlation",
          "secondary scale distorts cross-series comparison", f"right axis stretched by {f}x"],
    "C": ["inverted axis flips decline narrative", "descending scale reverses trend meaning",
          "axis direction turns fall into rise"],
    "D": ["log scale compresses linear acceleration", "log axis hides arithmetic growth pace",
          "linear growth appears flattened on log", f"growth visually compressed by {f}x"],
}[kind]

# Axis-fix patterns (function ma in the quiz JS)
def fix_ok(s):
    if kind == "A":
        return bool(re.search(r"\bmin\s*:\s*0(?:\.0+)?\b", s))
    if kind == "B":
        return (not re.search(r"\by2\b\s*:", s) and not re.search(r"\byAxisID\s*:", s)
                and bool(re.search(r"%\s*change|percent\s*change|percentage\s*change", s, re.I)))
    if kind == "C":
        return bool(re.search(r"\breverse\s*:\s*false\b", s) or re.search(r"\bdirection\s*:\s*[\"']ascending[\"']", s))
    return bool(re.search(r"\btype\s*:\s*[\"']linear[\"']", s))

comments = " ".join(re.findall(r"<!--([\s\S]*?)-->", html))
m = re.search(r"-?\d+(?:\.\d+)?", comments)
first = float(m.group()) if m else None
tol = max(0.2, abs(expected) * 0.15)
norm = re.sub(r"\s+", " ", comments.lower())

checks = [
    ("length >= 140", len(html.strip()) >= 140),
    ("has comment", bool(comments.strip())),
    (f"first number in comment ({first}) within {expected} ± {tol:.2f}", first is not None and abs(first - expected) <= tol),
    (f"axis fix pattern for type {kind}", fix_ok(html)),
    ("distortion phrase present", any(p.lower() in norm for p in phrases)),
    ("log type mentions 'linear'", kind != "D" or bool(re.search(r"\blinear\b", comments + " " + html, re.I))),
    ("canvas + new Chart( + <script", bool(re.search(r"<canvas\b", html, re.I) and re.search(r"new\s+Chart\s*\(", html)
                                          and re.search(r"<script[\s>]", html, re.I))),
]
for name, ok in checks:
    print(("PASS " if ok else "FAIL ") + name)
sys.exit(0 if all(ok for _, ok in checks) else 1)
