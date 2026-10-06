# Approaches — q-sort-filter-json

## Problem in one line

Keep products with price ≥ 114.97, sort by category ↑, price ↓, name ↑, output minified JSON.

## Grader (from quiz JS)

- Seeded: 100 products (5 categories, names `<adj> <noun>`, price `20–200` to 2 decimals) and threshold `50–150`.
- Expected: `filter(price >= c)` then sort by `category.localeCompare || b.price - a.price || name.localeCompare`.
- Check: `JSON.parse(answer)`; same length; every item's `category`, `price`, `name` equal by position.
  **Formatting is not checked** (minified or pretty both parse).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "Filter out price < 114.97" | Boundary | Keeps **price ≥ 114.97**; an item at exactly 114.97 would stay (none here) |
| "single minified JSON string" | Mild distractor | The grader parses, so whitespace doesn't matter. Minified is still pasted to be safe |
| `localeCompare` vs Python string order | Note | Same result here (ASCII, capitalised words); confirmed by running the grader's own JS sort |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | **Python `json` + sort key `(category, -price, name)`** | **chosen** |
| B | `jq 'map(select(.price >= 114.97)) \| sort_by(.category, -.price, .name)' -c` | equivalent alternative |

## Verification

- `python3 src/sort_filter.py` → 44 items; monotonic order verified; no (category, price) ties.
- `node src/grader_check.mjs <exam-email> data/products.json data/answer.min.json` → data matches the paste,
  threshold 114.97, **grader check true (44/44)**.
- Exam "Check" button: ✅ passed on attempt 1 (2026-10-06).
