# Final — q-sort-filter-json

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-sort-filter-json](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-sort-filter-json)

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

1. Open your TDS folder for this GA (create `TDS/GA0` if you don't have one) and open a terminal in it.
2. Copy the JSON array from the question into a file `products.json`. Note your price threshold.
3. Create `sort.py`, set `THRESHOLD`, and run `python3 sort.py`:
   ```python
   import json
   THRESHOLD = 114.97   # yours from the question
   items = [p for p in json.load(open("products.json")) if p["price"] >= THRESHOLD]
   items.sort(key=lambda p: (p["category"], -p["price"], p["name"]))
   print(json.dumps(items, separators=(",", ":")))
   ```
4. It prints one line of minified JSON. Copy all of it into the answer box, then Check and Save.

## Final prompt

```text
Given this JSON array of products (category, price, name), keep items with price >= <THRESHOLD>, sort by category
A→Z, then price high→low, then name A→Z, and output the result as minified JSON. Give a Python script that does it.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
python3 src/sort_filter.py 114.97 data/products.json > data/answer.min.json
# or: jq -c 'map(select(.price >= 114.97)) | sort_by(.category, -.price, .name)' data/products.json
pbcopy < data/answer.min.json
```

## Expected output

44 items, starting `[{"category":"Apparel","price":194.45,"name":"Mini Kit"},...` and ending
`...{"category":"Toys","price":121.44,"name":"Mini Device"}]`.

## Answer submitted (✅ passed, attempt 1)

[data/answer.min.json](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-sort-filter-json/data/answer.min.json), copied with `pbcopy`.
