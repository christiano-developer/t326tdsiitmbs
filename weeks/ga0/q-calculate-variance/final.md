# Final — q-calculate-variance

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
I have a JSON file containing an array of numbers. Write a short Python script that loads it, verifies
every element is a number (no strings, null or NaN), and prints the SAMPLE variance (N-1 denominator,
statistics.variance) rounded to 2 decimals. Also print the population variance for contrast, and
cross-check the sample variance with a manual sum((x-mean)^2)/(n-1).
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

1. Download `q-calculate-variance.json` from the exam page into `data/` (values are seeded per student).
2. Run:

```bash
python3 src/variance.py
# one-liner alternative:
python3 -c "import json,statistics;print(f'{statistics.variance(json.load(open(\"data/q-calculate-variance.json\"))):.2f}')"
```

Excel/Sheets equivalent: put the values in column A, then `=ROUND(VAR.S(A1:A1000), 2)`.

## Expected output

```
n=1000 min=24 max=64 mean=43.9610
population variance (N, wrong): 130.04
ANSWER sample variance (N-1): 130.17
```

## Answer submitted (✅ passed)

```
130.17
```

Enter the bare number with no surrounding whitespace.
