# Approaches — q-axis-scale-manipulation-repair

## Problem in one line

Find the axis trick in a Chart.js line chart, put a number on how much it exaggerates the trend,
and return the same chart with an honest y-axis plus an explanatory HTML comment that the grader can parse.

## Diagnosis

The broken config is `"scales":{"y":{"min":825.62,"beginAtZero":false}}`.

- Data range: 878.32 → 924.2 (Jan → Aug, monotonic rise).
- `min: 825.62` = exactly **94%** of the lowest value (0.94 × 878.32). The generator picks this
  multiplier from `[0.85, 0.88, 0.91, 0.94, 0.97]`, so the baseline sits just under the data.
- This is a **truncated (non-zero) y-axis**: grader type **A**.

## How the grader works (read from `exam-tds-2026-09-ga0.js`, hacking allowed)

The chart variant is seeded from the student email. There are 4 types:

| Type | Manipulation | Broken config | Required fix pattern (regex on whole submission) | Distortion value |
|------|--------------|---------------|-------------------------------------------------|------------------|
| **A** | truncated y-axis | `y.min` = data min × k | `\bmin\s*:\s*0\b` → literal **`min: 0`** | `round(max / (max − axis_min), 1)` |
| B | dual axis | `y2` + `yAxisID` | no `y2:` / `yAxisID:`, and text "% change" | scale factor of series B |
| C | inverted axis | `reverse: true` | `reverse: false` (or `direction: "ascending"`) | 1 |
| D | log scale | `type: "logarithmic"` | `type: "linear"` + the word "linear" | last delta / first delta |

Checks, in order (each failure stops grading with its error message):

1. Submission ≥ 140 chars.
2. At least one `<!-- … -->` comment.
3. **The first number anywhere in the joined comments** must be within `max(0.2, 15%)` of the distortion value.
4. The axis-fix regex for the type (table above).
5. The comment contains one of the type's phrases. For A: `inflates tiny deltas by 9.4x`,
   `magnifies small movement about 9.4x` or `makes mild change look 9.4x`.
6. (type D only) mentions "linear".
7. Contains `<canvas`, `new Chart(` and `<script`.

The grader never runs the chart. It checks the submitted text only.

## Quantification

| Measure | Formula | Value |
|---------|---------|-------|
| True span (zero baseline) | max − 0 | 924.2 |
| Visible span (truncated) | max − axis min = 924.2 − 825.62 | 98.58 |
| **Distortion (grader)** | **round(max / (max − axis min), 1)** | **9.4** (accepted 7.99 – 10.81) |
| Actual % change Jan→Aug | (924.2 − 878.32) / 878.32 | +5.22% (used in the insight sentence) |

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Compute metrics by hand + minimal config edit | python3, editor | Exact numbers; minimal diff | Guessed the metric and comment format → rejected twice | used for attempts 1–2 |
| B | Ask an LLM to "fix this chart and explain" | ChatGPT / Claude | Fast | Same guessing problem; may rewrite data | rejected |
| C | **Read the grader from the quiz JS, replicate its checks locally, write to spec** | DevTools / curl, python3 | Exact requirements; verifiable before submitting | Needs JS reading | **chosen (attempt 3, passed)** |

## Chosen: C

**Why:** the grader is a deterministic text check, not a human or LLM judge. Reading its source turns
guessing into a spec, and [src/check.py](src/check.py) replicates it, so a submission can be validated
locally before using an attempt.

### Fix decisions

- Config → `"scales":{"y":{min: 0,"beginAtZero":true}}`. The unquoted `min: 0` is valid JS (the
  argument is an object literal, not JSON), and it is required because the grader's regex
  `\bmin\s*:` doesn't match JSON's `"min":0` (the quote sits between `min` and `:`).
- Comment starts with `Quantification: 9.4x`, so **9.4 is the first number**.
- `Distortion:` line uses the exact grader phrase `inflates tiny deltas by 9.4x`.
- Removed every other number before 9.4 (825.62, 878.32, 94%) from the comment.
- Data, labels, colours and title unchanged.

## Attempts

| # | Submission | Grader result | Real cause (confirmed by check.py) |
|---|------------|---------------|------------------------------------|
| 1 | [data/attempt-1-rejected.html](data/attempt-1-rejected.html): lie factor 16.7, `beginAtZero:true` | ❌ "Distortion quantification is outside tolerance. Expected approximately 9.4 (±15%)." | First number in comment = **825.62** (from the Manipulation line); would also fail fix + phrase checks |
| 2 | [data/attempt-2-rejected.html](data/attempt-2-rejected.html): 9.4 in Quantification/Distortion lines | ❌ same error | Still 825.62 first. The metric was never the issue; the line order was. Also, the pasted copy was mangled (copied from terminal) |
| 3 | [src/corrected.html](src/corrected.html): 9.4 first, grader phrase, `min: 0` | ✅ **passed** | all 7 checks pass |

## Gotchas hit

- **First number wins.** The grader takes the first numeric token across *all* comments. Lead with the distortion value.
- **Exact phrase required.** For type A, `inflates tiny deltas by <d>x` (or the two alternatives), with `<d>` to 1 decimal.
- **`min: 0` unquoted.** `beginAtZero: true` alone, or JSON `"min":0`, fails the fix check.
- **Don't copy submissions from the terminal.** Line wrapping mangled attempt 2's body. Use `pbcopy < src/corrected.html`.
- **Read the grader first.** For any auto-graded GA question, check the quiz JS before guessing (it's allowed).

## Verification

- `python3 src/check.py src/corrected.html` → 7/7 PASS. Attempts 1 and 2 → FAIL on the same checks the real grader reported.
- `diff data/original.html src/corrected.html`: only the top comment and `scales.y` differ.
- Rendered with headless Chrome → [data/corrected-chart.png](data/corrected-chart.png): y-axis 0 to 1,000.
- Exam "Check" button: ✅ passed on attempt 3 (2026-10-05).
