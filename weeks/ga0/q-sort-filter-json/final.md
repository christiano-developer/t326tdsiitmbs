# Final — q-sort-filter-json

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Given this JSON array of products (category, price, name), keep items with price >= <THRESHOLD>, sort by category
A→Z, then price high→low, then name A→Z, and output the result as minified JSON. Give a Python script that does it.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

```bash
python3 src/sort_filter.py 114.97 data/products.json > data/answer.min.json
# or: jq -c 'map(select(.price >= 114.97)) | sort_by(.category, -.price, .name)' data/products.json
pbcopy < data/answer.min.json
```

## Expected output

44 items, starting `[{"category":"Apparel","price":194.45,"name":"Mini Kit"},...` and ending
`...{"category":"Toys","price":121.44,"name":"Mini Device"}]`.

## Answer submitted (✅ passed, attempt 1)

[data/answer.min.json](data/answer.min.json), copied with `pbcopy`.
