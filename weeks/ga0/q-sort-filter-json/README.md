# q-sort-filter-json

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**Sort and Filter a JSON Product Catalog**: background: JSON types, nesting, validation, JSON Lines, tools (JSONLint,
jq, JSON Schema), Python `json` / pandas.

> You're auditing an e-commerce catalog. Below is a JSON array of 100 products, each with a category, price and name.
> Filter out any product with price < **114.97**. Sort the remaining items by category (A→Z), then price
> (highest→lowest), then name (A→Z). Paste the final array as a single minified JSON string.

Per-user variant: the catalog and threshold are seeded from the student email.

## Inputs / given data

- [data/products.json](data/products.json): the 100 products as shown on the page.

## Final answer

✅ Passed on the first submission (grader check 44/44 locally). Paste [data/answer.min.json](data/answer.min.json) (`pbcopy < data/answer.min.json`).
44 products: Apparel 8, Books 8, Electronics 11, Home 10, Toys 7.

## Status notes

- Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md)
- [src/sort_filter.py](src/sort_filter.py) — filter + sort + minify
- [src/grader_check.mjs](src/grader_check.mjs) — regenerates the seeded data and runs the grader's exact comparison
