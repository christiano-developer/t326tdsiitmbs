# Final — q-calculate-variance

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-calculate-variance](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-calculate-variance)

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

1. Open your TDS folder for this GA (create `TDS/GA0` if you don't have one) and open a terminal in it.
2. Download `q-calculate-variance.json` from the question into that folder.
3. Create `variance.py` with this code:
   ```python
   import json, statistics
   data = json.load(open("q-calculate-variance.json"))
   print("%.2f" % statistics.variance(data))   # sample variance (n-1), not population
   ```
4. Run `python3 variance.py`. It prints one number like `130.17`. That's your answer.
5. Type it into the box with no spaces, then Check and Save.

Google Sheets alternative: paste the values in column A, then use `=ROUND(VAR.S(A:A), 2)`.

## Final prompt

```text
I have a JSON file containing an array of numbers. Write a short Python script that loads it, verifies
every element is a number (no strings, null or NaN), and prints the SAMPLE variance (N-1 denominator,
statistics.variance) rounded to 2 decimals. Also print the population variance for contrast, and
cross-check the sample variance with a manual sum((x-mean)^2)/(n-1).
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

1. Download `q-calculate-variance.json` from the exam page into [`data/`](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-calculate-variance/data) (values are seeded per student).
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
