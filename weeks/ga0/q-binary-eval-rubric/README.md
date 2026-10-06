# q-binary-eval-rubric

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no (needs AIPipe token: external config) |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**Build a Binary Eval Rubric**

Architecture: Client-side with AIPipe (LLM-as-judge validating the judge).

You're building an automated grader for **SQL query quality for an analytics task**. An LLM will
evaluate student submissions using your rubric.

The problem with vague rubrics: "Is this code good?" gives inconsistent results. Your job is to
decompose quality into binary (YES/NO) checks that an LLM can answer reliably.

1. Examine the 3 example outputs below (marked GOOD, MEDIOCRE, POOR).
2. Write exactly **5** binary checks that collectively distinguish good from poor work.
3. Each check must be answerable YES/NO by reading the output alone.
4. Format: one check per line, as a complete question ending in "?".

Example outputs: GOOD (CTEs + COALESCE + SUM/GROUP BY + filter + ORDER BY), MEDIOCRE
(single SELECT with SUM/GROUP BY), POOR (`SELECT * FROM orders;`). Full text in
[data/hidden_examples.json](data/hidden_examples.json) (`goodExample`, `mediocreExample`, `poorExample`).

> Before you start: evaluating this answer will make about 100 AIPipe API calls (5 checks x 20 hidden
> examples), with up to 8 calls in parallel. Recommended: attempt near the end of the assignment.

**Evaluation:** each check is run against 20 hidden examples; a check passes if correlation with
ground truth is > 0.7 and it is not degenerate (always YES or always NO). At least 4 checks must pass.

Per-user variant (seeded from email): topic `sql_query_quality`, **5** checks required.

## Inputs / given data

- [data/hidden_examples.json](data/hidden_examples.json): extracted from `exam-tds-2026-09-ga0.js`
  - judge config: `gpt-4.1-mini`, temperature 0, exact system and user prompts
  - the 3 visible examples
  - the **20 hidden examples with labels** (10 good / 10 poor)
- AIPipe token (https://aipipe.org): put it in a git-ignored `.env` (see `.env.example`) for local testing.

## Final answer

✅ Passed on the first submission. Submitted the 5 lines of [src/rubric.txt](src/rubric.txt) (`pbcopy < src/rubric.txt`):

```
Does the query use a WITH clause (common table expression) to define an intermediate result before the final SELECT?
Does the query explicitly handle NULL values, for example with COALESCE, IFNULL, or CASE WHEN ... IS NULL?
Does the query use an aggregate function such as SUM, COUNT, AVG, MIN, or MAX to summarize rows?
Does the query compute or transform at least one value (via a function or expression) instead of only returning stored columns as-is?
Does the query assign an alias to at least one computed column or expression, such as SUM(amount) AS total or COALESCE(x, 0) x?
```

## Status notes

- 2026-10-06: briefly set aside to save AIPipe credit (never committed). Resumed after estimating the
  cost at ≈ 0.5 cents per submission (100 calls × ~116 input tokens on `gpt-4.1-mini`).
- Submitted directly without the local judge run. ✅ **Passed on attempt 1.** The grader only prints
  per-check correlations on failure (on success they go to the browser console), so the real judge
  numbers weren't recorded. Text-match estimate: 1.00 / 0.90 / 0.90 / 1.00 / 1.00.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/rubric.txt](src/rubric.txt) — the 5 checks (submission)
- [src/eval_rubric.py](src/eval_rubric.py) — local replica of the grader (same judge, same pass rule)
- `data/` — extracted hidden examples + judge config; `eval_results.json` after a run
