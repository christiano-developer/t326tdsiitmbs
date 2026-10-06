"""Local replica of the GA0 colour-encoding grader (ported from exam-tds-2026-09-ga0.js).

Usage: python3 src/check.py src/corrected.html [scheme]   (scheme default: categorical)

Ported exactly, including quirks:
- hex extraction: EVERY #rgb/#rrggbb in the whole submission (CSS, comments, text), deduped in order
- categorical: pairwise CIEDE2000 >= 30 over the FIRST 8 extracted colours
- the grader's CIEDE2000 hue adds 360 when b < 0 OR a' < 0 (non-standard), replicated as-is
"""
import math
import re
import sys

PHRASES = [  # "Website Traffic by Source" variant: expectedSynonyms
    "falsely implies traffic sources have a natural progression",
    "hierarchy among sources",
    "implies ordering among unordered sources",
    "traffic sources have a natural progression",
    "false hierarchy",
]


def extract_hex(html):
    out = []
    for h in re.findall(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", html):
        h = "#" + "".join(c * 2 for c in h[1:]) if len(h) == 4 else h.lower()
        if h not in out:
            out.append(h)
    return out


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lab(h):
    r, g, b = (_lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.072175 * b
    z = 0.0193339 * r + 0.119192 * g + 0.9503041 * b
    f = lambda t: math.copysign(abs(t) ** (1 / 3), t) if t > 0.008856 else 7.787 * t + 0.13793103448275862
    fx, fy, fz = f(x / 0.95047), f(y / 1), f(z / 1.08883)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def ciede2000(c1, c2):
    e, r, n = lab(c1)
    l, s, a = lab(c2)
    i, u = math.hypot(r, n), math.hypot(s, a)
    d = ((i + u) / 2) ** 7
    m = 0.5 * (1 - math.sqrt(d / (d + 25 ** 7)))
    p, h = r * (1 + m), s * (1 + m)
    g, f = math.hypot(p, n), math.hypot(h, a)
    y = math.degrees(math.atan2(n, p)) + (360 if (n < 0 or p < 0) else 0)
    w = math.degrees(math.atan2(a, h)) + (360 if (a < 0 or h < 0) else 0)
    b, x, E = l - e, f - g, w - y
    if abs(E) > 180:
        E += -360 if E > 0 else 360
    T = 2 * math.sqrt(g * f) * math.sin(math.radians(E / 2))
    _, A, O = (e + l) / 2, (g + f) / 2, (y + w) / 2
    if abs(y - w) > 180:
        O += 180 if O < 180 else -180
    P = (1 - 0.17 * math.cos(math.radians(O - 30)) + 0.24 * math.cos(math.radians(2 * O))
         + 0.32 * math.cos(math.radians(3 * O + 6)) - 0.2 * math.cos(math.radians(4 * O - 63)))
    k = 1 + 0.015 * (_ - 50) ** 2 / math.sqrt(20 + (_ - 50) ** 2)
    C, R = 1 + 0.045 * A, 1 + 0.015 * A * P
    q = 2 * math.sqrt(A ** 7 / (A ** 7 + 25 ** 7))
    V = 30 * math.exp(-(((O - 275) / 25) ** 2))
    Q = -math.sin(math.radians(2 * V)) * q
    return math.sqrt((b / k) ** 2 + (x / C) ** 2 + (T / R) ** 2 + Q * (x / C) * (T / R))


def hue(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    mx, mn = max(r, g, b), min(r, g, b)
    if mx == mn:
        return 0
    if mx == r:
        c = math.fmod((g - b) / (mx - mn), 6)  # JS % keeps the sign
    elif mx == g:
        c = (b - r) / (mx - mn) + 2
    else:
        c = (r - g) / (mx - mn) + 4
    return (c * 60 + 360) % 360


def main():
    html = open(sys.argv[1]).read()
    scheme = sys.argv[2] if len(sys.argv) > 2 else "categorical"
    cols = extract_hex(html)
    print("extracted hex (in order):", cols)
    fails = []
    if len(html.strip()) < 50:
        fails.append("submission too short")
    if len(cols) < 2:
        fails.append("fewer than 2 hex colours")
    if len(cols) >= 6:
        hs = sorted(hue(c) for c in cols)
        if hs[-1] - hs[0] > 270:
            fails.append(f"rainbow: hue span {hs[-1]-hs[0]:.0f} > 270")
    if scheme == "categorical":
        first8 = cols[:8]
        for i in range(len(first8)):
            for j in range(i + 1, len(first8)):
                d = ciede2000(first8[i], first8[j])
                flag = "OK " if d >= 30 else "LOW"
                print(f"  {flag} dE00 {first8[i]} vs {first8[j]} = {d:.1f}")
                if d < 30:
                    fails.append(f"{first8[i]} vs {first8[j]} dE00 {d:.1f} < 30")
    if scheme not in html.lower():
        fails.append(f"scheme word '{scheme}' missing")
    if not any(p.lower() in html.lower() for p in PHRASES):
        fails.append("no accepted mismatch phrase")
    print("\nPASS" if not fails else "\nFAIL:\n  " + "\n  ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
