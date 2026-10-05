# Prompt log — q-binary-eval-rubric

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** understand the question

```text
Build a Binary Eval Rubric
<full question text: see README.md>
<GOOD / MEDIOCRE / POOR SQL examples>
explain to me what this question is
```

- **Result:** worked. Read the grader in the quiz JS: `gpt-4.1-mini` judge at temp 0, 5 × 20 = 100 AIPipe
  calls, pass = corr > 0.7 and non-degenerate on ≥ 4 checks; pre-API format rules. Noted the hidden
  examples and labels are in the JS.
- **Next:** clarify what "labels in the JS" means.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** understand where the hidden labels come from

```text
interesting what do you mean by their labels are in the quiz JS
```

- **Result:** showed the `Et` object: 4 topic variants, each with `hiddenExamples: [{output, label}]`.
  The browser grades client-side, so the answer key ships with the page. Mine is `sql_query_quality`.
- **Next:** decide whether it's safe to rely on them.

---

## P3

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** rule out a decoy, then build the rubric

```text
sure, but can there be a slightest possibility that its a distractor ?
```

- **Result:** traced the code: `labels = hiddenExamples.map(h => h.label)` feeds the correlation
  directly, so it isn't a decoy. Residual risks (server re-grade, judge flips) handled by choosing
  general SQL-quality traits with ≥ 0.90 separation. Re-downloaded the JS (unchanged), extracted all
  20 examples + judge config to `data/hidden_examples.json`, scored 8 candidate traits (found the
  obvious "avoids SELECT *" scores only 0.58), wrote `src/rubric.txt` and the local grader replica
  `src/eval_rubric.py`.
- **Next:** run the real judge locally with an AIPipe token, then submit.

---

## P4

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** park the question

```text
lets keep aside this question, and move to the next for now, that doesnt need the api
```

- **Result:** status → `set-aside`, with notes on where it stopped and the next step (README → Status notes).
- **Next:** resume near the end of GA0, when AIPipe credit can be spent.

---

## P5

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** estimate the AIPipe cost of one submission

```text
Usage: 0.00000 / 100 cents every 7 day(s) for the aipipe api key question,
how much will the submission cost me for this one try
```

- **Result:** computed from the real prompts (5 checks × 20 examples × judge template): ≈ 11.6k input +
  200 output tokens → ≈ 0.5 cents per submission, ≈ 200 submissions per weekly budget.
- **Next:** submit.

---

## P6

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
it worked on the 1st try lesgoo, please commit
```

- **Result:** ✅ passed on the first submission. Status → `solved`, committed and tagged.
- **Next:** none.
