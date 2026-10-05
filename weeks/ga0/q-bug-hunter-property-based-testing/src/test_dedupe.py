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
