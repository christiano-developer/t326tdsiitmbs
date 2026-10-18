# q-broken-json-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 1 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-09 |
| Closed    | 2026-10-18 |

## Question

A critical JSON file was corrupted (~N syntax errors). Download `broken_json.zip`
(`broken.json` + `README.md`), fix all syntax errors, validate, and paste the entire fixed JSON.
Only fix syntax — don't change values or delete records.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

`broken.json`: 300 records seeded from `email#q-broken-json-server<version>`; 20 corruption attempts.

## Final answer

The repaired JSON (300 records), pretty-printed: output of [src/fix.mjs](src/fix.mjs), identical in content to [data/fixed.json](data/fixed.json).

```
[
  {
    "id": "record_00000",
    "name": "Entry 0",
    "value": 9548,
    …
```

## Status notes

Checked ✅ in Chrome on 2026-10-18. Marked solved at the user\'s request before the GA1 page was saved.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
