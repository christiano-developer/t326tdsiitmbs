# q-bug-hunter-property-based-testing

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no (runs in-browser Pyodide; no API) |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 2) |

## Question

**The Bug Hunter (Property-Based Testing)**

Architecture: In-browser Pyodide execution. Your submitted Python code is executed against both a buggy
implementation and a reference implementation without calling any external runner URL.

Hand-crafted unit tests often miss edge cases. Your goal is to write a Hypothesis property test that
automatically discovers a counterexample for this seeded function variant: **Topic Dedupe**.

Buggy function:

```python
def dedupe_topics(items):
  seen = set()
  out = []
  for item in items:
    key = str(item).lower()
    if key in seen:
      continue
    seen.add(key)
    out.append(item)
  return out
```

What the function should do: *Remove only exact duplicates while preserving first occurrence order and original casing.*

Known passing unit tests (these do not catch the bug):

```python
def test_exact_duplicate_removal():
  assert dedupe_topics(["a", "a", "b"]) == ["a", "b"]
  assert dedupe_topics([]) == []
  assert dedupe_topics(["x", "y"]) == ["x", "y"]
```

Your task:
1. Write a `@given`-decorated test function using `hypothesis`.
2. Submit complete Python test code (imports + test function[s]).
3. We run your test for up to 1000 generated examples. You pass only if your property fails on buggy
   code but passes on the reference implementation.

Hint: known failing input region: *Strings that differ only by case, like `['A', 'a']` or `['X', 'x', 'X']`.*

Per-user variant (seeded from email): `dedupe-3 / Topic Dedupe` (`dedupe_topics`), one of 20 variants.

## Inputs / given data

- [data/variant.py](data/variant.py): buggy + reference implementations, verbatim from the quiz JS
- [data/hypothesis_shim.py](data/hypothesis_shim.py): the grader's **own Hypothesis stand-in**
  (not the real library), verbatim from the quiz JS

## Final answer

✅ Passed (attempt 2; attempt 1 rejected, see Status notes). Copy **from the file**: `pbcopy < src/test_dedupe.py`.

```python
from hypothesis import given, strategies as st

# dedupe_topics is provided by the grader (do not import it).
# Case pairs so that "a"/"A"-style variants appear often.
CASE_PAIRS = ["a", "A", "b", "B", "x", "X", "Topic", "topic"]


@given(st.lists(st.sampled_from(CASE_PAIRS), max_size=8))
def test_dedupe_removes_only_exact_duplicates(items):
    result = dedupe_topics(items)

    # Contract: first occurrence of each exact value,
    # original order and casing.
    expected = []
    for item in items:
        if item not in expected:
            expected.append(item)

    assert result == expected
    assert set(result) == set(items)
    assert len(result) == len(set(result))
```

## Status notes

- Attempt 1 ❌ `Test setup error: Failed to import/define tests: f-string: single '}' is not allowed
  (<string>, line 18)`. Line 18 was an 86-char f-string assert message. The pasted copy got wrapped and
  split inside the f-string (the file itself compiles). Kept as [data/attempt-1-rejected.py](data/attempt-1-rejected.py).
- Attempt 2: no f-strings or braces, max line length 61. Local replica **PASS**. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/test_dedupe.py](src/test_dedupe.py) — submission
- [src/run_grader.py](src/run_grader.py) — local replica of the grader (uses the exam's shim)
