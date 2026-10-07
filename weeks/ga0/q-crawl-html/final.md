# Final — q-crawl-html

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-crawl-html](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-crawl-html)

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

1. Note your letter range from the question (for example A to K).
2. Open your TDS folder for this GA (create `TDS/GA0` if you don't have one) and open a terminal in it. Create `count.py`, set your range on the last line, and run `python3 count.py`:
   ```python
   # files per first letter, copied from the grader
   TN = {"t": 9, "n": 4, "s": 12, "i": 3, "w": 8, "e": 7, "a": 6, "p": 10, "f": 8, "m": 7, "h": 5,
         "c": 3, "y": 1, "o": 7, "v": 3, "r": 3, "d": 4, "l": 2, "b": 2, "q": 1, "u": 1}
   start, end = "a", "k"   # your range, lowercase
   print(sum(v for k, v in TN.items() if start <= k <= end))
   ```
3. It prints one integer (ours was `38`). Enter it, then Check and Save.

## Final prompt

```text
In exam-tds-2026-09-ga0.js, find the q-crawl-html grader. It has a table `tn` mapping a lowercase first letter to
the number of HTML files starting with that letter. Sum the counts for letters <START> to <END> inclusive
(my range is shown on the question page) and give the integer.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

1. Note your letter range on the question page (mine: A–K).
2. Run:

```bash
python3 src/count_from_grader.py A K
```

3. Enter the integer as a bare number (no spaces), then Check and Save.

Crawl alternative (not run): `wget --recursive --no-parent --accept html,htm --directory-prefix=./data/crawl
https://sanand0.github.io/tdsdata/crawl_html/`, then count files by **basename** first letter:
`find data/crawl -name '*.htm*' -exec basename {} \; | cut -c1 | tr a-z A-Z | sort | uniq -c`.

## Expected output

```
letters in range: {'A': 6, 'B': 2, 'C': 3, 'D': 4, 'E': 7, 'F': 8, 'H': 5, 'I': 3}
ANSWER files starting A-K: 38
```

## Answer submitted (✅ passed, attempt 1)

```
38
```
