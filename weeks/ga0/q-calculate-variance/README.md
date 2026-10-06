# q-calculate-variance

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed) |

## Question

**Calculate variance**: *Quality Control Analytics for PrecisionParts Manufacturing* (topic label:
"Spreadsheet: Excel, Google Sheets").

PrecisionParts measures critical dimensions of parts in each production run and uses variance to detect
process drift, maintain quality standards, predict maintenance and tune machine settings.

Your task:
- Download `q-calculate-variance.json`. It contains an array of 1000 measurements from the latest production run.
- Calculate the **sample variance (N-1 denominator)** using Python, Excel, or JavaScript. The data contains no
  missing values. Write the answer rounded to 2 decimal places, e.g. 123.45.
- Note: in Python use `statistics.variance(data)`; in Excel use `VAR.S()`.

What is the sample variance of these measurements?

Per-user variant: 1000 integers seeded from the student email.

## Inputs / given data

- [data/q-calculate-variance.json](data/q-calculate-variance.json): downloaded from the exam page (1000 ints, 24–64)

## Final answer

```
130.17
```

## Status notes

- ✅ Passed. The first entry was rejected because of stray whitespace in the typed value; `130.17` re-entered cleanly was accepted.
- Data verified as the exact seeded array for the exam login (`src/regenerate.mjs`).

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/variance.py](src/variance.py) — computes the answer with sanity checks
- [src/regenerate.mjs](src/regenerate.mjs) — regenerates the seeded data with the grader's RNG (verification)
