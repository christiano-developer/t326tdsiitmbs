# Final — q-unicode-data

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-unicode-data](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-unicode-data)

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

1. Open your TDS folder for this GA (create `TDS/GA0` if you don't have one) and open a terminal in it.
2. Download `q-unicode-data.zip`, unzip it, and `cd` into the folder with `data1.csv`, `data2.csv` and `data3.txt`.
3. Create `sum.py` there. Put your question's three symbols in `TARGETS` (ours were € ˆ ”), then run `python3 sum.py`:
   ```python
   TARGETS = {"\u20ac", "\u02c6", "\u201d"}   # escapes avoid look-alike characters
   FILES = [("data1.csv", "cp1252", ","), ("data2.csv", "utf-8", ","), ("data3.txt", "utf-16", "\t")]
   total = 0
   for name, enc, sep in FILES:
       for line in open(name, encoding=enc).read().splitlines()[1:]:
           if line:
               sym, val = line.split(sep, 1)
               if sym in TARGETS:
                   total += int(val)
   print(total)
   ```
4. It prints one integer (ours was `40909`). Enter it, then Check and Save.

## Final prompt

```text
Python: read data1.csv as cp1252, data2.csv as utf-8 (comma-separated) and data3.txt as utf-16 (tab-separated). Each
has header symbol,value. Sum value where symbol is one of "€", "ˆ", "”" (use escapes, not pasted
characters). Split each line on the first separator only; don't use a CSV quoting parser.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

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
