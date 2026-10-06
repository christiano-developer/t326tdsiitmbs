# q-css-selectors-sum

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**CSS: Featured-Sale Discount Sum**: background on CSS selectors (basic, attribute, combinators; MDN; CSS Diner).

> **Case Study: eShopCo Promotional Audit.** eShopCo wants to verify that all featured sale products are correctly
> tagged in the front-end. Inspect the hidden product list below. Each `<li>` represents a product with its
> promotional classes and a `data-discount` (percentage).
>
> Using a single CSS selector that targets elements with both `featured` and `sale` classes, calculate the sum of
> their `data-discount` values.
>
> Sum of discounts on `.featured.sale` items:

Per-user variant: the 20-item list (classes + discounts) is seeded from the student email.

## Inputs / given data

- The hidden list is **in the exam page itself**: `<ul class="products d-none">` with 20 `<li class="…" data-discount="…">`.
  "eShopCo" is fictional; there's no external site.

## Final answer

```
293
```

8 matching items (#7, 8, 9, 10, 13, 14, 18, 19): 23 + 47 + 33 + 36 + 45 + 40 + 21 + 48 = 293.

## Status notes

- Regenerated with the grader's RNG and confirmed with Chrome's real `querySelectorAll('ul.products li.featured.sale')`
  (SUM=293, COUNT=8). Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/regenerate.mjs](src/regenerate.mjs) — rebuilds the hidden list from the seed and sums `.featured.sale`
