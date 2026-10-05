# Final — q-binary-eval-rubric

> Goal: the answer can be reproduced from this file alone.
> Status: ✅ passed on the first submission (2026-10-06).

## Final prompt

Works in one pass in any capable LLM, given the extracted examples. Replace `<EXAMPLES_JSON>` with the
`hiddenExamples` array for your variant (topic and check count are seeded per student).

```text
I need N binary YES/NO rubric checks for an LLM judge (gpt-4.1-mini, temperature 0) that grades
<TOPIC>. Below are 20 labelled examples (label 1 = good, 0 = poor):

<EXAMPLES_JSON>

Requirements:
- Exactly N checks, one per line, each a complete question ending in "?", each at least 24 characters,
  no duplicates.
- Each check must be answerable YES/NO from the text alone, using concrete observable features
  (name the keywords/constructs to look for). Nothing subjective like "is it good/readable".
- For each check, count how many good and poor examples would get YES. Keep only checks where nearly
  all good examples are YES and nearly all poor examples are NO (Pearson corr with labels >= 0.9).
  No check may be YES for all 20 or NO for all 20.
- Prefer traits that reflect genuine quality and would generalize beyond these 20 examples.
- Avoid checks that half the poor examples would also pass.
Output the N checks only, one per line.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5). Data and judge config extracted from
  `exam-tds-2026-09-ga0.js`, trait separation scored with python3.

## Reproduction steps

1. Download the quiz JS and extract your variant's examples (see `CMDS.md` → Exam submissions). The
   extraction for `sql_query_quality` is saved in `data/hidden_examples.json`.
2. Write the checks into `src/rubric.txt` (one per line).
3. Validate the format (no API calls):

```bash
python3 src/eval_rubric.py --validate
```

4. Run the real judge locally (~100 AIPipe calls). The token goes in a git-ignored `.env`:

```bash
cp .env.example .env        # then set AIPIPE_TOKEN=...
python3 src/eval_rubric.py  # writes data/eval_results.json
```

5. If ≥ 4 checks pass with comfortable margins (corr ≥ 0.85), copy and submit:

```bash
pbcopy < src/rubric.txt
```

Paste into the exam, Check, and enter the AIPipe token when prompted. Then Save.

## Expected output

```
Format OK: 5 checks
#1..#5 PASS (corr ≈ 0.9–1.0 each)
5/5 checks passed -> PASS (need >= 4)
```

The exam passed on attempt 1. Per-check judge correlations are only shown on failure, so they weren't captured.

## Answer submitted (✅ passed, attempt 1)

```
Does the query use a WITH clause (common table expression) to define an intermediate result before the final SELECT?
Does the query explicitly handle NULL values, for example with COALESCE, IFNULL, or CASE WHEN ... IS NULL?
Does the query use an aggregate function such as SUM, COUNT, AVG, MIN, or MAX to summarize rows?
Does the query compute or transform at least one value (via a function or expression) instead of only returning stored columns as-is?
Does the query assign an alias to at least one computed column or expression, such as SUM(amount) AS total or COALESCE(x, 0) x?
```
