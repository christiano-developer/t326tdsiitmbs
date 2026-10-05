# q-axis-scale-manipulation-repair

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-05 |
| Closed    | 2026-10-05 (passed on attempt 3) |

## Question

**Scale Manipulation Repair in Axis Design**

This chart uses a deceptive scale configuration. Your goal is to identify the manipulation,
quantify the distortion, and submit corrected chart HTML.

1. Identify the manipulation type and quantify distortion using a number or ratio.
2. Fix the axis configuration and submit corrected HTML.
3. Write one sentence describing what the corrected chart reveals that the broken chart hid.
4. Include your explanation as an HTML comment at the top of your submission, for example:
   `<!-- Quantification: ... Distortion: ... -->`

Per-user variant: chart title *"What does this chart claim to show? Quarterly uplift is dramatic"*,
line chart, `Revenue Index`, Jan–Aug, `scales.y.min = 825.62`, `beginAtZero: false`.

## Inputs / given data

- [data/original.html](data/original.html): broken chart HTML as given (Chart.js 4.4.1)
- [data/original-chart.png](data/original-chart.png): screenshot of the broken chart
- [data/data.csv](data/data.csv): underlying data table (Period, Series A)

## Final answer

✅ Passed (attempt 3). Paste the full contents of [src/corrected.html](src/corrected.html) (`pbcopy < src/corrected.html`).

- **Manipulation:** truncated y-axis (`scales.y.min = 825.62`, `beginAtZero: false`)
- **Quantification:** round(max / (max − axis min), 1) = 924.2 / 98.58 = **9.4** (must be the first number in the comment)
- **Distortion phrase:** "the truncated y-axis inflates tiny deltas by 9.4x"
- **Fix:** `"scales":{"y":{min: 0,"beginAtZero":true}}` (unquoted `min: 0` is required by the grader)
- **Insight:** with a zero baseline the index shows a steady, modest ~5% rise over eight months, not a dramatic uplift.
- Attempts 1–2 rejected: the comment's first number was 825.62. Details in [approaches.md](approaches.md#attempts).

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/check.py](src/check.py) — local replica of the grader
- `src/` — code · `data/` — inputs/outputs
