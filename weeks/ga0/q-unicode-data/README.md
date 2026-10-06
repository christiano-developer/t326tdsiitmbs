# q-unicode-data

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**Process files with different encodings**: background: *Unicode* (ASCII, UTF-8/16/32, BOM, chardet, pandas encodings).

> Download and process the files in `q-unicode-data.zip`, which contains three files with different encodings:
> - `data1.csv`: CSV file encoded in CP-1252
> - `data2.csv`: CSV file encoded in UTF-8
> - `data3.txt`: Tab-separated file encoded in UTF-16
>
> Each file has 2 columns: symbol and value. Sum up all the values where the symbol matches **€ OR ˆ OR ”** across
> all three files. What is the sum of all values associated with these symbols?

Per-user variant: rows and target symbols seeded from the student email.

## Inputs / given data

- [data/extracted/q-unicode-data/](data/extracted/q-unicode-data/): `data1.csv` (CP-1252, CRLF), `data2.csv` (UTF-8),
  `data3.txt` (UTF-16 LE with BOM `FF FE`, tab-separated); 500 rows each.

## Final answer

```
40909
```

data1 13010 + data2 12385 + data3 15514.

## Status notes

- Python result and the grader's seeded formula agree. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md)
- [src/sum_symbols.py](src/sum_symbols.py) — decodes each file with its encoding and sums the target symbols
