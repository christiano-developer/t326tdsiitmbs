# Final — q-bug-hunter-property-based-testing

> Goal: the answer can be reproduced from this file alone.

## Final prompt

Works in one pass for any of the 20 seeded variants. Replace the bracketed parts with your variant's text.

```text
Write a property-based test for an auto-grader. The grader does NOT use real Hypothesis: it installs a
minimal stand-in where `hypothesis.strategies` only has integers, booleans, floats, sampled_from, text,
lists, tuples, one_of, dates. Strategy objects have no .map/.filter, and there's no @composite/just/characters.
It runs with a fixed seed for up to 1000 examples, with no shrinking.

The function under test is already defined in the same namespace as <FUNCTION_NAME>. Do NOT import it.

Buggy implementation:
<BUGGY_CODE>

Contract: <CONTRACT_TEXT>
Known failing input region: <HINT>

Write complete Python code: `from hypothesis import given, strategies as st` plus ONE test_* function
decorated with @given that:
- generates inputs concentrated in the failing region (prefer sampled_from over a small, hand-picked
  alphabet/value set so the bug triggers within the first few examples),
- asserts the full contract by computing the expected result independently (not just a weak invariant
  the buggy code also satisfies),
- would pass for a correct implementation on every generated input.
Formatting: no f-strings or curly braces, every line under 70 characters (the code is pasted into a
textarea, and wrapped f-strings break).
Output only the code.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5). Grader + shim read from `exam-tds-2026-09-ga0.js`;
  verified with `src/run_grader.py`.

## Reproduction steps

1. Copy the variant's buggy/reference code into `data/variant.py`, and the shim (`Ra` string in the quiz JS)
   into `data/hypothesis_shim.py` (both already saved for `dedupe-3`).
2. Write the test into `src/test_dedupe.py` (below).
3. Run the replica (no dependencies, no real Hypothesis needed):

```bash
python3 src/run_grader.py
```

4. Copy **from the file** (never from terminal or chat output): `pbcopy < src/test_dedupe.py`, then Check and Save.

## Expected output

```
buggy  : {"status": "failed", "test": "test_dedupe_removes_only_exact_duplicates", "error": "", "counterexample": {"args": [["X", "b", "X", "Topic", "X", "x", "Topic", "B"]], "kwargs": {}, "attempt": 1}}
correct: {"status": "passed", "tests": ["test_dedupe_removes_only_exact_duplicates"]}
PASS: property fails on buggy code and passes on the reference implementation
```

## Answer submitted (✅ passed, attempt 2)

[src/test_dedupe.py](src/test_dedupe.py), copied with `pbcopy`.

> History: attempt 1 hit a setup error because a long f-string was wrapped while pasting (see approaches.md → Gotchas).
