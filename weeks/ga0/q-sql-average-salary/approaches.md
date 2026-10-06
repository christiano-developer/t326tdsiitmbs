# Approaches — q-sql-average-salary

## Problem in one line

`AVG(salary)` per department, rounded, ordered by department.

## Grader (from quiz JS)

- Seeds 500 employees (5 departments, salary 40000–119999) into an in-browser SQLite (`sqlite-wasm`).
- Runs the submitted SQL with `rowMode: "array"`. For each row, **`row[0]` = department, `row[1]` = average**
  (`Math.round(Number(...))`).
- Every department must be present and within **±5** of the JS-computed `Math.round(mean)`.
- **Row order and column names are not checked.**

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "Order by department name alphabetically" | Mild distractor | Not checked by the grader. Kept anyway (correct SQL) |
| "Round to the nearest whole number" | Mild | Grader rounds `row[1]` itself; ±5 tolerance |
| Column order | **Trap** | Department must be the **first** column and the average the **second** (`SELECT AVG(salary), department …` would fail) |
| Long SQLite tutorial | Background | Not checked |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | **`SELECT department, ROUND(AVG(salary)) … GROUP BY department ORDER BY department`** | **chosen** |

## Verification

- Regenerated the seeded table (`src/gen_employees.mjs`); first 5 rows match the page preview.
- `python3 src/check.py` → rows match expected exactly → PASS.
- Exam "Check" button: ✅ passed on attempt 1 (2026-10-06).
