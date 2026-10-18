# q-csv-sales-analysis-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 1 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**TechMart Electronics.** Download `sales_data.zip`, load `sales_data.csv`
(`date,city,product,quantity,price`), and compute total revenue = SUM(quantity × price) for **<city>** in
**<month> 2025**. Round to the nearest integer.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

CSV, city and month seeded from `email#q-csv-sales-analysis-server` (100–149 rows). Dates are `2025-Mon-D`.

## Final answer

Bangalore, May 2025:

```
12010
```

## Status notes

Checked ✅ in Chrome on 2026-10-18. Marked solved at the user\'s request before the GA1 page was saved.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
