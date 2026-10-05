# Approaches — q-bug-hunter-property-based-testing

## Problem in one line

Write a `@given` property that **fails** on the case-insensitive buggy `dedupe_topics` and **passes** on
the exact-match reference, within the grader's 1000 generated examples.

## The bug

The buggy version dedupes on `str(item).lower()`, so `"A"` is dropped after `"a"`. The contract says only
**exact** duplicates are removed and casing is preserved, so `["a", "A"]` → expected `["a", "A"]`, but buggy gives `["a"]`.

## How the grader works (read from `exam-tds-2026-09-ga0.js`, hacking allowed)

- Variant seeded from `email#q-bug-hunter-property-based-testing` → 1 of 20 (sort / revenue overflow /
  leap day / dedupe / pagination / moving average). **Mine: `dedupe-3`, `dedupe_topics`.**
- Text pre-checks: the code must contain `@given(` and a `test_…(`.
- For each of buggy and reference: `exec(target_code)` then `exec(student_code)` into one namespace,
  run **every** callable named `test_*` (sorted by name), and stop at the first exception.
- Verdict: PASS only if buggy → `failed` **and** reference → `passed`.
- **It is not real Hypothesis.** A preamble installs a minimal stand-in as the `hypothesis` module
  (saved as [data/hypothesis_shim.py](data/hypothesis_shim.py)):
  - strategies: `integers, booleans, floats, sampled_from, text, lists, tuples, one_of, dates` only
  - strategy objects have **no `.map()` / `.filter()` / `.flatmap()`**; there's no `@composite`, `just`,
    `characters`, `from_regex`, `data` or `@example`
  - `@settings(max_examples=…)` is honoured, everything else in it is ignored; `assume()` works
  - fixed RNG seed `1337`, no shrinking, up to 1000 successful examples
    (default `text()` alphabet = letters + digits, max 12 chars; `lists()` max 10 items)

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "Write a Hypothesis property test" / "using `hypothesis`" | **Distractor** | It's a stand-in with a small API. Real-Hypothesis idioms (`.map`, `.filter`, `@composite`, `st.characters`) crash with `'_ExamStrategy' object has no attribute 'map'` (confirmed locally) |
| Skeleton comment "*import or use the buggy function name directly*" | **Distractor** | There is no module to import. The function is exec'd into the same namespace, so use `dedupe_topics` directly. An import fails setup |
| "up to 1000 generated examples" | Accurate | But it's seeded, so results are deterministic; no shrinking, so counterexamples aren't minimal |
| Hint "Strings that differ only by case" | Genuine | Correct failing region |
| Hidden text in this question's markup | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size. Nothing in this question (one hidden `d-none` list exists in a *different* GA0 question) |

## Options considered

| # | Approach | Pros | Cons | Verdict |
|---|----------|------|------|---------|
| A | `st.text()` lists + "no duplicates" property | Simple | Buggy output has no duplicates either → passes on buggy → **fails the question** (confirmed with a negative control) | rejected |
| B | `st.lists(st.text())` + full contract | General | Default alphabet is 62 chars, max 12 long: case-only collisions are rare, so it might miss the bug in 1000 runs | rejected |
| C | **`st.sampled_from` small alphabet of case pairs + full contract (first-occurrence exact dedupe)** | Case variants collide constantly; fails on attempt 1 | Narrow input domain (fine: the goal is isolating this bug) | **chosen** |

## Chosen: C

**Why:** the property states the *contract*, not examples. Expected = keep the first occurrence of each
exact value in order. The reference satisfies it for any input, so it can't false-fail. A tiny
alphabet of `a/A, b/B, x/X, Topic/topic/TOPIC` guarantees case-only collisions, so the buggy version fails immediately.

Extra assertions (`set(result) == set(items)`, no exact duplicates) restate the contract and also hold
for the reference.

## Gotchas

- Only use shim-supported strategies. No `.map/.filter`.
- Don't import `dedupe_topics`.
- Every `test_*` function runs. Any extra test must also pass on the reference (e.g. don't paste the
  known unit tests with a typo).
- Use hashable string elements: the reference uses a `set`.
- **Paste-safe code (attempt 1 rejected).** Long lines get wrapped when copied from the terminal or chat.
  Wrapping inside an f-string broke it: `f-string: single '}' is not allowed (<string>, line 18)`.
  Keep submissions free of f-strings and braces, keep lines under about 70 chars, and copy with
  `pbcopy < file`. The local replica can't catch this because it reads the file, not the pasted text.

## Verification

- `python3 src/run_grader.py` → **PASS**. Buggy fails at attempt 1 with input
  `['X','b','X','Topic','X','x','Topic','B']` → got `['X','b','Topic']`, expected `['X','b','Topic','x','B']`;
  reference passes all 1000.
- Negative controls (scratch files, not kept): option A → "did not discover the bug"; a `.map()` strategy →
  setup error `'_ExamStrategy' object has no attribute 'map'`. The replica reproduces the grader's messages.
- Exam "Check" button:
  - Attempt 1: ❌ setup error from a wrapped f-string (see Gotchas)
  - Attempt 2 (no f-strings, ≤ 61-char lines): ✅ passed (2026-10-06)
