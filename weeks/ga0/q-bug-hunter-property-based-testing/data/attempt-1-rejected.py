from hypothesis import given, strategies as st

# dedupe_topics is injected into this namespace by the grader (do not import it).
# Small alphabet with upper/lower pairs, so case-only variants like "a"/"A" appear often.
CASE_PAIRS = ["a", "A", "b", "B", "x", "X", "Topic", "topic", "TOPIC"]


@given(st.lists(st.sampled_from(CASE_PAIRS), min_size=0, max_size=8))
def test_dedupe_removes_only_exact_duplicates(items):
    result = dedupe_topics(items)

    # Contract: keep the first occurrence of each exact value, in original order and casing.
    expected = []
    for item in items:
        if item not in expected:
            expected.append(item)

    assert result == expected, f"input={items!r} got={result!r} expected={expected!r}"
    # Every distinct input value survives (case variants are different values).
    assert set(result) == set(items)
    # No exact duplicates remain.
    assert len(result) == len(set(result))
