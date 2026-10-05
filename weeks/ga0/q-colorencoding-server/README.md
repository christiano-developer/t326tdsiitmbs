# q-colorencoding-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**Fix the Color Encoding Mismatch**

The chart below uses the wrong color scheme for its data type. Color is a data encoding: choosing the
wrong scheme actively misleads viewers. Your job is to diagnose the problem, explain it, and fix the chart.

Broken chart: **Website Traffic by Source**. Monthly visits (thousands) by traffic source: Organic, Paid,
Social, Direct, Email. Bar chart, data `[85, 42, 33, 67, 18]`, palette = light-to-dark orange ramp.

Your task (all three parts required):
1. **Explain the mismatch:** what does the current color scheme incorrectly imply about the data?
2. **Name the correct scheme type** (sequential, categorical, or diverging) and explain why it fits.
3. **Fix the chart:** submit corrected HTML using an appropriate palette. The explanation must appear as an
   HTML comment or visible text inside the submitted HTML.

Hint: the categories have no inherent numeric or rank order.

Verification criteria (as stated): sequential L* monotonic; categorical all pairwise CIEDE2000 ≥ 30;
diverging midpoint L* ≥ 80 and endpoints L* ≤ 65; no rainbow (hue span ≤ 270° across ≥ 6 colours); scheme
word present; mismatch explained.

The page also shows a colour-scheme primer that suggests Tableau 10 for categorical data.

## Inputs / given data

- [data/original.html](data/original.html): broken chart HTML as given
- [data/original-chart.png](data/original-chart.png) / [data/corrected-chart.png](data/corrected-chart.png): headless-Chrome renders

## Final answer

✅ Passed on the first submission. Copy **from the file**: `pbcopy < src/corrected.html`.

- **Mismatch:** a sequential light-to-dark ramp on nominal categories falsely implies traffic sources have a
  natural progression or hierarchy (Organic "least" … Email "most"), contradicting the bar heights.
- **Correct scheme:** **categorical**. Unordered groups need distinct hues of equal visual weight.
- **Palette:** Okabe-Ito `#0072b2 #d55e00 #009e73 #cc79a7 #f0e442` (min pairwise CIEDE2000 = 37.0).
- **These are the only hex colours in the file.** The CSS was converted to `rgb()` / `white`.

## Status notes

- Local grader replica (`src/check.py`): **PASS**. Exam Check ✅ **passed on attempt 1**.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/corrected.html](src/corrected.html) — submission
- [src/check.py](src/check.py) — local replica of the grader (exact CIEDE2000 port)
