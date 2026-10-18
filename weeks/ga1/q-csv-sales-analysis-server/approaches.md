# Approaches — q-csv-sales-analysis-server

## Problem in one line

Filtered SUM(quantity*price), rounded.

## Grader (from quiz JS)

- Client-side: recomputes from the seed; passes if `|answer − expected| ≤ 2`.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| `date` format | Gotcha | `2025-Mar-5`: month is a name, day not zero-padded; don't parse as ISO |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Small script: split CSV, filter city + month name, sum qty × price | Node (or browser JS) | No dependencies, handles the `2025-May-8` format explicitly | None here | chosen |
| B | DuckDB / sqlite SQL over the CSV | duckdb | One query | Date isn't ISO, so it needs `split_part`/string matching anyway | rejected |
| C | Spreadsheet filter + SUMPRODUCT | Excel / Sheets | Visual | Manual, slower | rejected |

## Chosen: A

**Why:** 112 rows; a 10-line script is the fastest and also handles the non-ISO dates.

## Gotchas hit

- Month is a name (`May`), not a number, and days aren't zero-padded: match the middle part of `date.split("-")`.
- No messy data in this seed: no extra spaces, case variants or bad rows (checked: every row has 5 fields).
- The ZIP is a `blob:` URL built in the page, so it can be fetched and unzipped in the tab.

## Verification

- Rows matched: `2025-May-8 Keyboard 4×475.99`, `2025-May-22 Monitor 7×573.82`, `2025-May-16 Mouse 10×472.45`,
  `2025-May-12 Phone 7×195.04` → 1903.96 + 4016.74 + 4724.50 + 1365.28 = 12010.48 → 12010.
- `node src/revenue.mjs data/sales_data.csv Bangalore May` → `12010`.
- Exam **Check** → "Correct" (Brave and Chrome, 2026-10-18). Grader tolerance is ±2.
