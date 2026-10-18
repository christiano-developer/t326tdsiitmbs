# q-cosine-similarity-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 1.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**VecSearch Labs.** Download your task JSON: 250 documents and 10 queries, each with a precomputed
64-dim embedding (unit-normalised). For each query return the top 5 doc_ids by cosine similarity,
descending; ties → smaller doc_id first.

Answer: `{"Q001": ["D...", ×5], …}`

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

`q-cosine-similarity-server.json`, generated in the browser from seed `tds-2026-05-ga3-cosine-sim-client-v1#<email lower>#<version>`.

## Final answer

Top-5 doc_ids per query (full JSON in [data/answer.json](data/answer.json)):

```
{"Q001": ["D000036","D000131","D000236","D000196","D000186"], …, "Q010": ["D000055","D000220","D000235","D000200","D000195"]}
```

## Status notes

Checked ✅ (10/10) in Chrome on 2026-10-18. Marked solved at the user\'s request before the GA1 page was saved.
The 525 KB task file isn't in `data/`; download it from the exam page to rerun `src/cosine.mjs`.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
