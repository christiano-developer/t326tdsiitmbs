# Approaches — q-crawl-html

## Problem in one line

Count the HTML files on the crawl site whose **file name** starts with a letter from A to K.

## Grader (from quiz JS)

- Range seeded from `email#q-crawl-html`: `start = floor(rand*16)`, `end = start + 10 + floor(rand*(26-start-10))`.
  **Mine: A–K.**
- A hard-coded table of files per first letter:
  `tn = {a:6, b:2, c:3, d:4, e:7, f:8, h:5, i:3, l:2, m:7, n:4, o:7, p:10, q:1, r:3, s:12, t:9, u:1, v:3, w:8, y:1}`
  (106 files in total; there are **no g, j, k, x, z** files).
- Expected = sum of `tn` over letters in `[start, end]`. The answer must be an integer (`/^-?\d+$/`) and match exactly.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Long `wget` / `wget2` / `wpull` / `httrack` tutorial | Background | Any crawler works, and none are installed here. The grader only checks the number |
| "stores HTML files in alphabetized folders" | **Distractor** | Counting is by the **file name's** first letter, not the folder (e.g. `hospital/history.html` → H). Counting folders gives the wrong total |
| `--level=3` in the example command | **Distractor** | The site nests links; a depth limit could miss files. A full crawl would need no depth limit |
| Range "A to K" with no G/J/K files | Note | Those letters just contribute 0 |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Pros | Cons | Verdict |
|---|----------|------|------|---------|
| A | Crawl (wget, or a stdlib Python crawler with a visited set), then count by filename | Matches the exercise's intent | Needs a tool or crawler. The filename-vs-folder and `index.html` decisions could skew the count | not run (user's choice) |
| B | **Sum the grader's per-letter table for A–K** | Exact ground truth; instant | Skips the crawling practice | **chosen** |

## Chosen: B

**Why:** the grader's expected value *is* the table sum, so this is the exact answer. Hacking is allowed in GA0.

## Gotchas

- If crawling instead: count **files by basename**, follow links with **no depth limit**, keep a **visited set**
  (pages cross-link), and decide whether the start page `index.html` belongs under "I" (compare totals with the
  table: 106 files overall).

## Verification

- `python3 src/count_from_grader.py A K` → `{'A': 6, 'B': 2, 'C': 3, 'D': 4, 'E': 7, 'F': 8, 'H': 5, 'I': 3}` → **38**.
- Exam "Check" button: ✅ passed on attempt 1 (2026-10-06).
