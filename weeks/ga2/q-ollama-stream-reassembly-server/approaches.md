# Approaches — q-ollama-stream-reassembly-server

## Problem in one line

Turn three arrays of hex byte-chunks into `{text, complete, error}` per stream using Ollama NDJSON streaming semantics, and host the JSON publicly.

## Grader (from quiz JS)

- Data generator `be(email)` in `exam-tds-2026-09-ga2.js`: tag `job-<fnv1a(email) hex>`; three fixed record lists:
  - A: `Report <tag>: ` / `{thinking, response:""}` / `café\n` / `Ready ✓` with `done:true` → full text, complete.
  - B: `Partial <tag>` then a truncated `{"response":"unfinished` (no newline) → EOF case.
  - C: `Draft <tag>` / `{error:"model unloaded"}` / `IGNORE` with `done:true` → error case.
- Chunking: 11 + i%13 bytes, but a chunk is cut right after any byte ≥ 0xC0 (UTF-8 lead byte), so multibyte chars are always split across chunks (`c3|a9`, `e2|9c93`).
- Checking is server-side (`/backendVerify` GETs the URL); exact comparison of the JSON is assumed.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "treats every network chunk as a complete JSON object" | Distractor | Chunks are arbitrary byte slices; must buffer to `\n`. |
| `thinking` field | Genuine | Ignore it; its record has `response: ""`. |
| `IGNORE` record after the error in C | Trap | Stop at the error record. |
| Trailing `{"response":"unfinished` in B | Trap | Incomplete record → drop it. |
| `\n` in A | Genuine | It is an escaped newline inside the JSON string → a real newline in `text`. |

Scanned the question HTML for hidden elements/comments: none found.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Python incremental UTF-8 decoder + newline buffer | python3 | General, mirrors a real streaming client | — | chosen |
| B | Hand-decode the hex | — | — | Error-prone with split UTF-8 | rejected |
| C | Read expected values from the generator in quiz JS | DevTools | Instant cross-check | Not a method | used as verification |

## Chosen: A

**Why:** reusable for any Ollama/NDJSON stream; `codecs.getincrementaldecoder("utf-8")` holds partial multibyte sequences between chunks.

## Gotchas hit

- Decoding each chunk separately (`bytes.fromhex(c).decode()`) raises / produces U+FFFD at `c3|a9` and `e2|9c93`.
- Hosting: needs raw JSON, so a static file on Vercel (not a GitHub blob page).

## Verification

`python3 src/reassemble.py data/chunks.json` output equals the record lists in the generator `be()` (A text `Report job-48c9d2a0: café\nReady ✓`).
