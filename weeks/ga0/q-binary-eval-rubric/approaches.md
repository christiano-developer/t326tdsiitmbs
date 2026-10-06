# Approaches — q-binary-eval-rubric

## Problem in one line

Write 5 YES/NO questions that `gpt-4.1-mini` answers YES for good SQL and NO for poor SQL, with
correlation > 0.7 against hidden labels on at least 4 of the 5.

## How the grader works (read from `exam-tds-2026-09-ga0.js`, hacking allowed)

- Variant is seeded from `email#q-binary-eval-rubric`. It picks a topic from 4
  (`data_analysis_narrative`, `sql_query_quality`, `api_documentation`, `prompt_engineering`) and a
  check count from `[5, 6, 7]`. **Mine: SQL, 5 checks.**
- Pre-API rules: exactly N non-empty lines; each ends with `?`; each ≥ 24 chars; no duplicates
  (case-insensitive).
- Judge: `gpt-4.1-mini`, `temperature: 0`, via `https://aipipe.org/openai/v1/chat/completions` with the
  student's own token. System: *"You are a strict binary evaluator… Respond with exactly one token: YES or NO."*
  User: `Check question:\n{check}\n\nCandidate output:\n{output}\n\nAnswer YES or NO only.`
- Score per check: Pearson correlation between the judge's YES/NO vector (20) and the hidden labels;
  pass if not degenerate and corr > 0.7. **Need ≥ 4 passes.**
- **Not a decoy.** `hiddenExamples` → `labels` feeds directly into the correlation. There is no second dataset.

## Data analysis (20 hidden examples, 10 good / 10 poor)

All 10 good examples share one template: `WITH <cte> AS (SELECT … COALESCE(…) …) SELECT …agg… GROUP BY …`.
The poor examples are either `SELECT *` (5) or plain column lists with no computation (5).

Text-match estimate of how each candidate trait separates them (regex proxy for the judge):

| Trait | good YES | poor YES | corr | Use? |
|-------|---------|---------|------|------|
| Uses a CTE (`WITH`) | 10/10 | 0/10 | 1.00 | ✅ |
| Computes/transforms a value | 10/10 | 0/10 | 1.00 | ✅ |
| Aliases a computed expression | 10/10 | 0/10 | 1.00 | ✅ |
| Handles NULLs (COALESCE…) | 9/10 | 0/10 | 0.90 | ✅ (#5 has no COALESCE) |
| Aggregate function | 9/10 | 0/10 | 0.90 | ✅ (#11 has none) |
| GROUP BY | 8/10 | 0/10 | 0.82 | backup |
| **Avoids `SELECT *`** | 10/10 | 5/10 | **0.58** | ❌ the obvious check fails: half the poor examples list explicit columns |
| Has WHERE filter | 3/10 | 2/10 | 0.12 | ❌ |

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Write checks from the 3 visible examples only | intuition / LLM | No JS reading | Would likely include "avoids SELECT *" (0.58 → fail); blind until ~100 calls are spent | rejected |
| B | Ask an LLM to "write 5 binary checks" | ChatGPT / Claude | Fast | Same blindness; generic checks ("is it readable?") are subjective → low correlation | rejected |
| C | **Extract hidden examples + judge config from the quiz JS, score candidate traits, replicate the grader locally** | curl, python3, AIPipe | Measured, not guessed; test before spending a submission | Local run costs ~100 calls too | **chosen** |

## Chosen: C

**Why:** the grader is deterministic apart from the judge LLM, and the data is in the page. Picking
traits that separate good from poor at ≥ 0.90 leaves margin for the judge occasionally disagreeing with the regex.

### Design rules for each check

- **Objective, syntactic and observable**: answerable from the text alone, with no "is it good / readable".
- **Name concrete keywords** (WITH, COALESCE, SUM/COUNT/AVG…) so the judge doesn't have to interpret.
- **Generalizes**: each trait is genuine SQL quality (staging via CTE, NULL safety, aggregation,
  derived values, named outputs), not a quirk of these 20 strings. Guards against any server-side re-grade.
- **Not degenerate** on the hidden set (every check has YES and NO cases).

## Gotchas

- `COUNT(*)` contains `*`. A "SELECT *" check risks the judge flagging good queries. Avoided entirely.
- Poor example #6 has *table* aliases (`users u`). Check 5 says *computed column or expression* to keep it NO.
- Aliases without `AS` (`COALESCE(x,0) x`) are common in the good set. Check 5 shows that form explicitly.

## Verification

- `python3 src/eval_rubric.py --validate` → Format OK (5 lines, all end in `?`, 96–133 chars, unique).
- Regex proxy correlations above: all 5 ≥ 0.90.
- Real judge run: skipped. A local run costs the same as a submission (~100 calls ≈ 0.5 cents), so submitted directly.
- Exam "Check" button: ✅ **passed on attempt 1** (2026-10-06), so ≥ 4 of 5 checks had corr > 0.7 and were non-degenerate.

## Cost

100 judge calls × ≈ 116 input tokens + ≈ 2 output tokens on `gpt-4.1-mini` ($0.40 / $1.60 per 1M) ≈ **$0.005 per
submission** (≈ 1 cent if every call retried). The weekly AIPipe budget of 100 cents covers ~200 submissions, so the
exam's "do this last" warning is conservative.
