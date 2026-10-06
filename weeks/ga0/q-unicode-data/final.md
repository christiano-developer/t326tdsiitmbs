# Final — q-unicode-data

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Python: read data1.csv as cp1252, data2.csv as utf-8 (comma-separated) and data3.txt as utf-16 (tab-separated). Each
has header symbol,value. Sum value where symbol is one of "€", "ˆ", "”" (use escapes, not pasted
characters). Split each line on the first separator only; don't use a CSV quoting parser.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

```bash
unzip q-unicode-data.zip -d data/extracted
python3 src/sum_symbols.py data/extracted/q-unicode-data
```

## Expected output

```
data1.csv  cp1252  rows=500 matches=56 subtotal=13010
data2.csv  utf-8   rows=500 matches=51 subtotal=12385
data3.txt  utf-16  rows=500 matches=58 subtotal=15514
ANSWER 40909
```

## Answer submitted (✅ passed, attempt 1)

```
40909
```
