# Approaches — q-unicode-data

## Problem in one line

Decode three files (CP-1252 / UTF-8 / UTF-16), sum `value` where `symbol ∈ {€, ˆ, ”}`.

## Grader (from quiz JS)

- Symbols come from a table of the CP-1252-only characters (code points 128–159: `€ ‚ ƒ „ … † ‡ ˆ ‰ Š …`).
- Each file has 500 rows, `symbol` random from that table, `value` = **row index** (0–499).
- Targets = the **first three symbols of data1.csv** (here € ˆ ”).
- Expected = sum of values whose symbol is a target, across all three files (exact integer).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| `ˆ` in the question | **Trap** | U+02C6 MODIFIER LETTER CIRCUMFLEX, not ASCII `^`. Copy-paste/IME may swap it |
| `”` in the question | **Trap** | U+201D RIGHT DOUBLE QUOTATION MARK, not ASCII `"`. A CSV parser may also treat quotes specially |
| Mixed encodings and line endings | Genuine | Wrong encoding garbles exactly these CP-1252-range symbols. data1 uses `\r\n` |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | pandas `read_csv(encoding=…)` per file | works, but `”` could interact with CSV quoting |
| B | **Plain Python: `read_text(encoding)`, `splitlines()`, split on the first separator; targets as `\u` escapes** | **chosen**: no quoting surprises, no lookalike risk |

## Verification

- `python3 src/sum_symbols.py` → 13010 + 12385 + 15514 = **40909**. Asserts the targets equal data1's first 3 symbols.
- Grader formula regenerated from the seed (seedrandom + symbol table) → **40909**.
- Exam "Check" button: ✅ passed on attempt 1 (2026-10-06).
