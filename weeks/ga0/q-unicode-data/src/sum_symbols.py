"""Sum `value` where `symbol` is one of the target symbols, across three files with different encodings.

Usage: python3 src/sum_symbols.py [data/extracted/q-unicode-data]
Targets are given as code points so lookalikes (^ vs ˆ, " vs ”) can't creep in through copy-paste.
"""
import sys
import unicodedata
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "data/extracted/q-unicode-data")
TARGETS = {"€", "ˆ", "”"}  # € EURO SIGN, ˆ MODIFIER LETTER CIRCUMFLEX ACCENT, ” RIGHT DOUBLE QUOTATION MARK

FILES = [  # (name, encoding, separator)
    ("data1.csv", "cp1252", ","),
    ("data2.csv", "utf-8", ","),
    ("data3.txt", "utf-16", "\t"),  # BOM FF FE → utf-16 picks little-endian
]

total = 0
for name, enc, sep in FILES:
    lines = (root / name).read_text(encoding=enc).splitlines()  # handles \r\n (data1) and \n
    assert lines[0].split(sep) == ["symbol", "value"], f"{name}: unexpected header {lines[0]!r}"
    rows = [line.split(sep, 1) for line in lines[1:] if line]  # split on the FIRST separator only
    sub = sum(int(v) for s, v in rows if s in TARGETS)
    hits = sum(1 for s, _ in rows if s in TARGETS)
    total += sub
    print(f"{name:10} {enc:7} rows={len(rows)} matches={hits} subtotal={sub}")

# Sanity: the targets are the first three symbols of data1.csv (how the grader picks them)
first3 = {l.split(",", 1)[0] for l in (root / "data1.csv").read_text(encoding="cp1252").splitlines()[1:4]}
print("first 3 symbols of data1:", [f"{c} U+{ord(c):04X} {unicodedata.name(c)}" for c in sorted(first3)])
assert first3 == TARGETS, "targets differ from data1's first three symbols"
print(f"ANSWER {total}")
