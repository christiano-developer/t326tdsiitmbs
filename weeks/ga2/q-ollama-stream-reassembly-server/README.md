# q-ollama-stream-reassembly-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 1.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Recover a fragmented LLM stream (1.5 marks)**

Your LLM client treats every network chunk as a complete JSON object and sometimes corrupts Unicode. Reconstruct these three independent native Ollama-style NDJSON streams.

Each array contains ordered hex-encoded byte chunks, not JSON records. Decode the hex, preserve UTF-8 characters across chunk boundaries, buffer complete newline-delimited JSON records, and concatenate only their `response` strings. Ignore `thinking`.

- Include any response text on the first `done: true` record, then stop with `complete: true`.
- On an error record, preserve earlier response text, set that error string and stop with `complete: false`. Ignore subsequent records.
- At transport EOF without a terminal record, use `complete: false` and `error: null`. Ignore any incomplete trailing JSON record.
- Preserve spaces, escaped newlines and Unicode exactly. Use `error: null` unless an error record was encountered.

Serve `{"A":{"text":"...","complete":true,"error":null},"B":{...},"C":{...}}` at a public URL (raw JSON, no auth, no HTML wrapper, < 10 s, <= 64 KiB). The exam server GETs it; CORS not required.

## Inputs / given data

Hex chunks (seeded per email; tag `job-48c9d2a0`) saved in [data/chunks.json](data/chunks.json).

## Final answer

```
https://<your-project>.vercel.app/answer.json
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [deploy.md](deploy.md) — commands + guide to deploy / boot / configure
- `src/` — code · `data/` — inputs/outputs
