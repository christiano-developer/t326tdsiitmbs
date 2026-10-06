# Prompt log — q-sort-filter-json

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** filter + sort the catalog

```text
Sort and Filter a JSON Product Catalog
<JSON background + task + 100-product array: see README.md / data/products.json>
```

- **Result:** read the grader (parses JSON, compares fields by position; keeps price ≥ threshold). `src/sort_filter.py`
  → 44 items. Regenerated the seeded data with the grader's JS sort: matches the paste, check passes 44/44.
- **Next:** user submits.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
correct
```

- **Result:** ✅ passed on the first submission. Status → `solved`, committed and tagged.
- **Next:** none.
