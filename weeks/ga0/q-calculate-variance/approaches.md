# Approaches — q-calculate-variance

## Problem in one line

Sample variance (N−1) of 1000 numbers from a JSON array, rounded to 2 decimals.

## Grader (from quiz JS)

- Data: seeded from `email#q-calculate-variance`. `base = rand*50 + 25`, then 1000 values
  `floor(max(0, base + rand*40 − 20))` → integers in a ±20 band around the base.
- Expected: `sampleVariance(s).toFixed(2)` from **simple-statistics@7** (N−1).
- Check: `parseFloat(answer)` must be within **±0.05** of the expected value.
- The JSON is generated in the browser from the same array (`JSON.stringify(s)`), so the file matches the expected value exactly.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Topic label "Spreadsheet: Excel, Google Sheets" with a JSON download | Mild distractor | It's the skill category, not a requirement. The grader only checks the number; any tool works. Sheets has no native JSON import, so Python is simplest |
| "Sample variance (N−1)" and the `statistics.variance` / `VAR.S` hint | Genuine | Grader uses `sampleVariance` (N−1). **Population variance (N) = 130.04 is off by 0.13, outside ±0.05 → would fail** |
| "The data contains no missing values" | Genuine (verified) | 1000 ints, no strings/null/NaN |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Pros | Cons | Verdict |
|---|----------|------|------|---------|
| A | Python `statistics.variance` + manual N−1 cross-check | One command, exact, reproducible | — | **chosen** |
| B | Excel/Sheets `VAR.S` | Matches the topic label | Needs JSON → cells conversion (Power Query or paste + split) | not needed |
| C | JS `simple-statistics.sampleVariance` | Identical to the grader | Needs Node + package | not needed |

## Chosen: A

**Why:** fastest and exact. The manual formula guards against using the wrong function.

## Gotchas

- N vs N−1: with n=1000 the gap is only 0.13, but the tolerance is 0.05, so the wrong formula fails.
- **Enter the bare number.** Stray whitespace in the typed value got the first entry rejected. Paste exactly `130.17`.

## Verification

- `python3 src/variance.py` → `ANSWER sample variance (N-1): 130.17` (manual N−1 = 130.1736526527, identical).
- `node src/regenerate.mjs data/q-calculate-variance.json <email>` (needs `npm i seedrandom@3 simple-statistics@7`):
  the file matches the seed for `<my-exam-email>` exactly → expected 130.17.
- Exam "Check" button: first entry rejected because of stray whitespace in the typed value. `130.17` re-entered
  cleanly → ✅ **passed** (2026-10-06).
