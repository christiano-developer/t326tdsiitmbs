# q-rename-files-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 1 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

Download `files_to_reorganize.zip` (30 text files in nested dirs). Move each file to
`{category}/{path-with-dashes}-{filename}`, where category is the first line matching `category: …`.
Then run `find . -type f | LC_ALL=C sort | sha256sum` and submit the hash.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

Files seeded from `email#q-rename-files-server<version>`. Paths and categories include Unicode, spaces, accents.

## Final answer

```
621877e7d4c18e9c500c752d8c7c7e2c05c1ad3cc1cecd9e8f962a3de10b1451
```

## Status notes

Checked ✅ in Chrome on 2026-10-18. Marked solved at the user\'s request before the GA1 page was saved.
`data/manifest.json` keeps only path → category (enough to reproduce the hash), not the file bodies.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
